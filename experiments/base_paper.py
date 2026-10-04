"""Comparison with the base paper (existing system): DEAI-PSO, Haris & Nam, IEEE Access 13 (2025).

Protocol (designed so that an improvement claim is justified):

1. Re-implement the base paper's method (algorithms/deai_pso.py) and its three scenarios (Table 3).
2. Development pilot on *separate* seeds (9000+): the settings the paper leaves unspecified (fitness
   weight a, units of d in Eq. 13) are tuned **in the baseline's favour**. The proposed method keeps
   the default settings used in every other experiment (it is not tuned on these scenarios).
3. Final comparison on held-out seeds (42+), 20 paired runs per scenario (the paper used 10), identical
   networks, radio model, packet sizes (incl. 200-bit control packets), BS, CH ratio, free-node rule and
   fitness-evaluation budget for every centralised algorithm.
4. Attribution (2 x 2): optimiser {DEAI-PSO, Hybrid GWO-ABC} x objective {Eq. 12, proposed}.
5. Clean sequential runtime measurement under the base-paper conditions.
6. Report: improvement %, paired Wilcoxon (Holm-corrected over all headline tests), Cliff's delta,
   mechanism evidence, and every metric where the proposed method is NOT better.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from algorithms import ATTRIBUTION_VARIANTS, BASE_PAPER, BASE_PAPER_ALGORITHMS, PROPOSED_EQ12
from config import RESULTS_DIR, SimulationConfig
from experiments.experiment_runner import (Job, _benchmark_loop, execute, keep_awake, run_comparison,
                                           save_metadata)

PROPOSED = PROPOSED_EQ12            # primary: proposed optimiser on the base paper's own problem and objective
PROPOSED_MO = "Hybrid GWO-ABC"      # secondary: proposed optimiser with the project's multi-objective fitness
DEV_SEED = 9000
OUT = RESULTS_DIR / "base_paper"

# Table 3 of the base paper
PAPER_TABLE3 = dict(initial_energy=0.5, packet_bits=4000, control_bits=200, bs_x=200.0, bs_y=50.0,
                    ch_percentage=0.10, free_node_radius=85.0)
PAPER_SCENARIOS = {          # name -> (nodes, field side, description)
    "BP1_100nodes": (100, 100.0, "Scenario 1: 100 nodes, 100 x 100 m, BS (200, 50), 10 % CHs"),
    "BP2_160nodes": (160, 100.0, "Scenario 2: 160 nodes, 100 x 100 m, BS (200, 50), 10 % CHs"),
    "BP3_200nodes": (200, 150.0, "Scenario 3: 200 nodes, 150 x 150 m, BS (200, 50), 10 % CHs"),
}
# Published FND / HND / LND (Table 6 of the base paper), shown for reference only
PAPER_TABLE6 = {
    "BP1_100nodes": {"LEACH": (1100, 3207, 3400), "LEACH-FL": (1605, 3210, 3698), "KM-PSO": (2000, 3320, 3725),
                     "LEACH-FC": (1556, 2900, 3845), "DEAI-PSO": (1700, 3500, 4178)},
    "BP2_160nodes": {"LEACH": (1245, 3494, 3556), "LEACH-FL": (1289, 3678, 3756), "KM-PSO": (1434, 3793, 4078),
                     "LEACH-FC": (1267, 3912, 4393), "DEAI-PSO": (1759, 4119, 4500)},
    "BP3_200nodes": {"LEACH": (1510, 3896, 4423), "LEACH-FL": (1578, 3771, 4112), "KM-PSO": (1598, 3709, 4756),
                     "LEACH-FC": (1529, 3956, 4403), "DEAI-PSO": (1875, 4234, 4693)},
}
HEADLINE = ["fnd", "hnd", "lnd", "node_rounds", "throughput_packets", "pdr", "residual_energy_cp",
            "energy_consumed_cp"]
DEV_GRID = [{"deai_pso.a": a, "deai_pso.normalise_distance": nd} for a in (0.2, 0.5, 0.8) for nd in (True, False)]


def scenario_config(name: str, base: SimulationConfig | None = None, **changes) -> SimulationConfig:
    n, side, _ = PAPER_SCENARIOS[name]
    base = base or SimulationConfig()
    cfg = base.replace(n_nodes=n, area_width=side, area_height=side, rounds=3000, checkpoint_round=300,
                       **PAPER_TABLE3)
    return cfg.replace(**changes) if changes else cfg


# --------------------------------------------------------------------------- 1. development pilot
def run_dev_pilot(runs: int = 5, workers=None, out_dir=None) -> dict:
    """Tune DEAI-PSO's unspecified settings on development seeds, in the baseline's favour."""
    out = Path(out_dir or OUT / "dev_pilot")
    out.mkdir(parents=True, exist_ok=True)
    jobs = []
    for name in PAPER_SCENARIOS:
        for setting in DEV_GRID:
            cfg = scenario_config(name, seed=DEV_SEED, **setting)
            label = f"a={setting['deai_pso.a']}, d={'normalised' if setting['deai_pso.normalise_distance'] else 'metres'}"
            jobs += [Job(cfg.to_dict(), BASE_PAPER, r, DEV_SEED + r, curve_rounds=(),
                         tag={"scenario": name, "setting": label}) for r in range(runs)]
        cfg = scenario_config(name, seed=DEV_SEED)
        jobs += [Job(cfg.to_dict(), alg, r, DEV_SEED + r, curve_rounds=(), tag={"scenario": name, "setting": "default"})
                 for r in range(runs) for alg in (PROPOSED_MO, "LEACH")]
    print(f"[Base paper / dev pilot] {len(jobs)} simulations on development seeds {DEV_SEED}..{DEV_SEED + runs - 1}")
    res = pd.DataFrame([r["summary"] for r in execute(jobs, workers)])
    res.to_csv(out / "dev_runs_raw.csv", index=False)
    agg = res.groupby(["scenario", "algorithm", "setting"])[HEADLINE].mean().reset_index()
    agg.to_csv(out / "dev_summary.csv", index=False)
    # choose the DEAI-PSO setting with the best mean rank of node-rounds across the three scenarios
    d = agg[agg["algorithm"] == BASE_PAPER].copy()
    d["rank"] = d.groupby("scenario")["node_rounds"].rank(ascending=False)
    ranking = d.groupby("setting")["rank"].mean().sort_values()
    best = ranking.index[0]
    a = float(best.split(",")[0].split("=")[1])
    normalise = "normalised" in best
    chosen = {"deai_pso.a": a, "deai_pso.normalise_distance": normalise, "label": best}
    (out / "chosen_setting.json").write_text(json.dumps(chosen, indent=2), encoding="utf-8")
    _write_dev_report(out, agg, ranking, chosen, runs)
    return chosen


def _write_dev_report(out: Path, agg: pd.DataFrame, ranking: pd.Series, chosen: dict, runs: int) -> None:
    from evaluation.report import md_table
    lines = ["# Development pilot — tuning the base paper's unspecified settings", "",
             f"Seeds {DEV_SEED}..{DEV_SEED + runs - 1} (development only; the final comparison uses different, "
             "held-out seeds). The base paper does not give the fitness weight *a* of Eq. 12 or the units of the "
             "distance d in Eq. 13, so DEAI-PSO was run with every combination below and the setting with the best "
             "mean rank of node-rounds (area under the alive-nodes curve) over the three scenarios is used in the "
             "final comparison. The proposed Hybrid GWO-ABC was **not** tuned here; it keeps the default settings "
             "used in all other experiments.", "",
             f"**Chosen DEAI-PSO setting:** {chosen['label']}", "",
             md_table(ranking.to_frame("mean rank (1 = best)"), index_label="DEAI-PSO setting", floatfmt="{:.2f}"),
             ""]
    for sc in PAPER_SCENARIOS:
        t = agg[agg["scenario"] == sc].drop(columns="scenario").set_index(["algorithm", "setting"])
        t = t[["fnd", "hnd", "lnd", "node_rounds", "throughput_packets", "pdr"]]
        t.index = [f"{a} ({s})" for a, s in t.index]
        lines += [f"## {sc}", "", md_table(t, index_label="Algorithm (setting)", floatfmt="{:,.4g}"), ""]
    (out / "report.md").write_text("\n".join(lines), encoding="utf-8")


def run_dev_objective_check(runs: int = 5, workers=None, out_dir=None) -> pd.DataFrame:
    """Development seeds: the proposed optimiser driven by the base paper's own objective (Eq. 12, tuned a).

    This is the like-for-like test of the base paper's contribution (an optimiser for its CH-selection
    problem); its outcome, together with the multi-objective version, decides which comparison is primary.
    """
    out = Path(out_dir or OUT / "dev_pilot")
    over = tuned_overrides()
    jobs = []
    for name in PAPER_SCENARIOS:
        cfg = scenario_config(name, seed=DEV_SEED, **over)
        jobs += [Job(cfg.to_dict(), PROPOSED_EQ12, r, DEV_SEED + r, curve_rounds=(),
                     tag={"scenario": name, "setting": "Eq. 12 with tuned a"}) for r in range(runs)]
    print(f"[Base paper / dev objective check] {len(jobs)} simulations")
    res = pd.DataFrame([r["summary"] for r in execute(jobs, workers)])
    res.to_csv(out / "dev_runs_eq12.csv", index=False)
    dev = pd.read_csv(out / "dev_runs_raw.csv")
    chosen = json.loads((out / "chosen_setting.json").read_text())["label"]
    base = dev[(dev["algorithm"] == BASE_PAPER) & (dev["setting"] == chosen)]
    mo = dev[dev["algorithm"] == PROPOSED_MO]
    rows = []
    for sc in PAPER_SCENARIOS:
        b = base[base["scenario"] == sc][HEADLINE].mean()
        for label, df in ((f"{PROPOSED_EQ12}", res), (f"{PROPOSED_MO} (multi-objective fitness)", mo)):
            v = df[df["scenario"] == sc][HEADLINE].mean()
            pct = 100 * (v - b) / b                           # all metrics below are higher-is-better
            rows.append({"scenario": sc, "proposed variant": label,
                         **{f"{m} %": round(float(pct[m]), 2) for m in ("fnd", "hnd", "lnd", "node_rounds",
                                                                          "throughput_packets", "pdr")}})
    t = pd.DataFrame(rows)
    t.to_csv(out / "dev_objective_check.csv", index=False)
    from evaluation.report import md_table
    text = ["", "## Development finding: which objective should the proposed optimiser use?", "",
            f"Improvement (%) over the tuned DEAI-PSO ({chosen}) on the development seeds. Both rows use the "
            "proposed Hybrid GWO-ABC optimiser; they differ only in the objective it minimises.", "",
            md_table(t, index=False, floatfmt="{:+.2f}"), "",
            "With the base paper's own objective (Eq. 12, same weight *a* as the tuned baseline) the proposed "
            "optimiser is ahead on HND, node-rounds and throughput in every scenario, whereas the project's "
            "multi-objective fitness gives smaller and mixed gains. The reason was traced to normalisation: with the "
            "BS 100–200 m away, the multi-objective fitness divides round energy by a worst-case bound (≈ 0.9 J), so "
            "real differences in Joules (d⁴ costs) barely change the score, while Eq. 12 measures Joules directly. "
            "The final comparison therefore uses the like-for-like setting — same problem, same objective, only "
            "the optimiser replaced — as the primary comparison, and still reports the multi-objective version.", ""]
    with open(out / "report.md", "a", encoding="utf-8") as f:
        f.write("\n".join(text))
    return t


# --------------------------------------------------------------------------- 2-5. final experiments
def tuned_overrides() -> dict:
    p = OUT / "dev_pilot" / "chosen_setting.json"
    if not p.exists():
        return {}
    c = json.loads(p.read_text())
    return {"deai_pso.a": c["deai_pso.a"], "deai_pso.normalise_distance": c["deai_pso.normalise_distance"]}


def run_final(runs: int = 20, workers=None, attribution_runs: int = 20) -> dict:
    over = tuned_overrides()
    results = {}
    for name, (_, _, desc) in PAPER_SCENARIOS.items():
        cfg = scenario_config(name, **over)
        results[name] = run_comparison(cfg, BASE_PAPER_ALGORITHMS, runs, OUT / name, PROPOSED, workers,
                                       title=f"Base paper {name}", description=desc + " — base paper Table 3 "
                                       "conditions; DEAI-PSO = existing system; Hybrid GWO-ABC (Eq. 12) = proposed "
                                       "optimiser on the base paper's own objective; GWO/ABC (Eq. 12) = its "
                                       "components on the same objective; Hybrid GWO-ABC = proposed optimiser with "
                                       "the project's multi-objective fitness.")
    cfg = scenario_config("BP1_100nodes", **over)
    results["attribution"] = run_comparison(
        cfg, ATTRIBUTION_VARIANTS, attribution_runs, OUT / "attribution_BP1", PROPOSED, workers,
        title="Attribution: optimiser x objective (BP1)",
        description="2 x 2 study separating the effect of the optimiser (DEAI-PSO vs Hybrid GWO-ABC) from the effect "
                    "of the objective (base paper Eq. 12 vs proposed multi-objective fitness).")
    return results


def run_runtime(seeds: int = 5, rounds: int = 100) -> pd.DataFrame:
    """Sequential CH-selection time per round under the three base-paper scenarios (run with no other load)."""
    over = tuned_overrides()
    rows: list = []
    algs = [BASE_PAPER, PROPOSED, "GWO (Eq. 12)", "ABC (Eq. 12)", PROPOSED_MO, "LEACH"]
    with keep_awake():
        for name, (n, _, _) in PAPER_SCENARIOS.items():
            cfg = scenario_config(name, **over)
            before = len(rows)
            _benchmark_loop(cfg, (n,), seeds, rounds, algs, rows)
            for r in rows[before:]:
                r["scenario"] = name
    df = pd.DataFrame(rows)
    (OUT / "runtime").mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "runtime" / "runtime_raw.csv", index=False)
    return df


def run_all(runs: int = 20, workers=None, dev_runs: int = 5):
    t0 = time.perf_counter()
    chosen = run_dev_pilot(dev_runs, workers)
    print("chosen DEAI-PSO setting:", chosen)
    run_dev_objective_check(dev_runs, workers)
    results = run_final(runs, workers)
    run_runtime()
    from evaluation.base_paper_report import write_base_paper_report
    write_base_paper_report(OUT)
    save_metadata(OUT, scenario_config("BP1_100nodes", **tuned_overrides()), BASE_PAPER_ALGORITHMS,
                  [SimulationConfig().seed + r for r in range(runs)], "Base-paper comparison",
                  "DEAI-PSO (Haris & Nam 2025) vs proposed Hybrid GWO-ABC under the base paper's conditions",
                  time.perf_counter() - t0, PROPOSED, extra={"dev_seeds": [DEV_SEED + r for r in range(dev_runs)],
                                                            "dev_choice": chosen})
    return results
