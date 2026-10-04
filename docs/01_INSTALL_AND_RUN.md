# 1. Install, run and understand the outputs (Windows + VS Code)

This guide assumes Windows 10/11 and (optionally) Visual Studio Code. Every command is written so that you can copy
it exactly. Commands are typed in a **terminal** (PowerShell) that is open **in the project folder**
`Hybrid-GWO-ABC-WSN`.

> Times below were measured on the laptop used to build the project (12 logical CPU cores). A slower computer
> takes longer, but produces exactly the same numbers (see "Re-running" below).

---

## The fastest way: one-click installer (`install.bat` + `run.bat`)

1. **Get the project.** On <https://github.com/kowshickj-git/Hybrid-Grey-Wolf-Optimizer-GWO-Network> click the green
   **Code** button → **Download ZIP**. Right-click the downloaded ZIP → **Extract All…** → **Extract**.
   (With Git: `git clone https://github.com/kowshickj-git/Hybrid-Grey-Wolf-Optimizer-GWO-Network.git`.)
2. **Install.** Open the extracted folder and double-click **`install.bat`**. If Windows shows *"Windows protected
   your PC"*, click **More info → Run anyway** (the file comes from the internet, so Windows asks once).
   The installer:
   * looks for Python 3.10 or newer — if there is none, it offers to install Python 3.12 for you (via winget);
   * creates a private environment in the folder `.venv` (other Python projects are not affected);
   * installs NumPy, pandas, Matplotlib, SciPy and pytest (about 100 MB, a few minutes the first time);
   * runs the 93 automatic tests and shows `Automatic tests: passed`.
3. **Run.** Double-click **`run.bat`** and type a number:

```text
   1  Open the simulator window - GUI
   2  One simulation of the proposed Hybrid GWO-ABC      ~35 s
   3  Compare Random, LEACH, GWO, ABC and Hybrid on 3 networks   ~2 min
   4  Run the automatic tests                           ~15 s
   5  Main comparison, scenario S1, 20 networks        ~12 min
   6  Comparison with the base paper                 ~1 h 20 min
   7  Redraw the documentation diagrams                 ~10 s
   8  Open the beginner guide in the web browser
   9  Open the results folder
   0  Exit
```

Options 5 and 6 ask before they replace the saved results. `run.bat 4` (with a number) starts that option
directly. The rest of this guide explains the same things step by step, for when you want to do them by hand or
something goes wrong.

---

## Step 1 — Install Python

1. Open <https://www.python.org/downloads/> and download **Python 3.12** for Windows (any version **3.10 or newer**
   works; the project was built and tested with Python 3.12.10).
2. Run the installer. On the first screen **tick "Add python.exe to PATH"**, then click **Install Now**.
   (The standard installer also installs `pip` and Tkinter, which the window/GUI needs.)
3. Open a new terminal (Start menu → type `PowerShell` → Enter) and check:

```powershell
python --version
python -m pip --version
```

