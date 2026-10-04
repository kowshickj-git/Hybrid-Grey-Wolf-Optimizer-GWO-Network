# Scenario S1_100nodes

100 nodes, 100x100 m, BS at the centre (50, 50)

All numbers below were produced by the simulator in this folder (20 independent paired runs per algorithm; run r uses deployment/algorithm seed 42 + r). Raw per-run results: `runs_raw.csv`; per-round histories: `history_raw.csv.gz`; statistics: `statistics.csv`; proposed-vs-baseline tests: `improvement_vs_baselines.csv`.

## Configuration

| Parameter | Value |
|---|---|
| Nodes | 100 |
| Area (m) | 100 x 100 |
| BS position | (50, 50) |
| Initial energy (J/node) | 0.5 |
| Packet size (bits) | 4000 |
| Control packet (bits) | 0 |
| Max rounds | 2000 |
| CH percentage p | 0.05 |
| CH count tolerance | K_opt x (1 ± 0.5) |
| CH eligibility (optimisers) | E ≥ 1.0 x mean alive energy |
| Optimisation iterations / round | 30 |
| GWO population | 20 |
| ABC colony size (food sources) | 20 (10) |
| ABC abandonment limit | 10 |
| Hybrid budget share / transfer / feedback | 0.5 / 3 / True |
| Fitness weights w1..w5 | 0.3, 0.25, 0.2, 0.15, 0.1 |
| Radio E_elec / E_fs / E_mp / E_DA | 5e-08 / 1e-11 / 1.3e-15 / 5e-09 |
| Checkpoint round (energy / averages) | 500 |
| Base seed | 42 |

## Final result table (mean ± std over runs)

| Metric | Random | LEACH | GWO | ABC | Hybrid GWO-ABC |
|---|---:|---:|---:|---:|---:|
| FND (rounds) | 807 ± 31 | 892 ± 28 | 1,126 ± 7 | 1,125 ± 8 | 1,128 ± 7 |
| HND (rounds) | 1,125 ± 11 | 1,104 ± 8 | 1,138 ± 7 | 1,138 ± 6 | 1,138 ± 6 |
| LND (rounds) | 1,321 ± 27 | 1,287 ± 28 | 1,162 ± 11 | 1,162 ± 10 | 1,158 ± 13 |
| Residual Energy (J) | 27.750 ± 0.119 | 27.395 ± 0.156 | 28.110 ± 0.097 | 28.113 ± 0.101 | 28.102 ± 0.104 |
| Energy Consumption (J) | 22.250 ± 0.119 | 22.605 ± 0.156 | 21.890 ± 0.097 | 21.887 ± 0.101 | 21.898 ± 0.104 |
| Throughput (packets) | 109,907 ± 603 | 108,883 ± 730 | 113,715 ± 611 | 113,732 ± 611 | 113,662 ± 617 |
| PDR (ratio) | 0.9898 ± 0.0009 | 0.9892 ± 0.0014 | 0.9985 ± 0.0005 | 0.9986 ± 0.0005 | 0.9982 ± 0.0006 |
| Avg. Cluster Distance (m) | 25.055 ± 0.805 | 27.073 ± 0.850 | 22.499 ± 0.774 | 22.470 ± 0.805 | 22.563 ± 0.823 |
| Avg. CH-BS Distance (m) | 38.545 ± 1.562 | 38.554 ± 1.446 | 38.282 ± 1.384 | 38.278 ± 1.352 | 38.225 ± 1.417 |
| Runtime (s) | 0.56 ± 0.13 | 0.06 ± 0.01 | 54.54 ± 9.69 | 101.17 ± 15.92 | 132.15 ± 20.97 |
| Final Fitness (-) | 0.2904 ± 0.0117 | 1.3309 ± 0.1298 | 0.2416 ± 0.0113 | 0.2402 ± 0.0122 | 0.2387 ± 0.0115 |

Residual energy and energy consumption are measured at the checkpoint round 500; distance, imbalance and fitness averages cover rounds 1–500. '≥' marks lifetime values where at least one run had not reached the event within 2000 rounds (the horizon is then used as a lower bound).

## Descriptive statistics

**FND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| Random | 20 | 807 | 31 | 767 | 889 |
| LEACH | 20 | 892 | 28 | 829 | 931 |
| GWO | 20 | 1,126 | 7 | 1,115 | 1,138 |
| ABC | 20 | 1,125 | 8 | 1,111 | 1,138 |
| Hybrid GWO-ABC | 20 | 1,128 | 7 | 1,118 | 1,140 |

**HND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| Random | 20 | 1,125 | 11 | 1,105 | 1,147 |
| LEACH | 20 | 1,104 | 8 | 1,092 | 1,119 |
| GWO | 20 | 1,138 | 7 | 1,125 | 1,148 |
| ABC | 20 | 1,138 | 6 | 1,126 | 1,147 |
| Hybrid GWO-ABC | 20 | 1,138 | 6 | 1,128 | 1,148 |

**LND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| Random | 20 | 1,321 | 27 | 1,278 | 1,381 |
| LEACH | 20 | 1,287 | 28 | 1,242 | 1,365 |
| GWO | 20 | 1,162 | 11 | 1,141 | 1,183 |
| ABC | 20 | 1,162 | 10 | 1,138 | 1,181 |
| Hybrid GWO-ABC | 20 | 1,158 | 13 | 1,141 | 1,192 |

