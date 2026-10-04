"""Base paper (DEAI-PSO, Haris & Nam 2025) re-implementation: equations, decoding, free nodes."""
import numpy as np
import pytest

from algorithms import ATTRIBUTION_VARIANTS, BASE_PAPER_ALGORITHMS, make_algorithm
from algorithms.base import free_nodes
from algorithms.deai_pso import DEAIPSO, PaperFitness, deai_inertia, tvac
from algorithms.fitness import FitnessContext
from config import SimulationConfig
from models.energy_model import EnergyModel
from models.network import Network
from simulation.simulator import Simulator


@pytest.fixture
def bp_cfg():
    # base paper scenario 1 geometry (BS outside the field), small budget for speed
    return SimulationConfig(n_nodes=60, bs_x=200.0, bs_y=50.0, ch_percentage=0.10, opt_iterations=6,
                            rounds=40, checkpoint_round=10, seed=3)


def test_deai_inertia_equation():
    assert deai_inertia(0.0, 0, 10) == pytest.approx(np.exp(-1))          # particle at its personal best
    assert deai_inertia(5.0, 0, 10) == pytest.approx(1.0, abs=1e-6)        # far from Pbest, early
    assert deai_inertia(0.3, 9, 10) == pytest.approx(np.exp(-np.exp(-0.3)))
    w = deai_inertia(np.array([0.05, 0.05]), np.array([0, 9]), 10)
    assert w[0] > w[1]                                                     # inertia decays over iterations


def test_tvac_equations():
    assert tvac(0, 20, 2.5, 0.5) == pytest.approx(2.5)
    assert tvac(20, 20, 2.5, 0.5) == pytest.approx(0.5)
    assert tvac(10, 20, 0.5, 2.5) == pytest.approx(1.5)


def test_paper_fitness_matches_hand_calculation(bp_cfg):
    net = Network.deploy(bp_cfg)
    free = np.array([], dtype=int)
    ctx = FitnessContext(net, bp_cfg, exclude=free)
    paper = PaperFitness(ctx, net, free, a=0.4)
    x = ctx.random_solutions(1, np.random.default_rng(0))[0]
    em, k = EnergyModel(bp_cfg.energy), bp_cfg.packet_bits
    ch = np.flatnonzero(x)
    cost = np.zeros(ctx.m)
    for i in range(ctx.m):
        if x[i]:
            continue
        j = ch[np.argmin(ctx.D[i, ch])]
        cost[i] = em.tx_energy(k, ctx.D[i, j])
        cost[j] += em.rx_energy(k) + em.aggregation_energy(k)
    for j in ch:
        cost[j] += em.aggregation_energy(k) + em.tx_energy(k, ctx.d_bs[j])
    R = ctx.E - cost
    expected = 0.4 * cost.sum() + 0.6 * ctx.m * R.std(ddof=1)
    assert paper.evaluate(x[None, :])[0] == pytest.approx(expected, rel=1e-10)


def test_decode_gives_k_distinct_eligible_nodes(bp_cfg):
    net = Network.deploy(bp_cfg)
    net.energy[:20] = 0.1                                   # below mean -> not eligible
    ctx = FitnessContext(net, bp_cfg)
    rng = np.random.default_rng(1)
    pos = rng.uniform(0, 100, size=(12, 6, 2))
    X = DEAIPSO.decode(ctx, pos, net.positions[ctx.ids])
    assert (X.sum(1) == 6).all()
    assert not (X & ~ctx.eligible).any()


def test_deai_pso_converges_and_is_valid(bp_cfg):
    net = Network.deploy(bp_cfg)
    ctx = FitnessContext(net, bp_cfg)
    opt = DEAIPSO.from_config(bp_cfg)
    res = opt.optimize(ctx, np.random.default_rng(0), net, np.array([], dtype=int), net.area)
    curve = np.array(res.curves["deai_pso"])
    assert np.all(np.diff(curve) <= 1e-12) and curve[-1] <= curve[0]
    assert res.best.sum() == min(ctx.k_opt, ctx.n_eligible) == 6
    # equal evaluation budget: 36 particles x (iterations + 1) ~ opt_iterations x gwo.population
    assert opt.iterations == round(bp_cfg.opt_iterations * bp_cfg.gwo.population / 36)


def test_free_nodes_send_directly(bp_cfg):
    cfg = bp_cfg.replace(free_node_radius=120.0)            # nodes within 120 m of (200, 50) are free
    sim = Simulator(cfg, "DEAI-PSO")
    free = free_nodes(sim.network, cfg.free_node_radius)
    assert 0 < len(free) < sim.network.n
    before = sim.network.energy.copy()
    sim.step()
    cl = sim.last_clusters
    assert not set(free) & set(cl.ch) and not set(free) & set(cl.members)
    assert set(free) <= set(cl.unclustered)
    em = EnergyModel(cfg.energy)
    spent = before[free] - sim.network.energy[free]
    assert np.allclose(spent, em.tx_energy(cfg.packet_bits, sim.network.dist_to_bs[free]))


@pytest.mark.parametrize("name", sorted(set(BASE_PAPER_ALGORITHMS + ATTRIBUTION_VARIANTS)))
def test_base_paper_algorithms_select_valid_chs(bp_cfg, name):
    net = Network.deploy(bp_cfg)
    net.alive[:4] = False
    alg = make_algorithm(name, bp_cfg, seed=0)
    alg.reset(net)
    sel = alg.select(net, 1)
    assert len(np.unique(sel.ch)) == len(sel.ch) and net.alive[sel.ch].all()
    if name.startswith("DEAI-PSO") or name.endswith("fixed K)"):
        assert len(sel.ch) == round(0.10 * net.n_alive)            # exactly 10 % CHs
    if "Eq. 12" in name or name.startswith("DEAI-PSO"):
        assert sel.fitness is None and sel.evaluations > 0          # re-scored by the simulator, budget counted
