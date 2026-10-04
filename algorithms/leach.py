"""LEACH (Heinzelman, Chandrakasan & Balakrishnan, 2000) distributed CH election.

Every round each alive node n draws u ~ U(0, 1) and becomes a CH if u < T(n):

    T(n) = p / (1 - p * (r mod 1/p))     if n in G
         = 0                             otherwise

G is the set of nodes that have not been CH in the current epoch of 1/p
rounds, so each node serves as CH once per epoch and the CH role rotates.
Elected CHs advertise; every other node joins the CH with the strongest
advertisement (nearest CH) -- done by ``simulation.clustering.form_clusters``.
If no node elects itself, nodes transmit directly to the BS, as in LEACH.
"""
from __future__ import annotations

import numpy as np

from algorithms.base import CHSelector, Selection
from models.network import Network


class LEACH(CHSelector):
    name = "LEACH"
    centralized = False

    def reset(self, network: Network) -> None:
        self.epoch = max(1, int(round(1.0 / self.config.ch_percentage)))
        self.served = np.zeros(network.n, dtype=bool)   # was CH in the current epoch (not in G)

    def threshold(self, round_no: int) -> float:
        p = self.config.ch_percentage
        rm = (round_no - 1) % self.epoch
        denom = 1.0 - p * rm
        return 1.0 if denom <= p else min(1.0, p / denom)

    def select(self, network: Network, round_no: int) -> Selection:
        if (round_no - 1) % self.epoch == 0:
            self.served[:] = False                       # new epoch: everyone back in G
        eligible = network.alive & ~self.served
        u = self.rng.random(network.n)
        ch = np.flatnonzero(eligible & (u < self.threshold(round_no)))
        self.served[ch] = True
        return Selection(ch)
