"""Proposed Hybrid GWO-ABC (co-evolutionary, bidirectional exchange every iteration).

    initialise wolf pack (GWO) and food sources (ABC) with valid CH sets
    for t = 1..T:
        1. GWO global exploration  : every wolf moves w.r.t. alpha/beta/delta
        2. GWO -> ABC transfer     : alpha, beta, delta replace the worst food
                                     sources when better and not duplicates
                                     (elite GWO solutions are preserved in ABC)
        3. ABC employed bees       : refine every source (incl. the GWO elites)
        4. ABC onlooker bees       : exploit the most promising sources
        5. ABC scout bees          : re-seed an exhausted source (exploration)
        6. ABC -> GWO feedback     : if the ABC best beats the pack's delta it
                                     replaces the worst wolf and joins the
                                     leader set, so it steers the next GWO move
        7. elite preservation      : global best = min(alpha, ABC best)

Budget fairness: the pack has ``gwo.population * budget_share`` wolves and
the colony ``abc.colony_size * budget_share`` bees, so with the default
share 0.5 the hybrid spends the same number of fitness evaluations per
iteration as standalone GWO or ABC.

Sequential variants (ablation study) split the iterations in two halves:
``GWO->ABC`` runs GWO, then seeds ABC with the best wolves; ``ABC->GWO`` does
the reverse. They use the full standalone population sizes.
"""
from __future__ import annotations

import numpy as np

from algorithms.abc import ArtificialBeeColony, BeeColony
from algorithms.base import MetaheuristicSelector, OptResult
from algorithms.fitness import FitnessContext
from algorithms.gwo import GreyWolfOptimizer, WolfPack, control_parameter, distinct_best


class HybridGWOABC:
    def __init__(self, n_wolves: int, n_sources: int, limit: int, iterations: int,
                 transfer_size: int = 3, feedback: bool = True):
        self.n_wolves = max(3, n_wolves)
        self.n_sources = max(2, n_sources)
        self.limit = limit
        self.iterations = iterations
        self.transfer_size = transfer_size
        self.feedback = feedback

    @classmethod
    def from_config(cls, config) -> "HybridGWOABC":
        h = config.hybrid
        wolves = int(round(config.gwo.population * h.budget_share))
        sources = int(round(config.abc.colony_size * h.budget_share)) // 2
        return cls(wolves, sources, config.abc.limit, config.opt_iterations, h.transfer_size, h.feedback)

    def optimize(self, ctx: FitnessContext, rng: np.random.Generator) -> OptResult:
        T = self.iterations
        pack = WolfPack.create(ctx, rng, self.n_wolves)
        colony = BeeColony.create(ctx, rng, self.n_sources, self.limit)
        best, best_fit = self._elite(pack, colony)
        curves = {"gwo": [pack.best_fit], "abc": [colony.best_fit], "hybrid": [best_fit]}
        transfers = feedbacks = 0

        for t in range(T):
            pack.step(ctx, rng, control_parameter(t, T))                     # 1
            k = self.transfer_size
            transfers += colony.inject(pack.leaders[:k], pack.leader_fit[:k])  # 2
            colony.employed_phase(ctx, rng)                                  # 3
            colony.onlooker_phase(ctx, rng)                                  # 4
            colony.scout_phase(ctx, rng)                                     # 5
            if self.feedback and colony.best_fit < pack.leader_fit[-1]:      # 6
                if not (pack.leaders == colony.best).all(1).any():
                    pack.absorb(colony.best.copy(), colony.best_fit)
                    feedbacks += 1
            best, best_fit = self._elite(pack, colony, best, best_fit)         # 7
            curves["gwo"].append(pack.best_fit)
            curves["abc"].append(colony.best_fit)
            curves["hybrid"].append(best_fit)

        return OptResult(best, best_fit, curves, {"transfers": transfers, "feedbacks": feedbacks})

    @staticmethod
    def _elite(pack: WolfPack, colony: BeeColony, best=None, best_fit=np.inf):
        for x, f in ((pack.alpha, pack.best_fit), (colony.best, colony.best_fit)):
            if f < best_fit:
                best, best_fit = x.copy(), float(f)
        return best, best_fit


class SequentialHybrid:
    """Two-stage hybrids used in the ablation study (``order`` = 'gwo_abc' or 'abc_gwo')."""

    def __init__(self, gwo: GreyWolfOptimizer, abc: ArtificialBeeColony, iterations: int, order: str):
        if order not in ("gwo_abc", "abc_gwo"):
            raise ValueError(order)
        self.gwo, self.abc, self.iterations, self.order = gwo, abc, iterations, order

    def optimize(self, ctx: FitnessContext, rng: np.random.Generator) -> OptResult:
        t1 = self.iterations // 2
        t2 = self.iterations - t1
        if self.order == "gwo_abc":
            pack, c1 = self.gwo.run(ctx, rng, t1)
            pool = np.vstack([pack.leaders, pack.X])
            pool_fit = np.concatenate([pack.leader_fit, pack.fit])
            seeds = pool[distinct_best(pool, pool_fit, self.abc.n_sources)]
            colony, c2 = self.abc.run(ctx, rng, t2, init=seeds)
            best, best_fit = colony.best, colony.best_fit
            if pack.best_fit < best_fit:
                best, best_fit = pack.alpha, pack.best_fit
            curves = {"gwo": c1, "abc": c2}
        else:
            colony, c1 = self.abc.run(ctx, rng, t1)
            seeds = np.vstack([colony.best[None, :], colony.ranked_sources()])
            pack, c2 = self.gwo.run(ctx, rng, t2, init=seeds)
            best, best_fit = pack.alpha, pack.best_fit
            if colony.best_fit < best_fit:
                best, best_fit = colony.best, colony.best_fit
            curves = {"abc": c1, "gwo": c2}
        combined = list(np.minimum.accumulate(np.concatenate([curves[k] for k in curves])))
        curves["hybrid"] = combined
        return OptResult(best.copy(), float(best_fit), curves)


def make_hybrid(config, seed=None, weights=None, name: str = "Hybrid GWO-ABC") -> MetaheuristicSelector:
    return MetaheuristicSelector(config, HybridGWOABC.from_config(config), name, seed, weights)


def make_sequential(config, order: str, seed=None, weights=None) -> MetaheuristicSelector:
    gwo = GreyWolfOptimizer(config.gwo.population, config.opt_iterations)
    abc = ArtificialBeeColony(config.abc.colony_size, config.abc.limit, config.opt_iterations)
    name = "GWO->ABC" if order == "gwo_abc" else "ABC->GWO"
    return MetaheuristicSelector(config, SequentialHybrid(gwo, abc, config.opt_iterations, order), name, seed, weights)
