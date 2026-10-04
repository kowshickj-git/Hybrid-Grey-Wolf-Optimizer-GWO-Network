# Runtime benchmark

CH-selection wall-clock time per round, measured sequentially in one process (no parallel load), over the first 100 rounds of identical networks (5 seeds); the algorithm order is rotated per seed. This is the authoritative runtime comparison: scenario runtimes were measured with 11 simulations running in parallel. The median over seeds is the headline value because it is robust to transient interference from other software; mean ± std is shown for completeness. Raw data: `runtime_raw.csv`.

| Algorithm | 100 nodes (median ms/round) | 200 nodes (median ms/round) | 300 nodes (median ms/round) |
|---|---:|---:|---:|
| LEACH | 0.01 | 0.01 | 0.01 |
| GWO | 11.94 | 19.85 | 33.38 |
| ABC | 21.53 | 28.36 | 38.03 |
| Hybrid GWO-ABC | 27.78 | 35.86 | 45.79 |

| Algorithm | 100 nodes (mean ± std) | 200 nodes (mean ± std) | 300 nodes (mean ± std) |
|---|---:|---:|---:|
| LEACH | 0.01 ± 0.00 | 0.01 ± 0.00 | 0.02 ± 0.02 |
| GWO | 11.89 ± 0.22 | 19.89 ± 0.15 | 43.33 ± 24.23 |
| ABC | 21.50 ± 0.31 | 28.29 ± 0.22 | 60.90 ± 49.30 |
| Hybrid GWO-ABC | 27.85 ± 0.19 | 35.76 ± 0.41 | 48.83 ± 5.89 |

| Algorithm | 100 nodes (evals/round) | 200 nodes (evals/round) | 300 nodes (evals/round) |
|---|---:|---:|---:|
| LEACH | 0.0 | 0.0 | 0.0 |
| GWO | 620.0 | 620.0 | 620.0 |
| ABC | 622.2 | 616.8 | 614.7 |
| Hybrid GWO-ABC | 624.9 | 619.7 | 617.5 |

![runtime](runtime_benchmark.png)

**Observed:** 100 nodes: Hybrid 27.8 ms vs GWO 11.9 ms per round (median ratio ×2.33; Hybrid slower on 5/5 seeds, Wilcoxon p = 0.0625). 100 nodes: Hybrid 27.8 ms vs ABC 21.5 ms per round (median ratio ×1.29; Hybrid slower on 5/5 seeds, Wilcoxon p = 0.0625). 200 nodes: Hybrid 35.9 ms vs GWO 19.8 ms per round (median ratio ×1.81; Hybrid slower on 5/5 seeds, Wilcoxon p = 0.0625). 200 nodes: Hybrid 35.9 ms vs ABC 28.4 ms per round (median ratio ×1.26; Hybrid slower on 5/5 seeds, Wilcoxon p = 0.0625). 300 nodes: Hybrid 45.8 ms vs GWO 33.4 ms per round (median ratio ×1.37; Hybrid slower on 4/5 seeds, Wilcoxon p = 0.625). 300 nodes: Hybrid 45.8 ms vs ABC 38.0 ms per round (median ratio ×1.20; Hybrid slower on 4/5 seeds, Wilcoxon p = 0.625).

With 5 paired seeds the smallest possible two-sided Wilcoxon p-value is 0.0625, so these timing differences cannot reach p < 0.05 even when the hybrid is slower on every seed; the per-seed counts above show how consistent the direction is.

All three optimisers spend about the same number of fitness evaluations per round; the hybrid's extra time comes from running two populations and more operators (transfer, duplicate checks) per iteration in Python.

**Data-quality note:** timings above 1.5× the median of the same algorithm and size (most likely disturbed by other activity on the computer; they are visible as outlying dots in the figure): GWO, 300 nodes, seed 45: 86.6 ms; ABC, 300 nodes, seed 45: 149.0 ms. They are kept in the raw data and in the mean ± std table; the medians are barely affected.
