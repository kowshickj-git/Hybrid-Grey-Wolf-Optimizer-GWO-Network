# Base paper BP2_160nodes

Scenario 2: 160 nodes, 100 x 100 m, BS (200, 50), 10 % CHs — base paper Table 3 conditions; DEAI-PSO = existing system; Hybrid GWO-ABC (Eq. 12) = proposed optimiser on the base paper's own objective; GWO/ABC (Eq. 12) = its components on the same objective; Hybrid GWO-ABC = proposed optimiser with the project's multi-objective fitness.

All numbers below were produced by the simulator in this folder (20 independent paired runs per algorithm; run r uses deployment/algorithm seed 42 + r). Raw per-run results: `runs_raw.csv`; per-round histories: `history_raw.csv.gz`; statistics: `statistics.csv`; proposed-vs-baseline tests: `improvement_vs_baselines.csv`.

## Configuration

| Parameter | Value |
|---|---|
| Nodes | 160 |
| Area (m) | 100 x 100 |
| BS position | (200, 50) |
| Initial energy (J/node) | 0.5 |
| Packet size (bits) | 4000 |
| Control packet (bits) | 200 |
| Max rounds | 3000 |
| CH percentage p | 0.1 |
| CH count tolerance | K_opt x (1 ± 0.5) |
| CH eligibility (optimisers) | E ≥ 1.0 x mean alive energy |
| Optimisation iterations / round | 30 |
| GWO population | 20 |
| ABC colony size (food sources) | 20 (10) |
| ABC abandonment limit | 10 |
| Hybrid budget share / transfer / feedback | 0.5 / 3 / True |
| Fitness weights w1..w5 | 0.3, 0.25, 0.2, 0.15, 0.1 |
| Radio E_elec / E_fs / E_mp / E_DA | 5e-08 / 1e-11 / 1.3e-15 / 5e-09 |
| Checkpoint round (energy / averages) | 300 |
| Base seed | 42 |

## Final result table (mean ± std over runs)

| Metric | LEACH | DEAI-PSO | GWO (Eq. 12) | ABC (Eq. 12) | Hybrid GWO-ABC (Eq. 12) | Hybrid GWO-ABC |
|---|---:|---:|---:|---:|---:|---:|
| FND (rounds) | 361 ± 6 | 635 ± 8 | 645 ± 18 | 647 ± 18 | 645 ± 18 | 636 ± 11 |
| HND (rounds) | 573 ± 16 | 659 ± 10 | 707 ± 10 | 702 ± 10 | 708 ± 10 | 668 ± 12 |
| LND (rounds) | 902 ± 13 | 695 ± 27 | 718 ± 10 | 713 ± 10 | 718 ± 11 | 687 ± 11 |
| Residual Energy (J) | 35.320 ± 0.649 | 43.392 ± 0.572 | 45.757 ± 0.445 | 45.569 ± 0.453 | 45.776 ± 0.454 | 43.589 ± 0.597 |
| Energy Consumption (J) | 44.680 ± 0.649 | 36.608 ± 0.572 | 34.243 ± 0.445 | 34.431 ± 0.453 | 34.224 ± 0.454 | 36.411 ± 0.597 |
| Throughput (packets) | 92,244 ± 1,310 | 104,428 ± 1,860 | 111,886 ± 1,597 | 111,108 ± 1,617 | 111,964 ± 1,594 | 106,600 ± 1,751 |
| PDR (ratio) | 0.9904 ± 0.0009 | 0.9906 ± 0.0023 | 0.9924 ± 0.0014 | 0.9914 ± 0.0014 | 0.9926 ± 0.0016 | 0.9977 ± 0.0003 |
| Avg. Cluster Distance (m) | 13.917 ± 0.261 | 20.364 ± 0.814 | 24.078 ± 0.812 | 23.824 ± 0.870 | 24.030 ± 0.799 | 20.480 ± 0.822 |
| Avg. CH-BS Distance (m) | 153.602 ± 1.651 | 124.275 ± 1.586 | 125.673 ± 1.422 | 124.463 ± 1.505 | 125.650 ± 1.468 | 126.118 ± 2.053 |
| Runtime (s) | 0.06 ± 0.01 | 77.35 ± 7.09 | 75.76 ± 4.28 | 91.25 ± 7.13 | 121.04 ± 13.47 | 114.28 ± 13.14 |
| Final Fitness (-) | 0.5505 ± 0.0839 | 0.3276 ± 0.0031 | 0.3476 ± 0.0065 | 0.3534 ± 0.0055 | 0.3453 ± 0.0061 | 0.3086 ± 0.0044 |

Residual energy and energy consumption are measured at the checkpoint round 300; distance, imbalance and fitness averages cover rounds 1–300. '≥' marks lifetime values where at least one run had not reached the event within 3000 rounds (the horizon is then used as a lower bound).

## Descriptive statistics

**FND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 20 | 361 | 6 | 348 | 374 |
| DEAI-PSO | 20 | 635 | 8 | 621 | 648 |
| GWO (Eq. 12) | 20 | 645 | 18 | 608 | 681 |
| ABC (Eq. 12) | 20 | 647 | 18 | 609 | 683 |
| Hybrid GWO-ABC (Eq. 12) | 20 | 645 | 18 | 609 | 682 |
| Hybrid GWO-ABC | 20 | 636 | 11 | 617 | 649 |

**HND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 20 | 573 | 16 | 547 | 602 |
| DEAI-PSO | 20 | 659 | 10 | 638 | 677 |
| GWO (Eq. 12) | 20 | 707 | 10 | 688 | 729 |
| ABC (Eq. 12) | 20 | 702 | 10 | 682 | 724 |
| Hybrid GWO-ABC (Eq. 12) | 20 | 708 | 10 | 687 | 728 |
| Hybrid GWO-ABC | 20 | 668 | 12 | 641 | 689 |

**LND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 20 | 902 | 13 | 885 | 927 |
| DEAI-PSO | 20 | 695 | 27 | 652 | 750 |
| GWO (Eq. 12) | 20 | 718 | 10 | 698 | 738 |
| ABC (Eq. 12) | 20 | 713 | 10 | 693 | 734 |
| Hybrid GWO-ABC (Eq. 12) | 20 | 718 | 11 | 698 | 738 |
| Hybrid GWO-ABC | 20 | 687 | 11 | 663 | 706 |

