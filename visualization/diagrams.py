"""Explanatory figures for the beginner documentation (written to docs/figures/).

Run with ``python main.py diagrams``. Concept diagrams (architecture, flowcharts, algorithm schematics)
are drawn by hand. Every curve or number in them that describes the model is computed with the
project's own code (EnergyModel, FitnessContext, LEACH.threshold, control_parameter, sigmoid_transfer)
or read from saved results (lifetime figure), so the pictures cannot drift away from the implementation.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

from config import PROJECT_ROOT, RESULTS_DIR, SimulationConfig
from models.energy_model import EnergyModel
from models.network import Network
from visualization import style

FIG_DIR = PROJECT_ROOT / "docs" / "figures"
NODE, CH, BS, DEAD, LINK = style.SLOTS[0], style.SLOTS[1], style.INK, style.CRITICAL, "#b7b5ac"
GWO_C, ABC_C = style.SLOTS[2], style.SLOTS[3]
TINT = {"setup": "#efeee8", "loop": "#e8f1fb", "post": "#e4f4ec", "gwo": "#e2f4ec", "abc": "#fdf2dc",
        "hybrid": "#e6effb", "warn": "#fdebe4", "plain": "#ffffff"}

# worked fitness example (also used in docs/03_MATHEMATICS.md and tests/test_docs_examples.py)
EXAMPLE_POSITIONS = np.array([[10, 10], [20, 10], [10, 20], [90, 90], [80, 90], [90, 80]], dtype=float)
EXAMPLE_GOOD, EXAMPLE_BAD = [1, 4], [0, 1]


# ------------------------------------------------------------------------------------------ helpers
def _canvas(w, h, xlim=(0, 100), ylim=(0, 100)):
    fig = style.new_figure(w, h)
    ax = fig.add_subplot()
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def _box(ax, x, y, w, h, text, fc=TINT["plain"], ec=style.AXIS, fs=9.0, weight="normal", lw=1.2, color=None):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=fc, ec=ec, lw=lw, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color or style.INK, fontweight=weight,
            zorder=3, linespacing=1.35)


def _arrow(ax, p, q, color=style.INK_2, lw=1.4, rad=0.0, ls="-", head=12):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=head, color=color, lw=lw, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=1))


def _path(ax, pts, color=style.INK_2, lw=1.4, label=None, label_at=0, label_offset=(1.0, 1.0)):
    """Poly-line with an arrow head on the last segment."""
    pts = np.asarray(pts, dtype=float)
    ax.plot(pts[:-1, 0].tolist() + [pts[-1, 0]], pts[:-1, 1].tolist() + [pts[-1, 1]], color=color, lw=lw, zorder=1)
    _arrow(ax, pts[-2], pts[-1], color=color, lw=lw)
    if label:
        x, y = pts[label_at]
        ax.text(x + label_offset[0], y + label_offset[1], label, fontsize=9, color=color, fontweight="bold")


def _save(fig, name: str, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    path = out / name
    fig.savefig(path, dpi=130)
    return path


# ------------------------------------------------------------------------------------------ figures
def fig_architecture(out: Path) -> Path:
    """Sensor nodes -> cluster heads -> base station (schematic)."""
    fig, ax = _canvas(10.5, 6.0, (0, 178), (0, 104))
    ax.add_patch(Rectangle((4, 8), 104, 90, fill=False, ec=style.AXIS, lw=1.2, ls="--"))
    ax.text(6, 96, "Sensor field (default 100 m × 100 m)", fontsize=9, color=style.INK_2, va="top")
    bs = np.array([150.0, 52.0])
    rng = np.random.default_rng(7)
    clusters = [(np.array([30.0, 70.0]), -0.15), (np.array([33.0, 30.0]), 0.15), (np.array([80.0, 55.0]), 0.0)]
    pts_all = []
    for c, rad in clusters:
        ang = np.linspace(0, 2 * np.pi, 7)[:-1] + rng.uniform(-0.3, 0.3, 6)
        r = rng.uniform(9, 15, 6)
        pts = c + np.c_[np.cos(ang) * r, np.sin(ang) * r * 0.9]
        ax.add_patch(Ellipse(tuple(c), 42, 36, fc=NODE, alpha=0.07, ec=NODE, lw=0.6, ls=":"))
        for p in pts:
            ax.plot([p[0], c[0]], [p[1], c[1]], color=LINK, lw=1.1, zorder=1)
        ax.scatter(pts[:, 0], pts[:, 1], s=60, color=NODE, edgecolors=style.SURFACE, lw=0.8, zorder=3)
        ax.scatter([c[0]], [c[1]], s=210, marker="^", color=CH, edgecolors=style.SURFACE, lw=1.0, zorder=4)
        _arrow(ax, (c[0] + 3.5, c[1]), (bs[0] - 5, bs[1] + np.sign(c[1] - bs[1]) * 1.5), color=CH, lw=1.8, rad=rad)
        pts_all.append(pts)
    ax.scatter([bs[0]], [bs[1]], s=480, marker="s", color=BS, zorder=5)

    note = dict(fontsize=9, color=style.INK, va="center", ha="left", linespacing=1.35)
    ax.text(118, 86, "Cluster head (CH)\nreceives its members' packets,\naggregates them and sends\n"
                     "ONE packet to the base station", **note)
    _arrow(ax, (117, 84), (83.5, 57), color=style.INK_2, lw=0.9, rad=0.15, head=9)
    ax.text(118, 18, "Member (sensor) node\nsenses the environment and\nsends its packet to the\n"
                     "NEAREST cluster head (short hop)", **note)
    m = pts_all[1][np.argmax(pts_all[1][:, 0])]
    _arrow(ax, (117, 20), (m[0] + 1.5, m[1] - 0.5), color=style.INK_2, lw=0.9, rad=-0.15, head=9)
    ax.text(bs[0] - 4, bs[1] - 10.5, "Base station (BS)\ncollects all data;\nmains-powered", fontsize=9,
            color=style.INK, ha="left", va="top", linespacing=1.35)
    ax.text(30, 92, "a cluster = 1 CH + its members", fontsize=8.5, color=NODE, ha="center")
    handles = [Line2D([], [], marker="o", ls="", color=NODE, label="Sensor node (member)"),
               Line2D([], [], marker="^", ls="", color=CH, markersize=9, label="Cluster head"),
               Line2D([], [], marker="s", ls="", color=BS, markersize=9, label="Base station"),
               Line2D([], [], color=LINK, lw=1.4, label="member → CH (short, cheap)"),
               Line2D([], [], color=CH, lw=1.8, label="CH → BS (long, expensive)")]
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.0, -0.06), ncol=5, fontsize=8.5,
              handletextpad=0.4, columnspacing=1.2)
    ax.set_title("WSN architecture used in this project: sensor nodes → cluster heads → base station",
                 loc="left")
    return _save(fig, "fig01_wsn_architecture.png", out)


def fig_round_flowchart(out: Path) -> Path:
    """What the simulator does: set-up, the per-round loop and post-processing."""
    fig, ax = _canvas(10.5, 11.0, (0, 100), (0, 100))
    L, R, W, H = 28.0, 76.0, 42.0, 5.6
    ax.text(L - W / 2, 99.2, "SET-UP (once)", fontsize=10, fontweight="bold", color=style.INK_2, va="top")
    _box(ax, L, 94, W, 4.4, "START:  python main.py  (or a command such as  compare)", fc="#ffffff",
         ec=style.INK, weight="bold")
    _box(ax, L, 87, W, H, "Read the parameters\n(config.py defaults, optional --set changes)", fc=TINT["setup"])
    _box(ax, L, 79.5, W, H, "Create N sensor nodes at random (x, y)\n(same seed → same network every time)",
         fc=TINT["setup"])
    _box(ax, L, 72, W, H, "Give every node its battery: E0 = 0.5 J\nall nodes ALIVE, base station placed",
         fc=TINT["setup"])
    for y0, y1 in ((91.8, 89.8), (84.2, 82.3), (76.7, 74.8), (69.2, 64.6)):
        _arrow(ax, (L, y0), (L, y1))

    ax.add_patch(FancyBboxPatch((3, 4), 50.5, 64, boxstyle="round,pad=0,rounding_size=2", fc=TINT["loop"],
                                ec=NODE, lw=1.0, ls="--", zorder=0))
    ax.text(30.5, 67.4, "REPEATED EVERY ROUND\nr = 1, 2, 3, …", fontsize=9.5, fontweight="bold", color=NODE,
            va="top")
    steps = ["1  Select cluster heads\n(Random / LEACH / GWO / ABC / Hybrid GWO-ABC)",
             "2  Form clusters: every alive node\njoins its nearest cluster head",
             "3  Transmit data:  member → CH → base station",
             "4  Consume energy (radio model): subtract\nsend / receive / aggregation costs",
             "5  Check dead nodes: energy = 0 J → DEAD\n(a dead node is never used again)",
             "6  Record the round: alive, dead, energy,\npackets, number of CHs, fitness"]
    ys = [61.8, 54.2, 46.6, 39.0, 31.4, 23.8]
    for y, s in zip(ys, steps):
        _box(ax, L, y, W, H, s)
    for y0, y1 in zip(ys[:-1], ys[1:]):
        _arrow(ax, (L, y0 - H / 2), (L, y1 + H / 2))
    dy = 12.0
    ax.add_patch(Polygon([[L - 17, dy], [L, dy + 5], [L + 17, dy], [L, dy - 5]], closed=True, fc=TINT["warn"],
                         ec=CH, lw=1.2, zorder=2))
    ax.text(L, dy, "All nodes dead, or\nlast round reached?", ha="center", va="center", fontsize=9, zorder=3)
    _arrow(ax, (L, ys[-1] - H / 2), (L, dy + 5))
    _path(ax, [(L - 17, dy), (4.5, dy), (4.5, ys[0]), (L - W / 2, ys[0])], color=NODE, label="NO → next round",
          label_at=1, label_offset=(0.8, 3.5))
    ax.text(R - W / 2, 70.5, "AFTER THE LAST ROUND", fontsize=10, fontweight="bold", color=style.SLOTS[5], va="top")
    post = ["Calculate the run's metrics: FND, HND, LND,\nresidual energy, throughput, PDR, …",
            "Repeat for every algorithm on the SAME\nnetworks (paired runs, 20 seeds in S1)",
            "Compare the algorithms: mean ± std,\nWilcoxon test, Holm correction, Cliff's δ",
            "Save CSV files: runs_raw.csv,\nhistory_raw.csv.gz, statistics.csv, …",
            "Draw the graphs (PNG) and write report.md\n→ final comparison table"]
    py = [61.8, 51.0, 40.2, 29.4, 18.6]
    for y, s in zip(py, post):
        _box(ax, R, y, W, 6.4, s, fc=TINT["post"])
    for y0, y1 in zip(py[:-1], py[1:]):
        _arrow(ax, (R, y0 - 3.2), (R, y1 + 3.2))
    _path(ax, [(L + 17, dy), (52, dy), (52, py[0]), (R - W / 2, py[0])], color=style.SLOTS[5], label="YES",
          label_at=1, label_offset=(-3.5, -4.0))
    ax.set_title("What the program does: set-up → round loop → results", loc="left")
    return _save(fig, "fig02_simulation_flowchart.png", out)


def fig_energy_model(out: Path, cfg: SimulationConfig) -> Path:
    em, k = EnergyModel(cfg.energy), cfg.packet_bits
    fig = style.new_figure(11.8, 4.6)
    a1, a2 = fig.subplots(1, 2, width_ratios=[1.3, 1])
    d = np.linspace(0, 200, 801)
    a1.axvspan(0, em.d0, color=NODE, alpha=0.06, lw=0)
    a1.axvspan(em.d0, 200, color=CH, alpha=0.07, lw=0)
    a1.plot(d, em.tx_energy(k, d) * 1e3, color=NODE, label="send (TX) 4000 bits over d metres")
    a1.axhline(em.rx_energy(k) * 1e3, color=GWO_C, ls=":", lw=1.8, label="receive (RX) 4000 bits")
    a1.axvline(em.d0, color=style.MUTED, ls="--", lw=1)
    a1.text(em.d0 + 2, 7.6, f"d0 = {em.d0:.1f} m", fontsize=9, color=style.INK_2)
    a1.text(4, 5.2, "free space:\ncost ∝ d²", fontsize=9, color=NODE)
    a1.text(122, 5.2, "multipath:\ncost ∝ d⁴", fontsize=9, color=CH)
    for dd, label, dx, dy in ((20, "member → CH (20 m)", 4, 1.0), (40, "CH → BS at centre (40 m)", -10, 3.0),
                              (150, "BS outside field (150 m)", -64, 1.6)):
        e = em.tx_energy(k, dd) * 1e3
        a1.scatter([dd], [e], color=style.INK, s=22, zorder=4)
        a1.annotate(f"{label}: {e:.3f} mJ", (dd, e), xytext=(dd + dx, e + dy), fontsize=8.5, color=style.INK,
                    arrowprops=dict(arrowstyle="-", color=style.MUTED, lw=0.8))
    a1.set_xlim(0, 200)
    a1.set_ylim(0, 9)
    a1.set_xlabel("Distance d (m)")
    a1.set_ylabel("Energy per 4000-bit packet (mJ)")
    a1.set_title("Sending gets very expensive beyond d0", loc="left")
    a1.legend(loc="upper left")

    rx_da = (em.rx_energy(k) + em.aggregation_energy(k))
    parts = {"receive 19 packets": 19 * em.rx_energy(k), "aggregate 20 packets": 20 * em.aggregation_energy(k),
             "send 1 packet to BS (40 m)": em.tx_energy(k, 40)}
    member = em.tx_energy(k, 20)
    left = 0.0
    for i, (lab, v) in enumerate(parts.items()):          # y = 0: cluster head, y = 1: member
        a2.barh([0], [v * 1e3], left=left, color=[CH, ABC_C, style.SLOTS[6]][i], height=0.55, label=lab,
                edgecolor=style.SURFACE, linewidth=2)
        left += v * 1e3
    a2.barh([1], [member * 1e3], color=NODE, height=0.55, label="send 1 packet to CH (20 m)")
    total_ch = 19 * rx_da + em.aggregation_energy(k) + em.tx_energy(k, 40)
    a2.text(total_ch * 1e3 + 0.08, 0, f"{total_ch * 1e3:.3f} mJ", va="center", fontsize=9)
    a2.text(member * 1e3 + 0.08, 1, f"{member * 1e3:.3f} mJ", va="center", fontsize=9)
    a2.set_yticks([0, 1], ["Cluster head\n(19 members)", "Member node"])
    a2.set_xlim(0, 5.6)
    a2.set_xlabel("Energy spent in one round (mJ)")
    a2.set_title(f"Being a CH costs ≈ {total_ch / member:.0f}× more", loc="left")
    a2.grid(axis="y", visible=False)
    a2.legend(loc="upper left", bbox_to_anchor=(0.0, -0.22), ncol=2, fontsize=8)
    return _save(fig, "fig03_energy_model.png", out)


def example_context():
    """The 6-node worked example of the fitness function (BS at the centre, every node 0.5 J, K_opt = 2)."""
    from algorithms.fitness import FitnessContext
    cfg = SimulationConfig(n_nodes=6, ch_percentage=0.3)
    net = Network(EXAMPLE_POSITIONS, 0.5, (50.0, 50.0), (100.0, 100.0))
    return net, cfg, FitnessContext(net, cfg)


def fig_fitness_example(out: Path) -> Path:
    net, cfg, ctx = example_context()
    fig = style.new_figure(12.5, 4.6)
    axes = fig.subplots(1, 3, width_ratios=[1, 1, 1.35])
    names = ["energy", "intra_distance", "ch_bs_distance", "balance", "ch_count"]
    labels = ["w1 · energy", "w2 · member→CH distance", "w3 · CH→BS distance", "w4 · imbalance",
              "w5 · CH-count penalty"]
    results = {}
    for ax, (title, chs) in zip(axes[:2], (("Choice A: CHs = nodes 1 and 4", EXAMPLE_GOOD),
                                          ("Choice B: CHs = nodes 0 and 1", EXAMPLE_BAD))):
        x = ctx.from_node_ids(chs)
        comp = ctx.components(x)
        results[title[:8]] = comp
        pos = net.positions
        members = [i for i in range(net.n) if i not in chs]
        for i in members:
            j = min(chs, key=lambda c: net.distances[i, c])
            ax.plot(*zip(pos[i], pos[j]), color=LINK, lw=1.2, zorder=1)
        ax.scatter(pos[members, 0], pos[members, 1], s=70, color=NODE, zorder=3)
        ax.scatter(pos[chs, 0], pos[chs, 1], s=190, marker="^", color=CH, zorder=4)
        ax.scatter([50], [50], s=200, marker="s", color=BS, zorder=4)
        for i, (px, py) in enumerate(pos):
            ax.annotate(str(i), (px, py), xytext=(5, 4), textcoords="offset points", fontsize=9, color=style.INK_2)
        ax.text(55, 41, "BS", fontsize=9)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_aspect("equal")
        ax.set_title(f"{title}\nfitness F = {comp['fitness']:.4f}", loc="left", fontsize=10.5)
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
    ax = axes[2]
    w = ctx.weights
    y = np.arange(2)
    left = np.zeros(2)
    for i, (nm, lab) in enumerate(zip(names, labels)):
        vals = np.array([w[i] * results["Choice A"][nm], w[i] * results["Choice B"][nm]])
        ax.barh(y, vals, left=left, color=style.SLOTS[i], height=0.55, label=lab, edgecolor=style.SURFACE,
                linewidth=2)
        left += vals
    for yi, tot in zip(y, left):
        ax.text(tot + 0.006, yi, f"F = {tot:.4f}", va="center", fontsize=9.5, fontweight="bold")
    ax.set_yticks(y, ["Choice A", "Choice B"])
    ax.invert_yaxis()
    ax.set_xlim(0, 0.62)
    ax.set_xlabel("Weighted contribution to the fitness (lower = better)")
    ax.set_title("Same 6 nodes, two CH choices: A wins", loc="left", fontsize=10.5)
    ax.grid(axis="y", visible=False)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, -0.2), ncol=2, fontsize=8)
    return _save(fig, "fig04_fitness_example.png", out)


def fig_gwo_concept(out: Path) -> Path:
    fig = style.new_figure(12.0, 5.0)
    a1, a2 = fig.subplots(1, 2, width_ratios=[1, 1.1])
    a1.set_xlim(0, 100)
    a1.set_ylim(0, 100)
    a1.axis("off")
    layers = [("α  ALPHA", "best CH set found so far", 0.95),
              ("β  BETA", "2nd-best CH set", 0.75),
              ("δ  DELTA", "3rd-best CH set", 0.55),
              ("ω  OMEGA", "every other wolf (candidate CH set):\nfollows α, β and δ", 0.30)]
    top, h = 92.0, 19.0
    for i, (name, desc, alpha) in enumerate(layers):
        y1, y0 = top - i * h, top - (i + 1) * h
        half1, half0 = 8 + i * 10, 8 + (i + 1) * 10
        a1.add_patch(Polygon([[50 - half0, y0 + 1], [50 + half0, y0 + 1], [50 + half1, y1], [50 - half1, y1]],
                             closed=True, fc=GWO_C, alpha=alpha, ec=style.SURFACE, lw=2))
        a1.text(50, (y0 + y1) / 2 + 3.2, name, ha="center", va="center", fontsize=10, fontweight="bold",
                color="white" if alpha > 0.5 else style.INK)
        a1.text(50, (y0 + y1) / 2 - 3.6, desc, ha="center", va="center", fontsize=8.5,
                color="white" if alpha > 0.5 else style.INK, linespacing=1.2)
    a1.set_title("Wolf hierarchy = ranking of candidate solutions", loc="left")

    a2.set_xlim(0, 100)
    a2.set_ylim(0, 100)
    a2.set_aspect("equal")
    a2.axis("off")
    prey = np.array([66.0, 67.0])
    a2.scatter(*prey, s=360, marker="*", color=style.SLOTS[7], zorder=5)
    a2.text(prey[0] + 4, prey[1] + 2, "best possible CH set\n(unknown 'prey')", fontsize=8.5, color=style.SLOTS[7])
    leaders = {"α": np.array([46.0, 64.0]), "β": np.array([84.0, 50.0]), "δ": np.array([60.0, 86.0])}
    wolf = np.array([10.0, 14.0])
    sugg = {"α": np.array([40.0, 55.0]), "β": np.array([74.0, 42.0]), "δ": np.array([54.0, 76.0])}
    for key, p in leaders.items():
        a2.scatter(*p, s=170, color=GWO_C, edgecolors=style.SURFACE, zorder=4)
        a2.text(p[0] + 2.5, p[1] + 1.5, key, fontsize=12, fontweight="bold", color=GWO_C)
        a2.plot(*zip(wolf, p), color=style.MUTED, lw=0.9, ls="--", zorder=1)
        s = sugg[key]
        a2.scatter(*s, s=40, color=style.INK_2, zorder=4)
        a2.annotate("", s, p, arrowprops=dict(arrowstyle="-|>", color=style.INK_2, lw=0.8))
        a2.text(s[0] - 1, s[1] - 5.5, {"α": "X1", "β": "X2", "δ": "X3"}[key], fontsize=8.5, color=style.INK_2)
    new = np.mean(list(sugg.values()), axis=0)
    a2.scatter(*wolf, s=150, color=style.SLOTS[4], edgecolors=style.SURFACE, zorder=4)
    a2.text(wolf[0] - 2, wolf[1] - 8, "ω wolf now (X)", fontsize=9, color=style.INK)
    a2.scatter(*new, s=170, marker="D", color=NODE, edgecolors=style.SURFACE, zorder=5)
    a2.annotate("", new, wolf, arrowprops=dict(arrowstyle="-|>", color=NODE, lw=2.0, shrinkB=7))
    a2.annotate("new position = (X1 + X2 + X3) / 3", new, xytext=(52, 24), fontsize=8.5, color=NODE,
                arrowprops=dict(arrowstyle="-", color=NODE, lw=0.8))
    a2.text(2, 96, "Each leader 'suggests' a position near itself (grey dots);\n"
                   "the wolf moves to the average of the 3 suggestions.", fontsize=8.5, color=style.INK_2, va="top")
    a2.set_title("One GWO move (illustration in 2-D)", loc="left")
    return _save(fig, "fig05_gwo_concept.png", out)


def fig_gwo_parameters(out: Path, iterations: int = 30) -> Path:
    from algorithms.gwo import control_parameter, sigmoid_transfer
    fig = style.new_figure(11.8, 4.4)
    a1, a2 = fig.subplots(1, 2)
    t = np.arange(iterations + 1)
    a = np.array([control_parameter(i, iterations) for i in t])
    a1.fill_between(t, -a, a, color=GWO_C, alpha=0.15, lw=0, label="possible values of A = 2a·r1 − a")
    a1.plot(t, a, color=GWO_C, label="a (decreases 2 → 0)")
    a1.axhline(1, color=style.MUTED, ls="--", lw=1)
    a1.axhline(-1, color=style.MUTED, ls="--", lw=1)
    half = iterations / 2
    a1.axvline(half, color=style.MUTED, ls=":", lw=1)
    a1.text(1, -1.85, "|A| can exceed 1:\nwolves may jump AWAY\n= EXPLORATION", fontsize=8.5, color=style.INK)
    a1.text(half + 1, 1.25, "|A| < 1: wolves close\nIN on the leaders\n= EXPLOITATION", fontsize=8.5,
            color=style.INK)
    a1.set_xlabel("Iteration t (within one round's optimisation)")
    a1.set_ylabel("a and range of A")
    a1.set_ylim(-2.2, 2.2)
    a1.set_title("Control parameter a: explore first, exploit later", loc="left")
    a1.legend(loc="upper right", fontsize=8)

    y = np.linspace(-0.25, 1.25, 301)
    a2.plot(y, sigmoid_transfer(y), color=NODE)
    a2.axhline(0.5, color=style.MUTED, ls="--", lw=1)
    a2.axvline(0.5, color=style.MUTED, ls="--", lw=1)
    ex = 0.8667
    a2.scatter([ex], [sigmoid_transfer(np.array(ex))], color=CH, zorder=4, s=36)
    a2.annotate(f"worked example: y = {ex:.4f} → S = {float(sigmoid_transfer(np.array(ex))):.3f}",
                (ex, float(sigmoid_transfer(np.array(ex)))), xytext=(-0.22, 0.80), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=style.MUTED, lw=0.8))
    a2.text(0.52, 0.08, "y < 0.5: node is\nprobably NOT a CH", fontsize=8.5)
    a2.text(-0.22, 0.55, "y > 0.5: node is\nprobably a CH", fontsize=8.5)
    a2.set_xlabel("Continuous GWO value y for one node")
    a2.set_ylabel("Probability that the node becomes CH")
    a2.set_title("Sigmoid S(y) = 1 / (1 + e^(−10(y − 0.5)))", loc="left")
    return _save(fig, "fig06_gwo_parameters.png", out)


def fig_abc_cycle(out: Path) -> Path:
    fig, ax = _canvas(11.0, 6.4, (0, 110), (0, 64))
    _box(ax, 34, 33, 25, 10, "FOOD SOURCES\n= candidate CH sets\n(10 in ABC, 5 in the hybrid)", fc=TINT["abc"],
         ec=ABC_C, weight="bold", fs=9)
    boxes = {
        "emp": (34, 56, "1  EMPLOYED BEES (one per source)\nmake a small change to their source;\n"
                        "keep it only if the fitness is better"),
        "onl": (63, 33, "2  ONLOOKER BEES\npick sources with probability\np_i ∝ 1 / (1 + F_i): good sources\n"
                        "get more visits (exploitation)"),
        "sct": (34, 9.5, "3  SCOUT BEE\na source not improved for > limit (10)\n"
                         "tries is abandoned and replaced by a\nrandom CH set (exploration)"),
        "mem": (8.5, 33, "4  REMEMBER\nthe best source\never found"),
    }
    sizes = {"emp": (34, 9), "onl": (30, 11.5), "sct": (34, 10), "mem": (15, 9)}
    for key, (x, y, text) in boxes.items():
        _box(ax, x, y, *sizes[key], text, fc="#ffffff", ec=ABC_C, fs=8.5)
    _arrow(ax, (51, 54), (64, 39.2), color=ABC_C, rad=-0.3, lw=1.6)
    _arrow(ax, (64, 26.8), (51, 12), color=ABC_C, rad=-0.3, lw=1.6)
    _arrow(ax, (17, 10), (8.5, 28.2), color=ABC_C, rad=-0.3, lw=1.6)
    _arrow(ax, (8.5, 37.8), (17, 55), color=ABC_C, rad=-0.3, lw=1.6)
    ax.text(34, 46, "one ABC iteration = 1 → 2 → 3 → 4", ha="center", fontsize=8.5, color=style.INK_2)

    ax.text(80, 61, "How a bee changes a CH set (neighbour move)", fontsize=9.5, fontweight="bold", va="top")
    ax.text(80, 55.5, "Example with 6 nodes (1 = cluster head):", fontsize=8.5, va="top", color=style.INK_2)
    rows = [("my source x_i", [1, 0, 1, 0, 0, 0]), ("partner x_k", [0, 1, 1, 0, 0, 0]),
            ("a) share (φ ≥ 0)", [0, 1, 1, 0, 0, 0]), ("b) local move", [1, 0, 0, 1, 0, 0])]
    for r, (lab, bits) in enumerate(rows):
        yy = 49 - r * 6.5
        ax.text(80, yy, lab, fontsize=8.5, va="center")
        for c, b in enumerate(bits):
            ax.add_patch(Rectangle((93 + c * 2.6, yy - 2), 2.4, 4, fc=CH if b else "#ffffff", ec=style.AXIS, lw=0.8))
            ax.text(94.2 + c * 2.6, yy, str(b), ha="center", va="center", fontsize=8,
                    color="white" if b else style.INK_2)
    ax.text(80, 21, "a) swap one of my CHs (node 0) for one of\n    the partner's CHs (node 1): information sharing\n"
                    "b) hand a CH role (node 2) to a NEAR neighbour\n    (node 3): local search\n"
                    "c) with probability 0.1 add or remove one CH", fontsize=8.3, va="top", linespacing=1.35)
    ax.set_title("Artificial Bee Colony (ABC): improve candidate CH sets like bees exploit flower patches",
                 loc="left")
    return _save(fig, "fig07_abc_cycle.png", out)


def fig_hybrid_flow(out: Path) -> Path:
    fig, ax = _canvas(11.5, 8.4, (0, 100), (0, 100))
    ax.add_patch(FancyBboxPatch((3, 21), 39, 65, boxstyle="round,pad=0,rounding_size=2", fc=TINT["gwo"],
                                ec=GWO_C, lw=1.2, zorder=0))
    ax.add_patch(FancyBboxPatch((58, 21), 40, 65, boxstyle="round,pad=0,rounding_size=2", fc=TINT["abc"],
                                ec=ABC_C, lw=1.2, zorder=0))
    ax.text(22, 83, "GWO WOLF PACK (10 wolves)", ha="center", fontsize=10, fontweight="bold", color=GWO_C)
    ax.text(78, 83, "ABC BEE COLONY (5 food sources)", ha="center", fontsize=10, fontweight="bold", color=ABC_C)
    _box(ax, 50, 95, 60, 5, "Start of a round: create 10 random wolves + 5 random food sources (valid CH sets)",
         fc="#ffffff", ec=style.INK, fs=9)
    _box(ax, 22, 73, 34, 7, "1  GWO step: every wolf moves\ntowards α, β, δ (global exploration)", fs=8.8)
    _box(ax, 78, 60, 34, 7, "2  Receive α, β, δ: they replace the\nWORST food sources (if better, no copies)",
         fs=8.8)
    _box(ax, 78, 49, 34, 6, "3  Employed bees refine every source\n(including the received elites)", fs=8.8)
    _box(ax, 78, 39, 34, 6, "4  Onlooker bees exploit the\nmost promising sources", fs=8.8)
    _box(ax, 78, 29, 34, 6, "5  Scout bee replaces an exhausted\nsource (keeps diversity)", fs=8.8)
    _box(ax, 22, 29, 34, 7, "6  If ABC's best beats δ, it REPLACES\nthe worst wolf and joins α/β/δ", fs=8.8)
    ax.text(22, 51, "The pack always remembers\nα, β, δ = the three best DIFFERENT\nCH sets found so far.\n\n"
                    "A bee's refinement that enters the\nleader set steers every wolf's\nnext move (step 1).",
            ha="center", va="center", fontsize=8.5, color=style.INK_2, linespacing=1.35)
    _box(ax, 50, 12, 52, 6, "7  Elite preservation: best so far = better of (α, ABC best)", fs=8.8,
         fc="#ffffff", ec=NODE)
    _arrow(ax, (50, 92.5), (22, 76.6), color=style.INK_2)
    _arrow(ax, (39, 70), (61, 61), color=GWO_C, lw=2.2)
    ax.text(50, 69.5, "GWO → ABC\nelite transfer", ha="center", fontsize=8.8, fontweight="bold", color=GWO_C)
    for y0, y1 in ((56.5, 52), (46, 42), (36, 32)):
        _arrow(ax, (78, y0), (78, y1), color=ABC_C)
    _arrow(ax, (61, 28), (39, 29), color=ABC_C, lw=2.2)
    ax.text(50, 32.5, "ABC → GWO\nfeedback", ha="center", fontsize=8.8, fontweight="bold", color=ABC_C)
    _arrow(ax, (22, 25.5), (30, 15), color=style.INK_2)
    _path(ax, [(24, 12), (1.2, 12), (1.2, 73), (5, 73)], color=NODE, lw=1.3)
    ax.text(1.8, 47, "repeat for 30 iterations", fontsize=8.5, color=NODE, fontweight="bold", rotation=90,
            va="center")
    _arrow(ax, (76, 12), (82, 12), color=NODE)
    ax.text(83, 12, "after the last iteration:\nthe best CH set is used\nin this round", fontsize=8.5, color=NODE,
            va="center")
    ax.text(50, 3, "Fair budget: 10 wolves + 5 employed + 5 onlooker bees = 20 fitness evaluations per iteration "
                   "(+1 when a scout fires) —\nthe same as GWO alone (20 wolves) or ABC alone (10 employed + 10 "
                   "onlooker bees, +1 scout).", ha="center", fontsize=8.3, color=style.INK_2, va="center")
    ax.set_title("Proposed Hybrid GWO-ABC: two populations that exchange their best solutions every iteration",
                 loc="left")
    return _save(fig, "fig08_hybrid_gwo_abc.png", out)


def fig_encoding(out: Path) -> Path:
    fig, ax = _canvas(11.0, 4.6, (0, 110), (0, 46))
    bits = [0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
    energy = [0.48, 0.50, 0.21, 0.47, 0.49, 0.46, 0.30, 0.44, 0.50, 0.45]
    mean = float(np.mean(energy))
    ax.text(2, 43, "A candidate solution = one 0/1 value per ALIVE node (1 = this node is a cluster head)",
            fontsize=10, fontweight="bold", va="top")
    for i, (b, e) in enumerate(zip(bits, energy)):
        x = 14 + i * 9
        eligible = e >= mean
        ax.add_patch(Rectangle((x, 24), 8, 8, fc=CH if b else "#ffffff", ec=style.INK_2, lw=1))
        ax.text(x + 4, 28, str(b), ha="center", va="center", fontsize=13, fontweight="bold",
                color="white" if b else style.INK)
        ax.text(x + 4, 34, f"node {i}", ha="center", fontsize=8.5, color=style.INK_2)
        ax.text(x + 4, 20.5, f"{e:.2f} J", ha="center", fontsize=8.5, color=style.INK if eligible else DEAD)
        ax.text(x + 4, 16.5, "eligible" if eligible else "too low", ha="center", fontsize=7.8,
                color=GWO_C if eligible else DEAD)
    ax.text(2, 28, "x =", fontsize=12, va="center")
    ax.text(2, 20.5, "energy", fontsize=8.5, va="center", color=style.INK_2)
    ax.text(2, 16.5, f"E ≥ mean\n({mean:.3f} J)?", fontsize=7.8, va="center", color=style.INK_2)
    ax.text(2, 8.5, "Rules applied to every candidate (repair):", fontsize=9, fontweight="bold")
    ax.text(2, 3.5, "• only eligible nodes (energy ≥ average) may be 1    • the number of 1s must stay between "
                    "K_min and K_max (default 2…8 for 100 nodes)    • dead nodes are not in the vector at all",
            fontsize=8.6)
    ax.set_title("How a cluster-head choice is stored inside GWO, ABC and the hybrid", loc="left")
    return _save(fig, "fig09_solution_encoding.png", out)


def fig_lifetime_metrics(out: Path, folder: Path | None = None) -> Path | None:
    """FND / HND / LND and node-rounds marked on real alive-node curves (scenario S1, run 0)."""
    from evaluation.metrics import lifetime_rounds
    folder = folder or RESULTS_DIR / "scenarios" / "S1_100nodes"
    if not (folder / "history_raw.csv.gz").exists():
        return None
    hist = pd.read_csv(folder / "history_raw.csv.gz", usecols=["algorithm", "run", "round", "alive", "dead"])
    fig = style.new_figure(11.0, 4.8)
    ax = fig.add_subplot()
    for alg in ("LEACH", "Hybrid GWO-ABC"):
        h = hist[(hist["algorithm"] == alg) & (hist["run"] == 0)]
        if h.empty:
            continue
        n = int(h["alive"].iloc[0] + h["dead"].iloc[0])
        deaths = np.full(n, -1)
        dead_by_round = np.r_[0, h["dead"].values]
        newly = np.diff(dead_by_round)
        k = 0
        for r, c in zip(h["round"].values, newly):
            deaths[k:k + c] = r
            k += c
        lt = lifetime_rounds(deaths, n)
        col = style.color(alg)
        ax.plot(h["round"], h["alive"], color=col, ls=style.linestyle(alg), label=f"{alg} (run 0)")
        if alg == "Hybrid GWO-ABC":
            ax.fill_between(h["round"], 0, h["alive"], color=col, alpha=0.08, lw=0)
            ax.text(380, 40, "shaded area = node-rounds\n(sum of alive nodes over all rounds)", fontsize=8.5,
                    color=col)
        for key, txt in (("fnd", "FND"), ("hnd", "HND"), ("lnd", "LND")):
            r = lt[key]
            y = float(h.loc[h["round"] == r, "alive"].iloc[0]) if (h["round"] == r).any() else 0.0
            ax.scatter([r], [y], color=col, s=36, zorder=4)
            off = {"LEACH": (-58, -26), "Hybrid GWO-ABC": (8, 10)}[alg]
            ax.annotate(f"{txt} {r:.0f}", (r, y), xytext=off, textcoords="offset points", fontsize=8.5, color=col,
                        arrowprops=dict(arrowstyle="-", color=col, lw=0.7))
    ax.axhline(50, color=style.MUTED, ls=":", lw=1)
    ax.text(5, 52, "half of the nodes (HND line)", fontsize=8, color=style.MUTED)
    ax.set_xlabel("Round")
    ax.set_ylabel("Alive nodes")
    ax.set_ylim(0, 105)
    ax.set_title("Network lifetime metrics on real simulation data (scenario S1, run 0)", loc="left")
    ax.legend(loc="lower left")
    return _save(fig, "fig10_lifetime_metrics.png", out)


def fig_program_structure(out: Path) -> Path:
    fig, ax = _canvas(11.5, 6.8, (0, 100), (0, 100))
    _box(ax, 50, 92, 44, 8, "main.py  (command line)      gui/dashboard.py  (window)\nyou start everything here",
         fc="#ffffff", ec=style.INK, weight="bold", fs=9)
    _box(ax, 50, 74, 44, 9, "experiments/\nexperiment_runner.py, base_paper.py\nruns many simulations (paired seeds)",
         fc=TINT["setup"], fs=8.8)
    _box(ax, 16, 50, 26, 11, "simulation/\nsimulator.py (round loop),\nclustering.py,\ntransmission.py",
         fc=TINT["loop"], fs=8.6)
    _box(ax, 50, 50, 28, 11, "algorithms/\nleach.py, gwo.py, abc.py,\nhybrid_gwo_abc.py, deai_pso.py,\nfitness.py",
         fc=TINT["gwo"], fs=8.6)
    _box(ax, 84, 50, 26, 11, "models/\nnetwork.py, node.py,\nenergy_model.py", fc=TINT["abc"], fs=8.6)
    _box(ax, 30, 26, 34, 10, "evaluation/\nmetrics.py, statistics.py,\ncomparison.py, report.py", fc=TINT["post"],
         fs=8.6)
    _box(ax, 74, 26, 30, 10, "visualization/\nnetwork, performance and\nconvergence plots", fc=TINT["post"], fs=8.6)
    _box(ax, 50, 7, 70, 8, "results/   CSV files  +  PNG graphs  +  report.md  (one folder per experiment)",
         fc="#ffffff", ec=style.SLOTS[5], weight="bold", fs=9)
    ax.text(50, 99, "config.py holds every parameter (defaults, JSON save/load, --set changes)", ha="center",
            fontsize=8.5, color=style.INK_2)
    _arrow(ax, (50, 88), (50, 78.5))
    _arrow(ax, (40, 69.5), (20, 55.5))
    _arrow(ax, (29, 50), (36, 50))
    ax.text(32.5, 52.3, "asks for\nCH set", fontsize=7.5, ha="center", color=style.INK_2)
    _arrow(ax, (64, 50), (71, 50))
    ax.text(67.5, 52.3, "uses", fontsize=7.5, ha="center", color=style.INK_2)
    _arrow(ax, (14, 44.5), (24, 31))
    ax.text(1, 36, "metrics of every round", fontsize=7.8, color=style.INK_2)
    _arrow(ax, (47, 26), (59, 26))
    ax.text(53, 28, "figures", fontsize=7.8, ha="center", color=style.INK_2)
    _arrow(ax, (30, 21), (42, 11))
    _arrow(ax, (74, 21), (60, 11))
    ax.set_title("How the program is organised (folders and their jobs)", loc="left")
    return _save(fig, "fig11_program_structure.png", out)


def fig_leach_threshold(out: Path, cfg: SimulationConfig) -> Path:
    from algorithms.leach import LEACH
    alg = LEACH(cfg, 0)
    alg.reset(Network.deploy(cfg))
    r = np.arange(1, 2 * alg.epoch + 1)
    T = np.array([alg.threshold(int(x)) for x in r])
    fig = style.new_figure(9.0, 4.0)
    ax = fig.add_subplot()
    ax.bar(r, T, color=style.color("LEACH"), width=0.7)
    for x in (1, 10, 19, 20):
        ax.annotate(f"{alg.threshold(x):.3f}", (x, alg.threshold(x)), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=8)
    ax.set_xlabel("Round r")
    ax.set_ylabel("Threshold T(n)")
    ax.set_title(f"LEACH: chance that a node in G becomes CH (p = {cfg.ch_percentage}, epoch = {alg.epoch} rounds)",
                 loc="left")
    ax.grid(axis="x", visible=False)
    return _save(fig, "fig12_leach_threshold.png", out)


def make_all(out: Path | None = None) -> list[Path]:
    """Create every documentation figure; returns the written paths."""
    out = Path(out or FIG_DIR)
    cfg = SimulationConfig()
    paths = [fig_architecture(out), fig_round_flowchart(out), fig_energy_model(out, cfg), fig_fitness_example(out),
             fig_gwo_concept(out), fig_gwo_parameters(out, cfg.opt_iterations), fig_abc_cycle(out),
             fig_hybrid_flow(out), fig_encoding(out), fig_lifetime_metrics(out), fig_program_structure(out),
             fig_leach_threshold(out, cfg)]
    return [p for p in paths if p is not None]


if __name__ == "__main__":
    for p in make_all():
        print(p)
