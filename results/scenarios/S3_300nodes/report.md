# Scenario S3_300nodes

300 nodes, 100x100 m, BS at the centre (50, 50)

All numbers below were produced by the simulator in this folder (10 independent paired runs per algorithm; run r uses deployment/algorithm seed 42 + r). Raw per-run results: `runs_raw.csv`; per-round histories: `history_raw.csv.gz`; statistics: `statistics.csv`; proposed-vs-baseline tests: `improvement_vs_baselines.csv`.

## Configuration

| Parameter | Value |
|---|---|
| Nodes | 300 |
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
| FND (rounds) | 940 ± 47 | 1,174 ± 3 | 1,172 ± 2 | 1,173 ± 3 |
| HND (rounds) | 1,164 ± 4 | 1,188 ± 2 | 1,187 ± 1 | 1,187 ± 2 |
| LND (rounds) | 1,440 ± 36 | 1,244 ± 39 | 1,229 ± 21 | 1,236 ± 34 |
| Residual Energy (J) | 86.390 ± 0.056 | 86.894 ± 0.056 | 86.848 ± 0.046 | 86.858 ± 0.066 |
| Energy Consumption (J) | 63.610 ± 0.056 | 63.106 ± 0.056 | 63.152 ± 0.046 | 63.142 ± 0.066 |
| Throughput (packets) | 348,250 ± 529 | 355,022 ± 485 | 354,711 ± 474 | 354,664 ± 743 |
| PDR (ratio) | 0.9876 ± 0.0009 | 0.9961 ± 0.0010 | 0.9959 ± 0.0008 | 0.9957 ± 0.0014 |
| Avg. Cluster Distance (m) | 14.370 ± 0.179 | 12.448 ± 0.243 | 12.568 ± 0.198 | 12.584 ± 0.268 |
| Avg. CH-BS Distance (m) | 38.383 ± 0.419 | 37.707 ± 0.375 | 37.882 ± 0.347 | 37.646 ± 0.366 |
| Runtime (s) | 0.09 ± 0.00 | 334.24 ± 566.26 | 388.20 ± 559.33 | 608.02 ± 738.43 |
| Final Fitness (-) | 0.5005 ± 0.0892 | 0.2161 ± 0.0051 | 0.2245 ± 0.0059 | 0.2126 ± 0.0059 |

Residual energy and energy consumption are measured at the checkpoint round 500; distance, imbalance and fitness averages cover rounds 1–500. '≥' marks lifetime values where at least one run had not reached the event within 2000 rounds (the horizon is then used as a lower bound).

## Descriptive statistics

**FND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 940 | 47 | 855 | 989 |
| GWO | 10 | 1,174 | 3 | 1,168 | 1,177 |
| ABC | 10 | 1,172 | 2 | 1,169 | 1,176 |
| Hybrid GWO-ABC | 10 | 1,173 | 3 | 1,169 | 1,176 |

**HND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 1,164 | 4 | 1,158 | 1,170 |
| GWO | 10 | 1,188 | 2 | 1,184 | 1,191 |
| ABC | 10 | 1,187 | 1 | 1,185 | 1,189 |
| Hybrid GWO-ABC | 10 | 1,187 | 2 | 1,184 | 1,190 |

**LND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 1,440 | 36 | 1,389 | 1,518 |
| GWO | 10 | 1,244 | 39 | 1,205 | 1,331 |
| ABC | 10 | 1,229 | 21 | 1,200 | 1,259 |
| Hybrid GWO-ABC | 10 | 1,236 | 34 | 1,201 | 1,304 |

