# Hybrid Grey Wolf Optimizer (GWO) and Artificial Bee Colony (ABC) for Energy-Efficient Cluster-Head Selection in Wireless Sensor Networks

A complete, executable Python WSN simulator (no MATLAB) that selects cluster heads (CHs) every round with
**LEACH**, **GWO**, **ABC** and the proposed **Hybrid GWO-ABC**, then measures how the choice affects network
lifetime, energy, throughput, delivery ratio, clustering quality, convergence and computational cost.

> **Research hypothesis (tested, not assumed):** combining GWO's global exploration with ABC's solution refinement
> may give better energy-aware CH selection than either algorithm alone or LEACH.
> Every number in this project comes from the simulator; the reports state where the hybrid is better, worse,
> or not significantly different. See [Results](#8-results) and [Comparison with the base paper](#9-comparison-with-the-base-paper-existing-system).

> **New to the project?** Start with the beginner documentation, [docs/00_START_HERE.md](docs/00_START_HERE.md):
> installing and running on Windows, every concept and equation explained from zero with diagrams and worked
> examples, how to read every graph, the MATLAB → Python justification, troubleshooting, a 23-step study guide, and
> presentation/viva preparation.

---

## 1. Quick start

```bash
python -m pip install -r requirements.txt

python main.py                       # GUI dashboard
python -m pytest                     # automatic tests (all must pass)
python main.py simulate -a "Hybrid GWO-ABC"            # one run, all figures, report.md
python main.py compare --runs 10                       # Random vs LEACH vs GWO vs ABC vs Hybrid, paired runs
python main.py scenarios --only S1_100nodes            # the main comparison (≈ 12 min)
python main.py scenarios | ablation | sensitivity | convergence
python main.py basepaper                               # vs the base paper's DEAI-PSO (existing system), §9 (≈ 1 h 20 min)
python main.py benchmark            # clean sequential runtime comparison (no parallel load)
python main.py all                   # every experiment of §8 (≈ 4 h on a 12-thread laptop)
python main.py all --quick           # smoke test of every experiment (tiny sizes, written to results_quick/)
python main.py postprocess           # refresh report text (trade-offs, data-quality notes) from saved CSVs
python main.py reproduce results/scenarios/S1_100nodes # re-run a saved experiment exactly
python main.py diagrams              # redraw the explanatory figures in docs/figures
```

Change any parameter with `--set` (dotted names for nested fields) or load a saved `config.json`:

```bash
python main.py compare --runs 20 --set n_nodes=200 --set bs_y=175 --set gwo.population=30
python main.py compare --config results/scenarios/S2_200nodes/config.json
```

Requires Python ≥ 3.10, NumPy, pandas, Matplotlib, SciPy (Wilcoxon test only), Tkinter (bundled with the
Windows/macOS installers). Runs on a normal laptop; experiments use all cores but one by default (`--workers`).

## 2. Project structure

```text
Hybrid-GWO-ABC-WSN/
├── main.py                      CLI: gui | simulate | compare | scenarios | ablation | sensitivity | convergence | all | reproduce
├── config.py                    every parameter (dataclasses, JSON save/load, dotted overrides, validation)
├── models/                      node.py (SensorNode), network.py (deployment, state, death), energy_model.py (radio model)
├── PROGRESS.md                  visible to-do list / progress of the project
├── algorithms/                  leach.py, gwo.py, abc.py, hybrid_gwo_abc.py, fitness.py (objective), base.py (interface),
│                                deai_pso.py (base paper's method, the "existing system")
├── simulation/                  simulator.py (round loop), clustering.py, routing.py, transmission.py (energy accounting)
├── evaluation/                  metrics.py (definitions), statistics.py (tests), comparison.py (tables, interpretation), report.py,
│                                base_paper_report.py (improvement-over-base-paper report)
├── visualization/               network_plot.py, convergence_plot.py, performance_plots.py, style.py,
│                                diagrams.py (explanatory figures of the documentation)
├── gui/dashboard.py             Tkinter dashboard
├── experiments/experiment_runner.py   paired multi-run experiments, scenarios, ablation, sensitivity, convergence
├── experiments/base_paper.py          base-paper scenarios, development pilot, final comparison, attribution
├── tests/                       pytest suite (models, energy, clustering, transmission, fitness, every algorithm, pipeline,
│                                base paper, the documentation's worked examples)
├── docs/                        beginner documentation (start with docs/00_START_HERE.md) and its figures
├── data/                        (user data, e.g. exported topologies)
├── results/                     generated: CSVs, figures, report.md per experiment
└── results_quick/               generated by `all --quick` (smoke test only, never used for reporting)
```

## 3. System model

### 3.1 Network and nodes
`N` nodes are deployed uniformly at random in a `W × H` field (reproducible seed); the base station (BS) can be
anywhere, inside or outside the field. Each `SensorNode` exposes ID, coordinates, initial/residual energy,
ALIVE/DEAD status, CH status, cluster ID, distance to CH and BS, and packets generated/transmitted/received.
(For speed the network stores node state as NumPy arrays; `SensorNode` is an object view onto one row, so the
object API and the vectorised simulator always agree.)

Defaults: 100 nodes, 100 m × 100 m, 0.5 J/node, BS (50, 50), 4000-bit packets, 2000 rounds, p = 5 % CHs.

### 3.2 First-order radio energy model

| Operation | Energy |
|---|---|
| Transmit k bits over d < d0 | `E_tx = E_elec·k + E_fs·k·d²` |
| Transmit k bits over d ≥ d0 | `E_tx = E_elec·k + E_mp·k·d⁴` |
| Receive k bits | `E_rx = E_elec·k` |
| Aggregate one k-bit signal | `E_DA·k` |
| Crossover distance | `d0 = √(E_fs / E_mp)` ≈ 87.7 m |

`E_elec = 50 nJ/bit, E_fs = 10 pJ/bit/m², E_mp = 0.0013 pJ/bit/m⁴, E_DA = 5 nJ/bit/signal` (all configurable).

### 3.3 One simulation round
```text
check alive nodes → select CHs (algorithm) → form clusters (each alive non-CH node joins its nearest CH)
→ every alive node generates one reading → members transmit to CH (E_tx)
→ CH receives (E_rx) and aggregates (E_DA) each packet + its own → CH sends one packet to the BS (E_tx)
→ update energy → nodes with 0 J become DEAD → record metrics → next round
```
The simulation stops at the round limit or when every node is dead. A node that cannot afford an operation spends
what it has and dies; data held by a CH that dies mid-round is lost (counted in PDR). If no CH exists (possible in
LEACH), nodes transmit directly to the BS. Control-packet overhead is off by default (`control_bits = 0`) and
can be enabled for all algorithms.

## 4. Algorithms

All algorithms receive the same network object, so node coordinates, initial energy, BS, packet size, radio
model and horizon are identical. The three optimisers run at the BS with global knowledge (LEACH-C style) and
share the same fitness function, solution encoding, repair operator and CH-eligibility rule. A **Random** baseline
(`RandomSelector` in `algorithms/base.py`: K_opt alive nodes chosen uniformly at random every round, no energy
check) is included in the main scenario to show what CH selection without any intelligence achieves.

**Solution encoding.** A binary vector over the alive nodes, e.g. `[0,1,0,0,1,0,1,…]` (1 = CH). Dead nodes are
excluded from the search space. `repair` keeps the CH count in `[K_min, K_max] = K_opt·(1 ± 0.5)`,
`K_opt = round(p·N_alive)`, and a binary vector cannot contain duplicate CHs.

**CH eligibility (all optimisers).** Only nodes with residual energy ≥ the mean alive energy may be CHs (the
LEACH-C rule; `ch_energy_threshold`, 0 disables it). *Disclosure:* this was added after a pilot run in which all
three optimisers had a much earlier FND than LEACH (533–617 vs 887 rounds), because the CH→BS distance term kept
re-electing the nodes closest to the BS. The rule applies equally to GWO, ABC and the hybrid, and its effect is
measured in the sensitivity analysis (`ch_energy_threshold` = 0, 0.5, 1).

### 4.1 LEACH (`algorithms/leach.py`)
Each alive node in G (not CH during the current epoch of 1/p rounds) becomes CH if `u < T(n)`,
`T(n) = p / (1 − p·(r mod 1/p))`. G is reset every epoch, so each node is CH once per epoch. Members join the
nearest CH (strongest advertisement). LEACH is not weakened: it uses the same radio model and clustering code.

### 4.2 Binary GWO (`algorithms/gwo.py`)
Alpha, beta and delta are the three best *distinct* solutions found so far (elitist); every other wolf is an omega.
For each leader `L`: `A = 2a·r1 − a`, `C = 2·r2`, `D = |C·L − X|`, `X_L = L − A·D`; the continuous step is
`Y = (X_α + X_β + X_δ)/3`. `a` decreases linearly 2 → 0 (|A| > 1 exploration, |A| < 1 exploitation).
Discretisation: `S(y) = 1/(1 + e^(−10(y−0.5)))`, bit j = 1 with probability `S(y_j)`; the repair keeps/adds the
highest-`S` nodes.

### 4.3 Discrete ABC (`algorithms/abc.py`)
`SN = colony/2` food sources (CH sets). **Employed bees** create one neighbour per source and keep the better one
(greedy); failures increase the source's trial counter. **Onlooker bees** pick sources with probability
`p_i = fit_i / Σfit`, `fit_i = 1/(1+F_i)`, and search the same way. **Scout bees** replace the source with the most
trials once `trial > limit`. The best source ever found is memorised. Neighbour operator (discrete analogue of
`v_ij = x_ij + φ(x_ij − x_kj)`): with partner `x_k` and `φ ~ U(−1,1)`, `φ ≥ 0` swaps one of my CHs for one of the
partner's (information sharing); otherwise a CH hands its role to one of its nearest eligible neighbours (local
search); with probability 0.1 one CH is added/removed (count exploration).

