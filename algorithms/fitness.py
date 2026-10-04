"""Multi-objective cluster-head fitness (minimised, lower = better).

A candidate solution is a binary vector over the *alive* nodes of the current
round (dead nodes are excluded from the search space, so they can never be
selected)::

    x = [0, 1, 0, 0, 1, 0, 1, ...]      1 = cluster head, 0 = member

Every alive non-CH node joins its nearest CH. The fitness is

    F(x) = w1*EnergyCost + w2*IntraDist + w3*CH_BS + w4*Imbalance + w5*CountPenalty
           + invalid_penalty * [x is infeasible]

Normalisation (every term lies in [0, 1]):

    EnergyCost   = 0.5 * (1 - mean(E_CH) / max(E_alive))          residual-energy part
                 + 0.5 * E_round(x) / E_upper                       consumption part
                   E_round = predicted radio energy of one round with this clustering
                   E_upper = m * (E_tx(k, d_max) + E_rx(k) + E_DA*k)  (no clustering can exceed it)
    IntraDist    = mean member->CH distance / max alive node-node distance
    CH_BS        = mean CH->BS distance / max alive node->BS distance
    Imbalance    = min(1, coefficient of variation of cluster sizes)
    CountPenalty = min(1, |K - K_opt| / K_opt),   K_opt = round(p * m)

A solution is *infeasible* when it has no CH, its CH count lies outside
[K_min, K_max], or a CH cannot afford its predicted round load (it would die
mid-round and drop its cluster's data). Optimisers repair counts with
``repair``, so the penalty mainly guards the energy-feasibility condition.

CH eligibility (search-space constraint, as in LEACH-C): optimisers only
place CHs on nodes with E >= ch_energy_threshold * mean(E_alive). Without it,
the CH->BS distance term keeps re-electing the nodes nearest to the BS and
drains them far below the network average. ``evaluate`` itself does not
penalise ineligible CHs, so CH sets from any algorithm (e.g. LEACH) are scored
with the same objective.
"""
from __future__ import annotations

import numpy as np

from config import FitnessWeights, SimulationConfig
from models.energy_model import EnergyModel
from models.network import Network

COMPONENTS = ("energy", "intra_distance", "ch_bs_distance", "balance", "ch_count")


def ch_count_bounds(n_alive: int, p: float, tolerance: float) -> tuple[int, int, int]:
    """(K_opt, K_min, K_max) for ``n_alive`` candidates."""
    if n_alive <= 0:
        return 0, 0, 0
    k_opt = max(1, int(np.floor(p * n_alive + 0.5)))
    k_min = max(1, int(np.floor(k_opt * (1 - tolerance))))
    k_max = max(k_min, int(np.ceil(k_opt * (1 + tolerance))))
    return min(k_opt, n_alive), min(k_min, n_alive), min(k_max, n_alive)


