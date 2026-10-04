"""Tkinter dashboard: configure, run, pause, stop, reset and export WSN simulations.

The simulation runs in a worker thread (one ``Simulator.step`` per round) and
posts records to a queue; the Tk main loop polls the queue and redraws, so the
window stays responsive. All values shown come from the running simulation.
"""
from __future__ import annotations

import json
import queue
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from algorithms import BASE_PAPER, COMPARISON_ALGORITHMS, MAIN_ALGORITHMS, PROPOSED_EQ12
from config import RESULTS_DIR, SimulationConfig
from models.network import Network
from simulation.simulator import Simulator
from visualization import style
from visualization.network_plot import draw_network, network_snapshot

FIELDS = [  # label, config key, type
    ("Number of nodes", "n_nodes", int), ("Area width (m)", "area_width", float),
    ("Area height (m)", "area_height", float), ("Initial energy (J)", "initial_energy", float),
    ("Packet size (bits)", "packet_bits", int), ("Number of rounds", "rounds", int),
    ("CH percentage (0-1)", "ch_percentage", float), ("BS x (m)", "bs_x", float), ("BS y (m)", "bs_y", float),
    ("GWO population", "gwo.population", int), ("ABC colony size", "abc.colony_size", int),
    ("Optimisation iterations", "opt_iterations", int), ("Random seed", "seed", int),
]
STATS = [("round", "Current round"), ("alive", "Alive nodes"), ("dead", "Dead nodes"),
         ("residual", "Residual energy (J)"), ("consumed", "Energy consumed (J)"), ("ch", "CH count"),
         ("generated", "Packets generated"), ("delivered", "Packets delivered"), ("pdr", "PDR"),
         ("fitness", "Current fitness")]
# LEACH, GWO, ABC, Hybrid GWO-ABC (spec) + base paper's DEAI-PSO + proposed optimiser on the paper's objective
ALGORITHMS = MAIN_ALGORITHMS + [BASE_PAPER, PROPOSED_EQ12, "Random"]
COMPARE = COMPARISON_ALGORITHMS + [BASE_PAPER, PROPOSED_EQ12]


def presets(default: SimulationConfig) -> dict:
    """Configurations selectable in the dashboard: project default + the base paper's three scenarios."""
    from experiments.base_paper import PAPER_SCENARIOS, scenario_config, tuned_overrides
    out = {"Project default (BS at centre)": default}
    for name, (n, side, _) in PAPER_SCENARIOS.items():
        out[f"Base paper {name[:3]}: {n} nodes, {side:g}×{side:g} m, BS (200, 50)"] = \
            scenario_config(name, default, **tuned_overrides())
    return out


def _get(cfg: SimulationConfig, dotted: str):
    obj = cfg
    for part in dotted.split("."):
        obj = getattr(obj, part)
    return obj