### 4.4 Proposed Hybrid GWO-ABC (`algorithms/hybrid_gwo_abc.py`)
A co-evolutionary hybrid with a two-way exchange every iteration:
```text
initialise wolf pack + food sources (valid CH sets)
repeat T times:
  1. GWO step: every wolf moves w.r.t. alpha/beta/delta        (global exploration)
  2. GWO → ABC: alpha, beta, delta replace the worst food sources if better and not duplicates
  3. ABC employed phase                                        (refines the transferred elites)
  4. ABC onlooker phase                                        (exploitation of promising sources)
  5. ABC scout phase                                           (re-seeds exhausted sources)
  6. ABC → GWO: if the ABC best beats delta, it replaces the worst wolf and joins the leader set
  7. elite preservation: global best = min(alpha, ABC best)
return global best (always a valid CH set)
```
**Fair budget:** the hybrid uses half the wolves (10) and half the bees (10) by default, so it spends the same
number of fitness evaluations per iteration (20) as standalone GWO (20 wolves) or ABC (20 bees). It records GWO,
ABC and hybrid best-so-far fitness per iteration.

### 4.5 Base paper — DEAI-PSO, the "existing system" (`algorithms/deai_pso.py`)
Re-implemented from M. Haris and H. Nam, *IEEE Access* 13 (2025), doi:10.1109/ACCESS.2025.3583922:
PSO whose particles are the coordinates of K = 10 % CHs (decoded to the nearest unused node with above-average
energy, as in PSO-C), velocity/position update (Eqs. 8–9), time-varying acceleration coefficients (Eqs. 10–11),
double-exponential adaptive inertia ω = e^(−e^(−d(X, Pbest)·(T−k))) (Eq. 13), and the objective
F = a·Σ E_t(N_i) + (1 − a)·n·std(R_t) (Eq. 12: predicted round energy + spread of residual energy). Its three-tier
model (free nodes within 85 m of the BS send directly) and 200-bit control packets are supported by the simulator
(`free_node_radius`, `control_bits`). `PaperFitness` reproduces Eq. 12 exactly (checked against a hand calculation
in `tests/test_base_paper.py`), so any of the project's optimisers can also be run on the base paper's objective:
`GWO (Eq. 12)`, `ABC (Eq. 12)`, `Hybrid GWO-ABC (Eq. 12)`.

