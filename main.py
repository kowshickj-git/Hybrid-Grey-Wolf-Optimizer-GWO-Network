"""Hybrid GWO-ABC cluster-head selection for WSNs — command-line entry point.

    python main.py                          # GUI dashboard
    python main.py simulate -a "Hybrid GWO-ABC" --set n_nodes=200
    python main.py compare --runs 10        # Random vs LEACH vs GWO vs ABC vs Hybrid on paired networks
    python main.py scenarios [--only S1_100nodes] | ablation | sensitivity | convergence
    python main.py basepaper                # vs the base paper's DEAI-PSO (dev pilot, final, runtime, report)
    python main.py benchmark                # clean sequential runtime comparison
    python main.py all [--quick]            # every experiment (quick = smoke-test sizes, in results_quick/)
    python main.py postprocess              # refresh report text from saved CSVs
    python main.py reproduce results/scenarios/S1_100nodes
    python main.py diagrams                 # explanatory figures for the documentation (docs/figures)

Config: ``--config file.json`` loads a saved configuration; ``--set key=value``
overrides fields (dotted names for nested ones, e.g. ``--set gwo.population=30``).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

from config import RESULTS_DIR, SimulationConfig  # noqa: E402


def parse_value(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def build_config(args) -> SimulationConfig:
    cfg = SimulationConfig.load(args.config) if getattr(args, "config", None) else SimulationConfig()
    changes = {}
    for item in getattr(args, "set", None) or []:
        key, _, value = item.partition("=")
        changes[key.strip()] = parse_value(value.strip())
    if changes:
        cfg = cfg.replace(**changes)
    cfg.validate()
    return cfg


def cmd_simulate(args):
    from experiments.experiment_runner import run_comparison
    cfg = build_config(args)
    out = Path(args.out or RESULTS_DIR / f"single_{args.algorithm.replace(' ', '_')}")
    res = run_comparison(cfg, [args.algorithm], 1, out, proposed=None, workers=1,
                         title=f"Single simulation: {args.algorithm}")
    _print_summary(res)


def cmd_compare(args):
    from algorithms import COMPARISON_ALGORITHMS
    from experiments.experiment_runner import PROPOSED, run_comparison
    cfg = build_config(args)
    algs = args.algorithms or COMPARISON_ALGORITHMS
    res = run_comparison(cfg, algs, args.runs, args.out, PROPOSED, args.workers, title="Algorithm comparison")
    _print_summary(res)


def _print_summary(res):
    print()
    print(res.table.to_string())
    print(f"\nReport: {res.out_dir / 'report.md'}")


def cmd_scenarios(args):
    from experiments.experiment_runner import run_scenarios
    run_scenarios(build_config(args), args.runs, args.runs_other, args.workers, args.out, only=args.only)


def cmd_ablation(args):
    from experiments.experiment_runner import run_ablation
    res = run_ablation(build_config(args), args.runs, args.workers, args.out)
    _print_summary(res)


def cmd_sensitivity(args):
    from experiments.experiment_runner import run_sensitivity
    run_sensitivity(build_config(args), args.runs, args.workers, args.out, args.factors)


def cmd_convergence(args):
    from experiments.experiment_runner import run_convergence
    run_convergence(build_config(args), args.runs, args.iterations, args.out)


def cmd_basepaper(args):
    """Comparison with the base paper (DEAI-PSO, Haris & Nam, IEEE Access 2025)."""
    from experiments import base_paper as bp
    stage = args.stage
    if stage in ("dev", "all"):
        print("chosen DEAI-PSO setting:", bp.run_dev_pilot(args.dev_runs, args.workers))
    if stage in ("dev", "devcheck", "all"):
        print(bp.run_dev_objective_check(args.dev_runs, args.workers).to_string())
    if stage in ("final", "all"):
        bp.run_final(args.runs, args.workers)
    if stage in ("runtime", "all"):
        bp.run_runtime()
    if stage in ("report", "final", "runtime", "all"):
        from evaluation.base_paper_report import write_base_paper_report
        print("report:", write_base_paper_report(bp.OUT))


def cmd_benchmark(args):
    from experiments.experiment_runner import run_runtime_benchmark
    run_runtime_benchmark(build_config(args), tuple(args.sizes), args.seeds, args.rounds, args.out)


def cmd_postprocess(args):
    """Refresh report text from saved CSVs (trade-offs, runtime data-quality notes, scenario overview)."""
    from evaluation.report import flag_runtime_outliers, refresh_tradeoffs
    from experiments.experiment_runner import export_ch_logs, write_scenario_overview
    root = Path(args.root)
    for folder in sorted(p.parent for p in root.rglob("runs_raw.csv")):
        if not (folder / "improvement_vs_baselines.csv").exists():
            continue
        refresh_tradeoffs(folder)
        bad = flag_runtime_outliers(folder)
        msg = f"{folder}: trade-offs refreshed; runtime outliers: {bad or 'none'}"
        if args.ch_logs and not (folder / "reproducibility_check_run0.csv").exists():
            check = export_ch_logs(folder, args.workers)
            msg += f"; run-0 re-simulation identical: {bool(check['identical'].all())}"
        print(msg, flush=True)
    if (root / "scenarios").exists():
        write_scenario_overview(root / "scenarios")


def cmd_diagrams(args):
    from visualization.diagrams import make_all
    for path in make_all(args.out):
        print(path)


def cmd_all(args):
    from experiments.experiment_runner import run_all
    run_all(build_config(args), quick=args.quick, workers=args.workers, out_root=args.out)


def cmd_reproduce(args):
    from experiments.experiment_runner import reproduce
    res = reproduce(args.folder, args.workers, args.out)
    _print_summary(res)


def cmd_gui(args):
    from gui.dashboard import launch
    launch(build_config(args))


def main(argv=None):
    p = argparse.ArgumentParser(description="Hybrid GWO-ABC energy-efficient CH selection in WSNs")
    p.set_defaults(func=cmd_gui)
    sub = p.add_subparsers(dest="command")

    def common(sp, runs=None):
        sp.add_argument("--config", help="JSON configuration file")
        sp.add_argument("--set", action="append", metavar="KEY=VALUE", help="override a config field")
        sp.add_argument("--out", help="output folder")
        sp.add_argument("--workers", type=int, default=None, help="parallel processes (default: CPUs - 1)")
        if runs is not None:
            sp.add_argument("--runs", type=int, default=runs)

    sp = sub.add_parser("gui", help="interactive dashboard")
    common(sp)
    sp.set_defaults(func=cmd_gui)

    sp = sub.add_parser("simulate", help="one simulation with full figures")
    common(sp)
    sp.add_argument("-a", "--algorithm", default="Hybrid GWO-ABC")
    sp.set_defaults(func=cmd_simulate)

    sp = sub.add_parser("compare", help="multi-run comparison of algorithms")
    common(sp, runs=10)
    sp.add_argument("--algorithms", nargs="+")
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("scenarios", help="100/200/300 nodes and BS-position scenarios")
    common(sp, runs=20)
    sp.add_argument("--runs-other", type=int, default=10)
    sp.add_argument("--only", nargs="+", metavar="NAME",
                    choices=["S1_100nodes", "S2_200nodes", "S3_300nodes", "S4_100nodes_BS_edge",
                             "S5_100nodes_BS_outside"], help="run only these scenarios")
    sp.set_defaults(func=cmd_scenarios)

    sp = sub.add_parser("ablation", help="ablation study of the hybrid")
    common(sp, runs=10)
    sp.set_defaults(func=cmd_ablation)

    sp = sub.add_parser("sensitivity", help="one-factor-at-a-time sensitivity analysis")
    common(sp, runs=5)
    sp.add_argument("--factors", nargs="+")
    sp.set_defaults(func=cmd_sensitivity)

    sp = sub.add_parser("convergence", help="optimiser convergence on identical network states")
    common(sp, runs=20)
    sp.add_argument("--iterations", type=int, default=None)
    sp.set_defaults(func=cmd_convergence)

    sp = sub.add_parser("basepaper", help="compare with the base paper's DEAI-PSO (existing system)")
    sp.add_argument("--stage", choices=["dev", "devcheck", "final", "runtime", "report", "all"], default="all")
    sp.add_argument("--runs", type=int, default=20)
    sp.add_argument("--dev-runs", type=int, default=5)
    sp.add_argument("--workers", type=int, default=None)
    sp.set_defaults(func=cmd_basepaper)

    sp = sub.add_parser("benchmark", help="sequential single-process runtime benchmark")
    common(sp)
    sp.add_argument("--sizes", type=int, nargs="+", default=[100, 200, 300])
    sp.add_argument("--seeds", type=int, default=5)
    sp.add_argument("--rounds", type=int, default=100)
    sp.set_defaults(func=cmd_benchmark)

    sp = sub.add_parser("postprocess", help="refresh report text from saved CSVs")
    sp.add_argument("root", nargs="?", default=str(RESULTS_DIR))
    sp.add_argument("--ch-logs", action="store_true",
                    help="re-simulate run 0 of each folder to save its CH log and verify reproducibility")
    sp.add_argument("--workers", type=int, default=None)
    sp.set_defaults(func=cmd_postprocess)

    sp = sub.add_parser("all", help="run every experiment")
    common(sp)
    sp.add_argument("--quick", action="store_true",
                    help="tiny smoke-test sizes, written to results_quick/ (not for reporting)")
    sp.set_defaults(func=cmd_all)

    sp = sub.add_parser("diagrams", help="draw the explanatory figures of the documentation (docs/figures)")
    sp.add_argument("--out", help="output folder (default docs/figures)")
    sp.set_defaults(func=cmd_diagrams)

    sp = sub.add_parser("reproduce", help="re-run a saved experiment folder")
    sp.add_argument("folder")
    sp.add_argument("--out")
    sp.add_argument("--workers", type=int, default=None)
    sp.set_defaults(func=cmd_reproduce)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