class Dashboard(ttk.Frame):
    def __init__(self, master: tk.Tk, config: SimulationConfig | None = None):
        super().__init__(master, padding=8)
        self.master = master
        self.base_config = config or SimulationConfig()
        self.queue: queue.Queue = queue.Queue()
        self.worker: threading.Thread | None = None
        self.running = threading.Event()        # set = not paused
        self.stop_flag = threading.Event()
        self.sim: Simulator | None = None
        self.records: list = []
        self.compare_results: dict = {}
        self.network: Network | None = None
        self.vars: dict[str, tk.StringVar] = {}
        self.stat_vars: dict[str, tk.StringVar] = {}

        style.apply()
        self._build()
        self.grid(sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.reset()
        self.after(60, self._poll)

    # ================================================================ layout
    def _scrollable_left(self) -> ttk.Frame:
        """Left control column inside a vertically scrollable canvas (fits small laptop screens)."""
        holder = ttk.Frame(self)
        holder.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        holder.rowconfigure(0, weight=1)
        canvas = tk.Canvas(holder, highlightthickness=0, width=250)
        bar = ttk.Scrollbar(holder, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)
        inner.bind("<Configure>", lambda e: (canvas.configure(scrollregion=canvas.bbox("all")),
                                             canvas.configure(width=inner.winfo_reqwidth())))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=bar.set)
        canvas.grid(row=0, column=0, sticky="ns")
        bar.grid(row=0, column=1, sticky="ns")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-e.delta / 120), "units")
                        if str(e.widget).startswith(str(holder)) else None)
        return inner

    def _build(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        left = self._scrollable_left()

        preset_box = ttk.LabelFrame(left, text="Scenario preset", padding=6)
        preset_box.pack(fill="x", pady=(0, 6))
        self.presets = presets(self.base_config)
        self.preset = tk.StringVar(value=next(iter(self.presets)))
        combo = ttk.Combobox(preset_box, textvariable=self.preset, values=list(self.presets), state="readonly",
                             width=34)
        combo.pack(fill="x")
        combo.bind("<<ComboboxSelected>>", lambda e: self.apply_preset())

        cfg_box = ttk.LabelFrame(left, text="Configuration", padding=6)
        cfg_box.pack(fill="x")
        for r, (label, key, _) in enumerate(FIELDS):
            ttk.Label(cfg_box, text=label).grid(row=r, column=0, sticky="w", pady=1)
            var = tk.StringVar(value=str(_get(self.base_config, key)))
            ttk.Entry(cfg_box, textvariable=var, width=10, justify="right").grid(row=r, column=1, pady=1)
            self.vars[key] = var

        alg_box = ttk.LabelFrame(left, text="Algorithm", padding=6)
        alg_box.pack(fill="x", pady=6)
        self.algorithm = tk.StringVar(value="Hybrid GWO-ABC")
        labels = {BASE_PAPER: "DEAI-PSO (base paper)", PROPOSED_EQ12: "Hybrid GWO-ABC on base-paper objective"}
        for a in ALGORITHMS:
            ttk.Radiobutton(alg_box, text=labels.get(a, a), value=a, variable=self.algorithm).pack(anchor="w")

        view_box = ttk.LabelFrame(left, text="Display", padding=6)
        view_box.pack(fill="x")
        ttk.Label(view_box, text="Redraw every N rounds").grid(row=0, column=0, sticky="w")
        self.redraw_every = tk.StringVar(value="5")
        ttk.Entry(view_box, textvariable=self.redraw_every, width=5, justify="right").grid(row=0, column=1)
        self.show_links = tk.BooleanVar(value=True)
        self.show_bs = tk.BooleanVar(value=False)
        self.show_ids = tk.BooleanVar(value=False)
        ttk.Checkbutton(view_box, text="Cluster links", variable=self.show_links).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(view_box, text="CH → BS links", variable=self.show_bs).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(view_box, text="Node IDs", variable=self.show_ids).grid(row=3, column=0, sticky="w")

        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=8)
        self.btn_run = ttk.Button(btns, text="Run", command=self.run)
        self.btn_pause = ttk.Button(btns, text="Pause", command=self.toggle_pause, state="disabled")
        self.btn_stop = ttk.Button(btns, text="Stop", command=self.stop, state="disabled")
        self.btn_reset = ttk.Button(btns, text="Reset", command=self.reset)
        self.btn_export = ttk.Button(btns, text="Export Results", command=self.export)
        for i, b in enumerate((self.btn_run, self.btn_pause, self.btn_stop, self.btn_reset)):
            b.grid(row=i // 2, column=i % 2, sticky="ew", padx=2, pady=2)
        self.btn_export.grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=2)
        btns.columnconfigure((0, 1), weight=1)
        self.status = tk.StringVar(value="Ready")
        ttk.Label(left, textvariable=self.status, wraplength=230, foreground=style.INK_2).pack(fill="x")

        right = ttk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        dash = ttk.LabelFrame(right, text="Dashboard", padding=6)
        dash.grid(row=0, column=0, sticky="ew")
        for i, (key, label) in enumerate(STATS):
            cell = ttk.Frame(dash, padding=(6, 2))
            cell.grid(row=i // 5, column=i % 5, sticky="w")
            ttk.Label(cell, text=label, foreground=style.INK_2).pack(anchor="w")
            v = tk.StringVar(value="–")
            ttk.Label(cell, textvariable=v, font=("Segoe UI", 13, "bold")).pack(anchor="w")
            self.stat_vars[key] = v
        for c in range(5):
            dash.columnconfigure(c, weight=1)

        nb = ttk.Notebook(right)
        nb.grid(row=1, column=0, sticky="nsew", pady=(6, 0))
        self.fig_net, self.canvas_net = self._tab(nb, "Network", 6, 4.2)
        self.ax_net = self.fig_net.add_subplot()
        self.fig_perf, self.canvas_perf = self._tab(nb, "Performance", 6, 4.2)
        self.ax_perf = self.fig_perf.subplots(2, 2)
        self.fig_conv, self.canvas_conv = self._tab(nb, "Convergence", 6, 4.2)
        self.ax_conv = self.fig_conv.add_subplot()
        self._build_compare_tab(nb)

    def _tab(self, nb, title, w, h):
        frame = ttk.Frame(nb)
        nb.add(frame, text=title)
        fig = Figure(figsize=(w, h), layout="constrained")
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return fig, canvas

    def _build_compare_tab(self, nb):
        frame = ttk.Frame(nb, padding=6)
        nb.add(frame, text="Compare all")
        top = ttk.Frame(frame)
        top.pack(fill="x")
        self.btn_compare = ttk.Button(top, text="Run all algorithms (incl. base paper DEAI-PSO) on the same network",
                                      command=self.run_comparison)
        self.btn_compare.pack(side="left")
        self.compare_status = tk.StringVar(value="")
        ttk.Label(top, textvariable=self.compare_status, foreground=style.INK_2).pack(side="left", padx=8)
        cols = ("Algorithm", "FND", "HND", "LND", "Residual@cp (J)", "Throughput", "PDR", "Runtime (s)",
                "Fitness")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=5)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=80, minwidth=50, anchor="e" if c != "Algorithm" else "w")
        self.tree.pack(fill="x", pady=6)
        self.fig_cmp = Figure(figsize=(6, 3), layout="constrained")
        self.canvas_cmp = FigureCanvasTkAgg(self.fig_cmp, master=frame)
        self.canvas_cmp.get_tk_widget().pack(fill="both", expand=True)
        self.ax_cmp = self.fig_cmp.subplots(1, 2)

    # ================================================================ config
    def apply_preset(self):
        """Load a preset (incl. settings without a field, e.g. control packets and free-node radius)."""
        self.base_config = self.presets[self.preset.get()]
        for _, key, _ in FIELDS:
            self.vars[key].set(str(_get(self.base_config, key)))
        self.reset()

    def read_config(self) -> SimulationConfig | None:
        changes = {}
        try:
            for label, key, typ in FIELDS:
                changes[key] = typ(self.vars[key].get().strip())
            cfg = self.base_config.replace(**changes)
            cfg.checkpoint_round = min(cfg.checkpoint_round, cfg.rounds)
            cfg.validate()
            return cfg
        except (ValueError, KeyError) as e:
            messagebox.showerror("Invalid configuration", str(e))
            return None

    # ================================================================ actions
    def reset(self):
        self._halt_worker()
        cfg = self.read_config()
        if cfg is None:
            return
        self.config_used = cfg
        self.network = Network.deploy(cfg)
        self.sim = None
        self.records = []
        for v in self.stat_vars.values():
            v.set("–")
        self.stat_vars["alive"].set(str(self.network.n))
        self.stat_vars["residual"].set(f"{self.network.total_energy:.3f}")
        snap = network_snapshot(self.network)
        draw_network(self.ax_net, snap, ids=self.show_ids.get(), title="Initial deployment")
        self.canvas_net.draw_idle()
        self._draw_performance()
        self.ax_conv.clear()
        self.ax_conv.set_title("Optimiser convergence (latest round)", loc="left")
        self.canvas_conv.draw_idle()
        self._buttons(idle=True)
        self.status.set(f"Network deployed: {cfg.n_nodes} nodes, seed {cfg.seed}. Press Run.")

    def run(self):
        if self.worker and self.worker.is_alive():
            return
        cfg = self.read_config()
        if cfg is None:
            return
        if (self.sim is None or self.sim.finished or cfg != self.config_used
                or self.sim.algorithm.name != self.algorithm.get()):
            self.config_used = cfg
            self.network = Network.deploy(cfg)
            self.sim = Simulator(cfg, self.algorithm.get(), self.network, curve_rounds=())
            self.records = []
        try:
            every = max(1, int(self.redraw_every.get()))
        except ValueError:
            every = 5
        self.stop_flag.clear()
        self.running.set()
        self.worker = threading.Thread(target=self._work, args=(self.sim, every), daemon=True)
        self.worker.start()
        self._buttons(idle=False)
        self.status.set(f"Running {self.sim.algorithm.name} …")

    def _work(self, sim: Simulator, every: int):
        t0 = time.perf_counter()
        while not sim.finished and not self.stop_flag.is_set():
            self.running.wait()
            if self.stop_flag.is_set():
                break
            rec = sim.step()
            sel = sim.last_selection
            curves = sel.curves if sel is not None else {}
            snap = sim.snapshot() if (rec.round % every == 0 or sim.finished) else None
            self.queue.put(("round", rec, snap, curves))
        self.queue.put(("done", time.perf_counter() - t0, sim.finished))

    def toggle_pause(self):
        if self.running.is_set():
            self.running.clear()
            self.btn_pause.config(text="Resume")
            self.status.set("Paused")
        else:
            self.running.set()
            self.btn_pause.config(text="Pause")
            self.status.set("Running …")

    def stop(self):
        if not (self.worker and self.worker.is_alive()):
            return                                    # nothing running: keep the final status message
        self.stop_flag.set()
        self.running.set()
        self.status.set("Stopping …")

    def _halt_worker(self):
        self.stop_flag.set()
        self.running.set()
        if self.worker and self.worker.is_alive():
            self.worker.join(timeout=5)
        while not self.queue.empty():
            self.queue.get_nowait()

    def _buttons(self, idle: bool):
        self.btn_run.config(state="normal" if idle else "disabled")
        self.btn_pause.config(state="disabled" if idle else "normal", text="Pause")
        self.btn_stop.config(state="disabled" if idle else "normal")

    # ================================================================ updates
    def _poll(self):
        last_snap, last_curves, got = None, None, False
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg[0] == "round":
                    _, rec, snap, curves = msg
                    self.records.append(rec)
                    got = True
                    if snap is not None:
                        last_snap, last_curves = snap, curves
                elif msg[0] == "done":
                    self._finished(msg[1], msg[2])
                elif msg[0] == "compare":
                    self._compare_done(msg[1])
                elif msg[0] == "compare_progress":
                    self.compare_status.set(msg[1])
        except queue.Empty:
            pass
        if got:
            self._update_stats(self.records[-1])
        if last_snap is not None:
            draw_network(self.ax_net, last_snap, links=self.show_links.get(), bs_links=self.show_bs.get(),
                         ids=self.show_ids.get(), energy=True, initial_energy=self.config_used.initial_energy,
                         title=f"{self.sim.algorithm.name} — round {last_snap['round']}")
            self.canvas_net.draw_idle()
            self._draw_performance()
            if last_curves:
                self._draw_convergence(last_curves, last_snap["round"])
        self.after(60, self._poll)

    def _update_stats(self, rec):
        sv = self.stat_vars
        sv["round"].set(str(rec.round))
        sv["alive"].set(str(rec.alive))
        sv["dead"].set(str(rec.dead))
        sv["residual"].set(f"{rec.residual_energy:.3f}")
        sv["consumed"].set(f"{rec.consumed_energy:.3f}")
        sv["ch"].set(str(rec.ch_count))
        sv["generated"].set(f"{rec.packets_generated:,}")
        sv["delivered"].set(f"{rec.packets_delivered:,}")
        sv["pdr"].set(f"{rec.pdr:.4f}")
        sv["fitness"].set("n/a" if np.isnan(rec.fitness) else f"{rec.fitness:.4f}")

    def _draw_performance(self):
        axes = self.ax_perf.ravel()
        specs = [("alive", "Alive nodes"), ("residual_energy", "Residual energy (J)"),
                 ("pdr", "PDR (cumulative)"), ("ch_count", "CH count")]
        df = pd.DataFrame([r.as_dict() for r in self.records]) if self.records else None
        name = self.sim.algorithm.name if self.sim else ""
        for ax, (col, title) in zip(axes, specs):
            ax.clear()
            ax.set_title(title, loc="left", fontsize=10)
            if df is not None and len(df):
                ax.plot(df["round"], df[col], color=style.color(name), lw=1.6)
            ax.set_xlabel("Round", fontsize=8)
        self.canvas_perf.draw_idle()

    def _draw_convergence(self, curves: dict, round_no: int):
        from visualization.convergence_plot import CURVE_COLORS, CURVE_LABELS
        ax = self.ax_conv
        ax.clear()
        order = [k for k in ("hybrid", "abc", "gwo", "deai_pso") if k in curves] + \
                [k for k in curves if k not in ("hybrid", "abc", "gwo", "deai_pso")]
        for key in order:
            ax.plot(np.arange(len(curves[key])), curves[key], color=CURVE_COLORS.get(key, style.SLOTS[4]),
                    label=CURVE_LABELS.get(key, key), ls={"gwo": "-.", "abc": ":"}.get(key, "-"))
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Best-so-far fitness")
        ax.set_title(f"Optimiser convergence — round {round_no}", loc="left")
        ax.legend()
        self.canvas_conv.draw_idle()

    def _finished(self, elapsed: float, completed: bool):
        self._buttons(idle=True)
        if self.sim is None:
            return
        res = self.sim.result()
        s = res.summary
        note = "finished" if completed else "stopped"
        self.status.set(f"{self.sim.algorithm.name} {note} after {self.sim.round} rounds ({elapsed:.1f}s). "
                        f"FND {s['fnd']:.0f}{'+' if s['fnd_censored'] else ''}, "
                        f"HND {s['hnd']:.0f}{'+' if s['hnd_censored'] else ''}, "
                        f"LND {s['lnd']:.0f}{'+' if s['lnd_censored'] else ''}, PDR {s['pdr']:.4f}.")
        snap = self.sim.snapshot()
        draw_network(self.ax_net, snap, links=self.show_links.get(), bs_links=self.show_bs.get(),
                     ids=self.show_ids.get(), energy=True, initial_energy=self.config_used.initial_energy,
                     title=f"{self.sim.algorithm.name} — round {snap['round']} ({note})")
        self.canvas_net.draw_idle()
        self._draw_performance()

    # ================================================================ comparison tab
    def run_comparison(self):
        cfg = self.read_config()
        if cfg is None:
            return
        self.btn_compare.config(state="disabled")
        net = Network.deploy(cfg)

        def work():
            out = {}
            for alg in COMPARE:
                self.queue.put(("compare_progress", f"Running {alg} …"))
                out[alg] = Simulator(cfg, alg, net, curve_rounds=()).run()
            self.queue.put(("compare", out))

        threading.Thread(target=work, daemon=True).start()

    def _compare_done(self, results: dict):
        self.compare_results = results
        self.btn_compare.config(state="normal")
        self.compare_status.set("Done — identical network, seed and radio model for every algorithm.")
        for row in self.tree.get_children():
            self.tree.delete(row)
        for alg, res in results.items():
            s = res.summary
            lt = [f"{s[k]:.0f}{'+' if s[k + '_censored'] else ''}" for k in ("fnd", "hnd", "lnd")]
            self.tree.insert("", "end", values=(alg, *lt, f"{s['residual_energy_cp']:.2f}",
                                                f"{s['throughput_packets']:,}", f"{s['pdr']:.4f}",
                                                f"{s['runtime']:.2f}", f"{s['final_fitness']:.4f}"))
        a1, a2 = self.ax_cmp
        for ax, col, title in ((a1, "alive", "Alive nodes"), (a2, "residual_energy", "Residual energy (J)")):
            ax.clear()
            for alg, res in results.items():
                ax.plot(res.history["round"], res.history[col], color=style.color(alg), ls=style.linestyle(alg),
                        label=alg)
            ax.set_title(title, loc="left", fontsize=10)
            ax.set_xlabel("Round")
        a1.legend(fontsize=8)
        self.canvas_cmp.draw_idle()

    # ================================================================ export
    def export(self):
        if not self.records and not self.compare_results:
            messagebox.showinfo("Export", "Nothing to export yet — run a simulation first.")
            return
        out = RESULTS_DIR / "gui_exports" / datetime.now().strftime("%Y%m%d_%H%M%S")
        out.mkdir(parents=True, exist_ok=True)
        self.config_used.save(out / "config.json")
        if self.sim is not None and self.records:
            res = self.sim.result()
            res.history.to_csv(out / "history.csv", index=False)
            summary = {"algorithm": res.algorithm, "seed": res.seed, **res.summary}
            pd.DataFrame([summary]).to_csv(out / "summary.csv", index=False)
            (out / "summary.json").write_text(json.dumps(summary, indent=2, default=float), encoding="utf-8")
            self.sim.network.to_dataframe().to_csv(out / "nodes_final.csv", index=False)
            res.ch_log.to_csv(out / "cluster_heads.csv", index=False)
            self.fig_net.savefig(out / "network.png", dpi=130)
            self.fig_perf.savefig(out / "performance.png", dpi=130)
            self.fig_conv.savefig(out / "convergence.png", dpi=130)
        if self.compare_results:
            rows = [{"algorithm": a, **r.summary} for a, r in self.compare_results.items()]
            pd.DataFrame(rows).to_csv(out / "comparison_summary.csv", index=False)
            pd.concat([r.history.assign(algorithm=a) for a, r in self.compare_results.items()]).to_csv(
                out / "comparison_history.csv", index=False)
            pd.concat([r.ch_log.assign(algorithm=a) for a, r in self.compare_results.items()]).to_csv(
                out / "comparison_cluster_heads.csv", index=False)
            self.fig_cmp.savefig(out / "comparison.png", dpi=130)
        messagebox.showinfo("Export", f"Results exported to\n{out}")
        self.status.set(f"Exported to {out}")


def launch(config: SimulationConfig | None = None):
    root = tk.Tk()
    root.title("Hybrid GWO-ABC WSN Simulator")
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{min(1400, sw - 40)}x{min(900, sh - 80)}+10+10")
    root.minsize(900, 560)
    try:
        root.state("zoomed")               # maximised on Windows
    except tk.TclError:
        pass
    try:
        ttk.Style().theme_use("vista")
    except tk.TclError:
        pass
    app = Dashboard(root, config)

    def on_close():
        app._halt_worker()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