## 5. Fitness function (`algorithms/fitness.py`, minimised)

```text
F = w1·EnergyCost + w2·IntraDist + w3·CH_BS + w4·Imbalance + w5·CountPenalty  (+ 10 if infeasible)
```

| Term | Normalised definition (each in [0, 1]) | Default weight |
|---|---|---|
| EnergyCost | `0.5·(1 − mean E_CH / max E_alive) + 0.5·E_round / E_upper` (CH residual energy + predicted round consumption) | 0.30 |
| IntraDist | mean member→CH distance / max alive node–node distance | 0.25 |
| CH_BS | mean CH→BS distance / max alive node–BS distance | 0.20 |
| Imbalance | min(1, coefficient of variation of cluster sizes) | 0.15 |
| CountPenalty | min(1, \|K − K_opt\| / K_opt) | 0.10 |

`E_round` is the radio energy the round would consume with this clustering (member TX + CH RX/DA + CH→BS TX);
`E_upper = N_alive·(E_tx(k, d_max) + E_rx + E_DA·k)` bounds it. A solution is **infeasible** (penalty 10) if it has
no CH, its CH count is outside the bounds, or a CH cannot afford its predicted round load. The weights are a
starting point, not proven optima; the sensitivity analysis varies them. The same function and weights score
every algorithm's CH sets (including LEACH's) for the "Final Fitness" metric.

## 6. Metrics (`evaluation/metrics.py`)

| Metric | Definition | Better |
|---|---|---|
| FND / HND / LND | round in which the first node / ≥ 50 % of nodes / the last node died (if not reached: rounds simulated, marked ≥) | higher |
| Node-rounds | Σ over rounds of alive nodes (area under the alive curve) | higher |
| Residual energy | total residual energy at the checkpoint round (default 500) | higher |
| Energy consumption | N·E0 − residual energy at the checkpoint round | lower |
| Throughput | sensor data packets delivered to the BS (directly or inside aggregated CH packets); bits = BS packets × packet size | higher |
| PDR | delivered data packets / generated data packets | higher |
| Avg. cluster distance | mean member→CH distance, averaged over rounds 1..checkpoint | lower |
| Avg. CH–BS distance | mean CH→BS distance, averaged over rounds 1..checkpoint | lower |
| Cluster imbalance | CV of cluster sizes, averaged over rounds 1..checkpoint | lower |
| Final fitness | mean per-round fitness of the CH set used (same weights for all), rounds 1..checkpoint | lower |
| Runtime | wall-clock CH-selection time per simulation (and ms/round) | lower |
| Computational cost | total fitness evaluations | lower |
| Convergence | best-so-far fitness per iteration | — |

Improvement is computed from data: higher-is-better `((P − B)/B)·100`, lower-is-better `((B − P)/B)·100`, so a
positive value always favours the proposed algorithm.

## 7. Experimental method

* **Paired runs.** Run *r* of every algorithm uses deployment and algorithm seed `seed + r`: same topology, same
  conditions. Defaults: 20 runs (scenario 1, which also includes the Random baseline), 10 runs (other scenarios,
  ablation), 5 runs per sensitivity setting.
* **Statistics.** Mean, std, min, median, max; paired two-sided **Wilcoxon signed-rank** test, Holm-corrected over
  the baselines; **Cliff's δ** effect size. "Significant" means Holm-adjusted p < 0.05. Differences below 1 % are
  flagged as practically negligible even when significant.
* **Scenarios.** S1 100 nodes, S2 200 nodes, S3 300 nodes (100 × 100 m, BS centre); S4 BS on the edge (50, 100);
  S5 BS outside the field (50, 175).
* **Ablation.** GWO only, ABC only, GWO→ABC (sequential halves), ABC→GWO, hybrid without the energy term,
  without the distance terms (w2 = w3 = 0), without the balance term, full hybrid.
* **Sensitivity (one factor at a time).** Nodes, field size, initial energy, CH %, BS position, GWO population,
  ABC colony, iterations, fitness-weight presets, CH-eligibility threshold.
* **Convergence.** GWO, ABC and Hybrid optimise identical network states (fresh, and after 500 LEACH rounds),
  20 seeds, equal evaluation budgets.

Every experiment folder contains `config.json`, `experiment.json` (algorithms, runs, seeds, versions),
`runs_raw.csv`, `history_raw.csv.gz`, `statistics.csv`, `improvement_vs_baselines.csv`, `result_table.csv/.md`,
`ch_log_run0.csv` (every selected CH of run 0: round, CH id, coordinates, residual energy at selection, CH–BS
distance, cluster size), `reproducibility_check_run0.csv` (run 0 re-simulated from the saved config and compared
with the saved results), all figures and an auto-generated `report.md`, which explains each figure and metric (what it represents, how it was
calculated, why it matters, the observed values, whether differences are significant, possible mechanisms
and trade-offs).

## 8. Results

All values below are copied from the generated reports in `results/` (default configuration unless stated;
mean ± std over paired runs). `*` = significant after Holm correction (paired Wilcoxon, α = 0.05).

### 8.1 Short answer to the hypothesis

