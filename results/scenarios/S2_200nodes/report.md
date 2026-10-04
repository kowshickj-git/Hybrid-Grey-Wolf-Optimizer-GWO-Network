# Scenario S2_200nodes

200 nodes, 100x100 m, BS at the centre (50, 50)

All numbers below were produced by the simulator in this folder (10 independent paired runs per algorithm; run r uses deployment/algorithm seed 42 + r). Raw per-run results: `runs_raw.csv`; per-round histories: `history_raw.csv.gz`; statistics: `statistics.csv`; proposed-vs-baseline tests: `improvement_vs_baselines.csv`.

## Configuration

| Parameter | Value |
|---|---|
| Nodes | 200 |
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

| Metric | LEACH | GWO | ABC | Hybrid GWO-ABC |
|---|---:|---:|---:|---:|
| FND (rounds) | 921 ± 35 | 1,164 ± 3 | 1,162 ± 5 | 1,162 ± 6 |
| HND (rounds) | 1,148 ± 8 | 1,176 ± 3 | 1,175 ± 3 | 1,174 ± 2 |
| LND (rounds) | 1,401 ± 42 | 1,215 ± 28 | 1,205 ± 23 | 1,200 ± 14 |
| Residual Energy (J) | 56.926 ± 0.051 | 57.514 ± 0.066 | 57.507 ± 0.054 | 57.473 ± 0.072 |
| Energy Consumption (J) | 43.074 ± 0.051 | 42.486 ± 0.066 | 42.493 ± 0.054 | 42.527 ± 0.072 |
| Throughput (packets) | 228,269 ± 447 | 234,517 ± 538 | 234,452 ± 481 | 234,130 ± 639 |
| PDR (ratio) | 0.9881 ± 0.0009 | 0.9971 ± 0.0008 | 0.9971 ± 0.0005 | 0.9966 ± 0.0006 |
| Avg. Cluster Distance (m) | 18.155 ± 0.248 | 15.505 ± 0.339 | 15.496 ± 0.284 | 15.713 ± 0.361 |
| Avg. CH-BS Distance (m) | 38.128 ± 0.401 | 37.825 ± 0.348 | 37.935 ± 0.350 | 37.703 ± 0.320 |
| Runtime (s) | 0.08 ± 0.01 | 93.55 ± 11.90 | 141.80 ± 15.66 | 176.52 ± 25.55 |
| Final Fitness (-) | 1.0819 ± 0.1169 | 0.2259 ± 0.0076 | 0.2311 ± 0.0086 | 0.2230 ± 0.0083 |

Residual energy and energy consumption are measured at the checkpoint round 500; distance, imbalance and fitness averages cover rounds 1–500. '≥' marks lifetime values where at least one run had not reached the event within 2000 rounds (the horizon is then used as a lower bound).

## Descriptive statistics

**FND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 921 | 35 | 849 | 970 |
| GWO | 10 | 1,164 | 3 | 1,158 | 1,167 |
| ABC | 10 | 1,162 | 5 | 1,154 | 1,168 |
| Hybrid GWO-ABC | 10 | 1,162 | 6 | 1,151 | 1,167 |

**HND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 1,148 | 8 | 1,136 | 1,160 |
| GWO | 10 | 1,176 | 3 | 1,171 | 1,179 |
| ABC | 10 | 1,175 | 3 | 1,171 | 1,179 |
| Hybrid GWO-ABC | 10 | 1,174 | 2 | 1,171 | 1,177 |

**LND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 1,401 | 42 | 1,355 | 1,481 |
| GWO | 10 | 1,215 | 28 | 1,192 | 1,272 |
| ABC | 10 | 1,205 | 23 | 1,188 | 1,267 |
| Hybrid GWO-ABC | 10 | 1,200 | 14 | 1,187 | 1,232 |

