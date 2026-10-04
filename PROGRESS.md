# Project progress — Hybrid GWO-ABC CH selection for WSNs

**Overall: 48 / 48 tasks done (100 %)**  `████████████████████`
_Last updated: 2026-10-04 — project complete and published on GitHub
(<https://github.com/kowshickj-git/Hybrid-Grey-Wolf-Optimizer-GWO-Network>). Start reading at
`docs/00_START_HERE.md`; on Windows double-click `install.bat`, then `run.bat`._

Legend: ✅ done · 🔄 in progress · ⬜ to do

## Part A — Original specification (22 / 22) ✅

| # | Task | Status | Evidence |
|---|---|:-:|---|
| A1 | Network & sensor-node model | ✅ | `models/node.py`, `models/network.py` |
| A2 | First-order radio energy model | ✅ | `models/energy_model.py` |
| A3 | Communication model (member → CH → BS) | ✅ | `simulation/transmission.py` |
| A4 | LEACH | ✅ | `algorithms/leach.py` |
| A5 | GWO (alpha/beta/delta, binary) | ✅ | `algorithms/gwo.py` |
| A6 | ABC (employed / onlooker / scout) | ✅ | `algorithms/abc.py` |
| A7 | Hybrid GWO-ABC (two-way exchange) | ✅ | `algorithms/hybrid_gwo_abc.py` |
| A8 | Multi-objective fitness function | ✅ | `algorithms/fitness.py` |
| A9 | Cluster formation + CH records (ids, energy, coordinates, BS distance) | ✅ | `simulation/clustering.py`, `ch_log_run0.csv` |
| A10 | Multi-round simulation & node death | ✅ | `simulation/simulator.py` |
| A11 | Performance metrics (FND/HND/LND, energy, throughput, PDR, …) | ✅ | `evaluation/metrics.py` |
| A12 | Visualisation (18+ figure types) | ✅ | `visualization/` |
| A13 | GUI dashboard (Run/Pause/Stop/Reset/Export) | ✅ | `gui/dashboard.py` |
| A14 | Comparison, statistics (Wilcoxon, Cliff's δ), auto-interpretation | ✅ | `evaluation/` |
| A15 | Scenarios S1–S5 (100/200/300 nodes, 3 BS positions) | ✅ | `results/scenarios/` |
| A16 | Ablation study (8 variants) | ✅ | `results/ablation/` |
| A17 | Sensitivity analysis (10 factors, 590 simulations) | ✅ | `results/sensitivity/` |
| A18 | Convergence analysis | ✅ | `results/convergence/` |
| A19 | Clean runtime benchmark | ✅ | `results/runtime_benchmark/` |
| A20 | Reproducibility check (run 0 re-simulated → identical) | ✅ | `reproducibility_check_run0.csv` |
| A21 | Automated tests | ✅ | `python -m pytest` |
| A22 | README results: sensitivity (§8.6) and runtime (§8.7) | ✅ | `README.md` §8.6–8.7 |

## Part B — Base paper: improve on the existing system (8 / 8) ✅

Base paper: M. Haris, H. Nam, *"Enhancing Energy Efficiency in IoT-WSNs Through Optimized PSO Cluster Head
Selection"*, IEEE Access, vol. 13, 2025, DOI 10.1109/ACCESS.2025.3583922 (DEAI-PSO).

| # | Task | Status | Notes |
|---|---|:-:|---|
| B1 | Read the base paper, extract its method and parameters (Table 3) | ✅ | 0.5 J, 4000/200-bit packets, BS (200, 50), 10 % CHs, 36 particles, MATLAB R2023a |
| B2 | Implement DEAI-PSO (Eqs. 8–13) as the existing-system baseline | ✅ | `algorithms/deai_pso.py` |
| B3 | Base-paper fitness (Eq. 12), free nodes near the BS, 200-bit control packets | ✅ | `PaperFitness`, `free_node_radius`, `control_bits` |
| B4 | Tests for the base-paper method | ✅ | `tests/test_base_paper.py` (Eq. 12 checked against a hand calculation) |
| B5 | Development pilot on separate seeds (baseline tuned in its own favour) | ✅ | a = 0.8, d in metres (`results/base_paper/dev_pilot/`) |
| B6 | Final comparison on the 3 scenarios (held-out seeds, 20 runs) + attribution + runtime | ✅ | `results/base_paper/BP1…BP3`, `attribution_BP1`, `runtime` |
| B7 | "Improvement over the base paper" report with statistics and justification | ✅ | `results/base_paper/README.md` (generated from the data, reviewed) |
| B8 | README §9 + GUI (DEAI-PSO selectable, base-paper presets) | ✅ | `README.md` §9, `gui/dashboard.py` |

### Final result vs the base paper (20 held-out paired runs per scenario)

Proposed Hybrid GWO-ABC on the base paper's own objective (Eq. 12) vs DEAI-PSO: **significantly better in 18 of 24**
scenario × metric comparisons, significantly worse in 1, no significant difference in 5.

| Scenario | HND | LND | Node-rounds | Throughput | Energy left @ round 300 | FND |
|---|---:|---:|---:|---:|---:|---:|
| BP1 (100 nodes) | +6.90 %* | +7.09 %* | +6.72 %* | +6.74 %* | +5.11 %* | +0.51 % (n.s.) |
| BP2 (160 nodes) | +7.39 %* | +3.27 %* | +7.02 %* | +7.22 %* | +5.49 %* | +1.53 % (n.s.) |
| BP3 (200 nodes) | +2.98 %* | 0.00 % (identical) | +2.08 %* | +2.17 %* | +1.26 %* | **−1.16 %*** |

`*` significant (Wilcoxon, Holm-corrected). Most of the gain comes from using fewer, better CHs (≈ 5 instead of 10 in
BP1); with the CH count fixed at 10 % the hybrid still wins, but only by ≈ 0.4 %.

## Part C — Beginner documentation and final polish (16 / 16) ✅

| # | Task | Status | Evidence |
|---|---|:-:|---|
| C1 | Start page and reading order | ✅ | `docs/00_START_HERE.md` |
| C2 | Install & run guide (Windows, VS Code, venv), "What happens when I run the program?", "What is the final output?" | ✅ | `docs/01_INSTALL_AND_RUN.md` |
| C3 | Every concept explained (what / why / how / inside the program / analogy / project) | ✅ | `docs/02_CONCEPTS.md` |
| C4 | Every equation with variables, purpose, worked example and code location | ✅ | `docs/03_MATHEMATICS.md`, `tests/test_docs_examples.py` |
| C5 | GWO, ABC, Hybrid and DEAI-PSO from zero, incl. a real hybrid trace | ✅ | `docs/04_ALGORITHMS.md` |
| C6 | 12 explanatory diagrams (architecture, flowchart, energy, fitness, GWO, ABC, hybrid, …) | ✅ | `docs/figures/`, `python main.py diagrams` |
| C7 | MATLAB → Python justification | ✅ | `docs/06_MATLAB_TO_PYTHON.md` |
| C8 | Troubleshooting (Problem → Reason → Solution) | ✅ | `docs/07_TROUBLESHOOTING.md` |
| C9 | Study guide "If I know nothing…" (23 steps) | ✅ | `docs/08_STUDY_GUIDE.md` |
| C10 | Random baseline in the main comparison (scenario S1 re-run; the other 80 runs reproduced bit-for-bit) | ✅ | `results/scenarios/S1_100nodes/` |
| C11 | Results and every important graph explained in plain words | ✅ | `docs/05_RESULTS_AND_GRAPHS.md` |
| C12 | 30–60 s explanation, technical explanation, viva Q&A | ✅ | `docs/09_PRESENTATION_AND_VIVA.md` |
| C13 | Final checklist with evidence | ✅ | `docs/10_FINAL_CHECKLIST.md` |
| C14 | Safety/usability: quick test writes to `results_quick/`, `scenarios --only`, `diagrams` command | ✅ | `main.py`, `experiments/experiment_runner.py` |
| C15 | Published on GitHub (all 709 files, verified) | ✅ | <https://github.com/kowshickj-git/Hybrid-Grey-Wolf-Optimizer-GWO-Network> |
| C16 | One-click Windows installer and run menu (tested: install 158 s, all tests passed) | ✅ | `install.bat`, `run.bat` |

## Final

| # | Task | Status |
|---|---|:-:|
| F1 | Full test run + final review (93 tests pass; all doc links and cited tests verified) | ✅ |
| F2 | Final summary of results | ✅ |

### Ground rules kept throughout
* Every number comes from the simulator; nothing is hard-coded or edited.
* The base paper's method is re-implemented faithfully and compared under **identical** conditions (same networks,
  seeds, radio model, packet sizes, BS position, CH ratio and fitness-evaluation budget).
* Settings the base paper leaves open were tuned **in its favour**; the proposed method was not tuned.
* Improvements are claimed only where the paired statistics show them; any metric where the proposed system is
  not better is reported as such.