* **Hybrid GWO-ABC vs LEACH:** in every scenario the hybrid has a significantly later first node death (FND
  +24.9 % to +37.0 %), later HND (+2 % to +9 %), more delivered data (+1.8 % to +7.8 %), higher PDR, more residual
  energy at round 500, 12–17 % shorter member→CH links and far more balanced clusters. LEACH has a significantly
  **later last node death** (the hybrid's LND is 10–19 % earlier) and is about 1,000–4,600× cheaper to compute.
  These gains are shared by GWO and ABC; they come from centralised, energy-aware optimisation, not from the
  hybridisation itself.
* **Hybrid GWO-ABC vs GWO and ABC:** the hybrid is a **better optimiser** of the fitness function: 5–7.5 % lower
  final fitness in the dedicated convergence test (p < 0.01) and 0.6–5.3 % lower in-simulation fitness in all five
  scenarios, mostly through better cluster balance. That advantage **does not translate into a longer network
  lifetime.** FND and LND show no significant difference in any scenario. HND, residual energy, throughput
  and node-rounds are either not significantly different or *slightly worse* (always < 0.2 %, practically
  negligible). The hybrid is also 1.2–2.3× slower per round than ABC/GWO at an equal number of fitness
  evaluations (§8.7).
* **Hybrid GWO-ABC vs Random selection (S1):** FND +39.8 %, HND +1.1 %, throughput +3.4 %, PDR, energy, member
  links and balance significantly better; LND 12.3 % earlier. Random is the worst method on FND (807 rounds) but,
  because it always uses exactly K_opt CHs while LEACH's CH count fluctuates (per-round std 2.2), it beats LEACH on
  HND, LND, energy and throughput — LEACH's rotation protects only the first death.
* **Conclusion:** the experiments support the hypothesis at the *optimisation* level (better CH configurations
  according to the objective) but **not** at the *network* level against GWO and ABC; at the network level all
  three metaheuristics beat Random and LEACH on stability period (FND) and lose to them on LND.

### 8.2 Final result table — Scenario 1 (100 nodes, 100 × 100 m, BS at (50, 50), 20 paired runs)

| Metric | Random | LEACH | GWO | ABC | Hybrid GWO-ABC |
|---|---:|---:|---:|---:|---:|
| FND (rounds) | 807 ± 31 | 892 ± 28 | 1,126 ± 7 | 1,125 ± 8 | 1,128 ± 7 |
| HND (rounds) | 1,125 ± 11 | 1,104 ± 8 | 1,138 ± 7 | 1,138 ± 6 | 1,138 ± 6 |
| LND (rounds) | 1,321 ± 27 | 1,287 ± 28 | 1,162 ± 11 | 1,162 ± 10 | 1,158 ± 13 |
| Residual energy @ round 500 (J) | 27.750 ± 0.119 | 27.395 ± 0.156 | 28.110 ± 0.097 | 28.113 ± 0.101 | 28.102 ± 0.104 |
| Energy consumption @ round 500 (J) | 22.250 ± 0.119 | 22.605 ± 0.156 | 21.890 ± 0.097 | 21.887 ± 0.101 | 21.898 ± 0.104 |
| Throughput (packets) | 109,907 ± 603 | 108,883 ± 730 | 113,715 ± 611 | 113,732 ± 611 | 113,662 ± 617 |
| PDR | 0.9898 ± 0.0009 | 0.9892 ± 0.0014 | 0.9985 ± 0.0005 | 0.9986 ± 0.0005 | 0.9982 ± 0.0006 |
| Avg. cluster distance (m) | 25.055 ± 0.805 | 27.073 ± 0.850 | 22.499 ± 0.774 | 22.470 ± 0.805 | 22.563 ± 0.823 |
| Avg. CH–BS distance (m) | 38.545 ± 1.562 | 38.554 ± 1.446 | 38.282 ± 1.384 | 38.278 ± 1.352 | 38.225 ± 1.417 |
| Runtime per simulation (s)† | 0.56 ± 0.13 | 0.06 ± 0.01 | 54.54 ± 9.69 | 101.17 ± 15.92 | 132.15 ± 20.97 |
| Final fitness | 0.2904 ± 0.0117 | 1.3309 ± 0.1298 | 0.2416 ± 0.0113 | 0.2402 ± 0.0122 | 0.2387 ± 0.0115 |

† Measured with 11 simulations in parallel (noisy, see §8.7 for the clean benchmark). The S1 folder was re-run when
the Random baseline was added; the 80 runs of the other four algorithms reproduced the earlier results exactly
(only the wall-clock runtimes differ). LEACH's final fitness is high because in 10.1 % of rounds 1–500 its random
election produces a CH count outside the allowed range (0.5 % of rounds have no CH at all), which the objective
penalises; LEACH does not optimise this objective.

### 8.3 All scenarios — Hybrid GWO-ABC improvement (%) over each baseline

Positive = hybrid better (direction-aware formula), `*` = significant. Full tables, figures and interpretation:
`results/scenarios/<scenario>/report.md`; overview: `results/scenarios/README.md`.

| Metric | Baseline | S1 100 n | S2 200 n | S3 300 n | S4 BS edge | S5 BS outside |
|---|---|---:|---:|---:|---:|---:|
| FND / HND / LND | Random | +39.75* / +1.11* / −12.33* | — | — | — | — |
| Throughput / PDR / residual energy | Random | +3.42* / +0.85* / +1.27* | — | — | — | — |
| FND | LEACH | +26.49* | +26.10* | +24.86* | +27.49* | +37.03* |
| FND | GWO | +0.12 | −0.21 | −0.04 | −0.13 | +0.04 |
| FND | ABC | +0.20 | −0.04 | +0.10 | +0.01 | +0.19 |
| HND | LEACH | +3.02* | +2.25* | +1.98* | +3.24* | +9.23* |
| HND | GWO | +0.01 | −0.10* | −0.07 | −0.11* | −0.14* |
| HND | ABC | −0.01 | −0.09* | +0.00 | −0.12* | −0.10* |
| LND | LEACH | −9.99* | −14.32* | −14.22* | −15.31* | −18.75* |
| LND | GWO | −0.32 | −1.19* | −0.63 | −0.32 | −0.13 |
| LND | ABC | −0.35 | −0.42 | +0.58 | −0.02 | −0.06 |
| Residual energy @500 | LEACH | +2.58* | +0.96* | +0.54* | +2.78* | +8.35* |
| Residual energy @500 | GWO | −0.03 | −0.07* | −0.04* | −0.09* | −0.06* |
| Residual energy @500 | ABC | −0.04* | −0.06* | +0.01 | −0.11* | −0.05 |
| Throughput | LEACH | +4.39* | +2.57* | +1.84* | +4.48* | +7.83* |
| Throughput | GWO | −0.05 | −0.17* | −0.10 | −0.13 | −0.07 |
| Throughput | ABC | −0.06 | −0.14* | −0.01 | −0.18* | −0.07 |
| PDR | LEACH | +0.91* | +0.86* | +0.82* | +0.91* | +0.74* |
| PDR | GWO / ABC | −0.03 / −0.04 | −0.05 / −0.05 | −0.04 / −0.02 | −0.02 / −0.07 | +0.03 / −0.03 |
| Cluster imbalance | GWO | +14.71* | +16.87* | +16.38* | +20.88* | +24.55* |
| Cluster imbalance | ABC | +4.92* | +19.08* | +23.69* | +9.16* | +10.58* |
| Final fitness | GWO | +1.19* | +1.31* | +1.61* | +1.75* | +2.71* |
| Final fitness | ABC | +0.62* | +3.53* | +5.30* | +0.87* | +1.11* |
| Avg. cluster distance | GWO | −0.28 | −1.34* | −1.09* | −0.85* | +0.44* |
| Avg. cluster distance | ABC | −0.41* | −1.40* | −0.13 | −1.04* | −0.22 |

Absolute lifetimes (mean FND / HND / LND): S2 LEACH 921 / 1,148 / 1,401 vs Hybrid 1,162 / 1,174 / 1,200;
S3 LEACH 940 / 1,164 / 1,440 vs Hybrid 1,173 / 1,187 / 1,236; S4 LEACH 876 / 1,091 / 1,345 vs Hybrid
1,117 / 1,126 / 1,139; S5 (BS outside, multipath CH→BS links) LEACH 703 / 895 / 1,218 vs Hybrid 963 / 978 / 989.

### 8.4 Convergence (`results/convergence/report.md`)

Same network states, 20 seeds, 30 iterations, ≈ 620 fitness evaluations each:

| Network state | GWO final fitness | ABC final fitness | Hybrid final fitness | Hybrid vs GWO | Hybrid vs ABC |
|---|---:|---:|---:|---:|---:|
| Fresh (round 0) | 0.1736 ± 0.0131 | 0.1693 ± 0.0167 | 0.1605 ± 0.0100 | 7.53 % lower, p = 4.8e-5 | 5.22 % lower, p = 0.0083 |
| After 500 LEACH rounds | 0.2195 ± 0.0169 | 0.2147 ± 0.0150 | 0.2047 ± 0.0139 | 6.75 % lower, p = 2.1e-4 | 4.66 % lower, p = 0.0011 |

The hybrid's internal curves show the mechanism: transferred GWO elites start the ABC colony from good regions,
and ABC refinements fed back to the pack become new alpha wolves.

### 8.5 Ablation (`results/ablation/report.md`, S1 settings, 10 paired runs)

| Variant | FND | HND | LND | Throughput | Final fitness |
|---|---:|---:|---:|---:|---:|
| GWO only | 1,126 ± 7 | 1,138 ± 7 | 1,162 ± 12 | 113,713 ± 627 | 0.2467 ± 0.0128 |
| ABC only | 1,124 ± 9 | 1,138 ± 7 | 1,165 ± 8 | 113,780 ± 640 | 0.2457 ± 0.0135 |
| GWO→ABC (sequential) | 1,126 ± 8 | 1,137 ± 7 | 1,161 ± 9 | 113,667 ± 661 | 0.2453 ± 0.0126 |
| ABC→GWO (sequential) | 1,128 ± 8 | 1,137 ± 7 | 1,160 ± 13 | 113,696 ± 641 | 0.2474 ± 0.0126 |
| Hybrid w/o energy term | 1,116 ± 11 | 1,132 ± 8 | 1,302 ± 96 | 113,070 ± 751 | 0.2470 ± 0.0136 |
| Hybrid w/o distance terms | 1,132 ± 7 | 1,140 ± 7 | 1,150 ± 6 | 113,676 ± 635 | 0.2232 ± 0.0118 |
| Hybrid w/o balance term | 1,130 ± 5 | 1,146 ± 5 | 1,155 ± 4 | 114,244 ± 455 | 0.2703 ± 0.0127 |
| **Full Hybrid GWO-ABC** | 1,128 ± 7 | 1,138 ± 7 | 1,158 ± 13 | 113,637 ± 663 | 0.2439 ± 0.0128 |

* **Co-evolution vs sequential hybrids:** the full hybrid reaches significantly better fitness than GWO→ABC
  (+0.60 %) and ABC→GWO (+1.42 %), but no lifetime metric differs significantly.
* **Energy term:** removing it significantly lowers FND (−1.0 %), HND and throughput, and makes LND much later
  and far more variable (1,302 ± 96). Without the residual-energy incentive, drain is less even.
* **Balance term:** removing it gives significantly *better* HND (+0.7 %), node-rounds, residual energy and
  throughput (all < 1 %), but much worse balance. The balance term pushes toward equal-size clusters at a small
  energy cost, which is the same trade-off seen when comparing the hybrid with GWO/ABC.
* **Distance terms:** the variant without them has a *lower* mean full-weight fitness over rounds 1–500
  (0.2232 vs 0.2439), although at round 1 the full hybrid is clearly better (0.165 vs 0.200 over 8 seeds;
  checked separately). Per-round optimisation is myopic: the full objective keeps choosing CHs near the BS,
  depleting them and making later rounds harder, while the distance-free variant spends outer nodes first. Network
  lifetime is almost unchanged (FND −0.35 %, n.s. for HND/LND/throughput).

### 8.6 Sensitivity (`results/sensitivity/report.md`, one factor at a time, 5 paired runs per setting)

Mean FND / HND / LND (rounds); default setting in bold. "≥ 2000" = not reached within the 2000-round horizon.

| Factor | Setting | LEACH | GWO | ABC | Hybrid GWO-ABC |
|---|---|---:|---:|---:|---:|
| CH eligibility threshold | 0 (rule off) | — | 659 / 1,192 / 1,305 | 665 / 1,214 / 1,299 | 644 / 1,215 / 1,298 |
| | 0.5 | — | 1,063 / 1,135 / 1,234 | 1,056 / 1,138 / 1,239 | 1,061 / 1,137 / 1,230 |
| | **1.0** | — | 1,130 / 1,141 / 1,166 | 1,124 / 1,141 / 1,166 | 1,130 / 1,141 / 1,162 |
| CH percentage | 3 % | 891 / 1,071 / 1,252 | 1,067 / 1,091 / 1,117 | 1,066 / 1,092 / 1,120 | 1,067 / 1,092 / 1,120 |
| | **5 %** | 884 / 1,105 / 1,295 | 1,130 / 1,141 / 1,166 | 1,124 / 1,141 / 1,166 | 1,130 / 1,141 / 1,162 |
| | 10 % | 1,000 / 1,168 / 1,436 | 1,184 / 1,191 / 1,204 | 1,186 / 1,193 / 1,208 | 1,184 / 1,191 / 1,204 |
| Initial energy | 0.25 J | 417 / 559 / 670 | 561 / 572 / 593 | 562 / 572 / 585 | 563 / 571 / 585 |
| | 1.0 J | 1,829 / ≥ 2000 / ≥ 2000 | ≥ 2000 (all) | ≥ 2000 (all) | ≥ 2000 (all) |
| Field side (BS at centre) | 50 m | 918 / 1,188 / 1,560 | 1,181 / 1,197 / 1,214 | 1,186 / 1,198 / 1,210 | 1,180 / 1,198 / 1,212 |
| | 200 m | 493 / 785 / 1,041 | 641 / 912 / 943 | 613 / 910 / 946 | 589 / 910 / 935 |
| Nodes | 50 | 954 / 1,080 / 1,223 | 1,082 / 1,094 / 1,109 | 1,082 / 1,096 / 1,111 | 1,080 / 1,095 / 1,114 |
| | 200 | 931 / 1,151 / 1,402 | 1,164 / 1,176 / 1,219 | 1,163 / 1,176 / 1,210 | 1,163 / 1,175 / 1,203 |
| BS position | (0, 0) corner | 868 / 1,067 / 1,383 | 1,106 / 1,116 / 1,128 | 1,107 / 1,116 / 1,127 | 1,105 / 1,115 / 1,125 |
| | (50, 150) outside | 813 / 997 / 1,298 | 1,050 / 1,062 / 1,076 | 1,049 / 1,062 / 1,074 | 1,050 / 1,062 / 1,075 |

What the sensitivity analysis shows:

* **The CH-eligibility rule is a trade-off, not a free gain.** Switching it off cuts FND by about 42 % (≈ 1,130 → ≈ 650)
  but raises HND by ≈ 6 % and LND by ≈ 12 % for all three optimisers. The default (1.0) favours the stability
  period (FND); applications that care about the last surviving nodes may prefer 0 or 0.5.
* **CH percentage matters more than the optimiser settings.** 10 % CHs gives a later FND, HND and LND than the
  default 5 % for every algorithm (e.g. Hybrid FND 1,184 vs 1,130), so 5 % is not optimal for this network.
* **Optimiser budget is not the bottleneck.** GWO population 10–40, ABC colony 10–40 and 10–50 iterations change
  mean FND/HND by at most 7 rounds (see `results/sensitivity/report.md`).
* **The optimisers' FND advantage over LEACH holds for every network size, energy, field size and BS position
  tested**, and LEACH keeps the later LND in every setting except 1.0 J, where both reach the horizon.
* **Fitness weights:** energy-heavy weights give the best Hybrid FND/HND (1,136 / 1,147) and distance-heavy
  weights the best LND (1,196). Balance-heavy weights are worst on FND/HND (1,115 / 1,128), consistent with the
  ablation finding that the balance term costs some energy.
* In the largest field (200 m × 200 m) the spread between runs is large (FND std 75–121 rounds over 5 runs), so the
  differences between GWO (641), ABC (613) and Hybrid (589) there are not conclusive.

### 8.7 Runtime — clean sequential benchmark (`results/runtime_benchmark/report.md`)

CH-selection time per round over the first 100 rounds, one process, no parallel load, median of 5 seeds:

| Algorithm | 100 nodes | 200 nodes | 300 nodes | Fitness evaluations / round |
|---|---:|---:|---:|---:|
| LEACH | 0.01 ms | 0.01 ms | 0.01 ms | 0 |
| GWO | 11.94 ms | 19.85 ms | 33.38 ms | 620 |
| ABC | 21.53 ms | 28.36 ms | 38.03 ms | 615–622 |
| Hybrid GWO-ABC | 27.78 ms | 35.86 ms | 45.79 ms | 618–625 |

The hybrid spends the same number of fitness evaluations as GWO and ABC, but runs two populations and more
operators per iteration, so it is 1.20–1.29× slower than ABC and 1.37–2.33× slower than GWO per round. It was
slower on every seed except one disturbed 300-node measurement (flagged in the report). LEACH is about
1,000–4,600× cheaper. All optimisers stay below 50 ms per round, which is acceptable for a BS that re-clusters once
per round.

### 8.8 Discussion

* **Why all optimisers beat LEACH on FND but lose on LND.** The optimisers only use above-average-energy nodes as
  CHs and minimise predicted round energy, so energy drains almost uniformly: nodes die within a narrow window
  (mean LND − FND in S1: 31 rounds for the hybrid, 36 for GWO, 37 for ABC, 395 for LEACH, 514 for Random). LEACH's random rotation drains some nodes faster (early
  FND) and leaves others with energy that keeps a sparse network alive longer (later LND). Which is preferable
  depends on the application: full coverage (stability period, FND/HND) favours the optimisers; "any node still
  reporting" (LND) favours LEACH.
