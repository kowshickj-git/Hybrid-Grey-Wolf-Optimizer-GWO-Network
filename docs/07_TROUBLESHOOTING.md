# 7. Troubleshooting — Problem → Reason → Solution

Run every command from the project folder `Hybrid-GWO-ABC-WSN` (the folder that contains `main.py`). If your
problem is not listed, copy the **last lines** of the error message — they name the problem.

Contents: [Installation](#installation-and-python) · [Running](#running-the-program) · [Graphs and CSV](#graphs-and-csv-files) ·
[Parameters](#parameters) · [Speed](#speed-and-long-runs) · [Results](#results-that-look-unexpected) ·
[Cluster heads](#cluster-head-selection) · [GUI](#the-window-gui) · [Tests](#tests)

---

## Installation and Python

<a id="t1"></a>
### 'python' is not recognized as an internal or external command

* **Reason:** Python is not installed, or its folder was not added to PATH during installation.
* **Solution:**
  1. Try the Python launcher instead: `py --version`. If it works, use `py` wherever these documents say `python`
     (e.g. `py main.py`, `py -m pip install -r requirements.txt`).
  2. Otherwise re-run the Python installer → *Modify* → enable *Add Python to environment variables*, or uninstall
     and reinstall with **"Add python.exe to PATH"** ticked.
  3. **Close and reopen** the terminal (and VS Code) afterwards — PATH changes only apply to new terminals.

### Typing `python` opens the Microsoft Store, or says "Python was not found"

* **Reason:** Windows has a built-in shortcut ("app execution alias") that points to the Store.
* **Solution:** install Python from python.org (Step 1 of [01_INSTALL_AND_RUN.md](01_INSTALL_AND_RUN.md)), then
  Windows Settings → *Apps* → *Advanced app settings* → *App execution aliases* → switch **off** `python.exe` and
  `python3.exe`. Reopen the terminal.

### `pip` is not recognized, or `pip install` fails

* **Reason:** pip is not on PATH, it is outdated, or the network/permissions block the download.
* **Solution:**
  * Always call pip through Python: `python -m pip install -r requirements.txt`.
  * Update it: `python -m pip install --upgrade pip`.
  * *Permission denied*: use a virtual environment (Step 3), or add `--user`.
  * *SSL / proxy / timeout errors*: check the internet connection (university networks may need a proxy:
    `python -m pip install --proxy http://user:password@proxy:port -r requirements.txt`).

### ModuleNotFoundError: No module named 'numpy' (or pandas, matplotlib, scipy)

* **Reason:** the libraries were installed into a different Python than the one running the program (e.g. you
  installed them before activating the virtual environment, or VS Code uses another interpreter).
* **Solution:** activate the environment you use (`.\.venv\Scripts\Activate.ps1`), then run
  `python -m pip install -r requirements.txt` again. In VS Code: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> →
  *Python: Select Interpreter* → choose the same one. Check with
  `python -c "import sys; print(sys.executable)"`.

### Activate.ps1 cannot be loaded because running scripts is disabled on this system

* **Reason:** PowerShell's default security setting blocks scripts, including the venv activation script.
* **Solution:** run once `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` and answer `Y`.
  Alternatives without changing the setting: use *Command Prompt* and `.venv\Scripts\activate.bat`, or skip
  activation and call the environment's Python directly: `.venv\Scripts\python.exe main.py`.

### No module named 'tkinter' / '_tkinter' (the GUI does not start)

* **Reason:** Python was installed without "tcl/tk and IDLE" (or a minimal Python distribution is used).
* **Solution:** re-run the python.org installer → *Modify* → tick **tcl/tk and IDLE**. Everything except the GUI
  (all experiments, CSV files, graphs, reports) also works without Tkinter.

---

## Running the program

### can't open file '...main.py': [Errno 2] No such file or directory

* **Reason:** the terminal is not in the project folder.
* **Solution:** `cd` into the folder that contains `main.py`, e.g.
  `cd "C:\Users\<you>\Hybrid-GWO-ABC-WSN"` (quotes are needed if the path contains spaces). Check with `dir main.py`.

### ModuleNotFoundError: No module named 'config' (or 'algorithms', 'models', …)

* **Reason:** a file inside a sub-folder was started directly (e.g. `python algorithms\gwo.py`), so Python cannot
  see the project's packages.
* **Solution:** always start from the project folder through `main.py` (or `python -m pytest`, `python -m
  visualization.diagrams`).

### Incorrect paths / paths with spaces

* **Reason:** PowerShell splits arguments at spaces.
* **Solution:** put paths and names that contain spaces in double quotes:
  `python main.py reproduce "results\scenarios\S1_100nodes"`, `python main.py simulate -a "Hybrid GWO-ABC"`.
  Use backslashes `\` or forward slashes `/`; both work.

### ValueError: Unknown algorithm 'hybrid'

* **Reason:** algorithm names are case- and spelling-sensitive.
* **Solution:** use one of: `Random`, `LEACH`, `GWO`, `ABC`, `"Hybrid GWO-ABC"`, `DEAI-PSO`,
  `"Hybrid GWO-ABC (Eq. 12)"` (the error message lists every valid name).

---

## Graphs and CSV files

### Graphs are not created, or the report shows broken images

* **Reason:** the run stopped before the end (error, Ctrl+C, laptop asleep), the output folder is not writable,
  or the report is viewed from a different place than its folder.
* **Solution:** look at the last lines in the terminal for an error; re-run the command. Open `report.md` **from
  its own folder** in VS Code and press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd> (images are linked relative
  to the report). The graphs are ordinary PNG files next to `report.md`.

### Matplotlib errors about a "backend" or a display

* **Reason:** some environments have no screen.
* **Solution:** the project draws all saved graphs without a screen (Matplotlib `Figure` objects, no pop-up
  windows), so experiments work anywhere. Only the GUI needs a display.

### PermissionError: [Errno 13] Permission denied: '...\runs_raw.csv'

* **Reason:** the CSV file is open in Excel, which locks it, so the program cannot overwrite it.
* **Solution:** close the file in Excel and run the command again. To keep old results, copy the folder first
  or use `--out results\my_new_folder`.

### CSV files are missing

* **Reason:** CSV files are written only after **all** simulations of an experiment have finished.
* **Solution:** wait for the run to finish (the terminal prints the result table and the report path); for a
  fast check use `python main.py compare --runs 2`.

---

## Parameters

### ValueError: … must be … (invalid parameter)

* **Reason:** `config.validate()` rejects impossible values before anything runs. The messages are:
  `n_nodes must be >= 2`, `area must be positive`, `initial_energy must be > 0`, `packet_bits must be > 0`,
  `control_bits must be >= 0`, `rounds must be >= 1`, `ch_percentage must be in (0, 1)`,
  `ch_energy_threshold must be in [0, 1]`, `free_node_radius must be >= 0`, `DEAI-PSO needs >= 2 particles`,
  `DEAI-PSO weight a must be in [0, 1]`, `opt_iterations must be >= 1`,
  `GWO population must be >= 3 (alpha, beta, delta)`, `ABC colony_size must be >= 4`, `ABC limit must be >= 1`,
  `hybrid budget_share must be in (0, 1]`.
* **Solution:** use a value in the stated range. Percentages are fractions: 5 % is `ch_percentage=0.05`, not `5`.

### KeyError: 'Unknown config field: n_node'

* **Reason:** a typo in a `--set` name.
* **Solution:** use the exact names from the table in [01_INSTALL_AND_RUN.md](01_INSTALL_AND_RUN.md#step-9--change-parameters)
  or from `config.py`. Nested names need a dot: `gwo.population`, `abc.colony_size`, `weights.energy`.

### My `--set` change seems to have no effect

* **Reason:** spaces around `=`, or a GUI value changed without pressing **Reset**/**Run**.
* **Solution:** write `--set n_nodes=200` (no spaces). Every run saves the used values in `config.json` — check
  it. In the GUI, press **Reset** after editing a field.

---

## Speed and long runs

### The simulation is too slow

* **Reason:** each round, GWO/ABC/Hybrid evaluate about 620 candidate CH sets; the main experiments run hundreds
  of simulations. Larger networks (300 nodes) and more iterations take longer.
* **Solution (choose one):**
  * quick checks: `python main.py all --quick`, or fewer runs: `python main.py compare --runs 3`;
  * a smaller budget: `--set opt_iterations=10`, or a smaller network: `--set n_nodes=50`;
  * use more processor cores: experiments already use all cores but one (`--workers` changes it);
  * close other heavy programs and plug in the laptop (battery saving slows the processor);
  * LEACH and Random are almost instant — use them to check a setting first.

### The laptop went to sleep / a long run stopped

* **Reason:** Windows' sleep timer, or the lid was closed.
* **Solution:** the experiment commands ask Windows to stay awake while they run (no settings are changed), but
  closing the lid or an empty battery still stops them. Keep the laptop plugged in with the lid open, then run
  the command again (results are written only at the end of each experiment).

---

## Results that look unexpected

### "The Hybrid is not better than GWO or ABC in network lifetime"

* **Reason:** this is a real, measured result, not an error. All three optimisers find almost equally good CH sets
  for the network in the project's scenarios; the hybrid's advantage is a 4.7–7.5 % better **fitness**
  (optimisation quality), which does not turn into a significantly longer lifetime there.
* **Solution:** report it honestly — [05_RESULTS_AND_GRAPHS.md](05_RESULTS_AND_GRAPHS.md) and the viva section
  explain why. Do **not** change parameters to make the hybrid look better.

### "LEACH has a later Last Node Death (LND) than the optimisers"

* **Reason:** also real. The optimisers spread energy use very evenly, so all nodes die within a short window
  (FND is much later, but LND comes sooner). LEACH drains nodes unevenly: some die early, a few survive long.
* **Solution:** explain it as a trade-off: full coverage (FND/HND) favours the optimisers; "any node still alive"
  (LND) favours LEACH.

### "My lifetimes are much shorter than the base paper's published numbers"

* **Reason:** the base paper's published lifetimes (LND up to 4,756 rounds) are impossible under its own stated
  parameters: a node with 0.5 J that only powers its radio electronics for one 4000-bit packet per round lasts at
  most 0.5 / (4000 × 50 × 10⁻⁹) = 2,500 rounds.
* **Solution:** compare methods inside the same simulator (that is what this project does); see
  `results/base_paper/README.md`, section "Published numbers".

### "My numbers differ from the saved results / from a friend's"

* **Reason:** a different seed, different parameters, or different library versions. Run times always differ
  (they depend on the computer).
* **Solution:** use the saved settings: `python main.py reproduce results\scenarios\S1_100nodes`. With the same
  configuration, seed and library versions, lifetime, energy and packet numbers are identical.

---

## Cluster-head selection

### LEACH sometimes has 0 cluster heads, or a very different number each round

* **Reason:** LEACH's election is random by design (each node draws a random number). In scenario S1 about 0.5 %
  of rounds 1–500 have no CH; then every alive node sends directly to the BS, which is LEACH's normal fallback.
* **Solution:** none needed — it is the correct behaviour of LEACH and is visible in graph
  `15_ch_count_vs_rounds.png`.

### The optimisers choose between 2 and 8 CHs instead of exactly 5

* **Reason:** by design they may use K_opt × (1 ± 0.5) CHs (`count_tolerance`), and the fitness decides.
* **Solution:** to force exactly K_opt, use `--set count_tolerance=0`.

### Some nodes are never chosen as cluster head

* **Reason:** the optimisers only choose nodes whose energy is at least the average (eligibility rule), so
  nodes that have worked hard recover their turn only later; nodes far from everybody are rarely good CHs.
* **Solution:** check `ch_log_run0.csv` (every CH of every round). To switch the rule off: `--set
  ch_energy_threshold=0` (expect a much earlier first node death).

### With a base-paper preset, many nodes are never CH

* **Reason:** in the base paper's three-tier model, nodes closer than 85 m to the BS at (200, 50) are *free nodes*:
  they send directly to the BS and are never clustered.
* **Solution:** this is the paper's design (`free_node_radius`); set `--set free_node_radius=0` to disable it.

### "fitness = n/a" or no CH in the last rounds

* **Reason:** when almost all nodes are dead, there may be no node left to cluster.
* **Solution:** normal at the end of a simulation.

---

## The window (GUI)

### The window is bigger than the screen or looks cut off

* **Reason:** high display scaling on small laptop screens.
* **Solution:** the window opens maximised and the left panel scrolls (mouse wheel over the panel). Lower the
  Windows display scaling if needed.

### The window seems frozen ("Not responding")

* **Reason:** the simulation runs in the background; very frequent redrawing of large networks can make the window
  slow.
* **Solution:** increase *Redraw every N rounds* (e.g. 20), or press **Pause**. *Compare all* takes a few minutes
  because it runs every algorithm to the end.

---

## Tests

### Some tests fail

* **Reason:** usually a missing library or a wrong working folder; occasionally a changed parameter in
  `config.py`.
* **Solution:** run `python -m pip install -r requirements.txt`, run `python -m pytest` from the project folder,
  and undo edits in `config.py` (the tests expect the documented defaults). The failing test's name says which
  part is affected (e.g. `test_round_energy_accounting_exact` → energy model / transmission).

### MemoryError with very large networks

* **Reason:** the program stores all node-to-node distances (N × N values) and evaluates many candidate CH sets at
  once.
* **Solution:** networks up to a few hundred nodes are fine; for thousands of nodes use fewer runs and expect
  long run times.
