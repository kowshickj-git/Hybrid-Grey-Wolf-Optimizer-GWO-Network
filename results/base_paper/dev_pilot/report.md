# Development pilot — tuning the base paper's unspecified settings

Seeds 9000..9004 (development only; the final comparison uses different, held-out seeds). The base paper does not give the fitness weight *a* of Eq. 12 or the units of the distance d in Eq. 13, so DEAI-PSO was run with every combination below and the setting with the best mean rank of node-rounds (area under the alive-nodes curve) over the three scenarios is used in the final comparison. The proposed Hybrid GWO-ABC was **not** tuned here; it keeps the default settings used in all other experiments.

**Chosen DEAI-PSO setting:** a=0.8, d=metres

| DEAI-PSO setting | mean rank (1 = best) |
|---|---:|
| a=0.8, d=metres | 1.00 |
| a=0.8, d=normalised | 2.00 |
| a=0.5, d=normalised | 3.33 |
| a=0.5, d=metres | 3.67 |
| a=0.2, d=normalised | 5.00 |
| a=0.2, d=metres | 6.00 |

## BP1_100nodes

| Algorithm (setting) | fnd | hnd | lnd | node_rounds | throughput_packets | pdr |
|---|---:|---:|---:|---:|---:|---:|
| DEAI-PSO (a=0.2, d=metres) | 619.2 | 636.4 | 649 | 6.353e+04 | 6.328e+04 | 0.9944 |
| DEAI-PSO (a=0.2, d=normalised) | 616.6 | 637.2 | 652.4 | 6.361e+04 | 6.328e+04 | 0.9932 |
| DEAI-PSO (a=0.5, d=metres) | 625.4 | 644.2 | 655 | 6.425e+04 | 6.395e+04 | 0.9937 |
| DEAI-PSO (a=0.5, d=normalised) | 625.2 | 644 | 657.8 | 6.429e+04 | 6.398e+04 | 0.9935 |
| DEAI-PSO (a=0.8, d=metres) | 634.6 | 656.4 | 662.4 | 6.55e+04 | 6.509e+04 | 0.9922 |
| DEAI-PSO (a=0.8, d=normalised) | 633.8 | 656.4 | 663 | 6.543e+04 | 6.499e+04 | 0.9918 |
| Hybrid GWO-ABC (default) | 621.6 | 662 | 677.6 | 6.605e+04 | 6.602e+04 | 0.998 |
| LEACH (default) | 372.8 | 610.8 | 913.8 | 6.142e+04 | 6.095e+04 | 0.9909 |

## BP2_160nodes

| Algorithm (setting) | fnd | hnd | lnd | node_rounds | throughput_packets | pdr |
|---|---:|---:|---:|---:|---:|---:|
| DEAI-PSO (a=0.2, d=metres) | 625.4 | 646.8 | 669.8 | 1.035e+05 | 1.031e+05 | 0.9943 |
| DEAI-PSO (a=0.2, d=normalised) | 626.2 | 647 | 671.2 | 1.035e+05 | 1.031e+05 | 0.9947 |
| DEAI-PSO (a=0.5, d=metres) | 632.6 | 652.4 | 675.8 | 1.043e+05 | 1.038e+05 | 0.9934 |
| DEAI-PSO (a=0.5, d=normalised) | 631 | 652.6 | 680 | 1.044e+05 | 1.039e+05 | 0.9938 |
| DEAI-PSO (a=0.8, d=metres) | 643.4 | 663 | 694 | 1.059e+05 | 1.05e+05 | 0.9901 |
| DEAI-PSO (a=0.8, d=normalised) | 640.4 | 662.6 | 699.8 | 1.058e+05 | 1.05e+05 | 0.9911 |
| Hybrid GWO-ABC (default) | 641.6 | 672.4 | 691 | 1.075e+05 | 1.074e+05 | 0.9979 |
| LEACH (default) | 364.8 | 589.4 | 908.4 | 9.379e+04 | 9.304e+04 | 0.9903 |

## BP3_200nodes

| Algorithm (setting) | fnd | hnd | lnd | node_rounds | throughput_packets | pdr |
|---|---:|---:|---:|---:|---:|---:|
| DEAI-PSO (a=0.2, d=metres) | 507.8 | 714.4 | 1,498 | 1.531e+05 | 1.529e+05 | 0.9973 |
| DEAI-PSO (a=0.2, d=normalised) | 507.8 | 715.2 | 1,498 | 1.532e+05 | 1.53e+05 | 0.9975 |
| DEAI-PSO (a=0.5, d=metres) | 508.4 | 720 | 1,498 | 1.541e+05 | 1.539e+05 | 0.9969 |
| DEAI-PSO (a=0.5, d=normalised) | 508.2 | 720.2 | 1,498 | 1.54e+05 | 1.537e+05 | 0.9968 |
| DEAI-PSO (a=0.8, d=metres) | 507 | 723.8 | 1,498 | 1.546e+05 | 1.543e+05 | 0.997 |
| DEAI-PSO (a=0.8, d=normalised) | 507.4 | 722.6 | 1,498 | 1.545e+05 | 1.542e+05 | 0.9971 |
| Hybrid GWO-ABC (default) | 487.4 | 727.8 | 1,498 | 1.548e+05 | 1.548e+05 | 0.9986 |
| LEACH (default) | 298.4 | 610.6 | 926.6 | 1.174e+05 | 1.165e+05 | 0.9905 |

## Development finding: which objective should the proposed optimiser use?

Improvement (%) over the tuned DEAI-PSO (a=0.8, d=metres) on the development seeds. Both rows use the proposed Hybrid GWO-ABC optimiser; they differ only in the objective it minimises.

| scenario | proposed variant | fnd % | hnd % | lnd % | node_rounds % | throughput_packets % | pdr % |
|---|---|---:|---:|---:|---:|---:|---:|
| BP1_100nodes | Hybrid GWO-ABC (Eq. 12) | -0.44 | +7.25 | +7.61 | +6.96 | +6.85 | -0.10 |
| BP1_100nodes | Hybrid GWO-ABC (multi-objective fitness) | -2.05 | +0.85 | +2.29 | +0.84 | +1.43 | +0.58 |
| BP2_160nodes | Hybrid GWO-ABC (Eq. 12) | +0.99 | +7.60 | +4.21 | +7.27 | +7.50 | +0.23 |
| BP2_160nodes | Hybrid GWO-ABC (multi-objective fitness) | -0.28 | +1.42 | -0.43 | +1.49 | +2.29 | +0.79 |
| BP3_200nodes | Hybrid GWO-ABC (Eq. 12) | -1.14 | +3.18 | +0.00 | +2.16 | +2.19 | +0.03 |
| BP3_200nodes | Hybrid GWO-ABC (multi-objective fitness) | -3.87 | +0.55 | +0.00 | +0.17 | +0.33 | +0.16 |

With the base paper's own objective (Eq. 12, same weight *a* as the tuned baseline) the proposed optimiser is ahead on HND, node-rounds and throughput in every scenario, whereas the project's multi-objective fitness gives smaller and mixed gains. The reason was traced to normalisation: with the BS 100–200 m away, the multi-objective fitness divides round energy by a worst-case bound (≈ 0.9 J), so real differences in Joules (d⁴ costs) barely change the score, while Eq. 12 measures Joules directly. The final comparison therefore uses the like-for-like setting — same problem, same objective, only the optimiser replaced — as the primary comparison, and still reports the multi-objective version.
