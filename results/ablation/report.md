# Ablation study

Contribution of each hybrid component (100 nodes, 100x100 m, BS centre). 'w/o distance' removes both distance terms (w2 = w3 = 0); every variant's CH sets are re-scored with the full default weights for 'Final Fitness'.

All numbers below were produced by the simulator in this folder (10 independent paired runs per algorithm; run r uses deployment/algorithm seed 42 + r). Raw per-run results: `runs_raw.csv`; per-round histories: `history_raw.csv.gz`; statistics: `statistics.csv`; proposed-vs-baseline tests: `improvement_vs_baselines.csv`.

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

| Metric | GWO only | ABC only | GWO->ABC | ABC->GWO | Hybrid w/o energy | Hybrid w/o distance | Hybrid w/o balance | Full Hybrid GWO-ABC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| FND (rounds) | 1,126 ± 7 | 1,124 ± 9 | 1,126 ± 8 | 1,128 ± 8 | 1,116 ± 11 | 1,132 ± 7 | 1,130 ± 5 | 1,128 ± 7 |
| HND (rounds) | 1,138 ± 7 | 1,138 ± 7 | 1,137 ± 7 | 1,137 ± 7 | 1,132 ± 8 | 1,140 ± 7 | 1,146 ± 5 | 1,138 ± 7 |
| LND (rounds) | 1,162 ± 12 | 1,165 ± 8 | 1,161 ± 9 | 1,160 ± 13 | 1,302 ± 96 | 1,150 ± 6 | 1,155 ± 4 | 1,158 ± 13 |
| Residual Energy (J) | 28.115 ± 0.094 | 28.118 ± 0.106 | 28.107 ± 0.113 | 28.100 ± 0.099 | 28.077 ± 0.113 | 28.101 ± 0.098 | 28.160 ± 0.089 | 28.105 ± 0.109 |
| Energy Consumption (J) | 21.885 ± 0.094 | 21.882 ± 0.106 | 21.893 ± 0.113 | 21.900 ± 0.099 | 21.923 ± 0.113 | 21.899 ± 0.098 | 21.840 ± 0.089 | 21.895 ± 0.109 |
| Throughput (packets) | 113,713 ± 627 | 113,780 ± 640 | 113,667 ± 661 | 113,696 ± 641 | 113,070 ± 751 | 113,676 ± 635 | 114,244 ± 455 | 113,637 ± 663 |
| PDR (ratio) | 0.9986 ± 0.0004 | 0.9988 ± 0.0003 | 0.9985 ± 0.0005 | 0.9986 ± 0.0004 | 0.9972 ± 0.0011 | 0.9969 ± 0.0007 | 0.9979 ± 0.0006 | 0.9981 ± 0.0006 |
| Avg. Cluster Distance (m) | 22.465 ± 0.765 | 22.440 ± 0.855 | 22.515 ± 0.886 | 22.568 ± 0.798 | 22.745 ± 0.891 | 22.609 ± 0.724 | 22.226 ± 0.773 | 22.546 ± 0.871 |
| Avg. CH-BS Distance (m) | 37.925 ± 1.093 | 37.956 ± 1.072 | 37.876 ± 1.118 | 37.891 ± 1.118 | 37.817 ± 1.142 | 37.675 ± 1.122 | 38.755 ± 1.017 | 37.863 ± 1.160 |
| Runtime (s) | 181.94 ± 408.87 | 506.66 ± 556.98 | 152.73 ± 240.97 | 149.41 ± 242.00 | 554.02 ± 557.89 | 460.83 ± 557.01 | 538.25 ± 558.56 | 536.72 ± 558.48 |
| Final Fitness (-) | 0.2467 ± 0.0128 | 0.2457 ± 0.0135 | 0.2453 ± 0.0126 | 0.2474 ± 0.0126 | 0.2470 ± 0.0136 | 0.2232 ± 0.0118 | 0.2703 ± 0.0127 | 0.2439 ± 0.0128 |

Residual energy and energy consumption are measured at the checkpoint round 500; distance, imbalance and fitness averages cover rounds 1–500. '≥' marks lifetime values where at least one run had not reached the event within 2000 rounds (the horizon is then used as a lower bound).

## Descriptive statistics

**FND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| GWO only | 10 | 1,126 | 7 | 1,115 | 1,138 |
| ABC only | 10 | 1,124 | 9 | 1,111 | 1,138 |
| GWO->ABC | 10 | 1,126 | 8 | 1,115 | 1,139 |
| ABC->GWO | 10 | 1,128 | 8 | 1,117 | 1,142 |
| Hybrid w/o energy | 10 | 1,116 | 11 | 1,103 | 1,136 |
| Hybrid w/o distance | 10 | 1,132 | 7 | 1,122 | 1,140 |
| Hybrid w/o balance | 10 | 1,130 | 5 | 1,123 | 1,136 |
| Full Hybrid GWO-ABC | 10 | 1,128 | 7 | 1,118 | 1,140 |

**HND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| GWO only | 10 | 1,138 | 7 | 1,129 | 1,148 |
| ABC only | 10 | 1,138 | 7 | 1,128 | 1,147 |
| GWO->ABC | 10 | 1,137 | 7 | 1,127 | 1,148 |
| ABC->GWO | 10 | 1,137 | 7 | 1,128 | 1,148 |
| Hybrid w/o energy | 10 | 1,132 | 8 | 1,120 | 1,146 |
| Hybrid w/o distance | 10 | 1,140 | 7 | 1,130 | 1,148 |
| Hybrid w/o balance | 10 | 1,146 | 5 | 1,137 | 1,154 |
| Full Hybrid GWO-ABC | 10 | 1,138 | 7 | 1,129 | 1,148 |

**LND (rounds)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| GWO only | 10 | 1,162 | 12 | 1,141 | 1,183 |
| ABC only | 10 | 1,165 | 8 | 1,155 | 1,181 |
| GWO->ABC | 10 | 1,161 | 9 | 1,150 | 1,176 |
| ABC->GWO | 10 | 1,160 | 13 | 1,141 | 1,179 |
| Hybrid w/o energy | 10 | 1,302 | 96 | 1,171 | 1,422 |
| Hybrid w/o distance | 10 | 1,150 | 6 | 1,139 | 1,155 |
| Hybrid w/o balance | 10 | 1,155 | 4 | 1,148 | 1,161 |
| Full Hybrid GWO-ABC | 10 | 1,158 | 13 | 1,141 | 1,181 |

