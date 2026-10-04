"""Algorithm comparison: result tables and automatic, data-driven interpretation.

Nothing here assumes which algorithm is better. Every sentence is generated
from measured means, paired tests and effect sizes; "why" statements are
phrased as possible mechanisms and are only emitted when the data show the
corresponding pattern.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from evaluation.metrics import METRICS, TABLE_METRICS
from evaluation.statistics import compare_to_baselines, describe

PRACTICAL_PCT = 1.0       # |improvement| below this is reported as practically small

MECHANISMS = {
    "fnd": ("CH selection that avoids low-energy nodes and rotates the CH role evenly delays the first "
            "death; a node chosen repeatedly as CH (e.g. because it is close to the BS) dies early."),
    "hnd": "HND reflects how evenly energy is drained across the whole network.",
    "lnd": ("A very even energy drain makes all nodes die at nearly the same time: FND is delayed but the "
            "last node also dies sooner. Uneven drain leaves a few nodes with spare energy that keep running."),
    "node_rounds": "The area under the alive-nodes curve combines stability period and tail length.",
    "residual_energy_cp": ("Residual energy at a fixed round depends on per-round radio cost: shorter "
                           "member->CH links and shorter or fewer CH->BS links consume less."),
    "energy_consumed_cp": "Consumption is the complement of residual energy at the same checkpoint.",
    "throughput_packets": ("Throughput grows with the number of rounds in which nodes are alive and with "
                           "the share of packets that are not lost to CHs dying mid-round."),
    "pdr": ("Packets are lost when a CH runs out of energy before forwarding its cluster's data, or when "
            "a node dies while transmitting. Energy-feasibility checks on CHs reduce such losses."),
    "avg_cluster_distance": ("The fitness function explicitly penalises member->CH distance; LEACH places "
                             "CHs at random positions, which typically lengthens member links."),
    "avg_ch_bs_distance": ("The fitness penalises CH->BS distance, but the energy-eligibility rule and the "
                           "energy term limit how often nodes near the BS can be selected."),
    "cluster_imbalance": "The fitness penalises unequal cluster sizes; nearest-CH assignment does not.",
    "final_fitness": ("Optimisers minimise this objective directly; LEACH does not use it, and rounds in "
                      "which LEACH elects zero CHs or too many receive the invalid-solution penalty."),
    "runtime": ("Metaheuristics evaluate hundreds of candidate CH sets per round; LEACH needs one random "
                "draw per node. The hybrid runs two populations and more operators per iteration, which "
                "adds overhead even at an equal number of fitness evaluations."),
}

HOW = {
    "fnd": "min over nodes of the round in which residual energy reached 0 (simulation horizon if none died).",
    "hnd": "round in which the number of dead nodes reached ceil(N/2).",
    "lnd": "round in which the last node died (simulation horizon if nodes were still alive).",
    "node_rounds": "sum over rounds of alive nodes.",
    "residual_energy_cp": "sum of node residual energies after the checkpoint round.",
    "energy_consumed_cp": "N * E0 - residual energy at the checkpoint round.",
    "throughput_packets": "count of sensor readings that reached the BS over the whole run.",
    "pdr": "delivered readings / generated readings over the whole run.",
    "avg_cluster_distance": "per round mean member->CH distance, averaged over rounds 1..checkpoint.",
    "avg_ch_bs_distance": "per round mean CH->BS distance, averaged over rounds 1..checkpoint.",
    "cluster_imbalance": "per round std/mean of cluster sizes, averaged over rounds 1..checkpoint.",
    "final_fitness": "per round fitness of the CH set used (same weights for all), mean over rounds 1..checkpoint.",
    "runtime": "sum of wall-clock CH-selection time over all rounds (time.perf_counter).",
    "runtime_per_round": "runtime / rounds simulated.",
    "evaluations": "sum of fitness evaluations over all rounds.",
}


def fmt(metric: str, value: float) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "n/a"
    if metric in ("fnd", "hnd", "lnd", "throughput_packets", "evaluations", "node_rounds"):
        return f"{value:,.0f}"
    if metric == "pdr":
        return f"{value:.4f}"
    if metric in ("runtime",):
        return f"{value:.2f}"
    if metric in ("final_fitness", "cluster_imbalance"):
        return f"{value:.4f}"
    return f"{value:.3f}"


def result_table(runs: pd.DataFrame, algorithms, metrics=TABLE_METRICS, with_std: bool = True,
                 censored: dict | None = None) -> pd.DataFrame:
    """Metric x algorithm table of 'mean ± std' strings (index = metric labels)."""
    desc = describe(runs, metrics).set_index(["algorithm", "metric"])
    data = {}
    for alg in algorithms:
        col = []
        for m in metrics:
            row = desc.loc[(alg, m)]
            s = fmt(m, row["mean"])
            if with_std and row["n"] > 1:
                s += f" ± {fmt(m, row['std'])}"
            if censored and censored.get((alg, m)):
                s = "≥ " + s
            col.append(s)
        data[alg] = col
    idx = [f"{METRICS[m].label} ({METRICS[m].unit})" for m in metrics]
    return pd.DataFrame(data, index=idx)


def censoring(runs: pd.DataFrame) -> dict:
    """(algorithm, metric) -> True when any run did not reach FND/HND/LND within the horizon."""
    out = {}
    for alg, df in runs.groupby("algorithm"):
        for m in ("fnd", "hnd", "lnd"):
            col = f"{m}_censored"
            out[(alg, m)] = bool(col in df and df[col].any())
    return out


def means_by_algorithm(runs: pd.DataFrame, metric: str) -> pd.Series:
    return runs.groupby("algorithm", sort=False)[metric].mean()


def _best(means: pd.Series, metric: str) -> str:
    return means.idxmax() if METRICS[metric].higher_is_better else means.idxmin()


def interpret_metric(metric: str, runs: pd.DataFrame, cmp: pd.DataFrame, proposed: str,
                     algorithms) -> str:
    info = METRICS[metric]
    means = means_by_algorithm(runs, metric).reindex(algorithms)
    stds = runs.groupby("algorithm")[metric].std().reindex(algorithms)
    direction = "higher is better" if info.higher_is_better else "lower is better"
    lines = [f"#### {info.label}",
             f"- **What it represents:** {info.definition}",
             f"- **How it was calculated:** {HOW.get(metric, info.definition)} ({direction}, unit: {info.unit})",
             f"- **Why it matters:** {info.why}"]
    observed = ", ".join(f"{a} {fmt(metric, means[a])} (± {fmt(metric, stds[a])})" for a in algorithms)
    best = _best(means, metric)
    lines.append(f"- **Observed (mean ± std over runs):** {observed}. Best mean: **{best}**.")

    rows = cmp[cmp["metric"] == metric]
    if proposed in algorithms and len(rows):
        parts = []
        for _, r in rows.iterrows():
            kind = "improvement" if r["higher_is_better"] else "reduction"
            pct = r["improvement_pct"]
            sig = (f"p = {r['p_holm']:.3g} (Holm), Cliff's δ = {r['cliffs_delta']:+.2f} ({r['effect']})")
            if np.isnan(pct):
                parts.append(f"vs {r['baseline']}: not computable (baseline mean is 0)")
                continue
            word = "better" if pct > 0 else "worse" if pct < 0 else "equal"
            size = " — practically small" if abs(pct) < PRACTICAL_PCT else ""
            if abs(pct) >= 1000 and r["baseline_mean"]:
                size += f" (proposed/baseline ratio {r['proposed_mean'] / r['baseline_mean']:.0f}×)"
            parts.append(f"vs {r['baseline']}: {proposed} is {abs(pct):.2f}% {word} "
                         f"({kind} formula), {sig} → **{r['verdict']}**{size}")
        lines.append("- **Proposed vs baselines:** " + "; ".join(parts) + ".")
        n_sig = int(rows["significant"].sum())
        lines.append(f"- **Is the difference meaningful?** {n_sig} of {len(rows)} comparisons are statistically "
                     f"significant at α = 0.05 after Holm correction. Differences that are not significant, or "
                     f"below {PRACTICAL_PCT}% in size, should not be presented as improvements.")
    mech = _mechanism_sentence(metric, means, runs, algorithms)
    if mech:
        lines.append(f"- **Possible explanation:** {mech}")
    return "\n".join(lines)


def _mechanism_sentence(metric: str, means: pd.Series, runs: pd.DataFrame, algorithms) -> str:
    base = MECHANISMS.get(metric, "")
    if metric in ("fnd", "lnd") and {"fnd", "lnd"} <= set(runs.columns):
        spread = (runs.groupby("algorithm")["lnd"].mean() - runs.groupby("algorithm")["fnd"].mean())
        spread = spread.reindex(algorithms)
        desc = ", ".join(f"{a} {spread[a]:.0f}" for a in algorithms)
        base += f" Measured LND − FND spread (rounds): {desc}."
    if metric == "runtime" and "LEACH" in means.index and means.get("LEACH", 0) > 0:
        ratios = ", ".join(f"{a} {means[a] / means['LEACH']:.0f}×" for a in algorithms if a != "LEACH")
        base += f" Runtime relative to LEACH: {ratios}."
    return base


def trade_off_summary(cmp: pd.DataFrame, proposed: str) -> str:
    if cmp.empty:
        return ""
    def tag(rows):
        return [f"{r['label']} ({r['improvement_pct']:+.2f}%{', < 1%: practically negligible' if abs(r['improvement_pct']) < PRACTICAL_PCT else ''})"
                for _, r in rows.iterrows()]

    lines = []
    for base, df in cmp.groupby("baseline", sort=False):
        better = tag(df[df["verdict"] == "proposed better"])
        worse = tag(df[df["verdict"] == "proposed worse"])
        same = df[df["verdict"] == "no significant difference"]["label"].tolist()
        lines.append(f"- **{proposed} vs {base}** — significantly better: {', '.join(better) or 'none'}; "
                     f"significantly worse: {', '.join(worse) or 'none'}; no significant difference: "
                     f"{', '.join(same) or 'none'}.")
    return "\n".join(lines)


def full_comparison(runs: pd.DataFrame, algorithms, proposed: str | None, metrics=None):
    """Convenience: (result table, stats long table, baseline comparison)."""
    from evaluation.metrics import STAT_METRICS
    metrics = metrics or STAT_METRICS
    table = result_table(runs, algorithms, censored=censoring(runs))
    stats_df = describe(runs, metrics)
    if proposed and proposed in algorithms:
        baselines = [a for a in algorithms if a != proposed]
        cmp = compare_to_baselines(runs, proposed, baselines, metrics)
    else:
        cmp = pd.DataFrame(columns=["metric", "baseline", "verdict"])
    return table, stats_df, cmp