* **Why the hybrid's better fitness does not give a longer lifetime.** (i) Under the eligibility rule and the energy
  term, GWO and ABC already find near-equivalent CH sets, so the remaining fitness gain (1–5 %) is small in
  energy terms. (ii) Most of the hybrid's extra fitness comes from cluster balance, which the ablation shows costs a
  little energy. (iii) The objective is optimised one round at a time; a better per-round score is not the same as a
  better long-term energy plan (see the distance-term ablation).
* **What would be needed to show a network-level benefit:** a fitness designed around lifetime, e.g. a
  multi-round or residual-energy-variance term, stronger energy weights, or a multi-hop/heterogeneous setting where
  CH placement matters more. These are suggested as future work, not tested here.

## 9. Comparison with the base paper (existing system)

**Base paper:** M. Haris and H. Nam, *"Enhancing Energy Efficiency in IoT-WSNs Through Optimized PSO Cluster Head
Selection"*, IEEE Access, vol. 13, pp. 126496–126512, 2025, doi:10.1109/ACCESS.2025.3583922 (DEAI-PSO, simulated by
the authors in MATLAB R2023a). The full, automatically generated report is
[`results/base_paper/README.md`](results/base_paper/README.md).

### 9.1 How the comparison was made fair

* **Same problem.** DEAI-PSO was re-implemented (§4.5) and run under the paper's Table 3 conditions: BP1 100 nodes
  in 100 × 100 m, BP2 160 nodes in 100 × 100 m, BP3 200 nodes in 150 × 150 m; BS at (200, 50); 0.5 J per node;
  4000-bit data and 200-bit control packets; 10 % CH target; nodes within 85 m of the BS send directly ("free
  nodes"); CH candidates need at least average energy; 3000-round horizon, energy compared at round 300.
* **Primary comparison = only the optimiser changes.** `Hybrid GWO-ABC (Eq. 12)` runs the proposed hybrid optimiser
  on the paper's **own** objective (Eq. 12, same weight *a*), so any difference comes from the optimiser. The
  project's multi-objective `Hybrid GWO-ABC`, and GWO/ABC on Eq. 12, are reported too.
* **Baseline tuned in its favour.** Settings the paper leaves open were chosen on separate development seeds
  (9000–9004) to maximise DEAI-PSO's performance (a ∈ {0.2, 0.5, 0.8} × distance normalised/in metres → a = 0.8,
  metres). The proposed method was not tuned.