**Residual Energy (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 86.390 | 0.056 | 86.314 | 86.467 |
| GWO | 10 | 86.894 | 0.056 | 86.789 | 86.964 |
| ABC | 10 | 86.848 | 0.046 | 86.746 | 86.898 |
| Hybrid GWO-ABC | 10 | 86.858 | 0.066 | 86.713 | 86.936 |

**Energy Consumption (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 63.610 | 0.056 | 63.533 | 63.686 |
| GWO | 10 | 63.106 | 0.056 | 63.036 | 63.211 |
| ABC | 10 | 63.152 | 0.046 | 63.102 | 63.254 |
| Hybrid GWO-ABC | 10 | 63.142 | 0.066 | 63.064 | 63.287 |

**Throughput (packets)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 348,250 | 529 | 347,313 | 348,988 |
| GWO | 10 | 355,022 | 485 | 353,802 | 355,558 |
| ABC | 10 | 354,711 | 474 | 353,895 | 355,459 |
| Hybrid GWO-ABC | 10 | 354,664 | 743 | 353,407 | 355,596 |

**PDR (ratio)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 0.9876 | 0.0009 | 0.9863 | 0.9891 |
| GWO | 10 | 0.9961 | 0.0010 | 0.9947 | 0.9976 |
| ABC | 10 | 0.9959 | 0.0008 | 0.9950 | 0.9973 |
| Hybrid GWO-ABC | 10 | 0.9957 | 0.0014 | 0.9922 | 0.9971 |

**Runtime (s)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| LEACH | 10 | 0.09 | 0.00 | 0.09 | 0.10 |
| GWO | 10 | 334.24 | 566.26 | 132.02 | 1945.60 |
| ABC | 10 | 388.20 | 559.33 | 183.16 | 1979.78 |
| Hybrid GWO-ABC | 10 | 608.02 | 738.43 | 250.69 | 2026.39 |

## Hybrid GWO-ABC vs baselines

Improvement % uses ((P − B) / B) × 100 for higher-is-better metrics and ((B − P) / B) × 100 for lower-is-better metrics, so a positive value always means the proposed algorithm did better. p-values: paired two-sided Wilcoxon signed-rank test, Holm-corrected over the baselines. Cliff's δ > 0 favours the proposed algorithm (|δ| < 0.147 negligible, < 0.33 small, < 0.474 medium, otherwise large).

| Metric | Baseline | Better | Improvement % | p (Holm) | Cliff's δ | Effect | Verdict |
|---|---|---|---:|---:|---:|---|---|
| FND | LEACH | higher | +24.86 | 0.00586 | +1.00 | large | proposed better |
| FND | GWO | higher | -0.04 | 0.93 | -0.10 | negligible | no significant difference |
| FND | ABC | higher | +0.10 | 0.234 | +0.30 | small | no significant difference |
| HND | LEACH | higher | +1.98 | 0.00586 | +1.00 | large | proposed better |
| HND | GWO | higher | -0.07 | 0.156 | -0.18 | small | no significant difference |
| HND | ABC | higher | +0.00 | 1 | +0.05 | negligible | no significant difference |
| LND | LEACH | higher | -14.22 | 0.00586 | -1.00 | large | proposed worse |
| LND | GWO | higher | -0.63 | 0.695 | -0.16 | small | no significant difference |
| LND | ABC | higher | +0.58 | 0.695 | +0.11 | negligible | no significant difference |
| Node-rounds | LEACH | higher | +1.02 | 0.00586 | +1.00 | large | proposed better |
| Node-rounds | GWO | higher | -0.07 | 0.00781 | -0.28 | small | proposed worse |
| Node-rounds | ABC | higher | +0.01 | 0.846 | +0.11 | negligible | no significant difference |
| Residual Energy | LEACH | higher | +0.54 | 0.00586 | +1.00 | large | proposed better |
| Residual Energy | GWO | higher | -0.04 | 0.00586 | -0.34 | medium | proposed worse |
| Residual Energy | ABC | higher | +0.01 | 0.232 | +0.18 | small | no significant difference |
| Energy Consumption | LEACH | lower | +0.74 | 0.00586 | +1.00 | large | proposed better |
| Energy Consumption | GWO | lower | -0.06 | 0.00586 | -0.34 | medium | proposed worse |
| Energy Consumption | ABC | lower | +0.02 | 0.232 | +0.18 | small | no significant difference |
| Throughput | LEACH | higher | +1.84 | 0.00586 | +1.00 | large | proposed better |
| Throughput | GWO | higher | -0.10 | 0.129 | -0.48 | large | no significant difference |
| Throughput | ABC | higher | -0.01 | 1 | +0.10 | negligible | no significant difference |
| PDR | LEACH | higher | +0.82 | 0.00586 | +1.00 | large | proposed better |
| PDR | GWO | higher | -0.04 | 1 | -0.04 | negligible | no significant difference |
| PDR | ABC | higher | -0.02 | 1 | +0.10 | negligible | no significant difference |
| Avg. Cluster Distance | LEACH | lower | +12.43 | 0.00586 | +1.00 | large | proposed better |
| Avg. Cluster Distance | GWO | lower | -1.09 | 0.00586 | -0.28 | small | proposed worse |
| Avg. Cluster Distance | ABC | lower | -0.13 | 0.557 | -0.08 | negligible | no significant difference |
| Avg. CH-BS Distance | LEACH | lower | +1.92 | 0.00586 | +0.78 | large | proposed better |
| Avg. CH-BS Distance | GWO | lower | +0.16 | 0.0195 | +0.12 | negligible | proposed better |
| Avg. CH-BS Distance | ABC | lower | +0.62 | 0.00586 | +0.36 | medium | proposed better |
| Final Fitness | LEACH | lower | +57.53 | 0.00586 | +1.00 | large | proposed better |
| Final Fitness | GWO | lower | +1.61 | 0.00586 | +0.32 | small | proposed better |
| Final Fitness | ABC | lower | +5.30 | 0.00586 | +0.84 | large | proposed better |
| Runtime | LEACH | lower | -655157.92 | 0.00586 | -1.00 | large | proposed worse |
| Runtime | GWO | lower | -81.91 | 0.00586 | -0.84 | large | proposed worse |
| Runtime | ABC | lower | -56.63 | 0.00586 | -0.84 | large | proposed worse |

### Trade-offs

- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+24.86%), HND (+1.98%), Node-rounds (+1.02%), Residual Energy (+0.54%, < 1%: practically negligible), Energy Consumption (+0.74%, < 1%: practically negligible), Throughput (+1.84%), PDR (+0.82%, < 1%: practically negligible), Avg. Cluster Distance (+12.43%), Avg. CH-BS Distance (+1.92%), Cluster Imbalance (+66.88%), Final Fitness (+57.53%); significantly worse: LND (-14.22%), Runtime (-655157.92%), Runtime / round (-773401.55%); no significant difference: Fitness Evaluations.
- **Hybrid GWO-ABC vs GWO** — significantly better: Avg. CH-BS Distance (+0.16%, < 1%: practically negligible), Cluster Imbalance (+16.38%), Final Fitness (+1.61%); significantly worse: Node-rounds (-0.07%, < 1%: practically negligible), Residual Energy (-0.04%, < 1%: practically negligible), Energy Consumption (-0.06%, < 1%: practically negligible), Avg. Cluster Distance (-1.09%), Runtime (-81.91%), Runtime / round (-82.86%); no significant difference: FND, HND, LND, Throughput, PDR, Fitness Evaluations.
- **Hybrid GWO-ABC vs ABC** — significantly better: Avg. CH-BS Distance (+0.62%, < 1%: practically negligible), Cluster Imbalance (+23.69%), Final Fitness (+5.30%); significantly worse: Runtime (-56.63%), Runtime / round (-56.73%); no significant difference: FND, HND, LND, Node-rounds, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance, Fitness Evaluations.

## Figures

### Initial WSN topology (run 0; every algorithm uses this same network in run 0).

![Initial WSN topology (run 0; every algorithm uses this same network in run 0).](01_topology.png)

**Observed:** 300 nodes uniformly deployed in 100 x 100 m (seed 42); BS at (50, 50). Mean node–BS distance 38.1 m (max 67.5 m); d0 = 87.7 m, so 0% of nodes would use the multipath (d^4) model for a direct BS transmission.

### LEACH: cluster heads selected in round 1 (run 0).

![LEACH: cluster heads selected in round 1 (run 0).](02_ch_selection_LEACH.png)

**Observed:** 15 CHs; mean CH–BS distance 39.2 m.

### LEACH: cluster formation in round 1 (members joined the nearest CH).

![LEACH: cluster formation in round 1 (members joined the nearest CH).](03_clusters_LEACH.png)

**Observed:** 15 clusters, sizes 2–32 (CV 0.46); member→CH distance mean 12.8 m, max 33.2 m.

### LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![LEACH: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_LEACH.png)

**Observed:** Round 1170: 152 dead, 148 alive. Mean distance to BS — dead nodes 31.5 m, alive nodes 44.9 m (near nodes died first on average).

### GWO: cluster heads selected in round 1 (run 0).

![GWO: cluster heads selected in round 1 (run 0).](02_ch_selection_GWO.png)

**Observed:** 15 CHs; mean CH–BS distance 34.2 m.

### GWO: cluster formation in round 1 (members joined the nearest CH).

![GWO: cluster formation in round 1 (members joined the nearest CH).](03_clusters_GWO.png)

**Observed:** 15 clusters, sizes 13–26 (CV 0.22); member→CH distance mean 11.4 m, max 32.5 m.

### GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_GWO.png)

**Observed:** Round 1191: 162 dead, 138 alive. Mean distance to BS — dead nodes 37.9 m, alive nodes 38.4 m (near nodes died first on average).

### ABC: cluster heads selected in round 1 (run 0).

![ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_ABC.png)

**Observed:** 14 CHs; mean CH–BS distance 34.6 m.

### ABC: cluster formation in round 1 (members joined the nearest CH).

![ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_ABC.png)

**Observed:** 14 clusters, sizes 12–30 (CV 0.23); member→CH distance mean 12.6 m, max 41.9 m.

### ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_ABC.png)

**Observed:** Round 1188: 160 dead, 140 alive. Mean distance to BS — dead nodes 35.6 m, alive nodes 40.9 m (near nodes died first on average).

### Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).

![Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_GWO-ABC.png)

**Observed:** 15 CHs; mean CH–BS distance 35.8 m.

### Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).

![Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_GWO-ABC.png)

**Observed:** 15 clusters, sizes 15–25 (CV 0.12); member→CH distance mean 11.4 m, max 25.7 m.

### Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).

![Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).](04_communication_Hybrid_GWO-ABC.png)

