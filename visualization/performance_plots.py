"""Per-round performance curves and summary bar charts (all from simulation data)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from evaluation.metrics import METRICS
from visualization import style

# columns that keep their last value after a run ends (all nodes dead)
CUMULATIVE = ["alive", "dead", "residual_energy", "consumed_energy", "packets_generated",
              "packets_delivered", "bs_packets", "throughput_bits", "pdr"]
PER_ROUND = ["round_energy", "ch_count", "avg_intra_distance", "avg_ch_bs_distance", "cluster_imbalance",
             "fitness", "selection_time", "round_pdr"]

ROUND_PLOTS = {  # column -> (y label, title, rolling window)
    "alive": ("Alive nodes", "Alive nodes vs rounds", None),
    "dead": ("Dead nodes", "Dead nodes vs rounds", None),
    "residual_energy": ("Total residual energy (J)", "Residual energy vs rounds", None),
    "consumed_energy": ("Cumulative energy consumed (J)", "Energy consumption vs rounds", None),
    "packets_delivered": ("Data packets delivered to BS", "Throughput vs rounds (cumulative)", None),
    "pdr": ("Packet delivery ratio (cumulative)", "PDR vs rounds", None),
    "ch_count": ("Cluster heads per round", "CH count vs rounds (20-round rolling mean)", 20),
    "avg_intra_distance": ("Mean member → CH distance (m)",
                           "Average cluster distance vs rounds (20-round rolling mean)", 20),
}


def mean_round_curves(histories: pd.DataFrame, max_round: int | None = None) -> pd.DataFrame:
    """Average per-round histories over runs, per algorithm.

    Runs that ended early (all nodes dead) are padded: cumulative columns keep
    their final value, per-round columns become NaN (ignored in the mean).
    """
    max_round = max_round or int(histories["round"].max())
    rounds = pd.RangeIndex(1, max_round + 1, name="round")
    out = []
    for (alg, run), df in histories.groupby(["algorithm", "run"], sort=False):
        df = df.set_index("round").reindex(rounds)
        df[[c for c in CUMULATIVE if c in df]] = df[[c for c in CUMULATIVE if c in df]].ffill()
        df["algorithm"], df["run"] = alg, run
        out.append(df.reset_index())
    full = pd.concat(out, ignore_index=True)
    cols = [c for c in CUMULATIVE + PER_ROUND if c in full]
    return full.groupby(["algorithm", "round"], sort=False)[cols].mean().reset_index()


def plot_round_metric(curves: pd.DataFrame, column: str, algorithms, path=None, ylabel=None, title=None,
                      window=None, n_runs: int | None = None):
    label, default_title, default_window = ROUND_PLOTS.get(column, (column, column, None))
    window = default_window if window is None else window
    fig = style.new_figure(7.5, 4.5)
    ax = fig.add_subplot()
    for alg in algorithms:
        df = curves[curves["algorithm"] == alg]
        y = df[column]
        if window:
            y = y.rolling(window, min_periods=1).mean()
        ax.plot(df["round"], y, color=style.color(alg), ls=style.linestyle(alg), label=alg)
    ax.set_xlabel("Round")
    ax.set_ylabel(ylabel or label)
    sub = f" — mean of {n_runs} runs" if n_runs and n_runs > 1 else ""
    ax.set_title((title or default_title) + sub, loc="left")
    ax.legend()
    if column == "pdr":
        lo = np.nanmin(curves[column].values)
        ax.set_ylim(max(0.0, lo - 0.01), 1.002)
    return style.save(fig, path) if path else fig


def plot_lifetime_bars(runs: pd.DataFrame, algorithms, path=None, title="Network lifetime: FND / HND / LND"):
    fig = style.new_figure(7.8, 4.6)
    ax = fig.add_subplot()
    metrics = ["fnd", "hnd", "lnd"]
    width = 0.8 / len(algorithms)
    x = np.arange(len(metrics))
    for i, alg in enumerate(algorithms):
        df = runs[runs["algorithm"] == alg]
        means = [df[m].mean() for m in metrics]
        sds = [df[m].std(ddof=1) if len(df) > 1 else 0 for m in metrics]
        pos = x - 0.4 + width * (i + 0.5)
        ax.bar(pos, means, width * 0.92, yerr=sds, color=style.color(alg), label=alg,
               error_kw=dict(ecolor=style.INK_2, lw=1, capsize=3), edgecolor=style.SURFACE, linewidth=1)
    ax.set_xticks(x, [METRICS[m].label for m in metrics])
    ax.set_ylabel("Round")
    ax.set_title(title + (" (mean ± std)" if runs["run"].nunique() > 1 else ""), loc="left")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    return style.save(fig, path) if path else fig


def plot_metric_bars(runs: pd.DataFrame, metric: str, algorithms, path=None, title=None, log=False):
    info = METRICS[metric]
    fig = style.new_figure(7.0, 4.2)
    ax = fig.add_subplot()
    means = [runs.loc[runs["algorithm"] == a, metric].mean() for a in algorithms]
    sds = [runs.loc[runs["algorithm"] == a, metric].std(ddof=1) for a in algorithms]
    sds = [0 if np.isnan(s) else s for s in sds]
    y = np.arange(len(algorithms))
    ax.barh(y, means, xerr=sds, color=[style.color(a) for a in algorithms], height=0.6,
            error_kw=dict(ecolor=style.INK_2, lw=1, capsize=3))
    for yi, m, s in zip(y, means, sds):
        ax.annotate(f"{m:.3g}", (m + s, yi), xytext=(4, 0), textcoords="offset points", va="center",
                    fontsize=8, color=style.INK_2)
    ax.set_yticks(y, algorithms)
    ax.invert_yaxis()
    if log:
        ax.set_xscale("log")
    ax.set_xlabel(f"{info.label} ({info.unit})")
    ax.grid(axis="y", visible=False)
    ax.set_title(title or f"{info.label} comparison", loc="left")
    return style.save(fig, path) if path else fig


def plot_energy_breakdown(histories: pd.DataFrame, algorithms, path=None, checkpoint: int | None = None):
    """Mean energy per radio activity over rounds 1..checkpoint (stacked)."""
    parts = ["e_member_tx", "e_ch_rx", "e_aggregation", "e_ch_tx", "e_direct_tx", "e_control"]
    labels = ["Member → CH TX", "CH RX", "Aggregation", "CH → BS TX", "Direct → BS TX", "Control"]
    h = histories if checkpoint is None else histories[histories["round"] <= checkpoint]
    per_run = h.groupby(["algorithm", "run"])[parts].sum().groupby("algorithm").mean().reindex(algorithms)
    keep = [p for p in parts if per_run[p].sum() > 0]
    fig = style.new_figure(7.8, 4.4)
    ax = fig.add_subplot()
    left = np.zeros(len(algorithms))
    for i, p in enumerate(keep):
        ax.barh(algorithms, per_run[p], left=left, color=style.SLOTS[i], height=0.6,
                label=labels[parts.index(p)], edgecolor=style.SURFACE, linewidth=2)
        left += per_run[p].values
    ax.invert_yaxis()
    ax.set_xlabel("Energy (J)")
    ax.grid(axis="y", visible=False)
    suffix = f" over rounds 1–{checkpoint}" if checkpoint else ""
    ax.set_title("Energy by radio activity" + suffix, loc="left")
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    return style.save(fig, path) if path else fig


def plot_runtime_benchmark(df: pd.DataFrame, algorithms, path=None):
    """Grouped bars: median CH-selection ms/round per network size (log scale); dots = individual seeds."""
    sizes = sorted(df["n_nodes"].unique())
    fig = style.new_figure(7.8, 4.4)
    ax = fig.add_subplot()
    width = 0.8 / len(algorithms)
    x = np.arange(len(sizes))
    for i, alg in enumerate(algorithms):
        sub = df[df["algorithm"] == alg]
        med = sub.groupby("n_nodes")["ms_per_round"].median().reindex(sizes)
        pos = x - 0.4 + width * (i + 0.5)
        ax.bar(pos, med, width * 0.92, color=style.color(alg), label=alg, edgecolor=style.SURFACE, linewidth=1)
        for p, n in zip(pos, sizes):
            vals = sub.loc[sub["n_nodes"] == n, "ms_per_round"]
            ax.scatter(np.full(len(vals), p), vals, s=12, color=style.INK_2, zorder=3, linewidths=0)
    ax.set_yscale("log")
    ax.set_xticks(x, [f"{s} nodes" for s in sizes])
    ax.set_ylabel("CH-selection time per round (ms, log)")
    ax.grid(axis="x", visible=False)
    ax.set_title("Runtime per round — sequential benchmark (bar = median, dots = seeds)", loc="left")
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    return style.save(fig, path) if path else fig


def plot_sensitivity(df: pd.DataFrame, factor: str, metric: str, path=None, xlabel=None):
    """``df`` columns: algorithm, value, <metric>_mean, <metric>_std."""
    info = METRICS[metric]
    fig = style.new_figure(6.8, 4.2)
    ax = fig.add_subplot()
    numeric = pd.api.types.is_numeric_dtype(df["value"])
    labels = list(dict.fromkeys(df["value"].astype(str)))
    for alg, g in df.groupby("algorithm", sort=False):
        x = g["value"] if numeric else [labels.index(v) for v in g["value"].astype(str)]
        ax.errorbar(x, g[f"{metric}_mean"], yerr=g[f"{metric}_std"], color=style.color(alg),
                    ls=style.linestyle(alg), marker="o", ms=5, capsize=3, label=alg)
    if not numeric:
        ax.set_xticks(range(len(labels)), labels, rotation=15)
    ax.set_xlabel(xlabel or factor)
    ax.set_ylabel(f"{info.label} ({info.unit})")
    ax.set_title(f"Sensitivity of {info.label} to {xlabel or factor}", loc="left")
    ax.legend()
    return style.save(fig, path) if path else fig