**Residual Energy (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 56.926 | 0.051 | 56.876 | 57.011 |
| GWO | 10 | 57.514 | 0.066 | 57.381 | 57.589 |
| ABC | 10 | 57.507 | 0.054 | 57.399 | 57.567 |
| Hybrid GWO-ABC | 10 | 57.473 | 0.072 | 57.327 | 57.539 |

**Energy Consumption (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 43.074 | 0.051 | 42.989 | 43.124 |
| GWO | 10 | 42.486 | 0.066 | 42.411 | 42.619 |
| ABC | 10 | 42.493 | 0.054 | 42.433 | 42.601 |
| Hybrid GWO-ABC | 10 | 42.527 | 0.072 | 42.461 | 42.673 |

**Throughput (packets)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 228,269 | 447 | 227,642 | 229,198 |
| GWO | 10 | 234,517 | 538 | 233,340 | 235,073 |
| ABC | 10 | 234,452 | 481 | 233,512 | 235,011 |
| Hybrid GWO-ABC | 10 | 234,130 | 639 | 233,000 | 234,718 |

**PDR (ratio)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 0.9881 | 0.0009 | 0.9869 | 0.9901 |
| GWO | 10 | 0.9971 | 0.0008 | 0.9956 | 0.9982 |
| ABC | 10 | 0.9971 | 0.0005 | 0.9958 | 0.9977 |
| Hybrid GWO-ABC | 10 | 0.9966 | 0.0006 | 0.9954 | 0.9975 |

**Runtime (s)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 0.08 | 0.01 | 0.07 | 0.11 |
| GWO | 10 | 93.55 | 11.90 | 63.76 | 102.15 |
| ABC | 10 | 141.80 | 15.66 | 104.92 | 155.93 |
| Hybrid GWO-ABC | 10 | 176.52 | 25.55 | 118.94 | 197.31 |

## Hybrid GWO-ABC vs baselines

Improvement % uses ((P − B) / B) × 100 for higher-is-better metrics and ((B − P) / B) × 100 for lower-is-better metrics, so a positive value always means the proposed algorithm did better. p-values: paired two-sided Wilcoxon signed-rank test, Holm-corrected over the baselines. Cliff's δ > 0 favours the proposed algorithm (|δ| < 0.147 negligible, < 0.33 small, < 0.474 medium, otherwise large).

| Metric | Baseline | Better | Improvement % | p (Holm) | Cliff's δ | Effect | Verdict |
|---|---|---|---:|---:|---:|---|---|
| FND | LEACH | higher | +26.10 | 0.00586 | +1.00 | large | proposed better |
| FND | GWO | higher | -0.21 | 0.234 | -0.11 | negligible | no significant difference |
| FND | ABC | higher | -0.04 | 0.789 | +0.04 | negligible | no significant difference |
| HND | LEACH | higher | +2.25 | 0.00586 | +1.00 | large | proposed better |
| HND | GWO | higher | -0.10 | 0.0312 | -0.29 | small | proposed worse |
| HND | ABC | higher | -0.09 | 0.0312 | -0.28 | small | proposed worse |
| LND | LEACH | higher | -14.32 | 0.00586 | -1.00 | large | proposed worse |
| LND | GWO | higher | -1.19 | 0.00781 | -0.34 | medium | proposed worse |
| LND | ABC | higher | -0.42 | 0.133 | -0.12 | negligible | no significant difference |
| Node-rounds | LEACH | higher | +1.70 | 0.00586 | +1.00 | large | proposed better |
| Node-rounds | GWO | higher | -0.11 | 0.00586 | -0.36 | medium | proposed worse |
| Node-rounds | ABC | higher | -0.09 | 0.00586 | -0.34 | medium | proposed worse |
| Residual Energy | LEACH | higher | +0.96 | 0.00586 | +1.00 | large | proposed better |
| Residual Energy | GWO | higher | -0.07 | 0.00586 | -0.38 | medium | proposed worse |
| Residual Energy | ABC | higher | -0.06 | 0.00586 | -0.36 | medium | proposed worse |
| Energy Consumption | LEACH | lower | +1.27 | 0.00586 | +1.00 | large | proposed better |
| Energy Consumption | GWO | lower | -0.10 | 0.00586 | -0.38 | medium | proposed worse |
| Energy Consumption | ABC | lower | -0.08 | 0.00586 | -0.36 | medium | proposed worse |
| Throughput | LEACH | higher | +2.57 | 0.00586 | +1.00 | large | proposed better |
| Throughput | GWO | higher | -0.17 | 0.00586 | -0.38 | medium | proposed worse |
| Throughput | ABC | higher | -0.14 | 0.00586 | -0.34 | medium | proposed worse |
| PDR | LEACH | higher | +0.86 | 0.00586 | +1.00 | large | proposed better |
| PDR | GWO | higher | -0.05 | 0.0742 | -0.38 | medium | no significant difference |
| PDR | ABC | higher | -0.05 | 0.084 | -0.54 | large | no significant difference |
| Avg. Cluster Distance | LEACH | lower | +13.45 | 0.00586 | +1.00 | large | proposed better |
| Avg. Cluster Distance | GWO | lower | -1.34 | 0.00586 | -0.46 | medium | proposed worse |
| Avg. Cluster Distance | ABC | lower | -1.40 | 0.00586 | -0.46 | medium | proposed worse |
| Avg. CH-BS Distance | LEACH | lower | +1.11 | 0.00586 | +0.64 | large | proposed better |
| Avg. CH-BS Distance | GWO | lower | +0.32 | 0.00586 | +0.24 | small | proposed better |
| Avg. CH-BS Distance | ABC | lower | +0.61 | 0.00586 | +0.38 | medium | proposed better |
| Final Fitness | LEACH | lower | +79.39 | 0.00586 | +1.00 | large | proposed better |
| Final Fitness | GWO | lower | +1.31 | 0.00586 | +0.18 | small | proposed better |
| Final Fitness | ABC | lower | +3.53 | 0.00586 | +0.50 | large | proposed better |
| Runtime | LEACH | lower | -218939.38 | 0.00586 | -1.00 | large | proposed worse |
| Runtime | GWO | lower | -88.70 | 0.00586 | -1.00 | large | proposed worse |
| Runtime | ABC | lower | -24.48 | 0.00586 | -0.72 | large | proposed worse |

### Trade-offs

- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+26.10%), HND (+2.25%), Node-rounds (+1.70%), Residual Energy (+0.96%, < 1%: practically negligible), Energy Consumption (+1.27%), Throughput (+2.57%), PDR (+0.86%, < 1%: practically negligible), Avg. Cluster Distance (+13.45%), Avg. CH-BS Distance (+1.11%), Cluster Imbalance (+67.32%), Final Fitness (+79.39%); significantly worse: LND (-14.32%), Runtime (-218939.38%), Runtime / round (-255548.94%); no significant difference: Fitness Evaluations.
- **Hybrid GWO-ABC vs GWO** — significantly better: Avg. CH-BS Distance (+0.32%, < 1%: practically negligible), Cluster Imbalance (+16.87%), Final Fitness (+1.31%), Fitness Evaluations (+0.86%, < 1%: practically negligible); significantly worse: HND (-0.10%, < 1%: practically negligible), LND (-1.19%), Node-rounds (-0.11%, < 1%: practically negligible), Residual Energy (-0.07%, < 1%: practically negligible), Energy Consumption (-0.10%, < 1%: practically negligible), Throughput (-0.17%, < 1%: practically negligible), Avg. Cluster Distance (-1.34%), Runtime (-88.70%), Runtime / round (-90.97%); no significant difference: FND, PDR.
- **Hybrid GWO-ABC vs ABC** — significantly better: Avg. CH-BS Distance (+0.61%, < 1%: practically negligible), Cluster Imbalance (+19.08%), Final Fitness (+3.53%); significantly worse: HND (-0.09%, < 1%: practically negligible), Node-rounds (-0.09%, < 1%: practically negligible), Residual Energy (-0.06%, < 1%: practically negligible), Energy Consumption (-0.08%, < 1%: practically negligible), Throughput (-0.14%, < 1%: practically negligible), Avg. Cluster Distance (-1.40%), Runtime (-24.48%), Runtime / round (-25.04%); no significant difference: FND, LND, PDR, Fitness Evaluations.

## Figures

### Initial WSN topology (run 0; every algorithm uses this same network in run 0).

![Initial WSN topology (run 0; every algorithm uses this same network in run 0).](01_topology.png)

**Observed:** 200 nodes uniformly deployed in 100 x 100 m (seed 42); BS at (50, 50). Mean node–BS distance 37.8 m (max 62.9 m); d0 = 87.7 m, so 0% of nodes would use the multipath (d^4) model for a direct BS transmission.

### LEACH: cluster heads selected in round 1 (run 0).

![LEACH: cluster heads selected in round 1 (run 0).](02_ch_selection_LEACH.png)

**Observed:** 9 CHs; mean CH–BS distance 38.7 m.

### LEACH: cluster formation in round 1 (members joined the nearest CH).

![LEACH: cluster formation in round 1 (members joined the nearest CH).](03_clusters_LEACH.png)

**Observed:** 9 clusters, sizes 9–44 (CV 0.52); member→CH distance mean 16.5 m, max 37.2 m.

### LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_LEACH.png)

**Observed:** Round 1157: 101 dead, 99 alive. Mean distance to BS — dead nodes 29.3 m, alive nodes 46.4 m (near nodes died first on average).

### GWO: cluster heads selected in round 1 (run 0).

![GWO: cluster heads selected in round 1 (run 0).](02_ch_selection_GWO.png)

**Observed:** 10 CHs; mean CH–BS distance 33.1 m.

### GWO: cluster formation in round 1 (members joined the nearest CH).

![GWO: cluster formation in round 1 (members joined the nearest CH).](03_clusters_GWO.png)

**Observed:** 10 clusters, sizes 17–24 (CV 0.13); member→CH distance mean 16.0 m, max 38.3 m.

### GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_GWO.png)

**Observed:** Round 1179: 108 dead, 92 alive. Mean distance to BS — dead nodes 35.4 m, alive nodes 40.6 m (near nodes died first on average).

### ABC: cluster heads selected in round 1 (run 0).

![ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_ABC.png)

**Observed:** 9 CHs; mean CH–BS distance 31.0 m.

### ABC: cluster formation in round 1 (members joined the nearest CH).

![ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_ABC.png)

**Observed:** 9 clusters, sizes 19–26 (CV 0.12); member→CH distance mean 15.6 m, max 38.8 m.

### ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_ABC.png)

**Observed:** Round 1179: 111 dead, 89 alive. Mean distance to BS — dead nodes 35.5 m, alive nodes 40.6 m (near nodes died first on average).

### Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).

![Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_GWO-ABC.png)

**Observed:** 10 CHs; mean CH–BS distance 31.6 m.

### Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).

![Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_GWO-ABC.png)

**Observed:** 10 clusters, sizes 16–24 (CV 0.11); member→CH distance mean 13.9 m, max 32.6 m.

### Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).

![Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).](04_communication_Hybrid_GWO-ABC.png)