**Observed:** 15 clusters, sizes 15–25 (CV 0.12); member→CH distance mean 11.4 m, max 25.7 m.

### Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_GWO-ABC.png)

**Observed:** Round 1189: 153 dead, 147 alive. Mean distance to BS — dead nodes 37.1 m, alive nodes 39.1 m (near nodes died first on average).

### GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_GWO.png)

**Observed:** mean best fitness 0.2260 → 0.1880 (16.8% lower); 95% of the improvement reached by iteration 23

### ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_ABC.png)

**Observed:** mean best fitness 0.2354 → 0.1915 (18.7% lower); 95% of the improvement reached by iteration 25

### Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_GWO-ABC.png)

**Observed:** GWO: mean best fitness 0.2354 → 0.1754 (25.5% lower); 95% of the improvement reached by iteration 26; ABC: mean best fitness 0.2483 → 0.1754 (29.3% lower); 95% of the improvement reached by iteration 24; HYBRID: mean best fitness 0.2342 → 0.1754 (25.1% lower); 95% of the improvement reached by iteration 26

### Alive nodes vs rounds.

![Alive nodes vs rounds.](09_alive_vs_rounds.png)

**Observed:** LEACH: FND 940, HND 1164, LND 1440; GWO: FND 1174, HND 1188, LND 1244; ABC: FND 1172, HND 1187, LND 1229; Hybrid GWO-ABC: FND 1173, HND 1187, LND 1236

