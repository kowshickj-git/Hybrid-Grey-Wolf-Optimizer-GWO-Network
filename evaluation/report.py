"""Markdown reports with figures and automatic, data-driven interpretation."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from evaluation.comparison import fmt, interpret_metric, trade_off_summary
from evaluation.metrics import METRICS, STAT_METRICS, TABLE_METRICS
from models.energy_model import EnergyModel

SUMMARY_STATS = ["fnd", "hnd", "lnd", "residual_energy_cp", "energy_consumed_cp", "throughput_packets", "pdr",
                 "runtime"]


def md_table(df: pd.DataFrame, index: bool = True, index_label: str = "", floatfmt: str = "{:.4g}") -> str:
    def cell(v):
        if isinstance(v, (float, np.floating)):
            return "n/a" if np.isnan(v) else floatfmt.format(v)
        return str(v).replace("|", "\\|")
    cols = ([index_label] if index else []) + [str(c) for c in df.columns]
    align = ["---:" if pd.api.types.is_numeric_dtype(df[c]) or _numeric_text(df[c]) else "---" for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "|".join(["---"] * (1 if index else 0) + align) + "|"]
    for idx, row in df.iterrows():
        vals = ([cell(idx)] if index else []) + [cell(v) for v in row.values]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def _numeric_text(col: pd.Series) -> bool:
    """Formatted numbers such as '1,234 ± 5' or '≥ 2000' are right-aligned too."""
    s = col.astype(str).str.replace(r"[\s,±≥+\-.%]|n/a", "", regex=True)
    return bool(len(s)) and s.str.fullmatch(r"\d*(e\d+)?").all()


def config_table(cfg) -> str:
    rows = [
        ("Nodes", cfg.n_nodes), ("Area (m)", f"{cfg.area_width:g} x {cfg.area_height:g}"),
        ("BS position", f"({cfg.bs_x:g}, {cfg.bs_y:g})"), ("Initial energy (J/node)", cfg.initial_energy),
        ("Packet size (bits)", cfg.packet_bits), ("Control packet (bits)", cfg.control_bits),
        ("Max rounds", cfg.rounds), ("CH percentage p", cfg.ch_percentage),
        ("CH count tolerance", f"K_opt x (1 ± {cfg.count_tolerance})"),
        ("CH eligibility (optimisers)", f"E ≥ {cfg.ch_energy_threshold} x mean alive energy"),
        ("Optimisation iterations / round", cfg.opt_iterations), ("GWO population", cfg.gwo.population),
        ("ABC colony size (food sources)", f"{cfg.abc.colony_size} ({cfg.abc.colony_size // 2})"),
        ("ABC abandonment limit", cfg.abc.limit),
        ("Hybrid budget share / transfer / feedback",
         f"{cfg.hybrid.budget_share} / {cfg.hybrid.transfer_size} / {cfg.hybrid.feedback}"),
        ("Fitness weights w1..w5", f"{cfg.weights.energy}, {cfg.weights.intra_distance}, "
                                   f"{cfg.weights.ch_bs_distance}, {cfg.weights.balance}, {cfg.weights.ch_count}"),
        ("Radio E_elec / E_fs / E_mp / E_DA", f"{cfg.energy.e_elec:g} / {cfg.energy.e_fs:g} / {cfg.energy.e_mp:g} / "
                                              f"{cfg.energy.e_da:g}"),
        ("Checkpoint round (energy / averages)", cfg.checkpoint_round), ("Base seed", cfg.seed),
    ]
    return md_table(pd.DataFrame({"Value": [str(v) for _, v in rows]}, index=[k for k, _ in rows]),
                    index_label="Parameter")


def stats_tables(stats_df: pd.DataFrame, algorithms, metrics=SUMMARY_STATS) -> str:
    out = []
    for m in metrics:
        sub = stats_df[stats_df["metric"] == m].set_index("algorithm").reindex(algorithms)
        t = pd.DataFrame({k: sub[k].map(lambda v, m=m: fmt(m, v)) for k in ("mean", "std", "min", "max")})
        t.insert(0, "n", sub["n"].astype(int))
        out.append(f"**{METRICS[m].label} ({METRICS[m].unit})**\n\n{md_table(t, index_label='Algorithm')}")
    return "\n\n".join(out)


def improvement_table(cmp: pd.DataFrame) -> str:
    if cmp.empty:
        return "_No proposed algorithm selected._"
    t = cmp[cmp["metric"].isin(TABLE_METRICS + ["node_rounds"])].copy()
    t["direction"] = np.where(t["higher_is_better"], "higher", "lower")
    t["improvement %"] = t["improvement_pct"].map(lambda v: "n/a" if np.isnan(v) else f"{v:+.2f}")
    t["p (Holm)"] = t["p_holm"].map(lambda v: f"{v:.3g}")
    t["Cliff's δ"] = t["cliffs_delta"].map(lambda v: f"{v:+.2f}")
    t = t[["label", "baseline", "direction", "improvement %", "p (Holm)", "Cliff's δ", "effect", "verdict"]]
    t.columns = ["Metric", "Baseline", "Better", "Improvement %", "p (Holm)", "Cliff's δ", "Effect", "Verdict"]
    return md_table(t, index=False)


# ----------------------------------------------------------------------------- figures
def _curve_obs(data: np.ndarray) -> str:
    mean = data.mean(0)
    start, end = mean[0], mean[-1]
    gain = start - end
    if gain <= 0:
        return f"mean best fitness {start:.4f} → {end:.4f} (no improvement)"
    it95 = int(np.argmax(mean <= start - 0.95 * gain))
    return (f"mean best fitness {start:.4f} → {end:.4f} ({100 * gain / start:.1f}% lower); 95% of the "
            f"improvement reached by iteration {it95}")


def make_comparison_figures(res, proposed) -> list[tuple[str, str, str]]:
    """Create every figure; returns (file name, caption, data-driven observation)."""
    from visualization import network_plot as npl
    from visualization.convergence_plot import plot_algorithm_convergence, plot_internal_convergence
    from visualization.performance_plots import (ROUND_PLOTS, mean_round_curves, plot_energy_breakdown,
                                                 plot_lifetime_bars, plot_metric_bars, plot_round_metric)
    from models.network import Network

    out, cfg, algs, runs = res.out_dir, res.config, res.algorithms, res.runs
    n_runs = int(runs["run"].nunique())
    figs: list[tuple[str, str, str]] = []

    # 1. topology (network of run 0)
    net = Network.deploy(cfg, seed=cfg.seed)
    npl.plot_topology(net, out / "01_topology.png", ids=net.n <= 100)
    d0 = EnergyModel(cfg.energy).d0
    figs.append(("01_topology.png", "Initial WSN topology (run 0; every algorithm uses this same network in run 0).",
                 f"{net.n} nodes uniformly deployed in {cfg.area_width:g} x {cfg.area_height:g} m "
                 f"(seed {cfg.seed}); BS at ({cfg.bs_x:g}, {cfg.bs_y:g}). Mean node–BS distance "
                 f"{net.dist_to_bs.mean():.1f} m (max {net.dist_to_bs.max():.1f} m); d0 = {d0:.1f} m, so "
                 f"{100 * (net.dist_to_bs >= d0).mean():.0f}% of nodes would use the multipath (d^4) model "
                 f"for a direct BS transmission."))

    # 2-5. per-algorithm network views (run 0)
    for alg in algs:
        snaps = res.snapshots.get(alg, {})
        slug = alg.replace(" ", "_").replace(">", "").replace("/", "")
        if 1 in snaps:
            s = snaps[1]
            ch = np.flatnonzero(s["is_ch"])
            bs = np.array([cfg.bs_x, cfg.bs_y])
            d_ch = np.linalg.norm(s["positions"][ch] - bs, axis=1) if len(ch) else np.array([np.nan])
            npl.plot_ch_selection(s, out / f"02_ch_selection_{slug}.png", alg)
            npl.plot_clusters(s, out / f"03_clusters_{slug}.png", alg)
            figs.append((f"02_ch_selection_{slug}.png", f"{alg}: cluster heads selected in round 1 (run 0).",
                         f"{len(ch)} CHs; mean CH–BS distance {np.nanmean(d_ch):.1f} m."))
            figs.append((f"03_clusters_{slug}.png", f"{alg}: cluster formation in round 1 (members joined the "
                                                    f"nearest CH).", _cluster_obs(s)))
            if alg == proposed or (proposed not in algs and alg == algs[0]):
                npl.plot_communication(s, out / f"04_communication_{slug}.png", alg)
                figs.append((f"04_communication_{slug}.png", f"{alg}: data communication in round 1 — members "
                             f"send to their CH (grey links), CHs aggregate and forward to the BS (arrows).",
                             _cluster_obs(s)))
        if "hnd" in snaps:
            s = snaps["hnd"]
            npl.plot_dead_nodes(s, out / f"05_dead_nodes_{slug}.png", alg, cfg.initial_energy)
            figs.append((f"05_dead_nodes_{slug}.png", f"{alg}: network at its half-node-death round "
                         f"(run 0); dead nodes are marked x, alive nodes shaded by residual energy.", _dead_obs(s)))

    # 6-8. convergence (round-1 optimisation inside the simulation, all runs)
    for alg in algs:
        curves = res.curves.get(alg)
        if not curves:
            continue
        slug = alg.replace(" ", "_").replace(">", "").replace("/", "")
        keys = list(curves[0])
        same_length = len({len(c[k]) for c in curves for k in keys}) == 1
        if len(keys) > 1 and same_length:            # co-evolutionary hybrid: gwo / abc / hybrid curves
            data = {k: np.array([c[k] for c in curves]) for k in keys}
            plot_internal_convergence(data, out / f"06_convergence_{slug}.png", f"{alg} convergence (round 1)",
                                      n_runs)
            obs = "; ".join(f"{k.upper()}: {_curve_obs(v)}" for k, v in data.items())
        else:
            key = "hybrid" if "hybrid" in keys else keys[0]
            data = np.array([c[key] for c in curves])
            plot_algorithm_convergence({alg: data}, out / f"06_convergence_{slug}.png",
                                       f"{alg} convergence (round 1)", n_runs)
            obs = _curve_obs(data)
        figs.append((f"06_convergence_{slug}.png", f"{alg}: best-so-far fitness per iteration of the round-1 "
                     f"CH optimisation (mean ± std over runs).", obs))

    # 9-16. per-round curves
    curves = mean_round_curves(res.histories)
    curves.to_csv(out / "round_means.csv", index=False)
    s = runs.groupby("algorithm")[STAT_METRICS].mean()
    obs_map = {
        "alive": lambda: "; ".join(f"{a}: FND {s.loc[a, 'fnd']:.0f}, HND {s.loc[a, 'hnd']:.0f}, LND "
                                   f"{s.loc[a, 'lnd']:.0f}" for a in algs),
        "dead": lambda: "Mirror image of the alive-nodes curve; a steeper rise means nodes die closer together.",
        "residual_energy": lambda: "Residual energy at round " + str(cfg.checkpoint_round) + ": " + "; ".join(
            f"{a} {s.loc[a, 'residual_energy_cp']:.2f} J" for a in algs),
        "consumed_energy": lambda: "Consumed by round " + str(cfg.checkpoint_round) + ": " + "; ".join(
            f"{a} {s.loc[a, 'energy_consumed_cp']:.2f} J" for a in algs),
        "packets_delivered": lambda: "Total delivered: " + "; ".join(
            f"{a} {s.loc[a, 'throughput_packets']:,.0f}" for a in algs),
        "pdr": lambda: "Final PDR: " + "; ".join(f"{a} {s.loc[a, 'pdr']:.4f}" for a in algs),
        "ch_count": lambda: "Mean CHs/round (rounds 1–" + str(cfg.checkpoint_round) + "): " + "; ".join(
            f"{a} {s.loc[a, 'avg_ch_count']:.2f} (per-round std {_ch_std(res.histories, a, cfg):.2f})"
            for a in algs),
        "avg_intra_distance": lambda: "Mean member→CH distance: " + "; ".join(
            f"{a} {s.loc[a, 'avg_cluster_distance']:.2f} m" for a in algs),
    }
    s["avg_ch_count"] = runs.groupby("algorithm")["avg_ch_count"].mean()
    for i, col in enumerate(ROUND_PLOTS, start=9):
        name = f"{i:02d}_{col}_vs_rounds.png"
        plot_round_metric(curves, col, algs, out / name, n_runs=n_runs)
        figs.append((name, ROUND_PLOTS[col][1] + ".", obs_map[col]()))

    # 17-18 + extras
    plot_metric_bars(runs, "runtime", algs, out / "17_runtime.png", "CH-selection runtime per simulation", log=True)
    figs.append(("17_runtime.png", "Total CH-selection runtime per simulation (log scale, mean ± std).",
                 "; ".join(f"{a} {s.loc[a, 'runtime']:.2f} s ({s.loc[a, 'runtime_per_round']:.2f} ms/round, "
                           f"{s.loc[a, 'evaluations']:,.0f} fitness evaluations)" for a in algs)))
    plot_lifetime_bars(runs, algs, out / "18_lifetime_fnd_hnd_lnd.png")
    figs.append(("18_lifetime_fnd_hnd_lnd.png", "FND / HND / LND comparison (mean ± std over runs).",
                 obs_map["alive"]()))
    plot_energy_breakdown(res.histories, algs, out / "19_energy_breakdown.png", cfg.checkpoint_round)
    figs.append(("19_energy_breakdown.png", "Where the energy goes: mean energy per radio activity over "
                 f"rounds 1–{cfg.checkpoint_round}.", _breakdown_obs(res.histories, algs, cfg.checkpoint_round)))
    plot_metric_bars(runs, "final_fitness", algs, out / "20_final_fitness.png",
                     "Mean per-round fitness of the CH sets used (lower = better)")
    figs.append(("20_final_fitness.png", "Final fitness: same objective and weights for every algorithm.",
                 "; ".join(f"{a} {s.loc[a, 'final_fitness']:.4f}" for a in algs)))
    return figs


def _ch_std(hist, alg, cfg):
    h = hist[(hist["algorithm"] == alg) & (hist["round"] <= cfg.checkpoint_round)]
    return float(h["ch_count"].std())


def _cluster_obs(s: dict) -> str:
    ch = np.flatnonzero(s["is_ch"])
    if not len(ch):
        return "No CH elected in this round: every alive node transmitted directly to the BS."
    members = np.flatnonzero(s["alive"] & ~s["is_ch"] & (s["cluster_id"] >= 0))
    d = np.linalg.norm(s["positions"][members] - s["positions"][s["cluster_id"][members]], axis=1)
    sizes = np.array([1 + np.sum(s["cluster_id"][members] == c) for c in ch])
    return (f"{len(ch)} clusters, sizes {sizes.min()}–{sizes.max()} (CV {sizes.std() / sizes.mean():.2f}); "
            f"member→CH distance mean {d.mean():.1f} m, max {d.max():.1f} m.")


def _dead_obs(s: dict) -> str:
    bs = s["bs"]
    dist = np.linalg.norm(s["positions"] - bs, axis=1)
    dead, alive = ~s["alive"], s["alive"]
    txt = f"Round {s['round']}: {dead.sum()} dead, {alive.sum()} alive."
    if dead.any() and alive.any():
        txt += (f" Mean distance to BS — dead nodes {dist[dead].mean():.1f} m, alive nodes {dist[alive].mean():.1f}"
                f" m ({'far' if dist[dead].mean() > dist[alive].mean() else 'near'} nodes died first on average).")
    return txt


def _breakdown_obs(hist, algs, cp):
    parts = {"e_member_tx": "member TX", "e_ch_rx": "CH RX", "e_aggregation": "aggregation", "e_ch_tx": "CH→BS TX",
             "e_direct_tx": "direct TX"}
    h = hist[hist["round"] <= cp]
    per = h.groupby(["algorithm", "run"])[list(parts)].sum().groupby("algorithm").mean()
    out = []
    for a in algs:
        row = per.loc[a]
        tot = row.sum()
        top = row.idxmax()
        out.append(f"{a}: total {tot:.2f} J, largest share {parts[top]} ({100 * row[top] / tot:.0f}%)")
    return "; ".join(out)


# ----------------------------------------------------------------------------- reports
def write_comparison_report(res, title: str, description: str = "", proposed: str | None = None) -> Path:
    figs = make_comparison_figures(res, proposed)
    cfg, algs, runs = res.config, res.algorithms, res.runs
    n_runs = int(runs["run"].nunique())
    parts = [f"# {title}", "", description, "",
             f"All numbers below were produced by the simulator in this folder ({n_runs} independent paired runs "
             f"per algorithm; run r uses deployment/algorithm seed {cfg.seed} + r). Raw per-run results: "
             f"`runs_raw.csv`; per-round histories: `history_raw.csv.gz`; statistics: `statistics.csv`; "
             f"proposed-vs-baseline tests: `improvement_vs_baselines.csv`.", "",
             "## Configuration", "", config_table(cfg), "",
             "## Final result table (mean ± std over runs)", "",
             md_table(res.table, index_label="Metric"), "",
             f"Residual energy and energy consumption are measured at the checkpoint round {cfg.checkpoint_round}; "
             f"distance, imbalance and fitness averages cover rounds 1–{cfg.checkpoint_round}. "
             f"'≥' marks lifetime values where at least one run had not reached the event within "
             f"{cfg.rounds} rounds (the horizon is then used as a lower bound).", "",
             "## Descriptive statistics", "", stats_tables(res.stats, algs), ""]
    if proposed and proposed in algs:
        parts += [f"## {proposed} vs baselines", "",
                  "Improvement % uses ((P − B) / B) × 100 for higher-is-better metrics and ((B − P) / B) × 100 for "
                  "lower-is-better metrics, so a positive value always means the proposed algorithm did better. "
                  "p-values: paired two-sided Wilcoxon signed-rank test, Holm-corrected over the baselines. "
                  "Cliff's δ > 0 favours the proposed algorithm (|δ| < 0.147 negligible, < 0.33 small, "
                  "< 0.474 medium, otherwise large).", "",
                  improvement_table(res.comparison), "", "### Trade-offs", "",
                  trade_off_summary(res.comparison, proposed), ""]
    parts += ["## Figures", ""]
    for name, caption, obs in figs:
        parts += [f"### {caption}", "", f"![{caption}]({name})", "", f"**Observed:** {obs}", ""]
    parts += ["## Metric-by-metric interpretation", ""]
    for m in TABLE_METRICS + ["node_rounds", "cluster_imbalance"]:
        parts += [interpret_metric(m, runs, res.comparison, proposed, algs), ""]
    if getattr(res, "ch_log", None) is not None and len(res.ch_log):
        parts += [ch_section(res.ch_log, algs), ""]
    parts += ["## Reproducing this experiment", "",
              "```", f"python main.py reproduce \"{res.out_dir}\"", "```", "",
              "`config.json` holds every parameter; `experiment.json` holds the algorithms, run count and seeds.", ""]
    path = res.out_dir / "report.md"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


CH_HEADING = "## Cluster-head records (run 0)"


def ch_section(ch_log: pd.DataFrame, algorithms, check: pd.DataFrame | None = None) -> str:
    """Markdown: per algorithm, the round-1 CH table and CH statistics over the whole run (from ch_log)."""
    lines = [CH_HEADING, "",
             "Every selected CH of every round is recorded in `ch_log_run0.csv` (round, CH id, coordinates, residual "
             "energy at selection, distance to the BS, cluster size including the CH). Dead and duplicate CHs are "
             "removed before clustering, so only valid CHs appear.", ""]
    if check is not None and len(check):
        ok = bool(check["identical"].all())
        lines += [f"**Reproducibility check:** run 0 of every algorithm was re-simulated from `config.json` and its "
                  f"seed; {'all' if ok else 'NOT all'} checked results ({', '.join(check['field'].unique())}) are "
                  f"{'identical to' if ok else 'different from'} the saved values "
                  f"(`reproducibility_check_run0.csv`).", ""]
    for alg in algorithms:
        g = ch_log[ch_log["algorithm"] == alg]
        if g.empty:
            continue
        per_round = g.groupby("round")
        times = g["ch_id"].value_counts()
        lines += [f"### {alg}", "",
                  f"Over {g['round'].nunique()} rounds with CHs: {per_round.size().mean():.2f} CHs/round on average; "
                  f"mean CH residual energy at selection {g['residual_energy'].mean():.4f} J; mean CH–BS distance "
                  f"{g['distance_to_bs'].mean():.2f} m; {len(times)} distinct nodes served as CH, the most frequent "
                  f"one {times.iloc[0]} times.", ""]
        first = g[g["round"] == g["round"].min()][["ch_id", "x", "y", "residual_energy", "distance_to_bs",
                                                    "cluster_size"]]
        first = first.rename(columns={"ch_id": "CH id", "x": "x (m)", "y": "y (m)",
                                      "residual_energy": "Residual energy (J)", "distance_to_bs": "CH–BS (m)",
                                      "cluster_size": "Cluster size"})
        lines += [f"Round {g['round'].min()} cluster heads:", "",
                  md_table(first.set_index("CH id"), index_label="CH id", floatfmt="{:.4g}"), ""]
    return "\n".join(lines)


def _put_section(text: str, heading: str, content: str, before: str = "## Reproducing this experiment") -> str:
    """Insert (or replace) a '## ' section, placed before the ``before`` heading when present."""
    start = text.find(heading)
    if start >= 0:                                     # replace the existing section
        nxt = text.find("\n## ", start + len(heading))
        text = text[:start] + (text[nxt + 1:] if nxt >= 0 else "")
    pos = text.find(before)
    if pos < 0:
        return text.rstrip() + "\n\n" + content + "\n"
    return text[:pos] + content + "\n\n" + text[pos:]


def append_ch_section(folder, ch_log: pd.DataFrame, check: pd.DataFrame | None, algorithms) -> None:
    report = Path(folder) / "report.md"
    text = report.read_text(encoding="utf-8")
    report.write_text(_put_section(text, CH_HEADING, ch_section(ch_log, algorithms, check)), encoding="utf-8")


OUTLIER_FACTOR = 1.5   # timing > 1.5 x the median of the same algorithm and size is flagged as disturbed


def runtime_outliers(df: pd.DataFrame) -> pd.DataFrame:
    med = df.groupby(["n_nodes", "algorithm"])["ms_per_round"].transform("median")
    return df[(df["ms_per_round"] > OUTLIER_FACTOR * med) & (med > 0.5)]


def write_runtime_report(out_dir: Path, df: pd.DataFrame, algorithms, rounds: int) -> Path:
    """Median over seeds is the headline statistic (robust to transient OS interference); mean ± std shown too."""
    from evaluation.statistics import paired_test
    g = df.groupby(["n_nodes", "algorithm"], sort=False).agg(ms_median=("ms_per_round", "median"),
                                                             ms_mean=("ms_per_round", "mean"),
                                                             ms_std=("ms_per_round", "std"),
                                                             evals=("evals_per_round", "mean")).reset_index()
    t = g.pivot(index="algorithm", columns="n_nodes", values="ms_median").reindex(algorithms)
    t.columns = [f"{c} nodes (median ms/round)" for c in t.columns]
    g["mean_std"] = [f"{m:.2f} ± {s:.2f}" for m, s in zip(g["ms_mean"], g["ms_std"].fillna(0))]
    ms = g.pivot(index="algorithm", columns="n_nodes", values="mean_std").reindex(algorithms)
    ms.columns = [f"{c} nodes (mean ± std)" for c in ms.columns]
    e = g.pivot(index="algorithm", columns="n_nodes", values="evals").reindex(algorithms)
    e.columns = [f"{c} nodes (evals/round)" for c in e.columns]
    n_seeds = df["seed"].nunique()
    lines = ["# Runtime benchmark", "",
             f"CH-selection wall-clock time per round, measured sequentially in one process (no parallel load), "
             f"over the first {rounds} rounds of identical networks ({n_seeds} seeds); the algorithm order is "
             f"rotated per seed. This is the authoritative runtime comparison: scenario runtimes were measured with "
             f"11 simulations running in parallel. The median over seeds is the headline value because it is robust "
             f"to transient interference from other software; mean ± std is shown for completeness. "
             f"Raw data: `runtime_raw.csv`.", "",
             md_table(t, index_label="Algorithm", floatfmt="{:.2f}"), "",
             md_table(ms, index_label="Algorithm"), "",
             md_table(e, index_label="Algorithm", floatfmt="{:.1f}"), "",
             "![runtime](runtime_benchmark.png)", ""]
    obs = []
    if "Hybrid GWO-ABC" in algorithms:
        for n in sorted(df["n_nodes"].unique()):
            sub = df[df["n_nodes"] == n]
            h = sub[sub["algorithm"] == "Hybrid GWO-ABC"].set_index("seed")["ms_per_round"]
            for base in ("GWO", "ABC"):
                b = sub[sub["algorithm"] == base].set_index("seed")["ms_per_round"].reindex(h.index)
                obs.append(f"{n} nodes: Hybrid {h.median():.1f} ms vs {base} {b.median():.1f} ms per round "
                           f"(median ratio ×{h.median() / b.median():.2f}; Hybrid slower on "
                           f"{int((h.values > b.values).sum())}/{len(h)} seeds, Wilcoxon p = "
                           f"{paired_test(h.values, b.values):.3g}).")
    lines += ["**Observed:** " + " ".join(obs), "",
              f"With {n_seeds} paired seeds the smallest possible two-sided Wilcoxon p-value is "
              f"{2 / 2 ** n_seeds:.4f}, so these timing differences cannot reach p < 0.05 even when the hybrid is "
              "slower on every seed; the per-seed counts above show how consistent the direction is.", "",
              "All three optimisers spend about the same number of fitness evaluations per round; the hybrid's "
              "extra time comes from running two populations and more operators (transfer, duplicate checks) per "
              "iteration in Python.", ""]
    bad = runtime_outliers(df)
    if len(bad):
        items = "; ".join(f"{r.algorithm}, {r.n_nodes} nodes, seed {r.seed}: {r.ms_per_round:.1f} ms"
                          for r in bad.itertuples())
        lines += ["**Data-quality note:** timings above "
                  f"{OUTLIER_FACTOR}× the median of the same algorithm and size (most likely disturbed by other "
                  f"activity on the computer; they are visible as outlying dots in the figure): {items}. They are "
                  "kept in the raw data and in the mean ± std table; the medians are barely affected.", ""]
    path = out_dir / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def flag_runtime_outliers(folder, factor: float = 3.0) -> list:
    """Append a data-quality note listing runs whose runtime/round exceeds ``factor`` x the algorithm median.

    Such runs were timed while the computer slept or was heavily loaded; their raw values are kept unchanged.
    """
    folder = Path(folder)
    runs = pd.read_csv(folder / "runs_raw.csv")
    med = runs.groupby("algorithm")["runtime_per_round"].transform("median")
    bad = runs[(runs["runtime_per_round"] > factor * med) & (med > 0.5)]
    report = folder / "report.md"
    text = report.read_text(encoding="utf-8")
    marker = "## Data-quality note"
    if marker in text:                                    # replace only this section, keep anything after it
        start = text.find(marker)
        nxt = text.find("\n## ", start + len(marker))
        text = text[:start].rstrip() + "\n" + (text[nxt:] if nxt >= 0 else "")
    note = [marker, "",
            "Runtime values in this folder were measured with 11 simulations running in parallel, so they include "
            "scheduling noise; see `results/runtime_benchmark/report.md` for a clean sequential runtime comparison."]
    if len(bad):
        items = ", ".join(f"{r.algorithm} run {r.run} ({r.runtime_per_round:.0f} ms/round vs median "
                          f"{m:.0f})" for r, m in zip(bad.itertuples(), med[bad.index]))
        note.append(f"Runs with runtime/round > {factor:g}× their algorithm's median (most likely timed across a "
                    f"system sleep): {items}. Their raw values are kept unchanged; only runtime metrics are affected "
                    f"(energy, lifetime and packet metrics count rounds, not seconds).")
    report.write_text(text.rstrip() + "\n\n" + "\n".join(note) + "\n", encoding="utf-8")
    return bad[["algorithm", "run"]].values.tolist()


def refresh_tradeoffs(folder) -> bool:
    """Regenerate the trade-off section of an existing report.md from its improvement_vs_baselines.csv."""
    import json
    folder = Path(folder)
    report, csv = folder / "report.md", folder / "improvement_vs_baselines.csv"
    if not report.exists() or not csv.exists():
        return False
    cmp = pd.read_csv(csv)
    if cmp.empty:
        return False
    proposed = json.loads((folder / "experiment.json").read_text()).get("proposed")
    text = report.read_text(encoding="utf-8")
    start, end = text.find("### Trade-offs"), text.find("## Figures")
    if start < 0 or end < 0:
        return False
    new = f"### Trade-offs\n\n{trade_off_summary(cmp, proposed)}\n\n"
    report.write_text(text[:start] + new + text[end:], encoding="utf-8")
    return True


def scenario_overview(results: dict) -> str:
    lines = ["# Scenario overview", "",
             "Mean over runs for each scenario (full details, statistics and figures in each scenario folder).", ""]
    for name, res in results.items():
        means = res.runs.groupby("algorithm", sort=False)[["fnd", "hnd", "lnd", "residual_energy_cp",
                                                           "throughput_packets", "pdr", "runtime"]].mean()
        means = means.reindex(res.algorithms)
        means.columns = [METRICS[c].label for c in means.columns]
        lines += [f"## {name}", "", f"_{res.runs['run'].nunique()} runs._ [report]({name}/report.md)", "",
                  md_table(means, index_label="Algorithm", floatfmt="{:,.4g}"), ""]
        cmp = res.comparison
        if not cmp.empty:
            lines += [trade_off_summary(cmp[cmp["metric"].isin(TABLE_METRICS)], "Hybrid GWO-ABC"), ""]
    return "\n".join(lines)


def rebuild_scenario_overview(root) -> str:
    """Rebuild results/scenarios/README.md from the saved CSVs of every scenario folder."""
    import json
    from types import SimpleNamespace
    root = Path(root)
    results = {}
    for folder in sorted(p for p in root.iterdir()
                         if (p / "runs_raw.csv").exists() and not p.name.endswith("_reproduced")):
        meta = json.loads((folder / "experiment.json").read_text())
        results[folder.name] = SimpleNamespace(runs=pd.read_csv(folder / "runs_raw.csv"),
                                               algorithms=meta["algorithms"],
                                               comparison=pd.read_csv(folder / "improvement_vs_baselines.csv"))
    text = scenario_overview(results)
    (root / "README.md").write_text(text, encoding="utf-8")
    return text


def write_sensitivity_report(out_dir: Path, agg: pd.DataFrame, factors, figures: dict, runs: int) -> Path:
    from experiments.experiment_runner import SENSITIVITY
    lines = ["# Sensitivity analysis", "",
             f"One factor is varied at a time around the default configuration; {runs} paired runs per setting "
             "(mean ± std). Raw data: `sensitivity_runs_raw.csv`, aggregated: `sensitivity_summary.csv`.", ""]
    for factor in factors:
        values, _, algs, label = SENSITIVITY[factor]
        sub = agg[agg["factor"] == factor]
        lines += [f"## {label}", ""]
        t = pd.DataFrame({
            "Setting": sub["value"].astype(str), "Algorithm": sub["algorithm"],
            **{METRICS[m].label: [f"{a:.4g} ± {b:.2g}" for a, b in zip(sub[f"{m}_mean"], sub[f"{m}_std"])]
               for m in ("fnd", "hnd", "lnd", "throughput_packets", "pdr", "runtime")}})
        lines += [md_table(t, index=False), ""]
        for f in figures.get(factor, []):
            lines += [f"![{factor}]({f})", ""]
        lines += [_sensitivity_obs(sub, values, algs), ""]
    path = out_dir / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _sensitivity_obs(sub: pd.DataFrame, values, algs) -> str:
    out = []
    for alg in algs:
        g = sub[sub["algorithm"] == alg].set_index("value")
        g = g.reindex([str(v) for v in values])
        if g["fnd_mean"].isna().all():
            continue
        best = g["fnd_mean"].idxmax()
        worst = g["fnd_mean"].idxmin()
        out.append(f"{alg}: FND ranges from {g['fnd_mean'].min():.0f} (at {worst}) to {g['fnd_mean'].max():.0f} "
                   f"(at {best}); throughput {g['throughput_packets_mean'].min():,.0f}–"
                   f"{g['throughput_packets_mean'].max():,.0f} packets.")
    # ranking stability
    ranks = []
    for v in values:
        g = sub[sub["value"] == str(v)].set_index("algorithm")["fnd_mean"]
        if len(g) > 1:
            ranks.append(f"{v}: {g.idxmax()}")
    if ranks:
        out.append("Highest FND per setting — " + "; ".join(ranks) + ".")
    return "**Observed:** " + " ".join(out)


def write_convergence_report(out_dir: Path, df: pd.DataFrame, figures: dict, cfg) -> Path:
    lines = ["# Convergence analysis", "",
             f"GWO (population {cfg.gwo.population}), ABC (colony {cfg.abc.colony_size}) and Hybrid GWO-ABC "
             f"(budget share {cfg.hybrid.budget_share}) optimise the CH set of identical network states for "
             f"{cfg.opt_iterations} iterations with comparable fitness-evaluation budgets. Curves are best-so-far "
             f"fitness (lower = better); raw data in `convergence_runs_raw.csv` and `curves_*.csv`.", ""]
    for state, figs in figures.items():
        sub = df[df["state_round"] == state]
        state_txt = "fresh network (round 0)" if not state else f"network after {state} LEACH rounds"
        g = sub.groupby("algorithm", sort=False).agg(initial=("initial_fitness", "mean"),
                                                     final=("final_fitness", "mean"),
                                                     final_std=("final_fitness", "std"),
                                                     evaluations=("evaluations", "mean"),
                                                     time_ms=("time_s", lambda v: 1000 * v.mean()))
        lines += [f"## {state_txt}", "", md_table(g, index_label="Algorithm"), ""]
        for key in ("gwo", "abc", "hybrid", "all"):
            lines += [f"![{key}]({figs[key]})", ""]
        from evaluation.statistics import paired_test
        h = sub[sub["algorithm"] == "Hybrid GWO-ABC"].set_index("run")["final_fitness"]
        obs = []
        for base in ("GWO", "ABC"):
            b = sub[sub["algorithm"] == base].set_index("run")["final_fitness"]
            p = paired_test(h.values, b.reindex(h.index).values)
            diff = 100 * (b.mean() - h.mean()) / b.mean()
            obs.append(f"Hybrid final fitness is {abs(diff):.2f}% {'lower (better)' if diff > 0 else 'higher (worse)'}"
                       f" than {base} (Wilcoxon p = {p:.3g}).")
        lines += ["**Observed:** " + " ".join(obs), ""]
    path = out_dir / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
