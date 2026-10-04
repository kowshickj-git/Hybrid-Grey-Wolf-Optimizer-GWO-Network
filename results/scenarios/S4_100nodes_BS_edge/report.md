# Scenario S4_100nodes_BS_edge

100 nodes, 100x100 m, BS on the field edge (50, 100)

All numbers below were produced by the simulator in this folder (10 independent paired runs per algorithm; run r uses deployment/algorithm seed 42 + r). Raw per-run results: `runs_raw.csv`; per-round histories: `history_raw.csv.gz`; statistics: `statistics.csv`; proposed-vs-baseline tests: `improvement_vs_baselines.csv`.

## Configuration

| Parameter | Value |
|---|---|
| Nodes | 100 |
| Area (m) | 100 x 100 |
| BS position | (50, 100) |
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
| FND (rounds) | 876 ± 31 | 1,118 ± 7 | 1,117 ± 9 | 1,117 ± 5 |
| HND (rounds) | 1,091 ± 8 | 1,128 ± 6 | 1,128 ± 6 | 1,126 ± 5 |
| LND (rounds) | 1,345 ± 33 | 1,143 ± 9 | 1,139 ± 6 | 1,139 ± 7 |
| Residual Energy (J) | 27.117 ± 0.140 | 27.896 ± 0.090 | 27.900 ± 0.089 | 27.871 ± 0.084 |
| Energy Consumption (J) | 22.883 ± 0.140 | 22.104 ± 0.090 | 22.100 ± 0.089 | 22.129 ± 0.084 |
| Throughput (packets) | 107,609 ± 658 | 112,578 ± 512 | 112,631 ± 582 | 112,427 ± 557 |
| PDR (ratio) | 0.9885 ± 0.0019 | 0.9977 ± 0.0008 | 0.9982 ± 0.0005 | 0.9975 ± 0.0007 |
| Avg. Cluster Distance (m) | 26.840 ± 0.727 | 22.247 ± 0.715 | 22.205 ± 0.734 | 22.437 ± 0.724 |
| Avg. CH-BS Distance (m) | 59.730 ± 3.603 | 56.806 ± 3.770 | 56.993 ± 3.794 | 57.135 ± 3.805 |
| Runtime (s) | 0.05 ± 0.01 | 46.01 ± 2.51 | 83.01 ± 6.86 | 107.41 ± 12.09 |
| Final Fitness (-) | 1.2909 ± 0.1535 | 0.2337 ± 0.0149 | 0.2316 ± 0.0143 | 0.2296 ± 0.0154 |

Residual energy and energy consumption are measured at the checkpoint round 500; distance, imbalance and fitness averages cover rounds 1–500. '≥' marks lifetime values where at least one run had not reached the event within 2000 rounds (the horizon is then used as a lower bound).

## Descriptive statistics

**FND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 876 | 31 | 823 | 912 |
| GWO | 10 | 1,118 | 7 | 1,108 | 1,128 |
| ABC | 10 | 1,117 | 9 | 1,098 | 1,128 |
| Hybrid GWO-ABC | 10 | 1,117 | 5 | 1,106 | 1,124 |

**HND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 1,091 | 8 | 1,076 | 1,103 |
| GWO | 10 | 1,128 | 6 | 1,117 | 1,136 |
| ABC | 10 | 1,128 | 6 | 1,116 | 1,137 |
| Hybrid GWO-ABC | 10 | 1,126 | 5 | 1,115 | 1,134 |

**LND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 1,345 | 33 | 1,305 | 1,402 |
| GWO | 10 | 1,143 | 9 | 1,135 | 1,161 |
| ABC | 10 | 1,139 | 6 | 1,127 | 1,147 |
| Hybrid GWO-ABC | 10 | 1,139 | 7 | 1,125 | 1,147 |

