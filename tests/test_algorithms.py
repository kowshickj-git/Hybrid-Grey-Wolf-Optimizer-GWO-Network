"""Validation that each algorithm really performs its defining operations (section 31)."""
import numpy as np
import pytest

from algorithms import ABLATION_VARIANTS, MAIN_ALGORITHMS, make_algorithm
from algorithms.abc import ArtificialBeeColony, BeeColony
from algorithms.fitness import FitnessContext
from algorithms.gwo import GreyWolfOptimizer, WolfPack, distinct_best, sigmoid_transfer
from algorithms.hybrid_gwo_abc import HybridGWOABC
from algorithms.leach import LEACH


# ------------------------------------------------------------------ LEACH
def test_leach_threshold_formula(cfg):
    leach = LEACH(cfg, seed=0)
    leach.reset(type("N", (), {"n": 10})())
    p = cfg.ch_percentage
    for r in range(1, 21):
        assert leach.threshold(r) == pytest.approx(min(1.0, p / (1 - p * ((r - 1) % 20))))
    assert leach.threshold(20) == pytest.approx(1.0)


def test_leach_rotation_once_per_epoch(net, cfg):
    leach = LEACH(cfg, seed=1)
    leach.reset(net)
    counts = np.zeros(net.n, int)
    for r in range(1, leach.epoch + 1):
        counts[leach.select(net, r).ch] += 1
    assert counts.max() <= 1                       # nobody is CH twice in one epoch
    assert counts.sum() == net.n                   # T(n) reaches 1 in the last round of the epoch


def test_leach_is_probabilistic_and_ignores_dead(net, cfg):
    net.alive[:20] = False
    sizes = []
    for seed in range(40):
        leach = LEACH(cfg, seed=seed)
        leach.reset(net)
        ch = leach.select(net, 1).ch
        assert not set(ch) & set(range(20))
        sizes.append(len(ch))
    assert len(set(sizes)) > 1                         # election is random, CH count varies
    assert np.mean(sizes) == pytest.approx(cfg.ch_percentage * 20, abs=0.6)   # E[K] = p * eligible


# ------------------------------------------------------------------ GWO
def test_sigmoid_transfer():
    assert sigmoid_transfer(np.array([0.5]))[0] == pytest.approx(0.5)
    assert sigmoid_transfer(np.array([1.0]))[0] > 0.99
    assert sigmoid_transfer(np.array([0.0]))[0] < 0.01


def test_distinct_best():
    X = np.array([[1, 0], [1, 0], [0, 1], [1, 1]], bool)
    idx = distinct_best(X, np.array([0.1, 0.1, 0.3, 0.2]), 3)
    assert list(idx) == [0, 3, 2]


def test_gwo_leaders_are_alpha_beta_delta(net, cfg):
    ctx = FitnessContext(net, cfg)
    rng = np.random.default_rng(0)
    pack = WolfPack.create(ctx, rng, 10)
    assert np.all(np.diff(pack.leader_fit) >= 0)                     # alpha <= beta <= delta
    assert pack.leader_fit[0] == pytest.approx(pack.fit.min())
    for t in range(5):
        prev = pack.leader_fit.copy()
        pack.step(ctx, rng, 2 - 2 * t / 5)
        assert pack.leader_fit[0] <= prev[0] + 1e-12                  # elitist alpha
        assert len({tuple(L) for L in pack.leaders}) == 3


def test_gwo_wolves_follow_leaders_when_a_is_zero(net, cfg):
    ctx = FitnessContext(net, cfg)
    rng = np.random.default_rng(0)
    pack = WolfPack.create(ctx, rng, 30)
    pack.leaders[:] = pack.leaders[0]             # all three leaders identical
    pack.step(ctx, rng, a=0.0)                    # A = 0 -> X_new = leader exactly (prob ~0.993)
    agree = (pack.X == pack.leaders[0]).mean()
    assert agree > 0.97


def test_gwo_converges(net, cfg):
    ctx = FitnessContext(net, cfg)
    _, curve = GreyWolfOptimizer(12, 15).run(ctx, np.random.default_rng(0))
    assert np.all(np.diff(curve) <= 1e-12) and curve[-1] < curve[0]


