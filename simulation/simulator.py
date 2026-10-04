"""Multi-round WSN simulation.

One round::

    check alive nodes -> select CHs (algorithm) -> form clusters -> generate data
    -> members -> CH -> aggregation -> CH -> BS -> update energy
    -> detect dead nodes -> compute metrics -> record

The simulation stops after ``config.rounds`` rounds or when every node is dead.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from algorithms import make_algorithm
from algorithms.base import CHSelector, Selection
from algorithms.fitness import FitnessContext
from config import SimulationConfig
from evaluation.metrics import RoundRecord, summarize
from models.energy_model import EnergyModel
from models.network import Network
from simulation.clustering import ClusterState, form_clusters
from simulation.routing import build_routing_plan
from simulation.transmission import execute_round


@dataclass
class SimulationResult:
    algorithm: str
    config: SimulationConfig
    seed: int
    history: pd.DataFrame
    summary: dict
    death_round: np.ndarray
    network: Network                                  # final network state
    curves: dict = field(default_factory=dict)        # round -> {curve name: best-so-far list}
    snapshots: dict = field(default_factory=dict)     # round -> network snapshot (see Simulator.snapshot)
    ch_log: pd.DataFrame = field(default_factory=pd.DataFrame)  # one row per selected CH per round


CH_LOG_COLUMNS = ["round", "ch_id", "x", "y", "residual_energy", "distance_to_bs", "cluster_size"]


class Simulator:
    def __init__(self, config: SimulationConfig, algorithm: str | CHSelector, network: Network | None = None,
                 seed: int | None = None, curve_rounds=(1,), snapshot_rounds=()):
        config.validate()
        self.config = config
        self.seed = config.seed if seed is None else seed
        self.network = network.copy() if network is not None else Network.deploy(config, self.seed)
        self.network.reset()
        self.algorithm = make_algorithm(algorithm, config, self.seed) if isinstance(algorithm, str) else algorithm
        self.algorithm.reset(self.network)
        self.em = EnergyModel(config.energy)
        self.curve_rounds = set(curve_rounds)
        self.snapshot_rounds = set(snapshot_rounds)
        self.round = 0
        self.records: list[RoundRecord] = []
        self.curves: dict = {}
        self.snapshots: dict = {}
        self.last_selection: Selection | None = None
        self.last_clusters: ClusterState | None = None
        self._cum = dict(generated=0, delivered=0, bs_packets=0)
        self._ch_rows: list[np.ndarray] = []                       # per-round CH records (see ch_log)

    # ---------------------------------------------------------------- state
    @property
    def finished(self) -> bool:
        return self.round >= self.config.rounds or self.network.n_alive == 0

    def snapshot(self) -> dict:
        net = self.network
        return {"round": self.round, "positions": net.positions.copy(), "bs": net.bs.copy(),
                "area": net.area, "alive": net.alive.copy(), "energy": net.energy.copy(),
                "is_ch": net.is_ch.copy(), "cluster_id": net.cluster_id.copy()}

    # ---------------------------------------------------------------- round
    def step(self) -> RoundRecord | None:
        if self.finished:
            return None
        net, cfg = self.network, self.config
        r = self.round + 1
        energy_before = net.total_energy

        t0 = time.perf_counter()
        sel = self.algorithm.select(net, r)                      # CH selection
        t_sel = time.perf_counter() - t0

        if sel.fitness is None:                                   # same objective for every algorithm
            ctx = FitnessContext(net, cfg)
            fitness = float(ctx.evaluate(ctx.from_node_ids(sel.ch)[None, :])[0]) if ctx.m else np.nan
        else:
            fitness = float(sel.fitness)

        clusters = form_clusters(net, sel.ch, sel.direct)         # cluster formation (dead/duplicate CHs dropped)
        if clusters.n_clusters:                                   # record final CHs: id, position, energy, BS dist.
            ch = clusters.ch
            self._ch_rows.append(np.column_stack([np.full(len(ch), r), ch, net.positions[ch], net.energy[ch],
                                                  net.dist_to_bs[ch], clusters.sizes]))
        plan = build_routing_plan(net, clusters)
        stats = execute_round(net, plan, self.em, cfg.packet_bits, cfg.control_bits,
                              self.algorithm.centralized)         # transmission + energy update
        if r in self.snapshot_rounds:                             # clusters as used this round
            self.snapshots[r] = self.snapshot() | {"round": r}
        newly_dead = net.detect_dead(r)                           # dead-node detection

        self.round = r
        c = self._cum
        c["generated"] += stats.generated
        c["delivered"] += stats.delivered
        c["bs_packets"] += stats.bs_packets
        residual = net.total_energy
        ch_bs = net.dist_to_bs[clusters.ch]
        rec = RoundRecord(
            round=r, alive=net.n_alive, dead=net.n - net.n_alive, newly_dead=len(newly_dead),
            residual_energy=residual, consumed_energy=net.total_initial_energy - residual,
            round_energy=energy_before - residual, ch_count=clusters.n_clusters,
            packets_generated=c["generated"], packets_delivered=c["delivered"], bs_packets=c["bs_packets"],
            throughput_bits=float(c["bs_packets"] * cfg.packet_bits),
            pdr=c["delivered"] / c["generated"] if c["generated"] else np.nan,
            round_pdr=stats.delivered / stats.generated if stats.generated else np.nan,
            avg_intra_distance=clusters.avg_distance, max_intra_distance=clusters.max_distance,
            avg_ch_bs_distance=float(ch_bs.mean()) if len(ch_bs) else np.nan,
            cluster_imbalance=clusters.imbalance if clusters.n_clusters else np.nan,
            fitness=fitness, selection_time=t_sel, evaluations=sel.evaluations,
            e_control=stats.energy["control"], e_member_tx=stats.energy["member_tx"],
            e_ch_rx=stats.energy["ch_rx"], e_aggregation=stats.energy["aggregation"],
            e_ch_tx=stats.energy["ch_tx"], e_direct_tx=stats.energy["direct_tx"],
        )
        self.records.append(rec)
        if r in self.curve_rounds and sel.curves:
            self.curves[r] = {k: list(map(float, v)) for k, v in sel.curves.items()}
        self.last_selection, self.last_clusters = sel, clusters
        return rec

    def run(self, callback=None, should_stop=None) -> SimulationResult:
        """Run to completion. ``callback(sim, record)`` after each round; ``should_stop()`` aborts."""
        while not self.finished:
            if should_stop is not None and should_stop():
                break
            rec = self.step()
            if callback is not None:
                callback(self, rec)
        return self.result()

    def history(self) -> pd.DataFrame:
        return pd.DataFrame([r.as_dict() for r in self.records])

    def ch_log(self) -> pd.DataFrame:
        """Selected cluster heads of every round: id, coordinates, residual energy at selection,
        distance to the BS and cluster size (members + CH)."""
        if not self._ch_rows:
            return pd.DataFrame(columns=CH_LOG_COLUMNS)
        df = pd.DataFrame(np.vstack(self._ch_rows), columns=CH_LOG_COLUMNS)
        return df.astype({"round": int, "ch_id": int, "cluster_size": int})

    def result(self) -> SimulationResult:
        hist = self.history()
        cfg = self.config
        summary = summarize(hist, self.network.death_round, self.network.n,
                            self.network.total_initial_energy, cfg.checkpoint_round, cfg.rounds)
        return SimulationResult(self.algorithm.name, cfg, self.seed, hist, summary,
                                self.network.death_round.copy(), self.network, self.curves, self.snapshots,
                                self.ch_log())


def run_simulation(config: SimulationConfig, algorithm: str, network: Network | None = None,
                   seed: int | None = None, **kwargs) -> SimulationResult:
    return Simulator(config, algorithm, network, seed, **kwargs).run()