**Residual Energy (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| Random | 20 | 27.750 | 0.119 | 27.508 | 27.985 |
| LEACH | 20 | 27.395 | 0.156 | 27.044 | 27.682 |
| GWO | 20 | 28.110 | 0.097 | 27.889 | 28.233 |
| ABC | 20 | 28.113 | 0.101 | 27.916 | 28.251 |
| Hybrid GWO-ABC | 20 | 28.102 | 0.104 | 27.902 | 28.252 |

**Energy Consumption (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| Random | 20 | 22.250 | 0.119 | 22.015 | 22.492 |
| LEACH | 20 | 22.605 | 0.156 | 22.318 | 22.956 |
| GWO | 20 | 21.890 | 0.097 | 21.767 | 22.111 |
| ABC | 20 | 21.887 | 0.101 | 21.749 | 22.084 |
| Hybrid GWO-ABC | 20 | 21.898 | 0.104 | 21.748 | 22.098 |

**Throughput (packets)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| Random | 20 | 109,907 | 603 | 108,505 | 110,994 |
| LEACH | 20 | 108,883 | 730 | 107,534 | 110,208 |
| GWO | 20 | 113,715 | 611 | 112,476 | 114,689 |
| ABC | 20 | 113,732 | 611 | 112,425 | 114,701 |
| Hybrid GWO-ABC | 20 | 113,662 | 617 | 112,601 | 114,549 |

**PDR (ratio)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| Random | 20 | 0.9898 | 0.0009 | 0.9883 | 0.9916 |
| LEACH | 20 | 0.9892 | 0.0014 | 0.9864 | 0.9920 |
| GWO | 20 | 0.9985 | 0.0005 | 0.9973 | 0.9991 |
| ABC | 20 | 0.9986 | 0.0005 | 0.9972 | 0.9991 |
| Hybrid GWO-ABC | 20 | 0.9982 | 0.0006 | 0.9971 | 0.9991 |

**Runtime (s)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| Random | 20 | 0.56 | 0.13 | 0.34 | 0.71 |
| LEACH | 20 | 0.06 | 0.01 | 0.03 | 0.07 |
| GWO | 20 | 54.54 | 9.69 | 36.22 | 61.99 |
| ABC | 20 | 101.17 | 15.92 | 74.31 | 114.16 |
| Hybrid GWO-ABC | 20 | 132.15 | 20.97 | 82.31 | 152.98 |

## Hybrid GWO-ABC vs baselines

Improvement % uses ((P − B) / B) × 100 for higher-is-better metrics and ((B − P) / B) × 100 for lower-is-better metrics, so a positive value always means the proposed algorithm did better. p-values: paired two-sided Wilcoxon signed-rank test, Holm-corrected over the baselines. Cliff's δ > 0 favours the proposed algorithm (|δ| < 0.147 negligible, < 0.33 small, < 0.474 medium, otherwise large).

| Metric | Baseline | Better | Improvement % | p (Holm) | Cliff's δ | Effect | Verdict |
|---|---|---|---:|---:|---:|---|---|
| FND | Random | higher | +39.75 | 0.000353 | +1.00 | large | proposed better |
| FND | LEACH | higher | +26.49 | 0.000353 | +1.00 | large | proposed better |
| FND | GWO | higher | +0.12 | 0.138 | +0.12 | negligible | no significant difference |
| FND | ABC | higher | +0.20 | 0.172 | +0.17 | small | no significant difference |
| HND | Random | higher | +1.11 | 0.00341 | +0.66 | large | proposed better |
| HND | LEACH | higher | +3.02 | 0.000353 | +1.00 | large | proposed better |
| HND | GWO | higher | +0.01 | 1 | -0.01 | negligible | no significant difference |
| HND | ABC | higher | -0.01 | 1 | -0.02 | negligible | no significant difference |
| LND | Random | higher | -12.33 | 0.000353 | -1.00 | large | proposed worse |
| LND | LEACH | higher | -9.99 | 0.000353 | -1.00 | large | proposed worse |
| LND | GWO | higher | -0.32 | 0.178 | -0.21 | small | no significant difference |
| LND | ABC | higher | -0.35 | 0.313 | -0.29 | small | no significant difference |
| Node-rounds | Random | higher | +2.55 | 7.63e-06 | +1.00 | large | proposed better |
| Node-rounds | LEACH | higher | +3.45 | 7.63e-06 | +1.00 | large | proposed better |
| Node-rounds | GWO | higher | -0.02 | 0.555 | -0.01 | negligible | no significant difference |
| Node-rounds | ABC | higher | -0.02 | 0.555 | -0.02 | negligible | no significant difference |
| Residual Energy | Random | higher | +1.27 | 7.63e-06 | +0.98 | large | proposed better |
| Residual Energy | LEACH | higher | +2.58 | 7.63e-06 | +1.00 | large | proposed better |
| Residual Energy | GWO | higher | -0.03 | 0.177 | -0.06 | negligible | no significant difference |
| Residual Energy | ABC | higher | -0.04 | 0.00203 | -0.09 | negligible | proposed worse |
| Energy Consumption | Random | lower | +1.58 | 7.63e-06 | +0.98 | large | proposed better |
| Energy Consumption | LEACH | lower | +3.13 | 7.63e-06 | +1.00 | large | proposed better |
| Energy Consumption | GWO | lower | -0.04 | 0.177 | -0.06 | negligible | no significant difference |
| Energy Consumption | ABC | lower | -0.05 | 0.00203 | -0.09 | negligible | proposed worse |
| Throughput | Random | higher | +3.42 | 7.63e-06 | +1.00 | large | proposed better |
| Throughput | LEACH | higher | +4.39 | 7.63e-06 | +1.00 | large | proposed better |
| Throughput | GWO | higher | -0.05 | 0.0725 | -0.03 | negligible | no significant difference |
| Throughput | ABC | higher | -0.06 | 0.0973 | -0.07 | negligible | no significant difference |
| PDR | Random | higher | +0.85 | 7.63e-06 | +1.00 | large | proposed better |
| PDR | LEACH | higher | +0.91 | 7.63e-06 | +1.00 | large | proposed better |
| PDR | GWO | higher | -0.03 | 0.08 | -0.34 | medium | no significant difference |
| PDR | ABC | higher | -0.04 | 0.08 | -0.44 | medium | no significant difference |
| Avg. Cluster Distance | Random | lower | +9.95 | 7.63e-06 | +0.97 | large | proposed better |
| Avg. Cluster Distance | LEACH | lower | +16.66 | 7.63e-06 | +1.00 | large | proposed better |
| Avg. Cluster Distance | GWO | lower | -0.28 | 0.165 | -0.07 | negligible | no significant difference |
| Avg. Cluster Distance | ABC | lower | -0.41 | 0.00142 | -0.07 | negligible | proposed worse |
| Avg. CH-BS Distance | Random | lower | +0.83 | 0.000143 | +0.14 | negligible | proposed better |
| Avg. CH-BS Distance | LEACH | lower | +0.85 | 1.53e-05 | +0.16 | small | proposed better |
| Avg. CH-BS Distance | GWO | lower | +0.15 | 0.0306 | +0.06 | negligible | proposed better |
| Avg. CH-BS Distance | ABC | lower | +0.14 | 0.114 | +0.04 | negligible | no significant difference |
| Final Fitness | Random | lower | +17.80 | 7.63e-06 | +1.00 | large | proposed better |
| Final Fitness | LEACH | lower | +82.06 | 7.63e-06 | +1.00 | large | proposed better |
| Final Fitness | GWO | lower | +1.19 | 7.63e-06 | +0.17 | small | proposed better |
| Final Fitness | ABC | lower | +0.62 | 0.00233 | +0.08 | negligible | proposed better |
| Runtime | Random | lower | -23624.50 | 7.63e-06 | -1.00 | large | proposed worse |
| Runtime | LEACH | lower | -234767.67 | 7.63e-06 | -1.00 | large | proposed worse |
| Runtime | GWO | lower | -142.31 | 7.63e-06 | -1.00 | large | proposed worse |
| Runtime | ABC | lower | -30.61 | 7.63e-06 | -0.68 | large | proposed worse |

### Trade-offs

- **Hybrid GWO-ABC vs Random** — significantly better: FND (+39.75%), HND (+1.11%), Node-rounds (+2.55%), Residual Energy (+1.27%), Energy Consumption (+1.58%), Throughput (+3.42%), PDR (+0.85%, < 1%: practically negligible), Avg. Cluster Distance (+9.95%), Avg. CH-BS Distance (+0.83%, < 1%: practically negligible), Cluster Imbalance (+69.31%), Final Fitness (+17.80%); significantly worse: LND (-12.33%), Runtime (-23624.50%), Runtime / round (-26944.75%); no significant difference: Fitness Evaluations.
- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+26.49%), HND (+3.02%), Node-rounds (+3.45%), Residual Energy (+2.58%), Energy Consumption (+3.13%), Throughput (+4.39%), PDR (+0.91%, < 1%: practically negligible), Avg. Cluster Distance (+16.66%), Avg. CH-BS Distance (+0.85%, < 1%: practically negligible), Cluster Imbalance (+66.84%), Final Fitness (+82.06%); significantly worse: LND (-9.99%), Runtime (-234767.67%), Runtime / round (-260624.02%); no significant difference: Fitness Evaluations.
- **Hybrid GWO-ABC vs GWO** — significantly better: Avg. CH-BS Distance (+0.15%, < 1%: practically negligible), Cluster Imbalance (+14.71%), Final Fitness (+1.19%); significantly worse: Runtime (-142.31%), Runtime / round (-142.92%), Fitness Evaluations (-0.90%, < 1%: practically negligible); no significant difference: FND, HND, LND, Node-rounds, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance.
- **Hybrid GWO-ABC vs ABC** — significantly better: Cluster Imbalance (+4.92%), Final Fitness (+0.62%, < 1%: practically negligible); significantly worse: Residual Energy (-0.04%, < 1%: practically negligible), Energy Consumption (-0.05%, < 1%: practically negligible), Avg. Cluster Distance (-0.41%, < 1%: practically negligible), Runtime (-30.61%), Runtime / round (-31.03%); no significant difference: FND, HND, LND, Node-rounds, Throughput, PDR, Avg. CH-BS Distance, Fitness Evaluations.

## Figures

### Initial WSN topology (run 0; every algorithm uses this same network in run 0).

![Initial WSN topology (run 0; every algorithm uses this same network in run 0).](01_topology.png)

**Observed:** 100 nodes uniformly deployed in 100 x 100 m (seed 42); BS at (50, 50). Mean node–BS distance 37.5 m (max 62.9 m); d0 = 87.7 m, so 0% of nodes would use the multipath (d^4) model for a direct BS transmission.

### Random: cluster heads selected in round 1 (run 0).

![Random: cluster heads selected in round 1 (run 0).](02_ch_selection_Random.png)

**Observed:** 5 CHs; mean CH–BS distance 38.9 m.

### Random: cluster formation in round 1 (members joined the nearest CH).

![Random: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Random.png)

**Observed:** 5 clusters, sizes 14–29 (CV 0.27); member→CH distance mean 20.6 m, max 43.2 m.

### Random: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Random: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Random.png)

**Observed:** Round 1134: 50 dead, 50 alive. Mean distance to BS — dead nodes 28.3 m, alive nodes 46.7 m (near nodes died first on average).

### LEACH: cluster heads selected in round 1 (run 0).

![LEACH: cluster heads selected in round 1 (run 0).](02_ch_selection_LEACH.png)

**Observed:** 4 CHs; mean CH–BS distance 45.5 m.

### LEACH: cluster formation in round 1 (members joined the nearest CH).

![LEACH: cluster formation in round 1 (members joined the nearest CH).](03_clusters_LEACH.png)

**Observed:** 4 clusters, sizes 17–34 (CV 0.27); member→CH distance mean 36.8 m, max 91.2 m.

### LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_LEACH.png)

**Observed:** Round 1108: 50 dead, 50 alive. Mean distance to BS — dead nodes 27.8 m, alive nodes 47.2 m (near nodes died first on average).

### GWO: cluster heads selected in round 1 (run 0).

![GWO: cluster heads selected in round 1 (run 0).](02_ch_selection_GWO.png)

**Observed:** 5 CHs; mean CH–BS distance 17.1 m.

### GWO: cluster formation in round 1 (members joined the nearest CH).

![GWO: cluster formation in round 1 (members joined the nearest CH).](03_clusters_GWO.png)

**Observed:** 5 clusters, sizes 18–25 (CV 0.14); member→CH distance mean 27.5 m, max 61.3 m.

### GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_GWO.png)

**Observed:** Round 1146: 54 dead, 46 alive. Mean distance to BS — dead nodes 35.0 m, alive nodes 40.4 m (near nodes died first on average).

### ABC: cluster heads selected in round 1 (run 0).

![ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_ABC.png)

**Observed:** 5 CHs; mean CH–BS distance 24.2 m.

### ABC: cluster formation in round 1 (members joined the nearest CH).

![ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_ABC.png)

**Observed:** 5 clusters, sizes 19–21 (CV 0.04); member→CH distance mean 20.0 m, max 47.9 m.

### ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_ABC.png)

**Observed:** Round 1147: 59 dead, 41 alive. Mean distance to BS — dead nodes 34.5 m, alive nodes 41.9 m (near nodes died first on average).

### Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).

![Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_GWO-ABC.png)

**Observed:** 5 CHs; mean CH–BS distance 20.0 m.

### Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).

![Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_GWO-ABC.png)

**Observed:** 5 clusters, sizes 18–22 (CV 0.08); member→CH distance mean 24.1 m, max 45.9 m.

### Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).

![Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).](04_communication_Hybrid_GWO-ABC.png)

