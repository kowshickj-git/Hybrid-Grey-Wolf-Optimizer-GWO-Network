"""Base paper ("existing system"): DEAI-PSO cluster-head selection.

M. Haris and H. Nam, "Enhancing Energy Efficiency in IoT-WSNs Through Optimized PSO Cluster Head
Selection", IEEE Access, vol. 13, pp. 126496-126512, 2025, doi:10.1109/ACCESS.2025.3583922.

Re-implemented from the paper so that it can be compared with the proposed Hybrid GWO-ABC under
identical conditions:

* Particle = coordinates of K = p * n candidate CHs (p = 10 % in the paper); each coordinate is
  decoded to the nearest *eligible* node (residual energy >= mean, as in PSO-C, the paper's ref. [41])
  that is not already used, so a particle always yields K distinct CHs.
* Velocity / position (Eqs. 8-9):  V = w V + c_p r1 (Pbest - X) + c_g r2 (Gbest - X),  X = X + V
* Time-varying acceleration coefficients (Eqs. 10-11): c = (c_f - c_i) * k / T + c_i
* Double-exponential adaptive inertia (Eq. 13): w_i = exp(-exp(-d(X_i, Pbest_i) * (T - k)))
* Fitness (Eq. 12, minimised):
      F = a * sum_i E_t(N_i) + (1 - a) * n * sqrt( 1/(n-1) * sum_i (R_t(N_i) - mean R_t)^2 )
  E_t(N_i): predicted energy node i spends this round (member TX, CH RX + aggregation + TX to the BS,
  or direct TX for free nodes); R_t(N_i): its residual energy after the round; n: alive nodes.
* Free nodes (three-tier model): alive nodes within ``free_node_radius`` of the BS send directly to it.

Details the paper does not specify are configurable (``DEAIPSOConfig``) and were tuned in the
baseline's favour on development seeds (see results/base_paper/dev_pilot): the weight ``a``, the
TVAC ranges, the velocity clamp and the units of d in Eq. 13. The paper used 36 particles and 5000
iterations in MATLAB; here every optimiser gets the same number of fitness evaluations per round.
"""
from __future__ import annotations

import numpy as np

from algorithms.base import CHSelector, OptResult, Selection, free_nodes
from algorithms.fitness import FitnessContext
from config import SimulationConfig
from models.network import Network


class PaperFitness:
    """Eq. 12 of the base paper, vectorised over P candidate CH sets (binary over ctx's nodes)."""

    def __init__(self, ctx: FitnessContext, network: Network, free: np.ndarray, a: float):
        self.ctx, self.a = ctx, a
        em, k = ctx.em, ctx.k
        free = np.asarray(free, dtype=int)
        self.E_free = network.energy[free]
        self.cost_free = np.atleast_1d(em.tx_energy(k, network.dist_to_bs[free])) if len(free) else np.zeros(0)
        self.n = ctx.m + len(free)
        self.evaluations = 0

    def node_costs(self, X) -> np.ndarray:
        """Predicted energy of every clusterable node for each solution, shape (P, m)."""
        ctx = self.ctx
        X = np.atleast_2d(np.asarray(X, dtype=bool))
        P, m = X.shape
        K = X.sum(1)
        kc = max(1, int(K.max()))
        slot_ok = np.arange(kc)[None, :] < K[:, None]
        heads = np.where(slot_ok, np.argsort(~X, axis=1, kind="stable")[:, :kc], m)
        d = ctx._D_pad[heads]                                    # (P, kc, m)
        nearest, dmin = d.argmin(1), d.min(1)
        has_ch = K > 0
        dmin = np.where(has_ch[:, None], dmin, ctx.d_bs[None, :])  # no CH: everybody sends directly
        cost = np.atleast_1d(ctx.em.tx_energy(ctx.k, dmin)).reshape(P, m) * ~X
        flat = (nearest + np.arange(P)[:, None] * kc).ravel()
        members = np.bincount(flat, minlength=P * kc).reshape(P, kc) - 1
        ch_cost = (members * ctx.rx_da + ctx.da + ctx._chtx_pad[heads]) * slot_ok
        padded = np.zeros((P, m + 1))
        np.put_along_axis(padded, heads, ch_cost, axis=1)        # CH nodes: their own load
        return cost + padded[:, :m]

    def evaluate(self, X) -> np.ndarray:
        X = np.atleast_2d(np.asarray(X, dtype=bool))
        self.evaluations += len(X)
        self.ctx.evaluations += len(X)
        cost = self.node_costs(X)
        total = cost.sum(1) + self.cost_free.sum()
        R = np.concatenate([self.ctx.E[None, :] - cost,
                            np.broadcast_to(self.E_free - self.cost_free, (len(X), len(self.E_free)))], axis=1)
        std = R.std(axis=1, ddof=1) if self.n > 1 else np.zeros(len(X))
        return self.a * total + (1 - self.a) * self.n * std


