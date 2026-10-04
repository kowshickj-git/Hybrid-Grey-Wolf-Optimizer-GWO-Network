# Scenario S5_100nodes_BS_outside

100 nodes, 100x100 m, BS outside the field (50, 175)

All numbers below were produced by the simulator in this folder (10 independent paired runs per algorithm; run r uses deployment/algorithm seed 42 + r). Raw per-run results: `runs_raw.csv`; per-round histories: `history_raw.csv.gz`; statistics: `statistics.csv`; proposed-vs-baseline tests: `improvement_vs_baselines.csv`.

## Configuration

| Parameter | Value |
|---|---|
| Nodes | 100 |
| Area (m) | 100 x 100 |
| BS position | (50, 175) |
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

| Metric | LEACH | GWO | ABC | Hybrid GWO-ABC |
|---|---:|---:|---:|---:|
| FND (rounds) | 703 ± 32 | 963 ± 17 | 962 ± 17 | 963 ± 18 |
| HND (rounds) | 895 ± 30 | 979 ± 18 | 978 ± 18 | 978 ± 18 |
| LND (rounds) | 1,218 ± 22 | 991 ± 18 | 990 ± 19 | 989 ± 18 |
| Residual Energy (J) | 22.506 ± 0.633 | 24.399 ± 0.483 | 24.396 ± 0.483 | 24.385 ± 0.482 |
| Energy Consumption (J) | 27.494 ± 0.633 | 25.601 ± 0.483 | 25.604 ± 0.483 | 25.615 ± 0.482 |
| Throughput (packets) | 90,375 ± 2,305 | 97,520 ± 1,796 | 97,526 ± 1,834 | 97,454 ± 1,801 |
| PDR (ratio) | 0.9896 ± 0.0025 | 0.9966 ± 0.0008 | 0.9972 ± 0.0011 | 0.9969 ± 0.0011 |
| Avg. Cluster Distance (m) | 26.840 ± 0.727 | 23.432 ± 0.895 | 23.277 ± 0.912 | 23.328 ± 0.881 |
| Avg. CH-BS Distance (m) | 129.030 ± 4.009 | 121.256 ± 4.326 | 121.520 ± 4.323 | 121.606 ± 4.280 |
| Runtime (s) | 0.05 ± 0.00 | 42.62 ± 2.87 | 76.74 ± 8.04 | 100.61 ± 9.79 |
| Final Fitness (-) | 1.3036 ± 0.1561 | 0.2430 ± 0.0090 | 0.2390 ± 0.0083 | 0.2364 ± 0.0090 |

Residual energy and energy consumption are measured at the checkpoint round 500; distance, imbalance and fitness averages cover rounds 1–500. '≥' marks lifetime values where at least one run had not reached the event within 2000 rounds (the horizon is then used as a lower bound).

## Descriptive statistics

**FND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 703 | 32 | 631 | 738 |
| GWO | 10 | 963 | 17 | 929 | 983 |
| ABC | 10 | 962 | 17 | 926 | 978 |
| Hybrid GWO-ABC | 10 | 963 | 18 | 926 | 983 |

**HND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 895 | 30 | 836 | 945 |
| GWO | 10 | 979 | 18 | 943 | 998 |
| ABC | 10 | 978 | 18 | 942 | 998 |
| Hybrid GWO-ABC | 10 | 978 | 18 | 941 | 996 |

**LND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 1,218 | 22 | 1,185 | 1,254 |
| GWO | 10 | 991 | 18 | 952 | 1,010 |
| ABC | 10 | 990 | 19 | 950 | 1,009 |
| Hybrid GWO-ABC | 10 | 989 | 18 | 952 | 1,008 |