### Dead nodes vs rounds.

![Dead nodes vs rounds.](10_dead_vs_rounds.png)

**Observed:** Mirror image of the alive-nodes curve; a steeper rise means nodes die closer together.

### Residual energy vs rounds.

![Residual energy vs rounds.](11_residual_energy_vs_rounds.png)

**Observed:** Residual energy at round 500: LEACH 86.39 J; GWO 86.89 J; ABC 86.85 J; Hybrid GWO-ABC 86.86 J

### Energy consumption vs rounds.

![Energy consumption vs rounds.](12_consumed_energy_vs_rounds.png)

**Observed:** Consumed by round 500: LEACH 63.61 J; GWO 63.11 J; ABC 63.15 J; Hybrid GWO-ABC 63.14 J

### Throughput vs rounds (cumulative).

![Throughput vs rounds (cumulative).](13_packets_delivered_vs_rounds.png)

**Observed:** Total delivered: LEACH 348,250; GWO 355,022; ABC 354,711; Hybrid GWO-ABC 354,664

### PDR vs rounds.

![PDR vs rounds.](14_pdr_vs_rounds.png)

**Observed:** Final PDR: LEACH 0.9876; GWO 0.9961; ABC 0.9959; Hybrid GWO-ABC 0.9957

### CH count vs rounds (20-round rolling mean).

![CH count vs rounds (20-round rolling mean).](15_ch_count_vs_rounds.png)

**Observed:** Mean CHs/round (rounds 1–500): LEACH 15.00 (per-round std 3.71); GWO 14.86 (per-round std 0.66); ABC 14.60 (per-round std 1.34); Hybrid GWO-ABC 14.74 (per-round std 0.90)

### Average cluster distance vs rounds (20-round rolling mean).

![Average cluster distance vs rounds (20-round rolling mean).](16_avg_intra_distance_vs_rounds.png)

**Observed:** Mean member→CH distance: LEACH 14.37 m; GWO 12.45 m; ABC 12.57 m; Hybrid GWO-ABC 12.58 m

### Total CH-selection runtime per simulation (log scale, mean ± std).

![Total CH-selection runtime per simulation (log scale, mean ± std).](17_runtime.png)

**Observed:** LEACH 0.09 s (0.06 ms/round, 0 fitness evaluations); GWO 334.24 s (272.49 ms/round, 770,970 fitness evaluations); ABC 388.20 s (317.92 ms/round, 755,939 fitness evaluations); Hybrid GWO-ABC 608.02 s (498.27 ms/round, 765,170 fitness evaluations)

### FND / HND / LND comparison (mean ± std over runs).

![FND / HND / LND comparison (mean ± std over runs).](18_lifetime_fnd_hnd_lnd.png)

**Observed:** LEACH: FND 940, HND 1164, LND 1440; GWO: FND 1174, HND 1188, LND 1244; ABC: FND 1172, HND 1187, LND 1229; Hybrid GWO-ABC: FND 1173, HND 1187, LND 1236

### Where the energy goes: mean energy per radio activity over rounds 1–500.

![Where the energy goes: mean energy per radio activity over rounds 1–500.](19_energy_breakdown.png)

**Observed:** LEACH: total 63.61 J, largest share member TX (47%); GWO: total 63.11 J, largest share member TX (47%); ABC: total 63.15 J, largest share member TX (47%); Hybrid GWO-ABC: total 63.14 J, largest share member TX (47%)

### Final fitness: same objective and weights for every algorithm.

![Final fitness: same objective and weights for every algorithm.](20_final_fitness.png)

