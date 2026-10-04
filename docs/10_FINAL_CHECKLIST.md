# 10. Final checklist

Every item was verified on 2026-10-04 on the project laptop (Windows 11, Python 3.12.10, NumPy 2.5.3, pandas 3.0.6,
Matplotlib 3.11.2, SciPy 1.18.1, pytest 9.1.1). "Evidence" tells you where to look or what to run to see it yourself.

| # | Item | Status | Evidence |
|---|---|:-:|---|
| 1 | Project implemented | ✅ | `main.py` + `models/`, `simulation/`, `algorithms/`, `evaluation/`, `visualization/`, `gui/`, `experiments/` |
| 2 | MATLAB removed from execution requirements | ✅ | no `.m`/`.mat` files; `requirements.txt` lists only Python packages; MATLAB appears only in text about the base paper's own tool |
| 3 | Python environment ready | ✅ | `requirements.txt`; one-click `install.bat` (finds/installs Python, creates `.venv`, installs libraries, runs the tests — verified: 158 s, tests passed) and `run.bat` menu; manual steps in [01_INSTALL_AND_RUN.md](01_INSTALL_AND_RUN.md) |
| 4 | WSN simulation working | ✅ | `python main.py simulate` (≈ 35 s) → `results/single_Hybrid_GWO-ABC/report.md`; GUI `python main.py` |
| 5 | GWO implemented | ✅ | `algorithms/gwo.py` (α/β/δ, a: 2 → 0, A, C, sigmoid, repair); tests `test_gwo_*`, `test_gwo_step_matches_worked_example` |
| 6 | ABC implemented | ✅ | `algorithms/abc.py` (employed, onlooker, scout, neighbour moves); tests `test_abc_*` |
| 7 | Hybrid GWO-ABC implemented (genuine two-way combination) | ✅ | `algorithms/hybrid_gwo_abc.py`; tests `test_hybrid_exchanges_information`, `test_hybrid_feedback_reaches_gwo`, `test_hybrid_budget_matches_standalone`; real trace in [04_ALGORITHMS.md §5.4](04_ALGORITHMS.md#54-a-real-trace-not-an-illustration) |
| 8 | Fitness function implemented | ✅ | `algorithms/fitness.py`; worked example reproduced by `test_fitness_worked_example` |
| 9 | Energy model implemented | ✅ | `models/energy_model.py`; `test_round_energy_accounting_exact`, `test_radio_model_examples` |
| 10 | Cluster-head selection implemented | ✅ | Random, LEACH, GWO, ABC, Hybrid, DEAI-PSO (`algorithms/`); every CH of every round in `ch_log_run0.csv` |
| 11 | Simulation rounds implemented | ✅ | `simulation/simulator.py` (`Simulator.step`): select CHs → clusters → transmit → energy → death → record |
| 12 | Node death implemented | ✅ | `Network.detect_dead`; tests `test_node_death`, `test_dead_nodes_never_participate` |
| 13 | Metrics calculated | ✅ | `evaluation/metrics.py`: FND, HND, LND, node-rounds, residual/consumed energy, throughput, PDR, distances, imbalance, fitness, runtime, evaluations |
| 14 | CSV results generated | ✅ | every experiment folder: `runs_raw.csv`, `history_raw.csv.gz`, `round_means.csv`, `statistics.csv`, `improvement_vs_baselines.csv`, `result_table.csv`, `ch_log_run0.csv` |
| 15 | Graphs generated | ✅ | `01_topology.png` … `20_final_fitness.png` per experiment; convergence, sensitivity, runtime and base-paper figures; 12 explanatory diagrams in `docs/figures/` |
| 16 | Algorithms compared fairly | ✅ | paired seeds, same radio model and budget; Wilcoxon + Holm + Cliff's δ; `results/scenarios/S1_100nodes/result_table.md`, `results/base_paper/README.md` |
| 17 | Results explained | ✅ | [05_RESULTS_AND_GRAPHS.md](05_RESULTS_AND_GRAPHS.md) (16 graphs, 7 questions each); automatic `report.md` in every folder |
| 18 | Improvement over the base paper justified | ✅ | `results/base_paper/README.md`: 18 of 24 tests significantly better, 1 worse, 5 equal; fairness protocol and attribution |
| 19 | Reproducibility verified | ✅ | S1 re-run reproduced 80/80 earlier runs bit-for-bit; `reproducibility_check_run0.csv` all `True`; `python main.py reproduce <folder>` |
| 20 | Automatic tests pass | ✅ | `python -m pytest` → 93 passed (≈ 15 s) |
| 21 | MATLAB-to-Python justification completed | ✅ | [06_MATLAB_TO_PYTHON.md](06_MATLAB_TO_PYTHON.md) |
| 22 | Beginner guide completed | ✅ | [00_START_HERE.md](00_START_HERE.md), [02_CONCEPTS.md](02_CONCEPTS.md) |
| 23 | Mathematics explained with worked examples that match the code | ✅ | [03_MATHEMATICS.md](03_MATHEMATICS.md); `tests/test_docs_examples.py` |
| 24 | Visual explanations completed | ✅ | `docs/figures/fig01…fig12` (`python main.py diagrams`), ASCII diagrams in every document |
| 25 | Run guide completed ("What happens when I run the program?", "What is the final output?") | ✅ | [01_INSTALL_AND_RUN.md](01_INSTALL_AND_RUN.md) |
| 26 | Troubleshooting completed | ✅ | [07_TROUBLESHOOTING.md](07_TROUBLESHOOTING.md) |
| 27 | Study guide completed ("If I know nothing…", 23 steps) | ✅ | [08_STUDY_GUIDE.md](08_STUDY_GUIDE.md) |
| 28 | Presentation explanation completed (30–60 s + technical) | ✅ | [09_PRESENTATION_AND_VIVA.md §1–4](09_PRESENTATION_AND_VIVA.md#1-the-3060-second-explanation-memorise-this) |
| 29 | Viva preparation completed (basic, intermediate, difficult, validity challenges) | ✅ | [09_PRESENTATION_AND_VIVA.md §5–8](09_PRESENTATION_AND_VIVA.md#5-basic-questions) |
| 30 | Final conclusion completed | ✅ | [09_PRESENTATION_AND_VIVA.md §9](09_PRESENTATION_AND_VIVA.md#9-final-conclusion), [05_RESULTS_AND_GRAPHS.md §5.9](05_RESULTS_AND_GRAPHS.md#59-conclusions-in-plain-words) |

## What was **not** done (stated openly)

* No real hardware test-bed and no packet-level network simulator (ns-3/OMNeT++): the study uses the standard
  round-based first-order radio model with an ideal channel.
* The base paper's other baselines (LEACH-FL, LEACH-FC, KM-PSO) were not re-implemented; its published lifetimes
  cannot be reproduced (they exceed the physical bound of its own parameters).
* The proposed method is not better than GWO or ABC in network lifetime in the BS-centre scenarios, and not better
  than DEAI-PSO in first node death — both are reported as measured.
