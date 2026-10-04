"""Descriptive statistics, paired significance tests and effect sizes over independent runs.

Runs are *paired*: run r of every algorithm uses the same deployment seed, so
the same network. Differences are therefore tested with the Wilcoxon
signed-rank test (non-parametric, paired). Effect size is Cliff's delta.
p-values are Holm-corrected over the baselines compared for one metric.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from evaluation.metrics import METRICS

ALPHA = 0.05


def describe(runs: pd.DataFrame, metrics, group: str = "algorithm") -> pd.DataFrame:
    """Long table: one row per (algorithm, metric) with n, mean, std, min, median, max."""
    rows = []
    for alg, df in runs.groupby(group, sort=False):
        for m in metrics:
            v = df[m].astype(float).dropna()
            rows.append({group: alg, "metric": m, "n": len(v), "mean": v.mean(),
                         "std": v.std(ddof=1) if len(v) > 1 else 0.0,
                         "min": v.min(), "median": v.median(), "max": v.max()})
    return pd.DataFrame(rows)


def improvement(proposed: float, baseline: float, higher_is_better: bool) -> float:
    """Improvement (%) of ``proposed`` over ``baseline`` (positive = proposed is better).

    higher-is-better: (P - B) / B * 100;  lower-is-better: (B - P) / B * 100.
    """
    if baseline == 0 or np.isnan(baseline) or np.isnan(proposed):
        return np.nan
    diff = proposed - baseline if higher_is_better else baseline - proposed
    return 100.0 * diff / abs(baseline)


def cliffs_delta(a, b) -> float:
    """P(a > b) - P(a < b) over all pairs (-1..1)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) == 0 or len(b) == 0:
        return np.nan
    diff = a[:, None] - b[None, :]
    return float((np.sign(diff)).mean())


def effect_magnitude(delta: float) -> str:
    d = abs(delta)
    if np.isnan(d):
        return "n/a"
    return "negligible" if d < 0.147 else "small" if d < 0.33 else "medium" if d < 0.474 else "large"


def paired_test(a, b) -> float:
    """Two-sided Wilcoxon signed-rank p-value for paired samples (1.0 if identical)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~(np.isnan(a) | np.isnan(b))
    a, b = a[ok], b[ok]
    if len(a) < 2 or np.allclose(a, b):
        return 1.0
    try:
        return float(stats.wilcoxon(a, b, zero_method="zsplit").pvalue)
    except ValueError:
        return 1.0


def holm(pvalues) -> np.ndarray:
    p = np.asarray(pvalues, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(p) - rank) * p[i]))
        adj[i] = running
    return adj


def compare_to_baselines(runs: pd.DataFrame, proposed: str, baselines, metrics,
                         group: str = "algorithm", pair_on: str = "run") -> pd.DataFrame:
    """Per metric and baseline: means, improvement %, p-value (raw and Holm), Cliff's delta, verdict."""
    rows = []
    prop = runs[runs[group] == proposed].set_index(pair_on)
    for m in metrics:
        info = METRICS[m]
        block = []
        for base in baselines:
            bdf = runs[runs[group] == base].set_index(pair_on)
            common = prop.index.intersection(bdf.index)
            pa, ba = prop.loc[common, m].astype(float), bdf.loc[common, m].astype(float)
            pm, bm = pa.mean(), ba.mean()
            # orient Cliff's delta so that positive = proposed better
            delta = cliffs_delta(pa, ba) * (1 if info.higher_is_better else -1)
            block.append({"metric": m, "label": info.label, "baseline": base,
                          "higher_is_better": info.higher_is_better, "proposed_mean": pm,
                          "baseline_mean": bm, "improvement_pct": improvement(pm, bm, info.higher_is_better),
                          "p_value": paired_test(pa, ba), "cliffs_delta": delta,
                          "effect": effect_magnitude(delta), "n_pairs": len(common)})
        for row, p_adj in zip(block, holm([r["p_value"] for r in block])):
            row["p_holm"] = p_adj
            row["significant"] = bool(p_adj < ALPHA)
            if not row["significant"] or np.isnan(row["improvement_pct"]):
                row["verdict"] = "no significant difference"
            elif row["improvement_pct"] > 0:
                row["verdict"] = "proposed better"
            elif row["improvement_pct"] < 0:
                row["verdict"] = "proposed worse"
            else:
                row["verdict"] = "no significant difference"
            rows.append(row)
    return pd.DataFrame(rows)
