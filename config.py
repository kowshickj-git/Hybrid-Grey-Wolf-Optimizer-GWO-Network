"""Central, serialisable configuration for every simulation and experiment.

Every value used by the simulator lives here so that an experiment can be
saved to JSON and reproduced exactly (see ``SimulationConfig.save`` /
``SimulationConfig.load``).
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields, is_dataclass
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"
QUICK_RESULTS_DIR = PROJECT_ROOT / "results_quick"   # smoke-test output, kept apart from the real results
DATA_DIR = PROJECT_ROOT / "data"


@dataclass
class EnergyConfig:
    """First-order radio model parameters (Heinzelman et al., LEACH)."""

    e_elec: float = 50e-9        # J/bit   electronics energy (TX and RX)
    e_fs: float = 10e-12         # J/bit/m^2 free-space amplifier
    e_mp: float = 0.0013e-12     # J/bit/m^4 multipath amplifier
    e_da: float = 5e-9           # J/bit/signal data aggregation


@dataclass
class FitnessWeights:
    """Weights of the multi-objective CH fitness (all terms are minimised).

    The defaults are a reasonable starting point, *not* proven optima; the
    sensitivity analysis varies them.
    """

    energy: float = 0.30          # w1: energy cost (CH residual energy + round consumption)
    intra_distance: float = 0.25  # w2: member -> CH distance
    ch_bs_distance: float = 0.20  # w3: CH -> BS distance
    balance: float = 0.15         # w4: cluster-size imbalance
    ch_count: float = 0.10        # w5: deviation from target CH count


@dataclass
class GWOConfig:
    population: int = 20          # number of wolves


@dataclass
class ABCConfig:
    colony_size: int = 20         # employed + onlooker bees; food sources = colony/2
    limit: int = 10               # abandonment limit (trials) before a scout replaces a source


@dataclass
class HybridConfig:
    """Hybrid GWO-ABC settings.

    To keep the comparison fair, the hybrid splits the budget: it uses
    ``gwo.population * budget_share`` wolves and ``abc.colony_size * budget_share``
    bees, so its fitness evaluations per iteration match standalone GWO / ABC.
    """

    budget_share: float = 0.5
    transfer_size: int = 3        # elite wolves (alpha, beta, delta) pushed to ABC every iteration
    feedback: bool = True         # ABC best is injected back into the wolf pack


@dataclass
class DEAIPSOConfig:
    """Base paper's DEAI-PSO (Haris & Nam, IEEE Access 2025). Values marked * are not given in the paper."""

    particles: int = 36           # N_p, Table 3
    iterations: int = 0           # 0 -> matched to the shared evaluation budget (opt_iterations x gwo.population)
    a: float = 0.5                # * weight of the energy term in Eq. 12 (tuned on development seeds)
    cp_i: float = 2.5             # * personal coefficient, initial -> final (Eq. 10; standard TVAC values)
    cp_f: float = 0.5
    cg_i: float = 0.5             # * global coefficient, initial -> final (Eq. 11)
    cg_f: float = 2.5
    vmax_frac: float = 0.2        # * velocity clamp as a fraction of the field size (standard PSO practice)
    normalise_distance: bool = True   # * d(X, Pbest) in Eq. 13 scaled to [0, 1] (units not given in the paper)


@dataclass
class SimulationConfig:
    # --- network ---
    n_nodes: int = 100
    area_width: float = 100.0
    area_height: float = 100.0
    initial_energy: float = 0.5   # J per node
    bs_x: float = 50.0
    bs_y: float = 50.0
    # --- traffic ---
    packet_bits: int = 4000
    control_bits: int = 0         # control-packet size; 0 disables control overhead
    rounds: int = 2000
    ch_percentage: float = 0.05   # target CH fraction p (LEACH p, optimiser target)
    count_tolerance: float = 0.5  # optimisers may use k_opt*(1 +/- tol) CHs
    ch_energy_threshold: float = 1.0  # optimiser CH candidates need E >= thr * mean alive E (LEACH-C rule); 0 = off
    free_node_radius: float = 0.0     # base paper's free nodes: alive nodes closer than this to the BS send
                                      # directly and are not clustered (centralised algorithms only); 0 = off
    # --- optimisation ---
    opt_iterations: int = 30
    gwo: GWOConfig = field(default_factory=GWOConfig)
    abc: ABCConfig = field(default_factory=ABCConfig)
    hybrid: HybridConfig = field(default_factory=HybridConfig)
    deai_pso: DEAIPSOConfig = field(default_factory=DEAIPSOConfig)
    weights: FitnessWeights = field(default_factory=FitnessWeights)
    energy: EnergyConfig = field(default_factory=EnergyConfig)
    invalid_penalty: float = 10.0
    # --- reporting ---
    checkpoint_round: int = 500   # round at which residual/consumed energy are compared
    seed: int = 42

    # ------------------------------------------------------------------ helpers
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SimulationConfig":
        return _build(cls, data)

    def save(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "SimulationConfig":
        return cls.from_dict(json.loads(Path(path).read_text()))

    def replace(self, **changes: Any) -> "SimulationConfig":
        """Return a copy with (possibly dotted) fields changed, e.g. ``{"gwo.population": 30}``."""
        data = self.to_dict()
        for key, value in changes.items():
            target = data
            parts = key.split(".")
            for part in parts[:-1]:
                target = target[part]
            if parts[-1] not in target:
                raise KeyError(f"Unknown config field: {key}")
            target[parts[-1]] = value
        return SimulationConfig.from_dict(data)

    def validate(self) -> None:
        checks = [
            (self.n_nodes >= 2, "n_nodes must be >= 2"),
            (self.area_width > 0 and self.area_height > 0, "area must be positive"),
            (self.initial_energy > 0, "initial_energy must be > 0"),
            (self.packet_bits > 0, "packet_bits must be > 0"),
            (self.control_bits >= 0, "control_bits must be >= 0"),
            (self.rounds >= 1, "rounds must be >= 1"),
            (0 < self.ch_percentage < 1, "ch_percentage must be in (0, 1)"),
            (0 <= self.ch_energy_threshold <= 1, "ch_energy_threshold must be in [0, 1]"),
            (self.free_node_radius >= 0, "free_node_radius must be >= 0"),
            (self.deai_pso.particles >= 2, "DEAI-PSO needs >= 2 particles"),
            (0 <= self.deai_pso.a <= 1, "DEAI-PSO weight a must be in [0, 1]"),
            (self.opt_iterations >= 1, "opt_iterations must be >= 1"),
            (self.gwo.population >= 3, "GWO population must be >= 3 (alpha, beta, delta)"),
            (self.abc.colony_size >= 4, "ABC colony_size must be >= 4"),
            (self.abc.limit >= 1, "ABC limit must be >= 1"),
            (0 < self.hybrid.budget_share <= 1, "hybrid budget_share must be in (0, 1]"),
        ]
        errors = [msg for ok, msg in checks if not ok]
        if errors:
            raise ValueError("; ".join(errors))


def _build(cls, data: Dict[str, Any]):
    kwargs = {}
    for f in fields(cls):
        if f.name not in data:
            continue
        value = data[f.name]
        default = f.default_factory() if callable(f.default_factory) else None  # type: ignore[misc]
        if default is not None and is_dataclass(default) and isinstance(value, dict):
            value = _build(type(default), value)
        kwargs[f.name] = value
    return cls(**kwargs)


DEFAULT_CONFIG = SimulationConfig()