**Observed:** 5 clusters, sizes 18–22 (CV 0.08); member→CH distance mean 24.1 m, max 45.9 m.

### Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_GWO-ABC.png)

**Observed:** Round 1146: 50 dead, 50 alive. Mean distance to BS — dead nodes 34.1 m, alive nodes 40.9 m (near nodes died first on average).

### GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_GWO.png)

**Observed:** mean best fitness 0.2282 → 0.1736 (23.9% lower); 95% of the improvement reached by iteration 22

### ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_ABC.png)

**Observed:** mean best fitness 0.2328 → 0.1693 (27.3% lower); 95% of the improvement reached by iteration 20

### Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_GWO-ABC.png)

**Observed:** GWO: mean best fitness 0.2328 → 0.1605 (31.1% lower); 95% of the improvement reached by iteration 25; ABC: mean best fitness 0.2695 → 0.1605 (40.4% lower); 95% of the improvement reached by iteration 20; HYBRID: mean best fitness 0.2328 → 0.1605 (31.1% lower); 95% of the improvement reached by iteration 25

### Alive nodes vs rounds.

![Alive nodes vs rounds.](09_alive_vs_rounds.png)

**Observed:** Random: FND 807, HND 1125, LND 1321; LEACH: FND 892, HND 1104, LND 1287; GWO: FND 1126, HND 1138, LND 1162; ABC: FND 1125, HND 1138, LND 1162; Hybrid GWO-ABC: FND 1128, HND 1138, LND 1158

