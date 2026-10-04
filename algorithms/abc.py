"""Artificial Bee Colony (Karaboga 2005) for discrete CH selection.

Colony of ``colony_size`` bees: half employed, half onlookers. There is one
food source (= one CH configuration) per employed bee, SN = colony_size / 2.

* Employed phase  : each employed bee produces a neighbour v_i of its source
                    x_i and keeps the better one (greedy selection). Failures
                    increment the source's trial counter.
* Onlooker phase  : onlookers pick sources with probability
                    p_i = fit_i / sum(fit),   fit_i = 1 / (1 + F_i)
                    and search their neighbourhood the same way.
* Scout phase     : the source with the most trials is abandoned if
                    trial > limit and replaced by a random configuration.
* The best source ever found is memorised (best-solution preservation).

Neighbour operator (discrete analogue of v_ij = x_ij + phi*(x_ij - x_kj)):
a random partner source x_k is chosen and phi ~ U(-1, 1).

* phi >= 0 and x_i differs from x_k: information sharing -- one CH of x_i
  that x_k does not use is swapped for one CH of x_k that x_i does not use.
* otherwise: local search -- one CH of x_i hands the role to one of its
  nearest eligible non-CH neighbours.
* with probability ``resize_prob`` one CH is added or removed (count
  exploration), always inside [K_min, K_max].

The onlooker phase is synchronous: all onlooker neighbours are generated
from the sources at the start of the phase and evaluated as one batch;
greedy selection is then applied in onlooker order.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from algorithms.base import MetaheuristicSelector, OptResult
from algorithms.fitness import FitnessContext

RESIZE_PROB = 0.1


def pick_true(mask: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Uniformly random True column per row (-1 where a row has none)."""
    r = rng.random(mask.shape)
    r[~mask] = -1.0
    idx = r.argmax(1)
    idx[~mask.any(1)] = -1
    return idx