**Residual Energy (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 27.117 | 0.140 | 26.903 | 27.334 |
| GWO | 10 | 27.896 | 0.090 | 27.771 | 28.046 |
| ABC | 10 | 27.900 | 0.089 | 27.761 | 28.049 |
| Hybrid GWO-ABC | 10 | 27.871 | 0.084 | 27.714 | 27.996 |

**Energy Consumption (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 22.883 | 0.140 | 22.666 | 23.097 |
| GWO | 10 | 22.104 | 0.090 | 21.954 | 22.229 |
| ABC | 10 | 22.100 | 0.089 | 21.951 | 22.239 |
| Hybrid GWO-ABC | 10 | 22.129 | 0.084 | 22.004 | 22.286 |

**Throughput (packets)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 107,609 | 658 | 106,538 | 108,369 |
| GWO | 10 | 112,578 | 512 | 111,732 | 113,404 |
| ABC | 10 | 112,631 | 582 | 111,464 | 113,460 |
| Hybrid GWO-ABC | 10 | 112,427 | 557 | 111,166 | 113,149 |

**PDR (ratio)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 0.9885 | 0.0019 | 0.9861 | 0.9919 |
| GWO | 10 | 0.9977 | 0.0008 | 0.9965 | 0.9986 |
| ABC | 10 | 0.9982 | 0.0005 | 0.9975 | 0.9989 |
| Hybrid GWO-ABC | 10 | 0.9975 | 0.0007 | 0.9964 | 0.9987 |

**Runtime (s)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 0.05 | 0.01 | 0.05 | 0.06 |
| GWO | 10 | 46.01 | 2.51 | 40.06 | 47.85 |
| ABC | 10 | 83.01 | 6.86 | 64.22 | 87.46 |
| Hybrid GWO-ABC | 10 | 107.41 | 12.09 | 78.14 | 115.57 |

## Hybrid GWO-ABC vs baselines

Improvement % uses ((P − B) / B) × 100 for higher-is-better metrics and ((B − P) / B) × 100 for lower-is-better metrics, so a positive value always means the proposed algorithm did better. p-values: paired two-sided Wilcoxon signed-rank test, Holm-corrected over the baselines. Cliff's δ > 0 favours the proposed algorithm (|δ| < 0.147 negligible, < 0.33 small, < 0.474 medium, otherwise large).

| Metric | Baseline | Better | Improvement % | p (Holm) | Cliff's δ | Effect | Verdict |
|---|---|---|---:|---:|---:|---|---|
| FND | LEACH | higher | +27.49 | 0.00586 | +1.00 | large | proposed better |
| FND | GWO | higher | -0.13 | 0.555 | -0.09 | negligible | no significant difference |
| FND | ABC | higher | +0.01 | 0.682 | -0.05 | negligible | no significant difference |
| HND | LEACH | higher | +3.24 | 0.00586 | +1.00 | large | proposed better |
| HND | GWO | higher | -0.11 | 0.0469 | -0.14 | negligible | proposed worse |
| HND | ABC | higher | -0.12 | 0.0469 | -0.17 | small | proposed worse |
| LND | LEACH | higher | -15.31 | 0.00586 | -1.00 | large | proposed worse |
| LND | GWO | higher | -0.32 | 0.109 | -0.20 | small | no significant difference |
| LND | ABC | higher | -0.02 | 0.406 | +0.00 | negligible | no significant difference |
| Node-rounds | LEACH | higher | +3.54 | 0.00586 | +1.00 | large | proposed better |
| Node-rounds | GWO | higher | -0.11 | 0.0273 | -0.10 | negligible | proposed worse |
| Node-rounds | ABC | higher | -0.11 | 0.0195 | -0.14 | negligible | proposed worse |
| Residual Energy | LEACH | higher | +2.78 | 0.00586 | +1.00 | large | proposed better |
| Residual Energy | GWO | higher | -0.09 | 0.0195 | -0.16 | small | proposed worse |
| Residual Energy | ABC | higher | -0.11 | 0.00781 | -0.18 | small | proposed worse |
| Energy Consumption | LEACH | lower | +3.30 | 0.00586 | +1.00 | large | proposed better |
| Energy Consumption | GWO | lower | -0.11 | 0.0195 | -0.16 | small | proposed worse |
| Energy Consumption | ABC | lower | -0.13 | 0.00781 | -0.18 | small | proposed worse |
| Throughput | LEACH | higher | +4.48 | 0.00586 | +1.00 | large | proposed better |
| Throughput | GWO | higher | -0.13 | 0.0645 | -0.18 | small | no significant difference |
| Throughput | ABC | higher | -0.18 | 0.0273 | -0.22 | small | proposed worse |
| PDR | LEACH | higher | +0.91 | 0.00586 | +1.00 | large | proposed better |
| PDR | GWO | higher | -0.02 | 0.557 | -0.14 | negligible | no significant difference |
| PDR | ABC | higher | -0.07 | 0.0742 | -0.58 | large | no significant difference |
| Avg. Cluster Distance | LEACH | lower | +16.41 | 0.00586 | +1.00 | large | proposed better |
| Avg. Cluster Distance | GWO | lower | -0.85 | 0.0137 | -0.16 | small | proposed worse |
| Avg. Cluster Distance | ABC | lower | -1.04 | 0.00781 | -0.16 | small | proposed worse |
| Avg. CH-BS Distance | LEACH | lower | +4.34 | 0.00586 | +0.46 | medium | proposed better |
| Avg. CH-BS Distance | GWO | lower | -0.58 | 0.00586 | -0.12 | negligible | proposed worse |
| Avg. CH-BS Distance | ABC | lower | -0.25 | 0.00586 | -0.08 | negligible | proposed worse |
| Final Fitness | LEACH | lower | +82.21 | 0.00586 | +1.00 | large | proposed better |
| Final Fitness | GWO | lower | +1.75 | 0.00586 | +0.22 | small | proposed better |
| Final Fitness | ABC | lower | +0.87 | 0.0195 | +0.10 | negligible | proposed better |
| Runtime | LEACH | lower | -204846.34 | 0.00586 | -1.00 | large | proposed worse |
| Runtime | GWO | lower | -133.48 | 0.00586 | -1.00 | large | proposed worse |
| Runtime | ABC | lower | -29.41 | 0.00586 | -0.82 | large | proposed worse |

### Trade-offs

- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+27.49%), HND (+3.24%), Node-rounds (+3.54%), Residual Energy (+2.78%), Energy Consumption (+3.30%), Throughput (+4.48%), PDR (+0.91%, < 1%: practically negligible), Avg. Cluster Distance (+16.41%), Avg. CH-BS Distance (+4.34%), Cluster Imbalance (+69.08%), Final Fitness (+82.21%); significantly worse: LND (-15.31%), Runtime (-204846.34%), Runtime / round (-241800.22%); no significant difference: Fitness Evaluations.
- **Hybrid GWO-ABC vs GWO** — significantly better: Cluster Imbalance (+20.88%), Final Fitness (+1.75%); significantly worse: HND (-0.11%, < 1%: practically negligible), Node-rounds (-0.11%, < 1%: practically negligible), Residual Energy (-0.09%, < 1%: practically negligible), Energy Consumption (-0.11%, < 1%: practically negligible), Avg. Cluster Distance (-0.85%, < 1%: practically negligible), Avg. CH-BS Distance (-0.58%, < 1%: practically negligible), Runtime (-133.48%), Runtime / round (-134.21%), Fitness Evaluations (-0.78%, < 1%: practically negligible); no significant difference: FND, LND, Throughput, PDR.
- **Hybrid GWO-ABC vs ABC** — significantly better: Cluster Imbalance (+9.16%), Final Fitness (+0.87%, < 1%: practically negligible); significantly worse: HND (-0.12%, < 1%: practically negligible), Node-rounds (-0.11%, < 1%: practically negligible), Residual Energy (-0.11%, < 1%: practically negligible), Energy Consumption (-0.13%, < 1%: practically negligible), Throughput (-0.18%, < 1%: practically negligible), Avg. Cluster Distance (-1.04%), Avg. CH-BS Distance (-0.25%, < 1%: practically negligible), Runtime (-29.41%), Runtime / round (-29.43%), Fitness Evaluations (-0.51%, < 1%: practically negligible); no significant difference: FND, LND, PDR.

## Figures

### Initial WSN topology (run 0; every algorithm uses this same network in run 0).

![Initial WSN topology (run 0; every algorithm uses this same network in run 0).](01_topology.png)

**Observed:** 100 nodes uniformly deployed in 100 x 100 m (seed 42); BS at (50, 100). Mean node–BS distance 57.8 m (max 103.7 m); d0 = 87.7 m, so 15% of nodes would use the multipath (d^4) model for a direct BS transmission.

### LEACH: cluster heads selected in round 1 (run 0).

![LEACH: cluster heads selected in round 1 (run 0).](02_ch_selection_LEACH.png)

**Observed:** 4 CHs; mean CH–BS distance 35.4 m.

### LEACH: cluster formation in round 1 (members joined the nearest CH).

![LEACH: cluster formation in round 1 (members joined the nearest CH).](03_clusters_LEACH.png)

**Observed:** 4 clusters, sizes 17–34 (CV 0.27); member→CH distance mean 36.8 m, max 91.2 m.

### LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_LEACH.png)

**Observed:** Round 1093: 50 dead, 50 alive. Mean distance to BS — dead nodes 57.1 m, alive nodes 58.4 m (near nodes died first on average).

### GWO: cluster heads selected in round 1 (run 0).

![GWO: cluster heads selected in round 1 (run 0).](02_ch_selection_GWO.png)

**Observed:** 5 CHs; mean CH–BS distance 52.6 m.

### GWO: cluster formation in round 1 (members joined the nearest CH).

![GWO: cluster formation in round 1 (members joined the nearest CH).](03_clusters_GWO.png)

**Observed:** 5 clusters, sizes 15–25 (CV 0.19); member→CH distance mean 19.9 m, max 37.7 m.

### GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_GWO.png)

**Observed:** Round 1136: 61 dead, 39 alive. Mean distance to BS — dead nodes 50.5 m, alive nodes 69.1 m (near nodes died first on average).

### ABC: cluster heads selected in round 1 (run 0).

![ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_ABC.png)

**Observed:** 5 CHs; mean CH–BS distance 46.2 m.

### ABC: cluster formation in round 1 (members joined the nearest CH).

![ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_ABC.png)

**Observed:** 5 clusters, sizes 19–21 (CV 0.04); member→CH distance mean 25.3 m, max 58.8 m.

### ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_ABC.png)

**Observed:** Round 1135: 58 dead, 42 alive. Mean distance to BS — dead nodes 49.9 m, alive nodes 68.6 m (near nodes died first on average).

### Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).

![Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_GWO-ABC.png)

**Observed:** 5 CHs; mean CH–BS distance 43.5 m.

### Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).

![Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_GWO-ABC.png)

**Observed:** 5 clusters, sizes 19–21 (CV 0.03); member→CH distance mean 26.7 m, max 62.5 m.

### Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).

![Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).](04_communication_Hybrid_GWO-ABC.png)

