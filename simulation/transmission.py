"""Data transmission for one round, with exact per-node energy accounting.

Order of events (steady-state phase of a round):
    0. (optional) control overhead
    1. members -> CH          (member pays E_tx, CH pays E_rx + E_DA per packet)
    2. direct nodes -> BS     (free nodes of the base paper's model, or every alive node when no CH exists)
    3. CH aggregates its own reading (E_DA) and sends one packet to the BS (E_tx)

A node that cannot afford an operation spends what it has left, its energy
becomes 0 and the packet is lost (it will be marked DEAD at the end of the
round). Data is "delivered" only when it reaches the BS.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from models.energy_model import EnergyModel
from models.network import Network
from simulation.routing import RoutingPlan


@dataclass
class TrafficStats:
    generated: int = 0        # sensor readings generated this round
    delivered: int = 0        # readings that reached the BS (inside aggregated or direct packets)
    bs_packets: int = 0       # physical packets received by the BS
    energy: dict = field(default_factory=lambda: {
        "control": 0.0, "member_tx": 0.0, "ch_rx": 0.0, "aggregation": 0.0, "ch_tx": 0.0, "direct_tx": 0.0})

    @property
    def lost(self) -> int:
        return self.generated - self.delivered

    @property
    def total_energy(self) -> float:
        return float(sum(self.energy.values()))


def spend(network: Network, ids: np.ndarray, cost) -> np.ndarray:
    """Charge ``cost`` to nodes ``ids``. Returns a mask of nodes that could afford it.

    Nodes that cannot afford it are drained to 0 (they die trying).
    """
    ids = np.asarray(ids, dtype=int)
    cost = np.broadcast_to(np.asarray(cost, dtype=float), ids.shape)
    ok = network.energy[ids] >= cost
    network.energy[ids[ok]] -= cost[ok]
    network.energy[ids[~ok]] = 0.0
    return ok


def _control_phase(network: Network, plan: RoutingPlan, em: EnergyModel, bits: int, centralized: bool):
    senders = plan.senders
    if centralized:
        # every node reports (energy, position) to the BS, then receives the BS's CH schedule
        spend(network, senders, em.tx_energy(bits, network.dist_to_bs[senders]))
        live = senders[network.energy[senders] > 0]
        spend(network, live, em.rx_energy(bits))
    else:
        # LEACH: CH advertisement broadcast over the whole field, join-requests to the CH
        radius = float(np.hypot(*network.area))
        if len(plan.ch):
            spend(network, plan.ch, em.tx_energy(bits, radius))
            non_ch = np.concatenate([plan.member_src, plan.direct_src])
            spend(network, non_ch, em.rx_energy(bits) * len(plan.ch))
            spend(network, plan.member_src, em.tx_energy(bits, plan.member_dist))
            joins = np.bincount(plan.member_slot, minlength=len(plan.ch))
            spend(network, plan.ch, em.rx_energy(bits) * joins)


def execute_round(network: Network, plan: RoutingPlan, em: EnergyModel, packet_bits: int,
                  control_bits: int = 0, centralized: bool = True) -> TrafficStats:
    stats = TrafficStats()
    k = packet_bits
    E = network.energy

    senders = plan.senders
    stats.generated = len(senders)
    network.pkt_generated[senders] += 1

    if control_bits > 0:
        before = E.sum()
        _control_phase(network, plan, em, control_bits, centralized)
        stats.energy["control"] = before - E.sum()

    # 1. members -> CH -------------------------------------------------------
    before = E.sum()
    src = plan.member_src
    can = E[src] > 0
    sent = np.zeros(len(src), dtype=bool)
    sent[can] = spend(network, src[can], em.tx_energy(k, plan.member_dist[can]))
    network.pkt_transmitted[src[sent]] += 1
    stats.energy["member_tx"] = before - E.sum()

    # 2. direct -> BS --------------------------------------------------------
    before = E.sum()
    dsrc = plan.direct_src
    can = E[dsrc] > 0
    ok = np.zeros(len(dsrc), dtype=bool)
    ok[can] = spend(network, dsrc[can], em.tx_energy(k, plan.direct_dist[can]))
    network.pkt_transmitted[dsrc[ok]] += 1
    stats.delivered += int(ok.sum())
    stats.bs_packets += int(ok.sum())
    stats.energy["direct_tx"] = before - E.sum()

    # 3. CH reception, aggregation, CH -> BS ----------------------------------
    ch = plan.ch
    if len(ch):
        incoming = np.bincount(plan.member_slot[sent], minlength=len(ch))
        per_packet = em.rx_energy(k) + em.aggregation_energy(k)
        ch_alive = E[ch] > 0
        capacity = np.floor(E[ch] / per_packet).astype(np.int64)
        n_rx = np.where(ch_alive, np.minimum(incoming, capacity), 0)
        rx_cost = n_rx * per_packet
        before = E.sum()
        E[ch] -= rx_cost
        starved = ch_alive & (n_rx < incoming)          # ran out of energy while receiving
        E[ch[starved]] = 0.0
        network.pkt_received[ch] += n_rx
        rx_energy = before - E.sum()
        # split reception energy into radio and aggregation parts
        stats.energy["ch_rx"] = rx_energy * em.rx_energy(k) / per_packet
        stats.energy["aggregation"] = rx_energy - stats.energy["ch_rx"]

        before = E.sum()
        working = np.flatnonzero(E[ch] > 0)
        own = spend(network, ch[working], em.aggregation_energy(k))
        stats.energy["aggregation"] += before - E.sum()
        working = working[own]

        before = E.sum()
        tx_ok = spend(network, ch[working], em.tx_energy(k, plan.ch_bs_dist[working]))
        stats.energy["ch_tx"] = before - E.sum()
        delivered_slots = working[tx_ok]
        network.pkt_transmitted[ch[delivered_slots]] += 1
        stats.delivered += int((n_rx[delivered_slots] + 1).sum())
        stats.bs_packets += len(delivered_slots)

    return stats