* **Equal budget** (≈ 620 fitness evaluations per round; DEAI-PSO 648), **20 paired runs** on held-out seeds 42–61
  (the paper used 10), Wilcoxon signed-rank tests with Holm correction over all 24 scenario × metric tests.

### 9.2 Results — proposed Hybrid GWO-ABC (Eq. 12) vs DEAI-PSO (mean ± std, 20 paired runs)

`*` = significant after Holm correction; improvement > 0 means the proposed method is better.

| Scenario | Metric | DEAI-PSO (base paper) | Hybrid GWO-ABC (Eq. 12) | Improvement |
|---|---|---:|---:|---:|
| BP1 (100 nodes) | FND / HND / LND (rounds) | 632 / 647 / 653 | 636 / 691 / 700 | +0.51 / **+6.90\*** / **+7.09\*** % |
| | Node-rounds | 64,509 ± 1,718 | 68,842 ± 1,514 | **+6.72 %\*** |
| | Throughput (packets) | 64,045 ± 1,710 | 68,360 ± 1,539 | **+6.74 %\*** |
| | Residual energy @ round 300 (J) | 26.77 ± 0.60 | 28.13 ± 0.46 | **+5.11 %\*** |
| | PDR | 0.9913 | 0.9915 | +0.03 % |
| BP2 (160 nodes) | FND / HND / LND (rounds) | 635 / 659 / 695 | 645 / 708 / 718 | +1.53 / **+7.39\*** / **+3.27\*** % |
| | Node-rounds | 105,257 ± 1,692 | 112,643 ± 1,561 | **+7.02 %\*** |
| | Throughput (packets) | 104,428 ± 1,860 | 111,964 ± 1,594 | **+7.22 %\*** |
| | Residual energy @ round 300 (J) | 43.39 ± 0.57 | 45.78 ± 0.45 | **+5.49 %\*** |
| | PDR | 0.9906 | 0.9926 | **+0.20 %\*** |
| BP3 (200 nodes) | FND / HND / LND (rounds) | 489 / 718 / 1,487 | 483 / 740 / 1,487 | **−1.16\*** / **+2.98\*** / 0.00 % |
| | Node-rounds | 153,481 ± 2,901 | 156,679 ± 2,669 | **+2.08 %\*** |
| | Throughput (packets) | 153,202 ± 2,951 | 156,526 ± 2,659 | **+2.17 %\*** |
| | Residual energy @ round 300 (J) | 59.76 ± 0.55 | 60.51 ± 0.53 | **+1.26 %\*** |
| | PDR | 0.9969 | 0.9978 | +0.09 % |