**Observed:** 5 clusters, sizes 19–21 (CV 0.03); member→CH distance mean 26.7 m, max 62.5 m.

### Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_GWO-ABC.png)

**Observed:** Round 1132: 50 dead, 50 alive. Mean distance to BS — dead nodes 47.9 m, alive nodes 67.7 m (near nodes died first on average).

### GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_GWO.png)

**Observed:** mean best fitness 0.2343 → 0.2039 (13.0% lower); 95% of the improvement reached by iteration 26

### ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_ABC.png)

**Observed:** mean best fitness 0.2476 → 0.1935 (21.8% lower); 95% of the improvement reached by iteration 21

### Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_GWO-ABC.png)

**Observed:** GWO: mean best fitness 0.2476 → 0.1912 (22.8% lower); 95% of the improvement reached by iteration 17; ABC: mean best fitness 0.2627 → 0.1912 (27.2% lower); 95% of the improvement reached by iteration 16; HYBRID: mean best fitness 0.2420 → 0.1912 (21.0% lower); 95% of the improvement reached by iteration 20

### Alive nodes vs rounds.

![Alive nodes vs rounds.](09_alive_vs_rounds.png)

**Observed:** LEACH: FND 876, HND 1091, LND 1345; GWO: FND 1118, HND 1128, LND 1143; ABC: FND 1117, HND 1128, LND 1139; Hybrid GWO-ABC: FND 1117, HND 1126, LND 1139

