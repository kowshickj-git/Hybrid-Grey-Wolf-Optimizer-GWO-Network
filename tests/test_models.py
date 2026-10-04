import numpy as np
import pytest

from config import EnergyConfig, SimulationConfig
from models.energy_model import EnergyModel
from models.network import Network
from models.node import SensorNode


def test_node_creation(net):
    node = net.nodes[3]
    assert isinstance(node, SensorNode)
    assert node.node_id == 3
    assert node.residual_energy == node.initial_energy == 0.5
    assert node.is_alive and node.status == "ALIVE"
    assert not node.is_cluster_head and node.cluster_id == -1
    assert node.packets_generated == node.packets_transmitted == node.packets_received == 0
    d = node.as_dict()
    for key in ("node_id", "x", "y", "initial_energy", "residual_energy", "status", "is_cluster_head",
                "cluster_id", "distance_to_ch", "distance_to_bs", "packets_generated", "packets_transmitted",
                "packets_received"):
        assert key in d


def test_node_view_writes_through(net):
    net.nodes[0].residual_energy = 0.1
    assert net.energy[0] == pytest.approx(0.1)
    net.nodes[0].residual_energy = -5
    assert net.energy[0] == 0.0


def test_deployment_inside_area_and_reproducible():
    cfg = SimulationConfig(n_nodes=200, area_width=80, area_height=50, seed=3)
    a, b = Network.deploy(cfg), Network.deploy(cfg)
    assert np.array_equal(a.positions, b.positions)
    assert (a.positions[:, 0] >= 0).all() and (a.positions[:, 0] <= 80).all()
    assert (a.positions[:, 1] >= 0).all() and (a.positions[:, 1] <= 50).all()
    assert not np.array_equal(a.positions, Network.deploy(cfg, seed=4).positions)


def test_distances(net):
    i, j = 2, 9
    expected = np.hypot(*(net.positions[i] - net.positions[j]))
    assert net.distances[i, j] == pytest.approx(expected)
    assert net.nodes[i].distance_to(net.nodes[j]) == pytest.approx(expected)
    assert net.dist_to_bs[i] == pytest.approx(np.hypot(*(net.positions[i] - net.bs)))
    assert np.allclose(net.distances, net.distances.T)


def test_copy_is_independent(net):
    c = net.copy()
    c.energy[:] = 0
    assert net.total_energy == pytest.approx(net.n * 0.5)


def test_transmission_energy_both_regimes():
    em = EnergyModel(EnergyConfig())
    k = 4000
    assert em.d0 == pytest.approx(np.sqrt(10e-12 / 0.0013e-12))
    d_short, d_long = 30.0, 120.0
    assert em.tx_energy(k, d_short) == pytest.approx(50e-9 * k + 10e-12 * k * d_short ** 2)
    assert em.tx_energy(k, d_long) == pytest.approx(50e-9 * k + 0.0013e-12 * k * d_long ** 4)
    arr = em.tx_energy(k, np.array([d_short, d_long]))
    assert arr.shape == (2,)


def test_reception_and_aggregation_energy():
    em = EnergyModel(EnergyConfig())
    assert em.rx_energy(4000) == pytest.approx(50e-9 * 4000)
    assert em.aggregation_energy(4000) == pytest.approx(5e-9 * 4000)
    assert em.aggregation_energy(4000, 3) == pytest.approx(3 * 5e-9 * 4000)


def test_node_death(net):
    net.energy[[1, 4]] = 0.0
    net.energy[5] = -1e-6
    dead = net.detect_dead(round_no=12)
    assert set(dead) == {1, 4, 5}
    assert not net.alive[[1, 4, 5]].any()
    assert (net.death_round[[1, 4, 5]] == 12).all()
    assert net.nodes[1].status == "DEAD"
    assert net.energy[5] == 0.0
    assert len(net.detect_dead(13)) == 0          # already dead nodes are not re-counted


def test_config_roundtrip_and_replace(tmp_path):
    cfg = SimulationConfig().replace(**{"gwo.population": 33, "weights.energy": 0.4, "n_nodes": 77})
    p = tmp_path / "c.json"
    cfg.save(p)
    loaded = SimulationConfig.load(p)
    assert loaded == cfg
    assert loaded.gwo.population == 33 and loaded.weights.energy == 0.4
    with pytest.raises(KeyError):
        cfg.replace(nonexistent=1)
    with pytest.raises(ValueError):
        SimulationConfig(ch_percentage=1.5).validate()
