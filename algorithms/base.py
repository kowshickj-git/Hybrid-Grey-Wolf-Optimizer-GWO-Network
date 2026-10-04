"""Common interface of every cluster-head selection algorithm."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from algorithms.fitness import FitnessContext
from config import FitnessWeights, SimulationConfig
from models.network import Network


@dataclass
class Selection:
    """Outcome of CH selection for one round."""

    ch: np.ndarray                     # selected CH node ids
    fitness: float | None = None       # fitness of the CH set (None -> simulator evaluates it)
    evaluations: int = 0               # fitness evaluations spent selecting it
    curves: dict = field(default_factory=dict)  # name -> best-so-far fitness per iteration
    direct: np.ndarray | None = None   # free nodes: send straight to the BS, not clustered (base paper)


@dataclass
class OptResult:
    best: np.ndarray                   # best binary solution over alive nodes
    fitness: float
    curves: dict                       # e.g. {"gwo": [...]} (index 0 = initial population)
    info: dict = field(default_factory=dict)


class CHSelector:
    """Base class. ``select`` is called once per round with the live network."""

    name = "base"
    centralized = True                 # CH set computed at the BS (affects control overhead only)

    def __init__(self, config: SimulationConfig, seed: int | None = None):
        self.config = config
        self.rng = np.random.default_rng(config.seed if seed is None else seed)

    def reset(self, network: Network) -> None:
        """Called once before round 1."""

    def select(self, network: Network, round_no: int) -> Selection:  # pragma: no cover
        raise NotImplementedError


class MetaheuristicSelector(CHSelector):
    """Runs an optimiser over the current round's FitnessContext and returns its best CH set."""

    def __init__(self, config: SimulationConfig, optimizer, name: str, seed: int | None = None,
                 weights: FitnessWeights | None = None):
        super().__init__(config, seed)
        self.optimizer = optimizer
        self.name = name
        self.weights = weights            # None -> config.weights

    def select(self, network: Network, round_no: int) -> Selection:
        free = free_nodes(network, self.config.free_node_radius)
        ctx = FitnessContext(network, self.config, self.weights, exclude=free)
        if ctx.m == 0:
            return Selection(np.array([], dtype=int), direct=free)
        res = self.optimizer.optimize(ctx, self.rng)
        # custom (ablation) weights or free nodes change the scored node set, so the simulator
        # re-scores the CH set with the standard objective over all alive nodes (same as for LEACH)
        fitness = res.fitness if self.weights is None and len(free) == 0 else None
        return Selection(ctx.to_node_ids(res.best), fitness, ctx.evaluations, res.curves, direct=free)


def free_nodes(network: Network, radius: float) -> np.ndarray:
    """Base paper's free nodes: alive nodes closer than ``radius`` to the BS (empty when radius <= 0)."""
    if radius <= 0:
        return np.array([], dtype=int)
    return np.flatnonzero(network.alive & (network.dist_to_bs < radius))


class RandomSelector(CHSelector):
    """Baseline: K_opt alive nodes chosen uniformly at random each round."""

    name = "Random"

    def select(self, network: Network, round_no: int) -> Selection:
        ctx = FitnessContext(network, self.config)
        if ctx.m == 0:
            return Selection(np.array([], dtype=int))
        x = np.zeros(ctx.m, dtype=bool)
        x[self.rng.choice(ctx.m, size=ctx.k_opt, replace=False)] = True
        return Selection(ctx.to_node_ids(x))