### Dead nodes vs rounds.

![Dead nodes vs rounds.](10_dead_vs_rounds.png)

**Observed:** Mirror image of the alive-nodes curve; a steeper rise means nodes die closer together.

### Residual energy vs rounds.

![Residual energy vs rounds.](11_residual_energy_vs_rounds.png)

**Observed:** Residual energy at round 500: Random 27.75 J; LEACH 27.40 J; GWO 28.11 J; ABC 28.11 J; Hybrid GWO-ABC 28.10 J

### Energy consumption vs rounds.

![Energy consumption vs rounds.](12_consumed_energy_vs_rounds.png)

**Observed:** Consumed by round 500: Random 22.25 J; LEACH 22.60 J; GWO 21.89 J; ABC 21.89 J; Hybrid GWO-ABC 21.90 J

### Throughput vs rounds (cumulative).

![Throughput vs rounds (cumulative).](13_packets_delivered_vs_rounds.png)

**Observed:** Total delivered: Random 109,907; LEACH 108,883; GWO 113,715; ABC 113,732; Hybrid GWO-ABC 113,662

### PDR vs rounds.

![PDR vs rounds.](14_pdr_vs_rounds.png)

**Observed:** Final PDR: Random 0.9898; LEACH 0.9892; GWO 0.9985; ABC 0.9986; Hybrid GWO-ABC 0.9982