**Observed:** 10 clusters, sizes 16–24 (CV 0.11); member→CH distance mean 13.9 m, max 32.6 m.

### Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_GWO-ABC.png)

**Observed:** Round 1176: 102 dead, 98 alive. Mean distance to BS — dead nodes 33.7 m, alive nodes 42.0 m (near nodes died first on average).

### GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_GWO.png)

**Observed:** mean best fitness 0.2328 → 0.1909 (18.0% lower); 95% of the improvement reached by iteration 19

### ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_ABC.png)

**Observed:** mean best fitness 0.2404 → 0.1884 (21.6% lower); 95% of the improvement reached by iteration 22

### Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_GWO-ABC.png)

**Observed:** GWO: mean best fitness 0.2404 → 0.1770 (26.4% lower); 95% of the improvement reached by iteration 22; ABC: mean best fitness 0.2518 → 0.1770 (29.7% lower); 95% of the improvement reached by iteration 20; HYBRID: mean best fitness 0.2375 → 0.1770 (25.5% lower); 95% of the improvement reached by iteration 22

### Alive nodes vs rounds.

![Alive nodes vs rounds.](09_alive_vs_rounds.png)

**Observed:** LEACH: FND 921, HND 1148, LND 1401; GWO: FND 1164, HND 1176, LND 1215; ABC: FND 1162, HND 1175, LND 1205; Hybrid GWO-ABC: FND 1162, HND 1174, LND 1200