**Residual Energy (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 20 | 35.320 | 0.649 | 33.885 | 36.492 |
| DEAI-PSO | 20 | 43.392 | 0.572 | 42.189 | 44.435 |
| GWO (Eq. 12) | 20 | 45.757 | 0.445 | 44.777 | 46.604 |
| ABC (Eq. 12) | 20 | 45.569 | 0.453 | 44.568 | 46.401 |
| Hybrid GWO-ABC (Eq. 12) | 20 | 45.776 | 0.454 | 44.779 | 46.629 |
| Hybrid GWO-ABC | 20 | 43.589 | 0.597 | 42.290 | 44.694 |

**Energy Consumption (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 20 | 44.680 | 0.649 | 43.508 | 46.115 |
| DEAI-PSO | 20 | 36.608 | 0.572 | 35.565 | 37.811 |
| GWO (Eq. 12) | 20 | 34.243 | 0.445 | 33.396 | 35.223 |
| ABC (Eq. 12) | 20 | 34.431 | 0.453 | 33.599 | 35.432 |
| Hybrid GWO-ABC (Eq. 12) | 20 | 34.224 | 0.454 | 33.371 | 35.221 |
| Hybrid GWO-ABC | 20 | 36.411 | 0.597 | 35.306 | 37.710 |

**Throughput (packets)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 20 | 92,244 | 1,310 | 89,465 | 94,729 |
| DEAI-PSO | 20 | 104,428 | 1,860 | 100,716 | 107,855 |
| GWO (Eq. 12) | 20 | 111,886 | 1,597 | 108,702 | 115,117 |
| ABC (Eq. 12) | 20 | 111,108 | 1,617 | 107,697 | 114,290 |
| Hybrid GWO-ABC (Eq. 12) | 20 | 111,964 | 1,594 | 108,734 | 114,959 |
| Hybrid GWO-ABC | 20 | 106,600 | 1,751 | 102,701 | 109,940 |

**PDR (ratio)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 20 | 0.9904 | 0.0009 | 0.9881 | 0.9918 |
| DEAI-PSO | 20 | 0.9906 | 0.0023 | 0.9868 | 0.9955 |
| GWO (Eq. 12) | 20 | 0.9924 | 0.0014 | 0.9891 | 0.9944 |
| ABC (Eq. 12) | 20 | 0.9914 | 0.0014 | 0.9891 | 0.9943 |
| Hybrid GWO-ABC (Eq. 12) | 20 | 0.9926 | 0.0016 | 0.9891 | 0.9951 |
| Hybrid GWO-ABC | 20 | 0.9977 | 0.0003 | 0.9971 | 0.9981 |

**Runtime (s)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 20 | 0.06 | 0.01 | 0.04 | 0.09 |
| DEAI-PSO | 20 | 77.35 | 7.09 | 62.56 | 93.67 |
| GWO (Eq. 12) | 20 | 75.76 | 4.28 | 63.29 | 81.51 |
| ABC (Eq. 12) | 20 | 91.25 | 7.13 | 68.06 | 103.00 |
| Hybrid GWO-ABC (Eq. 12) | 20 | 121.04 | 13.47 | 73.59 | 138.56 |
| Hybrid GWO-ABC | 20 | 114.28 | 13.14 | 67.61 | 126.00 |

## Hybrid GWO-ABC (Eq. 12) vs baselines

Improvement % uses ((P − B) / B) × 100 for higher-is-better metrics and ((B − P) / B) × 100 for lower-is-better metrics, so a positive value always means the proposed algorithm did better. p-values: paired two-sided Wilcoxon signed-rank test, Holm-corrected over the baselines. Cliff's δ > 0 favours the proposed algorithm (|δ| < 0.147 negligible, < 0.33 small, < 0.474 medium, otherwise large).

| Metric | Baseline | Better | Improvement % | p (Holm) | Cliff's δ | Effect | Verdict |
|---|---|---|---:|---:|---:|---|---|
| FND | LEACH | higher | +78.53 | 0.000395 | +1.00 | large | proposed better |
| FND | DEAI-PSO | higher | +1.53 | 0.0996 | +0.45 | medium | no significant difference |
| FND | GWO (Eq. 12) | higher | +0.06 | 0.0996 | +0.03 | negligible | no significant difference |
| FND | ABC (Eq. 12) | higher | -0.22 | 0.000395 | -0.08 | negligible | proposed worse |
| FND | Hybrid GWO-ABC | higher | +1.42 | 0.0996 | +0.37 | medium | no significant difference |
| HND | LEACH | higher | +23.42 | 0.000356 | +1.00 | large | proposed better |
| HND | DEAI-PSO | higher | +7.39 | 0.000356 | +1.00 | large | proposed better |
| HND | GWO (Eq. 12) | higher | +0.04 | 0.312 | +0.02 | negligible | no significant difference |
| HND | ABC (Eq. 12) | higher | +0.75 | 0.000356 | +0.34 | medium | proposed better |
| HND | Hybrid GWO-ABC | higher | +6.01 | 0.000356 | +0.99 | large | proposed better |
| LND | LEACH | higher | -20.42 | 0.000392 | -1.00 | large | proposed worse |
| LND | DEAI-PSO | higher | +3.27 | 0.00118 | +0.60 | large | proposed better |
| LND | GWO (Eq. 12) | higher | +0.03 | 0.194 | +0.04 | negligible | no significant difference |
| LND | ABC (Eq. 12) | higher | +0.67 | 0.000392 | +0.28 | small | proposed better |
| LND | Hybrid GWO-ABC | higher | +4.44 | 0.000392 | +0.97 | large | proposed better |
| Node-rounds | LEACH | higher | +21.14 | 9.54e-06 | +1.00 | large | proposed better |
| Node-rounds | DEAI-PSO | higher | +7.02 | 9.54e-06 | +1.00 | large | proposed better |
| Node-rounds | GWO (Eq. 12) | higher | +0.05 | 0.000253 | +0.07 | negligible | proposed better |
| Node-rounds | ABC (Eq. 12) | higher | +0.65 | 9.54e-06 | +0.29 | small | proposed better |
| Node-rounds | Hybrid GWO-ABC | higher | +5.58 | 9.54e-06 | +0.99 | large | proposed better |
| Residual Energy | LEACH | higher | +29.60 | 9.54e-06 | +1.00 | large | proposed better |
| Residual Energy | DEAI-PSO | higher | +5.49 | 9.54e-06 | +1.00 | large | proposed better |
| Residual Energy | GWO (Eq. 12) | higher | +0.04 | 0.000395 | +0.06 | negligible | proposed better |
| Residual Energy | ABC (Eq. 12) | higher | +0.45 | 9.54e-06 | +0.31 | small | proposed better |
| Residual Energy | Hybrid GWO-ABC | higher | +5.02 | 9.54e-06 | +1.00 | large | proposed better |
| Energy Consumption | LEACH | lower | +23.40 | 9.54e-06 | +1.00 | large | proposed better |
| Energy Consumption | DEAI-PSO | lower | +6.51 | 9.54e-06 | +1.00 | large | proposed better |
| Energy Consumption | GWO (Eq. 12) | lower | +0.06 | 0.000395 | +0.06 | negligible | proposed better |
| Energy Consumption | ABC (Eq. 12) | lower | +0.60 | 9.54e-06 | +0.31 | small | proposed better |
| Energy Consumption | Hybrid GWO-ABC | lower | +6.01 | 9.54e-06 | +1.00 | large | proposed better |
| Throughput | LEACH | higher | +21.38 | 9.54e-06 | +1.00 | large | proposed better |
| Throughput | DEAI-PSO | higher | +7.22 | 0.000177 | +1.00 | large | proposed better |
| Throughput | GWO (Eq. 12) | higher | +0.07 | 0.151 | +0.04 | negligible | no significant difference |
| Throughput | ABC (Eq. 12) | higher | +0.77 | 9.54e-06 | +0.32 | small | proposed better |
| Throughput | Hybrid GWO-ABC | higher | +5.03 | 9.54e-06 | +0.98 | large | proposed better |
| PDR | LEACH | higher | +0.22 | 0.00105 | +0.78 | large | proposed better |
| PDR | DEAI-PSO | higher | +0.20 | 0.00363 | +0.54 | large | proposed better |
| PDR | GWO (Eq. 12) | higher | +0.02 | 0.869 | +0.09 | negligible | no significant difference |
| PDR | ABC (Eq. 12) | higher | +0.12 | 0.0214 | +0.47 | medium | proposed better |
| PDR | Hybrid GWO-ABC | higher | -0.52 | 9.54e-06 | -1.00 | large | proposed worse |
| Avg. Cluster Distance | LEACH | lower | -72.67 | 9.54e-06 | -1.00 | large | proposed worse |
| Avg. Cluster Distance | DEAI-PSO | lower | -18.00 | 9.54e-06 | -1.00 | large | proposed worse |
| Avg. Cluster Distance | GWO (Eq. 12) | lower | +0.20 | 0.0362 | +0.04 | negligible | proposed better |
| Avg. Cluster Distance | ABC (Eq. 12) | lower | -0.86 | 9.54e-06 | -0.18 | small | proposed worse |
| Avg. Cluster Distance | Hybrid GWO-ABC | lower | -17.34 | 9.54e-06 | -0.99 | large | proposed worse |
| Avg. CH-BS Distance | LEACH | lower | +18.20 | 9.54e-06 | +1.00 | large | proposed better |
| Avg. CH-BS Distance | DEAI-PSO | lower | -1.11 | 9.54e-06 | -0.50 | large | proposed worse |
| Avg. CH-BS Distance | GWO (Eq. 12) | lower | +0.02 | 0.648 | +0.01 | negligible | no significant difference |
| Avg. CH-BS Distance | ABC (Eq. 12) | lower | -0.95 | 9.54e-06 | -0.45 | medium | proposed worse |
| Avg. CH-BS Distance | Hybrid GWO-ABC | lower | +0.37 | 0.0272 | +0.10 | negligible | proposed better |
| Final Fitness | LEACH | lower | +37.27 | 9.54e-06 | +1.00 | large | proposed better |
| Final Fitness | DEAI-PSO | lower | -5.41 | 9.54e-06 | -1.00 | large | proposed worse |
| Final Fitness | GWO (Eq. 12) | lower | +0.64 | 9.54e-06 | +0.20 | small | proposed better |
| Final Fitness | ABC (Eq. 12) | lower | +2.28 | 9.54e-06 | +0.66 | large | proposed better |
| Final Fitness | Hybrid GWO-ABC | lower | -11.90 | 9.54e-06 | -1.00 | large | proposed worse |
| Runtime | LEACH | lower | -212053.91 | 9.54e-06 | -1.00 | large | proposed worse |
| Runtime | DEAI-PSO | lower | -56.48 | 9.54e-06 | -0.93 | large | proposed worse |
| Runtime | GWO (Eq. 12) | lower | -59.76 | 9.54e-06 | -0.93 | large | proposed worse |
| Runtime | ABC (Eq. 12) | lower | -32.65 | 9.54e-06 | -0.91 | large | proposed worse |
| Runtime | Hybrid GWO-ABC | lower | -5.91 | 9.54e-06 | -0.48 | large | proposed worse |

### Trade-offs

- **Hybrid GWO-ABC (Eq. 12) vs LEACH** — significantly better: FND (+78.53%), HND (+23.42%), Node-rounds (+21.14%), Residual Energy (+29.60%), Energy Consumption (+23.40%), Throughput (+21.38%), PDR (+0.22%, < 1%: practically negligible), Avg. CH-BS Distance (+18.20%), Final Fitness (+37.27%); significantly worse: LND (-20.42%), Avg. Cluster Distance (-72.67%), Cluster Imbalance (-37.48%), Runtime (-212053.91%), Runtime / round (-266507.63%); no significant difference: Fitness Evaluations.
- **Hybrid GWO-ABC (Eq. 12) vs DEAI-PSO** — significantly better: HND (+7.39%), LND (+3.27%), Node-rounds (+7.02%), Residual Energy (+5.49%), Energy Consumption (+6.51%), Throughput (+7.22%), PDR (+0.20%, < 1%: practically negligible), Cluster Imbalance (+36.89%); significantly worse: Avg. Cluster Distance (-18.00%), Avg. CH-BS Distance (-1.11%), Final Fitness (-5.41%), Runtime (-56.48%), Runtime / round (-51.18%); no significant difference: FND, Fitness Evaluations.
- **Hybrid GWO-ABC (Eq. 12) vs GWO (Eq. 12)** — significantly better: Node-rounds (+0.05%, < 1%: practically negligible), Residual Energy (+0.04%, < 1%: practically negligible), Energy Consumption (+0.06%, < 1%: practically negligible), Avg. Cluster Distance (+0.20%, < 1%: practically negligible), Cluster Imbalance (+1.98%), Final Fitness (+0.64%, < 1%: practically negligible), Fitness Evaluations (+0.06%, < 1%: practically negligible); significantly worse: Runtime (-59.76%), Runtime / round (-59.76%); no significant difference: FND, HND, LND, Throughput, PDR, Avg. CH-BS Distance.
- **Hybrid GWO-ABC (Eq. 12) vs ABC (Eq. 12)** — significantly better: HND (+0.75%, < 1%: practically negligible), LND (+0.67%, < 1%: practically negligible), Node-rounds (+0.65%, < 1%: practically negligible), Residual Energy (+0.45%, < 1%: practically negligible), Energy Consumption (+0.60%, < 1%: practically negligible), Throughput (+0.77%, < 1%: practically negligible), PDR (+0.12%, < 1%: practically negligible), Cluster Imbalance (+15.46%), Final Fitness (+2.28%); significantly worse: FND (-0.22%, < 1%: practically negligible), Avg. Cluster Distance (-0.86%, < 1%: practically negligible), Avg. CH-BS Distance (-0.95%, < 1%: practically negligible), Runtime (-32.65%), Runtime / round (-31.78%), Fitness Evaluations (-1.86%); no significant difference: none.
- **Hybrid GWO-ABC (Eq. 12) vs Hybrid GWO-ABC** — significantly better: HND (+6.01%), LND (+4.44%), Node-rounds (+5.58%), Residual Energy (+5.02%), Energy Consumption (+6.01%), Throughput (+5.03%), Avg. CH-BS Distance (+0.37%, < 1%: practically negligible), Cluster Imbalance (+29.77%); significantly worse: PDR (-0.52%, < 1%: practically negligible), Avg. Cluster Distance (-17.34%), Final Fitness (-11.90%), Runtime (-5.91%), Runtime / round (-1.42%), Fitness Evaluations (-4.71%); no significant difference: FND.

## Figures

### Initial WSN topology (run 0; every algorithm uses this same network in run 0).

![Initial WSN topology (run 0; every algorithm uses this same network in run 0).](01_topology.png)

**Observed:** 160 nodes uniformly deployed in 100 x 100 m (seed 42); BS at (200, 50). Mean node–BS distance 156.1 m (max 202.0 m); d0 = 87.7 m, so 100% of nodes would use the multipath (d^4) model for a direct BS transmission.

### LEACH: cluster heads selected in round 1 (run 0).

![LEACH: cluster heads selected in round 1 (run 0).](02_ch_selection_LEACH.png)

**Observed:** 15 CHs; mean CH–BS distance 159.4 m.

### LEACH: cluster formation in round 1 (members joined the nearest CH).

![LEACH: cluster formation in round 1 (members joined the nearest CH).](03_clusters_LEACH.png)

**Observed:** 15 clusters, sizes 5–23 (CV 0.47); member→CH distance mean 13.2 m, max 38.9 m.

### LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_LEACH.png)

**Observed:** Round 555: 80 dead, 80 alive. Mean distance to BS — dead nodes 180.3 m, alive nodes 131.8 m (far nodes died first on average).

### DEAI-PSO: cluster heads selected in round 1 (run 0).

![DEAI-PSO: cluster heads selected in round 1 (run 0).](02_ch_selection_DEAI-PSO.png)

**Observed:** 16 CHs; mean CH–BS distance 130.2 m.

### DEAI-PSO: cluster formation in round 1 (members joined the nearest CH).

![DEAI-PSO: cluster formation in round 1 (members joined the nearest CH).](03_clusters_DEAI-PSO.png)

**Observed:** 16 clusters, sizes 1–30 (CV 0.88); member→CH distance mean 23.3 m, max 57.1 m.

### DEAI-PSO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![DEAI-PSO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_DEAI-PSO.png)

**Observed:** Round 643: 83 dead, 77 alive. Mean distance to BS — dead nodes 162.6 m, alive nodes 148.9 m (far nodes died first on average).

### GWO (Eq. 12): cluster heads selected in round 1 (run 0).

![GWO (Eq. 12): cluster heads selected in round 1 (run 0).](02_ch_selection_GWO_(Eq._12).png)

**Observed:** 10 CHs; mean CH–BS distance 133.3 m.

### GWO (Eq. 12): cluster formation in round 1 (members joined the nearest CH).

![GWO (Eq. 12): cluster formation in round 1 (members joined the nearest CH).](03_clusters_GWO_(Eq._12).png)

**Observed:** 10 clusters, sizes 7–29 (CV 0.48); member→CH distance mean 21.5 m, max 56.0 m.

### GWO (Eq. 12): network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![GWO (Eq. 12): network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_GWO_(Eq._12).png)

**Observed:** Round 691: 83 dead, 77 alive. Mean distance to BS — dead nodes 166.8 m, alive nodes 144.4 m (far nodes died first on average).

### ABC (Eq. 12): cluster heads selected in round 1 (run 0).

![ABC (Eq. 12): cluster heads selected in round 1 (run 0).](02_ch_selection_ABC_(Eq._12).png)

**Observed:** 9 CHs; mean CH–BS distance 132.6 m.

### ABC (Eq. 12): cluster formation in round 1 (members joined the nearest CH).

![ABC (Eq. 12): cluster formation in round 1 (members joined the nearest CH).](03_clusters_ABC_(Eq._12).png)

**Observed:** 9 clusters, sizes 7–32 (CV 0.51); member→CH distance mean 24.4 m, max 65.1 m.

### ABC (Eq. 12): network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![ABC (Eq. 12): network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_ABC_(Eq._12).png)

**Observed:** Round 686: 81 dead, 79 alive. Mean distance to BS — dead nodes 165.1 m, alive nodes 146.7 m (far nodes died first on average).

### Hybrid GWO-ABC (Eq. 12): cluster heads selected in round 1 (run 0).

![Hybrid GWO-ABC (Eq. 12): cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_GWO-ABC_(Eq._12).png)

**Observed:** 9 CHs; mean CH–BS distance 129.9 m.

### Hybrid GWO-ABC (Eq. 12): cluster formation in round 1 (members joined the nearest CH).

![Hybrid GWO-ABC (Eq. 12): cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_GWO-ABC_(Eq._12).png)

**Observed:** 9 clusters, sizes 8–34 (CV 0.54); member→CH distance mean 25.4 m, max 66.5 m.

### Hybrid GWO-ABC (Eq. 12): data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).

![Hybrid GWO-ABC (Eq. 12): data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).](04_communication_Hybrid_GWO-ABC_(Eq._12).png)

**Observed:** 9 clusters, sizes 8–34 (CV 0.54); member→CH distance mean 25.4 m, max 66.5 m.

### Hybrid GWO-ABC (Eq. 12): network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid GWO-ABC (Eq. 12): network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_GWO-ABC_(Eq._12).png)

**Observed:** Round 692: 84 dead, 76 alive. Mean distance to BS — dead nodes 165.3 m, alive nodes 145.8 m (far nodes died first on average).

### Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).

![Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_GWO-ABC.png)

**Observed:** 16 CHs; mean CH–BS distance 152.9 m.

### Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).

![Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_GWO-ABC.png)

**Observed:** 16 clusters, sizes 7–13 (CV 0.15); member→CH distance mean 11.2 m, max 28.1 m.

### Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_GWO-ABC.png)

**Observed:** Round 651: 81 dead, 79 alive. Mean distance to BS — dead nodes 176.6 m, alive nodes 135.0 m (far nodes died first on average).

### DEAI-PSO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![DEAI-PSO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_DEAI-PSO.png)

**Observed:** mean best fitness 0.1322 → 0.1177 (11.0% lower); 95% of the improvement reached by iteration 14

### GWO (Eq. 12): best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![GWO (Eq. 12): best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_GWO_(Eq._12).png)

**Observed:** mean best fitness 0.1287 → 0.1117 (13.2% lower); 95% of the improvement reached by iteration 14

### ABC (Eq. 12): best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![ABC (Eq. 12): best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_ABC_(Eq._12).png)

**Observed:** mean best fitness 0.1299 → 0.1137 (12.5% lower); 95% of the improvement reached by iteration 26

### Hybrid GWO-ABC (Eq. 12): best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid GWO-ABC (Eq. 12): best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_GWO-ABC_(Eq._12).png)

**Observed:** GWO: mean best fitness 0.1299 → 0.1106 (14.9% lower); 95% of the improvement reached by iteration 17; ABC: mean best fitness 0.1351 → 0.1106 (18.1% lower); 95% of the improvement reached by iteration 15; HYBRID: mean best fitness 0.1273 → 0.1106 (13.1% lower); 95% of the improvement reached by iteration 18

### Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_GWO-ABC.png)

**Observed:** GWO: mean best fitness 0.2609 → 0.2047 (21.5% lower); 95% of the improvement reached by iteration 23; ABC: mean best fitness 0.2722 → 0.2047 (24.8% lower); 95% of the improvement reached by iteration 22; HYBRID: mean best fitness 0.2574 → 0.2047 (20.5% lower); 95% of the improvement reached by iteration 23

### Alive nodes vs rounds.

![Alive nodes vs rounds.](09_alive_vs_rounds.png)

**Observed:** LEACH: FND 361, HND 573, LND 902; DEAI-PSO: FND 635, HND 659, LND 695; GWO (Eq. 12): FND 645, HND 707, LND 718; ABC (Eq. 12): FND 647, HND 702, LND 713; Hybrid GWO-ABC (Eq. 12): FND 645, HND 708, LND 718; Hybrid GWO-ABC: FND 636, HND 668, LND 687

### Dead nodes vs rounds.

![Dead nodes vs rounds.](10_dead_vs_rounds.png)

**Observed:** Mirror image of the alive-nodes curve; a steeper rise means nodes die closer together.

### Residual energy vs rounds.

![Residual energy vs rounds.](11_residual_energy_vs_rounds.png)

**Observed:** Residual energy at round 300: LEACH 35.32 J; DEAI-PSO 43.39 J; GWO (Eq. 12) 45.76 J; ABC (Eq. 12) 45.57 J; Hybrid GWO-ABC (Eq. 12) 45.78 J; Hybrid GWO-ABC 43.59 J

### Energy consumption vs rounds.

![Energy consumption vs rounds.](12_consumed_energy_vs_rounds.png)

**Observed:** Consumed by round 300: LEACH 44.68 J; DEAI-PSO 36.61 J; GWO (Eq. 12) 34.24 J; ABC (Eq. 12) 34.43 J; Hybrid GWO-ABC (Eq. 12) 34.22 J; Hybrid GWO-ABC 36.41 J

### Throughput vs rounds (cumulative).

![Throughput vs rounds (cumulative).](13_packets_delivered_vs_rounds.png)

**Observed:** Total delivered: LEACH 92,244; DEAI-PSO 104,428; GWO (Eq. 12) 111,886; ABC (Eq. 12) 111,108; Hybrid GWO-ABC (Eq. 12) 111,964; Hybrid GWO-ABC 106,600

### PDR vs rounds.

![PDR vs rounds.](14_pdr_vs_rounds.png)

**Observed:** Final PDR: LEACH 0.9904; DEAI-PSO 0.9906; GWO (Eq. 12) 0.9924; ABC (Eq. 12) 0.9914; Hybrid GWO-ABC (Eq. 12) 0.9926; Hybrid GWO-ABC 0.9977

### CH count vs rounds (20-round rolling mean).

![CH count vs rounds (20-round rolling mean).](15_ch_count_vs_rounds.png)

**Observed:** Mean CHs/round (rounds 1–300): LEACH 16.00 (per-round std 3.81); DEAI-PSO 16.00 (per-round std 0.00); GWO (Eq. 12) 8.06 (per-round std 0.26); ABC (Eq. 12) 9.12 (per-round std 1.46); Hybrid GWO-ABC (Eq. 12) 8.02 (per-round std 0.16); Hybrid GWO-ABC 14.49 (per-round std 2.88)

### Average cluster distance vs rounds (20-round rolling mean).

![Average cluster distance vs rounds (20-round rolling mean).](16_avg_intra_distance_vs_rounds.png)

**Observed:** Mean member→CH distance: LEACH 13.92 m; DEAI-PSO 20.36 m; GWO (Eq. 12) 24.08 m; ABC (Eq. 12) 23.82 m; Hybrid GWO-ABC (Eq. 12) 24.03 m; Hybrid GWO-ABC 20.48 m

### Total CH-selection runtime per simulation (log scale, mean ± std).

![Total CH-selection runtime per simulation (log scale, mean ± std).](17_runtime.png)

**Observed:** LEACH 0.06 s (0.06 ms/round, 0 fitness evaluations); DEAI-PSO 77.35 s (111.61 ms/round, 450,457 fitness evaluations); GWO (Eq. 12) 75.76 s (105.61 ms/round, 444,974 fitness evaluations); ABC (Eq. 12) 91.25 s (128.04 ms/round, 436,576 fitness evaluations); Hybrid GWO-ABC (Eq. 12) 121.04 s (168.73 ms/round, 444,687 fitness evaluations); Hybrid GWO-ABC 114.28 s (166.36 ms/round, 424,695 fitness evaluations)

### FND / HND / LND comparison (mean ± std over runs).

![FND / HND / LND comparison (mean ± std over runs).](18_lifetime_fnd_hnd_lnd.png)

**Observed:** LEACH: FND 361, HND 573, LND 902; DEAI-PSO: FND 635, HND 659, LND 695; GWO (Eq. 12): FND 645, HND 707, LND 718; ABC (Eq. 12): FND 647, HND 702, LND 713; Hybrid GWO-ABC (Eq. 12): FND 645, HND 708, LND 718; Hybrid GWO-ABC: FND 636, HND 668, LND 687

### Where the energy goes: mean energy per radio activity over rounds 1–300.

![Where the energy goes: mean energy per radio activity over rounds 1–300.](19_energy_breakdown.png)

**Observed:** LEACH: total 36.38 J, largest share CH→BS TX (49%); DEAI-PSO: total 27.29 J, largest share member TX (35%); GWO (Eq. 12): total 24.92 J, largest share member TX (43%); ABC (Eq. 12): total 25.11 J, largest share member TX (42%); Hybrid GWO-ABC (Eq. 12): total 24.90 J, largest share member TX (43%); Hybrid GWO-ABC: total 27.09 J, largest share member TX (36%)

### Final fitness: same objective and weights for every algorithm.

![Final fitness: same objective and weights for every algorithm.](20_final_fitness.png)

**Observed:** LEACH 0.5505; DEAI-PSO 0.3276; GWO (Eq. 12) 0.3476; ABC (Eq. 12) 0.3534; Hybrid GWO-ABC (Eq. 12) 0.3453; Hybrid GWO-ABC 0.3086

## Metric-by-metric interpretation

#### FND
- **What it represents:** First Node Death: the round in which the first node's residual energy reached 0.
- **How it was calculated:** min over nodes of the round in which residual energy reached 0 (simulation horizon if none died). (higher is better, unit: rounds)
- **Why it matters:** Marks the end of the stability period, during which every sensor still reports.
- **Observed (mean ± std over runs):** LEACH 361 (± 6), DEAI-PSO 635 (± 8), GWO (Eq. 12) 645 (± 18), ABC (Eq. 12) 647 (± 18), Hybrid GWO-ABC (Eq. 12) 645 (± 18), Hybrid GWO-ABC 636 (± 11). Best mean: **ABC (Eq. 12)**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 78.53% better (improvement formula), p = 0.000395 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 1.53% better (improvement formula), p = 0.0996 (Holm), Cliff's δ = +0.45 (medium) → **no significant difference**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.06% better (improvement formula), p = 0.0996 (Holm), Cliff's δ = +0.03 (negligible) → **no significant difference** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.22% worse (improvement formula), p = 0.000395 (Holm), Cliff's δ = -0.08 (negligible) → **proposed worse** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 1.42% better (improvement formula), p = 0.0996 (Holm), Cliff's δ = +0.37 (medium) → **no significant difference**.
- **Is the difference meaningful?** 2 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** CH selection that avoids low-energy nodes and rotates the CH role evenly delays the first death; a node chosen repeatedly as CH (e.g. because it is close to the BS) dies early. Measured LND − FND spread (rounds): LEACH 541, DEAI-PSO 60, GWO (Eq. 12) 73, ABC (Eq. 12) 66, Hybrid GWO-ABC (Eq. 12) 73, Hybrid GWO-ABC 51.

#### HND
- **What it represents:** Half Node Death: the round in which at least 50% of the nodes were dead.
- **How it was calculated:** round in which the number of dead nodes reached ceil(N/2). (higher is better, unit: rounds)
- **Why it matters:** Indicates how long the network keeps useful coverage.
- **Observed (mean ± std over runs):** LEACH 573 (± 16), DEAI-PSO 659 (± 10), GWO (Eq. 12) 707 (± 10), ABC (Eq. 12) 702 (± 10), Hybrid GWO-ABC (Eq. 12) 708 (± 10), Hybrid GWO-ABC 668 (± 12). Best mean: **Hybrid GWO-ABC (Eq. 12)**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 23.42% better (improvement formula), p = 0.000356 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 7.39% better (improvement formula), p = 0.000356 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.04% better (improvement formula), p = 0.312 (Holm), Cliff's δ = +0.02 (negligible) → **no significant difference** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.75% better (improvement formula), p = 0.000356 (Holm), Cliff's δ = +0.34 (medium) → **proposed better** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 6.01% better (improvement formula), p = 0.000356 (Holm), Cliff's δ = +0.99 (large) → **proposed better**.
- **Is the difference meaningful?** 4 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** HND reflects how evenly energy is drained across the whole network.

#### LND
- **What it represents:** Last Node Death: the round in which the last alive node died.
- **How it was calculated:** round in which the last node died (simulation horizon if nodes were still alive). (higher is better, unit: rounds)
- **Why it matters:** Upper bound of the network lifetime.
- **Observed (mean ± std over runs):** LEACH 902 (± 13), DEAI-PSO 695 (± 27), GWO (Eq. 12) 718 (± 10), ABC (Eq. 12) 713 (± 10), Hybrid GWO-ABC (Eq. 12) 718 (± 11), Hybrid GWO-ABC 687 (± 11). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 20.42% worse (improvement formula), p = 0.000392 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 3.27% better (improvement formula), p = 0.00118 (Holm), Cliff's δ = +0.60 (large) → **proposed better**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.03% better (improvement formula), p = 0.194 (Holm), Cliff's δ = +0.04 (negligible) → **no significant difference** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.67% better (improvement formula), p = 0.000392 (Holm), Cliff's δ = +0.28 (small) → **proposed better** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 4.44% better (improvement formula), p = 0.000392 (Holm), Cliff's δ = +0.97 (large) → **proposed better**.
- **Is the difference meaningful?** 4 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** A very even energy drain makes all nodes die at nearly the same time: FND is delayed but the last node also dies sooner. Uneven drain leaves a few nodes with spare energy that keep running. Measured LND − FND spread (rounds): LEACH 541, DEAI-PSO 60, GWO (Eq. 12) 73, ABC (Eq. 12) 66, Hybrid GWO-ABC (Eq. 12) 73, Hybrid GWO-ABC 51.

#### Residual Energy
- **What it represents:** Total residual energy of all nodes at the checkpoint round.
- **How it was calculated:** sum of node residual energies after the checkpoint round. (higher is better, unit: J)
- **Why it matters:** More energy left at the same round means cheaper operation.
- **Observed (mean ± std over runs):** LEACH 35.320 (± 0.649), DEAI-PSO 43.392 (± 0.572), GWO (Eq. 12) 45.757 (± 0.445), ABC (Eq. 12) 45.569 (± 0.453), Hybrid GWO-ABC (Eq. 12) 45.776 (± 0.454), Hybrid GWO-ABC 43.589 (± 0.597). Best mean: **Hybrid GWO-ABC (Eq. 12)**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 29.60% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 5.49% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.04% better (improvement formula), p = 0.000395 (Holm), Cliff's δ = +0.06 (negligible) → **proposed better** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.45% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +0.31 (small) → **proposed better** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 5.02% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**.
- **Is the difference meaningful?** 5 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Residual energy at a fixed round depends on per-round radio cost: shorter member->CH links and shorter or fewer CH->BS links consume less.

#### Energy Consumption
- **What it represents:** Initial total energy minus residual energy at the checkpoint round.
- **How it was calculated:** N * E0 - residual energy at the checkpoint round. (lower is better, unit: J)
- **Why it matters:** Energy spent to operate the network for the same number of rounds.
- **Observed (mean ± std over runs):** LEACH 44.680 (± 0.649), DEAI-PSO 36.608 (± 0.572), GWO (Eq. 12) 34.243 (± 0.445), ABC (Eq. 12) 34.431 (± 0.453), Hybrid GWO-ABC (Eq. 12) 34.224 (± 0.454), Hybrid GWO-ABC 36.411 (± 0.597). Best mean: **Hybrid GWO-ABC (Eq. 12)**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 23.40% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 6.51% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.06% better (reduction formula), p = 0.000395 (Holm), Cliff's δ = +0.06 (negligible) → **proposed better** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.60% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +0.31 (small) → **proposed better** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 6.01% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**.
- **Is the difference meaningful?** 5 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Consumption is the complement of residual energy at the same checkpoint.

#### Throughput
- **What it represents:** Total sensor data packets delivered to the BS over the whole simulation (directly or inside an aggregated CH packet).
- **How it was calculated:** count of sensor readings that reached the BS over the whole run. (higher is better, unit: packets)
- **Why it matters:** Amount of sensed data the application actually receives.
- **Observed (mean ± std over runs):** LEACH 92,244 (± 1,310), DEAI-PSO 104,428 (± 1,860), GWO (Eq. 12) 111,886 (± 1,597), ABC (Eq. 12) 111,108 (± 1,617), Hybrid GWO-ABC (Eq. 12) 111,964 (± 1,594), Hybrid GWO-ABC 106,600 (± 1,751). Best mean: **Hybrid GWO-ABC (Eq. 12)**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 21.38% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 7.22% better (improvement formula), p = 0.000177 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.07% better (improvement formula), p = 0.151 (Holm), Cliff's δ = +0.04 (negligible) → **no significant difference** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.77% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +0.32 (small) → **proposed better** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 5.03% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +0.98 (large) → **proposed better**.
- **Is the difference meaningful?** 4 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Throughput grows with the number of rounds in which nodes are alive and with the share of packets that are not lost to CHs dying mid-round.

#### PDR
- **What it represents:** Packet Delivery Ratio = delivered data packets / generated data packets.
- **How it was calculated:** delivered readings / generated readings over the whole run. (higher is better, unit: ratio)
- **Why it matters:** Reliability: share of generated readings that reach the BS.
- **Observed (mean ± std over runs):** LEACH 0.9904 (± 0.0009), DEAI-PSO 0.9906 (± 0.0023), GWO (Eq. 12) 0.9924 (± 0.0014), ABC (Eq. 12) 0.9914 (± 0.0014), Hybrid GWO-ABC (Eq. 12) 0.9926 (± 0.0016), Hybrid GWO-ABC 0.9977 (± 0.0003). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 0.22% better (improvement formula), p = 0.00105 (Holm), Cliff's δ = +0.78 (large) → **proposed better** — practically small; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 0.20% better (improvement formula), p = 0.00363 (Holm), Cliff's δ = +0.54 (large) → **proposed better** — practically small; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.02% better (improvement formula), p = 0.869 (Holm), Cliff's δ = +0.09 (negligible) → **no significant difference** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.12% better (improvement formula), p = 0.0214 (Holm), Cliff's δ = +0.47 (medium) → **proposed better** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 0.52% worse (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse** — practically small.
- **Is the difference meaningful?** 4 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Packets are lost when a CH runs out of energy before forwarding its cluster's data, or when a node dies while transmitting. Energy-feasibility checks on CHs reduce such losses.

#### Avg. Cluster Distance
- **What it represents:** Mean member->CH distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean member->CH distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** Shorter intra-cluster links cost less transmission energy (d^2 / d^4).
- **Observed (mean ± std over runs):** LEACH 13.917 (± 0.261), DEAI-PSO 20.364 (± 0.814), GWO (Eq. 12) 24.078 (± 0.812), ABC (Eq. 12) 23.824 (± 0.870), Hybrid GWO-ABC (Eq. 12) 24.030 (± 0.799), Hybrid GWO-ABC 20.480 (± 0.822). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 72.67% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 18.00% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.20% better (reduction formula), p = 0.0362 (Holm), Cliff's δ = +0.04 (negligible) → **proposed better** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.86% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -0.18 (small) → **proposed worse** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 17.34% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -0.99 (large) → **proposed worse**.
- **Is the difference meaningful?** 5 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness function explicitly penalises member->CH distance; LEACH places CHs at random positions, which typically lengthens member links.

#### Avg. CH-BS Distance
- **What it represents:** Mean CH->BS distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean CH->BS distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** CH->BS is the longest and most expensive hop.
- **Observed (mean ± std over runs):** LEACH 153.602 (± 1.651), DEAI-PSO 124.275 (± 1.586), GWO (Eq. 12) 125.673 (± 1.422), ABC (Eq. 12) 124.463 (± 1.505), Hybrid GWO-ABC (Eq. 12) 125.650 (± 1.468), Hybrid GWO-ABC 126.118 (± 2.053). Best mean: **DEAI-PSO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 18.20% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 1.11% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -0.50 (large) → **proposed worse**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.02% better (reduction formula), p = 0.648 (Holm), Cliff's δ = +0.01 (negligible) → **no significant difference** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.95% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -0.45 (medium) → **proposed worse** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 0.37% better (reduction formula), p = 0.0272 (Holm), Cliff's δ = +0.10 (negligible) → **proposed better** — practically small.
- **Is the difference meaningful?** 4 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises CH->BS distance, but the energy-eligibility rule and the energy term limit how often nodes near the BS can be selected.

#### Runtime
- **What it represents:** Total wall-clock time spent selecting CHs over the whole simulation.
- **How it was calculated:** sum of wall-clock CH-selection time over all rounds (time.perf_counter). (lower is better, unit: s)
- **Why it matters:** Computational cost of the CH selection algorithm.
- **Observed (mean ± std over runs):** LEACH 0.06 (± 0.01), DEAI-PSO 77.35 (± 7.09), GWO (Eq. 12) 75.76 (± 4.28), ABC (Eq. 12) 91.25 (± 7.13), Hybrid GWO-ABC (Eq. 12) 121.04 (± 13.47), Hybrid GWO-ABC 114.28 (± 13.14). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 212053.91% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse** (proposed/baseline ratio 2122×); vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 56.48% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -0.93 (large) → **proposed worse**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 59.76% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -0.93 (large) → **proposed worse**; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 32.65% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -0.91 (large) → **proposed worse**; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 5.91% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -0.48 (large) → **proposed worse**.
- **Is the difference meaningful?** 5 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Metaheuristics evaluate hundreds of candidate CH sets per round; LEACH needs one random draw per node. The hybrid runs two populations and more operators per iteration, which adds overhead even at an equal number of fitness evaluations. Runtime relative to LEACH: DEAI-PSO 1356×, GWO (Eq. 12) 1328×, ABC (Eq. 12) 1599×, Hybrid GWO-ABC (Eq. 12) 2122×, Hybrid GWO-ABC 2003×.

#### Final Fitness
- **What it represents:** Mean per-round fitness (same function and weights for every algorithm) of the CH set actually used, over rounds 1..checkpoint. Lower is better.
- **How it was calculated:** per round fitness of the CH set used (same weights for all), mean over rounds 1..checkpoint. (lower is better, unit: -)
- **Why it matters:** Quality of the CH configurations according to the optimisation objective.
- **Observed (mean ± std over runs):** LEACH 0.5505 (± 0.0839), DEAI-PSO 0.3276 (± 0.0031), GWO (Eq. 12) 0.3476 (± 0.0065), ABC (Eq. 12) 0.3534 (± 0.0055), Hybrid GWO-ABC (Eq. 12) 0.3453 (± 0.0061), Hybrid GWO-ABC 0.3086 (± 0.0044). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 37.27% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 5.41% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.64% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +0.20 (small) → **proposed better** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 2.28% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +0.66 (large) → **proposed better**; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 11.90% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**.
- **Is the difference meaningful?** 5 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Optimisers minimise this objective directly; LEACH does not use it, and rounds in which LEACH elects zero CHs or too many receive the invalid-solution penalty.

#### Node-rounds
- **What it represents:** Sum over rounds of the number of alive nodes (area under the alive-nodes curve).
- **How it was calculated:** sum over rounds of alive nodes. (higher is better, unit: node x rounds)
- **Why it matters:** Single-number lifetime measure that accounts for the whole death curve.
- **Observed (mean ± std over runs):** LEACH 92,982 (± 1,287), DEAI-PSO 105,257 (± 1,692), GWO (Eq. 12) 112,583 (± 1,550), ABC (Eq. 12) 111,910 (± 1,566), Hybrid GWO-ABC (Eq. 12) 112,643 (± 1,561), Hybrid GWO-ABC 106,685 (± 1,743). Best mean: **Hybrid GWO-ABC (Eq. 12)**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 21.14% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 7.02% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.05% better (improvement formula), p = 0.000253 (Holm), Cliff's δ = +0.07 (negligible) → **proposed better** — practically small; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 0.65% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +0.29 (small) → **proposed better** — practically small; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 5.58% better (improvement formula), p = 9.54e-06 (Holm), Cliff's δ = +0.99 (large) → **proposed better**.
- **Is the difference meaningful?** 5 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The area under the alive-nodes curve combines stability period and tail length.

#### Cluster Imbalance
- **What it represents:** Coefficient of variation of cluster sizes, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round std/mean of cluster sizes, averaged over rounds 1..checkpoint. (lower is better, unit: CV)
- **Why it matters:** Balanced clusters spread the CH load evenly.
- **Observed (mean ± std over runs):** LEACH 0.5593 (± 0.0114), DEAI-PSO 1.2184 (± 0.0551), GWO (Eq. 12) 0.7844 (± 0.0371), ABC (Eq. 12) 0.9096 (± 0.0379), Hybrid GWO-ABC (Eq. 12) 0.7689 (± 0.0344), Hybrid GWO-ABC 1.0948 (± 0.0649). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC (Eq. 12) is 37.48% worse (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs DEAI-PSO: Hybrid GWO-ABC (Eq. 12) is 36.89% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 1.98% better (reduction formula), p = 1.34e-05 (Holm), Cliff's δ = +0.26 (small) → **proposed better**; vs ABC (Eq. 12): Hybrid GWO-ABC (Eq. 12) is 15.46% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs Hybrid GWO-ABC: Hybrid GWO-ABC (Eq. 12) is 29.77% better (reduction formula), p = 9.54e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**.
- **Is the difference meaningful?** 5 of 5 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises unequal cluster sizes; nearest-CH assignment does not.

## Cluster-head records (run 0)

Every selected CH of every round is recorded in `ch_log_run0.csv` (round, CH id, coordinates, residual energy at selection, distance to the BS, cluster size including the CH). Dead and duplicate CHs are removed before clustering, so only valid CHs appear.

### LEACH

Over 830 rounds with CHs: 11.06 CHs/round on average; mean CH residual energy at selection 0.2484 J; mean CH–BS distance 149.07 m; 160 distinct nodes served as CH, the most frequent one 90 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 4 | 12.81 | 45.04 | 0.5 | 187.3 | 18 |
| 17 | 46.96 | 18.95 | 0.5 | 156.2 | 23 |
| 27 | 70.52 | 78.07 | 0.5 | 132.5 | 5 |
| 51 | 26.59 | 96.92 | 0.5 | 179.6 | 11 |
| 68 | 95.86 | 48.23 | 0.5 | 104.2 | 11 |
| 74 | 43.89 | 2.161 | 0.5 | 163.3 | 6 |
| 84 | 31.71 | 95.29 | 0.5 | 174.3 | 7 |
| 85 | 29.09 | 51.51 | 0.5 | 170.9 | 15 |
| 97 | 15.33 | 17.93 | 0.5 | 187.4 | 6 |
| 108 | 13.11 | 12.38 | 0.5 | 190.6 | 6 |
| 122 | 60.6 | 86.77 | 0.5 | 144.2 | 9 |
| 124 | 37.42 | 42.59 | 0.5 | 162.8 | 11 |
| 135 | 5.54 | 17.46 | 0.5 | 197.2 | 6 |
| 139 | 87.5 | 85.11 | 0.5 | 117.9 | 12 |
| 149 | 77.95 | 64.25 | 0.5 | 122.9 | 14 |

### DEAI-PSO

Over 664 rounds with CHs: 15.49 CHs/round on average; mean CH residual energy at selection 0.2537 J; mean CH–BS distance 125.78 m; 160 distinct nodes served as CH, the most frequent one 430 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 0 | 77.4 | 43.89 | 0.5 | 122.8 | 4 |
| 6 | 64.39 | 82.28 | 0.5 | 139.4 | 20 |
| 24 | 68.25 | 13.98 | 0.5 | 136.6 | 9 |
| 30 | 66.84 | 47.11 | 0.5 | 133.2 | 5 |
| 32 | 63.47 | 55.36 | 0.5 | 136.6 | 2 |
| 60 | 58.41 | 64.98 | 0.5 | 142.4 | 9 |
| 68 | 95.86 | 48.23 | 0.5 | 104.2 | 1 |
| 83 | 82.98 | 80.83 | 0.5 | 121 | 9 |
| 89 | 89.17 | 74.86 | 0.5 | 113.6 | 6 |
| 91 | 51.89 | 31.59 | 0.5 | 149.3 | 21 |
| 101 | 50.07 | 14.39 | 0.5 | 154.1 | 26 |
| 107 | 71.54 | 73.9 | 0.5 | 130.7 | 9 |
| 109 | 92.76 | 39.76 | 0.5 | 107.7 | 4 |
| 114 | 63.4 | 10.59 | 0.5 | 142.2 | 3 |
| 116 | 96.62 | 59.6 | 0.5 | 103.8 | 2 |
| 151 | 53.61 | 51.42 | 0.5 | 146.4 | 30 |

### GWO (Eq. 12)

Over 704 rounds with CHs: 7.87 CHs/round on average; mean CH residual energy at selection 0.2557 J; mean CH–BS distance 126.27 m; 156 distinct nodes served as CH, the most frequent one 264 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 0 | 77.4 | 43.89 | 0.5 | 122.8 | 10 |
| 28 | 45.89 | 56.87 | 0.5 | 154.3 | 29 |
| 33 | 55.92 | 30.4 | 0.5 | 145.4 | 17 |
| 36 | 85.34 | 23.39 | 0.5 | 117.7 | 10 |
| 50 | 90.86 | 69.97 | 0.5 | 111 | 8 |
| 89 | 89.17 | 74.86 | 0.5 | 113.6 | 7 |
| 114 | 63.4 | 10.59 | 0.5 | 142.2 | 14 |
| 118 | 46.74 | 78.48 | 0.5 | 155.9 | 27 |
| 139 | 87.5 | 85.11 | 0.5 | 117.9 | 13 |
| 155 | 47.79 | 41.69 | 0.5 | 152.4 | 25 |

### ABC (Eq. 12)

Over 697 rounds with CHs: 8.82 CHs/round on average; mean CH residual energy at selection 0.2562 J; mean CH–BS distance 125.36 m; 157 distinct nodes served as CH, the most frequent one 290 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 1 | 85.86 | 69.74 | 0.5 | 115.8 | 7 |
| 15 | 74.48 | 96.75 | 0.5 | 133.9 | 20 |
| 32 | 63.47 | 55.36 | 0.5 | 136.6 | 25 |
| 52 | 77.88 | 71.69 | 0.5 | 124 | 12 |
| 89 | 89.17 | 74.86 | 0.5 | 113.6 | 9 |
| 91 | 51.89 | 31.59 | 0.5 | 149.3 | 32 |
| 93 | 37.37 | 9.447 | 0.5 | 167.6 | 31 |
| 123 | 60.31 | 41.26 | 0.5 | 140 | 11 |
| 132 | 92.1 | 16.55 | 0.5 | 113 | 13 |

### Hybrid GWO-ABC (Eq. 12)

Over 702 rounds with CHs: 7.88 CHs/round on average; mean CH residual energy at selection 0.2554 J; mean CH–BS distance 126.30 m; 156 distinct nodes served as CH, the most frequent one 270 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 0 | 77.4 | 43.89 | 0.5 | 122.8 | 9 |
| 1 | 85.86 | 69.74 | 0.5 | 115.8 | 11 |
| 11 | 97.07 | 89.31 | 0.5 | 110.2 | 8 |
| 17 | 46.96 | 18.95 | 0.5 | 156.2 | 34 |
| 32 | 63.47 | 55.36 | 0.5 | 136.6 | 24 |
| 36 | 85.34 | 23.39 | 0.5 | 117.7 | 12 |
| 79 | 72.7 | 76.86 | 0.5 | 130.1 | 17 |
| 91 | 51.89 | 31.59 | 0.5 | 149.3 | 33 |
| 107 | 71.54 | 73.9 | 0.5 | 130.7 | 12 |

### Hybrid GWO-ABC

Over 670 rounds with CHs: 14.27 CHs/round on average; mean CH residual energy at selection 0.2576 J; mean CH–BS distance 125.13 m; 160 distinct nodes served as CH, the most frequent one 473 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 5 | 37.08 | 92.68 | 0.5 | 168.4 | 11 |
| 7 | 44.34 | 22.72 | 0.5 | 158 | 10 |
| 24 | 68.25 | 13.98 | 0.5 | 136.6 | 10 |
| 38 | 29.36 | 66.19 | 0.5 | 171.4 | 9 |
| 50 | 90.86 | 69.97 | 0.5 | 111 | 7 |
| 52 | 77.88 | 71.69 | 0.5 | 124 | 10 |
| 55 | 45.58 | 20.24 | 0.5 | 157.3 | 10 |
| 62 | 4.161 | 49.4 | 0.5 | 195.8 | 12 |
| 77 | 10.86 | 67.22 | 0.5 | 189.9 | 12 |
| 83 | 82.98 | 80.83 | 0.5 | 121 | 10 |
| 98 | 59.94 | 87.46 | 0.5 | 145 | 9 |
| 105 | 69.43 | 58.11 | 0.5 | 130.8 | 9 |
| 110 | 30.09 | 48.86 | 0.5 | 169.9 | 10 |
| 119 | 1.784 | 10.91 | 0.5 | 202 | 13 |
| 132 | 92.1 | 16.55 | 0.5 | 113 | 8 |
| 155 | 47.79 | 41.69 | 0.5 | 152.4 | 10 |


## Reproducing this experiment

```
python main.py reproduce "C:\Users\Admin\Hybrid-GWO-ABC-WSN\results\base_paper\BP2_160nodes"
```

`config.json` holds every parameter; `experiment.json` holds the algorithms, run count and seeds.