**Verdict:** of 24 paired scenario × metric comparisons, the proposed method is **significantly better in 18**,
significantly worse in 1 (FND in BP3, −1.16 %), and not significantly different in 5 (FND in BP1/BP2, PDR in
BP1/BP3, LND in BP3). In BP3 the last surviving nodes are free nodes next to the BS, which send directly and do not
depend on CH selection, so LND is identical for every centralised algorithm in every run.

### 9.3 Where the improvement comes from

* **Fewer, better-placed cluster heads.** With the BS 100–200 m away, every CH → BS packet is a multipath (d⁴)
  transmission. The proposed optimiser's binary encoding may use 5–15 % CHs and chooses about 5 per round in BP1
  (DEAI-PSO always uses 10): CH → BS energy up to round 300 falls by 44.5 % (2.81 J vs 5.07 J) while member → CH
  energy rises by 9.4 %, a net saving of 5.9 % (BP2: 6.5 %, BP3: 1.9 %).
* **Attribution study (BP1, 20 runs).** With the CH count fixed at exactly 10 % like DEAI-PSO, the hybrid still beats
  DEAI-PSO (node-rounds +0.44 %, FND +0.77 %, both unadjusted Wilcoxon p < 0.001): that is the better search alone.
  The remaining ≈ 6.3 points of the +6.72 % node-rounds gain come from the adaptive CH count.