### Dead nodes vs rounds.

![Dead nodes vs rounds.](10_dead_vs_rounds.png)

**Observed:** Mirror image of the alive-nodes curve; a steeper rise means nodes die closer together.

### Residual energy vs rounds.

![Residual energy vs rounds.](11_residual_energy_vs_rounds.png)

**Observed:** Residual energy at round 500: LEACH 56.93 J; GWO 57.51 J; ABC 57.51 J; Hybrid GWO-ABC 57.47 J

### Energy consumption vs rounds.

![Energy consumption vs rounds.](12_consumed_energy_vs_rounds.png)

**Observed:** Consumed by round 500: LEACH 43.07 J; GWO 42.49 J; ABC 42.49 J; Hybrid GWO-ABC 42.53 J

### Throughput vs rounds (cumulative).

![Throughput vs rounds (cumulative).](13_packets_delivered_vs_rounds.png)

**Observed:** Total delivered: LEACH 228,269; GWO 234,517; ABC 234,452; Hybrid GWO-ABC 234,130

### PDR vs rounds.

![PDR vs rounds.](14_pdr_vs_rounds.png)

**Observed:** Final PDR: LEACH 0.9881; GWO 0.9971; ABC 0.9971; Hybrid GWO-ABC 0.9966

### CH count vs rounds (20-round rolling mean).

![CH count vs rounds (20-round rolling mean).](15_ch_count_vs_rounds.png)