### CH count vs rounds (20-round rolling mean).

![CH count vs rounds (20-round rolling mean).](15_ch_count_vs_rounds.png)

**Observed:** Mean CHs/round (rounds 1–500): Random 5.00 (per-round std 0.00); LEACH 5.00 (per-round std 2.20); GWO 4.83 (per-round std 0.54); ABC 4.81 (per-round std 0.58); Hybrid GWO-ABC 4.81 (per-round std 0.54)

### Average cluster distance vs rounds (20-round rolling mean).

![Average cluster distance vs rounds (20-round rolling mean).](16_avg_intra_distance_vs_rounds.png)

**Observed:** Mean member→CH distance: Random 25.05 m; LEACH 27.07 m; GWO 22.50 m; ABC 22.47 m; Hybrid GWO-ABC 22.56 m

### Total CH-selection runtime per simulation (log scale, mean ± std).

![Total CH-selection runtime per simulation (log scale, mean ± std).](17_runtime.png)

**Observed:** Random 0.56 s (0.42 ms/round, 0 fitness evaluations); LEACH 0.06 s (0.04 ms/round, 0 fitness evaluations); GWO 54.54 s (46.94 ms/round, 720,471 fitness evaluations); ABC 101.17 s (87.03 ms/round, 725,709 fitness evaluations); Hybrid GWO-ABC 132.15 s (114.04 ms/round, 726,942 fitness evaluations)

### FND / HND / LND comparison (mean ± std over runs).

![FND / HND / LND comparison (mean ± std over runs).](18_lifetime_fnd_hnd_lnd.png)

**Observed:** Random: FND 807, HND 1125, LND 1321; LEACH: FND 892, HND 1104, LND 1287; GWO: FND 1126, HND 1138, LND 1162; ABC: FND 1125, HND 1138, LND 1162; Hybrid GWO-ABC: FND 1128, HND 1138, LND 1158

### Where the energy goes: mean energy per radio activity over rounds 1–500.

![Where the energy goes: mean energy per radio activity over rounds 1–500.](19_energy_breakdown.png)

**Observed:** Random: total 22.25 J, largest share member TX (50%); LEACH: total 22.60 J, largest share member TX (51%); GWO: total 21.89 J, largest share member TX (49%); ABC: total 21.89 J, largest share member TX (49%); Hybrid GWO-ABC: total 21.90 J, largest share member TX (49%)

### Final fitness: same objective and weights for every algorithm.

![Final fitness: same objective and weights for every algorithm.](20_final_fitness.png)

**Observed:** Random 0.2904; LEACH 1.3309; GWO 0.2416; ABC 0.2402; Hybrid GWO-ABC 0.2387

## Metric-by-metric interpretation

#### FND
- **What it represents:** First Node Death: the round in which the first node's residual energy reached 0.
- **How it was calculated:** min over nodes of the round in which residual energy reached 0 (simulation horizon if none died). (higher is better, unit: rounds)
- **Why it matters:** Marks the end of the stability period, during which every sensor still reports.
- **Observed (mean ± std over runs):** Random 807 (± 31), LEACH 892 (± 28), GWO 1,126 (± 7), ABC 1,125 (± 8), Hybrid GWO-ABC 1,128 (± 7). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 39.75% better (improvement formula), p = 0.000353 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs LEACH: Hybrid GWO-ABC is 26.49% better (improvement formula), p = 0.000353 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.12% better (improvement formula), p = 0.138 (Holm), Cliff's δ = +0.12 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.20% better (improvement formula), p = 0.172 (Holm), Cliff's δ = +0.17 (small) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** CH selection that avoids low-energy nodes and rotates the CH role evenly delays the first death; a node chosen repeatedly as CH (e.g. because it is close to the BS) dies early. Measured LND − FND spread (rounds): Random 514, LEACH 395, GWO 36, ABC 37, Hybrid GWO-ABC 31.

#### HND
- **What it represents:** Half Node Death: the round in which at least 50% of the nodes were dead.
- **How it was calculated:** round in which the number of dead nodes reached ceil(N/2). (higher is better, unit: rounds)
- **Why it matters:** Indicates how long the network keeps useful coverage.
- **Observed (mean ± std over runs):** Random 1,125 (± 11), LEACH 1,104 (± 8), GWO 1,138 (± 7), ABC 1,138 (± 6), Hybrid GWO-ABC 1,138 (± 6). Best mean: **ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 1.11% better (improvement formula), p = 0.00341 (Holm), Cliff's δ = +0.66 (large) → **proposed better**; vs LEACH: Hybrid GWO-ABC is 3.02% better (improvement formula), p = 0.000353 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.01% better (improvement formula), p = 1 (Holm), Cliff's δ = -0.01 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.01% worse (improvement formula), p = 1 (Holm), Cliff's δ = -0.02 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** HND reflects how evenly energy is drained across the whole network.