### Dead nodes vs rounds.

![Dead nodes vs rounds.](10_dead_vs_rounds.png)

**Observed:** Mirror image of the alive-nodes curve; a steeper rise means nodes die closer together.

### Residual energy vs rounds.

![Residual energy vs rounds.](11_residual_energy_vs_rounds.png)

**Observed:** Residual energy at round 500: LEACH 27.12 J; GWO 27.90 J; ABC 27.90 J; Hybrid GWO-ABC 27.87 J

### Energy consumption vs rounds.

![Energy consumption vs rounds.](12_consumed_energy_vs_rounds.png)

**Observed:** Consumed by round 500: LEACH 22.88 J; GWO 22.10 J; ABC 22.10 J; Hybrid GWO-ABC 22.13 J

### Throughput vs rounds (cumulative).

![Throughput vs rounds (cumulative).](13_packets_delivered_vs_rounds.png)

**Observed:** Total delivered: LEACH 107,609; GWO 112,578; ABC 112,631; Hybrid GWO-ABC 112,427

### PDR vs rounds.

![PDR vs rounds.](14_pdr_vs_rounds.png)

**Observed:** Final PDR: LEACH 0.9885; GWO 0.9977; ABC 0.9982; Hybrid GWO-ABC 0.9975

### CH count vs rounds (20-round rolling mean).