**Observed:** Mean CHs/round (rounds 1–500): LEACH 10.00 (per-round std 3.13); GWO 9.85 (per-round std 0.58); ABC 9.74 (per-round std 0.83); Hybrid GWO-ABC 9.74 (per-round std 0.73)

### Average cluster distance vs rounds (20-round rolling mean).

![Average cluster distance vs rounds (20-round rolling mean).](16_avg_intra_distance_vs_rounds.png)

**Observed:** Mean member→CH distance: LEACH 18.16 m; GWO 15.50 m; ABC 15.50 m; Hybrid GWO-ABC 15.71 m

### Total CH-selection runtime per simulation (log scale, mean ± std).

![Total CH-selection runtime per simulation (log scale, mean ± std).](17_runtime.png)

**Observed:** LEACH 0.08 s (0.06 ms/round, 0 fitness evaluations); GWO 93.55 s (77.03 ms/round, 753,114 fitness evaluations); ABC 141.80 s (117.65 ms/round, 744,880 fitness evaluations); Hybrid GWO-ABC 176.52 s (147.10 ms/round, 746,660 fitness evaluations)

### FND / HND / LND comparison (mean ± std over runs).

![FND / HND / LND comparison (mean ± std over runs).](18_lifetime_fnd_hnd_lnd.png)

**Observed:** LEACH: FND 921, HND 1148, LND 1401; GWO: FND 1164, HND 1176, LND 1215; ABC: FND 1162, HND 1175, LND 1205; Hybrid GWO-ABC: FND 1162, HND 1174, LND 1200

### Where the energy goes: mean energy per radio activity over rounds 1–500.

![Where the energy goes: mean energy per radio activity over rounds 1–500.](19_energy_breakdown.png)

**Observed:** LEACH: total 43.07 J, largest share member TX (48%); GWO: total 42.49 J, largest share member TX (47%); ABC: total 42.49 J, largest share member TX (47%); Hybrid GWO-ABC: total 42.53 J, largest share member TX (48%)

### Final fitness: same objective and weights for every algorithm.

![Final fitness: same objective and weights for every algorithm.](20_final_fitness.png)

**Observed:** LEACH 1.0819; GWO 0.2259; ABC 0.2311; Hybrid GWO-ABC 0.2230

## Metric-by-metric interpretation

#### FND
- **What it represents:** First Node Death: the round in which the first node's residual energy reached 0.
- **How it was calculated:** min over nodes of the round in which residual energy reached 0 (simulation horizon if none died). (higher is better, unit: rounds)
- **Why it matters:** Marks the end of the stability period, during which every sensor still reports.
- **Observed (mean ± std over runs):** LEACH 921 (± 35), GWO 1,164 (± 3), ABC 1,162 (± 5), Hybrid GWO-ABC 1,162 (± 6). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 26.10% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.21% worse (improvement formula), p = 0.234 (Holm), Cliff's δ = -0.11 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.04% worse (improvement formula), p = 0.789 (Holm), Cliff's δ = +0.04 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** CH selection that avoids low-energy nodes and rotates the CH role evenly delays the first death; a node chosen repeatedly as CH (e.g. because it is close to the BS) dies early. Measured LND − FND spread (rounds): LEACH 480, GWO 51, ABC 43, Hybrid GWO-ABC 39.

#### HND
- **What it represents:** Half Node Death: the round in which at least 50% of the nodes were dead.
- **How it was calculated:** round in which the number of dead nodes reached ceil(N/2). (higher is better, unit: rounds)
- **Why it matters:** Indicates how long the network keeps useful coverage.
- **Observed (mean ± std over runs):** LEACH 1,148 (± 8), GWO 1,176 (± 3), ABC 1,175 (± 3), Hybrid GWO-ABC 1,174 (± 2). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 2.25% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.10% worse (improvement formula), p = 0.0312 (Holm), Cliff's δ = -0.29 (small) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.09% worse (improvement formula), p = 0.0312 (Holm), Cliff's δ = -0.28 (small) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** HND reflects how evenly energy is drained across the whole network.