def deai_inertia(d: np.ndarray, k: int, T: int) -> np.ndarray:
    """Eq. 13: w = exp(-exp(-d * (T - k)))."""
    return np.exp(-np.exp(-np.asarray(d, dtype=float) * (T - k)))


def tvac(k: int, T: int, c_i: float, c_f: float) -> float:
    """Eqs. 10-11: time-varying acceleration coefficient."""
    return (c_f - c_i) * k / max(T, 1) + c_i


class DEAIPSO:
    """PSO with double-exponential adaptive inertia over K CH coordinates."""

    def __init__(self, particles: int, iterations: int, a: float = 0.5, cp=(2.5, 0.5), cg=(0.5, 2.5),
                 vmax_frac: float = 0.2, normalise_distance: bool = True, objective: str = "paper"):
        self.particles, self.iterations, self.a = particles, iterations, a
        self.cp, self.cg = cp, cg
        self.vmax_frac, self.normalise = vmax_frac, normalise_distance
        if objective not in ("paper", "proposed"):
            raise ValueError(objective)
        self.objective = objective

    @classmethod
    def from_config(cls, config: SimulationConfig, objective: str = "paper") -> "DEAIPSO":
        c = config.deai_pso
        iters = c.iterations or max(1, int(round(config.opt_iterations * config.gwo.population / c.particles)))
        return cls(c.particles, iters, c.a, (c.cp_i, c.cp_f), (c.cg_i, c.cg_f), c.vmax_frac,
                   c.normalise_distance, objective)

    # ------------------------------------------------------------------ decoding
    @staticmethod
    def decode(ctx: FitnessContext, positions: np.ndarray, node_xy: np.ndarray) -> np.ndarray:
        """(P, K, 2) coordinates -> (P, m) binary CH sets: nearest eligible, not-yet-used node per coordinate."""
        P, K, _ = positions.shape
        cand = np.flatnonzero(ctx.eligible)
        X = np.zeros((P, ctx.m), dtype=bool)
        d = np.linalg.norm(positions[:, :, None, :] - node_xy[cand][None, None, :, :], axis=3)   # (P, K, c)
        taken = np.zeros((P, len(cand)), dtype=bool)
        rows = np.arange(P)
        for j in range(min(K, len(cand))):
            dj = np.where(taken, np.inf, d[:, j, :])
            pick = dj.argmin(1)
            taken[rows, pick] = True
        X[:, cand] = taken
        return X

    # ------------------------------------------------------------------ search
    def optimize(self, ctx: FitnessContext, rng: np.random.Generator, network: Network, free: np.ndarray,
                 area: tuple) -> OptResult:
        W, H = area
        K = max(1, min(ctx.k_opt, ctx.n_eligible))
        node_xy = network.positions[ctx.ids]
        if self.objective == "paper":
            score = PaperFitness(ctx, network, free, self.a).evaluate
        else:
            score = ctx.evaluate
        P, T = self.particles, self.iterations
        lo, hi = np.zeros(2), np.array([W, H], dtype=float)
        vmax = self.vmax_frac * hi
        dist_scale = np.sqrt(K) * float(np.hypot(W, H)) if self.normalise else 1.0

        X = rng.uniform(lo, hi, size=(P, K, 2))
        V = np.zeros_like(X)
        bits = self.decode(ctx, X, node_xy)
        fit = score(bits)
        pbest, pbest_fit, pbest_bits = X.copy(), fit.copy(), bits.copy()
        g = int(np.argmin(fit))
        gbest, gbest_fit, gbest_bits = X[g].copy(), float(fit[g]), bits[g].copy()
        curve = [gbest_fit]

        for k in range(T):
            cp = tvac(k, T, *self.cp)
            cg = tvac(k, T, *self.cg)
            d = np.linalg.norm((X - pbest).reshape(P, -1), axis=1) / dist_scale
            w = deai_inertia(d, k, T)[:, None, None]
            r1, r2 = rng.random(X.shape), rng.random(X.shape)
            V = w * V + cp * r1 * (pbest - X) + cg * r2 * (gbest[None] - X)
            V = np.clip(V, -vmax, vmax)
            X = np.clip(X + V, lo, hi)
            bits = self.decode(ctx, X, node_xy)
            fit = score(bits)
            better = fit < pbest_fit
            pbest[better], pbest_fit[better], pbest_bits[better] = X[better], fit[better], bits[better]
            g = int(np.argmin(pbest_fit))
            if pbest_fit[g] < gbest_fit:
                gbest, gbest_fit, gbest_bits = pbest[g].copy(), float(pbest_fit[g]), pbest_bits[g].copy()
            curve.append(gbest_fit)
        return OptResult(gbest_bits, gbest_fit, {"deai_pso": curve}, {"K": K, "objective": self.objective})


