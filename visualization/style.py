"""Shared plot style: fixed colour per algorithm (never re-assigned by rank), recessive chrome."""
from __future__ import annotations

import matplotlib as mpl
from matplotlib.figure import Figure

# Validated categorical palette, fixed slot order (light surface)
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
CRITICAL = "#d03b3b"

ALGO_COLORS = {
    "Hybrid GWO-ABC": SLOTS[0], "LEACH": SLOTS[1], "GWO": SLOTS[2], "ABC": SLOTS[3], "Random": SLOTS[4],
    # ablation variants
    "Full Hybrid GWO-ABC": SLOTS[0], "GWO only": SLOTS[2], "ABC only": SLOTS[3],
    "GWO->ABC": SLOTS[1], "ABC->GWO": SLOTS[4], "Hybrid w/o energy": SLOTS[5],
    "Hybrid w/o distance": SLOTS[6], "Hybrid w/o balance": SLOTS[7],
    # base paper (existing system) and attribution variants
    "DEAI-PSO": SLOTS[6], "DEAI-PSO + proposed fitness": SLOTS[7],
    "Hybrid GWO-ABC (Eq. 12)": SLOTS[5], "Hybrid GWO-ABC (Eq. 12, fixed K)": SLOTS[4],
    "GWO (Eq. 12)": SLOTS[2], "ABC (Eq. 12)": SLOTS[3],
}
ALGO_STYLES = {"Hybrid GWO-ABC": "-", "Full Hybrid GWO-ABC": "-", "LEACH": "--", "GWO": "-.",
               "ABC": ":", "Random": (0, (5, 1, 1, 1)), "DEAI-PSO": (0, (6, 2, 1, 2, 1, 2)),
               "DEAI-PSO + proposed fitness": (0, (2, 2)), "Hybrid GWO-ABC (Eq. 12)": "-",
               "Hybrid GWO-ABC (Eq. 12, fixed K)": (0, (8, 2)), "GWO (Eq. 12)": "-.", "ABC (Eq. 12)": ":"}


def color(name: str, i: int = 0) -> str:
    return ALGO_COLORS.get(name, SLOTS[i % len(SLOTS)])


def linestyle(name: str) -> object:
    return ALGO_STYLES.get(name, "-")


def new_figure(w: float = 7.5, h: float = 4.5, **kw) -> Figure:
    """Backend-free figure (safe headless and inside Tkinter)."""
    return Figure(figsize=(w, h), layout="constrained", **kw)


def save(fig: Figure, path) -> str:
    fig.savefig(path, dpi=130)
    return str(path)


def apply() -> None:
    mpl.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS, "axes.labelcolor": INK_2, "axes.titlecolor": INK,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.labelsize": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
        "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelsize": 9, "ytick.labelsize": 9,
        "legend.frameon": False, "legend.fontsize": 9, "lines.linewidth": 2.0,
        "font.family": ["Segoe UI", "DejaVu Sans", "sans-serif"], "figure.dpi": 110,
    })


apply()