#### LND
- **What it represents:** Last Node Death: the round in which the last alive node died.
- **How it was calculated:** round in which the last node died (simulation horizon if nodes were still alive). (higher is better, unit: rounds)
- **Why it matters:** Upper bound of the network lifetime.
- **Observed (mean ± std over runs):** LEACH 1,401 (± 42), GWO 1,215 (± 28), ABC 1,205 (± 23), Hybrid GWO-ABC 1,200 (± 14). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 14.32% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs GWO: Hybrid GWO-ABC is 1.19% worse (improvement formula), p = 0.00781 (Holm), Cliff's δ = -0.34 (medium) → **proposed worse**; vs ABC: Hybrid GWO-ABC is 0.42% worse (improvement formula), p = 0.133 (Holm), Cliff's δ = -0.12 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** A very even energy drain makes all nodes die at nearly the same time: FND is delayed but the last node also dies sooner. Uneven drain leaves a few nodes with spare energy that keep running. Measured LND − FND spread (rounds): LEACH 480, GWO 51, ABC 43, Hybrid GWO-ABC 39.

#### Residual Energy
- **What it represents:** Total residual energy of all nodes at the checkpoint round.
- **How it was calculated:** sum of node residual energies after the checkpoint round. (higher is better, unit: J)
- **Why it matters:** More energy left at the same round means cheaper operation.
- **Observed (mean ± std over runs):** LEACH 56.926 (± 0.051), GWO 57.514 (± 0.066), ABC 57.507 (± 0.054), Hybrid GWO-ABC 57.473 (± 0.072). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 0.96% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better** — practically small; vs GWO: Hybrid GWO-ABC is 0.07% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -0.38 (medium) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.06% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -0.36 (medium) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Residual energy at a fixed round depends on per-round radio cost: shorter member->CH links and shorter or fewer CH->BS links consume less.

#### Energy Consumption
- **What it represents:** Initial total energy minus residual energy at the checkpoint round.
- **How it was calculated:** N * E0 - residual energy at the checkpoint round. (lower is better, unit: J)
- **Why it matters:** Energy spent to operate the network for the same number of rounds.
- **Observed (mean ± std over runs):** LEACH 43.074 (± 0.051), GWO 42.486 (± 0.066), ABC 42.493 (± 0.054), Hybrid GWO-ABC 42.527 (± 0.072). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 1.27% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.10% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.38 (medium) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.08% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.36 (medium) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Consumption is the complement of residual energy at the same checkpoint.

#### Throughput
- **What it represents:** Total sensor data packets delivered to the BS over the whole simulation (directly or inside an aggregated CH packet).
- **How it was calculated:** count of sensor readings that reached the BS over the whole run. (higher is better, unit: packets)
- **Why it matters:** Amount of sensed data the application actually receives.
- **Observed (mean ± std over runs):** LEACH 228,269 (± 447), GWO 234,517 (± 538), ABC 234,452 (± 481), Hybrid GWO-ABC 234,130 (± 639). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 2.57% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.17% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -0.38 (medium) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.14% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -0.34 (medium) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Throughput grows with the number of rounds in which nodes are alive and with the share of packets that are not lost to CHs dying mid-round.

#### PDR
- **What it represents:** Packet Delivery Ratio = delivered data packets / generated data packets.
- **How it was calculated:** delivered readings / generated readings over the whole run. (higher is better, unit: ratio)
- **Why it matters:** Reliability: share of generated readings that reach the BS.
- **Observed (mean ± std over runs):** LEACH 0.9881 (± 0.0009), GWO 0.9971 (± 0.0008), ABC 0.9971 (± 0.0005), Hybrid GWO-ABC 0.9966 (± 0.0006). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 0.86% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better** — practically small; vs GWO: Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.0742 (Holm), Cliff's δ = -0.38 (medium) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.084 (Holm), Cliff's δ = -0.54 (large) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Packets are lost when a CH runs out of energy before forwarding its cluster's data, or when a node dies while transmitting. Energy-feasibility checks on CHs reduce such losses.

#### Avg. Cluster Distance
- **What it represents:** Mean member->CH distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean member->CH distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** Shorter intra-cluster links cost less transmission energy (d^2 / d^4).
- **Observed (mean ± std over runs):** LEACH 18.155 (± 0.248), GWO 15.505 (± 0.339), ABC 15.496 (± 0.284), Hybrid GWO-ABC 15.713 (± 0.361). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 13.45% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 1.34% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.46 (medium) → **proposed worse**; vs ABC: Hybrid GWO-ABC is 1.40% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.46 (medium) → **proposed worse**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness function explicitly penalises member->CH distance; LEACH places CHs at random positions, which typically lengthens member links.

