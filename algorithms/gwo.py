"""Binary Grey Wolf Optimizer (Mirjalili et al. 2014; binary form after Emary et al. 2016).

Social hierarchy: alpha, beta and delta are the three best *distinct*
solutions found so far; every other wolf is an omega that follows them.

Encircling / hunting, for each leader L in {alpha, beta, delta} and wolf X:

    A = 2a*r1 - a,   C = 2*r2,         r1, r2 ~ U(0, 1) per dimension
    D_L = |C * L - X|
    X_L = L - A * D_L
    Y   = (X_alpha + X_beta + X_delta) / 3                  (continuous step)

``a`` decreases linearly from 2 to 0. While |A| > 1 wolves are pushed away
from the leaders (exploration); when |A| < 1 they close in on them
(exploitation).

Discretisation: the continuous step is mapped to a probability with the
sigmoid transfer S(y) = 1 / (1 + exp(-10 (y - 0.5))) and bit j becomes 1
(node j is a CH) with probability S(y_j). The CH count is then repaired into
[K_min, K_max], keeping/adding the nodes with the highest S(y_j).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from algorithms.base import MetaheuristicSelector, OptResult
from algorithms.fitness import FitnessContext

N_LEADERS = 3


def sigmoid_transfer(y: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-10.0 * (y - 0.5)))


def distinct_best(X: np.ndarray, fit: np.ndarray, k: int) -> np.ndarray:
    """Indices of the ``k`` best rows of ``X`` that are pairwise different."""
    chosen: list[int] = []
    for i in np.argsort(fit, kind="stable"):
        if not chosen or not (X[chosen] == X[i]).all(1).any():
            chosen.append(int(i))
            if len(chosen) == k:
                break
    while len(chosen) < k:                  # fewer than k distinct solutions exist
        chosen.append(chosen[-1])
    return np.array(chosen)


@dataclass
class WolfPack:
    X: np.ndarray            # (P, m) binary wolf positions
    fit: np.ndarray          # (P,)
    leaders: np.ndarray      # (3, m) alpha, beta, delta
    leader_fit: np.ndarray   # (3,)

    @classmethod
    def create(cls, ctx: FitnessContext, rng: np.random.Generator, size: int,
               init: np.ndarray | None = None) -> "WolfPack":
        X = ctx.random_solutions(size, rng)
        if init is not None and len(init):
            n = min(len(init), size)
            X[:n] = init[:n]
        fit = ctx.evaluate(X)
        pack = cls(X, fit, X[:0].copy(), np.empty(0))
        pack.update_leaders(X, fit)
        return pack

    @property
    def alpha(self) -> np.ndarray:
        return self.leaders[0]

    @property
    def best_fit(self) -> float:
        return float(self.leader_fit[0])

    def update_leaders(self, X: np.ndarray, fit: np.ndarray) -> None:
        """Alpha/beta/delta = best three distinct solutions seen so far (elitist)."""
        pool = np.vstack([self.leaders, X]) if len(self.leaders) else X
        pool_fit = np.concatenate([self.leader_fit, fit]) if len(self.leaders) else fit
        idx = distinct_best(pool, pool_fit, N_LEADERS)
        self.leaders, self.leader_fit = pool[idx].copy(), pool_fit[idx].copy()

    def step(self, ctx: FitnessContext, rng: np.random.Generator, a: float) -> None:
        """One GWO iteration: every wolf moves w.r.t. alpha, beta, delta."""
        P, m = self.X.shape
        X = self.X.astype(float)
        Y = np.zeros((P, m))
        for L in self.leaders.astype(float):
            A = 2.0 * a * rng.random((P, m)) - a
            C = 2.0 * rng.random((P, m))
            Y += L - A * np.abs(C * L - X)
        prob = sigmoid_transfer(Y / N_LEADERS)
        X_new = ctx.repair(rng.random((P, m)) < prob, priority=prob)
        self.X = X_new
        self.fit = ctx.evaluate(X_new)
        self.update_leaders(X_new, self.fit)

    def absorb(self, x: np.ndarray, fx: float) -> None:
        """Replace the worst wolf by an external solution (used by the hybrid)."""
        worst = int(np.argmax(self.fit))
        self.X[worst], self.fit[worst] = x, fx
        self.update_leaders(x[None, :], np.array([fx]))


def control_parameter(t: int, iterations: int) -> float:
    """a(t): linear decrease 2 -> 0 over the run."""
    return 2.0 - 2.0 * t / max(iterations, 1)


class GreyWolfOptimizer:
    def __init__(self, population: int, iterations: int):
        self.population = population
        self.iterations = iterations

    def run(self, ctx: FitnessContext, rng: np.random.Generator, iterations: int | None = None,
            init: np.ndarray | None = None) -> tuple[WolfPack, list[float]]:
        T = self.iterations if iterations is None else iterations
        pack = WolfPack.create(ctx, rng, self.population, init)
        curve = [pack.best_fit]
        for t in range(T):
            pack.step(ctx, rng, control_parameter(t, T))
            curve.append(pack.best_fit)
        return pack, curve

    def optimize(self, ctx: FitnessContext, rng: np.random.Generator) -> OptResult:
        pack, curve = self.run(ctx, rng)
        return OptResult(pack.alpha.copy(), pack.best_fit, {"gwo": curve})


def make_gwo(config, seed=None, weights=None) -> MetaheuristicSelector:
    opt = GreyWolfOptimizer(config.gwo.population, config.opt_iterations)
    return MetaheuristicSelector(config, opt, "GWO", seed, weights)