class _PaperObjectiveView:
    """FitnessContext whose ``evaluate`` is the base paper's Eq. 12 (used for the attribution study)."""

    def __init__(self, ctx: FitnessContext, paper: PaperFitness):
        self._ctx, self._paper = ctx, paper

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def evaluate(self, X):
        return self._paper.evaluate(X)


class PaperObjectiveSelector(CHSelector):
    """Any of our optimisers driven by the base paper's objective (Eq. 12) instead of ours."""

    def __init__(self, config: SimulationConfig, optimizer, name: str, seed: int | None = None):
        super().__init__(config, seed)
        self.optimizer, self.name = optimizer, name

    def select(self, network: Network, round_no: int) -> Selection:
        free = free_nodes(network, self.config.free_node_radius)
        ctx = FitnessContext(network, self.config, exclude=free)
        if ctx.m == 0:
            return Selection(np.array([], dtype=int), direct=free)
        paper = PaperFitness(ctx, network, free, self.config.deai_pso.a)
        res = self.optimizer.optimize(_PaperObjectiveView(ctx, paper), self.rng)
        return Selection(ctx.to_node_ids(res.best), None, ctx.evaluations, res.curves, direct=free)


class DEAIPSOSelector(CHSelector):
    """Base paper's centralised CH selection (runs at the BS every round)."""

    name = "DEAI-PSO"

    def __init__(self, config: SimulationConfig, seed: int | None = None, objective: str = "paper"):
        super().__init__(config, seed)
        self.optimizer = DEAIPSO.from_config(config, objective)

    def select(self, network: Network, round_no: int) -> Selection:
        free = free_nodes(network, self.config.free_node_radius)
        ctx = FitnessContext(network, self.config, exclude=free)
        if ctx.m == 0:
            return Selection(np.array([], dtype=int), direct=free)
        res = self.optimizer.optimize(ctx, self.rng, network, free, network.area)
        # fitness None: the simulator scores the CH set with the common objective, as for every algorithm
        return Selection(ctx.to_node_ids(res.best), None, ctx.evaluations, res.curves, direct=free)