![CH count vs rounds (20-round rolling mean).](15_ch_count_vs_rounds.png)

**Observed:** Mean CHs/round (rounds 1–500): LEACH 5.00 (per-round std 2.17); GWO 4.94 (per-round std 0.34); ABC 4.94 (per-round std 0.35); Hybrid GWO-ABC 4.91 (per-round std 0.39)

### Average cluster distance vs rounds (20-round rolling mean).

![Average cluster distance vs rounds (20-round rolling mean).](16_avg_intra_distance_vs_rounds.png)

**Observed:** Mean member→CH distance: LEACH 26.84 m; GWO 22.25 m; ABC 22.21 m; Hybrid GWO-ABC 22.44 m

### Total CH-selection runtime per simulation (log scale, mean ± std).

![Total CH-selection runtime per simulation (log scale, mean ± std).](17_runtime.png)

**Observed:** LEACH 0.05 s (0.04 ms/round, 0 fitness evaluations); GWO 46.01 s (40.25 ms/round, 708,536 fitness evaluations); ABC 83.01 s (72.84 ms/round, 710,440 fitness evaluations); Hybrid GWO-ABC 107.41 s (94.28 ms/round, 714,040 fitness evaluations)

### FND / HND / LND comparison (mean ± std over runs).

![FND / HND / LND comparison (mean ± std over runs).](18_lifetime_fnd_hnd_lnd.png)

**Observed:** LEACH: FND 876, HND 1091, LND 1345; GWO: FND 1118, HND 1128, LND 1143; ABC: FND 1117, HND 1128, LND 1139; Hybrid GWO-ABC: FND 1117, HND 1126, LND 1139

### Where the energy goes: mean energy per radio activity over rounds 1–500.

![Where the energy goes: mean energy per radio activity over rounds 1–500.](19_energy_breakdown.png)

**Observed:** LEACH: total 22.88 J, largest share member TX (50%); GWO: total 22.10 J, largest share member TX (48%); ABC: total 22.10 J, largest share member TX (48%); Hybrid GWO-ABC: total 22.13 J, largest share member TX (48%)

### Final fitness: same objective and weights for every algorithm.

![Final fitness: same objective and weights for every algorithm.](20_final_fitness.png)

**Observed:** LEACH 1.2909; GWO 0.2337; ABC 0.2316; Hybrid GWO-ABC 0.2296

## Metric-by-metric interpretation

#### FND
- **What it represents:** First Node Death: the round in which the first node's residual energy reached 0.
- **How it was calculated:** min over nodes of the round in which residual energy reached 0 (simulation horizon if none died). (higher is better, unit: rounds)
- **Why it matters:** Marks the end of the stability period, during which every sensor still reports.
- **Observed (mean ± std over runs):** LEACH 876 (± 31), GWO 1,118 (± 7), ABC 1,117 (± 9), Hybrid GWO-ABC 1,117 (± 5). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 27.49% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.13% worse (improvement formula), p = 0.555 (Holm), Cliff's δ = -0.09 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.01% better (improvement formula), p = 0.682 (Holm), Cliff's δ = -0.05 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** CH selection that avoids low-energy nodes and rotates the CH role evenly delays the first death; a node chosen repeatedly as CH (e.g. because it is close to the BS) dies early. Measured LND − FND spread (rounds): LEACH 469, GWO 24, ABC 23, Hybrid GWO-ABC 22.

#### HND
- **What it represents:** Half Node Death: the round in which at least 50% of the nodes were dead.
- **How it was calculated:** round in which the number of dead nodes reached ceil(N/2). (higher is better, unit: rounds)
- **Why it matters:** Indicates how long the network keeps useful coverage.
- **Observed (mean ± std over runs):** LEACH 1,091 (± 8), GWO 1,128 (± 6), ABC 1,128 (± 6), Hybrid GWO-ABC 1,126 (± 5). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 3.24% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.11% worse (improvement formula), p = 0.0469 (Holm), Cliff's δ = -0.14 (negligible) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.12% worse (improvement formula), p = 0.0469 (Holm), Cliff's δ = -0.17 (small) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** HND reflects how evenly energy is drained across the whole network.

