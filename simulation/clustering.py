"""Cluster-head validation and cluster formation."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from models.network import Network


@dataclass
class ClusterState:
    ch: np.ndarray            # CH node ids
    members: np.ndarray       # alive non-CH node ids assigned to a CH
    member_slot: np.ndarray   # index into ``ch`` for every member
    member_dist: np.ndarray   # member -> CH distance (m)
    unclustered: np.ndarray   # alive non-CH nodes sending directly to the BS (free nodes, or no CH available)
    sizes: np.ndarray         # nodes per cluster, CH included

    @property
    def n_clusters(self) -> int:
        return len(self.ch)

    @property
    def avg_distance(self) -> float:
        """Mean member -> CH distance (NaN when there are no members)."""
        return float(self.member_dist.mean()) if len(self.member_dist) else float("nan")

    @property
    def max_distance(self) -> float:
        return float(self.member_dist.max()) if len(self.member_dist) else float("nan")

    @property
    def imbalance(self) -> float:
        """Coefficient of variation of cluster sizes (0 = perfectly balanced)."""
        if len(self.sizes) < 2:
            return 0.0
        return float(self.sizes.std() / self.sizes.mean())


def validate_cluster_heads(network: Network, ch) -> np.ndarray:
    """Drop dead nodes and duplicates from a CH selection."""
    ch = np.unique(np.asarray(ch, dtype=int).ravel())
    ch = ch[(ch >= 0) & (ch < network.n)]
    return ch[network.alive[ch]]


def form_clusters(network: Network, ch, direct=None) -> ClusterState:
    """Assign every alive non-CH node to its nearest CH (strongest received advertisement).

    Dead nodes are never assigned. ``direct`` lists free nodes (base paper's three-tier
    model) that skip clustering and transmit straight to the BS. If no CH exists, all
    alive nodes transmit directly to the BS (LEACH's fallback).
    """
    ch = validate_cluster_heads(network, ch)
    network.clear_round_state()
    alive = network.alive.copy()
    alive[ch] = False
    free = np.zeros(network.n, dtype=bool)
    if direct is not None and len(direct):
        free[np.asarray(direct, dtype=int)] = True
        free &= alive                                   # only alive non-CH nodes can be free
        alive &= ~free
    others = np.flatnonzero(alive)
    free_ids = np.flatnonzero(free)

    if len(ch) == 0:
        empty_i, empty_f = np.array([], dtype=int), np.array([], dtype=float)
        return ClusterState(ch, empty_i, empty_i, empty_f, np.sort(np.concatenate([others, free_ids])), empty_i)

    d = network.distances[np.ix_(others, ch)]
    slot = d.argmin(axis=1)
    dist = d[np.arange(len(others)), slot]

    network.is_ch[ch] = True
    network.cluster_id[ch] = ch
    network.dist_to_ch[ch] = 0.0
    network.cluster_id[others] = ch[slot]
    network.dist_to_ch[others] = dist

    sizes = np.bincount(slot, minlength=len(ch)) + 1
    return ClusterState(ch, others, slot, dist, free_ids, sizes)
