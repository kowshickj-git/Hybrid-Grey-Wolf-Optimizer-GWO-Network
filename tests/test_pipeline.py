"""End-to-end: network -> optimisation -> CH selection -> clustering -> transmission
-> energy update -> node death -> metrics -> results."""
import numpy as np
import pandas as pd
import pytest

from config import SimulationConfig
from evaluation.comparison import result_table
from evaluation.metrics import lifetime_rounds
from evaluation.statistics import cliffs_delta, compare_to_baselines, holm, improvement
from models.network import Network
from simulation.simulator import Simulator, run_simulation


@pytest.fixture
def small():
    # low initial energy so that nodes actually die within the horizon
    return SimulationConfig(n_nodes=30, initial_energy=0.02, rounds=400, opt_iterations=5, checkpoint_round=10,
                            seed=11)


@pytest.mark.parametrize("alg", ["LEACH", "GWO", "ABC", "Hybrid GWO-ABC"])
def test_full_pipeline(small, alg):
    res = run_simulation(small, alg)
    h = res.history
    assert (np.diff(h["residual_energy"]) <= 1e-12).all()             # energy only decreases
    assert (h["round_energy"] > 0).all()
    assert h["dead"].iloc[-1] > 0                                      # nodes actually die
    assert (np.diff(h["alive"]) <= 0).all()
    s = res.summary
    assert s["fnd"] <= s["hnd"] <= s["lnd"]
    assert 0 <= s["pdr"] <= 1
    assert s["throughput_packets"] == h["packets_delivered"].iloc[-1]
    assert s["energy_consumed_cp"] == pytest.approx(small.n_nodes * small.initial_energy - s["residual_energy_cp"])
    if alg != "LEACH":
        assert s["evaluations"] > 0


def test_dead_nodes_never_participate(small):
    sim = Simulator(small, "Hybrid GWO-ABC")
    dead_seen: set = set()
    while not sim.finished:
        rec = sim.step()
        net = sim.network
        ch = sim.last_clusters.ch
        assert not set(ch) & dead_seen
        assert not set(sim.last_clusters.members) & dead_seen
        dead_seen |= set(np.flatnonzero(~net.alive))
        assert rec.alive == net.n_alive
    assert sim.network.n_alive == 0 or sim.round == small.rounds


def test_cluster_head_records(small):
    """Section 13: CH ids, residual energy, coordinates and CH-BS distance are recorded every round."""
    sim = Simulator(small, "Hybrid GWO-ABC")
    for _ in range(5):
        energy_before = sim.network.energy.copy()
        alive_before = sim.network.alive.copy()
        sim.step()
        log = sim.ch_log()
        rows = log[log["round"] == sim.round]
        ch = rows["ch_id"].to_numpy()
        assert set(ch) == set(sim.last_clusters.ch)
        assert alive_before[ch].all() and len(set(ch)) == len(ch)                   # valid, no duplicates
        assert np.allclose(rows["residual_energy"], energy_before[ch])                  # energy at selection
        assert np.allclose(rows[["x", "y"]], sim.network.positions[ch])
        assert np.allclose(rows["distance_to_bs"], sim.network.dist_to_bs[ch])
        assert rows["cluster_size"].sum() == alive_before.sum()                         # every alive node clustered
    assert list(sim.result().ch_log.columns) == ["round", "ch_id", "x", "y", "residual_energy", "distance_to_bs",
                                                 "cluster_size"]


def test_lifetime_definitions():
    dr = np.array([5, 9, -1, 7])
    lt = lifetime_rounds(dr, 4)
    assert lt["fnd"] == 5 and lt["hnd"] == 7 and np.isnan(lt["lnd"])
    lt = lifetime_rounds(np.array([5, 9, 3, 7]), 4)
    assert lt["lnd"] == 9


def test_same_network_for_all_algorithms(small):
    net = Network.deploy(small)
    a = Simulator(small, "LEACH", net)
    b = Simulator(small, "GWO", net)
    assert np.array_equal(a.network.positions, b.network.positions)
    assert a.network is not b.network and a.network is not net


def test_reproducible(small):
    r1 = run_simulation(small.replace(rounds=30), "Hybrid GWO-ABC")
    r2 = run_simulation(small.replace(rounds=30), "Hybrid GWO-ABC")
    pd.testing.assert_frame_equal(r1.history.drop(columns="selection_time"),
                                  r2.history.drop(columns="selection_time"))


def test_improvement_formulas():
    assert improvement(120, 100, True) == pytest.approx(20)
    assert improvement(80, 100, False) == pytest.approx(20)
    assert improvement(120, 100, False) == pytest.approx(-20)
    assert np.isnan(improvement(1, 0, True))


def test_statistics_helpers():
    assert cliffs_delta([3, 4], [1, 2]) == 1.0
    assert holm([0.01, 0.04, 0.03]).tolist() == pytest.approx([0.03, 0.06, 0.06])


def test_results_come_from_runs():
    runs = pd.DataFrame({
        "algorithm": ["A"] * 3 + ["B"] * 3, "run": [0, 1, 2] * 2,
        **{m: [10.0, 12.0, 14.0, 20.0, 22.0, 24.0] for m in
           ["fnd", "hnd", "lnd", "residual_energy_cp", "energy_consumed_cp", "throughput_packets", "pdr",
            "avg_cluster_distance", "avg_ch_bs_distance", "runtime", "final_fitness"]}})
    t = result_table(runs, ["A", "B"], with_std=False)
    assert t.loc["FND (rounds)", "A"] == "12" and t.loc["FND (rounds)", "B"] == "22"
    cmp = compare_to_baselines(runs, "B", ["A"], ["fnd", "runtime"])
    fnd = cmp[cmp["metric"] == "fnd"].iloc[0]
    rt = cmp[cmp["metric"] == "runtime"].iloc[0]
    assert fnd["improvement_pct"] == pytest.approx(100 * (22 - 12) / 12)
    assert rt["improvement_pct"] == pytest.approx(100 * (12 - 22) / 12)   # lower is better -> negative
