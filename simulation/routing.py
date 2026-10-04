"""Routing plan for one round.

Topology is the classic two-tier single-hop LEACH structure:
    member --(intra-cluster, free-space/multipath)--> CH --(single hop)--> BS
Nodes with no CH in a round transmit directly to the BS.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from models.network import Network
from simulation.clustering import ClusterState


@dataclass
class RoutingPlan:
    member_src: np.ndarray    # member node ids
    member_slot: np.ndarray   # index of destination CH in ``ch``
    member_dist: np.ndarray   # member -> CH distance
    ch: np.ndarray            # CH node ids
    ch_bs_dist: np.ndarray    # CH -> BS distance
    direct_src: np.ndarray    # nodes transmitting straight to the BS
    direct_dist: np.ndarray

    @property
    def senders(self) -> np.ndarray:
        """Every node that generates a reading this round."""
        return np.concatenate([self.member_src, self.ch, self.direct_src])


def build_routing_plan(network: Network, clusters: ClusterState) -> RoutingPlan:
    return RoutingPlan(
        member_src=clusters.members,
        member_slot=clusters.member_slot,
        member_dist=clusters.member_dist,
        ch=clusters.ch,
        ch_bs_dist=network.dist_to_bs[clusters.ch],
        direct_src=clusters.unclustered,
        direct_dist=network.dist_to_bs[clusters.unclustered],
    )