**Residual Energy (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 22.506 | 0.633 | 21.081 | 23.123 |
| GWO | 10 | 24.399 | 0.483 | 23.389 | 24.873 |
| ABC | 10 | 24.396 | 0.483 | 23.374 | 24.880 |
| Hybrid GWO-ABC | 10 | 24.385 | 0.482 | 23.370 | 24.867 |

**Energy Consumption (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 27.494 | 0.633 | 26.877 | 28.919 |
| GWO | 10 | 25.601 | 0.483 | 25.127 | 26.611 |
| ABC | 10 | 25.604 | 0.483 | 25.120 | 26.626 |
| Hybrid GWO-ABC | 10 | 25.615 | 0.482 | 25.133 | 26.630 |

**Throughput (packets)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 90,375 | 2,305 | 85,300 | 92,752 |
| GWO | 10 | 97,520 | 1,796 | 93,765 | 99,321 |
| ABC | 10 | 97,526 | 1,834 | 93,633 | 99,276 |
| Hybrid GWO-ABC | 10 | 97,454 | 1,801 | 93,694 | 99,330 |

**PDR (ratio)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 0.9896 | 0.0025 | 0.9860 | 0.9932 |
| GWO | 10 | 0.9966 | 0.0008 | 0.9956 | 0.9978 |
| ABC | 10 | 0.9972 | 0.0011 | 0.9956 | 0.9988 |
| Hybrid GWO-ABC | 10 | 0.9969 | 0.0011 | 0.9950 | 0.9988 |

**Runtime (s)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 0.05 | 0.00 | 0.04 | 0.06 |
| GWO | 10 | 42.62 | 2.87 | 39.45 | 46.00 |
| ABC | 10 | 76.74 | 8.04 | 59.58 | 86.37 |
| Hybrid GWO-ABC | 10 | 100.61 | 9.79 | 77.08 | 112.51 |

## Hybrid GWO-ABC vs baselines

Improvement % uses ((P − B) / B) × 100 for higher-is-better metrics and ((B − P) / B) × 100 for lower-is-better metrics, so a positive value always means the proposed algorithm did better. p-values: paired two-sided Wilcoxon signed-rank test, Holm-corrected over the baselines. Cliff's δ > 0 favours the proposed algorithm (|δ| < 0.147 negligible, < 0.33 small, < 0.474 medium, otherwise large).

| Metric | Baseline | Better | Improvement % | p (Holm) | Cliff's δ | Effect | Verdict |
|---|---|---|---:|---:|---:|---|---|
| FND | LEACH | higher | +37.03 | 0.00586 | +1.00 | large | proposed better |
| FND | GWO | higher | +0.04 | 0.594 | +0.04 | negligible | no significant difference |
| FND | ABC | higher | +0.19 | 0.0625 | +0.12 | negligible | no significant difference |
| HND | LEACH | higher | +9.23 | 0.00586 | +0.98 | large | proposed better |
| HND | GWO | higher | -0.14 | 0.00781 | -0.10 | negligible | proposed worse |
| HND | ABC | higher | -0.10 | 0.0273 | -0.08 | negligible | proposed worse |
| LND | LEACH | higher | -18.75 | 0.00586 | -1.00 | large | proposed worse |
| LND | GWO | higher | -0.13 | 0.219 | -0.09 | negligible | no significant difference |
| LND | ABC | higher | -0.06 | 0.227 | -0.06 | negligible | no significant difference |
| Node-rounds | LEACH | higher | +7.05 | 0.00586 | +1.00 | large | proposed better |
| Node-rounds | GWO | higher | -0.10 | 0.00781 | -0.10 | negligible | proposed worse |
| Node-rounds | ABC | higher | -0.05 | 0.084 | -0.04 | negligible | no significant difference |
| Residual Energy | LEACH | higher | +8.35 | 0.00586 | +1.00 | large | proposed better |
| Residual Energy | GWO | higher | -0.06 | 0.0391 | -0.06 | negligible | proposed worse |
| Residual Energy | ABC | higher | -0.05 | 0.084 | -0.06 | negligible | no significant difference |
| Energy Consumption | LEACH | lower | +6.83 | 0.00586 | +1.00 | large | proposed better |
| Energy Consumption | GWO | lower | -0.06 | 0.0391 | -0.06 | negligible | proposed worse |
| Energy Consumption | ABC | lower | -0.04 | 0.084 | -0.06 | negligible | no significant difference |
| Throughput | LEACH | higher | +7.83 | 0.00586 | +1.00 | large | proposed better |
| Throughput | GWO | higher | -0.07 | 0.129 | -0.02 | negligible | no significant difference |
| Throughput | ABC | higher | -0.07 | 0.129 | -0.04 | negligible | no significant difference |
| PDR | LEACH | higher | +0.74 | 0.00586 | +1.00 | large | proposed better |
| PDR | GWO | higher | +0.03 | 0.75 | +0.22 | small | no significant difference |
| PDR | ABC | higher | -0.03 | 0.922 | -0.10 | negligible | no significant difference |
| Avg. Cluster Distance | LEACH | lower | +13.08 | 0.00586 | +1.00 | large | proposed better |
| Avg. Cluster Distance | GWO | lower | +0.44 | 0.0117 | +0.14 | negligible | proposed better |
| Avg. Cluster Distance | ABC | lower | -0.22 | 0.105 | -0.04 | negligible | no significant difference |
| Avg. CH-BS Distance | LEACH | lower | +5.75 | 0.00586 | +0.72 | large | proposed better |
| Avg. CH-BS Distance | GWO | lower | -0.29 | 0.00781 | -0.16 | small | proposed worse |
| Avg. CH-BS Distance | ABC | lower | -0.07 | 0.232 | -0.08 | negligible | no significant difference |
| Final Fitness | LEACH | lower | +81.87 | 0.00586 | +1.00 | large | proposed better |
| Final Fitness | GWO | lower | +2.71 | 0.00586 | +0.52 | large | proposed better |
| Final Fitness | ABC | lower | +1.11 | 0.00586 | +0.30 | small | proposed better |
| Runtime | LEACH | lower | -204338.71 | 0.00586 | -1.00 | large | proposed worse |
| Runtime | GWO | lower | -136.09 | 0.00586 | -1.00 | large | proposed worse |
| Runtime | ABC | lower | -31.11 | 0.00586 | -0.90 | large | proposed worse |

### Trade-offs

- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+37.03%), HND (+9.23%), Node-rounds (+7.05%), Residual Energy (+8.35%), Energy Consumption (+6.83%), Throughput (+7.83%), PDR (+0.74%, < 1%: practically negligible), Avg. Cluster Distance (+13.08%), Avg. CH-BS Distance (+5.75%), Cluster Imbalance (+69.05%), Final Fitness (+81.87%); significantly worse: LND (-18.75%), Runtime (-204338.71%), Runtime / round (-251333.64%); no significant difference: Fitness Evaluations.
- **Hybrid GWO-ABC vs GWO** — significantly better: Avg. Cluster Distance (+0.44%, < 1%: practically negligible), Cluster Imbalance (+24.55%), Final Fitness (+2.71%); significantly worse: HND (-0.14%, < 1%: practically negligible), Node-rounds (-0.10%, < 1%: practically negligible), Residual Energy (-0.06%, < 1%: practically negligible), Energy Consumption (-0.06%, < 1%: practically negligible), Avg. CH-BS Distance (-0.29%, < 1%: practically negligible), Runtime (-136.09%), Runtime / round (-136.12%), Fitness Evaluations (-0.81%, < 1%: practically negligible); no significant difference: FND, LND, Throughput, PDR.
- **Hybrid GWO-ABC vs ABC** — significantly better: Cluster Imbalance (+10.58%), Final Fitness (+1.11%); significantly worse: HND (-0.10%, < 1%: practically negligible), Runtime (-31.11%), Runtime / round (-31.16%), Fitness Evaluations (-0.30%, < 1%: practically negligible); no significant difference: FND, LND, Node-rounds, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance, Avg. CH-BS Distance.

## Figures

### Initial WSN topology (run 0; every algorithm uses this same network in run 0).

![Initial WSN topology (run 0; every algorithm uses this same network in run 0).](01_topology.png)

**Observed:** 100 nodes uniformly deployed in 100 x 100 m (seed 42); BS at (50, 175). Mean node–BS distance 126.5 m (max 176.8 m); d0 = 87.7 m, so 92% of nodes would use the multipath (d^4) model for a direct BS transmission.

### LEACH: cluster heads selected in round 1 (run 0).

![LEACH: cluster heads selected in round 1 (run 0).](02_ch_selection_LEACH.png)

**Observed:** 4 CHs; mean CH–BS distance 99.3 m.

### LEACH: cluster formation in round 1 (members joined the nearest CH).

![LEACH: cluster formation in round 1 (members joined the nearest CH).](03_clusters_LEACH.png)

**Observed:** 4 clusters, sizes 17–34 (CV 0.27); member→CH distance mean 36.8 m, max 91.2 m.

### LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_LEACH.png)

**Observed:** Round 912: 51 dead, 49 alive. Mean distance to BS — dead nodes 147.8 m, alive nodes 104.3 m (far nodes died first on average).

### GWO: cluster heads selected in round 1 (run 0).

![GWO: cluster heads selected in round 1 (run 0).](02_ch_selection_GWO.png)

**Observed:** 5 CHs; mean CH–BS distance 123.3 m.

### GWO: cluster formation in round 1 (members joined the nearest CH).

![GWO: cluster formation in round 1 (members joined the nearest CH).](03_clusters_GWO.png)

**Observed:** 5 clusters, sizes 17–23 (CV 0.11); member→CH distance mean 19.9 m, max 37.7 m.

### GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_GWO.png)

**Observed:** Round 994: 50 dead, 50 alive. Mean distance to BS — dead nodes 139.9 m, alive nodes 113.1 m (far nodes died first on average).

### ABC: cluster heads selected in round 1 (run 0).

![ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_ABC.png)

**Observed:** 5 CHs; mean CH–BS distance 122.5 m.

### ABC: cluster formation in round 1 (members joined the nearest CH).

![ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_ABC.png)

**Observed:** 5 clusters, sizes 18–22 (CV 0.06); member→CH distance mean 19.0 m, max 40.5 m.

### ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_ABC.png)

**Observed:** Round 994: 54 dead, 46 alive. Mean distance to BS — dead nodes 136.4 m, alive nodes 114.9 m (far nodes died first on average).

### Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).

![Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_GWO-ABC.png)

**Observed:** 5 CHs; mean CH–BS distance 121.7 m.

### Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).

![Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_GWO-ABC.png)

**Observed:** 5 clusters, sizes 18–21 (CV 0.05); member→CH distance mean 18.2 m, max 44.4 m.

### Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).

![Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).](04_communication_Hybrid_GWO-ABC.png)