* **Hybrid vs its components on Eq. 12:** better than ABC (Eq. 12) in HND, node-rounds and throughput in all three
  scenarios and in LND in BP1/BP2 (+0.3 % to +0.8 %, significant), but 0.22 % worse in FND in BP2 (significant);
  better than GWO (Eq. 12) only in node-rounds (+0.05 % to +0.09 %, significant), other differences not significant.
* **The project's multi-objective Hybrid vs DEAI-PSO** is mixed: significantly better HND (+0.75 % to +1.31 %),
  throughput (+0.51 % to +2.08 %) and PDR, but a significantly earlier FND in BP1 (−1.91 %) and BP3 (−3.73 %). Its
  energy term divides the round energy by a worst-case bound, which under-weights real d⁴ costs when the BS is far
  away; the base paper's Eq. 12 measures Joules directly. This is a lesson for the design of the project's fitness.

### 9.4 Cost and the published numbers

* **Runtime** (sequential, median ms per round, first 100 rounds): DEAI-PSO 14.7 / 31.4 / 38.0 ms vs Hybrid GWO-ABC
  (Eq. 12) 27.1 / 32.8 / 33.4 ms in BP1 / BP2 / BP3 — slower for 100 nodes (×1.84), similar for 160 (×1.05), faster
  for 200 (×0.88).
* **The paper's own Table 6 lifetimes (LND 3,400–4,756 rounds) cannot be reproduced by any simulator that uses its
  Table 3 parameters:** the transmitter electronics alone cost 4000 × 50 nJ = 0.2 mJ per packet, so a 0.5 J node can
  send at most 2,500 packets — no node can live beyond 2,500 rounds. Only the same-simulator comparison above is used
  to judge improvement; the published numbers are listed in the report for reference.
* **Limitations:** DEAI-PSO is a re-implementation (open details tuned in its favour); every method received the
  same evaluation budget instead of the paper's 36 × 5000; LEACH-FL, LEACH-FC and KM-PSO were not re-implemented;
  single-hop CH → BS links.

## 10. GUI

`python main.py` opens the dashboard:

* **Scenario preset:** project default (BS at the centre) or the base paper's three scenarios (with its control
  packets, free nodes and tuned DEAI-PSO settings).
* **Configuration panel:** nodes, area, initial energy, packet size, rounds, CH %, BS x/y, GWO population,
  ABC colony, iterations, seed.
* **Algorithm selection:** LEACH, GWO, ABC, Hybrid GWO-ABC, DEAI-PSO (base paper), Hybrid GWO-ABC on the base
  paper's objective, and the Random baseline.
* **Buttons:** Run, Pause/Resume, Stop, Reset (redeploys the network), Export Results
  (`results/gui_exports/<timestamp>/`: config, per-round history, summary, final node table, cluster-head log,
  figures).
* **Dashboard:** current round, alive/dead nodes, residual and consumed energy, CH count, packets generated and
  delivered, PDR, current fitness.
* **Tabs:** live network (normal nodes ●, CHs ▲, dead nodes ✕, BS ■, cluster links, optional CH→BS arrows, nodes
  shaded by residual energy), performance curves, the latest round's optimiser convergence, and *Compare all*
  (runs Random, LEACH, GWO, ABC, Hybrid GWO-ABC, DEAI-PSO and Hybrid GWO-ABC (Eq. 12) on the same network and
  tabulates FND/HND/LND, energy, throughput, PDR, runtime, fitness).

The simulation runs in a background thread, so the window stays responsive.

## 11. Validation (section 31 checklist → tests)

| Claim | Verified by |
|---|---|
| LEACH uses probabilistic threshold election, once per epoch | `test_leach_threshold_formula`, `test_leach_rotation_once_per_epoch`, `test_leach_is_probabilistic_and_ignores_dead` |
| GWO updates wolves from alpha/beta/delta | `test_gwo_leaders_are_alpha_beta_delta`, `test_gwo_wolves_follow_leaders_when_a_is_zero`, `test_gwo_converges` |
| ABC runs employed, onlooker and scout phases | `test_abc_phases`, `test_abc_scout_replaces_exhausted_source`, `test_abc_neighbours_valid` |
| Hybrid transfers solutions both ways | `test_hybrid_exchanges_information` (GWO→ABC), `test_hybrid_feedback_reaches_gwo` (ABC→GWO), `test_hybrid_budget_matches_standalone` |
| Fitness uses energy, distance and cluster factors; penalises invalid solutions | `tests/test_fitness.py` |
| Energy decreases due to communication (exact formulas) | `test_round_energy_accounting_exact`, `test_full_pipeline` |
| Nodes die at 0 J and never participate again | `test_node_death`, `test_dead_nodes_never_participate` |
| CH ids, residual energy, coordinates and CH–BS distance are recorded | `test_cluster_head_records` |
| Results originate from simulation data | `test_results_come_from_runs`, `test_full_pipeline`, `test_experiment_outputs` |
| Saved experiments are exactly reproducible | `test_reproducible`, `test_rerun_reproduces_saved_results` |
| Base paper's method re-implemented faithfully (Eq. 12, Eq. 13, TVAC, decoding, free nodes, 10 % CHs) | `tests/test_base_paper.py` (Eq. 12 against a hand calculation) |
| Every worked example in `docs/` matches the code (radio model, fitness example, GWO step, ABC probabilities, LEACH threshold, metrics, statistics) | `tests/test_docs_examples.py` |

## 12. Limitations

* Single-hop member→CH→BS topology, an ideal MAC (no collisions or retransmissions) and one packet per node per
  round, as in the LEACH literature.
* Runtime figures are wall-clock times in pure Python/NumPy. Experiments ran in 11 parallel processes, so absolute
  times are inflated and noisy; the convergence experiment (single process) and the fitness-evaluation counts give
  a cleaner cost comparison.
* The fitness weights and the eligibility rule are design choices; the sensitivity analysis shows how results
  change with them.
* The study compares four algorithms on synthetic uniform deployments; results may differ for clustered
  deployments, heterogeneous energy or multi-hop routing.