#### Avg. CH-BS Distance
- **What it represents:** Mean CH->BS distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean CH->BS distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** CH->BS is the longest and most expensive hop.
- **Observed (mean ± std over runs):** LEACH 38.128 (± 0.401), GWO 37.825 (± 0.348), ABC 37.935 (± 0.350), Hybrid GWO-ABC 37.703 (± 0.320). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 1.11% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.64 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.32% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.24 (small) → **proposed better** — practically small; vs ABC: Hybrid GWO-ABC is 0.61% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.38 (medium) → **proposed better** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises CH->BS distance, but the energy-eligibility rule and the energy term limit how often nodes near the BS can be selected.

#### Runtime
- **What it represents:** Total wall-clock time spent selecting CHs over the whole simulation.
- **How it was calculated:** sum of wall-clock CH-selection time over all rounds (time.perf_counter). (lower is better, unit: s)
- **Why it matters:** Computational cost of the CH selection algorithm.
- **Observed (mean ± std over runs):** LEACH 0.08 (± 0.01), GWO 93.55 (± 11.90), ABC 141.80 (± 15.66), Hybrid GWO-ABC 176.52 (± 25.55). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 218939.38% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse** (proposed/baseline ratio 2190×); vs GWO: Hybrid GWO-ABC is 88.70% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs ABC: Hybrid GWO-ABC is 24.48% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.72 (large) → **proposed worse**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Metaheuristics evaluate hundreds of candidate CH sets per round; LEACH needs one random draw per node. The hybrid runs two populations and more operators per iteration, which adds overhead even at an equal number of fitness evaluations. Runtime relative to LEACH: GWO 1161×, ABC 1760×, Hybrid GWO-ABC 2190×.

#### Final Fitness
- **What it represents:** Mean per-round fitness (same function and weights for every algorithm) of the CH set actually used, over rounds 1..checkpoint. Lower is better.
- **How it was calculated:** per round fitness of the CH set used (same weights for all), mean over rounds 1..checkpoint. (lower is better, unit: -)
- **Why it matters:** Quality of the CH configurations according to the optimisation objective.
- **Observed (mean ± std over runs):** LEACH 1.0819 (± 0.1169), GWO 0.2259 (± 0.0076), ABC 0.2311 (± 0.0086), Hybrid GWO-ABC 0.2230 (± 0.0083). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 79.39% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 1.31% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.18 (small) → **proposed better**; vs ABC: Hybrid GWO-ABC is 3.53% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.50 (large) → **proposed better**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Optimisers minimise this objective directly; LEACH does not use it, and rounds in which LEACH elects zero CHs or too many receive the invalid-solution penalty.

#### Node-rounds
- **What it represents:** Sum over rounds of the number of alive nodes (area under the alive-nodes curve).
- **How it was calculated:** sum over rounds of alive nodes. (higher is better, unit: node x rounds)
- **Why it matters:** Single-number lifetime measure that accounts for the whole death curve.
- **Observed (mean ± std over runs):** LEACH 230,817 (± 411), GWO 235,001 (± 487), ABC 234,939 (± 454), Hybrid GWO-ABC 234,731 (± 540). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 1.70% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.11% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -0.36 (medium) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.09% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -0.34 (medium) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The area under the alive-nodes curve combines stability period and tail length.

#### Cluster Imbalance
- **What it represents:** Coefficient of variation of cluster sizes, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round std/mean of cluster sizes, averaged over rounds 1..checkpoint. (lower is better, unit: CV)
- **Why it matters:** Balanced clusters spread the CH load evenly.
- **Observed (mean ± std over runs):** LEACH 0.5253 (± 0.0052), GWO 0.2065 (± 0.0095), ABC 0.2121 (± 0.0121), Hybrid GWO-ABC 0.1716 (± 0.0110). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 67.32% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 16.87% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs ABC: Hybrid GWO-ABC is 19.08% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.98 (large) → **proposed better**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises unequal cluster sizes; nearest-CH assignment does not.

## Cluster-head records (run 0)

Every selected CH of every round is recorded in `ch_log_run0.csv` (round, CH id, coordinates, residual energy at selection, distance to the BS, cluster size including the CH). Dead and duplicate CHs are removed before clustering, so only valid CHs appear.

**Reproducibility check:** run 0 of every algorithm was re-simulated from `config.json` and its seed; all checked results (fnd, hnd, lnd, node_rounds, throughput_packets, packets_generated, residual_energy_cp, final_fitness) are identical to the saved values (`reproducibility_check_run0.csv`).

### LEACH

