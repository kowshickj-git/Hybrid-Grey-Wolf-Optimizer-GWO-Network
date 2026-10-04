# Scenario overview

Mean over runs for each scenario (full details, statistics and figures in each scenario folder).

## S1_100nodes

_20 runs._ [report](S1_100nodes/report.md)

| Algorithm | FND | HND | LND | Residual Energy | Throughput | PDR | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|
| Random | 806.9 | 1,125 | 1,321 | 27.75 | 1.099e+05 | 0.9898 | 0.557 |
| LEACH | 891.5 | 1,104 | 1,287 | 27.4 | 1.089e+05 | 0.9892 | 0.05626 |
| GWO | 1,126 | 1,138 | 1,162 | 28.11 | 1.137e+05 | 0.9985 | 54.54 |
| ABC | 1,125 | 1,138 | 1,162 | 28.11 | 1.137e+05 | 0.9986 | 101.2 |
| Hybrid GWO-ABC | 1,128 | 1,138 | 1,158 | 28.1 | 1.137e+05 | 0.9982 | 132.1 |

- **Hybrid GWO-ABC vs Random** — significantly better: FND (+39.75%), HND (+1.11%), Residual Energy (+1.27%), Energy Consumption (+1.58%), Throughput (+3.42%), PDR (+0.85%, < 1%: practically negligible), Avg. Cluster Distance (+9.95%), Avg. CH-BS Distance (+0.83%, < 1%: practically negligible), Final Fitness (+17.80%); significantly worse: LND (-12.33%), Runtime (-23624.50%); no significant difference: none.
- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+26.49%), HND (+3.02%), Residual Energy (+2.58%), Energy Consumption (+3.13%), Throughput (+4.39%), PDR (+0.91%, < 1%: practically negligible), Avg. Cluster Distance (+16.66%), Avg. CH-BS Distance (+0.85%, < 1%: practically negligible), Final Fitness (+82.06%); significantly worse: LND (-9.99%), Runtime (-234767.67%); no significant difference: none.
- **Hybrid GWO-ABC vs GWO** — significantly better: Avg. CH-BS Distance (+0.15%, < 1%: practically negligible), Final Fitness (+1.19%); significantly worse: Runtime (-142.31%); no significant difference: FND, HND, LND, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance.
- **Hybrid GWO-ABC vs ABC** — significantly better: Final Fitness (+0.62%, < 1%: practically negligible); significantly worse: Residual Energy (-0.04%, < 1%: practically negligible), Energy Consumption (-0.05%, < 1%: practically negligible), Avg. Cluster Distance (-0.41%, < 1%: practically negligible), Runtime (-30.61%); no significant difference: FND, HND, LND, Throughput, PDR, Avg. CH-BS Distance.

## S2_200nodes

_10 runs._ [report](S2_200nodes/report.md)

| Algorithm | FND | HND | LND | Residual Energy | Throughput | PDR | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|
| LEACH | 921.1 | 1,148 | 1,401 | 56.93 | 2.283e+05 | 0.9881 | 0.08059 |
| GWO | 1,164 | 1,176 | 1,215 | 57.51 | 2.345e+05 | 0.9971 | 93.55 |
| ABC | 1,162 | 1,175 | 1,205 | 57.51 | 2.345e+05 | 0.9971 | 141.8 |
| Hybrid GWO-ABC | 1,162 | 1,174 | 1,200 | 57.47 | 2.341e+05 | 0.9966 | 176.5 |

- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+26.10%), HND (+2.25%), Residual Energy (+0.96%, < 1%: practically negligible), Energy Consumption (+1.27%), Throughput (+2.57%), PDR (+0.86%, < 1%: practically negligible), Avg. Cluster Distance (+13.45%), Avg. CH-BS Distance (+1.11%), Final Fitness (+79.39%); significantly worse: LND (-14.32%), Runtime (-218939.38%); no significant difference: none.
- **Hybrid GWO-ABC vs GWO** — significantly better: Avg. CH-BS Distance (+0.32%, < 1%: practically negligible), Final Fitness (+1.31%); significantly worse: HND (-0.10%, < 1%: practically negligible), LND (-1.19%), Residual Energy (-0.07%, < 1%: practically negligible), Energy Consumption (-0.10%, < 1%: practically negligible), Throughput (-0.17%, < 1%: practically negligible), Avg. Cluster Distance (-1.34%), Runtime (-88.70%); no significant difference: FND, PDR.
- **Hybrid GWO-ABC vs ABC** — significantly better: Avg. CH-BS Distance (+0.61%, < 1%: practically negligible), Final Fitness (+3.53%); significantly worse: HND (-0.09%, < 1%: practically negligible), Residual Energy (-0.06%, < 1%: practically negligible), Energy Consumption (-0.08%, < 1%: practically negligible), Throughput (-0.14%, < 1%: practically negligible), Avg. Cluster Distance (-1.40%), Runtime (-24.48%); no significant difference: FND, LND, PDR.

## S3_300nodes

_10 runs._ [report](S3_300nodes/report.md)

| Algorithm | FND | HND | LND | Residual Energy | Throughput | PDR | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|
| LEACH | 939.6 | 1,164 | 1,440 | 86.39 | 3.483e+05 | 0.9876 | 0.09279 |
| GWO | 1,174 | 1,188 | 1,244 | 86.89 | 3.55e+05 | 0.9961 | 334.2 |
| ABC | 1,172 | 1,187 | 1,229 | 86.85 | 3.547e+05 | 0.9959 | 388.2 |
| Hybrid GWO-ABC | 1,173 | 1,187 | 1,236 | 86.86 | 3.547e+05 | 0.9957 | 608 |

- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+24.86%), HND (+1.98%), Residual Energy (+0.54%, < 1%: practically negligible), Energy Consumption (+0.74%, < 1%: practically negligible), Throughput (+1.84%), PDR (+0.82%, < 1%: practically negligible), Avg. Cluster Distance (+12.43%), Avg. CH-BS Distance (+1.92%), Final Fitness (+57.53%); significantly worse: LND (-14.22%), Runtime (-655157.92%); no significant difference: none.
- **Hybrid GWO-ABC vs GWO** — significantly better: Avg. CH-BS Distance (+0.16%, < 1%: practically negligible), Final Fitness (+1.61%); significantly worse: Residual Energy (-0.04%, < 1%: practically negligible), Energy Consumption (-0.06%, < 1%: practically negligible), Avg. Cluster Distance (-1.09%), Runtime (-81.91%); no significant difference: FND, HND, LND, Throughput, PDR.
- **Hybrid GWO-ABC vs ABC** — significantly better: Avg. CH-BS Distance (+0.62%, < 1%: practically negligible), Final Fitness (+5.30%); significantly worse: Runtime (-56.63%); no significant difference: FND, HND, LND, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance.

## S4_100nodes_BS_edge

_10 runs._ [report](S4_100nodes_BS_edge/report.md)

| Algorithm | FND | HND | LND | Residual Energy | Throughput | PDR | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|
| LEACH | 876.1 | 1,091 | 1,345 | 27.12 | 1.076e+05 | 0.9885 | 0.05241 |
| GWO | 1,118 | 1,128 | 1,143 | 27.9 | 1.126e+05 | 0.9977 | 46.01 |
| ABC | 1,117 | 1,128 | 1,139 | 27.9 | 1.126e+05 | 0.9982 | 83.01 |
| Hybrid GWO-ABC | 1,117 | 1,126 | 1,139 | 27.87 | 1.124e+05 | 0.9975 | 107.4 |

- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+27.49%), HND (+3.24%), Residual Energy (+2.78%), Energy Consumption (+3.30%), Throughput (+4.48%), PDR (+0.91%, < 1%: practically negligible), Avg. Cluster Distance (+16.41%), Avg. CH-BS Distance (+4.34%), Final Fitness (+82.21%); significantly worse: LND (-15.31%), Runtime (-204846.34%); no significant difference: none.
- **Hybrid GWO-ABC vs GWO** — significantly better: Final Fitness (+1.75%); significantly worse: HND (-0.11%, < 1%: practically negligible), Residual Energy (-0.09%, < 1%: practically negligible), Energy Consumption (-0.11%, < 1%: practically negligible), Avg. Cluster Distance (-0.85%, < 1%: practically negligible), Avg. CH-BS Distance (-0.58%, < 1%: practically negligible), Runtime (-133.48%); no significant difference: FND, LND, Throughput, PDR.
- **Hybrid GWO-ABC vs ABC** — significantly better: Final Fitness (+0.87%, < 1%: practically negligible); significantly worse: HND (-0.12%, < 1%: practically negligible), Residual Energy (-0.11%, < 1%: practically negligible), Energy Consumption (-0.13%, < 1%: practically negligible), Throughput (-0.18%, < 1%: practically negligible), Avg. Cluster Distance (-1.04%), Avg. CH-BS Distance (-0.25%, < 1%: practically negligible), Runtime (-29.41%); no significant difference: FND, LND, PDR.

## S5_100nodes_BS_outside

_10 runs._ [report](S5_100nodes_BS_outside/report.md)

| Algorithm | FND | HND | LND | Residual Energy | Throughput | PDR | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|
| LEACH | 703 | 894.9 | 1,218 | 22.51 | 9.038e+04 | 0.9896 | 0.04921 |
| GWO | 962.9 | 978.9 | 990.6 | 24.4 | 9.752e+04 | 0.9966 | 42.62 |
| ABC | 961.5 | 978.5 | 989.9 | 24.4 | 9.753e+04 | 0.9972 | 76.74 |
| Hybrid GWO-ABC | 963.3 | 977.5 | 989.3 | 24.38 | 9.745e+04 | 0.9969 | 100.6 |

- **Hybrid GWO-ABC vs LEACH** — significantly better: FND (+37.03%), HND (+9.23%), Residual Energy (+8.35%), Energy Consumption (+6.83%), Throughput (+7.83%), PDR (+0.74%, < 1%: practically negligible), Avg. Cluster Distance (+13.08%), Avg. CH-BS Distance (+5.75%), Final Fitness (+81.87%); significantly worse: LND (-18.75%), Runtime (-204338.71%); no significant difference: none.
- **Hybrid GWO-ABC vs GWO** — significantly better: Avg. Cluster Distance (+0.44%, < 1%: practically negligible), Final Fitness (+2.71%); significantly worse: HND (-0.14%, < 1%: practically negligible), Residual Energy (-0.06%, < 1%: practically negligible), Energy Consumption (-0.06%, < 1%: practically negligible), Avg. CH-BS Distance (-0.29%, < 1%: practically negligible), Runtime (-136.09%); no significant difference: FND, LND, Throughput, PDR.
- **Hybrid GWO-ABC vs ABC** — significantly better: Final Fitness (+1.11%); significantly worse: HND (-0.10%, < 1%: practically negligible), Runtime (-31.11%); no significant difference: FND, LND, Residual Energy, Energy Consumption, Throughput, PDR, Avg. Cluster Distance, Avg. CH-BS Distance.