**Observed:** 5 clusters, sizes 18–21 (CV 0.05); member→CH distance mean 18.2 m, max 44.4 m.

### Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_GWO-ABC.png)

**Observed:** Round 993: 51 dead, 49 alive. Mean distance to BS — dead nodes 140.3 m, alive nodes 112.2 m (far nodes died first on average).

### GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_GWO.png)

**Observed:** mean best fitness 0.2463 → 0.2121 (13.9% lower); 95% of the improvement reached by iteration 17

### ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_ABC.png)

**Observed:** mean best fitness 0.2579 → 0.2084 (19.2% lower); 95% of the improvement reached by iteration 24

### Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_GWO-ABC.png)

**Observed:** GWO: mean best fitness 0.2579 → 0.2048 (20.6% lower); 95% of the improvement reached by iteration 16; ABC: mean best fitness 0.2737 → 0.2048 (25.2% lower); 95% of the improvement reached by iteration 14; HYBRID: mean best fitness 0.2530 → 0.2048 (19.1% lower); 95% of the improvement reached by iteration 17

### Alive nodes vs rounds.

![Alive nodes vs rounds.](09_alive_vs_rounds.png)

**Observed:** LEACH: FND 703, HND 895, LND 1218; GWO: FND 963, HND 979, LND 991; ABC: FND 962, HND 978, LND 990; Hybrid GWO-ABC: FND 963, HND 978, LND 989

