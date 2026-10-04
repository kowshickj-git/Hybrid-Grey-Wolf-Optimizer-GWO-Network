# 6. From MATLAB to Python — what changed and what did not

## 6.1 The statement to use in your report

> The project was originally planned as a MATLAB implementation. The final implementation was developed in
> Python 3 (NumPy, SciPy, pandas, Matplotlib, Tkinter). Only the implementation environment changed: the wireless
> sensor network model, the first-order radio energy model and its parameters, the cluster formation procedure,
> the LEACH, GWO, ABC and Hybrid GWO-ABC algorithms, the fitness function, the round-based simulation, the
> performance metrics and the research objective are the same as planned. Because random-number generators and
> numerical libraries differ between environments, a MATLAB implementation of the same model would not produce
> bit-identical numbers; the conclusions are therefore drawn from many paired simulation runs and statistical
> tests rather than from single values, and every Python result can be reproduced exactly from the saved
> configuration and random seeds.

MATLAB is **not** needed anywhere: installing, testing, simulating, plotting and producing the final results use
only Python and the free libraries listed in `requirements.txt`.

## 6.2 What stayed the same

| Part of the project | Planned (MATLAB) | Implemented (Python) | Same? |
|---|---|---|:-:|
| Research objective | energy-efficient CH selection with a hybrid GWO-ABC | the same | ✅ |
| Network model | N nodes randomly deployed, one BS, batteries, rounds | the same (`models/`) | ✅ |
| Energy model | first-order radio model (E_elec, ε_fs, ε_mp, E_DA, d0) | the same equations and values (`models/energy_model.py`) | ✅ |
| Clustering | members join the nearest CH, CH aggregates and forwards to the BS | the same (`simulation/`) | ✅ |
| Algorithms | LEACH, GWO, ABC, Hybrid GWO-ABC | the same, plus Random and the base paper's DEAI-PSO (`algorithms/`) | ✅ |
| Fitness function | energy, distance, balance factors | the same factors, documented weights (`algorithms/fitness.py`) | ✅ |
| Metrics | FND, HND, LND, residual energy, throughput, PDR … | the same (`evaluation/metrics.py`) | ✅ |
| Outputs | tables and graphs | CSV tables, PNG graphs, automatic reports | ✅ |

## 6.3 What changed

* **The language and its libraries:** NumPy arrays instead of MATLAB matrices, Matplotlib instead of MATLAB
  plotting, SciPy instead of the Statistics Toolbox, CSV/JSON files instead of `.mat` files, a Tkinter window
  instead of App Designer.
* **Additions that make the work verifiable** (they do not change the model): automatic tests (`tests/`), fixed
  random seeds and saved configurations for exact reproduction, paired multi-run statistics, automatically
  generated reports.

## 6.4 Why Python

1. **No licence is needed.** MATLAB and its toolboxes require a paid licence; Python and all libraries used here are
   free and open source, so anyone — including the examiner — can install and run the project on any computer.
2. **Transparency and reproducibility.** The complete source code, the exact library versions
   (`requirements.txt`), the configuration (`config.json`) and the random seeds of every experiment are saved;
   `python main.py reproduce <folder>` regenerates a result.
3. **The scientific tools are equivalent.** NumPy provides MATLAB-style vectorised arrays, SciPy provides the
   statistical tests, Matplotlib provides MATLAB-like plotting, and pandas handles result tables.
4. **One automated pipeline.** Simulation → statistics → graphs → written report runs from a single command, and
   many simulations run in parallel on all processor cores (MATLAB would need the Parallel Computing Toolbox).
5. **Widely used in research and industry** (IoT, data science, machine learning), so the skills and the code are
   reusable.

If in your case MATLAB was simply not available (licence, computer), say so — that is a legitimate and honest
reason; the points above explain why the change does not harm the project.

## 6.5 Why the numbers would not be identical in MATLAB (be honest about this)

| Cause | Explanation |
|---|---|
| Different random-number generators | MATLAB's default generator (Mersenne Twister) and NumPy's (`default_rng`, PCG64) produce **different** random sequences for the same seed number. Different random node positions and random choices (LEACH draws, GWO's r1/r2, ABC's partners) → different individual results. |
| Floating-point details | The order of arithmetic operations and library internals differ; tiny rounding differences can move a node's death by a round. |
| Implementation details | Choices that a plan does not fix exactly (tie-breaking, the repair strategy, the exact moment death is checked) can differ between any two implementations, even in the same language. |
| Statistical routines | MATLAB's `signrank` and SciPy's `wilcoxon` can compute p-values slightly differently (exact vs approximate). |

So: **same model, same method, same metrics, statistically comparable conclusions — but not bit-identical
numbers.** Do not claim that MATLAB would give exactly the same values.

## 6.6 Why this does not weaken the results

* Conclusions rest on **20 paired runs** and **statistical tests** (Wilcoxon + Holm), not on one lucky number.
* Every number is **exactly reproducible in Python**: re-simulating run 0 from the saved settings gives identical
  values (`reproducibility_check_run0.csv`, test `test_rerun_reproduces_saved_results`).
* The equations are language-independent, written out in [03_MATHEMATICS.md](03_MATHEMATICS.md) and checked by
  tests (exact energy accounting, the base paper's Eq. 12 against a hand calculation).
* The **base paper itself used MATLAB R2023a** (Haris & Nam 2025, Section IV). Its method was re-implemented in
  Python and run in the same simulator as the proposed method. Comparing two methods in one simulator under
  identical conditions is fairer than comparing with numbers produced by a different simulator, whatever the
  language.

## 6.7 MATLAB → Python dictionary (for an examiner who knows MATLAB)

| MATLAB | Python in this project |
|---|---|
| `rng(42)` | `np.random.default_rng(42)` |
| `rand(N,2)*100` | `rng.uniform([0, 0], [100, 100], size=(N, 2))` (`Network.deploy`) |
| `pdist2(P, P)` | NumPy broadcasting (`Network.distances`) |
| `for` loops over nodes | vectorised NumPy operations on all nodes at once |
| struct array of nodes | `SensorNode` objects backed by NumPy arrays (`models/node.py`, `models/network.py`) |
| `plot`, `scatter`, `bar` | Matplotlib (`visualization/`) |
| `signrank` | `scipy.stats.wilcoxon` (`evaluation/statistics.py`) |
| `save results.mat`, `writetable` | CSV and JSON files (pandas) |
| GUIDE / App Designer | Tkinter (`gui/dashboard.py`) |
| `parfor` | `concurrent.futures.ProcessPoolExecutor` (`experiments/experiment_runner.py`) |
| MATLAB Unit Test | pytest (`tests/`) |

## 6.8 One-sentence viva answer

> "Only the tool changed, not the science: the network model, energy model, algorithms, fitness function and
> metrics are the same as planned; Python is free, reproducible and has equivalent numerical libraries; exact
> numbers would differ in MATLAB because the random generators differ, which is why the conclusions are based on
> 20 paired runs and significance tests, and every Python result can be reproduced exactly."
