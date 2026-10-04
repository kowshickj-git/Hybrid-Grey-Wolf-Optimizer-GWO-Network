"""The worked examples printed in docs/ are recomputed here with the project's own code, so the documentation
cannot silently disagree with the implementation (docs/03_MATHEMATICS.md, 04_ALGORITHMS.md, 02_CONCEPTS.md)."""
from math import comb

import numpy as np
import pytest

from algorithms.abc import BeeColony
from algorithms.deai_pso import deai_inertia, tvac
from algorithms.fitness import ch_count_bounds
from algorithms.gwo import WolfPack, control_parameter, sigmoid_transfer
from algorithms.leach import LEACH
from config import SimulationConfig
from evaluation.metrics import lifetime_rounds
from evaluation.statistics import cliffs_delta, holm, improvement, paired_test
from models.energy_model import EnergyModel
from models.network import Network
from simulation.clustering import form_clusters
from visualization.diagrams import EXAMPLE_BAD, EXAMPLE_GOOD, example_context

MJ = 1e-3
K = 4000


def test_radio_model_examples():
    em = EnergyModel()
    assert em.d0 == pytest.approx(87.706, abs=1e-3)
    assert em.tx_energy(K, 20) == pytest.approx(0.216 * MJ)
    assert em.tx_energy(K, 100) == pytest.approx(0.72 * MJ)
    assert em.tx_energy(K, 150) == pytest.approx(2.8325 * MJ)
    assert em.rx_energy(K) == pytest.approx(0.2 * MJ)
    assert em.aggregation_energy(K) == pytest.approx(0.02 * MJ)


def test_member_vs_cluster_head_round_energy():
    em = EnergyModel()
    member = em.tx_energy(K, 20)
    ch = 19 * (em.rx_energy(K) + em.aggregation_energy(K)) + em.aggregation_energy(K) + em.tx_energy(K, 40)
    assert ch == pytest.approx(4.464 * MJ)
    assert round(ch / member) == 21
    assert int(0.5 / member) == 2314 and int(0.5 / ch) == 112
    assert 0.5 / (K * SimulationConfig().energy.e_elec) == pytest.approx(2500)      # base paper bound


def test_ch_count_examples():
    assert ch_count_bounds(100, 0.05, 0.5) == (5, 2, 8)
    assert ch_count_bounds(60, 0.05, 0.5) == (3, 1, 5)
    assert ch_count_bounds(100, 0.10, 0.5) == (10, 5, 15)
    assert sum(comb(100, k) for k in range(2, 9)) == 203_366_882_895


def test_fitness_worked_example():
    net, cfg, ctx = example_context()
    assert ctx.score_bounds == (2, 1, 3)
    assert ctx.d_norm == pytest.approx(113.137, abs=1e-3)
    assert ctx.bs_norm == pytest.approx(56.569, abs=1e-3)
    assert ctx.e_upper == pytest.approx(7.631808 * MJ)
    a = ctx.components(ctx.from_node_ids(EXAMPLE_GOOD))
    b = ctx.components(ctx.from_node_ids(EXAMPLE_BAD))
    expected_a = {"energy": 0.153568, "intra_distance": 0.106694, "ch_bs_distance": 0.883883, "balance": 0.0,
                  "ch_count": 0.0, "invalid": 0.0, "fitness": 0.249521}
    expected_b = {"energy": 0.26438, "intra_distance": 0.696713, "ch_bs_distance": 0.941942, "balance": 1 / 3,
                  "ch_count": 0.0, "invalid": 0.0, "fitness": 0.491881}
    for got, exp in ((a, expected_a), (b, expected_b)):
        for key, value in exp.items():
            assert got[key] == pytest.approx(value, abs=1e-6), key
    no_ch = ctx.components(np.zeros(6, dtype=bool))
    four = ctx.components(ctx.from_node_ids([0, 1, 3, 4]))
    assert no_ch["invalid"] == four["invalid"] == 1.0
    assert no_ch["fitness"] == pytest.approx(10.4018, abs=1e-4) and four["fitness"] == pytest.approx(10.4034, abs=1e-4)
    # clusters drawn in the figure: members join their nearest CH
    cl = form_clusters(net, EXAMPLE_GOOD)
    assert dict(zip(cl.members.tolist(), cl.ch[cl.member_slot].tolist())) == {0: 1, 2: 1, 3: 4, 5: 4}