### Dead nodes vs rounds.

![Dead nodes vs rounds.](10_dead_vs_rounds.png)

**Observed:** Mirror image of the alive-nodes curve; a steeper rise means nodes die closer together.

### Residual energy vs rounds.

![Residual energy vs rounds.](11_residual_energy_vs_rounds.png)

**Observed:** Residual energy at round 500: LEACH 22.51 J; GWO 24.40 J; ABC 24.40 J; Hybrid GWO-ABC 24.38 J

### Energy consumption vs rounds.

![Energy consumption vs rounds.](12_consumed_energy_vs_rounds.png)

**Observed:** Consumed by round 500: LEACH 27.49 J; GWO 25.60 J; ABC 25.60 J; Hybrid GWO-ABC 25.62 J

### Throughput vs rounds (cumulative).

![Throughput vs rounds (cumulative).](13_packets_delivered_vs_rounds.png)

**Observed:** Total delivered: LEACH 90,375; GWO 97,520; ABC 97,526; Hybrid GWO-ABC 97,454

### PDR vs rounds.

![PDR vs rounds.](14_pdr_vs_rounds.png)

**Observed:** Final PDR: LEACH 0.9896; GWO 0.9966; ABC 0.9972; Hybrid GWO-ABC 0.9969

### CH count vs rounds (20-round rolling mean).

