"""Result generation: a tiny paired experiment must produce raw CSVs, statistics, figures,
a report and reproducibility metadata, and every table value must come from the raw runs."""
import json

import numpy as np
import pandas as pd

from config import SimulationConfig
from experiments.experiment_runner import run_comparison


def test_experiment_outputs(tmp_path):
    cfg = SimulationConfig(n_nodes=20, initial_energy=0.01, rounds=60, opt_iterations=3, checkpoint_round=10,
                           seed=5)
    algs = ["LEACH", "GWO", "ABC", "Hybrid GWO-ABC"]
    res = run_comparison(cfg, algs, runs=2, out_dir=tmp_path, workers=1, title="test")

    for name in ("config.json", "experiment.json", "runs_raw.csv", "history_raw.csv.gz", "statistics.csv",
                 "improvement_vs_baselines.csv", "result_table.csv", "result_table.md", "report.md",
                 "round_means.csv", "convergence_round1.json", "ch_log_run0.csv", "01_topology.png",
                 "09_alive_vs_rounds.png",
                 "17_runtime.png", "18_lifetime_fnd_hnd_lnd.png"):
        assert (tmp_path / name).exists(), name

    # reproducibility metadata
    meta = json.loads((tmp_path / "experiment.json").read_text())
    assert meta["algorithms"] == algs and meta["seeds"] == [5, 6]
    assert SimulationConfig.load(tmp_path / "config.json") == cfg

    # table values are the means of the raw per-run results
    runs = pd.read_csv(tmp_path / "runs_raw.csv")
    assert len(runs) == 2 * len(algs)
    for alg in algs:
        fnd = runs.loc[runs["algorithm"] == alg, "fnd"].mean()
        assert res.table.loc["FND (rounds)", alg].startswith(f"{fnd:,.0f}")

    # the run-level summary agrees with the per-round history
    hist = pd.read_csv(tmp_path / "history_raw.csv.gz")
    for (alg, run), h in hist.groupby(["algorithm", "run"]):
        row = runs[(runs["algorithm"] == alg) & (runs["run"] == run)].iloc[0]
        assert row["throughput_packets"] == h["packets_delivered"].iloc[-1]
        assert np.isclose(row["node_rounds"], h["alive"].sum())

    report = (tmp_path / "report.md").read_text(encoding="utf-8")
    for section in ("## Final result table", "## Hybrid GWO-ABC vs baselines", "### Trade-offs",
                    "## Metric-by-metric interpretation", "## Cluster-head records (run 0)",
                    "## Reproducing this experiment"):
        assert section in report


def test_rerun_reproduces_saved_results(tmp_path):
    """export_ch_logs re-simulates run 0 from the saved config and must match the saved results exactly."""
    from experiments.experiment_runner import export_ch_logs
    cfg = SimulationConfig(n_nodes=20, initial_energy=0.01, rounds=60, opt_iterations=3, checkpoint_round=10,
                           seed=9)
    run_comparison(cfg, ["LEACH", "Hybrid GWO-ABC"], runs=1, out_dir=tmp_path, workers=1, title="t")
    check = export_ch_logs(tmp_path, workers=1)
    assert check["identical"].all()
    assert "Reproducibility check" in (tmp_path / "report.md").read_text(encoding="utf-8")
