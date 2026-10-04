"""Optimisation convergence (best-so-far fitness vs iteration)."""
from __future__ import annotations

import numpy as np

from visualization import style

CURVE_COLORS = {"gwo": style.color("GWO"), "abc": style.color("ABC"), "hybrid": style.color("Hybrid GWO-ABC"),
                "deai_pso": style.color("DEAI-PSO")}
CURVE_LABELS = {"gwo": "GWO pack (alpha)", "abc": "ABC colony (best source)", "hybrid": "Hybrid elite",
                "deai_pso": "DEAI-PSO global best"}


def _band(ax, data, color, label, ls="-"):
    data = np.asarray(data, float)
    x = np.arange(data.shape[1])
    mean = data.mean(0)
    ax.plot(x, mean, color=color, ls=ls, label=label)
    if data.shape[0] > 1:
        sd = data.std(0)
        ax.fill_between(x, mean - sd, mean + sd, color=color, alpha=0.12, lw=0)


def plot_algorithm_convergence(curves: dict, path=None, title: str = "Convergence", n_runs: int | None = None):
    """``curves``: algorithm -> array (runs x iterations+1) of best-so-far fitness."""
    fig = style.new_figure(7.5, 4.5)
    ax = fig.add_subplot()
    for alg, data in curves.items():
        _band(ax, data, style.color(alg), alg, style.linestyle(alg))
    ax.set_xlabel("Iteration (0 = initial population)")
    ax.set_ylabel("Best-so-far fitness (lower = better)")
    sub = f" — mean ± std over {n_runs} runs" if n_runs else ""
    ax.set_title(title + sub, loc="left")
    ax.legend()
    return style.save(fig, path) if path else fig


def plot_internal_convergence(curves: dict, path=None, title: str = "Hybrid GWO-ABC internal convergence",
                              n_runs: int | None = None):
    """``curves``: 'gwo'/'abc'/'hybrid' -> array (runs x iterations+1) from the hybrid optimiser."""
    fig = style.new_figure(7.5, 4.5)
    ax = fig.add_subplot()
    styles = {"gwo": "-.", "abc": ":", "hybrid": "-"}
    for key in ("hybrid", "abc", "gwo"):      # elite first so the coinciding sub-curves stay visible on top
        if key in curves:
            _band(ax, curves[key], CURVE_COLORS[key], CURVE_LABELS[key], styles[key])
    ax.set_xlabel("Iteration (0 = initial population)")
    ax.set_ylabel("Best-so-far fitness (lower = better)")
    sub = f" — mean ± std over {n_runs} runs" if n_runs else ""
    ax.set_title(title + sub, loc="left")
    ax.legend()
    return style.save(fig, path) if path else fig


def plot_single_curves(curves: dict, path=None, title: str = "Convergence (single round)"):
    """``curves``: name -> list for one optimisation (as stored in SimulationResult.curves[round])."""
    fig = style.new_figure(7.0, 4.2)
    ax = fig.add_subplot()
    for key, values in curves.items():
        ax.plot(np.arange(len(values)), values, color=CURVE_COLORS.get(key, style.SLOTS[4]),
                label=CURVE_LABELS.get(key, key))
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Best-so-far fitness")
    ax.set_title(title, loc="left")
    ax.legend()
    return style.save(fig, path) if path else fig