**Observed:** LEACH 0.5005; GWO 0.2161; ABC 0.2245; Hybrid GWO-ABC 0.2126

## Metric-by-metric interpretation

#### FND
- **What it represents:** First Node Death: the round in which the first node's residual energy reached 0.
- **How it was calculated:** min over nodes of the round in which residual energy reached 0 (simulation horizon if none died). (higher is better, unit: rounds)
- **Why it matters:** Marks the end of the stability period, during which every sensor still reports.
- **Observed (mean ± std over runs):** LEACH 940 (± 47), GWO 1,174 (± 3), ABC 1,172 (± 2), Hybrid GWO-ABC 1,173 (± 3). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 24.86% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.04% worse (improvement formula), p = 0.93 (Holm), Cliff's δ = -0.10 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.10% better (improvement formula), p = 0.234 (Holm), Cliff's δ = +0.30 (small) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** CH selection that avoids low-energy nodes and rotates the CH role evenly delays the first death; a node chosen repeatedly as CH (e.g. because it is close to the BS) dies early. Measured LND − FND spread (rounds): LEACH 501, GWO 70, ABC 57, Hybrid GWO-ABC 62.

#### HND
- **What it represents:** Half Node Death: the round in which at least 50% of the nodes were dead.
- **How it was calculated:** round in which the number of dead nodes reached ceil(N/2). (higher is better, unit: rounds)
- **Why it matters:** Indicates how long the network keeps useful coverage.
- **Observed (mean ± std over runs):** LEACH 1,164 (± 4), GWO 1,188 (± 2), ABC 1,187 (± 1), Hybrid GWO-ABC 1,187 (± 2). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 1.98% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.07% worse (improvement formula), p = 0.156 (Holm), Cliff's δ = -0.18 (small) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.00% equal (improvement formula), p = 1 (Holm), Cliff's δ = +0.05 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** HND reflects how evenly energy is drained across the whole network.

#### LND
- **What it represents:** Last Node Death: the round in which the last alive node died.
- **How it was calculated:** round in which the last node died (simulation horizon if nodes were still alive). (higher is better, unit: rounds)
- **Why it matters:** Upper bound of the network lifetime.
- **Observed (mean ± std over runs):** LEACH 1,440 (± 36), GWO 1,244 (± 39), ABC 1,229 (± 21), Hybrid GWO-ABC 1,236 (± 34). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 14.22% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs GWO: Hybrid GWO-ABC is 0.63% worse (improvement formula), p = 0.695 (Holm), Cliff's δ = -0.16 (small) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.58% better (improvement formula), p = 0.695 (Holm), Cliff's δ = +0.11 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** A very even energy drain makes all nodes die at nearly the same time: FND is delayed but the last node also dies sooner. Uneven drain leaves a few nodes with spare energy that keep running. Measured LND − FND spread (rounds): LEACH 501, GWO 70, ABC 57, Hybrid GWO-ABC 62.

#### Residual Energy
- **What it represents:** Total residual energy of all nodes at the checkpoint round.
- **How it was calculated:** sum of node residual energies after the checkpoint round. (higher is better, unit: J)
- **Why it matters:** More energy left at the same round means cheaper operation.
- **Observed (mean ± std over runs):** LEACH 86.390 (± 0.056), GWO 86.894 (± 0.056), ABC 86.848 (± 0.046), Hybrid GWO-ABC 86.858 (± 0.066). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 0.54% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better** — practically small; vs GWO: Hybrid GWO-ABC is 0.04% worse (improvement formula), p = 0.00586 (Holm), Cliff's δ = -0.34 (medium) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.01% better (improvement formula), p = 0.232 (Holm), Cliff's δ = +0.18 (small) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Residual energy at a fixed round depends on per-round radio cost: shorter member->CH links and shorter or fewer CH->BS links consume less.

#### Energy Consumption
- **What it represents:** Initial total energy minus residual energy at the checkpoint round.
- **How it was calculated:** N * E0 - residual energy at the checkpoint round. (lower is better, unit: J)
- **Why it matters:** Energy spent to operate the network for the same number of rounds.
- **Observed (mean ± std over runs):** LEACH 63.610 (± 0.056), GWO 63.106 (± 0.056), ABC 63.152 (± 0.046), Hybrid GWO-ABC 63.142 (± 0.066). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 0.74% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better** — practically small; vs GWO: Hybrid GWO-ABC is 0.06% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.34 (medium) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.02% better (reduction formula), p = 0.232 (Holm), Cliff's δ = +0.18 (small) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Consumption is the complement of residual energy at the same checkpoint.

