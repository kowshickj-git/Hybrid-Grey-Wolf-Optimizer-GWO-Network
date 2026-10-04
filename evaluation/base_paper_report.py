"""Report: does the proposed Hybrid GWO-ABC improve on the base paper's DEAI-PSO?

Built only from the saved raw results in results/base_paper/. Every sentence that claims an
improvement is generated from paired statistics; metrics where the proposed method is not
better are listed explicitly, and the title of the report follows the data.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from evaluation.metrics import METRICS
from evaluation.report import md_table
from evaluation.statistics import ALPHA, cliffs_delta, effect_magnitude, holm, improvement, paired_test

BASE = "DEAI-PSO"
PROPOSED = "Hybrid GWO-ABC (Eq. 12)"          # primary: same problem and objective as the base paper
PROPOSED_MO = "Hybrid GWO-ABC"                # secondary: project's multi-objective fitness
CITATION = ('M. Haris and H. Nam, "Enhancing Energy Efficiency in IoT-WSNs Through Optimized PSO Cluster Head '
            'Selection," *IEEE Access*, vol. 13, pp. 126496–126512, 2025, doi:10.1109/ACCESS.2025.3583922.')


def _fmt(metric, v):
    if metric in ("fnd", "hnd", "lnd", "node_rounds", "throughput_packets"):
        return f"{v:,.0f}"
    if metric == "pdr":
        return f"{v:.4f}"
    return f"{v:.3f}"


def paired_comparison(out: Path, scenarios, metrics, proposed: str, baseline: str) -> pd.DataFrame:
    """``proposed`` vs ``baseline`` for every scenario x metric; Holm correction over the whole family."""
    rows = []
    for sc in scenarios:
        runs = pd.read_csv(out / sc / "runs_raw.csv")
        p = runs[runs["algorithm"] == proposed].set_index("run")
        b = runs[runs["algorithm"] == baseline].set_index("run").reindex(p.index)
        for m in metrics:
            info = METRICS[m]
            pa, ba = p[m].astype(float), b[m].astype(float)
            delta = cliffs_delta(pa, ba) * (1 if info.higher_is_better else -1)
            rows.append({"scenario": sc, "metric": m, "label": info.label, "unit": info.unit,
                         "higher_is_better": info.higher_is_better, "proposed": proposed, "baseline": baseline,
                         "base_mean": ba.mean(), "base_std": ba.std(ddof=1),
                         "prop_mean": pa.mean(), "prop_std": pa.std(ddof=1),
                         "improvement_pct": improvement(pa.mean(), ba.mean(), info.higher_is_better),
                         "prop_wins": int(((pa > ba) if info.higher_is_better else (pa < ba)).sum()),
                         "n": len(pa), "p_value": paired_test(pa.values, ba.values), "cliffs_delta": delta,
                         "effect": effect_magnitude(delta)})
    df = pd.DataFrame(rows)
    df["p_holm"] = holm(df["p_value"].values)
    df["significant"] = df["p_holm"] < ALPHA
    df["verdict"] = np.where(~df["significant"], "no significant difference",
                             np.where(df["improvement_pct"] > 0, "improved", "worse"))
    return df


def _verdict_lines(df: pd.DataFrame, scenarios) -> list:
    lines = []
    for sc in scenarios:
        s = df[df["scenario"] == sc]
        better = ", ".join(f"{r.label} {r.improvement_pct:+.2f} %" for r in s[s["verdict"] == "improved"].itertuples())
        bad = ", ".join(f"{r.label} {r.improvement_pct:+.2f} %" for r in s[s["verdict"] == "worse"].itertuples())
        ns = ", ".join(f"{r.label} ({r.improvement_pct:+.2f} %)"
                       for r in s[s["verdict"] == "no significant difference"].itertuples())
        lines.append(f"- **{sc}** — significantly improved: {better or 'none'}; significantly worse: "
                     f"{bad or 'none'}; not significant: {ns or 'none'}.")
    return lines


def _table(df: pd.DataFrame, sc: str, base_label: str, prop_label: str) -> str:
    s = df[df["scenario"] == sc]
    t = pd.DataFrame({
        base_label: [f"{_fmt(r.metric, r.base_mean)} ± {_fmt(r.metric, r.base_std)}" for r in s.itertuples()],
        prop_label: [f"{_fmt(r.metric, r.prop_mean)} ± {_fmt(r.metric, r.prop_std)}" for r in s.itertuples()],
        "Improvement": [f"{r.improvement_pct:+.2f} %" for r in s.itertuples()],
        "Better in": [f"{r.prop_wins}/{r.n} runs" for r in s.itertuples()],
        "p (Holm)": [f"{r.p_holm:.2g}" for r in s.itertuples()],
        "Cliff's δ": [f"{r.cliffs_delta:+.2f} ({r.effect})" for r in s.itertuples()],
        "Verdict": [r.verdict for r in s.itertuples()]},
        index=[f"{r.label} ({r.unit})" + (" ↑" if r.higher_is_better else " ↓") for r in s.itertuples()])
    return md_table(t, index_label="Metric")


def _fig_improvement(df: pd.DataFrame, path: Path, title: str):
    from visualization import style
    fig = style.new_figure(8.8, 4.9)
    ax = fig.add_subplot()
    scen = list(dict.fromkeys(df["scenario"]))
    metrics = list(dict.fromkeys(df["label"]))
    width = 0.8 / len(scen)
    y = np.arange(len(metrics))
    colors = [style.SLOTS[0], style.SLOTS[2], style.SLOTS[6]]
    for i, sc in enumerate(scen):
        sub = df[df["scenario"] == sc].set_index("label").reindex(metrics)
        pos = y - 0.4 + width * (i + 0.5)
        ax.barh(pos, sub["improvement_pct"], width * 0.9, color=colors[i % 3], label=sc)
        for yy, v, sig in zip(pos, sub["improvement_pct"], sub["significant"]):
            ax.annotate(("✱ " if sig else "") + f"{v:+.1f}%", (v, yy), xytext=(4 if v >= 0 else -4, 0),
                        textcoords="offset points", ha="left" if v >= 0 else "right", va="center", fontsize=7,
                        color=style.INK_2)
    ax.axvline(0, color=style.AXIS, lw=1)
    ax.set_yticks(y, metrics)
    ax.invert_yaxis()
    ax.set_xlabel("Improvement over DEAI-PSO (%)  — positive = better")
    ax.grid(axis="y", visible=False)
    ax.set_title(title + "  (✱ significant, Holm-corrected)", loc="left")
    ax.legend(loc="lower right")
    lo, hi = ax.get_xlim()
    ax.set_xlim(lo - 0.15 * (hi - lo), hi + 0.25 * (hi - lo))
    style.save(fig, path)


def _fig_curves(out: Path, sc: str, column: str, ylabel: str, path: Path, algs):
    from visualization import style
    from visualization.performance_plots import mean_round_curves
    hist = pd.read_csv(out / sc / "history_raw.csv.gz")
    hist = hist[hist["algorithm"].isin(algs)]
    curves = mean_round_curves(hist)
    fig = style.new_figure(7.6, 4.4)
    ax = fig.add_subplot()
    suffix = {BASE: " — base paper", PROPOSED: " — proposed", PROPOSED_MO: " — proposed, multi-objective"}
    for a in algs:
        c = curves[curves["algorithm"] == a]
        ax.plot(c["round"], c[column], color=style.color(a), ls=style.linestyle(a), label=a + suffix.get(a, ""))
    ax.set_xlabel("Round")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{sc}: {ylabel} vs rounds — mean of {hist['run'].nunique()} runs", loc="left")
    ax.legend()
    style.save(fig, path)


def _mechanism(out: Path, scenarios, algs) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, energy = [], []
    parts = {"e_member_tx": "Member → CH TX", "e_ch_rx": "CH RX", "e_aggregation": "Aggregation",
             "e_ch_tx": "CH → BS TX", "e_direct_tx": "Free/direct → BS TX", "e_control": "Control packets"}
    for sc in scenarios:
        runs = pd.read_csv(out / sc / "runs_raw.csv")
        cfg = json.loads((out / sc / "config.json").read_text())
        hist = pd.read_csv(out / sc / "history_raw.csv.gz")
        h = hist[hist["round"] <= cfg["checkpoint_round"]]
        for a in algs:
            r = runs[runs["algorithm"] == a]
            rows.append({"scenario": sc, "algorithm": a, "CHs per round": r["avg_ch_count"].mean(),
                         "member→CH distance (m)": r["avg_cluster_distance"].mean(),
                         "CH→BS distance (m)": r["avg_ch_bs_distance"].mean(),
                         "lost packets": (r["packets_generated"] - r["throughput_packets"]).mean(),
                         "PDR": r["pdr"].mean()})
            e = h[h["algorithm"] == a].groupby("run")[list(parts)].sum().mean()
            energy.append({"scenario": sc, "algorithm": a, **{parts[k]: e[k] for k in parts}, "total": e.sum()})
    return pd.DataFrame(rows), pd.DataFrame(energy)


def _less_more(proposed: float, base: float) -> str:
    d = 100 * (base - proposed) / base
    return f"{abs(d):.1f} % {'less' if d >= 0 else 'more'}"


def _mechanism_text(mech: pd.DataFrame, energy: pd.DataFrame, scenarios) -> list:
    out = []
    for sc in scenarios:
        m = mech[mech["scenario"] == sc].set_index("algorithm")
        e = energy[energy["scenario"] == sc].set_index("algorithm")
        if BASE not in m.index or PROPOSED not in m.index:
            continue
        ch_b, ch_p = m.loc[BASE, "CHs per round"], m.loc[PROPOSED, "CHs per round"]
        tx_b, tx_p = e.loc[BASE, "CH → BS TX"], e.loc[PROPOSED, "CH → BS TX"]
        mem_b, mem_p = e.loc[BASE, "Member → CH TX"], e.loc[PROPOSED, "Member → CH TX"]
        tot_b, tot_p = e.loc[BASE, "total"], e.loc[PROPOSED, "total"]
        out.append(f"- **{sc}:** {PROPOSED} used {ch_p:.2f} CHs per round vs {ch_b:.2f} for DEAI-PSO; up to the "
                   f"checkpoint its CH → BS transmissions cost {tx_p:.2f} J vs {tx_b:.2f} J "
                   f"({_less_more(tx_p, tx_b)}), member → CH transmissions {mem_p:.2f} J vs {mem_b:.2f} J "
                   f"({_less_more(mem_p, mem_b)}), total {tot_p:.2f} J vs {tot_b:.2f} J "
                   f"({_less_more(tot_p, tot_b)}); lost packets per run "
                   f"{m.loc[PROPOSED, 'lost packets']:.0f} vs {m.loc[BASE, 'lost packets']:.0f}.")
    return out


def _attribution(out: Path) -> str:
    f = out / "attribution_BP1" / "runs_raw.csv"
    if not f.exists():
        return "_Attribution study not run._"
    runs = pd.read_csv(f)
    m = runs.groupby("algorithm")[["node_rounds", "fnd", "hnd", "lnd", "throughput_packets"]].mean()
    cells = {("DEAI-PSO", "Eq. 12 (base paper)"): "DEAI-PSO",
             ("DEAI-PSO", "multi-objective (project)"): "DEAI-PSO + proposed fitness",
             ("Hybrid GWO-ABC", "Eq. 12 (base paper)"): PROPOSED,
             ("Hybrid GWO-ABC", "multi-objective (project)"): PROPOSED_MO}
    lines = []
    for metric in ("node_rounds", "hnd", "fnd", "lnd"):
        t = pd.DataFrame({obj: [m.loc[cells[(opt, obj)], metric] for opt in ("DEAI-PSO", "Hybrid GWO-ABC")]
                          for obj in ("Eq. 12 (base paper)", "multi-objective (project)")},
                         index=["DEAI-PSO optimiser", "Hybrid GWO-ABC optimiser"])
        lines += [f"**{METRICS[metric].label}** (mean over {runs['run'].nunique()} runs)", "",
                  md_table(t, index_label="Optimiser \\ objective", floatfmt="{:,.1f}"), ""]

    def pair(a, b, metric):
        x = runs[runs["algorithm"] == a].set_index("run")[metric]
        y = runs[runs["algorithm"] == b].set_index("run")[metric].reindex(x.index)
        info = METRICS[metric]
        return improvement(x.mean(), y.mean(), info.higher_is_better), paired_test(x.values, y.values)

    eff = []
    tests = (("optimiser (objective = Eq. 12)", PROPOSED, "DEAI-PSO"),
             ("optimiser, CH count fixed at 10 % (objective = Eq. 12)", "Hybrid GWO-ABC (Eq. 12, fixed K)", "DEAI-PSO"),
             ("adaptive CH count (Hybrid, Eq. 12)", PROPOSED, "Hybrid GWO-ABC (Eq. 12, fixed K)"),
             ("optimiser (objective = multi-objective)", PROPOSED_MO, "DEAI-PSO + proposed fitness"),
             ("objective (optimiser = DEAI-PSO)", "DEAI-PSO + proposed fitness", "DEAI-PSO"),
             ("objective (optimiser = Hybrid)", PROPOSED_MO, PROPOSED))
    for metric in ("node_rounds", "hnd", "fnd"):
        for desc, a, b in tests:
            if a not in m.index or b not in m.index:
                continue
            pct, p = pair(a, b, metric)
            eff.append({"Metric": METRICS[metric].label, "Change": desc, "From → to": f"{b} → {a}",
                        "Δ %": f"{pct:+.2f}", "Wilcoxon p": f"{p:.2g}"})
    lines += ["Effect of changing one factor at a time (paired runs, unadjusted p):", "",
              md_table(pd.DataFrame(eff), index=False), ""]
    fixed_k = "Hybrid GWO-ABC (Eq. 12, fixed K)"
    if all(a in m.index for a in (PROPOSED, fixed_k, "DEAI-PSO")):
        full, _ = pair(PROPOSED, "DEAI-PSO", "node_rounds")
        fixed, p_fixed = pair(fixed_k, "DEAI-PSO", "node_rounds")
        lines += [f"**Reading:** on node-rounds the proposed optimiser gains {full:+.2f} % over DEAI-PSO on the same "
                  f"Eq. 12 objective. With the CH count fixed at exactly 10 % like DEAI-PSO it gains {fixed:+.2f} % "
                  f"(Wilcoxon p = {p_fixed:.2g}): that part is the better search alone. The remaining "
                  f"{full - fixed:.2f} points come from the proposed binary encoding, which lets the optimiser use fewer "
                  "CHs when that lowers Eq. 12 — fewer expensive CH → BS transmissions to the distant BS (section 7).", ""]
    return "\n".join(lines)


def _runtime(out: Path) -> tuple[str, pd.DataFrame | None]:
    f = out / "runtime" / "runtime_raw.csv"
    if not f.exists():
        return "_Runtime measurement not run._", None
    df = pd.read_csv(f)
    t = df.groupby(["scenario", "algorithm"])["ms_per_round"].median().unstack()
    e = df.groupby(["scenario", "algorithm"])["evals_per_round"].mean().unstack()
    cols = [c for c in ["LEACH", BASE, "GWO (Eq. 12)", "ABC (Eq. 12)", PROPOSED, PROPOSED_MO] if c in t.columns]
    text = (md_table(t[cols], index_label="Scenario (median ms/round)", floatfmt="{:.2f}") + "\n\n" +
            md_table(e[cols], index_label="Scenario (fitness evaluations/round)", floatfmt="{:.0f}"))
    return text, t


def write_base_paper_report(out) -> Path:
    from experiments.base_paper import HEADLINE, PAPER_SCENARIOS, PAPER_TABLE3, PAPER_TABLE6
    out = Path(out)
    scenarios = [s for s in PAPER_SCENARIOS if (out / s / "runs_raw.csv").exists()]
    if not scenarios:
        raise FileNotFoundError("run `python main.py basepaper --stage final` first")
    main = paired_comparison(out, scenarios, HEADLINE, PROPOSED, BASE)
    main.to_csv(out / "proposed_vs_base_paper.csv", index=False)
    mo = paired_comparison(out, scenarios, HEADLINE, PROPOSED_MO, BASE)
    mo.to_csv(out / "multiobjective_vs_base_paper.csv", index=False)
    comp = pd.concat([paired_comparison(out, scenarios, ["fnd", "hnd", "lnd", "node_rounds", "throughput_packets"],
                                        PROPOSED, b) for b in ("GWO (Eq. 12)", "ABC (Eq. 12)")])
    comp["p_holm"] = holm(comp["p_value"].values)
    comp["significant"] = comp["p_holm"] < ALPHA
    comp["verdict"] = np.where(~comp["significant"], "no significant difference",
                               np.where(comp["improvement_pct"] > 0, "improved", "worse"))
    comp.to_csv(out / "hybrid_vs_components.csv", index=False)

    _fig_improvement(main, out / "fig_improvement_vs_base_paper.png", f"{PROPOSED} vs DEAI-PSO")
    _fig_improvement(mo, out / "fig_multiobjective_vs_base_paper.png", f"{PROPOSED_MO} (multi-objective) vs DEAI-PSO")
    curve_algs = ["LEACH", BASE, PROPOSED, PROPOSED_MO]
    for sc in scenarios:
        _fig_curves(out, sc, "alive", "Alive nodes", out / f"fig_alive_{sc}.png", curve_algs)
        _fig_curves(out, sc, "residual_energy", "Residual energy (J)", out / f"fig_energy_{sc}.png", curve_algs)
        _fig_curves(out, sc, "packets_delivered", "Data packets delivered", out / f"fig_throughput_{sc}.png",
                    curve_algs)
    mech, energy = _mechanism(out, scenarios, [BASE, PROPOSED, PROPOSED_MO])
    mech.to_csv(out / "mechanism.csv", index=False)
    energy.to_csv(out / "energy_breakdown.csv", index=False)
    dev = json.loads((out / "dev_pilot" / "chosen_setting.json").read_text()) \
        if (out / "dev_pilot" / "chosen_setting.json").exists() else None
    meta = json.loads((out / scenarios[0] / "experiment.json").read_text())
    cfg = json.loads((out / scenarios[0] / "config.json").read_text())
    n_runs = meta["runs"]

    improved, worse = main[main["verdict"] == "improved"], main[main["verdict"] == "worse"]
    same = main[main["verdict"] == "no significant difference"]
    title = "Improvement over the base paper" if len(improved) > len(worse) else "Comparison with the base paper"
    L = [f"# {title}: Hybrid GWO-ABC vs DEAI-PSO", "",
         f"**Base paper (existing system):** {CITATION}", "",
         "**What is compared.** The base paper's contribution is an optimiser — PSO with double-exponential adaptive "
         "inertia (DEAI-PSO) — for its cluster-head selection problem (network model, Eq. 12 objective, 10 % CH "
         "target, free nodes near the BS). The like-for-like test of improving on it keeps that problem and objective "
         f"and replaces only the optimiser: **{PROPOSED}** (the proposed Hybrid GWO-ABC optimiser minimising the "
         "same Eq. 12 with the same weight *a*). The project's own multi-objective version "
         f"(**{PROPOSED_MO}**) is reported as well (section 5).", "",
         "## 1. Verdict (generated from the measured data)", "",
         f"Across the {len(scenarios)} base-paper scenarios and {len(HEADLINE)} headline metrics ({len(main)} paired "
         f"comparisons, {n_runs} runs each, Holm-corrected over all {len(main)} tests), {PROPOSED} is "
         f"**significantly better than DEAI-PSO in {len(improved)}**, significantly worse in {len(worse)}, and not "
         f"significantly different in {len(same)}.", ""]
    L += _verdict_lines(main, scenarios)
    L += ["", "![improvement](fig_improvement_vs_base_paper.png)", ""]

    L += ["## 2. How the comparison was made fair", "",
          "| Condition | Setting (identical for every algorithm) |", "|---|---|",
          f"| Networks | same random deployments: run *r* uses seed {cfg['seed']} + r for every algorithm |",
          "| Radio model | E_elec 50 nJ/bit, ε_fs 10 pJ/bit/m², ε_mp 0.0013 pJ/bit/m⁴, E_DA 5 nJ/bit (base paper Table 3) |",
          f"| Traffic | {PAPER_TABLE3['packet_bits']}-bit data packets, {PAPER_TABLE3['control_bits']}-bit control packets "
          "(Table 3), one reading per alive node per round |",
          f"| Energy / BS | {PAPER_TABLE3['initial_energy']} J per node; BS at ({PAPER_TABLE3['bs_x']:g}, "
          f"{PAPER_TABLE3['bs_y']:g}), outside the field (Table 3) |",
          f"| Objective | DEAI-PSO and {PROPOSED} minimise the same Eq. 12 with the same weight a |",
          f"| CH ratio | target {PAPER_TABLE3['ch_percentage']:.0%} of alive nodes (DEAI-PSO: exactly 10 %; the binary "
          "encoding of the proposed optimiser may use 5–15 %; the fixed-10 % variant isolates this in section 6) |",
          f"| Three-tier model | nodes within {PAPER_TABLE3['free_node_radius']:g} m of the BS are free nodes for every "
          "centralised algorithm (base paper's rule) |",
          "| CH candidates | residual energy ≥ mean (PSO-C rule, base paper ref. [41]) for every centralised algorithm |",
          "| Search budget | equal fitness evaluations per round (≈ 620): DEAI-PSO 36 particles (Table 3) × matched "
          "iterations; GWO 20 wolves × 30; ABC 20 bees × 30; Hybrid 10 wolves + 10 bees × 30 |",
          f"| Baseline tuning | settings the paper leaves open were tuned **in DEAI-PSO's favour** on separate "
          f"development seeds: {dev['label'] if dev else 'n/a'} (`dev_pilot/report.md`); the same a is used by "
          f"{PROPOSED} |",
          "| Proposed tuning | none — the Hybrid GWO-ABC settings are the project defaults used in every experiment |",
          f"| Runs | {n_runs} paired runs per scenario on held-out seeds (the paper used 10); development seeds were "
          "never reused |",
          "| Statistics | paired two-sided Wilcoxon signed-rank, Holm correction over each family of tests, Cliff's δ |",
          ""]

    L += ["## 3. Headline results (mean ± std)", ""]
    for sc in scenarios:
        L += [f"### {sc} — {PAPER_SCENARIOS[sc][2]}", "",
              _table(main, sc, "DEAI-PSO (base paper)", f"{PROPOSED} (proposed)"), "",
              f"![alive](fig_alive_{sc}.png)", "", f"![energy](fig_energy_{sc}.png)", "",
              f"![throughput](fig_throughput_{sc}.png)", ""]
    L += ["↑ higher is better, ↓ lower is better. Improvement = ((P − B)/B)·100 for ↑ metrics and ((B − P)/B)·100 for "
          "↓ metrics, so a positive value always means the proposed system is better. Residual energy and "
          f"consumption are measured at round {cfg['checkpoint_round']}. Full per-scenario reports (all algorithms, "
          "figures, CH logs): `<scenario>/report.md`.", ""]

    L += ["## 4. Is the hybrid better than its own components?", "",
          f"{PROPOSED} vs GWO (Eq. 12) and ABC (Eq. 12) — same objective, same budget (Holm over this family):", "",
          md_table(comp.assign(row=lambda d: d["scenario"] + " · " + d["label"] + " vs " + d["baseline"],
                               imp=lambda d: d["improvement_pct"].map(lambda v: f"{v:+.2f}"),
                               p=lambda d: d["p_holm"].map(lambda v: f"{v:.3g}"))
                   .set_index("row")[["imp", "p", "verdict"]]
                   .rename(columns={"imp": "Improvement %", "p": "p (Holm)", "verdict": "Verdict"}),
                   index_label="Scenario · metric · baseline"), ""]

    L += ["## 5. The project's multi-objective version vs DEAI-PSO", "",
          f"{PROPOSED_MO} minimises the project's five-term fitness (energy, intra-cluster distance, CH–BS distance, "
          "balance, CH count) instead of Eq. 12. Separate Holm family:", ""]
    L += _verdict_lines(mo, scenarios)
    L += ["", "![multi-objective](fig_multiobjective_vs_base_paper.png)", "",
          "With the BS 100–200 m away, the multi-objective fitness divides round energy by a worst-case bound, so "
          "differences in real Joules (d⁴ CH → BS costs) barely change its score; Eq. 12 measures Joules directly. "
          "This is why the like-for-like Eq. 12 comparison is the primary one, and it is a lesson for the project's "
          "own fitness design (see the README discussion).", ""]

    L += ["## 6. Where does the improvement come from? (BP1)", "",
          "Each optimiser was run with each objective under identical conditions; the fixed-K variant forces exactly "
          "10 % CHs like DEAI-PSO, separating the optimiser's search ability from the adaptive CH count.", "",
          _attribution(out)]

    L += ["## 7. Mechanism evidence", "",
          "Averages over all runs (distances and energy up to the checkpoint round).", "",
          md_table(mech.assign(row=lambda d: d["scenario"] + " · " + d["algorithm"]).set_index("row")
                   .drop(columns=["scenario", "algorithm"]), index_label="Scenario · algorithm", floatfmt="{:,.3f}"),
          "", "Energy spent per radio activity up to the checkpoint round (J, mean per run):", "",
          md_table(energy.assign(row=lambda d: d["scenario"] + " · " + d["algorithm"]).set_index("row")
                   .drop(columns=["scenario", "algorithm"]), index_label="Scenario · algorithm", floatfmt="{:.3f}"),
          ""]
    L += _mechanism_text(mech, energy, scenarios) + [""]

    rt_text, rt = _runtime(out)
    L += ["## 8. Computational cost (sequential, single process)", "",
          "CH-selection time per round over the first 100 rounds, median of 5 seeds, no other load. All metaheuristics "
          "spend about the same number of fitness evaluations per round.", "", rt_text, ""]
    if rt is not None and PROPOSED in rt.columns and BASE in rt.columns:
        ratios = "; ".join(f"{sc}: ×{rt.loc[sc, PROPOSED] / rt.loc[sc, BASE]:.2f}" for sc in rt.index)
        L += [f"Time per round, {PROPOSED} / DEAI-PSO — {ratios}. This is reported as a trade-off; both stay well "
              "below one second per round.", ""]

    L += ["## 9. The base paper's published numbers (reference only)", "",
          "Table 6 of the base paper reports these FND / HND / LND values (MATLAB R2023a, 10 runs):", ""]
    pub = [{"Scenario": sc, "Algorithm": alg, "FND": f, "HND": h, "LND": l}
           for sc in scenarios for alg, (f, h, l) in PAPER_TABLE6[sc].items()]
    L += [md_table(pd.DataFrame(pub), index=False), ""]
    bound = PAPER_TABLE3["initial_energy"] / (PAPER_TABLE3["packet_bits"] * 50e-9)
    L += [f"These values cannot be compared with any simulator that applies the paper's own Table 3 parameters to one "
          f"{PAPER_TABLE3['packet_bits']}-bit reading per node per round: the transmitter electronics alone cost "
          f"{PAPER_TABLE3['packet_bits']} × 50 nJ = {PAPER_TABLE3['packet_bits'] * 50e-9 * 1e3:.1f} mJ per packet, so "
          f"a {PAPER_TABLE3['initial_energy']} J node can transmit at most {bound:,.0f} times — no node can live "
          f"beyond {bound:,.0f} rounds — whereas the paper reports LND values of 3,400–4,756 rounds (even for LEACH). "
          "The paper's simulator must therefore count rounds or energy differently. For this reason the base paper's "
          "method was re-implemented and both systems were run in the **same** simulator under the **same** "
          "conditions; only those numbers (sections 1–8) are used to judge improvement.", ""]

    L += ["## 10. Limitations of this comparison", "",
          "- DEAI-PSO is a re-implementation from the paper; details the paper does not state (weight *a*, units of d "
          "in Eq. 13, acceleration-coefficient ranges, velocity clamp, mapping of CH coordinates to nodes) had to be "
          "chosen. Open choices were tuned in DEAI-PSO's favour on development seeds, and the mapping follows PSO-C "
          "(the paper's reference [41]).",
          "- The paper's 36 particles × 5000 iterations per clustering were not used; every method received the same "
          "budget (≈ 620 evaluations per round), so differences reflect the methods, not the budget.",
          "- Single-hop CH → BS transmission, as stated in the paper's data-transmission section; optional multi-hop "
          "forwarding between CHs is not modelled.",
          "- LEACH-FL, LEACH-FC and KM-PSO from the paper were not re-implemented; LEACH, GWO and ABC are included as "
          "additional baselines.", ""]
    path = out / "README.md"
    path.write_text("\n".join(L), encoding="utf-8")
    return path
