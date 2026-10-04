import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import SimulationConfig  # noqa: E402
from models.network import Network  # noqa: E402


@pytest.fixture
def cfg():
    return SimulationConfig(n_nodes=40, rounds=60, opt_iterations=8, checkpoint_round=20, seed=7)


@pytest.fixture
def net(cfg):
    return Network.deploy(cfg)