#### LND
- **What it represents:** Last Node Death: the round in which the last alive node died.
- **How it was calculated:** round in which the last node died (simulation horizon if nodes were still alive). (higher is better, unit: rounds)
- **Why it matters:** Upper bound of the network lifetime.
- **Observed (mean ± std over runs):** Random 1,321 (± 27), LEACH 1,287 (± 28), GWO 1,162 (± 11), ABC 1,162 (± 10), Hybrid GWO-ABC 1,158 (± 13). Best mean: **Random**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 12.33% worse (improvement formula), p = 0.000353 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs LEACH: Hybrid GWO-ABC is 9.99% worse (improvement formula), p = 0.000353 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs GWO: Hybrid GWO-ABC is 0.32% worse (improvement formula), p = 0.178 (Holm), Cliff's δ = -0.21 (small) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.35% worse (improvement formula), p = 0.313 (Holm), Cliff's δ = -0.29 (small) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** A very even energy drain makes all nodes die at nearly the same time: FND is delayed but the last node also dies sooner. Uneven drain leaves a few nodes with spare energy that keep running. Measured LND − FND spread (rounds): Random 514, LEACH 395, GWO 36, ABC 37, Hybrid GWO-ABC 31.

#### Residual Energy
- **What it represents:** Total residual energy of all nodes at the checkpoint round.
- **How it was calculated:** sum of node residual energies after the checkpoint round. (higher is better, unit: J)
- **Why it matters:** More energy left at the same round means cheaper operation.
- **Observed (mean ± std over runs):** Random 27.750 (± 0.119), LEACH 27.395 (± 0.156), GWO 28.110 (± 0.097), ABC 28.113 (± 0.101), Hybrid GWO-ABC 28.102 (± 0.104). Best mean: **ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 1.27% better (improvement formula), p = 7.63e-06 (Holm), Cliff's δ = +0.98 (large) → **proposed better**; vs LEACH: Hybrid GWO-ABC is 2.58% better (improvement formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.03% worse (improvement formula), p = 0.177 (Holm), Cliff's δ = -0.06 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.04% worse (improvement formula), p = 0.00203 (Holm), Cliff's δ = -0.09 (negligible) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Residual energy at a fixed round depends on per-round radio cost: shorter member->CH links and shorter or fewer CH->BS links consume less.

#### Energy Consumption
- **What it represents:** Initial total energy minus residual energy at the checkpoint round.
- **How it was calculated:** N * E0 - residual energy at the checkpoint round. (lower is better, unit: J)
- **Why it matters:** Energy spent to operate the network for the same number of rounds.
- **Observed (mean ± std over runs):** Random 22.250 (± 0.119), LEACH 22.605 (± 0.156), GWO 21.890 (± 0.097), ABC 21.887 (± 0.101), Hybrid GWO-ABC 21.898 (± 0.104). Best mean: **ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 1.58% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +0.98 (large) → **proposed better**; vs LEACH: Hybrid GWO-ABC is 3.13% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.04% worse (reduction formula), p = 0.177 (Holm), Cliff's δ = -0.06 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.05% worse (reduction formula), p = 0.00203 (Holm), Cliff's δ = -0.09 (negligible) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Consumption is the complement of residual energy at the same checkpoint.