#### LND
- **What it represents:** Last Node Death: the round in which the last alive node died.
- **How it was calculated:** round in which the last node died (simulation horizon if nodes were still alive). (higher is better, unit: rounds)
- **Why it matters:** Upper bound of the network lifetime.
- **Observed (mean ± std over runs):** LEACH 1,345 (± 33), GWO 1,143 (± 9), ABC 1,139 (± 6), Hybrid GWO-ABC 1,139 (± 7). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 15.31% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs GWO: Hybrid GWO-ABC is 0.32% worse (improvement formula), p = 0.109 (Holm), Cliff's δ = -0.20 (small) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.02% worse (improvement formula), p = 0.406 (Holm), Cliff's δ = +0.00 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** A very even energy drain makes all nodes die at nearly the same time: FND is delayed but the last node also dies sooner. Uneven drain leaves a few nodes with spare energy that keep running. Measured LND − FND spread (rounds): LEACH 469, GWO 24, ABC 23, Hybrid GWO-ABC 22.

#### Residual Energy
- **What it represents:** Total residual energy of all nodes at the checkpoint round.
- **How it was calculated:** sum of node residual energies after the checkpoint round. (higher is better, unit: J)
- **Why it matters:** More energy left at the same round means cheaper operation.
- **Observed (mean ± std over runs):** LEACH 27.117 (± 0.140), GWO 27.896 (± 0.090), ABC 27.900 (± 0.089), Hybrid GWO-ABC 27.871 (± 0.084). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 2.78% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.09% worse (improvement formula), p = 0.0195 (Holm), Cliff's δ = -0.16 (small) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.11% worse (improvement formula), p = 0.00781 (Holm), Cliff's δ = -0.18 (small) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Residual energy at a fixed round depends on per-round radio cost: shorter member->CH links and shorter or fewer CH->BS links consume less.

#### Energy Consumption
- **What it represents:** Initial total energy minus residual energy at the checkpoint round.
- **How it was calculated:** N * E0 - residual energy at the checkpoint round. (lower is better, unit: J)
- **Why it matters:** Energy spent to operate the network for the same number of rounds.
- **Observed (mean ± std over runs):** LEACH 22.883 (± 0.140), GWO 22.104 (± 0.090), ABC 22.100 (± 0.089), Hybrid GWO-ABC 22.129 (± 0.084). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 3.30% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.11% worse (reduction formula), p = 0.0195 (Holm), Cliff's δ = -0.16 (small) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.13% worse (reduction formula), p = 0.00781 (Holm), Cliff's δ = -0.18 (small) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Consumption is the complement of residual energy at the same checkpoint.

#### Throughput
- **What it represents:** Total sensor data packets delivered to the BS over the whole simulation (directly or inside an aggregated CH packet).
- **How it was calculated:** count of sensor readings that reached the BS over the whole run. (higher is better, unit: packets)
- **Why it matters:** Amount of sensed data the application actually receives.
- **Observed (mean ± std over runs):** LEACH 107,609 (± 658), GWO 112,578 (± 512), ABC 112,631 (± 582), Hybrid GWO-ABC 112,427 (± 557). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 4.48% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.13% worse (improvement formula), p = 0.0645 (Holm), Cliff's δ = -0.18 (small) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.18% worse (improvement formula), p = 0.0273 (Holm), Cliff's δ = -0.22 (small) → **proposed worse** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Throughput grows with the number of rounds in which nodes are alive and with the share of packets that are not lost to CHs dying mid-round.

#### PDR
- **What it represents:** Packet Delivery Ratio = delivered data packets / generated data packets.
- **How it was calculated:** delivered readings / generated readings over the whole run. (higher is better, unit: ratio)
- **Why it matters:** Reliability: share of generated readings that reach the BS.
- **Observed (mean ± std over runs):** LEACH 0.9885 (± 0.0019), GWO 0.9977 (± 0.0008), ABC 0.9982 (± 0.0005), Hybrid GWO-ABC 0.9975 (± 0.0007). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 0.91% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better** — practically small; vs GWO: Hybrid GWO-ABC is 0.02% worse (improvement formula), p = 0.557 (Holm), Cliff's δ = -0.14 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.07% worse (improvement formula), p = 0.0742 (Holm), Cliff's δ = -0.58 (large) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Packets are lost when a CH runs out of energy before forwarding its cluster's data, or when a node dies while transmitting. Energy-feasibility checks on CHs reduce such losses.