#### Throughput
- **What it represents:** Total sensor data packets delivered to the BS over the whole simulation (directly or inside an aggregated CH packet).
- **How it was calculated:** count of sensor readings that reached the BS over the whole run. (higher is better, unit: packets)
- **Why it matters:** Amount of sensed data the application actually receives.
- **Observed (mean ± std over runs):** LEACH 348,250 (± 529), GWO 355,022 (± 485), ABC 354,711 (± 474), Hybrid GWO-ABC 354,664 (± 743). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 1.84% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.10% worse (improvement formula), p = 0.129 (Holm), Cliff's δ = -0.48 (large) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.01% worse (improvement formula), p = 1 (Holm), Cliff's δ = +0.10 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Throughput grows with the number of rounds in which nodes are alive and with the share of packets that are not lost to CHs dying mid-round.

#### PDR
- **What it represents:** Packet Delivery Ratio = delivered data packets / generated data packets.
- **How it was calculated:** delivered readings / generated readings over the whole run. (higher is better, unit: ratio)
- **Why it matters:** Reliability: share of generated readings that reach the BS.
- **Observed (mean ± std over runs):** LEACH 0.9876 (± 0.0009), GWO 0.9961 (± 0.0010), ABC 0.9959 (± 0.0008), Hybrid GWO-ABC 0.9957 (± 0.0014). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 0.82% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better** — practically small; vs GWO: Hybrid GWO-ABC is 0.04% worse (improvement formula), p = 1 (Holm), Cliff's δ = -0.04 (negligible) → **no significant difference** — practically small; vs ABC: Hybrid GWO-ABC is 0.02% worse (improvement formula), p = 1 (Holm), Cliff's δ = +0.10 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Packets are lost when a CH runs out of energy before forwarding its cluster's data, or when a node dies while transmitting. Energy-feasibility checks on CHs reduce such losses.

#### Avg. Cluster Distance
- **What it represents:** Mean member->CH distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean member->CH distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** Shorter intra-cluster links cost less transmission energy (d^2 / d^4).
- **Observed (mean ± std over runs):** LEACH 14.370 (± 0.179), GWO 12.448 (± 0.243), ABC 12.568 (± 0.198), Hybrid GWO-ABC 12.584 (± 0.268). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 12.43% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 1.09% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.28 (small) → **proposed worse**; vs ABC: Hybrid GWO-ABC is 0.13% worse (reduction formula), p = 0.557 (Holm), Cliff's δ = -0.08 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness function explicitly penalises member->CH distance; LEACH places CHs at random positions, which typically lengthens member links.

#### Avg. CH-BS Distance
- **What it represents:** Mean CH->BS distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean CH->BS distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** CH->BS is the longest and most expensive hop.
- **Observed (mean ± std over runs):** LEACH 38.383 (± 0.419), GWO 37.707 (± 0.375), ABC 37.882 (± 0.347), Hybrid GWO-ABC 37.646 (± 0.366). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 1.92% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.78 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.16% better (reduction formula), p = 0.0195 (Holm), Cliff's δ = +0.12 (negligible) → **proposed better** — practically small; vs ABC: Hybrid GWO-ABC is 0.62% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.36 (medium) → **proposed better** — practically small.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises CH->BS distance, but the energy-eligibility rule and the energy term limit how often nodes near the BS can be selected.

#### Runtime
- **What it represents:** Total wall-clock time spent selecting CHs over the whole simulation.
- **How it was calculated:** sum of wall-clock CH-selection time over all rounds (time.perf_counter). (lower is better, unit: s)
- **Why it matters:** Computational cost of the CH selection algorithm.
- **Observed (mean ± std over runs):** LEACH 0.09 (± 0.00), GWO 334.24 (± 566.26), ABC 388.20 (± 559.33), Hybrid GWO-ABC 608.02 (± 738.43). Best mean: **LEACH**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 655157.92% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -1.00 (large) → **proposed worse** (proposed/baseline ratio 6553×); vs GWO: Hybrid GWO-ABC is 81.91% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.84 (large) → **proposed worse**; vs ABC: Hybrid GWO-ABC is 56.63% worse (reduction formula), p = 0.00586 (Holm), Cliff's δ = -0.84 (large) → **proposed worse**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Metaheuristics evaluate hundreds of candidate CH sets per round; LEACH needs one random draw per node. The hybrid runs two populations and more operators per iteration, which adds overhead even at an equal number of fitness evaluations. Runtime relative to LEACH: GWO 3602×, ABC 4184×, Hybrid GWO-ABC 6553×.

#### Final Fitness
- **What it represents:** Mean per-round fitness (same function and weights for every algorithm) of the CH set actually used, over rounds 1..checkpoint. Lower is better.
- **How it was calculated:** per round fitness of the CH set used (same weights for all), mean over rounds 1..checkpoint. (lower is better, unit: -)
- **Why it matters:** Quality of the CH configurations according to the optimisation objective.
- **Observed (mean ± std over runs):** LEACH 0.5005 (± 0.0892), GWO 0.2161 (± 0.0051), ABC 0.2245 (± 0.0059), Hybrid GWO-ABC 0.2126 (± 0.0059). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 57.53% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 1.61% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.32 (small) → **proposed better**; vs ABC: Hybrid GWO-ABC is 5.30% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +0.84 (large) → **proposed better**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Optimisers minimise this objective directly; LEACH does not use it, and rounds in which LEACH elects zero CHs or too many receive the invalid-solution penalty.