#### Throughput
- **What it represents:** Total sensor data packets delivered to the BS over the whole simulation (directly or inside an aggregated CH packet).
- **How it was calculated:** count of sensor readings that reached the BS over the whole run. (higher is better, unit: packets)
- **Why it matters:** Amount of sensed data the application actually receives.
- **Observed (mean ± std over runs):** Random 109,907 (± 603), LEACH 108,883 (± 730), GWO 113,715 (± 611), ABC 113,732 (± 611), Hybrid GWO-ABC 113,662 (± 617). Best mean: **ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 3.42% better (improvement formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs LEACH: Hybrid GWO-ABC is 4.39% better (improvement formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.0725 (Holm), Cliff's δ = -0.03 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.06% worse (improvement formula), p = 0.0973 (Holm), Cliff's δ = -0.07 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Throughput grows with the number of rounds in which nodes are alive and with the share of packets that are not lost to CHs dying mid-round.

#### PDR
- **What it represents:** Packet Delivery Ratio = delivered data packets / generated data packets.
- **How it was calculated:** delivered readings / generated readings over the whole run. (higher is better, unit: ratio)
- **Why it matters:** Reliability: share of generated readings that reach the BS.
- **Observed (mean ± std over runs):** Random 0.9898 (± 0.0009), LEACH 0.9892 (± 0.0014), GWO 0.9985 (± 0.0005), ABC 0.9986 (± 0.0005), Hybrid GWO-ABC 0.9982 (± 0.0006). Best mean: **ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 0.85% better (improvement formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better** — practically small; vs LEACH: Hybrid GWO-ABC is 0.91% better (improvement formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better** — practically small; vs GWO: Hybrid GWO-ABC is 0.03% worse (improvement formula), p = 0.08 (Holm), Cliff's δ = -0.34 (medium) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.04% worse (improvement formula), p = 0.08 (Holm), Cliff's δ = -0.44 (medium) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Packets are lost when a CH runs out of energy before forwarding its cluster's data, or when a node dies while transmitting. Energy-feasibility checks on CHs reduce such losses.

#### Avg. Cluster Distance
- **What it represents:** Mean member->CH distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean member->CH distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** Shorter intra-cluster links cost less transmission energy (d^2 / d^4).
- **Observed (mean ± std over runs):** Random 25.055 (± 0.805), LEACH 27.073 (± 0.850), GWO 22.499 (± 0.774), ABC 22.470 (± 0.805), Hybrid GWO-ABC 22.563 (± 0.823). Best mean: **ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 9.95% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +0.97 (large) → **proposed better**; vs LEACH: Hybrid GWO-ABC is 16.66% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.28% worse (reduction formula), p = 0.165 (Holm), Cliff's δ = -0.07 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.41% worse (reduction formula), p = 0.00142 (Holm), Cliff's δ = -0.07 (negligible) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness function explicitly penalises member->CH distance; LEACH places CHs at random positions, which typically lengthens member links.

#### Avg. CH-BS Distance
- **What it represents:** Mean CH->BS distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean CH->BS distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** CH->BS is the longest and most expensive hop.
- **Observed (mean ± std over runs):** Random 38.545 (± 1.562), LEACH 38.554 (± 1.446), GWO 38.282 (± 1.384), ABC 38.278 (± 1.352), Hybrid GWO-ABC 38.225 (± 1.417). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 0.83% better (reduction formula), p = 0.000143 (Holm), Cliff's δ = +0.14 (negligible) → **proposed better** — practically small; vs LEACH: Hybrid GWO-ABC is 0.85% better (reduction formula), p = 1.53e-05 (Holm), Cliff's δ = +0.16 (small) → **proposed better** — practically small; vs GWO: Hybrid GWO-ABC is 0.15% better (reduction formula), p = 0.0306 (Holm), Cliff's δ = +0.06 (negligible) → **proposed better** — practically small; vs ABC: Hybrid GWO-ABC is 0.14% better (reduction formula), p = 0.114 (Holm), Cliff's δ = +0.04 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 3 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises CH->BS distance, but the energy-eligibility rule and the energy term limit how often nodes near the BS can be selected.

#### Runtime
- **What it represents:** Total wall-clock time spent selecting CHs over the whole simulation.
- **How it was calculated:** sum of wall-clock CH-selection time over all rounds (time.perf_counter). (lower is better, unit: s)
- **Why it matters:** Computational cost of the CH selection algorithm.
- **Observed (mean ± std over runs):** Random 0.56 (± 0.13), LEACH 0.06 (± 0.01), GWO 54.54 (± 9.69), ABC 101.17 (± 15.92), Hybrid GWO-ABC 132.15 (± 20.97). Best mean: **LEACH**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 23624.50% worse (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse** (proposed/baseline ratio 237×); vs LEACH: Hybrid GWO-ABC is 234767.67% worse (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse** (proposed/baseline ratio 2349×); vs GWO: Hybrid GWO-ABC is 142.31% worse (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs ABC: Hybrid GWO-ABC is 30.61% worse (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = -0.68 (large) → **proposed worse**.
- **Is the difference meaningful?** 4 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Metaheuristics evaluate hundreds of candidate CH sets per round; LEACH needs one random draw per node. The hybrid runs two populations and more operators per iteration, which adds overhead even at an equal number of fitness evaluations. Runtime relative to LEACH: Random 10×, GWO 969×, ABC 1798×, Hybrid GWO-ABC 2349×.

#### Final Fitness
- **What it represents:** Mean per-round fitness (same function and weights for every algorithm) of the CH set actually used, over rounds 1..checkpoint. Lower is better.
- **How it was calculated:** per round fitness of the CH set used (same weights for all), mean over rounds 1..checkpoint. (lower is better, unit: -)
- **Why it matters:** Quality of the CH configurations according to the optimisation objective.
- **Observed (mean ± std over runs):** Random 0.2904 (± 0.0117), LEACH 1.3309 (± 0.1298), GWO 0.2416 (± 0.0113), ABC 0.2402 (± 0.0122), Hybrid GWO-ABC 0.2387 (± 0.0115). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 17.80% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs LEACH: Hybrid GWO-ABC is 82.06% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 1.19% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +0.17 (small) → **proposed better**; vs ABC: Hybrid GWO-ABC is 0.62% better (reduction formula), p = 0.00233 (Holm), Cliff's δ = +0.08 (negligible) → **proposed better** — practically small.
- **Is the difference meaningful?** 4 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Optimisers minimise this objective directly; LEACH does not use it, and rounds in which LEACH elects zero CHs or too many receive the invalid-solution penalty.

#### Node-rounds
- **What it represents:** Sum over rounds of the number of alive nodes (area under the alive-nodes curve).
- **How it was calculated:** sum over rounds of alive nodes. (higher is better, unit: node x rounds)
- **Why it matters:** Single-number lifetime measure that accounts for the whole death curve.
- **Observed (mean ± std over runs):** Random 110,942 (± 599), LEACH 109,970 (± 736), GWO 113,786 (± 624), ABC 113,791 (± 607), Hybrid GWO-ABC 113,768 (± 617). Best mean: **ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 2.55% better (improvement formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs LEACH: Hybrid GWO-ABC is 3.45% better (improvement formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.02% worse (improvement formula), p = 0.555 (Holm), Cliff's δ = -0.01 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.02% worse (improvement formula), p = 0.555 (Holm), Cliff's δ = -0.02 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The area under the alive-nodes curve combines stability period and tail length.

#### Cluster Imbalance
- **What it represents:** Coefficient of variation of cluster sizes, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round std/mean of cluster sizes, averaged over rounds 1..checkpoint. (lower is better, unit: CV)
- **Why it matters:** Balanced clusters spread the CH load evenly.
- **Observed (mean ± std over runs):** Random 0.4833 (± 0.0132), LEACH 0.4471 (± 0.0120), GWO 0.1739 (± 0.0107), ABC 0.1560 (± 0.0112), Hybrid GWO-ABC 0.1483 (± 0.0089). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs Random: Hybrid GWO-ABC is 69.31% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs LEACH: Hybrid GWO-ABC is 66.84% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 14.71% better (reduction formula), p = 7.63e-06 (Holm), Cliff's δ = +0.93 (large) → **proposed better**; vs ABC: Hybrid GWO-ABC is 4.92% better (reduction formula), p = 1.91e-05 (Holm), Cliff's δ = +0.48 (large) → **proposed better**.
- **Is the difference meaningful?** 4 of 4 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises unequal cluster sizes; nearest-CH assignment does not.

## Cluster-head records (run 0)

Every selected CH of every round is recorded in `ch_log_run0.csv` (round, CH id, coordinates, residual energy at selection, distance to the BS, cluster size including the CH). Dead and duplicate CHs are removed before clustering, so only valid CHs appear.

**Reproducibility check:** run 0 of every algorithm was re-simulated from `config.json` and its seed; all checked results (fnd, hnd, lnd, node_rounds, throughput_packets, packets_generated, residual_energy_cp, final_fitness) are identical to the saved values (`reproducibility_check_run0.csv`).

### Random

Over 1348 rounds with CHs: 4.21 CHs/round on average; mean CH residual energy at selection 0.2519 J; mean CH–BS distance 38.70 m; 100 distinct nodes served as CH, the most frequent one 116 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 8 | 55.46 | 6.382 | 0.5 | 43.96 | 15 |
| 43 | 72.24 | 46.19 | 0.5 | 22.56 | 22 |
| 64 | 10.34 | 58.76 | 0.5 | 40.62 | 29 |
| 75 | 82.63 | 89.62 | 0.5 | 51.32 | 20 |
| 99 | 19.64 | 31.03 | 0.5 | 35.8 | 14 |

### LEACH

Over 1204 rounds with CHs: 4.60 CHs/round on average; mean CH residual energy at selection 0.2542 J; mean CH–BS distance 38.45 m; 100 distinct nodes served as CH, the most frequent one 65 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 27 | 70.52 | 78.07 | 0.5 | 34.77 | 29 |
| 51 | 26.59 | 96.92 | 0.5 | 52.44 | 20 |
| 68 | 95.86 | 48.23 | 0.5 | 45.89 | 34 |
| 84 | 31.71 | 95.29 | 0.5 | 48.84 | 17 |

### GWO

Over 1163 rounds with CHs: 4.75 CHs/round on average; mean CH residual energy at selection 0.2524 J; mean CH–BS distance 38.09 m; 100 distinct nodes served as CH, the most frequent one 67 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 28 | 45.89 | 56.87 | 0.5 | 8.008 | 21 |
| 30 | 66.84 | 47.11 | 0.5 | 17.09 | 18 |
| 31 | 56.52 | 76.5 | 0.5 | 27.29 | 18 |
| 70 | 48.67 | 49.07 | 0.5 | 1.626 | 25 |
| 92 | 77.2 | 66.17 | 0.5 | 31.64 | 18 |

### ABC

Over 1159 rounds with CHs: 4.76 CHs/round on average; mean CH residual energy at selection 0.2520 J; mean CH–BS distance 38.22 m; 100 distinct nodes served as CH, the most frequent one 66 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 44 | 16.13 | 50.1 | 0.5 | 33.87 | 21 |
| 52 | 77.88 | 71.69 | 0.5 | 35.32 | 21 |
| 53 | 44.94 | 27.22 | 0.5 | 23.33 | 20 |
| 59 | 43.21 | 62.73 | 0.5 | 14.43 | 19 |
| 82 | 55.49 | 37.09 | 0.5 | 14.02 | 19 |

### Hybrid GWO-ABC

Over 1160 rounds with CHs: 4.76 CHs/round on average; mean CH residual energy at selection 0.2526 J; mean CH–BS distance 38.11 m; 100 distinct nodes served as CH, the most frequent one 67 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 20 | 43.72 | 83.27 | 0.5 | 33.86 | 22 |
| 55 | 45.58 | 20.24 | 0.5 | 30.09 | 21 |
| 60 | 58.41 | 64.98 | 0.5 | 17.18 | 21 |
| 66 | 58.11 | 34.69 | 0.5 | 17.33 | 18 |
| 70 | 48.67 | 49.07 | 0.5 | 1.626 | 18 |


## Reproducing this experiment

```
python main.py reproduce "C:\Users\Admin\Hybrid-GWO-ABC-WSN\results\scenarios\S1_100nodes"
```

`config.json` holds every parameter; `experiment.json` holds the algorithms, run count and seeds.

## Data-quality note

Runtime values in this folder were measured with 11 simulations running in parallel, so they include scheduling noise; see `results/runtime_benchmark/report.md` for a clean sequential runtime comparison.