![CH count vs rounds (20-round rolling mean).](15_ch_count_vs_rounds.png)

**Observed:** Mean CHs/round (rounds 1–500): LEACH 5.00 (per-round std 2.17); GWO 4.94 (per-round std 0.34); ABC 4.95 (per-round std 0.30); Hybrid GWO-ABC 4.94 (per-round std 0.34)

### Average cluster distance vs rounds (20-round rolling mean).

![Average cluster distance vs rounds (20-round rolling mean).](16_avg_intra_distance_vs_rounds.png)

**Observed:** Mean member→CH distance: LEACH 26.84 m; GWO 23.43 m; ABC 23.28 m; Hybrid GWO-ABC 23.33 m

### Total CH-selection runtime per simulation (log scale, mean ± std).

![Total CH-selection runtime per simulation (log scale, mean ± std).](17_runtime.png)

**Observed:** LEACH 0.05 s (0.04 ms/round, 0 fitness evaluations); GWO 42.62 s (43.04 ms/round, 614,172 fitness evaluations); ABC 76.74 s (77.48 ms/round, 617,280 fitness evaluations); Hybrid GWO-ABC 100.61 s (101.62 ms/round, 619,136 fitness evaluations)

### FND / HND / LND comparison (mean ± std over runs).

![FND / HND / LND comparison (mean ± std over runs).](18_lifetime_fnd_hnd_lnd.png)

**Observed:** LEACH: FND 703, HND 895, LND 1218; GWO: FND 963, HND 979, LND 991; ABC: FND 962, HND 978, LND 990; Hybrid GWO-ABC: FND 963, HND 978, LND 989

### Where the energy goes: mean energy per radio activity over rounds 1–500.

![Where the energy goes: mean energy per radio activity over rounds 1–500.](19_energy_breakdown.png)

**Observed:** LEACH: total 27.49 J, largest share member TX (41%); GWO: total 25.60 J, largest share member TX (43%); ABC: total 25.60 J, largest share member TX (42%); Hybrid GWO-ABC: total 25.62 J, largest share member TX (42%)

### Final fitness: same objective and weights for every algorithm.

![Final fitness: same objective and weights for every algorithm.](20_final_fitness.png)

**Observed:** LEACH 1.3036; GWO 0.2430; ABC 0.2390; Hybrid GWO-ABC 0.2364

## Metric-by-metric interpretation

#### FND
- **What it represents:** First Node Death: the round in which the first node's residual energy reached 0.
- **How it was calculated:** min over nodes of the round in which residual energy reached 0 (simulation horizon if none died). (higher is better, unit: rounds)
- **Why it matters:** Marks the end of the stability period, during which every sensor still reports.
- **Observed (mean ± std over runs):** LEACH 703 (± 32), GWO 963 (± 17), ABC 962 (± 17), Hybrid GWO-ABC 963 (± 18). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 37.03% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.04% better (improvement formula), p = 0.594 (Holm), Cliff's δ = +0.04 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.19% better (improvement formula), p = 0.0625 (Holm), Cliff's δ = +0.12 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** CH selection that avoids low-energy nodes and rotates the CH role evenly delays the first death; a node chosen repeatedly as CH (e.g. because it is close to the BS) dies early. Measured LND − FND spread (rounds): LEACH 515, GWO 28, ABC 28, Hybrid GWO-ABC 26.

#### HND
- **What it represents:** Half Node Death: the round in which at least 50% of the nodes were dead.
- **How it was calculated:** round in which the number of dead nodes reached ceil(N/2). (higher is better, unit: rounds)
- **Why it matters:** Indicates how long the network keeps useful coverage.
- **Observed (mean ± std over runs):** LEACH 895 (± 30), GWO 979 (± 18), ABC 978 (± 18), Hybrid GWO-ABC 978 (± 18). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 9.23% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +0.98 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.14% worse (improvement formula), p = 0.00781 (Holm), Cliff's δ = -0.10 (negligible) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.10% worse (improvement formula), p = 0.0273 (Holm), Cliff's δ = -0.08 (negligible) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** HND reflects how evenly energy is drained across the whole network.