#### Avg. Cluster Distance
- **What it represents:** Mean member->CH distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean member->CH distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** Shorter intra-cluster links cost less transmission energy (d^2 / d^4).
- **Observed (mean ± std over runs):** LEACH 26.840 (± 0.727), GWO 22.247 (± 0.715), ABC 22.205 (± 0.734), Hybrid GWO-ABC 22.437 (± 0.724). Best mean: **ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 16.41% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.85% worse (reduction formula), p = 0.0137 (Holm), Cliff's δ = -0.16 (small) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 1.04% worse (reduction formula), p = 0.00781 (Holm), Cliff's δ = -0.16 (small) → **proposed worse**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness function explicitly penalises member->CH distance; LEACH places CHs at random positions, which typically lengthens member links.

#### Avg. CH-BS Distance
- **What it represents:** Mean CH->BS distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean CH->BS distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** CH->BS is the longest and most expensive hop.
- **Observed (mean ± std over runs):** LEACH 59.730 (± 3.603), GWO 56.806 (± 3.770), ABC 56.993 (± 3.794), Hybrid GWO-ABC 57.135 (± 3.805). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 4.34% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.46 (medium) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.58% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.12 (negligible) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.25% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.08 (negligible) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises CH->BS distance, but the energy-eligibility rule and the energy term limit how often nodes near the BS can be selected.

#### Runtime
- **What it represents:** Total wall-clock time spent selecting CHs over the whole simulation.
- **How it was calculated:** sum of wall-clock CH-selection time over all rounds (time.perf_counter). (lower is better, unit: s)
- **Why it matters:** Computational cost of the CH selection algorithm.
- **Observed (mean ± std over runs):** LEACH 0.05 (± 0.01), GWO 46.01 (± 2.51), ABC 83.01 (± 6.86), Hybrid GWO-ABC 107.41 (± 12.09). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 204846.34% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse** (proposed/baseline ratio 2049×); vs GWO: Hybrid GWO-ABC is 133.48% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs ABC: Hybrid GWO-ABC is 29.41% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.82 (large) → **proposed worse**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Metaheuristics evaluate hundreds of candidate CH sets per round; LEACH needs one random draw per node. The hybrid runs two populations and more operators per iteration, which adds overhead even at an equal number of fitness evaluations. Runtime relative to LEACH: GWO 878×, ABC 1584×, Hybrid GWO-ABC 2049×.

#### Final Fitness
- **What it represents:** Mean per-round fitness (same function and weights for every algorithm) of the CH set actually used, over rounds 1..checkpoint. Lower is better.
- **How it was calculated:** per round fitness of the CH set used (same weights for all), mean over rounds 1..checkpoint. (lower is better, unit: -)
- **Why it matters:** Quality of the CH configurations according to the optimisation objective.
- **Observed (mean ± std over runs):** LEACH 1.2909 (± 0.1535), GWO 0.2337 (± 0.0149), ABC 0.2316 (± 0.0143), Hybrid GWO-ABC 0.2296 (± 0.0154). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 82.21% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 1.75% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.22 (small) → **proposed better**; vs ABC: Hybrid GWO-ABC is 0.87% better (reduction formula), p = 0.0195 (Holm), Cliff's δ = +0.10 (negligible) → **proposed better** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Optimisers minimise this objective directly; LEACH does not use it, and rounds in which LEACH elects zero CHs or too many receive the invalid-solution penalty.

#### Node-rounds
- **What it represents:** Sum over rounds of the number of alive nodes (area under the alive-nodes curve).
- **How it was calculated:** sum over rounds of alive nodes. (higher is better, unit: node x rounds)
- **Why it matters:** Single-number lifetime measure that accounts for the whole death curve.
- **Observed (mean ± std over runs):** LEACH 108,758 (± 639), GWO 112,736 (± 532), ABC 112,733 (± 587), Hybrid GWO-ABC 112,607 (± 548). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 3.54% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.11% worse (improvement formula), p = 0.0273 (Holm), Cliff's δ = -0.10 (negligible) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.11% worse (improvement formula), p = 0.0195 (Holm), Cliff's δ = -0.14 (negligible) → **proposed worse** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The area under the alive-nodes curve combines stability period and tail length.

