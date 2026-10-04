"""Wireless sensor network: deployment, node state and base station."""
from __future__ import annotations

import copy

import numpy as np
import pandas as pd

from config import SimulationConfig
from models.node import SensorNode


class Network:
    def __init__(self, positions, initial_energy, bs_position, area):
        self.positions = np.asarray(positions, dtype=float)
        n = len(self.positions)
        self.n = n
        self.area = (float(area[0]), float(area[1]))
        self.bs = np.asarray(bs_position, dtype=float)
        self.initial_energy = np.broadcast_to(np.asarray(initial_energy, dtype=float), (n,)).copy()
        diff = self.positions[:, None, :] - self.positions[None, :, :]
        self.distances = np.sqrt((diff ** 2).sum(-1))          # (n, n) node-node
        self.dist_to_bs = np.linalg.norm(self.positions - self.bs, axis=1)
        self.reset()

    # ------------------------------------------------------------ construction
    @classmethod
    def deploy(cls, config: SimulationConfig, seed: int | None = None) -> "Network":
        """Uniform random deployment inside the area (reproducible via ``seed``)."""
        rng = np.random.default_rng(config.seed if seed is None else seed)
        pos = rng.uniform([0, 0], [config.area_width, config.area_height], size=(config.n_nodes, 2))
        return cls(pos, config.initial_energy, (config.bs_x, config.bs_y),
                   (config.area_width, config.area_height))

    def reset(self) -> None:
        """Restore every node to its initial state."""
        n = self.n
        self.energy = self.initial_energy.copy()
        self.alive = np.ones(n, dtype=bool)
        self.is_ch = np.zeros(n, dtype=bool)
        self.cluster_id = np.full(n, -1, dtype=int)
        self.dist_to_ch = np.full(n, np.nan)
        self.pkt_generated = np.zeros(n, dtype=np.int64)
        self.pkt_transmitted = np.zeros(n, dtype=np.int64)
        self.pkt_received = np.zeros(n, dtype=np.int64)
        self.death_round = np.full(n, -1, dtype=int)
        self.nodes = [SensorNode(self, i) for i in range(n)]

    def copy(self) -> "Network":
        """Independent copy (used so every algorithm starts from the identical network)."""
        new = copy.copy(self)
        for name in ("positions", "bs", "initial_energy", "energy", "alive", "is_ch", "cluster_id",
                     "dist_to_ch", "pkt_generated", "pkt_transmitted", "pkt_received", "death_round"):
            setattr(new, name, getattr(self, name).copy())
        new.distances = self.distances          # immutable, safe to share
        new.dist_to_bs = self.dist_to_bs
        new.nodes = [SensorNode(new, i) for i in range(new.n)]
        return new

    # ------------------------------------------------------------- state
    @property
    def alive_indices(self) -> np.ndarray:
        return np.flatnonzero(self.alive)

    @property
    def n_alive(self) -> int:
        return int(self.alive.sum())

    @property
    def total_energy(self) -> float:
        return float(self.energy.sum())

    @property
    def total_initial_energy(self) -> float:
        return float(self.initial_energy.sum())

    def clear_round_state(self) -> None:
        self.is_ch[:] = False
        self.cluster_id[:] = -1
        self.dist_to_ch[:] = np.nan

    def detect_dead(self, round_no: int) -> np.ndarray:
        """Mark nodes whose residual energy reached zero as DEAD. Returns newly dead ids."""
        self.energy[self.energy < 0] = 0.0
        newly_dead = np.flatnonzero(self.alive & (self.energy <= 0.0))
        self.alive[newly_dead] = False
        self.death_round[newly_dead] = round_no
        return newly_dead

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([node.as_dict() for node in self.nodes])