@dataclass
class BeeColony:
    foods: np.ndarray        # (SN, m) food sources (CH configurations)
    fit: np.ndarray          # (SN,) objective values (lower = better)
    trial: np.ndarray        # (SN,) consecutive failed improvement attempts
    limit: int
    best: np.ndarray
    best_fit: float

    @classmethod
    def create(cls, ctx: FitnessContext, rng: np.random.Generator, n_sources: int, limit: int,
               init: np.ndarray | None = None) -> "BeeColony":
        foods = ctx.random_solutions(n_sources, rng)
        if init is not None and len(init):
            n = min(len(init), n_sources)
            foods[:n] = init[:n]
        fit = ctx.evaluate(foods)
        b = int(np.argmin(fit))
        return cls(foods, fit, np.zeros(n_sources, dtype=int), limit, foods[b].copy(), float(fit[b]))

    @property
    def n_sources(self) -> int:
        return len(self.foods)

    # ------------------------------------------------------------ operators
    def neighbours(self, ctx: FitnessContext, rng: np.random.Generator, idx: np.ndarray) -> np.ndarray:
        S = len(idx)
        X = self.foods[idx]
        V = X.copy()
        rows = np.arange(S)
        if self.n_sources > 1:
            partner = (idx + rng.integers(1, self.n_sources, size=S)) % self.n_sources
        else:
            partner = idx
        Pk = self.foods[partner]
        phi = rng.uniform(-1.0, 1.0, size=S)

        out_i = pick_true(X & ~Pk, rng)       # my CH the partner does not use
        in_i = pick_true(Pk & ~X, rng)        # partner's CH I do not use
        share = (phi >= 0) & (out_i >= 0) & (in_i >= 0)
        V[rows[share], out_i[share]] = False
        V[rows[share], in_i[share]] = True

        loc = rows[~share]
        if len(loc):
            c = pick_true(X[loc], rng)
            has = c >= 0
            loc, c = loc[has], c[has]
            nb = ctx.neighbours[c]                         # (len, L) nearest neighbours
            free = ~X[loc[:, None], nb] & ctx.eligible[nb]
            j = pick_true(free, rng)
            ok = j >= 0
            new = nb[np.arange(len(loc)), np.maximum(j, 0)]
            V[loc[ok], c[ok]] = False
            V[loc[ok], new[ok]] = True

        resize = rng.random(S) < RESIZE_PROB
        if resize.any():
            K = V.sum(1)
            grow = resize & (rng.random(S) < 0.5) & (K < ctx.k_max)
            shrink = resize & ~grow & (K > ctx.k_min)
            g = rows[grow]
            add = pick_true(~V[g] & ctx.eligible, rng)
            V[g[add >= 0], add[add >= 0]] = True
            s = rows[shrink]
            drop = pick_true(V[s], rng)
            V[s[drop >= 0], drop[drop >= 0]] = False
        return ctx.repair(V, rng=rng)

    def _memorise(self) -> None:
        b = int(np.argmin(self.fit))
        if self.fit[b] < self.best_fit:
            self.best, self.best_fit = self.foods[b].copy(), float(self.fit[b])

    def employed_phase(self, ctx: FitnessContext, rng: np.random.Generator) -> None:
        idx = np.arange(self.n_sources)
        V = self.neighbours(ctx, rng, idx)
        fv = ctx.evaluate(V)
        better = fv < self.fit
        self.foods[better], self.fit[better] = V[better], fv[better]
        self.trial[better] = 0
        self.trial[~better] += 1
        self._memorise()

    def selection_probabilities(self) -> np.ndarray:
        q = 1.0 / (1.0 + self.fit)
        return q / q.sum()

    def onlooker_phase(self, ctx: FitnessContext, rng: np.random.Generator) -> None:
        chosen = rng.choice(self.n_sources, size=self.n_sources, p=self.selection_probabilities())
        V = self.neighbours(ctx, rng, chosen)
        fv = ctx.evaluate(V)
        for j, i in enumerate(chosen):
            if fv[j] < self.fit[i]:
                self.foods[i], self.fit[i], self.trial[i] = V[j], fv[j], 0
            else:
                self.trial[i] += 1
        self._memorise()

    def scout_phase(self, ctx: FitnessContext, rng: np.random.Generator) -> bool:
        i = int(np.argmax(self.trial))
        if self.trial[i] <= self.limit:
            return False
        self.foods[i] = ctx.random_solutions(1, rng)[0]
        self.fit[i] = ctx.evaluate(self.foods[i][None, :])[0]
        self.trial[i] = 0
        self._memorise()
        return True

    def iterate(self, ctx: FitnessContext, rng: np.random.Generator) -> None:
        self.employed_phase(ctx, rng)
        self.onlooker_phase(ctx, rng)
        self.scout_phase(ctx, rng)

    def inject(self, X: np.ndarray, fx: np.ndarray) -> int:
        """Replace the worst sources by better external solutions (no duplicates). Returns #accepted."""
        accepted = 0
        for x, f in zip(X, fx):
            if (self.foods == x).all(1).any():
                continue
            w = int(np.argmax(self.fit))
            if f < self.fit[w]:
                self.foods[w], self.fit[w], self.trial[w] = x, f, 0
                accepted += 1
        self._memorise()
        return accepted

    def ranked_sources(self) -> np.ndarray:
        return self.foods[np.argsort(self.fit, kind="stable")]


class ArtificialBeeColony:
    def __init__(self, colony_size: int, limit: int, iterations: int):
        self.n_sources = max(2, colony_size // 2)
        self.limit = limit
        self.iterations = iterations

    def run(self, ctx: FitnessContext, rng: np.random.Generator, iterations: int | None = None,
            init: np.ndarray | None = None) -> tuple[BeeColony, list[float]]:
        T = self.iterations if iterations is None else iterations
        colony = BeeColony.create(ctx, rng, self.n_sources, self.limit, init)
        curve = [colony.best_fit]
        for _ in range(T):
            colony.iterate(ctx, rng)
            curve.append(colony.best_fit)
        return colony, curve

    def optimize(self, ctx: FitnessContext, rng: np.random.Generator) -> OptResult:
        colony, curve = self.run(ctx, rng)
        return OptResult(colony.best.copy(), colony.best_fit, {"abc": curve})


def make_abc(config, seed=None, weights=None) -> MetaheuristicSelector:
    opt = ArtificialBeeColony(config.abc.colony_size, config.abc.limit, config.opt_iterations)
    return MetaheuristicSelector(config, opt, "ABC", seed, weights)
