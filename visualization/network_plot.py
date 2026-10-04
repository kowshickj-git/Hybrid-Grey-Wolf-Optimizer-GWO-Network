"""Network topology views: deployment, CH selection, clusters, data flow, dead nodes.

``draw_network`` works on a *snapshot* dict (see ``Simulator.snapshot``) so the
same drawing code serves saved figures and the live GUI. Node roles are
encoded by marker shape as well as colour (never colour alone).
"""
from __future__ import annotations

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

from models.network import Network
from visualization import style

NODE = style.SLOTS[0]
CH = style.SLOTS[1]
DEAD = style.CRITICAL
BS = style.INK
LINK = "#b7b5ac"


def network_snapshot(network: Network, round_no: int = 0) -> dict:
    return {"round": round_no, "positions": network.positions.copy(), "bs": network.bs.copy(),
            "area": network.area, "alive": network.alive.copy(), "energy": network.energy.copy(),
            "is_ch": network.is_ch.copy(), "cluster_id": network.cluster_id.copy()}


def draw_network(ax, snap: dict, *, links: bool = False, bs_links: bool = False, ids: bool = False,
                 dead: bool = True, energy: bool = False, title: str | None = None,
                 initial_energy: float | None = None) -> None:
    pos, bs = snap["positions"], snap["bs"]
    alive, is_ch, cid = snap["alive"], snap["is_ch"] & snap["alive"], snap["cluster_id"]
    W, H = snap["area"]
    ax.clear()
    ax.set_facecolor(style.SURFACE)
    ax.add_patch(_boundary(W, H))

    if links:
        members = np.flatnonzero(alive & ~is_ch & (cid >= 0))
        segs = np.stack([pos[members], pos[cid[members]]], 1)
        ax.add_collection(LineCollection(segs, colors=LINK, linewidths=0.7, zorder=1))
    if bs_links:
        for j in np.flatnonzero(is_ch):
            ax.annotate("", xy=bs, xytext=pos[j], zorder=2,
                        arrowprops=dict(arrowstyle="-|>", color=CH, lw=1.2, alpha=0.8,
                                        shrinkA=4, shrinkB=6))
        if not is_ch.any():                    # no CH this round: nodes send straight to the BS
            direct = np.flatnonzero(alive)
            segs = np.stack([pos[direct], np.broadcast_to(bs, (len(direct), 2))], 1)
            ax.add_collection(LineCollection(segs, colors=LINK, linewidths=0.6, zorder=1))

    normal = alive & ~is_ch
    if energy and initial_energy:
        frac = np.clip(snap["energy"][normal] / initial_energy, 0, 1)
        sc = ax.scatter(pos[normal, 0], pos[normal, 1], c=frac, cmap="Blues", vmin=-0.3, vmax=1, s=28,
                        edgecolors=NODE, linewidths=0.6, zorder=3)
        sc.set_label("_")
    else:
        ax.scatter(pos[normal, 0], pos[normal, 1], s=26, color=NODE, edgecolors=style.SURFACE,
                   linewidths=0.8, zorder=3)
    ax.scatter(pos[is_ch, 0], pos[is_ch, 1], s=110, marker="^", color=CH, edgecolors=style.SURFACE,
               linewidths=1.0, zorder=4)
    if dead:
        d = ~alive
        ax.scatter(pos[d, 0], pos[d, 1], s=34, marker="x", color=DEAD, linewidths=1.6, zorder=3)
    ax.scatter([bs[0]], [bs[1]], s=170, marker="s", color=BS, edgecolors=style.SURFACE, zorder=5)
    if ids:
        for i, (x, y) in enumerate(pos):
            ax.annotate(str(i), (x, y), xytext=(3, 3), textcoords="offset points", fontsize=6,
                        color=style.MUTED)

    pad_x, pad_y = 0.05 * W, 0.05 * H
    ax.set_xlim(min(0, bs[0]) - pad_x, max(W, bs[0]) + pad_x)
    ax.set_ylim(min(0, bs[1]) - pad_y, max(H, bs[1]) + pad_y)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.grid(False)
    n_alive, n_ch = int(alive.sum()), int(is_ch.sum())
    ax.set_title(title or f"Round {snap['round']}", loc="left")
    ax.legend(handles=_legend_handles(dead and (~alive).any(), n_ch > 0), loc="upper left",
              bbox_to_anchor=(1.01, 1.0), borderaxespad=0)
    ax.text(1.01, 0.02, f"alive {n_alive}\nCHs {n_ch}\ndead {len(alive) - n_alive}",
            transform=ax.transAxes, fontsize=9, color=style.INK_2, va="bottom")


def _boundary(W, H):
    from matplotlib.patches import Rectangle
    return Rectangle((0, 0), W, H, fill=False, ec=style.AXIS, lw=1.2, ls="--", zorder=0)


def _legend_handles(show_dead: bool, show_ch: bool):
    h = [Line2D([], [], marker="o", ls="", color=NODE, label="Sensor node"),
         Line2D([], [], marker="s", ls="", color=BS, markersize=9, label="Base station")]
    if show_ch:
        h.insert(1, Line2D([], [], marker="^", ls="", color=CH, markersize=9, label="Cluster head"))
    if show_dead:
        h.append(Line2D([], [], marker="x", ls="", color=DEAD, markeredgewidth=1.6, label="Dead node"))
    return h


# ------------------------------------------------------------- saved figures
def _fig(snap, **kw):
    fig = style.new_figure(7.6, 6.0)
    draw_network(fig.add_subplot(), snap, **kw)
    return fig


def plot_topology(network: Network, path=None, ids: bool = False):
    snap = network_snapshot(network)
    snap["is_ch"][:] = False
    fig = _fig(snap, ids=ids, title=f"Initial WSN topology ({network.n} nodes)")
    return style.save(fig, path) if path else fig


def plot_ch_selection(snap: dict, path=None, algorithm: str = ""):
    fig = _fig(snap, title=f"{algorithm} CH selection — round {snap['round']}".strip())
    return style.save(fig, path) if path else fig


def plot_clusters(snap: dict, path=None, algorithm: str = ""):
    fig = _fig(snap, links=True, title=f"{algorithm} cluster formation — round {snap['round']}".strip())
    return style.save(fig, path) if path else fig


def plot_communication(snap: dict, path=None, algorithm: str = ""):
    fig = _fig(snap, links=True, bs_links=True,
               title=f"{algorithm} data flow: member → CH → BS — round {snap['round']}".strip())
    return style.save(fig, path) if path else fig


def plot_dead_nodes(snap: dict, path=None, algorithm: str = "", initial_energy: float | None = None):
    fig = _fig(snap, links=True, energy=initial_energy is not None, initial_energy=initial_energy,
               title=f"{algorithm} dead nodes — round {snap['round']}".strip())
    return style.save(fig, path) if path else fig