def test_eligibility_example():
    energy = np.array([0.48, 0.50, 0.21, 0.47, 0.49, 0.46, 0.30, 0.44, 0.50, 0.45])
    assert energy.mean() == pytest.approx(0.43)
    assert np.flatnonzero(energy < energy.mean()).tolist() == [2, 6]


def test_leach_threshold_examples():
    cfg = SimulationConfig()
    leach = LEACH(cfg, 0)
    leach.reset(Network.deploy(cfg))
    assert leach.epoch == 20
    expected = {1: 0.05, 10: 0.0909, 19: 0.5, 20: 1.0, 21: 0.05}
    for r, t in expected.items():
        assert leach.threshold(r) == pytest.approx(t, abs=1e-4)


class FixedRandom:
    """Stand-in generator returning documented random numbers, one value per call (filled to the shape)."""

    def __init__(self, values):
        self.values = list(values)

    def random(self, shape):
        return np.full(shape, self.values.pop(0))


def test_gwo_step_matches_worked_example(monkeypatch):
    import algorithms.gwo as gwo
    _, _, ctx = example_context()
    a = control_parameter(5, 30)
    assert a == pytest.approx(1.6667, abs=1e-4)
    assert control_parameter(0, 30) == 2.0 and control_parameter(15, 30) == 1.0
    # node 1: alpha and beta say "CH" (1), delta says "not CH" (0); the wolf currently has 0
    leaders = np.array([[0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 0, 0], [1, 0, 0, 0, 1, 0]], dtype=bool)
    pack = WolfPack(np.zeros((1, 6), dtype=bool), np.array([1.0]), leaders, np.array([0.1, 0.2, 0.3]))
    seen = []
    monkeypatch.setattr(gwo, "sigmoid_transfer", lambda y: seen.append(y.copy()) or sigmoid_transfer(y))
    # r1, r2 for alpha, beta, delta (in the order WolfPack.step draws them), then the sampling numbers
    pack.step(ctx, FixedRandom([0.8, 0.3, 0.3, 0.9, 0.6, 0.5, 0.5]), a)
    y = seen[0][0, 1]
    assert y == pytest.approx((0.4 + 2.2 + 0.0) / 3, abs=1e-9)
    assert y == pytest.approx(0.8667, abs=1e-4)
    assert sigmoid_transfer(np.array(y)) == pytest.approx(0.9751, abs=1e-4)
    assert sigmoid_transfer(np.array(0.5)) == pytest.approx(0.5)


def test_abc_probability_example():
    col = BeeColony(np.zeros((3, 4), dtype=bool), np.array([0.20, 0.25, 0.40]), np.zeros(3, dtype=int), 10,
                    np.zeros(4, dtype=bool), 0.20)
    assert col.selection_probabilities() == pytest.approx([0.3550, 0.3408, 0.3043], abs=1e-4)


def test_deai_pso_examples():
    assert deai_inertia(0.1, 0, 17) == pytest.approx(0.833, abs=1e-3)
    assert deai_inertia(0.1, 16, 17) == pytest.approx(0.405, abs=1e-3)
    assert deai_inertia(0.0, 5, 17) == pytest.approx(np.exp(-1))
    assert tvac(0, 17, 2.5, 0.5) == 2.5 and tvac(17, 17, 2.5, 0.5) == 0.5
    e = np.array([0.001, 0.002, 0.005])
    r = 0.5 - e
    assert 0.8 * e.sum() + 0.2 * 3 * r.std(ddof=1) == pytest.approx(0.007649, abs=1e-6)


def test_metric_and_statistics_examples():
    lt = lifetime_rounds(np.array([120, 150, 150, 200]), 4)
    assert (lt["fnd"], lt["hnd"], lt["lnd"]) == (120, 150, 200)
    assert sum([4, 4, 3, 1]) == 12                                         # node-rounds example
    assert improvement(1127.65, 891.50, True) == pytest.approx(26.49, abs=0.01)
    assert improvement(21.90, 22.60, False) == pytest.approx(3.1, abs=0.05)
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert cliffs_delta([3, 4], [1, 3]) == pytest.approx(0.75)
    base = np.linspace(10, 12, 20)
    assert paired_test(base[:5] + 1, base[:5]) == pytest.approx(0.0625)    # smallest p possible with 5 runs
    assert paired_test(base + 1, base) < 1e-4                              # 20 wins out of 20


def test_documentation_figures_are_generated(tmp_path):
    from visualization.diagrams import make_all
    paths = make_all(tmp_path)
    assert len(paths) >= 11 and all(p.exists() and p.stat().st_size > 10_000 for p in paths)
