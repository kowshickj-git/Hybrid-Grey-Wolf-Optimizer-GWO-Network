import numpy as np
import pytest

from models.energy_model import EnergyModel
from models.network import Network
from simulation.clustering import form_clusters, validate_cluster_heads
from simulation.routing import build_routing_plan
from simulation.transmission import execute_round


def line_network():
    pos = [[0, 0], [10, 0], [20, 0], [30, 0], [100, 0]]
    return Network(pos, 0.5, (50, 0), (100, 10))


def test_validate_drops_dead_and_duplicates(net):
    net.alive[3] = False
    ch = validate_cluster_heads(net, [3, 5, 5, 7, -1, 999])
    assert list(ch) == [5, 7]


def test_cluster_formation_nearest_ch(net):
    ch = [0, 10, 20]
    cl = form_clusters(net, ch)
    for i, slot, d in zip(cl.members, cl.member_slot, cl.member_dist):
        assert d == pytest.approx(net.distances[i, ch].min())
        assert ch[slot] == ch[int(np.argmin(net.distances[i, ch]))]
    assert cl.sizes.sum() == net.n_alive
    assert set(cl.members).isdisjoint(ch)
    assert net.is_ch[ch].all() and net.cluster_id[ch].tolist() == ch


def test_dead_nodes_not_clustered(net):
    net.alive[[1, 2, 3]] = False
    cl = form_clusters(net, [0, 1, 10])
    assert 1 not in cl.ch
    assert not set(cl.members) & {1, 2, 3}
    assert (net.cluster_id[[1, 2, 3]] == -1).all()


def test_cluster_metrics(net):
    cl = form_clusters(net, [0, 10])
    assert cl.avg_distance == pytest.approx(cl.member_dist.mean())
    assert cl.max_distance == pytest.approx(cl.member_dist.max())
    assert cl.imbalance == pytest.approx(cl.sizes.std() / cl.sizes.mean())


def test_no_ch_means_direct_transmission(net):
    cl = form_clusters(net, [])
    assert len(cl.unclustered) == net.n
    em = EnergyModel()
    before = net.energy.copy()
    stats = execute_round(net, build_routing_plan(net, cl), em, 4000)
    assert stats.delivered == stats.generated == net.n
    assert np.allclose(before - net.energy, em.tx_energy(4000, net.dist_to_bs))


def test_round_energy_accounting_exact():
    net = line_network()
    em = EnergyModel()
    k = 4000
    cl = form_clusters(net, [1])               # nodes 0, 2, 3, 4 join CH 1
    before = net.energy.copy()
    stats = execute_round(net, build_routing_plan(net, cl), em, k)
    spent = before - net.energy
    for i in (0, 2, 3, 4):
        assert spent[i] == pytest.approx(em.tx_energy(k, net.distances[i, 1]))
    ch_cost = 4 * (em.rx_energy(k) + em.aggregation_energy(k)) + em.aggregation_energy(k) + \
        em.tx_energy(k, net.dist_to_bs[1])
    assert spent[1] == pytest.approx(ch_cost)
    assert stats.total_energy == pytest.approx(spent.sum())
    assert stats.generated == 5 and stats.delivered == 5 and stats.bs_packets == 1
    assert net.pkt_received[1] == 4 and net.pkt_transmitted.sum() == 5


def test_ch_running_out_of_energy_loses_packets():
    net = line_network()
    em = EnergyModel()
    net.energy[1] = 2.5 * (em.rx_energy(4000) + em.aggregation_energy(4000))   # can receive only 2 packets
    cl = form_clusters(net, [1])
    stats = execute_round(net, build_routing_plan(net, cl), em, 4000)
    assert net.energy[1] == 0.0
    assert stats.delivered == 0                       # CH died before forwarding
    assert stats.lost == 5
    assert net.detect_dead(1).tolist() == [1]
