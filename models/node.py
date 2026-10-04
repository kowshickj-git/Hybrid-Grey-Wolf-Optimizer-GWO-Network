"""Sensor node class.

For speed, the network stores node state in NumPy arrays (structure of
arrays). ``SensorNode`` is a proper object view onto one row of that state:
reading or writing ``node.residual_energy`` reads/writes the network array,
so the object API and the vectorised simulator can never disagree.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from models.network import Network


class SensorNode:
    __slots__ = ("_net", "node_id")

    def __init__(self, network: "Network", node_id: int):
        self._net = network
        self.node_id = node_id

    # --- static attributes -------------------------------------------------
    @property
    def x(self) -> float:
        return float(self._net.positions[self.node_id, 0])

    @property
    def y(self) -> float:
        return float(self._net.positions[self.node_id, 1])

    @property
    def initial_energy(self) -> float:
        return float(self._net.initial_energy[self.node_id])

    @property
    def distance_to_bs(self) -> float:
        return float(self._net.dist_to_bs[self.node_id])

    # --- dynamic attributes --------------------------------------------------
    @property
    def residual_energy(self) -> float:
        return float(self._net.energy[self.node_id])

    @residual_energy.setter
    def residual_energy(self, value: float) -> None:
        self._net.energy[self.node_id] = max(0.0, value)

    @property
    def is_alive(self) -> bool:
        return bool(self._net.alive[self.node_id])

    @property
    def status(self) -> str:
        return "ALIVE" if self.is_alive else "DEAD"

    @property
    def is_cluster_head(self) -> bool:
        return bool(self._net.is_ch[self.node_id])

    @property
    def cluster_id(self) -> int:
        """Node id of this node's CH (its own id if it is a CH, -1 if none)."""
        return int(self._net.cluster_id[self.node_id])

    @property
    def distance_to_ch(self) -> float:
        return float(self._net.dist_to_ch[self.node_id])

    @property
    def packets_generated(self) -> int:
        return int(self._net.pkt_generated[self.node_id])

    @property
    def packets_transmitted(self) -> int:
        return int(self._net.pkt_transmitted[self.node_id])

    @property
    def packets_received(self) -> int:
        return int(self._net.pkt_received[self.node_id])

    @property
    def death_round(self) -> int:
        return int(self._net.death_round[self.node_id])

    def distance_to(self, other: "SensorNode") -> float:
        return float(self._net.distances[self.node_id, other.node_id])

    def as_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "x": self.x,
            "y": self.y,
            "initial_energy": self.initial_energy,
            "residual_energy": self.residual_energy,
            "status": self.status,
            "is_cluster_head": self.is_cluster_head,
            "cluster_id": self.cluster_id,
            "distance_to_ch": self.distance_to_ch,
            "distance_to_bs": self.distance_to_bs,
            "packets_generated": self.packets_generated,
            "packets_transmitted": self.packets_transmitted,
            "packets_received": self.packets_received,
        }

    def __repr__(self) -> str:
        return (f"SensorNode(id={self.node_id}, pos=({self.x:.1f},{self.y:.1f}), "
                f"E={self.residual_energy:.4f}J, {self.status}, CH={self.is_cluster_head})")