#### LND
- **What it represents:** Last Node Death: the round in which the last alive node died.
- **How it was calculated:** round in which the last node died (simulation horizon if nodes were still alive). (higher is better, unit: rounds)
- **Why it matters:** Upper bound of the network lifetime.
- **Observed (mean ± std over runs):** LEACH 1,218 (± 22), GWO 991 (± 18), ABC 990 (± 19), Hybrid GWO-ABC 989 (± 18). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 18.75% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs GWO: Hybrid GWO-ABC is 0.13% worse (improvement formula), p = 0.219 (Holm), Cliff's δ = -0.09 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.06% worse (improvement formula), p = 0.227 (Holm), Cliff's δ = -0.06 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** A very even energy drain makes all nodes die at nearly the same time: FND is delayed but the last node also dies sooner. Uneven drain leaves a few nodes with spare energy that keep running. Measured LND − FND spread (rounds): LEACH 515, GWO 28, ABC 28, Hybrid GWO-ABC 26.

#### Residual Energy
- **What it represents:** Total residual energy of all nodes at the checkpoint round.
- **How it was calculated:** sum of node residual energies after the checkpoint round. (higher is better, unit: J)
- **Why it matters:** More energy left at the same round means cheaper operation.
- **Observed (mean ± std over runs):** LEACH 22.506 (± 0.633), GWO 24.399 (± 0.483), ABC 24.396 (± 0.483), Hybrid GWO-ABC 24.385 (± 0.482). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 8.35% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.06% worse (improvement formula), p = 0.0391 (Holm), Cliff's δ = -0.06 (negligible) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.084 (Holm), Cliff's δ = -0.06 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Residual energy at a fixed round depends on per-round radio cost: shorter member->CH links and shorter or fewer CH->BS links consume less.

#### Energy Consumption
- **What it represents:** Initial total energy minus residual energy at the checkpoint round.
- **How it was calculated:** N * E0 - residual energy at the checkpoint round. (lower is better, unit: J)
- **Why it matters:** Energy spent to operate the network for the same number of rounds.
- **Observed (mean ± std over runs):** LEACH 27.494 (± 0.633), GWO 25.601 (± 0.483), ABC 25.604 (± 0.483), Hybrid GWO-ABC 25.615 (± 0.482). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 6.83% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.06% worse (reduction formula), p = 0.0391 (Holm), Cliff's δ = -0.06 (negligible) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.04% worse (reduction formula), p = 0.084 (Holm), Cliff's δ = -0.06 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Consumption is the complement of residual energy at the same checkpoint.

#### Throughput
- **What it represents:** Total sensor data packets delivered to the BS over the whole simulation (directly or inside an aggregated CH packet).
- **How it was calculated:** count of sensor readings that reached the BS over the whole run. (higher is better, unit: packets)
- **Why it matters:** Amount of sensed data the application actually receives.
- **Observed (mean ± std over runs):** LEACH 90,375 (± 2,305), GWO 97,520 (± 1,796), ABC 97,526 (± 1,834), Hybrid GWO-ABC 97,454 (± 1,801). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 7.83% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.07% worse (improvement formula), p = 0.129 (Holm), Cliff's δ = -0.02 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.07% worse (improvement formula), p = 0.129 (Holm), Cliff's δ = -0.04 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Throughput grows with the number of rounds in which nodes are alive and with the share of packets that are not lost to CHs dying mid-round.

#### PDR
- **What it represents:** Packet Delivery Ratio = delivered data packets / generated data packets.
- **How it was calculated:** delivered readings / generated readings over the whole run. (higher is better, unit: ratio)
- **Why it matters:** Reliability: share of generated readings that reach the BS.
- **Observed (mean ± std over runs):** LEACH 0.9896 (± 0.0025), GWO 0.9966 (± 0.0008), ABC 0.9972 (± 0.0011), Hybrid GWO-ABC 0.9969 (± 0.0011). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 0.74% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better** — practically small; vs GWO: Hybrid GWO-ABC is 0.03% better (improvement formula), p = 0.75 (Holm), Cliff's δ = +0.22 (small) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.03% worse (improvement formula), p = 0.922 (Holm), Cliff's δ = -0.10 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Packets are lost when a CH runs out of energy before forwarding its cluster's data, or when a node dies while transmitting. Energy-feasibility checks on CHs reduce such losses.