Over 1309 rounds with CHs: 8.87 CHs/round on average; mean CH residual energy at selection 0.2543 J; mean CH–BS distance 38.60 m; 200 distinct nodes served as CH, the most frequent one 74 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 27 | 70.52 | 78.07 | 0.5 | 34.77 | 28 |
| 51 | 26.59 | 96.92 | 0.5 | 52.44 | 19 |
| 68 | 95.86 | 48.23 | 0.5 | 45.89 | 9 |
| 84 | 31.71 | 95.29 | 0.5 | 48.84 | 11 |
| 124 | 37.42 | 42.59 | 0.5 | 14.6 | 44 |
| 135 | 5.54 | 17.46 | 0.5 | 55.09 | 26 |
| 149 | 77.95 | 64.25 | 0.5 | 31.37 | 17 |
| 163 | 80.44 | 53.27 | 0.5 | 30.61 | 10 |
| 175 | 61.62 | 17.13 | 0.5 | 34.86 | 36 |

### GWO

Over 1193 rounds with CHs: 9.76 CHs/round on average; mean CH residual energy at selection 0.2526 J; mean CH–BS distance 37.88 m; 200 distinct nodes served as CH, the most frequent one 68 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 25 | 19.99 | 0.7362 | 0.5 | 57.68 | 22 |
| 34 | 3.082 | 43.67 | 0.5 | 47.34 | 22 |
| 43 | 72.24 | 46.19 | 0.5 | 22.56 | 17 |
| 46 | 44.62 | 38.1 | 0.5 | 13.06 | 17 |
| 60 | 58.41 | 64.98 | 0.5 | 17.18 | 18 |
| 66 | 58.11 | 34.69 | 0.5 | 17.33 | 17 |
| 137 | 68.07 | 39.36 | 0.5 | 20.97 | 21 |
| 147 | 84.36 | 90.27 | 0.5 | 52.93 | 24 |
| 158 | 37.95 | 68.57 | 0.5 | 22.14 | 23 |
| 169 | 8.449 | 93.59 | 0.5 | 60.22 | 19 |

### ABC

Over 1191 rounds with CHs: 9.68 CHs/round on average; mean CH residual energy at selection 0.2524 J; mean CH–BS distance 38.03 m; 200 distinct nodes served as CH, the most frequent one 71 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 66 | 58.11 | 34.69 | 0.5 | 17.33 | 20 |
| 70 | 48.67 | 49.07 | 0.5 | 1.626 | 19 |
| 75 | 82.63 | 89.62 | 0.5 | 51.32 | 22 |
| 76 | 14.02 | 55.4 | 0.5 | 36.38 | 25 |
| 91 | 51.89 | 31.59 | 0.5 | 18.5 | 24 |
| 92 | 77.2 | 66.17 | 0.5 | 31.64 | 20 |
| 96 | 12.28 | 83.11 | 0.5 | 50.19 | 25 |
| 99 | 19.64 | 31.03 | 0.5 | 35.8 | 26 |
| 152 | 85.76 | 46.28 | 0.5 | 35.95 | 19 |

### Hybrid GWO-ABC

Over 1194 rounds with CHs: 9.58 CHs/round on average; mean CH residual energy at selection 0.2524 J; mean CH–BS distance 37.81 m; 200 distinct nodes served as CH, the most frequent one 63 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 38 | 29.36 | 66.19 | 0.5 | 26.23 | 20 |
| 58 | 75.85 | 71.95 | 0.5 | 33.91 | 18 |
| 72 | 47.35 | 26.7 | 0.5 | 23.45 | 19 |
| 107 | 71.54 | 73.9 | 0.5 | 32.17 | 19 |
| 112 | 28.64 | 92.48 | 0.5 | 47.55 | 22 |
| 150 | 77.9 | 13.46 | 0.5 | 45.98 | 24 |
| 155 | 47.79 | 41.69 | 0.5 | 8.6 | 16 |
| 161 | 32.84 | 53.54 | 0.5 | 17.53 | 21 |
| 171 | 80.09 | 59.37 | 0.5 | 31.51 | 19 |
| 187 | 15.76 | 14.78 | 0.5 | 49.12 | 22 |


## Reproducing this experiment

```
python main.py reproduce "C:\Users\Admin\Hybrid-GWO-ABC-WSN\results\scenarios\S2_200nodes"
```

`config.json` holds every parameter; `experiment.json` holds the algorithms, run count and seeds.

## Data-quality note

Runtime values in this folder were measured with 11 simulations running in parallel, so they include scheduling noise; see `results/runtime_benchmark/report.md` for a clean sequential runtime comparison.
