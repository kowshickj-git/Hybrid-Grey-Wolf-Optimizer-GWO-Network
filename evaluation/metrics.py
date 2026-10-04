"""Performance metrics: definitions, per-round records and per-run summaries.

Every number reported by the project is computed here from simulation data.
``METRICS`` documents each summary metric (meaning, formula, direction).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd


@dataclass
class MetricInfo:
    label: str
    unit: str
    higher_is_better: bool
    definition: str
    why: str


METRICS: dict[str, MetricInfo] = {
    "fnd": MetricInfo("FND", "rounds", True,
                      "First Node Death: the round in which the first node's residual energy reached 0.",
                      "Marks the end of the stability period, during which every sensor still reports."),
    "hnd": MetricInfo("HND", "rounds", True,
                      "Half Node Death: the round in which at least 50% of the nodes were dead.",
                      "Indicates how long the network keeps useful coverage."),
    "lnd": MetricInfo("LND", "rounds", True,
                      "Last Node Death: the round in which the last alive node died.",
                      "Upper bound of the network lifetime."),
    "node_rounds": MetricInfo("Node-rounds", "node x rounds", True,
                              "Sum over rounds of the number of alive nodes (area under the alive-nodes curve).",
                              "Single-number lifetime measure that accounts for the whole death curve."),
    "residual_energy_cp": MetricInfo("Residual Energy", "J", True,
                                     "Total residual energy of all nodes at the checkpoint round.",
                                     "More energy left at the same round means cheaper operation."),
    "energy_consumed_cp": MetricInfo("Energy Consumption", "J", False,
                                     "Initial total energy minus residual energy at the checkpoint round.",
                                     "Energy spent to operate the network for the same number of rounds."),
    "throughput_packets": MetricInfo("Throughput", "packets", True,
                                     "Total sensor data packets delivered to the BS over the whole simulation "
                                     "(directly or inside an aggregated CH packet).",
                                     "Amount of sensed data the application actually receives."),
    "throughput_bits": MetricInfo("Throughput (bits)", "bits", True,
                                  "Packets physically received by the BS x packet size.",
                                  "Load carried on the CH->BS link."),
    "pdr": MetricInfo("PDR", "ratio", True,
                      "Packet Delivery Ratio = delivered data packets / generated data packets.",
                      "Reliability: share of generated readings that reach the BS."),
    "avg_cluster_distance": MetricInfo("Avg. Cluster Distance", "m", False,
                                       "Mean member->CH distance, averaged over rounds 1..checkpoint.",
                                       "Shorter intra-cluster links cost less transmission energy (d^2 / d^4)."),
    "avg_ch_bs_distance": MetricInfo("Avg. CH-BS Distance", "m", False,
                                     "Mean CH->BS distance, averaged over rounds 1..checkpoint.",
                                     "CH->BS is the longest and most expensive hop."),
    "avg_ch_count": MetricInfo("Avg. CH Count", "CHs", False,
                               "Mean number of CHs per round over rounds 1..checkpoint (lower is not "
                               "necessarily better; shown for reference).",
                               "Too few CHs lengthen member links; too many add CH->BS transmissions."),
    "cluster_imbalance": MetricInfo("Cluster Imbalance", "CV", False,
                                    "Coefficient of variation of cluster sizes, averaged over rounds 1..checkpoint.",
                                    "Balanced clusters spread the CH load evenly."),
    "final_fitness": MetricInfo("Final Fitness", "-", False,
                                "Mean per-round fitness (same function and weights for every algorithm) of "
                                "the CH set actually used, over rounds 1..checkpoint. Lower is better.",
                                "Quality of the CH configurations according to the optimisation objective."),
    "runtime": MetricInfo("Runtime", "s", False,
                          "Total wall-clock time spent selecting CHs over the whole simulation.",
                          "Computational cost of the CH selection algorithm."),
    "runtime_per_round": MetricInfo("Runtime / round", "ms", False,
                                    "CH selection time divided by simulated rounds.",
                                    "Per-round cost, independent of the network lifetime."),
    "evaluations": MetricInfo("Fitness Evaluations", "evals", False,
                              "Total number of fitness evaluations spent on CH selection.",
                              "Hardware-independent computational cost."),
}

# metrics shown in the final comparison table, in order
TABLE_METRICS = ["fnd", "hnd", "lnd", "residual_energy_cp", "energy_consumed_cp", "throughput_packets",
                 "pdr", "avg_cluster_distance", "avg_ch_bs_distance", "runtime", "final_fitness"]
STAT_METRICS = ["fnd", "hnd", "lnd", "node_rounds", "residual_energy_cp", "energy_consumed_cp",
                "throughput_packets", "pdr", "avg_cluster_distance", "avg_ch_bs_distance",
                "cluster_imbalance", "final_fitness", "runtime", "runtime_per_round", "evaluations"]


@dataclass
class RoundRecord:
    round: int
    alive: int
    dead: int
    newly_dead: int
    residual_energy: float
    consumed_energy: float          # cumulative
    round_energy: float
    ch_count: int
    packets_generated: int          # cumulative
    packets_delivered: int          # cumulative
    bs_packets: int                 # cumulative
    throughput_bits: float          # cumulative
    pdr: float                      # cumulative
    round_pdr: float
    avg_intra_distance: float
    max_intra_distance: float
    avg_ch_bs_distance: float
    cluster_imbalance: float
    fitness: float
    selection_time: float           # s
    evaluations: int
    e_control: float
    e_member_tx: float
    e_ch_rx: float
    e_aggregation: float
    e_ch_tx: float
    e_direct_tx: float

    def as_dict(self) -> dict:
        return asdict(self)


def lifetime_rounds(death_round: np.ndarray, n: int) -> dict:
    """FND / HND / LND from per-node death rounds (-1 = still alive). NaN when not reached."""
    deaths = np.sort(death_round[death_round >= 0])
    half = int(np.ceil(n / 2))
    return {
        "fnd": float(deaths[0]) if len(deaths) else np.nan,
        "hnd": float(deaths[half - 1]) if len(deaths) >= half else np.nan,
        "lnd": float(deaths[-1]) if len(deaths) == n else np.nan,
    }


def summarize(history: pd.DataFrame, death_round: np.ndarray, n_nodes: int, initial_energy: float,
              checkpoint: int, max_rounds: int) -> dict:
    """Per-run summary metrics (see ``METRICS``)."""
    out = lifetime_rounds(death_round, n_nodes)
    last = history.iloc[-1] if len(history) else None
    horizon = float(last["round"]) if last is not None else float(max_rounds)
    for key in ("fnd", "hnd", "lnd"):
        out[f"{key}_censored"] = bool(np.isnan(out[key]))
        if np.isnan(out[key]):
            out[key] = horizon                  # not reached within the simulated rounds -> lower bound

    cp = history[history["round"] <= checkpoint]
    cp_last = cp.iloc[-1] if len(cp) else None
    out["rounds_simulated"] = int(last["round"]) if last is not None else 0
    out["node_rounds"] = float(history["alive"].sum()) if len(history) else 0.0
    out["residual_energy_cp"] = float(cp_last["residual_energy"]) if cp_last is not None else initial_energy
    out["energy_consumed_cp"] = float(cp_last["consumed_energy"]) if cp_last is not None else 0.0
    out["residual_energy_end"] = float(last["residual_energy"]) if last is not None else initial_energy
    out["energy_consumed_end"] = float(last["consumed_energy"]) if last is not None else 0.0
    out["packets_generated"] = int(last["packets_generated"]) if last is not None else 0
    out["throughput_packets"] = int(last["packets_delivered"]) if last is not None else 0
    out["bs_packets"] = int(last["bs_packets"]) if last is not None else 0
    out["throughput_bits"] = float(last["throughput_bits"]) if last is not None else 0.0
    out["pdr"] = out["throughput_packets"] / out["packets_generated"] if out["packets_generated"] else np.nan
    out["avg_cluster_distance"] = float(cp["avg_intra_distance"].mean()) if len(cp) else np.nan
    out["avg_ch_bs_distance"] = float(cp["avg_ch_bs_distance"].mean()) if len(cp) else np.nan
    out["avg_ch_count"] = float(cp["ch_count"].mean()) if len(cp) else np.nan
    out["cluster_imbalance"] = float(cp["cluster_imbalance"].mean()) if len(cp) else np.nan
    out["final_fitness"] = float(cp["fitness"].mean()) if len(cp) else np.nan
    out["runtime"] = float(history["selection_time"].sum()) if len(history) else 0.0
    out["runtime_per_round"] = 1000 * out["runtime"] / max(out["rounds_simulated"], 1)
    out["evaluations"] = int(history["evaluations"].sum()) if len(history) else 0
    return out