#### Avg. Cluster Distance
- **What it represents:** Mean member->CH distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean member->CH distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** Shorter intra-cluster links cost less transmission energy (d^2 / d^4).
- **Observed (mean ± std over runs):** LEACH 26.840 (± 0.727), GWO 23.432 (± 0.895), ABC 23.277 (± 0.912), Hybrid GWO-ABC 23.328 (± 0.881). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 13.08% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.44% better (reduction formula), p = 0.0117 (Holm), Cliff's δ = +0.14 (negligible) → **proposed better** — practically small; vs ABC: Hybrid GWO-ABC is 0.22% worse (reduction formula), p = 0.105 (Holm), Cliff's δ = -0.04 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness function explicitly penalises member->CH distance; LEACH places CHs at random positions, which typically lengthens member links.

#### Avg. CH-BS Distance
- **What it represents:** Mean CH->BS distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean CH->BS distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** CH->BS is the longest and most expensive hop.
- **Observed (mean ± std over runs):** LEACH 129.030 (± 4.009), GWO 121.256 (± 4.326), ABC 121.520 (± 4.323), Hybrid GWO-ABC 121.606 (± 4.280). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 5.75% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.72 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.29% worse (reduction formula), p = 0.00781 (Holm), Cliff's δ = -0.16 (small) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.07% worse (reduction formula), p = 0.232 (Holm), Cliff's δ = -0.08 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises CH->BS distance, but the energy-eligibility rule and the energy term limit how often nodes near the BS can be selected.

#### Runtime
- **What it represents:** Total wall-clock time spent selecting CHs over the whole simulation.
- **How it was calculated:** sum of wall-clock CH-selection time over all rounds (time.perf_counter). (lower is better, unit: s)
- **Why it matters:** Computational cost of the CH selection algorithm.
- **Observed (mean ± std over runs):** LEACH 0.05 (± 0.00), GWO 42.62 (± 2.87), ABC 76.74 (± 8.04), Hybrid GWO-ABC 100.61 (± 9.79). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 204338.71% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse** (proposed/baseline ratio 2044×); vs GWO: Hybrid GWO-ABC is 136.09% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs ABC: Hybrid GWO-ABC is 31.11% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.90 (large) → **proposed worse**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Metaheuristics evaluate hundreds of candidate CH sets per round; LEACH needs one random draw per node. The hybrid runs two populations and more operators per iteration, which adds overhead even at an equal number of fitness evaluations. Runtime relative to LEACH: GWO 866×, ABC 1559×, Hybrid GWO-ABC 2044×.

#### Final Fitness
- **What it represents:** Mean per-round fitness (same function and weights for every algorithm) of the CH set actually used, over rounds 1..checkpoint. Lower is better.
- **How it was calculated:** per round fitness of the CH set used (same weights for all), mean over rounds 1..checkpoint. (lower is better, unit: -)
- **Why it matters:** Quality of the CH configurations according to the optimisation objective.
- **Observed (mean ± std over runs):** LEACH 1.3036 (± 0.1561), GWO 0.2430 (± 0.0090), ABC 0.2390 (± 0.0083), Hybrid GWO-ABC 0.2364 (± 0.0090). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 81.87% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 2.71% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.52 (large) → **proposed better**; vs ABC: Hybrid GWO-ABC is 1.11% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.30 (small) → **proposed better**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Optimisers minimise this objective directly; LEACH does not use it, and rounds in which LEACH elects zero CHs or too many receive the invalid-solution penalty.

#### Node-rounds
- **What it represents:** Sum over rounds of the number of alive nodes (area under the alive-nodes curve).
- **How it was calculated:** sum over rounds of alive nodes. (higher is better, unit: node x rounds)
- **Why it matters:** Single-number lifetime measure that accounts for the whole death curve.
- **Observed (mean ± std over runs):** LEACH 91,223 (± 2,142), GWO 97,748 (± 1,817), ABC 97,699 (± 1,803), Hybrid GWO-ABC 97,652 (± 1,791). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 7.05% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.10% worse (improvement formula), p = 0.00781 (Holm), Cliff's δ = -0.10 (negligible) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.084 (Holm), Cliff's δ = -0.04 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The area under the alive-nodes curve combines stability period and tail length.