# ------------------------------------------------------------------ ABC
def test_abc_phases(net, cfg):
    ctx = FitnessContext(net, cfg)
    rng = np.random.default_rng(0)
    col = BeeColony.create(ctx, rng, 6, limit=3)
    before = col.fit.copy()
    col.employed_phase(ctx, rng)
    assert np.all(col.fit <= before + 1e-12)                          # greedy selection
    assert ((col.trial == 0) | (col.trial == 1)).all()
    p = col.selection_probabilities()
    assert p.sum() == pytest.approx(1.0)
    assert p[np.argmin(col.fit)] == pytest.approx(p.max())            # fitter sources more likely
    col.onlooker_phase(ctx, rng)
    assert col.best_fit == pytest.approx(min(col.best_fit, col.fit.min()))


def test_abc_scout_replaces_exhausted_source(net, cfg):
    ctx = FitnessContext(net, cfg)
    rng = np.random.default_rng(0)
    col = BeeColony.create(ctx, rng, 4, limit=2)
    best_before = col.best_fit
    col.trial[2] = 5
    old = col.foods[2].copy()
    assert col.scout_phase(ctx, rng)
    assert col.trial[2] == 0 and not np.array_equal(old, col.foods[2])
    assert col.best_fit <= best_before                                # best solution preserved
    assert not col.scout_phase(ctx, rng)                              # nothing above the limit now


def test_abc_neighbours_valid(net, cfg):
    ctx = FitnessContext(net, cfg)
    rng = np.random.default_rng(0)
    col = BeeColony.create(ctx, rng, 8, limit=3)
    V = col.neighbours(ctx, rng, np.arange(8))
    K = V.sum(1)
    assert (K >= ctx.k_min).all() and (K <= ctx.k_max).all()
    assert not (V & ~ctx.eligible).any()
    assert (V != col.foods).any(1).mean() > 0.5                        # neighbours actually move


def test_abc_converges(net, cfg):
    ctx = FitnessContext(net, cfg)
    _, curve = ArtificialBeeColony(12, 5, 15).run(ctx, np.random.default_rng(0))
    assert np.all(np.diff(curve) <= 1e-12) and curve[-1] < curve[0]


# ------------------------------------------------------------------ Hybrid
def test_hybrid_exchanges_information(net, cfg):
    ctx = FitnessContext(net, cfg)
    res = HybridGWOABC(6, 4, 5, 20).optimize(ctx, np.random.default_rng(0))
    assert res.info["transfers"] > 0                                  # GWO -> ABC
    assert res.info["feedbacks"] >= 0
    c = {k: np.array(v) for k, v in res.curves.items()}
    assert len(c["gwo"]) == len(c["abc"]) == len(c["hybrid"]) == 21
    assert np.allclose(c["hybrid"], np.minimum(c["gwo"], c["abc"]))   # elite = best of both
    assert np.all(np.diff(c["hybrid"]) <= 1e-12)
    assert ctx.evaluate(res.best[None, :])[0] == pytest.approx(res.fitness)


def test_hybrid_feedback_reaches_gwo(net, cfg):
    ctx = FitnessContext(net, cfg)
    total = 0
    for s in range(5):
        res = HybridGWOABC(6, 4, 5, 20).optimize(ctx, np.random.default_rng(s))
        total += res.info["feedbacks"]
    assert total > 0                                                  # ABC -> GWO happened


def test_hybrid_budget_matches_standalone(cfg):
    h = HybridGWOABC.from_config(cfg)
    per_iter_hybrid = h.n_wolves + 2 * h.n_sources
    assert per_iter_hybrid == cfg.gwo.population == cfg.abc.colony_size


@pytest.mark.parametrize("name", MAIN_ALGORITHMS + ["Random"] + ABLATION_VARIANTS)
def test_every_algorithm_returns_valid_ch(net, cfg, name):
    net.alive[:5] = False
    alg = make_algorithm(name, cfg, seed=0)
    alg.reset(net)
    sel = alg.select(net, 1)
    assert len(np.unique(sel.ch)) == len(sel.ch)
    assert net.alive[sel.ch].all()
    if name not in ("LEACH", "Random"):
        ctx = FitnessContext(net, cfg)
        assert ctx.k_min <= len(sel.ch) <= ctx.k_max
        assert sel.evaluations > 0


def test_unknown_algorithm(cfg):
    with pytest.raises(ValueError):
        make_algorithm("PSO", cfg)