#### Node-rounds
- **What it represents:** Sum over rounds of the number of alive nodes (area under the alive-nodes curve).
- **How it was calculated:** sum over rounds of alive nodes. (higher is better, unit: node x rounds)
- **Why it matters:** Single-number lifetime measure that accounts for the whole death curve.
- **Observed (mean ± std over runs):** LEACH 352,307 (± 390), GWO 356,125 (± 491), ABC 355,872 (± 390), Hybrid GWO-ABC 355,893 (± 520). Best mean: **GWO**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 1.02% better (improvement formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 0.07% worse (improvement formula), p = 0.00781 (Holm), Cliff's δ = -0.28 (small) → **proposed worse** — practically small; vs ABC: Hybrid GWO-ABC is 0.01% better (improvement formula), p = 0.846 (Holm), Cliff's δ = +0.11 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The area under the alive-nodes curve combines stability period and tail length.

#### Cluster Imbalance
- **What it represents:** Coefficient of variation of cluster sizes, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round std/mean of cluster sizes, averaged over rounds 1..checkpoint. (lower is better, unit: CV)
- **Why it matters:** Balanced clusters spread the CH load evenly.
- **Observed (mean ± std over runs):** LEACH 0.5520 (± 0.0055), GWO 0.2187 (± 0.0069), ABC 0.2396 (± 0.0084), Hybrid GWO-ABC 0.1828 (± 0.0099). Best mean: **Hybrid GWO-ABC**.
- **Proposed vs baselines:** vs LEACH: Hybrid GWO-ABC is 66.88% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs GWO: Hybrid GWO-ABC is 16.38% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**; vs ABC: Hybrid GWO-ABC is 23.69% better (reduction formula), p = 0.00586 (Holm), Cliff's δ = +1.00 (large) → **proposed better**.
- **Is the difference meaningful?** 3 of 3 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises unequal cluster sizes; nearest-CH assignment does not.

## Cluster-head records (run 0)

Every selected CH of every round is recorded in `ch_log_run0.csv` (round, CH id, coordinates, residual energy at selection, distance to the BS, cluster size including the CH). Dead and duplicate CHs are removed before clustering, so only valid CHs appear.

**Reproducibility check:** run 0 of every algorithm was re-simulated from `config.json` and its seed; all checked results (fnd, hnd, lnd, node_rounds, throughput_packets, packets_generated, residual_energy_cp, final_fitness) are identical to the saved values (`reproducibility_check_run0.csv`).

### LEACH

Over 1356 rounds with CHs: 13.07 CHs/round on average; mean CH residual energy at selection 0.2537 J; mean CH–BS distance 38.71 m; 300 distinct nodes served as CH, the most frequent one 76 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 27 | 70.52 | 78.07 | 0.5 | 34.77 | 32 |
| 51 | 26.59 | 96.92 | 0.5 | 52.44 | 2 |
| 68 | 95.86 | 48.23 | 0.5 | 45.89 | 17 |
| 84 | 31.71 | 95.29 | 0.5 | 48.84 | 10 |
| 124 | 37.42 | 42.59 | 0.5 | 14.6 | 32 |
| 135 | 5.54 | 17.46 | 0.5 | 55.09 | 19 |
| 149 | 77.95 | 64.25 | 0.5 | 31.37 | 24 |
| 163 | 80.44 | 53.27 | 0.5 | 30.61 | 14 |
| 175 | 61.62 | 17.13 | 0.5 | 34.86 | 30 |
| 204 | 10.64 | 99.91 | 0.5 | 63.56 | 7 |
| 226 | 70.96 | 17.31 | 0.5 | 38.83 | 23 |
| 238 | 42.79 | 61.1 | 0.5 | 13.23 | 20 |
| 269 | 16.59 | 83.63 | 0.5 | 47.4 | 32 |
| 280 | 8.412 | 24.37 | 0.5 | 48.85 | 26 |
| 286 | 48.26 | 76.86 | 0.5 | 26.92 | 12 |

### GWO

Over 1331 rounds with CHs: 13.37 CHs/round on average; mean CH residual energy at selection 0.2519 J; mean CH–BS distance 38.05 m; 300 distinct nodes served as CH, the most frequent one 186 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 0 | 77.4 | 43.89 | 0.5 | 28.07 | 15 |
| 3 | 76.11 | 78.61 | 0.5 | 38.73 | 26 |
| 44 | 16.13 | 50.1 | 0.5 | 33.87 | 20 |
| 54 | 9.639 | 90.26 | 0.5 | 57.01 | 21 |
| 90 | 89.08 | 89.34 | 0.5 | 55.45 | 13 |
| 143 | 4.925 | 37.36 | 0.5 | 46.81 | 24 |
| 198 | 82.54 | 29.54 | 0.5 | 38.44 | 26 |
| 203 | 28.39 | 83.69 | 0.5 | 40.02 | 16 |
| 219 | 74.52 | 63 | 0.5 | 27.75 | 25 |
| 222 | 27.08 | 70.99 | 0.5 | 31.08 | 14 |
| 235 | 40.4 | 47.42 | 0.5 | 9.938 | 19 |
| 239 | 63.46 | 41.18 | 0.5 | 16.09 | 16 |
| 248 | 43.14 | 62.6 | 0.5 | 14.35 | 18 |
| 254 | 49.41 | 11.59 | 0.5 | 38.42 | 22 |
| 257 | 33.41 | 17.3 | 0.5 | 36.67 | 25 |

### ABC

Over 1259 rounds with CHs: 13.78 CHs/round on average; mean CH residual energy at selection 0.2528 J; mean CH–BS distance 38.18 m; 300 distinct nodes served as CH, the most frequent one 112 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 7 | 44.34 | 22.72 | 0.5 | 27.86 | 16 |
| 20 | 43.72 | 83.27 | 0.5 | 33.86 | 23 |
| 58 | 75.85 | 71.95 | 0.5 | 33.91 | 19 |
| 82 | 55.49 | 37.09 | 0.5 | 14.02 | 20 |
| 120 | 82.94 | 79.68 | 0.5 | 44.34 | 24 |
| 128 | 81.66 | 10.53 | 0.5 | 50.6 | 25 |
| 152 | 85.76 | 46.28 | 0.5 | 35.95 | 21 |
| 167 | 13.21 | 61.44 | 0.5 | 38.53 | 19 |
| 179 | 49.22 | 59.96 | 0.5 | 9.99 | 23 |
| 206 | 9.044 | 89.7 | 0.5 | 57.04 | 25 |
| 234 | 14.84 | 50.84 | 0.5 | 35.17 | 12 |
| 240 | 40.88 | 21.76 | 0.5 | 29.67 | 28 |
| 272 | 14.16 | 44.82 | 0.5 | 36.21 | 30 |
| 281 | 84.36 | 63.76 | 0.5 | 37.01 | 15 |

### Hybrid GWO-ABC

Over 1236 rounds with CHs: 14.21 CHs/round on average; mean CH residual energy at selection 0.2527 J; mean CH–BS distance 37.79 m; 300 distinct nodes served as CH, the most frequent one 87 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 40 | 66.43 | 40.64 | 0.5 | 18.91 | 19 |
| 41 | 81.4 | 16.7 | 0.5 | 45.77 | 18 |
| 46 | 44.62 | 38.1 | 0.5 | 13.06 | 22 |
| 81 | 23.02 | 3.741 | 0.5 | 53.55 | 23 |
| 85 | 29.09 | 51.51 | 0.5 | 20.96 | 17 |
| 127 | 23.67 | 74.6 | 0.5 | 36.04 | 19 |
| 129 | 6.656 | 59.44 | 0.5 | 44.36 | 18 |
| 139 | 87.5 | 85.11 | 0.5 | 51.37 | 25 |
| 162 | 84.86 | 65.26 | 0.5 | 38.05 | 20 |
| 179 | 49.22 | 59.96 | 0.5 | 9.99 | 15 |
| 206 | 9.044 | 89.7 | 0.5 | 57.04 | 22 |
| 219 | 74.52 | 63 | 0.5 | 27.75 | 21 |
| 221 | 73.46 | 19.3 | 0.5 | 38.64 | 20 |
| 286 | 48.26 | 76.86 | 0.5 | 26.92 | 19 |
| 297 | 0.7314 | 27.8 | 0.5 | 54.04 | 22 |


## Reproducing this experiment

```
python main.py reproduce "C:\Users\Admin\Hybrid-GWO-ABC-WSN\results\scenarios\S3_300nodes"
```

`config.json` holds every parameter; `experiment.json` holds the algorithms, run count and seeds.

## Data-quality note

Runtime values in this folder were measured with 11 simulations running in parallel, so they include scheduling noise; see `results/runtime_benchmark/report.md` for a clean sequential runtime comparison.
Runs with runtime/round > 3× their algorithm's median (most likely timed across a system sleep): Hybrid GWO-ABC run 8 (1679 ms/round vs median 209), GWO run 9 (1605 ms/round vs median 126), ABC run 9 (1633 ms/round vs median 174), Hybrid GWO-ABC run 9 (1643 ms/round vs median 209). Their raw values are kept unchanged; only runtime metrics are affected (energy, lifetime and packet metrics count rounds, not seconds).