**Residual Energy (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| GWO only | 10 | 28.115 | 0.094 | 27.949 | 28.233 |
| ABC only | 10 | 28.118 | 0.106 | 27.916 | 28.251 |
| GWO->ABC | 10 | 28.107 | 0.113 | 27.898 | 28.245 |
| ABC->GWO | 10 | 28.100 | 0.099 | 27.924 | 28.245 |
| Hybrid w/o energy | 10 | 28.077 | 0.113 | 27.853 | 28.236 |
| Hybrid w/o distance | 10 | 28.101 | 0.098 | 27.941 | 28.218 |
| Hybrid w/o balance | 10 | 28.160 | 0.089 | 28.004 | 28.292 |
| Full Hybrid GWO-ABC | 10 | 28.105 | 0.109 | 27.902 | 28.252 |

**Energy Consumption (J)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| GWO only | 10 | 21.885 | 0.094 | 21.767 | 22.051 |
| ABC only | 10 | 21.882 | 0.106 | 21.749 | 22.084 |
| GWO->ABC | 10 | 21.893 | 0.113 | 21.755 | 22.102 |
| ABC->GWO | 10 | 21.900 | 0.099 | 21.755 | 22.076 |
| Hybrid w/o energy | 10 | 21.923 | 0.113 | 21.764 | 22.147 |
| Hybrid w/o distance | 10 | 21.899 | 0.098 | 21.782 | 22.059 |
| Hybrid w/o balance | 10 | 21.840 | 0.089 | 21.708 | 21.996 |
| Full Hybrid GWO-ABC | 10 | 21.895 | 0.109 | 21.748 | 22.098 |

**Throughput (packets)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| GWO only | 10 | 113,713 | 627 | 112,781 | 114,689 |
| ABC only | 10 | 113,780 | 640 | 112,918 | 114,701 |
| GWO->ABC | 10 | 113,667 | 661 | 112,750 | 114,656 |
| ABC->GWO | 10 | 113,696 | 641 | 112,774 | 114,702 |
| Hybrid w/o energy | 10 | 113,070 | 751 | 111,874 | 114,509 |
| Hybrid w/o distance | 10 | 113,676 | 635 | 112,633 | 114,414 |
| Hybrid w/o balance | 10 | 114,244 | 455 | 113,517 | 114,908 |
| Full Hybrid GWO-ABC | 10 | 113,637 | 663 | 112,601 | 114,549 |

**PDR (ratio)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| GWO only | 10 | 0.9986 | 0.0004 | 0.9978 | 0.9991 |
| ABC only | 10 | 0.9988 | 0.0003 | 0.9983 | 0.9991 |
| GWO->ABC | 10 | 0.9985 | 0.0005 | 0.9977 | 0.9991 |
| ABC->GWO | 10 | 0.9986 | 0.0004 | 0.9978 | 0.9991 |
| Hybrid w/o energy | 10 | 0.9972 | 0.0011 | 0.9954 | 0.9987 |
| Hybrid w/o distance | 10 | 0.9969 | 0.0007 | 0.9960 | 0.9982 |
| Hybrid w/o balance | 10 | 0.9979 | 0.0006 | 0.9969 | 0.9986 |
| Full Hybrid GWO-ABC | 10 | 0.9981 | 0.0006 | 0.9971 | 0.9991 |

**Runtime (s)**

| Algorithm | n | mean | std | min | max |
|---|---:|---:|---:|---:|---:|
| GWO only | 10 | 181.94 | 408.87 | 47.40 | 1345.56 |
| ABC only | 10 | 506.66 | 556.98 | 92.81 | 1388.89 |
| GWO->ABC | 10 | 152.73 | 240.97 | 60.85 | 838.31 |
| ABC->GWO | 10 | 149.41 | 242.00 | 55.85 | 837.89 |
| Hybrid w/o energy | 10 | 554.02 | 557.89 | 133.12 | 1440.10 |
| Hybrid w/o distance | 10 | 460.83 | 557.01 | 119.90 | 1422.34 |
| Hybrid w/o balance | 10 | 538.25 | 558.56 | 122.46 | 1420.49 |
| Full Hybrid GWO-ABC | 10 | 536.72 | 558.48 | 122.94 | 1425.36 |

## Full Hybrid GWO-ABC vs baselines

Improvement % uses ((P − B) / B) × 100 for higher-is-better metrics and ((B − P) / B) × 100 for lower-is-better metrics, so a positive value always means the proposed algorithm did better. p-values: paired two-sided Wilcoxon signed-rank test, Holm-corrected over the baselines. Cliff's δ > 0 favours the proposed algorithm (|δ| < 0.147 negligible, < 0.33 small, < 0.474 medium, otherwise large).

| Metric | Baseline | Better | Improvement % | p (Holm) | Cliff's δ | Effect | Verdict |
|---|---|---|---:|---:|---:|---|---|
| FND | GWO only | higher | +0.11 | 0.656 | +0.10 | negligible | no significant difference |
| FND | ABC only | higher | +0.34 | 0.352 | +0.27 | small | no significant difference |
| FND | GWO->ABC | higher | +0.12 | 1 | +0.11 | negligible | no significant difference |
| FND | ABC->GWO | higher | +0.00 | 1 | +0.00 | negligible | no significant difference |
| FND | Hybrid w/o energy | higher | +1.04 | 0.0137 | +0.62 | large | proposed better |
| FND | Hybrid w/o distance | higher | -0.35 | 0.0352 | -0.36 | medium | proposed worse |
| FND | Hybrid w/o balance | higher | -0.16 | 0.773 | -0.13 | negligible | no significant difference |
| HND | GWO only | higher | +0.00 | 1 | -0.02 | negligible | no significant difference |
| HND | ABC only | higher | +0.00 | 1 | +0.04 | negligible | no significant difference |
| HND | GWO->ABC | higher | +0.01 | 1 | +0.03 | negligible | no significant difference |
| HND | ABC->GWO | higher | +0.03 | 1 | +0.08 | negligible | no significant difference |
| HND | Hybrid w/o energy | higher | +0.45 | 0.0137 | +0.39 | medium | proposed better |
| HND | Hybrid w/o distance | higher | -0.19 | 0.234 | -0.20 | small | no significant difference |
| HND | Hybrid w/o balance | higher | -0.70 | 0.0137 | -0.62 | large | proposed worse |
| LND | GWO only | higher | -0.32 | 0.352 | -0.25 | small | no significant difference |
| LND | ABC only | higher | -0.63 | 0.672 | -0.47 | medium | no significant difference |
| LND | GWO->ABC | higher | -0.27 | 1 | -0.16 | small | no significant difference |
| LND | ABC->GWO | higher | -0.13 | 1 | -0.10 | negligible | no significant difference |
| LND | Hybrid w/o energy | higher | -11.05 | 0.0137 | -0.96 | large | proposed worse |
| LND | Hybrid w/o distance | higher | +0.75 | 0.0703 | +0.47 | medium | no significant difference |
| LND | Hybrid w/o balance | higher | +0.24 | 1 | +0.07 | negligible | no significant difference |
| Node-rounds | GWO only | higher | -0.02 | 1 | -0.02 | negligible | no significant difference |
| Node-rounds | ABC only | higher | -0.05 | 0.523 | -0.08 | negligible | no significant difference |
| Node-rounds | GWO->ABC | higher | +0.01 | 1 | +0.04 | negligible | no significant difference |
| Node-rounds | ABC->GWO | higher | +0.00 | 1 | +0.00 | negligible | no significant difference |
| Node-rounds | Hybrid w/o energy | higher | +0.41 | 0.0137 | +0.38 | medium | proposed better |
| Node-rounds | Hybrid w/o distance | higher | -0.15 | 0.215 | -0.17 | small | no significant difference |
| Node-rounds | Hybrid w/o balance | higher | -0.56 | 0.0137 | -0.58 | large | proposed worse |
| Residual Energy | GWO only | higher | -0.04 | 1 | -0.08 | negligible | no significant difference |
| Residual Energy | ABC only | higher | -0.05 | 0.244 | -0.10 | negligible | no significant difference |
| Residual Energy | GWO->ABC | higher | -0.01 | 1 | -0.06 | negligible | no significant difference |
| Residual Energy | ABC->GWO | higher | +0.01 | 1 | +0.02 | negligible | no significant difference |
| Residual Energy | Hybrid w/o energy | higher | +0.10 | 0.0352 | +0.18 | small | proposed better |
| Residual Energy | Hybrid w/o distance | higher | +0.01 | 1 | +0.02 | negligible | no significant difference |
| Residual Energy | Hybrid w/o balance | higher | -0.20 | 0.0273 | -0.30 | small | proposed worse |
| Energy Consumption | GWO only | lower | -0.05 | 1 | -0.08 | negligible | no significant difference |
| Energy Consumption | ABC only | lower | -0.06 | 0.244 | -0.10 | negligible | no significant difference |
| Energy Consumption | GWO->ABC | lower | -0.01 | 1 | -0.06 | negligible | no significant difference |
| Energy Consumption | ABC->GWO | lower | +0.02 | 1 | +0.02 | negligible | no significant difference |
| Energy Consumption | Hybrid w/o energy | lower | +0.13 | 0.0352 | +0.18 | small | proposed better |
| Energy Consumption | Hybrid w/o distance | lower | +0.02 | 1 | +0.02 | negligible | no significant difference |
| Energy Consumption | Hybrid w/o balance | lower | -0.26 | 0.0273 | -0.30 | small | proposed worse |
| Throughput | GWO only | higher | -0.07 | 0.148 | -0.08 | negligible | no significant difference |
| Throughput | ABC only | higher | -0.13 | 0.137 | -0.14 | negligible | no significant difference |
| Throughput | GWO->ABC | higher | -0.03 | 1 | -0.06 | negligible | no significant difference |
| Throughput | ABC->GWO | higher | -0.05 | 0.48 | -0.08 | negligible | no significant difference |
| Throughput | Hybrid w/o energy | higher | +0.50 | 0.0137 | +0.44 | medium | proposed better |
| Throughput | Hybrid w/o distance | higher | -0.03 | 1 | -0.04 | negligible | no significant difference |
| Throughput | Hybrid w/o balance | higher | -0.53 | 0.0137 | -0.52 | large | proposed worse |
| PDR | GWO only | higher | -0.05 | 0.195 | -0.46 | medium | no significant difference |
| PDR | ABC only | higher | -0.07 | 0.117 | -0.70 | large | no significant difference |
| PDR | GWO->ABC | higher | -0.04 | 0.551 | -0.40 | medium | no significant difference |
| PDR | ABC->GWO | higher | -0.05 | 0.252 | -0.52 | large | no significant difference |
| PDR | Hybrid w/o energy | higher | +0.09 | 0.117 | +0.52 | large | no significant difference |
| PDR | Hybrid w/o distance | higher | +0.12 | 0.0137 | +0.80 | large | proposed better |
| PDR | Hybrid w/o balance | higher | +0.02 | 0.551 | +0.26 | small | no significant difference |
| Avg. Cluster Distance | GWO only | lower | -0.36 | 1 | -0.10 | negligible | no significant difference |
| Avg. Cluster Distance | ABC only | lower | -0.47 | 0.186 | -0.08 | negligible | no significant difference |
| Avg. Cluster Distance | GWO->ABC | lower | -0.14 | 1 | -0.02 | negligible | no significant difference |
| Avg. Cluster Distance | ABC->GWO | lower | +0.10 | 1 | +0.02 | negligible | no significant difference |
| Avg. Cluster Distance | Hybrid w/o energy | lower | +0.88 | 0.041 | +0.12 | negligible | proposed better |
| Avg. Cluster Distance | Hybrid w/o distance | lower | +0.28 | 1 | +0.06 | negligible | no significant difference |
| Avg. Cluster Distance | Hybrid w/o balance | lower | -1.44 | 0.0586 | -0.18 | small | no significant difference |
| Avg. CH-BS Distance | GWO only | lower | +0.16 | 0.322 | +0.12 | negligible | no significant difference |
| Avg. CH-BS Distance | ABC only | lower | +0.24 | 0.322 | +0.06 | negligible | no significant difference |
| Avg. CH-BS Distance | GWO->ABC | lower | +0.03 | 0.863 | -0.00 | negligible | no significant difference |
| Avg. CH-BS Distance | ABC->GWO | lower | +0.08 | 0.863 | +0.04 | negligible | no significant difference |
| Avg. CH-BS Distance | Hybrid w/o energy | lower | -0.12 | 0.322 | -0.08 | negligible | no significant difference |
| Avg. CH-BS Distance | Hybrid w/o distance | lower | -0.50 | 0.0234 | -0.14 | negligible | proposed worse |
| Avg. CH-BS Distance | Hybrid w/o balance | lower | +2.30 | 0.0137 | +0.44 | medium | proposed better |
| Final Fitness | GWO only | lower | +1.13 | 0.0137 | +0.22 | small | proposed better |
| Final Fitness | ABC only | lower | +0.75 | 0.0371 | +0.10 | negligible | proposed better |
| Final Fitness | GWO->ABC | lower | +0.60 | 0.0195 | +0.08 | negligible | proposed better |
| Final Fitness | ABC->GWO | lower | +1.42 | 0.0137 | +0.26 | small | proposed better |
| Final Fitness | Hybrid w/o energy | lower | +1.27 | 0.0137 | +0.20 | small | proposed better |
| Final Fitness | Hybrid w/o distance | lower | -9.24 | 0.0137 | -0.78 | large | proposed worse |
| Final Fitness | Hybrid w/o balance | lower | +9.79 | 0.0137 | +0.84 | large | proposed better |
| Runtime | GWO only | lower | -195.00 | 0.0137 | -0.84 | large | proposed worse |
| Runtime | ABC only | lower | -5.93 | 0.0137 | -0.42 | medium | proposed worse |
| Runtime | GWO->ABC | lower | -251.41 | 0.0137 | -0.88 | large | proposed worse |
| Runtime | ABC->GWO | lower | -259.22 | 0.0137 | -0.88 | large | proposed worse |
| Runtime | Hybrid w/o energy | lower | +3.12 | 0.0137 | +0.42 | medium | proposed better |
| Runtime | Hybrid w/o distance | lower | -16.47 | 0.262 | -0.22 | small | no significant difference |
| Runtime | Hybrid w/o balance | lower | +0.28 | 0.625 | -0.02 | negligible | no significant difference |

### Trade-offs

- **Full Hybrid GWO-ABC vs GWO only** — significantly better: Cluster Imbalance (+15.81%), Final Fitness (+1.13%); significantly worse: Runtime (-195.00%), Runtime / round (-196.45%), Fitness Evaluations (-0.89%, < 1%: practically negligible); no significant difference: FND, HND, LND, Node-rounds, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance, Avg. CH-BS Distance.
- **Full Hybrid GWO-ABC vs ABC only** — significantly better: Cluster Imbalance (+5.83%), Final Fitness (+0.75%, < 1%: practically negligible); significantly worse: Runtime (-5.93%), Runtime / round (-5.81%); no significant difference: FND, HND, LND, Node-rounds, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance, Avg. CH-BS Distance, Fitness Evaluations.
- **Full Hybrid GWO-ABC vs GWO->ABC** — significantly better: Cluster Imbalance (+4.54%), Final Fitness (+0.60%, < 1%: practically negligible), Fitness Evaluations (+1.90%); significantly worse: Runtime (-251.41%), Runtime / round (-252.80%); no significant difference: FND, HND, LND, Node-rounds, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance, Avg. CH-BS Distance.
- **Full Hybrid GWO-ABC vs ABC->GWO** — significantly better: Cluster Imbalance (+9.88%), Final Fitness (+1.42%), Fitness Evaluations (+1.27%); significantly worse: Runtime (-259.22%), Runtime / round (-257.51%); no significant difference: FND, HND, LND, Node-rounds, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance, Avg. CH-BS Distance.
- **Full Hybrid GWO-ABC vs Hybrid w/o energy** — significantly better: FND (+1.04%), HND (+0.45%, < 1%: practically negligible), Node-rounds (+0.41%, < 1%: practically negligible), Residual Energy (+0.10%, < 1%: practically negligible), Energy Consumption (+0.13%, < 1%: practically negligible), Throughput (+0.50%, < 1%: practically negligible), Avg. Cluster Distance (+0.88%, < 1%: practically negligible), Final Fitness (+1.27%), Runtime (+3.12%), Fitness Evaluations (+11.31%); significantly worse: LND (-11.05%); no significant difference: PDR, Avg. CH-BS Distance, Cluster Imbalance, Runtime / round.
- **Full Hybrid GWO-ABC vs Hybrid w/o distance** — significantly better: PDR (+0.12%, < 1%: practically negligible); significantly worse: FND (-0.35%, < 1%: practically negligible), Avg. CH-BS Distance (-0.50%, < 1%: practically negligible), Cluster Imbalance (-97.53%), Final Fitness (-9.24%), Fitness Evaluations (-1.06%); no significant difference: HND, LND, Node-rounds, Residual Energy, Energy Consumption, Throughput, Avg. Cluster Distance, Runtime, Runtime / round.
- **Full Hybrid GWO-ABC vs Hybrid w/o balance** — significantly better: Avg. CH-BS Distance (+2.30%), Cluster Imbalance (+56.27%), Final Fitness (+9.79%); significantly worse: HND (-0.70%, < 1%: practically negligible), Node-rounds (-0.56%, < 1%: practically negligible), Residual Energy (-0.20%, < 1%: practically negligible), Energy Consumption (-0.26%, < 1%: practically negligible), Throughput (-0.53%, < 1%: practically negligible); no significant difference: FND, LND, PDR, Avg. Cluster Distance, Runtime, Runtime / round, Fitness Evaluations.

## Figures

### Initial WSN topology (run 0; every algorithm uses this same network in run 0).

![Initial WSN topology (run 0; every algorithm uses this same network in run 0).](01_topology.png)

**Observed:** 100 nodes uniformly deployed in 100 x 100 m (seed 42); BS at (50, 50). Mean node–BS distance 37.5 m (max 62.9 m); d0 = 87.7 m, so 0% of nodes would use the multipath (d^4) model for a direct BS transmission.

### GWO only: cluster heads selected in round 1 (run 0).

![GWO only: cluster heads selected in round 1 (run 0).](02_ch_selection_GWO_only.png)

**Observed:** 5 CHs; mean CH–BS distance 17.1 m.

### GWO only: cluster formation in round 1 (members joined the nearest CH).

![GWO only: cluster formation in round 1 (members joined the nearest CH).](03_clusters_GWO_only.png)

**Observed:** 5 clusters, sizes 18–25 (CV 0.14); member→CH distance mean 27.5 m, max 61.3 m.

### GWO only: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![GWO only: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_GWO_only.png)

**Observed:** Round 1146: 54 dead, 46 alive. Mean distance to BS — dead nodes 35.0 m, alive nodes 40.4 m (near nodes died first on average).

### ABC only: cluster heads selected in round 1 (run 0).

![ABC only: cluster heads selected in round 1 (run 0).](02_ch_selection_ABC_only.png)

**Observed:** 5 CHs; mean CH–BS distance 24.2 m.

### ABC only: cluster formation in round 1 (members joined the nearest CH).

![ABC only: cluster formation in round 1 (members joined the nearest CH).](03_clusters_ABC_only.png)

**Observed:** 5 clusters, sizes 19–21 (CV 0.04); member→CH distance mean 20.0 m, max 47.9 m.

### ABC only: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![ABC only: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_ABC_only.png)

**Observed:** Round 1147: 59 dead, 41 alive. Mean distance to BS — dead nodes 34.5 m, alive nodes 41.9 m (near nodes died first on average).

### GWO->ABC: cluster heads selected in round 1 (run 0).

![GWO->ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_GWO-ABC.png)

**Observed:** 5 CHs; mean CH–BS distance 23.5 m.

### GWO->ABC: cluster formation in round 1 (members joined the nearest CH).

![GWO->ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_GWO-ABC.png)

**Observed:** 5 clusters, sizes 18–22 (CV 0.07); member→CH distance mean 22.7 m, max 51.6 m.

### GWO->ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![GWO->ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_GWO-ABC.png)

**Observed:** Round 1146: 52 dead, 48 alive. Mean distance to BS — dead nodes 36.0 m, alive nodes 39.2 m (near nodes died first on average).

### ABC->GWO: cluster heads selected in round 1 (run 0).

![ABC->GWO: cluster heads selected in round 1 (run 0).](02_ch_selection_ABC-GWO.png)

**Observed:** 5 CHs; mean CH–BS distance 24.0 m.

### ABC->GWO: cluster formation in round 1 (members joined the nearest CH).

![ABC->GWO: cluster formation in round 1 (members joined the nearest CH).](03_clusters_ABC-GWO.png)

**Observed:** 5 clusters, sizes 13–24 (CV 0.19); member→CH distance mean 21.0 m, max 48.5 m.

### ABC->GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![ABC->GWO: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_ABC-GWO.png)

**Observed:** Round 1146: 51 dead, 49 alive. Mean distance to BS — dead nodes 35.5 m, alive nodes 39.6 m (near nodes died first on average).

### Hybrid w/o energy: cluster heads selected in round 1 (run 0).

![Hybrid w/o energy: cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_wo_energy.png)

**Observed:** 5 CHs; mean CH–BS distance 22.6 m.

### Hybrid w/o energy: cluster formation in round 1 (members joined the nearest CH).

![Hybrid w/o energy: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_wo_energy.png)

**Observed:** 5 clusters, sizes 17–24 (CV 0.15); member→CH distance mean 21.8 m, max 50.3 m.

### Hybrid w/o energy: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid w/o energy: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_wo_energy.png)

**Observed:** Round 1143: 58 dead, 42 alive. Mean distance to BS — dead nodes 36.7 m, alive nodes 38.6 m (near nodes died first on average).

### Hybrid w/o distance: cluster heads selected in round 1 (run 0).

![Hybrid w/o distance: cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_wo_distance.png)

**Observed:** 5 CHs; mean CH–BS distance 32.0 m.

### Hybrid w/o distance: cluster formation in round 1 (members joined the nearest CH).

![Hybrid w/o distance: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_wo_distance.png)

**Observed:** 5 clusters, sizes 19–21 (CV 0.04); member→CH distance mean 18.8 m, max 40.4 m.

### Hybrid w/o distance: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid w/o distance: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_wo_distance.png)

**Observed:** Round 1147: 59 dead, 41 alive. Mean distance to BS — dead nodes 35.7 m, alive nodes 40.2 m (near nodes died first on average).

### Hybrid w/o balance: cluster heads selected in round 1 (run 0).

![Hybrid w/o balance: cluster heads selected in round 1 (run 0).](02_ch_selection_Hybrid_wo_balance.png)

**Observed:** 5 CHs; mean CH–BS distance 11.0 m.

### Hybrid w/o balance: cluster formation in round 1 (members joined the nearest CH).

![Hybrid w/o balance: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Hybrid_wo_balance.png)

**Observed:** 5 clusters, sizes 1–33 (CV 0.63); member→CH distance mean 27.5 m, max 53.0 m.

### Hybrid w/o balance: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Hybrid w/o balance: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Hybrid_wo_balance.png)

**Observed:** Round 1149: 54 dead, 46 alive. Mean distance to BS — dead nodes 33.9 m, alive nodes 41.7 m (near nodes died first on average).

### Full Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).

![Full Hybrid GWO-ABC: cluster heads selected in round 1 (run 0).](02_ch_selection_Full_Hybrid_GWO-ABC.png)

**Observed:** 5 CHs; mean CH–BS distance 20.0 m.

### Full Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).

![Full Hybrid GWO-ABC: cluster formation in round 1 (members joined the nearest CH).](03_clusters_Full_Hybrid_GWO-ABC.png)

**Observed:** 5 clusters, sizes 18–22 (CV 0.08); member→CH distance mean 24.1 m, max 45.9 m.

### Full Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).

![Full Hybrid GWO-ABC: data communication in round 1 — members send to their CH (grey links), CHs aggregate and forward to the BS (arrows).](04_communication_Full_Hybrid_GWO-ABC.png)

**Observed:** 5 clusters, sizes 18–22 (CV 0.08); member→CH distance mean 24.1 m, max 45.9 m.

### Full Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.

![Full Hybrid GWO-ABC: network at its half-node-death round (run 0); dead nodes are marked x, alive nodes shaded by residual energy.](05_dead_nodes_Full_Hybrid_GWO-ABC.png)

**Observed:** Round 1146: 50 dead, 50 alive. Mean distance to BS — dead nodes 34.1 m, alive nodes 40.9 m (near nodes died first on average).

### GWO only: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![GWO only: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_GWO_only.png)

**Observed:** mean best fitness 0.2251 → 0.1801 (20.0% lower); 95% of the improvement reached by iteration 26

### ABC only: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![ABC only: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_ABC_only.png)

**Observed:** mean best fitness 0.2361 → 0.1745 (26.1% lower); 95% of the improvement reached by iteration 17

### GWO->ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![GWO->ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_GWO-ABC.png)

**Observed:** mean best fitness 0.2251 → 0.1681 (25.3% lower); 95% of the improvement reached by iteration 29

### ABC->GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![ABC->GWO: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_ABC-GWO.png)

**Observed:** mean best fitness 0.2361 → 0.1781 (24.6% lower); 95% of the improvement reached by iteration 15

### Hybrid w/o energy: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid w/o energy: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_wo_energy.png)

**Observed:** GWO: mean best fitness 0.1959 → 0.1263 (35.5% lower); 95% of the improvement reached by iteration 21; ABC: mean best fitness 0.2360 → 0.1263 (46.5% lower); 95% of the improvement reached by iteration 16; HYBRID: mean best fitness 0.1959 → 0.1263 (35.5% lower); 95% of the improvement reached by iteration 21

### Hybrid w/o distance: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid w/o distance: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_wo_distance.png)

**Observed:** GWO: mean best fitness 0.0934 → 0.0461 (50.7% lower); 95% of the improvement reached by iteration 20; ABC: mean best fitness 0.1116 → 0.0461 (58.7% lower); 95% of the improvement reached by iteration 17; HYBRID: mean best fitness 0.0904 → 0.0461 (49.1% lower); 95% of the improvement reached by iteration 20

### Hybrid w/o balance: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Hybrid w/o balance: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Hybrid_wo_balance.png)

**Observed:** GWO: mean best fitness 0.1925 → 0.1341 (30.3% lower); 95% of the improvement reached by iteration 12; ABC: mean best fitness 0.2095 → 0.1341 (36.0% lower); 95% of the improvement reached by iteration 11; HYBRID: mean best fitness 0.1916 → 0.1341 (30.0% lower); 95% of the improvement reached by iteration 12

### Full Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).

![Full Hybrid GWO-ABC: best-so-far fitness per iteration of the round-1 CH optimisation (mean ± std over runs).](06_convergence_Full_Hybrid_GWO-ABC.png)

**Observed:** GWO: mean best fitness 0.2361 → 0.1643 (30.4% lower); 95% of the improvement reached by iteration 21; ABC: mean best fitness 0.2762 → 0.1643 (40.5% lower); 95% of the improvement reached by iteration 19; HYBRID: mean best fitness 0.2361 → 0.1643 (30.4% lower); 95% of the improvement reached by iteration 21

### Alive nodes vs rounds.

![Alive nodes vs rounds.](09_alive_vs_rounds.png)

**Observed:** GWO only: FND 1126, HND 1138, LND 1162; ABC only: FND 1124, HND 1138, LND 1165; GWO->ABC: FND 1126, HND 1137, LND 1161; ABC->GWO: FND 1128, HND 1137, LND 1160; Hybrid w/o energy: FND 1116, HND 1132, LND 1302; Hybrid w/o distance: FND 1132, HND 1140, LND 1150; Hybrid w/o balance: FND 1130, HND 1146, LND 1155; Full Hybrid GWO-ABC: FND 1128, HND 1138, LND 1158

### Dead nodes vs rounds.

![Dead nodes vs rounds.](10_dead_vs_rounds.png)

**Observed:** Mirror image of the alive-nodes curve; a steeper rise means nodes die closer together.

### Residual energy vs rounds.

![Residual energy vs rounds.](11_residual_energy_vs_rounds.png)

**Observed:** Residual energy at round 500: GWO only 28.11 J; ABC only 28.12 J; GWO->ABC 28.11 J; ABC->GWO 28.10 J; Hybrid w/o energy 28.08 J; Hybrid w/o distance 28.10 J; Hybrid w/o balance 28.16 J; Full Hybrid GWO-ABC 28.10 J

### Energy consumption vs rounds.

![Energy consumption vs rounds.](12_consumed_energy_vs_rounds.png)

**Observed:** Consumed by round 500: GWO only 21.89 J; ABC only 21.88 J; GWO->ABC 21.89 J; ABC->GWO 21.90 J; Hybrid w/o energy 21.92 J; Hybrid w/o distance 21.90 J; Hybrid w/o balance 21.84 J; Full Hybrid GWO-ABC 21.90 J

### Throughput vs rounds (cumulative).

![Throughput vs rounds (cumulative).](13_packets_delivered_vs_rounds.png)

**Observed:** Total delivered: GWO only 113,713; ABC only 113,780; GWO->ABC 113,667; ABC->GWO 113,696; Hybrid w/o energy 113,070; Hybrid w/o distance 113,676; Hybrid w/o balance 114,244; Full Hybrid GWO-ABC 113,637

### PDR vs rounds.

![PDR vs rounds.](14_pdr_vs_rounds.png)

**Observed:** Final PDR: GWO only 0.9986; ABC only 0.9988; GWO->ABC 0.9985; ABC->GWO 0.9986; Hybrid w/o energy 0.9972; Hybrid w/o distance 0.9969; Hybrid w/o balance 0.9979; Full Hybrid GWO-ABC 0.9981

### CH count vs rounds (20-round rolling mean).

![CH count vs rounds (20-round rolling mean).](15_ch_count_vs_rounds.png)

**Observed:** Mean CHs/round (rounds 1–500): GWO only 4.83 (per-round std 0.55); ABC only 4.79 (per-round std 0.60); GWO->ABC 4.80 (per-round std 0.59); ABC->GWO 4.77 (per-round std 0.60); Hybrid w/o energy 4.76 (per-round std 0.63); Hybrid w/o distance 4.97 (per-round std 0.20); Hybrid w/o balance 5.00 (per-round std 0.02); Full Hybrid GWO-ABC 4.80 (per-round std 0.56)

### Average cluster distance vs rounds (20-round rolling mean).

![Average cluster distance vs rounds (20-round rolling mean).](16_avg_intra_distance_vs_rounds.png)

**Observed:** Mean member→CH distance: GWO only 22.46 m; ABC only 22.44 m; GWO->ABC 22.51 m; ABC->GWO 22.57 m; Hybrid w/o energy 22.75 m; Hybrid w/o distance 22.61 m; Hybrid w/o balance 22.23 m; Full Hybrid GWO-ABC 22.55 m

### Total CH-selection runtime per simulation (log scale, mean ± std).

![Total CH-selection runtime per simulation (log scale, mean ± std).](17_runtime.png)

**Observed:** GWO only 181.94 s (155.53 ms/round, 720,316 fitness evaluations); ABC only 506.66 s (435.76 ms/round, 727,543 fitness evaluations); GWO->ABC 152.73 s (130.69 ms/round, 740,818 fitness evaluations); ABC->GWO 149.41 s (128.97 ms/round, 736,096 fitness evaluations); Hybrid w/o energy 554.02 s (431.68 ms/round, 819,422 fitness evaluations); Hybrid w/o distance 460.83 s (401.31 ms/round, 719,150 fitness evaluations); Hybrid w/o balance 538.25 s (466.13 ms/round, 725,505 fitness evaluations); Full Hybrid GWO-ABC 536.72 s (461.08 ms/round, 726,752 fitness evaluations)

### FND / HND / LND comparison (mean ± std over runs).

![FND / HND / LND comparison (mean ± std over runs).](18_lifetime_fnd_hnd_lnd.png)

**Observed:** GWO only: FND 1126, HND 1138, LND 1162; ABC only: FND 1124, HND 1138, LND 1165; GWO->ABC: FND 1126, HND 1137, LND 1161; ABC->GWO: FND 1128, HND 1137, LND 1160; Hybrid w/o energy: FND 1116, HND 1132, LND 1302; Hybrid w/o distance: FND 1132, HND 1140, LND 1150; Hybrid w/o balance: FND 1130, HND 1146, LND 1155; Full Hybrid GWO-ABC: FND 1128, HND 1138, LND 1158

### Where the energy goes: mean energy per radio activity over rounds 1–500.

![Where the energy goes: mean energy per radio activity over rounds 1–500.](19_energy_breakdown.png)

**Observed:** GWO only: total 21.89 J, largest share member TX (49%); ABC only: total 21.88 J, largest share member TX (49%); GWO->ABC: total 21.89 J, largest share member TX (49%); ABC->GWO: total 21.90 J, largest share member TX (49%); Hybrid w/o energy: total 21.92 J, largest share member TX (49%); Hybrid w/o distance: total 21.90 J, largest share member TX (49%); Hybrid w/o balance: total 21.84 J, largest share member TX (49%); Full Hybrid GWO-ABC: total 21.90 J, largest share member TX (49%)

### Final fitness: same objective and weights for every algorithm.

![Final fitness: same objective and weights for every algorithm.](20_final_fitness.png)

**Observed:** GWO only 0.2467; ABC only 0.2457; GWO->ABC 0.2453; ABC->GWO 0.2474; Hybrid w/o energy 0.2470; Hybrid w/o distance 0.2232; Hybrid w/o balance 0.2703; Full Hybrid GWO-ABC 0.2439

## Metric-by-metric interpretation

#### FND
- **What it represents:** First Node Death: the round in which the first node's residual energy reached 0.
- **How it was calculated:** min over nodes of the round in which residual energy reached 0 (simulation horizon if none died). (higher is better, unit: rounds)
- **Why it matters:** Marks the end of the stability period, during which every sensor still reports.
- **Observed (mean ± std over runs):** GWO only 1,126 (± 7), ABC only 1,124 (± 9), GWO->ABC 1,126 (± 8), ABC->GWO 1,128 (± 8), Hybrid w/o energy 1,116 (± 11), Hybrid w/o distance 1,132 (± 7), Hybrid w/o balance 1,130 (± 5), Full Hybrid GWO-ABC 1,128 (± 7). Best mean: **Hybrid w/o distance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.11% better (improvement formula), p = 0.656 (Holm), Cliff's δ = +0.10 (negligible) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.34% better (improvement formula), p = 0.352 (Holm), Cliff's δ = +0.27 (small) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.12% better (improvement formula), p = 1 (Holm), Cliff's δ = +0.11 (negligible) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.00% equal (improvement formula), p = 1 (Holm), Cliff's δ = +0.00 (negligible) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 1.04% better (improvement formula), p = 0.0137 (Holm), Cliff's δ = +0.62 (large) → **proposed better**; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.35% worse (improvement formula), p = 0.0352 (Holm), Cliff's δ = -0.36 (medium) → **proposed worse** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 0.16% worse (improvement formula), p = 0.773 (Holm), Cliff's δ = -0.13 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 2 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** CH selection that avoids low-energy nodes and rotates the CH role evenly delays the first death; a node chosen repeatedly as CH (e.g. because it is close to the BS) dies early. Measured LND − FND spread (rounds): GWO only 35, ABC only 42, GWO->ABC 35, ABC->GWO 32, Hybrid w/o energy 186, Hybrid w/o distance 18, Hybrid w/o balance 26, Full Hybrid GWO-ABC 30.

#### HND
- **What it represents:** Half Node Death: the round in which at least 50% of the nodes were dead.
- **How it was calculated:** round in which the number of dead nodes reached ceil(N/2). (higher is better, unit: rounds)
- **Why it matters:** Indicates how long the network keeps useful coverage.
- **Observed (mean ± std over runs):** GWO only 1,138 (± 7), ABC only 1,138 (± 7), GWO->ABC 1,137 (± 7), ABC->GWO 1,137 (± 7), Hybrid w/o energy 1,132 (± 8), Hybrid w/o distance 1,140 (± 7), Hybrid w/o balance 1,146 (± 5), Full Hybrid GWO-ABC 1,138 (± 7). Best mean: **Hybrid w/o balance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.00% equal (improvement formula), p = 1 (Holm), Cliff's δ = -0.02 (negligible) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.00% equal (improvement formula), p = 1 (Holm), Cliff's δ = +0.04 (negligible) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.01% better (improvement formula), p = 1 (Holm), Cliff's δ = +0.03 (negligible) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.03% better (improvement formula), p = 1 (Holm), Cliff's δ = +0.08 (negligible) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 0.45% better (improvement formula), p = 0.0137 (Holm), Cliff's δ = +0.39 (medium) → **proposed better** — practically small; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.19% worse (improvement formula), p = 0.234 (Holm), Cliff's δ = -0.20 (small) → **no significant difference** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 0.70% worse (improvement formula), p = 0.0137 (Holm), Cliff's δ = -0.62 (large) → **proposed worse** — practically small.
- **Is the difference meaningful?** 2 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** HND reflects how evenly energy is drained across the whole network.

#### LND
- **What it represents:** Last Node Death: the round in which the last alive node died.
- **How it was calculated:** round in which the last node died (simulation horizon if nodes were still alive). (higher is better, unit: rounds)
- **Why it matters:** Upper bound of the network lifetime.
- **Observed (mean ± std over runs):** GWO only 1,162 (± 12), ABC only 1,165 (± 8), GWO->ABC 1,161 (± 9), ABC->GWO 1,160 (± 13), Hybrid w/o energy 1,302 (± 96), Hybrid w/o distance 1,150 (± 6), Hybrid w/o balance 1,155 (± 4), Full Hybrid GWO-ABC 1,158 (± 13). Best mean: **Hybrid w/o energy**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.32% worse (improvement formula), p = 0.352 (Holm), Cliff's δ = -0.25 (small) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.63% worse (improvement formula), p = 0.672 (Holm), Cliff's δ = -0.47 (medium) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.27% worse (improvement formula), p = 1 (Holm), Cliff's δ = -0.16 (small) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.13% worse (improvement formula), p = 1 (Holm), Cliff's δ = -0.10 (negligible) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 11.05% worse (improvement formula), p = 0.0137 (Holm), Cliff's δ = -0.96 (large) → **proposed worse**; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.75% better (improvement formula), p = 0.0703 (Holm), Cliff's δ = +0.47 (medium) → **no significant difference** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 0.24% better (improvement formula), p = 1 (Holm), Cliff's δ = +0.07 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** A very even energy drain makes all nodes die at nearly the same time: FND is delayed but the last node also dies sooner. Uneven drain leaves a few nodes with spare energy that keep running. Measured LND − FND spread (rounds): GWO only 35, ABC only 42, GWO->ABC 35, ABC->GWO 32, Hybrid w/o energy 186, Hybrid w/o distance 18, Hybrid w/o balance 26, Full Hybrid GWO-ABC 30.

#### Residual Energy
- **What it represents:** Total residual energy of all nodes at the checkpoint round.
- **How it was calculated:** sum of node residual energies after the checkpoint round. (higher is better, unit: J)
- **Why it matters:** More energy left at the same round means cheaper operation.
- **Observed (mean ± std over runs):** GWO only 28.115 (± 0.094), ABC only 28.118 (± 0.106), GWO->ABC 28.107 (± 0.113), ABC->GWO 28.100 (± 0.099), Hybrid w/o energy 28.077 (± 0.113), Hybrid w/o distance 28.101 (± 0.098), Hybrid w/o balance 28.160 (± 0.089), Full Hybrid GWO-ABC 28.105 (± 0.109). Best mean: **Hybrid w/o balance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.04% worse (improvement formula), p = 1 (Holm), Cliff's δ = -0.08 (negligible) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.244 (Holm), Cliff's δ = -0.10 (negligible) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.01% worse (improvement formula), p = 1 (Holm), Cliff's δ = -0.06 (negligible) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.01% better (improvement formula), p = 1 (Holm), Cliff's δ = +0.02 (negligible) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 0.10% better (improvement formula), p = 0.0352 (Holm), Cliff's δ = +0.18 (small) → **proposed better** — practically small; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.01% better (improvement formula), p = 1 (Holm), Cliff's δ = +0.02 (negligible) → **no significant difference** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 0.20% worse (improvement formula), p = 0.0273 (Holm), Cliff's δ = -0.30 (small) → **proposed worse** — practically small.
- **Is the difference meaningful?** 2 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Residual energy at a fixed round depends on per-round radio cost: shorter member->CH links and shorter or fewer CH->BS links consume less.

#### Energy Consumption
- **What it represents:** Initial total energy minus residual energy at the checkpoint round.
- **How it was calculated:** N * E0 - residual energy at the checkpoint round. (lower is better, unit: J)
- **Why it matters:** Energy spent to operate the network for the same number of rounds.
- **Observed (mean ± std over runs):** GWO only 21.885 (± 0.094), ABC only 21.882 (± 0.106), GWO->ABC 21.893 (± 0.113), ABC->GWO 21.900 (± 0.099), Hybrid w/o energy 21.923 (± 0.113), Hybrid w/o distance 21.899 (± 0.098), Hybrid w/o balance 21.840 (± 0.089), Full Hybrid GWO-ABC 21.895 (± 0.109). Best mean: **Hybrid w/o balance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.05% worse (reduction formula), p = 1 (Holm), Cliff's δ = -0.08 (negligible) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.06% worse (reduction formula), p = 0.244 (Holm), Cliff's δ = -0.10 (negligible) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.01% worse (reduction formula), p = 1 (Holm), Cliff's δ = -0.06 (negligible) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.02% better (reduction formula), p = 1 (Holm), Cliff's δ = +0.02 (negligible) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 0.13% better (reduction formula), p = 0.0352 (Holm), Cliff's δ = +0.18 (small) → **proposed better** — practically small; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.02% better (reduction formula), p = 1 (Holm), Cliff's δ = +0.02 (negligible) → **no significant difference** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 0.26% worse (reduction formula), p = 0.0273 (Holm), Cliff's δ = -0.30 (small) → **proposed worse** — practically small.
- **Is the difference meaningful?** 2 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Consumption is the complement of residual energy at the same checkpoint.

#### Throughput
- **What it represents:** Total sensor data packets delivered to the BS over the whole simulation (directly or inside an aggregated CH packet).
- **How it was calculated:** count of sensor readings that reached the BS over the whole run. (higher is better, unit: packets)
- **Why it matters:** Amount of sensed data the application actually receives.
- **Observed (mean ± std over runs):** GWO only 113,713 (± 627), ABC only 113,780 (± 640), GWO->ABC 113,667 (± 661), ABC->GWO 113,696 (± 641), Hybrid w/o energy 113,070 (± 751), Hybrid w/o distance 113,676 (± 635), Hybrid w/o balance 114,244 (± 455), Full Hybrid GWO-ABC 113,637 (± 663). Best mean: **Hybrid w/o balance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.07% worse (improvement formula), p = 0.148 (Holm), Cliff's δ = -0.08 (negligible) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.13% worse (improvement formula), p = 0.137 (Holm), Cliff's δ = -0.14 (negligible) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.03% worse (improvement formula), p = 1 (Holm), Cliff's δ = -0.06 (negligible) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.48 (Holm), Cliff's δ = -0.08 (negligible) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 0.50% better (improvement formula), p = 0.0137 (Holm), Cliff's δ = +0.44 (medium) → **proposed better** — practically small; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.03% worse (improvement formula), p = 1 (Holm), Cliff's δ = -0.04 (negligible) → **no significant difference** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 0.53% worse (improvement formula), p = 0.0137 (Holm), Cliff's δ = -0.52 (large) → **proposed worse** — practically small.
- **Is the difference meaningful?** 2 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Throughput grows with the number of rounds in which nodes are alive and with the share of packets that are not lost to CHs dying mid-round.

#### PDR
- **What it represents:** Packet Delivery Ratio = delivered data packets / generated data packets.
- **How it was calculated:** delivered readings / generated readings over the whole run. (higher is better, unit: ratio)
- **Why it matters:** Reliability: share of generated readings that reach the BS.
- **Observed (mean ± std over runs):** GWO only 0.9986 (± 0.0004), ABC only 0.9988 (± 0.0003), GWO->ABC 0.9985 (± 0.0005), ABC->GWO 0.9986 (± 0.0004), Hybrid w/o energy 0.9972 (± 0.0011), Hybrid w/o distance 0.9969 (± 0.0007), Hybrid w/o balance 0.9979 (± 0.0006), Full Hybrid GWO-ABC 0.9981 (± 0.0006). Best mean: **ABC only**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.195 (Holm), Cliff's δ = -0.46 (medium) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.07% worse (improvement formula), p = 0.117 (Holm), Cliff's δ = -0.70 (large) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.04% worse (improvement formula), p = 0.551 (Holm), Cliff's δ = -0.40 (medium) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.252 (Holm), Cliff's δ = -0.52 (large) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 0.09% better (improvement formula), p = 0.117 (Holm), Cliff's δ = +0.52 (large) → **no significant difference** — practically small; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.12% better (improvement formula), p = 0.0137 (Holm), Cliff's δ = +0.80 (large) → **proposed better** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 0.02% better (improvement formula), p = 0.551 (Holm), Cliff's δ = +0.26 (small) → **no significant difference** — practically small.
- **Is the difference meaningful?** 1 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Packets are lost when a CH runs out of energy before forwarding its cluster's data, or when a node dies while transmitting. Energy-feasibility checks on CHs reduce such losses.

#### Avg. Cluster Distance
- **What it represents:** Mean member->CH distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean member->CH distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** Shorter intra-cluster links cost less transmission energy (d^2 / d^4).
- **Observed (mean ± std over runs):** GWO only 22.465 (± 0.765), ABC only 22.440 (± 0.855), GWO->ABC 22.515 (± 0.886), ABC->GWO 22.568 (± 0.798), Hybrid w/o energy 22.745 (± 0.891), Hybrid w/o distance 22.609 (± 0.724), Hybrid w/o balance 22.226 (± 0.773), Full Hybrid GWO-ABC 22.546 (± 0.871). Best mean: **Hybrid w/o balance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.36% worse (reduction formula), p = 1 (Holm), Cliff's δ = -0.10 (negligible) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.47% worse (reduction formula), p = 0.186 (Holm), Cliff's δ = -0.08 (negligible) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.14% worse (reduction formula), p = 1 (Holm), Cliff's δ = -0.02 (negligible) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.10% better (reduction formula), p = 1 (Holm), Cliff's δ = +0.02 (negligible) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 0.88% better (reduction formula), p = 0.041 (Holm), Cliff's δ = +0.12 (negligible) → **proposed better** — practically small; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.28% better (reduction formula), p = 1 (Holm), Cliff's δ = +0.06 (negligible) → **no significant difference** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 1.44% worse (reduction formula), p = 0.0586 (Holm), Cliff's δ = -0.18 (small) → **no significant difference**.
- **Is the difference meaningful?** 1 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness function explicitly penalises member->CH distance; LEACH places CHs at random positions, which typically lengthens member links.

#### Avg. CH-BS Distance
- **What it represents:** Mean CH->BS distance, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round mean CH->BS distance, averaged over rounds 1..checkpoint. (lower is better, unit: m)
- **Why it matters:** CH->BS is the longest and most expensive hop.
- **Observed (mean ± std over runs):** GWO only 37.925 (± 1.093), ABC only 37.956 (± 1.072), GWO->ABC 37.876 (± 1.118), ABC->GWO 37.891 (± 1.118), Hybrid w/o energy 37.817 (± 1.142), Hybrid w/o distance 37.675 (± 1.122), Hybrid w/o balance 38.755 (± 1.017), Full Hybrid GWO-ABC 37.863 (± 1.160). Best mean: **Hybrid w/o distance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.16% better (reduction formula), p = 0.322 (Holm), Cliff's δ = +0.12 (negligible) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.24% better (reduction formula), p = 0.322 (Holm), Cliff's δ = +0.06 (negligible) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.03% better (reduction formula), p = 0.863 (Holm), Cliff's δ = -0.00 (negligible) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.08% better (reduction formula), p = 0.863 (Holm), Cliff's δ = +0.04 (negligible) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 0.12% worse (reduction formula), p = 0.322 (Holm), Cliff's δ = -0.08 (negligible) → **no significant difference** — practically small; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.50% worse (reduction formula), p = 0.0234 (Holm), Cliff's δ = -0.14 (negligible) → **proposed worse** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 2.30% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.44 (medium) → **proposed better**.
- **Is the difference meaningful?** 2 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises CH->BS distance, but the energy-eligibility rule and the energy term limit how often nodes near the BS can be selected.

#### Runtime
- **What it represents:** Total wall-clock time spent selecting CHs over the whole simulation.
- **How it was calculated:** sum of wall-clock CH-selection time over all rounds (time.perf_counter). (lower is better, unit: s)
- **Why it matters:** Computational cost of the CH selection algorithm.
- **Observed (mean ± std over runs):** GWO only 181.94 (± 408.87), ABC only 506.66 (± 556.98), GWO->ABC 152.73 (± 240.97), ABC->GWO 149.41 (± 242.00), Hybrid w/o energy 554.02 (± 557.89), Hybrid w/o distance 460.83 (± 557.01), Hybrid w/o balance 538.25 (± 558.56), Full Hybrid GWO-ABC 536.72 (± 558.48). Best mean: **ABC->GWO**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 195.00% worse (reduction formula), p = 0.0137 (Holm), Cliff's δ = -0.84 (large) → **proposed worse**; vs ABC only: Full Hybrid GWO-ABC is 5.93% worse (reduction formula), p = 0.0137 (Holm), Cliff's δ = -0.42 (medium) → **proposed worse**; vs GWO->ABC: Full Hybrid GWO-ABC is 251.41% worse (reduction formula), p = 0.0137 (Holm), Cliff's δ = -0.88 (large) → **proposed worse**; vs ABC->GWO: Full Hybrid GWO-ABC is 259.22% worse (reduction formula), p = 0.0137 (Holm), Cliff's δ = -0.88 (large) → **proposed worse**; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 3.12% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.42 (medium) → **proposed better**; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 16.47% worse (reduction formula), p = 0.262 (Holm), Cliff's δ = -0.22 (small) → **no significant difference**; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 0.28% better (reduction formula), p = 0.625 (Holm), Cliff's δ = -0.02 (negligible) → **no significant difference** — practically small.
- **Is the difference meaningful?** 5 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Metaheuristics evaluate hundreds of candidate CH sets per round; LEACH needs one random draw per node. The hybrid runs two populations and more operators per iteration, which adds overhead even at an equal number of fitness evaluations.

#### Final Fitness
- **What it represents:** Mean per-round fitness (same function and weights for every algorithm) of the CH set actually used, over rounds 1..checkpoint. Lower is better.
- **How it was calculated:** per round fitness of the CH set used (same weights for all), mean over rounds 1..checkpoint. (lower is better, unit: -)
- **Why it matters:** Quality of the CH configurations according to the optimisation objective.
- **Observed (mean ± std over runs):** GWO only 0.2467 (± 0.0128), ABC only 0.2457 (± 0.0135), GWO->ABC 0.2453 (± 0.0126), ABC->GWO 0.2474 (± 0.0126), Hybrid w/o energy 0.2470 (± 0.0136), Hybrid w/o distance 0.2232 (± 0.0118), Hybrid w/o balance 0.2703 (± 0.0127), Full Hybrid GWO-ABC 0.2439 (± 0.0128). Best mean: **Hybrid w/o distance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 1.13% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.22 (small) → **proposed better**; vs ABC only: Full Hybrid GWO-ABC is 0.75% better (reduction formula), p = 0.0371 (Holm), Cliff's δ = +0.10 (negligible) → **proposed better** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.60% better (reduction formula), p = 0.0195 (Holm), Cliff's δ = +0.08 (negligible) → **proposed better** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 1.42% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.26 (small) → **proposed better**; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 1.27% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.20 (small) → **proposed better**; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 9.24% worse (reduction formula), p = 0.0137 (Holm), Cliff's δ = -0.78 (large) → **proposed worse**; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 9.79% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.84 (large) → **proposed better**.
- **Is the difference meaningful?** 7 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** Optimisers minimise this objective directly; LEACH does not use it, and rounds in which LEACH elects zero CHs or too many receive the invalid-solution penalty.

#### Node-rounds
- **What it represents:** Sum over rounds of the number of alive nodes (area under the alive-nodes curve).
- **How it was calculated:** sum over rounds of alive nodes. (higher is better, unit: node x rounds)
- **Why it matters:** Single-number lifetime measure that accounts for the whole death curve.
- **Observed (mean ± std over runs):** GWO only 113,778 (± 652), ABC only 113,815 (± 638), GWO->ABC 113,739 (± 696), ABC->GWO 113,751 (± 659), Hybrid w/o energy 113,288 (± 747), Hybrid w/o distance 113,928 (± 666), Hybrid w/o balance 114,390 (± 483), Full Hybrid GWO-ABC 113,754 (± 662). Best mean: **Hybrid w/o balance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 0.02% worse (improvement formula), p = 1 (Holm), Cliff's δ = -0.02 (negligible) → **no significant difference** — practically small; vs ABC only: Full Hybrid GWO-ABC is 0.05% worse (improvement formula), p = 0.523 (Holm), Cliff's δ = -0.08 (negligible) → **no significant difference** — practically small; vs GWO->ABC: Full Hybrid GWO-ABC is 0.01% better (improvement formula), p = 1 (Holm), Cliff's δ = +0.04 (negligible) → **no significant difference** — practically small; vs ABC->GWO: Full Hybrid GWO-ABC is 0.00% better (improvement formula), p = 1 (Holm), Cliff's δ = +0.00 (negligible) → **no significant difference** — practically small; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 0.41% better (improvement formula), p = 0.0137 (Holm), Cliff's δ = +0.38 (medium) → **proposed better** — practically small; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 0.15% worse (improvement formula), p = 0.215 (Holm), Cliff's δ = -0.17 (small) → **no significant difference** — practically small; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 0.56% worse (improvement formula), p = 0.0137 (Holm), Cliff's δ = -0.58 (large) → **proposed worse** — practically small.
- **Is the difference meaningful?** 2 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The area under the alive-nodes curve combines stability period and tail length.

#### Cluster Imbalance
- **What it represents:** Coefficient of variation of cluster sizes, averaged over rounds 1..checkpoint.
- **How it was calculated:** per round std/mean of cluster sizes, averaged over rounds 1..checkpoint. (lower is better, unit: CV)
- **Why it matters:** Balanced clusters spread the CH load evenly.
- **Observed (mean ± std over runs):** GWO only 0.1760 (± 0.0096), ABC only 0.1573 (± 0.0096), GWO->ABC 0.1552 (± 0.0092), ABC->GWO 0.1644 (± 0.0070), Hybrid w/o energy 0.1506 (± 0.0086), Hybrid w/o distance 0.0750 (± 0.0091), Hybrid w/o balance 0.3388 (± 0.0202), Full Hybrid GWO-ABC 0.1481 (± 0.0073). Best mean: **Hybrid w/o distance**.
- **Proposed vs baselines:** vs GWO only: Full Hybrid GWO-ABC is 15.81% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.98 (large) → **proposed better**; vs ABC only: Full Hybrid GWO-ABC is 5.83% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.64 (large) → **proposed better**; vs GWO->ABC: Full Hybrid GWO-ABC is 4.54% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.54 (large) → **proposed better**; vs ABC->GWO: Full Hybrid GWO-ABC is 9.88% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +0.86 (large) → **proposed better**; vs Hybrid w/o energy: Full Hybrid GWO-ABC is 1.65% better (reduction formula), p = 0.275 (Holm), Cliff's δ = +0.14 (negligible) → **no significant difference**; vs Hybrid w/o distance: Full Hybrid GWO-ABC is 97.53% worse (reduction formula), p = 0.0137 (Holm), Cliff's δ = -1.00 (large) → **proposed worse**; vs Hybrid w/o balance: Full Hybrid GWO-ABC is 56.27% better (reduction formula), p = 0.0137 (Holm), Cliff's δ = +1.00 (large) → **proposed better**.
- **Is the difference meaningful?** 6 of 7 comparisons are statistically significant at α = 0.05 after Holm correction. Differences that are not significant, or below 1.0% in size, should not be presented as improvements.
- **Possible explanation:** The fitness penalises unequal cluster sizes; nearest-CH assignment does not.

## Cluster-head records (run 0)

Every selected CH of every round is recorded in `ch_log_run0.csv` (round, CH id, coordinates, residual energy at selection, distance to the BS, cluster size including the CH). Dead and duplicate CHs are removed before clustering, so only valid CHs appear.

**Reproducibility check:** run 0 of every algorithm was re-simulated from `config.json` and its seed; all checked results (fnd, hnd, lnd, node_rounds, throughput_packets, packets_generated, residual_energy_cp, final_fitness) are identical to the saved values (`reproducibility_check_run0.csv`).

### GWO only

Over 1163 rounds with CHs: 4.75 CHs/round on average; mean CH residual energy at selection 0.2524 J; mean CH–BS distance 38.09 m; 100 distinct nodes served as CH, the most frequent one 67 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 28 | 45.89 | 56.87 | 0.5 | 8.008 | 21 |
| 30 | 66.84 | 47.11 | 0.5 | 17.09 | 18 |
| 31 | 56.52 | 76.5 | 0.5 | 27.29 | 18 |
| 70 | 48.67 | 49.07 | 0.5 | 1.626 | 25 |
| 92 | 77.2 | 66.17 | 0.5 | 31.64 | 18 |

### ABC only

Over 1159 rounds with CHs: 4.76 CHs/round on average; mean CH residual energy at selection 0.2520 J; mean CH–BS distance 38.22 m; 100 distinct nodes served as CH, the most frequent one 66 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 44 | 16.13 | 50.1 | 0.5 | 33.87 | 21 |
| 52 | 77.88 | 71.69 | 0.5 | 35.32 | 21 |
| 53 | 44.94 | 27.22 | 0.5 | 23.33 | 20 |
| 59 | 43.21 | 62.73 | 0.5 | 14.43 | 19 |
| 82 | 55.49 | 37.09 | 0.5 | 14.02 | 19 |

### GWO->ABC

Over 1157 rounds with CHs: 4.75 CHs/round on average; mean CH residual energy at selection 0.2534 J; mean CH–BS distance 38.03 m; 100 distinct nodes served as CH, the most frequent one 66 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 31 | 56.52 | 76.5 | 0.5 | 27.29 | 18 |
| 52 | 77.88 | 71.69 | 0.5 | 35.32 | 19 |
| 63 | 32.99 | 14.45 | 0.5 | 39.41 | 21 |
| 70 | 48.67 | 49.07 | 0.5 | 1.626 | 22 |
| 82 | 55.49 | 37.09 | 0.5 | 14.02 | 20 |

### ABC->GWO

Over 1157 rounds with CHs: 4.73 CHs/round on average; mean CH residual energy at selection 0.2527 J; mean CH–BS distance 38.20 m; 100 distinct nodes served as CH, the most frequent one 64 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 4 | 12.81 | 45.04 | 0.5 | 37.52 | 22 |
| 40 | 66.43 | 40.64 | 0.5 | 18.91 | 13 |
| 52 | 77.88 | 71.69 | 0.5 | 35.32 | 21 |
| 59 | 43.21 | 62.73 | 0.5 | 14.43 | 24 |
| 82 | 55.49 | 37.09 | 0.5 | 14.02 | 20 |

### Hybrid w/o energy

Over 1203 rounds with CHs: 4.46 CHs/round on average; mean CH residual energy at selection 0.2548 J; mean CH–BS distance 38.32 m; 100 distinct nodes served as CH, the most frequent one 88 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 52 | 77.88 | 71.69 | 0.5 | 35.32 | 24 |
| 56 | 30.6 | 57.92 | 0.5 | 20.96 | 23 |
| 66 | 58.11 | 34.69 | 0.5 | 17.33 | 17 |
| 85 | 29.09 | 51.51 | 0.5 | 20.96 | 17 |
| 91 | 51.89 | 31.59 | 0.5 | 18.5 | 19 |

### Hybrid w/o distance

Over 1153 rounds with CHs: 4.97 CHs/round on average; mean CH residual energy at selection 0.2517 J; mean CH–BS distance 37.22 m; 100 distinct nodes served as CH, the most frequent one 61 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 7 | 44.34 | 22.72 | 0.5 | 27.86 | 19 |
| 20 | 43.72 | 83.27 | 0.5 | 33.86 | 20 |
| 52 | 77.88 | 71.69 | 0.5 | 35.32 | 21 |
| 62 | 4.161 | 49.4 | 0.5 | 45.84 | 19 |
| 66 | 58.11 | 34.69 | 0.5 | 17.33 | 21 |

### Hybrid w/o balance

Over 1158 rounds with CHs: 4.96 CHs/round on average; mean CH residual energy at selection 0.2529 J; mean CH–BS distance 38.73 m; 100 distinct nodes served as CH, the most frequent one 91 times.

Round 1 cluster heads:

| CH id | x (m) | y (m) | Residual energy (J) | CH–BS (m) | Cluster size |
|---|---:|---:|---:|---:|---:|
| 28 | 45.89 | 56.87 | 0.5 | 8.008 | 9 |
| 32 | 63.47 | 55.36 | 0.5 | 14.5 | 27 |
| 70 | 48.67 | 49.07 | 0.5 | 1.626 | 1 |
| 73 | 33.16 | 52.07 | 0.5 | 16.97 | 33 |
| 82 | 55.49 | 37.09 | 0.5 | 14.02 | 30 |

### Full Hybrid GWO-ABC

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
python main.py reproduce "C:\Users\Admin\Hybrid-GWO-ABC-WSN\results\ablation"
```

`config.json` holds every parameter; `experiment.json` holds the algorithms, run count and seeds.

## Data-quality note

Runtime values in this folder were measured with 11 simulations running in parallel, so they include scheduling noise; see `results/runtime_benchmark/report.md` for a clean sequential runtime comparison.
Runs with runtime/round > 3× their algorithm's median (most likely timed across a system sleep): ABC only run 0 (1198 ms/round vs median 87), Hybrid w/o energy run 0 (1187 ms/round vs median 115), Hybrid w/o distance run 0 (1234 ms/round vs median 114), Hybrid w/o balance run 0 (1227 ms/round vs median 116), Full Hybrid GWO-ABC run 0 (1227 ms/round vs median 115), GWO only run 1 (1147 ms/round vs median 46), ABC only run 1 (1190 ms/round vs median 87), Hybrid w/o energy run 1 (1052 ms/round vs median 115), Hybrid w/o distance run 1 (1234 ms/round vs median 114), Hybrid w/o balance run 1 (1235 ms/round vs median 116), Full Hybrid GWO-ABC run 1 (1211 ms/round vs median 115), ABC only run 8 (743 ms/round vs median 87), GWO->ABC run 8 (713 ms/round vs median 67), ABC->GWO run 8 (724 ms/round vs median 64), Hybrid w/o energy run 8 (661 ms/round vs median 115), Hybrid w/o balance run 8 (773 ms/round vs median 116), Full Hybrid GWO-ABC run 8 (760 ms/round vs median 115), ABC only run 9 (721 ms/round vs median 87), Hybrid w/o energy run 9 (758 ms/round vs median 115), Hybrid w/o distance run 9 (772 ms/round vs median 114), Hybrid w/o balance run 9 (761 ms/round vs median 116), Full Hybrid GWO-ABC run 9 (747 ms/round vs median 115). Their raw values are kept unchanged; only runtime metrics are affected (energy, lifetime and packet metrics count rounds, not seconds).
