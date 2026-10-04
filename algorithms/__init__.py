"""Algorithm registry: ``make_algorithm(name, config, seed)`` builds a CH selector."""
from __future__ import annotations

from config import FitnessWeights, SimulationConfig

MAIN_ALGORITHMS = ["LEACH", "GWO", "ABC", "Hybrid GWO-ABC"]
BASELINES = ["Random"]
COMPARISON_ALGORITHMS = BASELINES + MAIN_ALGORITHMS    # main demonstration (scenario S1, `compare` default)
ABLATION_VARIANTS = [
    "GWO only", "ABC only", "GWO->ABC", "ABC->GWO",
    "Hybrid w/o energy", "Hybrid w/o distance", "Hybrid w/o balance", "Full Hybrid GWO-ABC",
]
BASE_PAPER = "DEAI-PSO"                       # existing system (Haris & Nam, IEEE Access 2025)
PROPOSED_EQ12 = "Hybrid GWO-ABC (Eq. 12)"     # proposed optimiser on the base paper's own problem/objective
EQ12_VARIANTS = ["GWO (Eq. 12)", "ABC (Eq. 12)", PROPOSED_EQ12, "Hybrid GWO-ABC (Eq. 12, fixed K)"]
BASE_PAPER_ALGORITHMS = ["LEACH", BASE_PAPER, "GWO (Eq. 12)", "ABC (Eq. 12)", PROPOSED_EQ12, "Hybrid GWO-ABC"]
ATTRIBUTION_VARIANTS = [BASE_PAPER, "DEAI-PSO + proposed fitness", PROPOSED_EQ12,
                        "Hybrid GWO-ABC (Eq. 12, fixed K)", "Hybrid GWO-ABC"]
ALL_ALGORITHMS = (MAIN_ALGORITHMS + BASELINES + ABLATION_VARIANTS +
                  [BASE_PAPER, "DEAI-PSO + proposed fitness"] + EQ12_VARIANTS)


def _weights_without(config: SimulationConfig, *terms: str) -> FitnessWeights:
    w = FitnessWeights(**vars(config.weights))
    for t in terms:
        setattr(w, t, 0.0)
    return w


def make_algorithm(name: str, config: SimulationConfig, seed: int | None = None):
    from algorithms.abc import make_abc
    from algorithms.base import RandomSelector
    from algorithms.gwo import make_gwo
    from algorithms.hybrid_gwo_abc import make_hybrid, make_sequential
    from algorithms.leach import LEACH

    if name == "LEACH":
        return LEACH(config, seed)
    if name == "Random":
        return RandomSelector(config, seed)
    if name in (BASE_PAPER, "DEAI-PSO + proposed fitness"):
        from algorithms.deai_pso import DEAIPSOSelector
        sel = DEAIPSOSelector(config, seed, objective="paper" if name == BASE_PAPER else "proposed")
        sel.name = name
        return sel
    if name in EQ12_VARIANTS:              # our optimisers driven by the base paper's Eq. 12 objective
        from algorithms.abc import ArtificialBeeColony
        from algorithms.deai_pso import PaperObjectiveSelector
        from algorithms.gwo import GreyWolfOptimizer
        from algorithms.hybrid_gwo_abc import HybridGWOABC
        cfg = config.replace(count_tolerance=0.0) if name.endswith("fixed K)") else config   # K = p * n exactly
        if name.startswith("GWO"):
            opt = GreyWolfOptimizer(cfg.gwo.population, cfg.opt_iterations)
        elif name.startswith("ABC"):
            opt = ArtificialBeeColony(cfg.abc.colony_size, cfg.abc.limit, cfg.opt_iterations)
        else:
            opt = HybridGWOABC.from_config(cfg)
        return PaperObjectiveSelector(cfg, opt, name, seed)
    if name in ("GWO", "GWO only"):
        sel = make_gwo(config, seed)
    elif name in ("ABC", "ABC only"):
        sel = make_abc(config, seed)
    elif name in ("Hybrid GWO-ABC", "Full Hybrid GWO-ABC"):
        sel = make_hybrid(config, seed)
    elif name == "GWO->ABC":
        sel = make_sequential(config, "gwo_abc", seed)
    elif name == "ABC->GWO":
        sel = make_sequential(config, "abc_gwo", seed)
    elif name == "Hybrid w/o energy":
        sel = make_hybrid(config, seed, _weights_without(config, "energy"))
    elif name == "Hybrid w/o distance":
        sel = make_hybrid(config, seed, _weights_without(config, "intra_distance", "ch_bs_distance"))
    elif name == "Hybrid w/o balance":
        sel = make_hybrid(config, seed, _weights_without(config, "balance"))
    else:
        raise ValueError(f"Unknown algorithm '{name}'. Choose from {ALL_ALGORITHMS}")
    sel.name = name
    return sel