class FitnessContext:
    """Snapshot of one round's network state plus a vectorised fitness evaluator."""

    def __init__(self, network: Network, config: SimulationConfig, weights: FitnessWeights | None = None,
                 exclude=None):
        self.config = config
        w = weights or config.weights
        self.weights = np.array([w.energy, w.intra_distance, w.ch_bs_distance, w.balance, w.ch_count])
        self.penalty = config.invalid_penalty

        mask = network.alive.copy()
        if exclude is not None and len(exclude):
            mask[np.asarray(exclude, dtype=int)] = False      # e.g. free nodes: neither CH nor member
        self.ids = np.flatnonzero(mask)                       # alive, clusterable node ids (search space)
        self.m = len(self.ids)
        self.D = network.distances[np.ix_(self.ids, self.ids)]
        self.d_bs = network.dist_to_bs[self.ids]
        self.E = network.energy[self.ids].copy()
        self.k_opt, self.k_min, self.k_max = ch_count_bounds(self.m, config.ch_percentage,
                                                             config.count_tolerance)
        self.score_bounds = (self.k_opt, self.k_min, self.k_max)    # used by the objective
        thr = config.ch_energy_threshold * (self.E.mean() if self.m else 0.0)
        self.eligible = self.E >= thr - 1e-15                  # CH candidates (never empty when m > 0)
        self.n_eligible = int(self.eligible.sum())
        self.k_max = min(self.k_max, self.n_eligible)               # search-space bounds
        self.k_min = min(self.k_min, self.k_max)

        em = EnergyModel(config.energy)
        k = config.packet_bits
        self.em, self.k = em, k
        self.rx_da = em.rx_energy(k) + em.aggregation_energy(k)  # CH cost per member packet
        self.da = em.aggregation_energy(k)                        # CH cost for its own reading
        self.ch_tx = np.atleast_1d(em.tx_energy(k, self.d_bs))    # CH -> BS cost of every node

        self.d_norm = float(self.D.max()) if self.m > 1 and self.D.max() > 0 else 1.0
        self.bs_norm = float(self.d_bs.max()) if self.m and self.d_bs.max() > 0 else 1.0
        self.e_max = float(self.E.max()) if self.m else 1.0
        d_far = max(self.d_norm, self.bs_norm)
        self.e_upper = self.m * (em.tx_energy(k, d_far) + self.rx_da) or 1.0
        # padded copies: index m is a sentinel "no CH" slot (infinitely far, zero cost)
        self._D_pad = np.vstack([self.D, np.full((1, self.m), np.inf)])
        self._dbs_pad = np.append(self.d_bs, 0.0)
        self._chtx_pad = np.append(self.ch_tx, 0.0)
        self._E_pad = np.append(self.E, 0.0)
        self.evaluations = 0
        self._neighbours = None

    # ------------------------------------------------------------ evaluation
    def evaluate(self, X) -> np.ndarray:
        """Fitness of every row of ``X`` (P x m boolean)."""
        return self._evaluate(X)[0]

    def components(self, x) -> dict:
        """Detailed breakdown of a single solution (for reporting/tests)."""
        cost, parts = self._evaluate(np.atleast_2d(x))
        out = {name: float(parts[name][0]) for name in parts}
        out["fitness"] = float(cost[0])
        return out

    def _evaluate(self, X):
        X = np.atleast_2d(np.asarray(X, dtype=bool))
        P, m = X.shape
        self.evaluations += P
        K = X.sum(1)
        kc = max(1, int(K.max()))
        slot_ok = np.arange(kc)[None, :] < K[:, None]                 # (P, kc) real CH slots
        heads = np.argsort(~X, axis=1, kind="stable")[:, :kc]          # CH indices first
        heads = np.where(slot_ok, heads, m)                            # pad -> sentinel index m
        d = self._D_pad[heads]                                         # (P, kc, m), pads = inf
        nearest = d.argmin(1)                                          # (P, m) slot of nearest CH
        dmin = d.min(1)                                                # (P, m)
        member = ~X
        n_mem = member.sum(1)
        has_ch = K > 0
        dmin = np.where(has_ch[:, None], dmin, self.d_bs[None, :])     # no CH -> direct to BS

        # sizes of each cluster (CH counted in its own cluster)
        flat = (nearest + np.arange(P)[:, None] * kc).ravel()
        sizes = np.bincount(flat, minlength=P * kc).reshape(P, kc)
        k_safe = np.maximum(K, 1)

        # --- distance terms
        intra = np.where(n_mem > 0, (dmin * member).sum(1) / np.maximum(n_mem, 1), 0.0) / self.d_norm
        chbs = self._dbs_pad[heads].sum(1) / k_safe / self.bs_norm

        # --- balance
        mean_size = m / k_safe
        var = (((sizes - mean_size[:, None]) ** 2) * slot_ok).sum(1) / k_safe
        imbalance = np.minimum(1.0, np.sqrt(var) / mean_size)

        # --- count
        k_opt, k_lo, k_hi = self.score_bounds
        count = np.minimum(1.0, np.abs(K - k_opt) / max(k_opt, 1))

        # --- energy: predicted consumption of this round + CH residual energy
        member_tx = np.atleast_1d(self.em.tx_energy(self.k, dmin)).reshape(P, m)
        load = sizes - 1                                               # members per CH
        ch_load = (load * self.rx_da + self.da + self._chtx_pad[heads]) * slot_ok   # (P, kc)
        e_round = (member_tx * member).sum(1) + ch_load.sum(1)
        e_heads = self._E_pad[heads]
        e_ch = (e_heads * slot_ok).sum(1) / k_safe
        energy = 0.5 * (1.0 - e_ch / self.e_max) + 0.5 * np.minimum(1.0, e_round / self.e_upper)

        parts = {"energy": energy, "intra_distance": intra, "ch_bs_distance": chbs,
                 "balance": imbalance, "ch_count": count}
        stacked = np.stack([parts[c] for c in COMPONENTS], 1)
        cost = stacked @ self.weights

        starving = ((e_heads < ch_load) & slot_ok).any(1)
        invalid = (~has_ch) | (K < k_lo) | (K > k_hi) | starving
        cost = cost + self.penalty * invalid
        parts["invalid"] = invalid.astype(float)
        return cost, parts

    # ------------------------------------------------------------ helpers
    def random_solutions(self, n: int, rng: np.random.Generator) -> np.ndarray:
        """``n`` random eligible solutions with K uniform in [K_min, K_max]."""
        X = np.zeros((n, self.m), dtype=bool)
        if self.m == 0:
            return X
        K = rng.integers(self.k_min, self.k_max + 1, size=n)
        score = np.where(self.eligible, rng.random((n, self.m)), -1.0)
        ranks = (-score).argsort(1).argsort(1)
        return ranks < K[:, None]

    def repair(self, X, priority=None, rng: np.random.Generator | None = None) -> np.ndarray:
        """Drop ineligible CHs and clip each row's CH count into [K_min, K_max].

        Surplus CHs with the lowest ``priority`` are dropped; missing CHs are
        filled with the highest-priority eligible non-CH nodes (random priority if none).
        """
        X = np.atleast_2d(np.asarray(X, dtype=bool)) & self.eligible
        if self.m == 0:
            return X
        K = X.sum(1)
        target = np.clip(K, self.k_min, self.k_max)
        if np.all(target == K):
            return X
        if priority is None:
            priority = (rng or np.random.default_rng()).random(X.shape)
        p = np.asarray(priority, dtype=float)
        p = (p - p.min()) / (np.ptp(p) + 1e-12)                    # into [0, 1]
        score = np.where(self.eligible, X * 2.0 + p, -1.0)          # existing CHs first, ineligible last
        rank = (-score).argsort(1).argsort(1)
        return rank < target[:, None]

    @property
    def neighbours(self) -> np.ndarray:
        """Nearest alive neighbours of every node (excluding itself), used by ABC local moves."""
        if self._neighbours is None:
            L = max(1, min(self.m - 1, int(np.ceil(self.m / max(self.k_opt, 1)))))
            if self.m <= 1:
                self._neighbours = np.zeros((self.m, 1), dtype=int)
            else:
                order = np.argsort(self.D, axis=1)[:, 1:L + 1]
                self._neighbours = order
        return self._neighbours

    def to_node_ids(self, x) -> np.ndarray:
        """Map a solution vector to network node ids."""
        return self.ids[np.asarray(x, dtype=bool)]

    def from_node_ids(self, ch_ids) -> np.ndarray:
        """Binary vector (over alive nodes) for a set of network node ids."""
        return np.isin(self.ids, np.asarray(ch_ids, dtype=int))