#### Cluster Imbalance
- **What it represents:** Coefficient of variation of cluster sizes, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round std/mean of cluster sizes, averaged over rounds 1..checkpoint. (lower is better, unit: CV)
- **Why it matters:** Balanced clusters spread the CH load evenly.
- **Observed (mean ± std over runs):** LEACH 0.4490 (± 0.0084), GWO 0.1755 (± 0.0096), ABC 0.1528 (± 0.0106), Hybrid GWO-ABC 0.1388 (± 0.0094). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 69.08% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 20.88% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs ABC: Hybrid GWO-ABC is 9.16% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.76 (large) → **proposed better**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises unequal cluster sizes; nearest-CH assignment does not.

## Cluster-head records (run 0)

Every selected CH of every round is recorded in `ch_log_run0.csv` (round, CH id, coordinates, residual energy at selection, distance to the BS, cluster size including the CH). Dead and duplicate CHs are removed before clustering, so only valid CHs appear.

**Reproducibility check:** run 0 of every algorithm was re-simulated from `config.json` and its seed; all checked results (fnd, hnd, lnd, node_rounds, throughput_packets, packets_generated, residual_energy_cp, final_fitness) are identical to the saved values (`reproducibility_check_run0.csv`).

### LEACH

Over 1197 rounds with CHs: 4.58 CHs/round on average; mean CH residual energy at selection 0.2537 J; mean CH–BS distance 57.75 m; 100 distinct nodes served as CH, the most frequent one 70 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 27 | 70.52 | 78.07 | 0.5 | 30.03 | 29 |
| 51 | 26.59 | 96.92 | 0.5 | 23.62 | 20 |
| 68 | 95.86 | 48.23 | 0.5 | 69.16 | 34 |
| 84 | 31.71 | 95.29 | 0.5 | 18.88 | 17 |

### GWO

Over 1154 rounds with CHs: 4.90 CHs/round on average; mean CH residual energy at selection 0.2524 J; mean CH–BS distance 55.66 m; 100 distinct nodes served as CH, the most frequent one 84 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 31 | 56.52 | 76.5 | 0.5 | 24.39 | 15 |
| 75 | 82.63 | 89.62 | 0.5 | 34.24 | 16 |
| 77 | 10.86 | 67.22 | 0.5 | 51.05 | 21 |
| 94 | 74.68 | 26.25 | 0.5 | 77.77 | 23 |
| 99 | 19.64 | 31.03 | 0.5 | 75.35 | 25 |

### ABC

Over 1146 rounds with CHs: 4.89 CHs/round on average; mean CH residual energy at selection 0.2533 J; mean CH–BS distance 55.75 m; 100 distinct nodes served as CH, the most frequent one 77 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 26 | 78.69 | 66.49 | 0.5 | 44.12 | 21 |
| 28 | 45.89 | 56.87 | 0.5 | 43.32 | 19 |
| 32 | 63.47 | 55.36 | 0.5 | 46.63 | 21 |
| 38 | 29.36 | 66.19 | 0.5 | 39.61 | 19 |
| 64 | 10.34 | 58.76 | 0.5 | 57.21 | 20 |

### Hybrid GWO-ABC

Over 1145 rounds with CHs: 4.83 CHs/round on average; mean CH residual energy at selection 0.2523 J; mean CH–BS distance 55.83 m; 100 distinct nodes served as CH, the most frequent one 76 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 19 | 22.69 | 66.98 | 0.5 | 42.85 | 20 |
| 59 | 43.21 | 62.73 | 0.5 | 37.88 | 19 |
| 60 | 58.41 | 64.98 | 0.5 | 36.01 | 20 |
| 62 | 4.161 | 49.4 | 0.5 | 68.28 | 20 |
| 79 | 72.7 | 76.86 | 0.5 | 32.41 | 21 |


## Reproducing this experiment

```
python main.py reproduce "C:\Users\Admin\Hybrid-GWO-ABC-WSN\results\scenarios\S4_100nodes_BS_edge"
```

`config.json` holds every parameter; `experiment.json` holds the algorithms, run count and seeds.

## Data-quality note

Runtime values in this folder were measured with 11 simulations running in parallel, so they include scheduling noise; see `results/runtime_benchmark/report.md` for a clean sequential runtime comparison.
