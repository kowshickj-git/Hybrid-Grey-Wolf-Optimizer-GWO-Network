"""Experiment runner: multi-run comparisons, scenarios, ablation, sensitivity, convergence.

Fairness / reproducibility rules applied everywhere:
* run r of every algorithm uses deployment seed ``config.seed + r`` (identical
  node coordinates, energy, BS, packet size, radio model and horizon) and the
  same algorithm RNG seed, so runs are paired;
* every experiment folder stores ``config.json`` + ``experiment.json`` (seeds,
  algorithms, runs) and can be re-run with ``python main.py reproduce <folder>``;
* raw per-run results are saved as CSV; nothing is post-edited.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json  # noqa: E402
import platform  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor, as_completed  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from datetime import datetime  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from algorithms import ABLATION_VARIANTS, COMPARISON_ALGORITHMS, MAIN_ALGORITHMS  # noqa: E402
from config import QUICK_RESULTS_DIR, RESULTS_DIR, SimulationConfig  # noqa: E402
from evaluation.comparison import full_comparison  # noqa: E402
from evaluation.metrics import STAT_METRICS  # noqa: E402
from evaluation.report import md_table, write_comparison_report  # noqa: E402
from models.network import Network  # noqa: E402
from simulation.simulator import Simulator  # noqa: E402

PROPOSED = "Hybrid GWO-ABC"
HISTORY_COLS = ["round", "alive", "dead", "residual_energy", "consumed_energy", "round_energy", "ch_count",
                "packets_generated", "packets_delivered", "bs_packets", "throughput_bits", "pdr", "round_pdr",
                "avg_intra_distance", "max_intra_distance", "avg_ch_bs_distance", "cluster_imbalance", "fitness",
                "selection_time",
                "evaluations", "e_control", "e_member_tx", "e_ch_rx", "e_aggregation", "e_ch_tx", "e_direct_tx"]


def default_workers() -> int:
    return max(1, (os.cpu_count() or 2) - 1)


class keep_awake:
    """Block idle system sleep while experiments run (Windows only; released on exit, no settings changed).

    Sleep would otherwise stall long runs and inflate wall-clock runtime measurements.
    """

    def __enter__(self):
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)  # CONTINUOUS | SYSTEM_REQUIRED
        return self

    def __exit__(self, *exc):
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        return False


# --------------------------------------------------------------------------- jobs
@dataclass
class Job:
    config: dict
    algorithm: str
    run: int
    seed: int
    curve_rounds: tuple = (1,)
    snapshots: bool = False
    tag: dict = field(default_factory=dict)       # extra columns (e.g. sensitivity factor/value)


def run_job(job: Job) -> dict:
    """Run one simulation in a worker process. Returns plain picklable data."""
    cfg = SimulationConfig.from_dict(job.config)
    net = Network.deploy(cfg, seed=job.seed)
    snaps: dict = {}
    snap_rounds = {1, cfg.checkpoint_round} if job.snapshots else set()
    sim = Simulator(cfg, job.algorithm, net, seed=job.seed, curve_rounds=job.curve_rounds,
                    snapshot_rounds=snap_rounds)
    half = int(np.ceil(net.n / 2))

    def on_round(s: Simulator, rec):
        if job.snapshots and "hnd" not in snaps and rec.dead >= half:
            snaps["hnd"] = s.snapshot()

    t0 = time.perf_counter()
    res = sim.run(callback=on_round)
    wall = time.perf_counter() - t0
    if job.snapshots:
        snaps.update({k: v for k, v in res.snapshots.items()})
        snaps["final"] = sim.snapshot()
    hist = res.history[HISTORY_COLS].copy()
    hist.insert(0, "run", job.run)
    hist.insert(0, "algorithm", job.algorithm)
    summary = {"algorithm": job.algorithm, "run": job.run, "seed": job.seed, **job.tag, **res.summary,
               "wall_time": wall}
    ch_log = None
    if job.snapshots:                       # full CH record (ids, positions, energy, BS distance) for run 0
        ch_log = res.ch_log.copy()
        ch_log.insert(0, "run", job.run)
        ch_log.insert(0, "algorithm", job.algorithm)
    return {"summary": summary, "history": hist, "curves": res.curves, "snapshots": snaps, "tag": job.tag,
            "ch_log": ch_log}


def execute(jobs: list[Job], workers: int | None = None, progress: bool = True) -> list[dict]:
    workers = default_workers() if workers is None else workers
    out: list[dict] = []
    t0 = time.perf_counter()
    if workers <= 1:
        with keep_awake():
            for i, j in enumerate(jobs, 1):
                out.append(run_job(j))
                if progress:
                    _progress(i, len(jobs), t0, j)
        return out
    with keep_awake(), ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_job, j): j for j in jobs}
        for i, f in enumerate(as_completed(futures), 1):
            out.append(f.result())
            if progress:
                _progress(i, len(jobs), t0, futures[f])
    return out


def _progress(i, n, t0, job):
    print(f"  [{i:>4}/{n}] {time.perf_counter() - t0:7.1f}s  {job.algorithm:<22} run {job.run} {job.tag or ''}",
          flush=True)


# --------------------------------------------------------------------------- comparison
@dataclass
class ExperimentResult:
    out_dir: Path
    config: SimulationConfig
    algorithms: list
    runs: pd.DataFrame
    histories: pd.DataFrame
    curves: dict            # algorithm -> list of round-1 curve dicts (one per run)
    snapshots: dict         # algorithm -> snapshots of run 0
    table: pd.DataFrame
    stats: pd.DataFrame
    comparison: pd.DataFrame
    ch_log: pd.DataFrame | None = None      # cluster heads of run 0, every round, every algorithm


def run_comparison(config: SimulationConfig, algorithms=None, runs: int = 10, out_dir=None,
                   proposed: str | None = PROPOSED, workers: int | None = None, title: str = "Comparison",
                   description: str = "", make_report: bool = True) -> ExperimentResult:
    """Run every algorithm ``runs`` times on identical paired networks and save everything."""
    config.validate()
    algorithms = list(algorithms or MAIN_ALGORITHMS)
    out_dir = Path(out_dir or RESULTS_DIR / f"comparison_{datetime.now():%Y%m%d_%H%M%S}")
    out_dir.mkdir(parents=True, exist_ok=True)
    seeds = [config.seed + r for r in range(runs)]
    # run-major, algorithm-interleaved order: every algorithm meets the same mix of parallel load
    jobs = [Job(config.to_dict(), alg, r, seeds[r], snapshots=(r == 0))
            for r in range(runs) for alg in algorithms]
    print(f"[{title}] {len(algorithms)} algorithms x {runs} runs -> {out_dir}")
    t0 = time.perf_counter()
    results = execute(jobs, workers)
    res = collect(results, config, algorithms, out_dir, proposed)
    save_metadata(out_dir, config, algorithms, seeds, title, description, time.perf_counter() - t0, proposed)
    if make_report:
        write_comparison_report(res, title=title, description=description, proposed=proposed)
    return res


def _cost_rank(alg: str) -> int:
    """Scheduling hint for sensitivity jobs (expensive first); not used where runtime is compared."""
    return 0 if "Hybrid" in alg else 1 if alg in ("ABC", "ABC only") else 3 if alg in ("LEACH", "Random") else 2


def collect(results: list[dict], config, algorithms, out_dir: Path, proposed) -> ExperimentResult:
    order = {a: i for i, a in enumerate(algorithms)}
    results = sorted(results, key=lambda r: (r["summary"]["run"], order.get(r["summary"]["algorithm"], 99)))
    runs = pd.DataFrame([r["summary"] for r in results])
    histories = pd.concat([r["history"] for r in results], ignore_index=True)
    curves: dict = {}
    snapshots: dict = {}
    for r in results:
        alg = r["summary"]["algorithm"]
        if 1 in r["curves"]:
            curves.setdefault(alg, []).append(r["curves"][1])
        if r["snapshots"]:
            snapshots[alg] = r["snapshots"]
    table, stats_df, cmp = full_comparison(runs, algorithms, proposed)
    logs = [r["ch_log"] for r in results if r.get("ch_log") is not None]
    ch_log = pd.concat(logs, ignore_index=True) if logs else None
    if ch_log is not None:
        ch_log.to_csv(out_dir / "ch_log_run0.csv", index=False)

    runs.to_csv(out_dir / "runs_raw.csv", index=False)
    histories.to_csv(out_dir / "history_raw.csv.gz", index=False, compression="gzip")
    stats_df.to_csv(out_dir / "statistics.csv", index=False)
    cmp.to_csv(out_dir / "improvement_vs_baselines.csv", index=False)
    table.to_csv(out_dir / "result_table.csv")
    if curves:   # raw round-1 optimisation curves behind the convergence figures
        (out_dir / "convergence_round1.json").write_text(json.dumps(curves), encoding="utf-8")
    (out_dir / "result_table.md").write_text(md_table(table, index_label="Metric"), encoding="utf-8")
    config.save(out_dir / "config.json")
    return ExperimentResult(out_dir, config, algorithms, runs, histories, curves, snapshots, table, stats_df, cmp,
                            ch_log)


REPRO_FIELDS = ["fnd", "hnd", "lnd", "node_rounds", "throughput_packets", "packets_generated",
                "residual_energy_cp", "final_fitness"]


def export_ch_logs(folder, workers: int | None = None) -> pd.DataFrame:
    """For an existing experiment folder: re-simulate run 0 of every algorithm from the saved config and seed,
    check that it reproduces the saved run-0 results exactly, and save the cluster-head log.

    Returns the reproducibility check (saved vs re-simulated value per algorithm and field).
    """
    from evaluation.report import append_ch_section
    folder = Path(folder)
    cfg = SimulationConfig.load(folder / "config.json")
    meta = json.loads((folder / "experiment.json").read_text())
    saved = pd.read_csv(folder / "runs_raw.csv")
    seed = meta["seeds"][0]
    results = execute([Job(cfg.to_dict(), alg, 0, seed, curve_rounds=(), snapshots=True)
                       for alg in meta["algorithms"]], workers, progress=False)
    ch_log = pd.concat([r["ch_log"] for r in results], ignore_index=True)
    ch_log.to_csv(folder / "ch_log_run0.csv", index=False)
    rows = []
    for r in results:
        s = r["summary"]
        old = saved[(saved["algorithm"] == s["algorithm"]) & (saved["run"] == 0)].iloc[0]
        for f in REPRO_FIELDS:
            rows.append({"algorithm": s["algorithm"], "field": f, "saved": old[f], "resimulated": s[f],
                         "identical": bool(np.isclose(old[f], s[f], rtol=1e-9, atol=1e-12))})
    check = pd.DataFrame(rows)
    check.to_csv(folder / "reproducibility_check_run0.csv", index=False)
    append_ch_section(folder, ch_log, check, meta["algorithms"])
    return check


def save_metadata(out_dir: Path, config, algorithms, seeds, title, description, elapsed, proposed=None,
                  extra: dict | None = None) -> None:
    meta = {"title": title, "description": description, "algorithms": list(algorithms), "runs": len(seeds),
            "seeds": seeds, "proposed": proposed, "created": datetime.now().isoformat(timespec="seconds"),
            "elapsed_s": round(elapsed, 1), "python": platform.python_version(), "numpy": np.__version__,
            "platform": platform.platform(), "seed_rule": "run r uses deployment and algorithm seed config.seed + r"}
    meta.update(extra or {})
    (out_dir / "experiment.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def reproduce(folder, workers: int | None = None, out_dir=None) -> ExperimentResult:
    """Re-run a saved comparison from its config.json + experiment.json."""
    folder = Path(folder)
    cfg = SimulationConfig.load(folder / "config.json")
    meta = json.loads((folder / "experiment.json").read_text())
    out = Path(out_dir or folder.parent / f"{folder.name}_reproduced")
    return run_comparison(cfg, meta["algorithms"], meta["runs"], out, meta.get("proposed"), workers,
                          title=meta["title"] + " (reproduced)", description=meta.get("description", ""))


# --------------------------------------------------------------------------- scenarios
def scenario_configs(base: SimulationConfig) -> dict[str, tuple[SimulationConfig, str]]:
    return {
        "S1_100nodes": (base.replace(n_nodes=100), "100 nodes, 100x100 m, BS at the centre (50, 50)"),
        "S2_200nodes": (base.replace(n_nodes=200), "200 nodes, 100x100 m, BS at the centre (50, 50)"),
        "S3_300nodes": (base.replace(n_nodes=300), "300 nodes, 100x100 m, BS at the centre (50, 50)"),
        "S4_100nodes_BS_edge": (base.replace(n_nodes=100, bs_x=50.0, bs_y=100.0),
                                "100 nodes, 100x100 m, BS on the field edge (50, 100)"),
        "S5_100nodes_BS_outside": (base.replace(n_nodes=100, bs_x=50.0, bs_y=175.0),
                                   "100 nodes, 100x100 m, BS outside the field (50, 175)"),
    }


def run_scenarios(base: SimulationConfig, runs_main: int = 20, runs_other: int = 10, workers=None,
                  out_root=None, only=None) -> dict[str, ExperimentResult]:
    out_root = Path(out_root or RESULTS_DIR / "scenarios")
    results = {}
    for name, (cfg, desc) in scenario_configs(base).items():
        if only and name not in only:
            continue
        main = name.startswith("S1")                  # S1 = main demonstration: also the Random baseline
        results[name] = run_comparison(cfg, COMPARISON_ALGORITHMS if main else MAIN_ALGORITHMS,
                                       runs_main if main else runs_other, out_root / name, PROPOSED, workers,
                                       title=f"Scenario {name}", description=desc)
    if results:
        write_scenario_overview(out_root)
    return results


def scenario_folders(out_root) -> list[Path]:
    """Saved scenario result folders under ``out_root`` (re-runs made with ``reproduce`` are skipped)."""
    return sorted(p for p in Path(out_root).iterdir()
                  if (p / "runs_raw.csv").exists() and not p.name.endswith("_reproduced"))


def write_scenario_overview(out_root) -> None:
    """Overview of every saved scenario folder (built from the CSVs, so running a subset keeps the others)."""
    from evaluation.report import rebuild_scenario_overview
    rows = []
    for folder in scenario_folders(out_root):
        df = pd.read_csv(folder / "runs_raw.csv").groupby("algorithm", sort=False)[STAT_METRICS].mean()
        df = df.reset_index()
        df.insert(0, "scenario", folder.name)
        rows.append(df)
    if rows:
        pd.concat(rows).to_csv(Path(out_root) / "scenario_overview.csv", index=False)
    rebuild_scenario_overview(out_root)


# --------------------------------------------------------------------------- ablation
def run_ablation(base: SimulationConfig, runs: int = 10, workers=None, out_dir=None) -> ExperimentResult:
    return run_comparison(base, ABLATION_VARIANTS, runs, out_dir or RESULTS_DIR / "ablation",
                          "Full Hybrid GWO-ABC", workers, title="Ablation study",
                          description="Contribution of each hybrid component (100 nodes, 100x100 m, BS centre). "
                                      "'w/o distance' removes both distance terms (w2 = w3 = 0); every variant's "
                                      "CH sets are re-scored with the full default weights for 'Final Fitness'.")


# --------------------------------------------------------------------------- sensitivity
OPTIMISERS = ["GWO", "ABC", "Hybrid GWO-ABC"]
WEIGHT_PRESETS = {
    "default (.30/.25/.20/.15/.10)": (0.30, 0.25, 0.20, 0.15, 0.10),
    "equal (.20 each)": (0.20, 0.20, 0.20, 0.20, 0.20),
    "energy-heavy (.50/.15/.15/.10/.10)": (0.50, 0.15, 0.15, 0.10, 0.10),
    "distance-heavy (.15/.35/.30/.10/.10)": (0.15, 0.35, 0.30, 0.10, 0.10),
    "balance-heavy (.20/.20/.15/.35/.10)": (0.20, 0.20, 0.15, 0.35, 0.10),
}


def _area(v):
    return {"area_width": float(v), "area_height": float(v), "bs_x": v / 2, "bs_y": v / 2}


def _weights(v):
    w = WEIGHT_PRESETS[v]
    return dict(zip(["weights.energy", "weights.intra_distance", "weights.ch_bs_distance", "weights.balance",
                     "weights.ch_count"], w))


SENSITIVITY = {  # factor -> (values, value -> config changes, algorithms, axis label)
    "n_nodes": ([50, 100, 150, 200], lambda v: {"n_nodes": v}, MAIN_ALGORITHMS, "Number of nodes"),
    "area": ([50, 100, 150, 200], _area, MAIN_ALGORITHMS, "Square field side (m), BS at centre"),
    "initial_energy": ([0.25, 0.5, 1.0], lambda v: {"initial_energy": v}, MAIN_ALGORITHMS, "Initial energy (J)"),
    "ch_percentage": ([0.03, 0.05, 0.08, 0.10], lambda v: {"ch_percentage": v}, MAIN_ALGORITHMS,
                      "Target CH percentage p"),
    "bs_position": (["(50,50)", "(50,100)", "(50,150)", "(0,0)"],
                    lambda v: dict(zip(["bs_x", "bs_y"], map(float, v.strip("()").split(",")))),
                    MAIN_ALGORITHMS, "BS position"),
    "gwo_population": ([10, 20, 30, 40], lambda v: {"gwo.population": v}, ["GWO", "Hybrid GWO-ABC"],
                       "GWO population"),
    "abc_colony": ([10, 20, 30, 40], lambda v: {"abc.colony_size": v}, ["ABC", "Hybrid GWO-ABC"],
                   "ABC colony size"),
    "iterations": ([10, 20, 30, 50], lambda v: {"opt_iterations": v}, OPTIMISERS, "Optimisation iterations"),
    "weights": (list(WEIGHT_PRESETS), _weights, ["Hybrid GWO-ABC"], "Fitness weights (w1..w5)"),
    "ch_energy_threshold": ([0.0, 0.5, 1.0], lambda v: {"ch_energy_threshold": v}, OPTIMISERS,
                            "CH eligibility threshold (x mean energy)"),
}
SENSITIVITY_METRICS = ["fnd", "hnd", "lnd", "residual_energy_cp", "throughput_packets", "pdr", "runtime",
                       "final_fitness"]


def run_sensitivity(base: SimulationConfig, runs: int = 5, workers=None, out_dir=None, factors=None):
    from evaluation.report import write_sensitivity_report
    from visualization.performance_plots import plot_sensitivity

    out_dir = Path(out_dir or RESULTS_DIR / "sensitivity")
    out_dir.mkdir(parents=True, exist_ok=True)
    factors = factors or list(SENSITIVITY)
    jobs, configs = [], {}
    for factor in factors:
        values, change, algs, _ = SENSITIVITY[factor]
        for v in values:
            cfg = base.replace(**change(v))
            cfg.validate()
            configs[f"{factor}={v}"] = cfg.to_dict()
            for r in range(runs):
                for alg in algs:
                    jobs.append(Job(cfg.to_dict(), alg, r, cfg.seed + r, curve_rounds=(),
                                    tag={"factor": factor, "value": str(v)}))
    jobs.sort(key=lambda j: _cost_rank(j.algorithm))
    print(f"[Sensitivity] {len(jobs)} simulations -> {out_dir}")
    t0 = time.perf_counter()
    results = execute(jobs, workers)
    runs_df = pd.DataFrame([r["summary"] for r in results]).sort_values(["factor", "value", "algorithm", "run"])
    runs_df.to_csv(out_dir / "sensitivity_runs_raw.csv", index=False)
    agg = runs_df.groupby(["factor", "value", "algorithm"], sort=False)[SENSITIVITY_METRICS].agg(["mean", "std"])
    agg.columns = [f"{m}_{s}" for m, s in agg.columns]
    agg = agg.reset_index()
    agg.to_csv(out_dir / "sensitivity_summary.csv", index=False)
    (out_dir / "configs.json").write_text(json.dumps(configs, indent=2), encoding="utf-8")

    figures = {}
    for factor in factors:
        values, _, algs, label = SENSITIVITY[factor]
        sub = agg[agg["factor"] == factor].copy()
        order = {str(v): i for i, v in enumerate(values)}
        sub["order"] = sub["value"].map(order)
        sub = sub.sort_values(["algorithm", "order"])
        if all(isinstance(v, (int, float)) for v in values):
            sub["value"] = sub["value"].astype(float)
        sub["algorithm"] = pd.Categorical(sub["algorithm"], [a for a in MAIN_ALGORITHMS if a in algs])
        sub = sub.sort_values(["algorithm", "order"])
        for metric in ("fnd", "hnd", "throughput_packets"):
            p = out_dir / f"sens_{factor}_{metric}.png"
            plot_sensitivity(sub, factor, metric, p, xlabel=label)
            figures.setdefault(factor, []).append(p.name)
    save_metadata(out_dir, base, sorted({j.algorithm for j in jobs}), [base.seed + r for r in range(runs)],
                  "Sensitivity analysis", "One-factor-at-a-time sensitivity around the default configuration",
                  time.perf_counter() - t0, extra={"factors": {f: [str(v) for v in SENSITIVITY[f][0]]
                                                              for f in factors}})
    base.save(out_dir / "config.json")
    write_sensitivity_report(out_dir, agg, factors, figures, runs)
    return agg


# --------------------------------------------------------------------------- convergence
def run_convergence(base: SimulationConfig, runs: int = 20, iterations: int | None = None, out_dir=None,
                    state_rounds=(0, None)) -> pd.DataFrame:
    """Best-so-far fitness per iteration of GWO, ABC and Hybrid on identical network states.

    ``state_rounds``: 0 = freshly deployed network; None = network after
    ``checkpoint_round`` rounds of LEACH (heterogeneous residual energy).
    """
    from algorithms.abc import ArtificialBeeColony
    from algorithms.fitness import FitnessContext
    from algorithms.gwo import GreyWolfOptimizer
    from algorithms.hybrid_gwo_abc import HybridGWOABC
    from evaluation.report import write_convergence_report
    from visualization.convergence_plot import plot_algorithm_convergence, plot_internal_convergence

    out_dir = Path(out_dir or RESULTS_DIR / "convergence")
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = base.replace(opt_iterations=iterations or base.opt_iterations)
    rows, figures = [], {}
    for state in state_rounds:
        state_round = cfg.checkpoint_round if state is None else state
        curves = {"GWO": [], "ABC": [], "Hybrid GWO-ABC": []}
        internal = {"gwo": [], "abc": [], "hybrid": []}
        for r in range(runs):
            seed = cfg.seed + r
            net = Network.deploy(cfg, seed=seed)
            if state_round:
                sim = Simulator(cfg.replace(rounds=state_round), "LEACH", net, seed=seed)
                sim.run()
                net = sim.network
            ctx_args = (net, cfg)
            opts = {"GWO": GreyWolfOptimizer(cfg.gwo.population, cfg.opt_iterations),
                    "ABC": ArtificialBeeColony(cfg.abc.colony_size, cfg.abc.limit, cfg.opt_iterations),
                    "Hybrid GWO-ABC": HybridGWOABC.from_config(cfg)}
            for name, opt in opts.items():
                ctx = FitnessContext(*ctx_args)
                t0 = time.perf_counter()
                res = opt.optimize(ctx, np.random.default_rng(seed))
                dt = time.perf_counter() - t0
                key = {"GWO": "gwo", "ABC": "abc"}.get(name, "hybrid")
                curves[name].append(res.curves[key])
                if name == "Hybrid GWO-ABC":
                    for k in internal:
                        internal[k].append(res.curves[k])
                rows.append({"state_round": state_round, "run": r, "seed": seed, "algorithm": name,
                             "initial_fitness": res.curves[key][0], "final_fitness": res.fitness,
                             "evaluations": ctx.evaluations, "time_s": dt, **res.info})
        tag = f"round{state_round}"
        arr = {k: np.array(v) for k, v in curves.items()}
        for k, v in arr.items():
            pd.DataFrame(v).to_csv(out_dir / f"curves_{tag}_{k.replace(' ', '_')}.csv", index_label="run")
        state_txt = "fresh network" if not state_round else f"after {state_round} LEACH rounds"
        figs = {
            "gwo": plot_algorithm_convergence({"GWO": arr["GWO"]}, out_dir / f"conv_gwo_{tag}.png",
                                              f"GWO convergence ({state_txt})", runs),
            "abc": plot_algorithm_convergence({"ABC": arr["ABC"]}, out_dir / f"conv_abc_{tag}.png",
                                              f"ABC convergence ({state_txt})", runs),
            "hybrid": plot_internal_convergence({k: np.array(v) for k, v in internal.items()},
                                                out_dir / f"conv_hybrid_{tag}.png",
                                                f"Hybrid GWO-ABC convergence ({state_txt})", runs),
            "all": plot_algorithm_convergence(arr, out_dir / f"conv_all_{tag}.png",
                                              f"Convergence comparison ({state_txt})", runs),
        }
        figures[state_round] = {k: Path(v).name for k, v in figs.items()}
    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "convergence_runs_raw.csv", index=False)
    cfg.save(out_dir / "config.json")
    save_metadata(out_dir, cfg, ["GWO", "ABC", "Hybrid GWO-ABC"], [cfg.seed + r for r in range(runs)],
                  "Convergence analysis", "Best-so-far fitness per iteration on identical network states", 0.0)
    write_convergence_report(out_dir, df, figures, cfg)
    return df


# --------------------------------------------------------------------------- runtime benchmark
def run_runtime_benchmark(base: SimulationConfig, sizes=(100, 200, 300), seeds: int = 5, rounds: int = 100,
                          out_dir=None, algorithms=None) -> pd.DataFrame:
    """Clean CH-selection runtime: one process, no parallel load, algorithm order rotated per seed.

    Each algorithm simulates the first ``rounds`` rounds of the same network
    (all nodes are still alive, so every algorithm does the same work per round).
    """
    from evaluation.report import write_runtime_report
    from visualization.performance_plots import plot_runtime_benchmark

    algorithms = list(algorithms or MAIN_ALGORITHMS)
    out_dir = Path(out_dir or RESULTS_DIR / "runtime_benchmark")
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    with keep_awake():
        _benchmark_loop(base, sizes, seeds, rounds, algorithms, rows)
    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "runtime_raw.csv", index=False)
    base.save(out_dir / "config.json")
    save_metadata(out_dir, base, algorithms, [base.seed + s for s in range(seeds)], "Runtime benchmark",
                  f"Sequential single-process CH-selection timing, first {rounds} rounds, sizes {list(sizes)}", 0.0,
                  extra={"cpu_count": os.cpu_count(), "processor": platform.processor()})
    plot_runtime_benchmark(df, algorithms, out_dir / "runtime_benchmark.png")
    write_runtime_report(out_dir, df, algorithms, rounds)
    return df


def _benchmark_loop(base, sizes, seeds, rounds, algorithms, rows):
    for n in sizes:
        cfg = base.replace(n_nodes=n, rounds=rounds)
        for s in range(seeds):
            seed = cfg.seed + s
            net = Network.deploy(cfg, seed=seed)
            order = algorithms[s % len(algorithms):] + algorithms[:s % len(algorithms)]
            for alg in order:
                res = Simulator(cfg, alg, net, seed=seed, curve_rounds=()).run()
                h = res.history
                rows.append({"n_nodes": n, "seed": seed, "algorithm": alg, "rounds": len(h),
                             "ms_per_round": 1000 * h["selection_time"].mean(),
                             "evals_per_round": h["evaluations"].mean()})
                print(f"  n={n} seed={seed} {alg:<16} {rows[-1]['ms_per_round']:8.2f} ms/round", flush=True)


# --------------------------------------------------------------------------- everything
def run_all(base: SimulationConfig | None = None, quick: bool = False, workers=None, out_root=None):
    base = base or SimulationConfig()
    out_root = Path(out_root or (QUICK_RESULTS_DIR if quick else RESULTS_DIR))
    if quick:   # smoke-test sizes; NOT for reporting (written to results_quick/ unless --out is given)
        base = base.replace(rounds=300, checkpoint_round=100, opt_iterations=10)
        run_scenarios(base, 2, 2, workers, out_root / "scenarios", only=["S1_100nodes", "S5_100nodes_BS_outside"])
        run_ablation(base, 2, workers, out_root / "ablation")
        run_sensitivity(base, 2, workers, out_root / "sensitivity", factors=["n_nodes", "weights"])
        run_convergence(base, 3, out_dir=out_root / "convergence")
        run_runtime_benchmark(base, (100,), 2, 20, out_root / "runtime_benchmark")
        return
    run_convergence(base, 20, out_dir=out_root / "convergence")
    run_runtime_benchmark(base, out_dir=out_root / "runtime_benchmark")   # before the parallel load starts
    run_scenarios(base, 20, 10, workers, out_root / "scenarios")
    run_ablation(base, 10, workers, out_root / "ablation")
    run_sensitivity(base, 5, workers, out_root / "sensitivity")