#### Cluster Imbalance
- **What it represents:** Coefficient of variation of cluster sizes, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round std/mean of cluster sizes, averaged over rounds 1..checkpoint. (lower is better, unit: CV)
- **Why it matters:** Balanced clusters spread the CH load evenly.
- **Observed (mean ± std over runs):** LEACH 0.4490 (± 0.0084), GWO 0.1842 (± 0.0085), ABC 0.1554 (± 0.0136), Hybrid GWO-ABC 0.1390 (± 0.0148). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 69.05% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 24.55% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs ABC: Hybrid GWO-ABC is 10.58% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.60 (large) → **proposed better**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises unequal cluster sizes; nearest-CH assignment does not.

## Cluster-head records (run 0)

Every selected CH of every round is recorded in `ch_log_run0.csv` (round, CH id, coordinates, residual energy at selection, distance to the BS, cluster size including the CH). Dead and duplicate CHs are removed before clustering, so only valid CHs appear.

**Reproducibility check:** run 0 of every algorithm was re-simulated from `config.json` and its seed; all checked results (fnd, hnd, lnd, node_rounds, throughput_packets, packets_generated, residual_energy_cp, final_fitness) are identical to the saved values (`reproducibility_check_run0.csv`).

### LEACH

Over 1069 rounds with CHs: 4.37 CHs/round on average; mean CH residual energy at selection 0.2566 J; mean CH–BS distance 123.36 m; 100 distinct nodes served as CH, the most frequent one 61 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 27 | 70.52 | 78.07 | 0.5 | 99.07 | 29 |
| 51 | 26.59 | 96.92 | 0.5 | 81.52 | 20 |
| 68 | 95.86 | 48.23 | 0.5 | 134.8 | 34 |
| 84 | 31.71 | 95.29 | 0.5 | 81.78 | 17 |

### GWO

Over 1006 rounds with CHs: 4.88 CHs/round on average; mean CH residual energy at selection 0.2546 J; mean CH–BS distance 118.24 m; 100 distinct nodes served as CH, the most frequent one 86 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 59 | 43.21 | 62.73 | 0.5 | 112.5 | 18 |
| 75 | 82.63 | 89.62 | 0.5 | 91.41 | 20 |
| 77 | 10.86 | 67.22 | 0.5 | 114.7 | 17 |
| 94 | 74.68 | 26.25 | 0.5 | 150.8 | 23 |
| 99 | 19.64 | 31.03 | 0.5 | 147.1 | 22 |

### ABC

Over 1006 rounds with CHs: 4.90 CHs/round on average; mean CH residual energy at selection 0.2545 J; mean CH–BS distance 118.31 m; 100 distinct nodes served as CH, the most frequent one 87 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 28 | 45.89 | 56.87 | 0.5 | 118.2 | 20 |
| 30 | 66.84 | 47.11 | 0.5 | 129 | 18 |
| 83 | 82.98 | 80.83 | 0.5 | 99.78 | 20 |
| 93 | 37.37 | 9.447 | 0.5 | 166 | 22 |
| 96 | 12.28 | 83.11 | 0.5 | 99.33 | 20 |

### Hybrid GWO-ABC

Over 1005 rounds with CHs: 4.88 CHs/round on average; mean CH residual energy at selection 0.2546 J; mean CH–BS distance 118.55 m; 100 distinct nodes served as CH, the most frequent one 85 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 3 | 76.11 | 78.61 | 0.5 | 99.87 | 20 |
| 40 | 66.43 | 40.64 | 0.5 | 135.4 | 20 |
| 57 | 17.68 | 85.66 | 0.5 | 95.01 | 18 |
| 59 | 43.21 | 62.73 | 0.5 | 112.5 | 21 |
| 93 | 37.37 | 9.447 | 0.5 | 166 | 21 |


## Reproducing this experiment

```
python main.py reproduce "C:\Users\Admin\Hybrid-GWO-ABC-WSN\results\scenarios\S5_100nodes_BS_outside"
```

`config.json` holds every parameter; `experiment.json` holds the algorithms, run count and seeds.

## Data-quality note

Runtime values in this folder were measured with 11 simulations running in parallel, so they include scheduling noise; see `results/runtime_benchmark/report.md` for a clean sequential runtime comparison.
