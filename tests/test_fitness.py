import numpy as np
import pytest

from algorithms.fitness import COMPONENTS, FitnessContext, ch_count_bounds


def test_count_bounds():
    assert ch_count_bounds(100, 0.05, 0.5) == (5, 2, 8)
    assert ch_count_bounds(3, 0.05, 0.5)[0] == 1
    assert ch_count_bounds(0, 0.05, 0.5) == (0, 0, 0)


def test_components_normalised_and_weighted(net, cfg):
    ctx = FitnessContext(net, cfg)
    x = ctx.random_solutions(1, np.random.default_rng(0))[0]
    comp = ctx.components(x)
    for c in COMPONENTS:
        assert 0.0 <= comp[c] <= 1.0
    w = cfg.weights
    expected = (w.energy * comp["energy"] + w.intra_distance * comp["intra_distance"] +
                w.ch_bs_distance * comp["ch_bs_distance"] + w.balance * comp["balance"] +
                w.ch_count * comp["ch_count"])
    assert comp["invalid"] == 0
    assert comp["fitness"] == pytest.approx(expected)


def test_batch_equals_individual(net, cfg):
    ctx = FitnessContext(net, cfg)
    X = ctx.random_solutions(12, np.random.default_rng(1))
    batch = ctx.evaluate(X)
    single = [ctx.evaluate(x[None, :])[0] for x in X]
    assert np.allclose(batch, single)


def test_invalid_solutions_penalised(net, cfg):
    ctx = FitnessContext(net, cfg)
    none = np.zeros(ctx.m, bool)
    too_many = np.ones(ctx.m, bool)
    ok = ctx.random_solutions(1, np.random.default_rng(0))[0]
    f_none, f_many, f_ok = ctx.evaluate(np.stack([none, too_many, ok]))
    assert f_none >= cfg.invalid_penalty and f_many >= cfg.invalid_penalty
    assert f_ok < 1.0


def test_starving_ch_is_infeasible(net, cfg):
    ctx = FitnessContext(net, cfg)
    x = ctx.random_solutions(1, np.random.default_rng(0))[0]
    ctx.E[np.flatnonzero(x)[0]] = 1e-9
    ctx._E_pad[:-1] = ctx.E
    assert ctx.components(x)["invalid"] == 1


def test_energy_term_prefers_high_energy_ch(net, cfg):
    net.energy[5] = 0.05
    ctx = FitnessContext(net, cfg.replace(ch_energy_threshold=0.0))
    a = ctx.from_node_ids([5, 20])
    b = ctx.from_node_ids([6, 20])
    assert ctx.components(a)["energy"] > ctx.components(b)["energy"]


def test_distance_term_prefers_central_ch():
    from config import SimulationConfig
    from models.network import Network
    cfg = SimulationConfig(n_nodes=4)
    net = Network([[0, 0], [10, 0], [20, 0], [90, 0]], 0.5, (10, 5), (100, 10))
    ctx = FitnessContext(net, cfg)
    near, far = ctx.from_node_ids([1]), ctx.from_node_ids([3])
    assert ctx.components(near)["intra_distance"] < ctx.components(far)["intra_distance"]
    assert ctx.components(near)["ch_bs_distance"] < ctx.components(far)["ch_bs_distance"]


def test_repair_enforces_bounds_and_eligibility(net, cfg):
    net.energy[:20] = 0.1                      # below mean -> ineligible
    ctx = FitnessContext(net, cfg)
    rng = np.random.default_rng(0)
    X = rng.random((50, ctx.m)) < 0.5
    X[0] = False
    R = ctx.repair(X, rng=rng)
    K = R.sum(1)
    assert (K >= ctx.k_min).all() and (K <= ctx.k_max).all()
    assert not (R & ~ctx.eligible).any()
    rs = ctx.random_solutions(50, rng)
    assert not (rs & ~ctx.eligible).any()


def test_dead_nodes_excluded_from_search_space(net, cfg):
    net.alive[:10] = False
    ctx = FitnessContext(net, cfg)
    assert ctx.m == net.n - 10
    assert not set(ctx.ids) & set(range(10))