You should see `Python 3.12.x` and a pip version. If you see *"'python' is not recognized"* or the Microsoft Store
opens, see [07_TROUBLESHOOTING.md](07_TROUBLESHOOTING.md#t1).

## Step 2 — Open the project in VS Code

1. Install VS Code from <https://code.visualstudio.com/> (optional but recommended).
2. Start VS Code → **File → Open Folder…** → select the folder `Hybrid-GWO-ABC-WSN` → *Yes, I trust the authors*.
3. Install the **Python** extension (Extensions icon on the left → search "Python" → the one by Microsoft →
   Install).
4. Open a terminal inside VS Code: **Terminal → New Terminal** (or press <kbd>Ctrl</kbd>+<kbd>`</kbd>). The terminal
   opens in the project folder. Check with:

```powershell
dir main.py
```

If the file is listed, you are in the right folder. Without VS Code: open the folder in File Explorer, click the
address bar, type `powershell` and press Enter.

## Step 3 — (Recommended) create a virtual environment

A virtual environment is a private copy of Python for this project, so the libraries it installs cannot clash with
other projects. It is optional: the project also works with the normal Python installation.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

The prompt now starts with `(.venv)`. If PowerShell says *"running scripts is disabled on this system"*, run this
once and answer `Y`, then activate again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

In VS Code also choose this environment: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → **Python: Select
Interpreter** → pick the one that shows `.venv`. Next time you open a terminal in VS Code it is activated
automatically. (You must activate the environment every time you open a new terminal outside VS Code.)

## Step 4 — Install the libraries

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs NumPy (fast arrays), pandas (tables/CSV), Matplotlib (graphs), SciPy (the Wilcoxon statistical test)
and pytest (automatic tests). Check:

```powershell
python -c "import numpy, pandas, matplotlib, scipy, tkinter; print('All libraries OK')"
```

## Step 5 — Quick checks (about 3 minutes)

**a) Automatic tests** — prove that every part works (energy model, clustering, algorithms, metrics, reports,
reproducibility):

```powershell
python -m pytest
```

Expected (about 15 seconds): a row of dots, one per test — 93 tests — and no `F` (failure) or `E` (error).
Add `-v` (`python -m pytest -v`) to see the name of every test with `PASSED` next to it.

**b) Your first simulation** — one network, the proposed Hybrid GWO-ABC, all graphs (about 35 seconds):

```powershell
python main.py simulate
```

At the end the terminal prints a result table and the path of the report:
`results\single_Hybrid_GWO-ABC\report.md`. Open that folder to see the graphs.

**c) Smoke test of every experiment** (about 1.5 minutes) — tiny sizes, only to check that the whole pipeline
runs. It writes to a separate folder `results_quick\`, so it never overwrites the real results:

```powershell
python main.py all --quick
```

## Step 6 — Use the window (GUI)

```powershell
python main.py
```

The window runs exactly the loop shown below, one round at a time, and draws every round:

![What the program does every round](figures/fig02_simulation_flowchart.png)

What to do in the window:

1. **Scenario preset** (top left): keep *Project default (BS at centre)*, or choose one of the base paper's three
   scenarios.
2. **Configuration**: number of nodes, field size, initial energy, packet size, rounds, CH percentage, BS position,
   GWO population, ABC colony size, optimisation iterations, random seed. Change a value and press **Reset** to
   create the new network.
3. **Algorithm**: choose *Hybrid GWO-ABC* (proposed), *GWO*, *ABC*, *LEACH*, *Random*, *DEAI-PSO (base paper)* or
   *Hybrid GWO-ABC on base-paper objective*.
4. Press **Run**. The *Network* tab shows the field live: blue dots = sensor nodes (lighter = less energy), orange
   triangles = cluster heads, grey lines = cluster membership, red crosses = dead nodes, black square = base
   station. The dashboard on top shows the round, alive/dead nodes, residual and consumed energy, CH count,
   packets and PDR, and the current fitness.
5. **Pause / Resume**, **Stop** (ends the run early) and **Reset** (new network, same settings) work at any time.
6. The *Performance* tab draws alive nodes, residual energy, PDR and CH count against rounds; the *Convergence*
   tab shows how the optimiser improved the fitness inside the latest round.
7. The *Compare all* tab runs every algorithm on the **same** network and fills a table with FND, HND, LND,
   residual energy, throughput, PDR, runtime and fitness (this takes a few minutes; the window stays usable).
8. **Export Results** saves everything to `results\gui_exports\<date_time>\` (configuration, per-round history,
   summary, final node table, cluster-head log, the pictures).

## Step 7 — Produce the main evidence

**Main comparison (scenario S1, about 12 minutes):** 100 nodes, 100 m × 100 m, BS at the centre; Random, LEACH,
GWO, ABC and the Hybrid GWO-ABC on the same 20 networks:

```powershell
python main.py scenarios --only S1_100nodes
```

**Everything for the original project (about 4 hours):** five scenarios (100/200/300 nodes, three BS positions),
ablation study, sensitivity analysis, convergence analysis and a clean runtime benchmark:

```powershell
python main.py all
```

**Comparison with the base paper (about 1 h 20 min):** DEAI-PSO (Haris & Nam, IEEE Access 2025) re-implemented and
compared with the proposed method under the paper's own conditions:

```powershell
python main.py basepaper
```

Long runs use all processor cores but one and stop the laptop from going to sleep while they run. Keep the laptop
plugged in. The results of every run are already saved in `results\`, so you only need to re-run if you want to
reproduce them or change something.

## Step 8 — Find and open the results

```text
results/
├── scenarios/S1_100nodes/        ← MAIN comparison (show this first)
├── scenarios/S2…S5/              ← 200 and 300 nodes, BS on the edge, BS outside the field
├── scenarios/README.md           ← one-page overview of all scenarios
├── ablation/                     ← which part of the hybrid matters
├── sensitivity/                  ← what happens when one parameter changes
├── convergence/                  ← how fast each optimiser improves the fitness
├── runtime_benchmark/            ← computation time per round
└── base_paper/                   ← comparison with the base paper (README.md = the justification report)
```

* Open any `report.md` in VS Code and press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd> to see it formatted
  with its graphs.
* Click a `.png` file to view a graph.
* Open a `.csv` file with Excel (double-click in File Explorer) or in VS Code.

## Step 9 — Change parameters

Every parameter has a default in [config.py](../config.py). Change one or more for a single command with
`--set name=value` (no spaces around `=`; nested names use a dot):

```powershell
python main.py simulate --set n_nodes=200
python main.py simulate -a "GWO" --set initial_energy=1.0 --set rounds=3000
python main.py compare --runs 5 --set bs_y=175
python main.py compare --runs 5 --set gwo.population=30 --set abc.colony_size=30 --set opt_iterations=50
python main.py compare --runs 5 --set weights.energy=0.5 --set weights.balance=0.05
```

| Parameter (`--set` name) | Default | Meaning |
|---|---|---|
| `n_nodes` | 100 | number of sensor nodes |
| `area_width`, `area_height` | 100, 100 | field size in metres |
| `initial_energy` | 0.5 | battery of each node at the start (J) |
| `bs_x`, `bs_y` | 50, 50 | base-station position (m); can be outside the field |
| `packet_bits` | 4000 | size of one data packet |
| `control_bits` | 0 | size of control packets (0 = no control overhead) |
| `rounds` | 2000 | maximum number of rounds |
| `ch_percentage` | 0.05 | target share of cluster heads (5 %) |
| `count_tolerance` | 0.5 | optimisers may use between 50 % and 150 % of the target CH count |
| `ch_energy_threshold` | 1.0 | a CH candidate needs energy ≥ 1.0 × average alive energy (0 switches the rule off) |
| `opt_iterations` | 30 | GWO/ABC/hybrid iterations per round |
| `gwo.population` | 20 | number of wolves |
| `abc.colony_size`, `abc.limit` | 20, 10 | bees (10 food sources) and abandonment limit |
| `hybrid.budget_share` | 0.5 | the hybrid uses half the wolves and half the bees (fair budget) |
| `weights.energy` … `weights.ch_count` | 0.30, 0.25, 0.20, 0.15, 0.10 | fitness weights w1…w5 |
| `checkpoint_round` | 500 | round at which residual/consumed energy are compared |
| `seed` | 42 | random seed: same seed → same network and same results |

In the GUI simply type new values in the *Configuration* panel and press **Reset**. Invalid values (for example
`ch_percentage=1.5`) are rejected with a clear message.

## Step 10 — Re-run and reproduce

* The same command with the same parameters and seed gives **exactly** the same numbers on any computer with the
  same library versions (random numbers come from fixed seeds: run *r* uses seed 42 + *r*).
* Re-run a saved experiment from its stored settings:

```powershell
python main.py reproduce results\scenarios\S1_100nodes
```

  It writes a new folder `results\scenarios\S1_100nodes_reproduced\`; compare its `result_table.md` with the
  original — lifetime, energy and packet numbers are identical (only the measured run times differ slightly).
* Change the seed to get different random networks: `--set seed=7`.

---

## WHAT HAPPENS WHEN I RUN THE PROGRAM?

Below is the complete chain for `python main.py compare` (or `scenarios`). The GUI follows the same chain for one
network and one algorithm, and draws every round on the screen.

```text
 Run program  (python main.py compare)
      │
      ▼
 Read the parameters ............ config.py (defaults) + --set changes, then validate()
      │
      ▼
 Plan the experiment ............ every algorithm × every run; run r uses seed 42 + r (paired runs)
      │
      ▼  (for each algorithm and each run, several in parallel)
 Create sensor nodes ............ models/network.py: Network.deploy()
 Place nodes in the field ....... random (x, y), BS position, all distances computed once
 Initialise battery energy ...... every node E0 = 0.5 J, status ALIVE
      │
      ▼  ┌──────────────── one ROUND (simulation/simulator.py: Simulator.step) ───────────────┐
      │  │ Select cluster heads ..... the chosen algorithm (algorithms/*.py)                  │
      │  │ Create clusters .......... each alive node joins its nearest CH (clustering.py)    │
      │  │ Transmit data ............ member → CH → BS (transmission.py)                      │
      │  │ Calculate energy use ..... radio model: send / receive / aggregate                 │
      │  │ Update node energy ....... subtract the cost from every node's battery             │
      │  │ Check dead nodes ......... energy = 0 J → DEAD (never used again)                  │
      │  │ Record the round ......... alive, dead, energy, packets, CHs, fitness, time        │
      │  └───────────── repeat until every node is dead or the round limit is reached ───────┘
      ▼
 Calculate performance metrics .. evaluation/metrics.py: FND, HND, LND, energy, throughput, PDR …
      │
      ▼
 Compare algorithms ............. mean ± std, Wilcoxon test, Holm correction, Cliff's δ
      │
      ▼
 Save CSV results ............... runs_raw.csv, history_raw.csv.gz, statistics.csv, …
      │
      ▼
 Generate graphs ................ 01_topology.png … 20_final_fitness.png
      │
      ▼
 Write report.md + show table ... the final comparison table is printed in the terminal
```

What each stage means, in plain words:

1. **Run program.** `main.py` reads which command you typed (`simulate`, `compare`, …).
2. **Read the parameters.** All settings come from `config.py`; anything you passed with `--set` replaces the
   default. `validate()` stops the program early with a clear message if a value is impossible.
3. **Plan the experiment.** The program makes a list of jobs, e.g. 5 algorithms × 20 runs = 100 simulations. Run
   number *r* of **every** algorithm uses the same seed, so all algorithms are tested on the same 20 networks
   (a fair, "paired" comparison).
4. **Create sensor nodes / place them.** For each job the program draws N random positions inside the field
   (uniform distribution, fixed seed), places the base station and calculates every node-to-node and node-to-BS
   distance once.
5. **Initialise battery energy.** Every node receives the same initial energy (0.5 J) and is marked ALIVE.
6. **Select cluster heads.** The algorithm under test picks this round's CHs. LEACH and Random use random numbers;
   GWO, ABC and the hybrid run 30 iterations of their search and return the CH set with the lowest fitness.
7. **Create clusters.** Every alive node that is not a CH joins the nearest CH.
8. **Transmit data.** Every alive node produces one 4000-bit reading. Members send it to their CH; the CH receives
   all of them, combines (aggregates) them with its own reading and sends one packet to the BS.
9. **Calculate energy consumption / update node energy.** The first-order radio model gives the energy of every
   send, receive and aggregation (see [03_MATHEMATICS.md](03_MATHEMATICS.md)); it is subtracted from the node's
   battery. A node that cannot afford an operation spends what it has left, and that packet is lost.
10. **Check dead nodes.** A node whose energy reached 0 J becomes DEAD; the round number is stored as its death
    round. Dead nodes are never selected or used again.
11. **Next round.** Steps 6–10 repeat until every node is dead or the round limit (2000) is reached.
12. **Calculate performance metrics.** From the stored rounds: FND, HND, LND, node-rounds, energy at round 500,
    throughput, PDR, average distances, cluster balance, fitness, run time.
13. **Compare algorithms.** For every metric: mean ± standard deviation over the runs, the improvement % of the
    proposed method over each baseline, a paired Wilcoxon test (is the difference real or luck?) with Holm
    correction, and Cliff's δ (how big is the difference?).
14. **Save CSV results and generate graphs.** All raw and summarised data are written as CSV files, the graphs
    as PNG files.
15. **Display the final comparison.** The final result table is printed in the terminal and written, with every
    graph and an automatic explanation, to `report.md`.

---

## WHAT IS THE FINAL OUTPUT OF THIS PROJECT?

**1. Working software**

* a Python WSN simulator (`python main.py …`) with Random, LEACH, GWO, ABC, the proposed Hybrid GWO-ABC and the
  base paper's DEAI-PSO;
* a window (`python main.py`) to configure, run, pause, stop, reset, compare and export simulations;
* an automatic test suite (`python -m pytest`).

**2. Result folders** (`results\…`), one per experiment. Each comparison folder contains:

| File | What it contains |
|---|---|
| `config.json` | every parameter used (re-run with `python main.py reproduce <folder>`) |
| `experiment.json` | algorithms, number of runs, seeds, date, Python/NumPy versions, run time |
| `runs_raw.csv` | one row per algorithm and run: FND, HND, LND, node-rounds, residual/consumed energy, throughput, PDR, distances, imbalance, fitness, run time, fitness evaluations |
| `history_raw.csv.gz` | one row per algorithm, run and **round**: alive, dead, residual and consumed energy, CH count, packets, PDR, distances, fitness, energy per radio activity (compressed CSV; Excel can open it after unzipping, pandas reads it directly) |
| `round_means.csv` | the per-round values averaged over runs (the data behind graphs 09–16) |
| `result_table.md` / `.csv` | **the final comparison table** (mean ± std) |
| `statistics.csv` | mean, std, min, median, max of every metric for every algorithm |
| `improvement_vs_baselines.csv` | proposed vs each baseline: improvement %, p-value, Holm-corrected p, Cliff's δ, verdict |
| `ch_log_run0.csv` | every cluster head of every round in run 0: round, CH id, x, y, residual energy, distance to BS, cluster size |
| `reproducibility_check_run0.csv` | run 0 simulated again from the saved settings; `identical = True` proves reproducibility |
| `convergence_round1.json` | the optimisers' improvement curves in round 1 |
| `01_topology.png` … `20_final_fitness.png` | the graphs (topology, CHs, clusters, data flow, dead nodes, convergence, alive/dead nodes, energy, throughput, PDR, CH count, distances, run time, lifetime bars, energy breakdown, fitness) |
| `report.md` | everything above explained automatically: tables, every graph, what each metric means, which differences are significant, trade-offs |

**3. Documentation**: the main [README.md](../README.md) (technical reference with all results) and these beginner
documents.

### What to show as evidence (in this order)

| # | Show | Where | Why |
|---|---|---|---|
| 1 | All tests pass | `python -m pytest` | the implementation is checked automatically |
| 2 | The GUI running live | `python main.py` | nodes, CHs, clusters, energy and death are really simulated |
| 3 | Network topology and clusters | `results\scenarios\S1_100nodes\01_topology.png`, `03_clusters_Hybrid_GWO-ABC.png` | what the network and the CH choice look like |
| 4 | Final result table | `results\scenarios\S1_100nodes\result_table.md` | the main comparison (20 paired runs) |
| 5 | Alive nodes vs rounds, lifetime bars | `09_alive_vs_rounds.png`, `18_lifetime_fnd_hnd_lnd.png` | network lifetime |
| 6 | Residual / consumed energy vs rounds | `11_residual_energy_vs_rounds.png`, `12_consumed_energy_vs_rounds.png` | energy efficiency |
| 7 | Convergence of GWO, ABC and Hybrid | `results\convergence\conv_all_round0.png` | the hybrid is the better optimiser |
| 8 | Comparison with the base paper | `results\base_paper\README.md`, `fig_improvement_vs_base_paper.png` | improvement over the existing system |
| 9 | Reproducibility | `reproducibility_check_run0.csv` (all `True`) | results are not invented |

[05_RESULTS_AND_GRAPHS.md](05_RESULTS_AND_GRAPHS.md) explains each of these graphs.

---

## Command cheat sheet

| Command | What it does | Time* |
|---|---|---|
| `python main.py` | open the GUI | — |
| `python -m pytest` | run all 93 automatic tests | ~15 s |
| `python main.py simulate` | one simulation of the Hybrid GWO-ABC with every graph | ~35 s |
| `python main.py simulate -a "LEACH"` | the same for another algorithm (`Random`, `LEACH`, `GWO`, `ABC`, `Hybrid GWO-ABC`, `DEAI-PSO`) | ≤ 35 s |
| `python main.py compare --runs 3` | Random, LEACH, GWO, ABC, Hybrid on 3 paired networks | ~2 min |
| `python main.py scenarios --only S1_100nodes` | the main comparison (20 paired runs) | ~12 min |
| `python main.py all --quick` | smoke test of every experiment (writes to `results_quick\`) | ~1.5 min |
| `python main.py all` | every experiment of the project | ~4 h |
| `python main.py basepaper` | comparison with the base paper | ~1 h 20 min |
| `python main.py reproduce <folder>` | re-run a saved experiment | as original |
| `python main.py diagrams` | re-draw the explanatory figures in `docs\figures\` | ~10 s |
| `python main.py postprocess` | refresh report text from the saved CSV files | ~10 s |

\* on the 12-core laptop used for the project.
