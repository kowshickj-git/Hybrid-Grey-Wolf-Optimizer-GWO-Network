# 4. The algorithms, explained from zero

Contents: [1 The problem](#1-the-problem-every-algorithm-solves) · [2 Random and LEACH](#2-the-baselines-random-and-leach) ·
[3 GWO](#3-grey-wolf-optimizer-gwo-from-zero) · [4 ABC](#4-artificial-bee-colony-abc-from-zero) ·
[5 Hybrid GWO-ABC](#5-the-proposed-hybrid-gwo-abc) · [6 DEAI-PSO (base paper)](#6-the-base-papers-deai-pso-and-the-eq-12-variants) ·
[7 Side by side](#7-all-algorithms-side-by-side)

---

## 1. The problem every algorithm solves

At the start of **every round**, the network looks like this: some nodes are alive, each with its own position and
remaining energy. The question is:

> **Which alive nodes should be cluster heads in this round?**

```text
         input                              algorithm                          output
 ┌───────────────────────────┐     ┌──────────────────────────┐     ┌───────────────────────────┐
 │ alive nodes: positions,   │ ──▶ │ select(network, round)   │ ──▶ │ CH ids, e.g. [20, 55, 60, │
 │ energies, BS position     │     │ Random / LEACH / GWO /   │     │ 66, 70]                   │
 └───────────────────────────┘     │ ABC / Hybrid / DEAI-PSO  │     └───────────────────────────┘
                                   └──────────────────────────┘
```

Everything else in the round (cluster formation, transmission, energy, death) is the **same code for every
algorithm**. So any difference in lifetime or energy comes only from the CH choice.

Why not simply try every possibility? With 100 nodes and 2 to 8 CHs there are **203,366,882,895** possible CH
sets. Even at a million checks per second that is about 56 hours — for **one** round. Metaheuristics (GWO, ABC,
the hybrid, PSO) instead check about 620 well-chosen candidates per round and still find very good sets.

---

## 2. The baselines: Random and LEACH

### 2.1 Random (`algorithms/base.py`, `RandomSelector`)

```text
each round:  K_opt = round(5 % of alive nodes)
             choose K_opt alive nodes uniformly at random → CHs
```

No energy check, no memory, no optimisation. It shows what happens **without any intelligence**.

### 2.2 LEACH (`algorithms/leach.py`)

```text
at the start of each epoch (every 1/p = 20 rounds):  every node is put back into G
each round r, each alive node n in G:
      draw u ~ U(0, 1)
      if u < T(n) = p / (1 − p·((r − 1) mod 20)):   n becomes CH and leaves G
the other alive nodes join the nearest CH (or send directly to the BS if nobody volunteered)
```

* **Distributed:** every node decides alone, with no global knowledge — no positions, no energies.
* **Fair rotation:** every node is CH once per epoch (T rises to 1 at the end of the epoch, see
  `docs/figures/fig12_leach_threshold.png`).
* **Weakness:** the CH count is random (sometimes 0, sometimes 10+), CHs may be badly placed or have little energy.
* LEACH is **not** weakened in this project: it uses the same radio model, the same clustering code and the
  same packet sizes. Its election messages are counted when control packets are switched on.

---

## 3. Grey Wolf Optimizer (GWO) from zero

![GWO concept](figures/fig05_gwo_concept.png)

### 3.1 The story

Grey wolves hunt in packs with a strict social ranking:

* **Alpha (α)** — the leader; makes decisions.
* **Beta (β)** — second in command; helps the alpha.
* **Delta (δ)** — third rank (scouts, sentinels).
* **Omega (ω)** — all the other wolves; they follow the leaders.

The hunt has three phases: **search** for prey (spread out), **encircle** it, **attack** (close in). Mirjalili et
al. (2014) turned this into an optimisation algorithm: the "prey" is the best solution, which nobody knows; the
three leaders are the best solutions found so far, and the leaders' positions are used to estimate where the prey
is.

### 3.2 Translation to cluster-head selection

| Wolf world | This project |
|---|---|
| a wolf | a candidate CH set (a 0/1 vector over the alive nodes) |
| position of the wolf | which nodes are CHs in that candidate |
| the prey | the best possible CH set for this round (unknown) |
| α, β, δ | the three best **different** CH sets found so far |
| how good a position is | the fitness F (lower = better) |
| hunting for 30 iterations | the search inside one round |

### 3.3 What happens, step by step, in one round

```text
1. create 20 random wolves (valid CH sets: eligible nodes only, 2–8 CHs for 100 nodes)
2. score every wolf with the fitness function
3. α, β, δ ← the three best different wolves
4. repeat for t = 0 … 29:
     a ← 2 − 2·t/30                                     (2 → 0: explore first, exploit later)
     for every wolf and every node j:
         for each leader L in α, β, δ:  A = 2a·r1 − a,  C = 2·r2,
                                         D = |C·L_j − X_j|,  X_L = L_j − A·D
         y_j ← (X_α + X_β + X_δ) / 3
         probability that j is CH ← S(y_j) = 1 / (1 + e^(−10(y_j − 0.5)))
         x_j ← 1 with that probability, else 0
     repair every wolf (only eligible nodes; CH count inside [K_min, K_max], keeping the most likely CHs)
     score the wolves; update α, β, δ (they are only replaced by better, different sets)
5. return α  →  the CH set used in this round
```

* **Exploration and exploitation:** while a > 1, |A| can be larger than 1, so a wolf may land *beyond* or *away
  from* the leaders — it explores new CH sets. Later |A| < 1 and the wolves settle *between* the leaders — they
  exploit the best region (see `docs/figures/fig06_gwo_parameters.png`).
* **Why a sigmoid?** GWO was invented for continuous numbers; a CH set is 0/1. The sigmoid turns the continuous
  value into a probability (binary GWO, Emary et al. 2016).
* **Worked example** with real numbers: [03_MATHEMATICS.md §9](03_MATHEMATICS.md#9-gwo-equations) (a node that
  two of the three leaders choose becomes CH with 97.5 % probability).

### 3.4 Where it is in the code

| Step | Code (`algorithms/gwo.py`) |
|---|---|
| random valid wolves, scoring, leaders | `WolfPack.create`, `FitnessContext.random_solutions` |
| a(t) | `control_parameter` |
| A, C, D, X_L, average, sigmoid, sampling, repair | `WolfPack.step` |
| α, β, δ = best three **distinct** sets so far | `distinct_best`, `WolfPack.update_leaders` |
| the whole loop | `GreyWolfOptimizer.run` / `optimize` |

**Strength:** fast convergence, very few parameters. **Weakness:** all wolves follow the same three leaders, so
the pack can crowd into one region and stop improving (premature convergence).

---

## 4. Artificial Bee Colony (ABC) from zero

![ABC cycle](figures/fig07_abc_cycle.png)

### 4.1 The story

A honey-bee colony finds nectar with three kinds of bees (Karaboga, 2005):

* **Employed bees** — each one works on one known flower patch (food source) and looks around it for a better
  spot nearby.
* **Onlooker bees** — wait in the hive, watch the employed bees' dances and fly to the **best** patches more often.
* **Scout bees** — when a patch has been exhausted (no improvement for a long time), a scout abandons it and
  searches for a completely new patch at random.

### 4.2 Translation to cluster-head selection

| Bee world | This project |
|---|---|
| food source (flower patch) | a candidate CH set |
| nectar amount | quality = 1 / (1 + F) |
| looking near the patch | a small change to the CH set (neighbour move) |
| patch exhausted | not improved for more than `limit` = 10 attempts |
| colony of 20 bees | 10 employed + 10 onlookers → 10 food sources |

### 4.3 What happens, step by step, in one round

```text
1. create 10 random valid CH sets (food sources), score them; trial counters = 0
2. repeat 30 times:
     EMPLOYED PHASE   for every source x_i: make a neighbour v_i; if F(v_i) < F(x_i): x_i ← v_i, trial_i = 0
                                                                   else: trial_i += 1
     ONLOOKER PHASE   10 onlookers pick sources with probability p_i = (1/(1+F_i)) / Σ(1/(1+F_s));
                      each makes a neighbour of its source and keeps it only if better (else trial += 1)
     SCOUT PHASE      if the largest trial > 10: replace that source with a new random valid CH set
     remember the best CH set ever found
3. return the best CH set
```

**Neighbour move** (how a bee changes a CH set; discrete version of v = x + φ(x − x_k)):

* *Information sharing* (φ ≥ 0): take a random partner source x_k; swap one of my CHs that the partner does not
  have for one of the partner's CHs that I do not have.
* *Local search* (otherwise): give one CH role to one of that CH's nearest eligible neighbours.
* *Size change* (probability 0.1): add or remove one CH (staying inside [K_min, K_max]).

Probability example: sources with F = 0.20, 0.25, 0.40 get onlooker probabilities 0.355, 0.341, 0.304
([03_MATHEMATICS.md §10](03_MATHEMATICS.md#10-abc-equations)).

### 4.4 Where it is in the code

| Step | Code (`algorithms/abc.py`) |
|---|---|
| sources, trial counters, best memory | `BeeColony.create`, `_memorise` |
| neighbour move | `BeeColony.neighbours` |
| employed / onlooker / scout | `employed_phase`, `onlooker_phase` (+ `selection_probabilities`), `scout_phase` |
| one iteration, the whole loop | `iterate`, `ArtificialBeeColony.run` / `optimize` |

**Strength:** careful local improvement; scouts keep diversity. **Weakness:** each change is small and starts from
random sources, so it can take many iterations to reach the best region.

---

## 5. The proposed Hybrid GWO-ABC

![Hybrid](figures/fig08_hybrid_gwo_abc.png)

### 5.1 Why combine GWO and ABC?

| | GWO | ABC | What the other one contributes |
|---|---|---|---|
| Good at | fast, global, leader-guided moves | careful local refinement, diversity (scouts) | — |
| Weak at | crowding around the leaders; coarse moves | slow start from random sources | GWO gives ABC good starting points; ABC gives GWO refined, new leaders |

### 5.2 "What exactly did you combine?" (answer for the examiner)

> **"I run a GWO wolf pack and an ABC bee colony at the same time inside every round's optimisation, on the same
> CH-selection problem and the same fitness function. In every iteration the two populations exchange their best
> solutions in both directions: GWO's three leaders (α, β, δ) are injected into the bee colony, replacing its worst
> food sources, so the bees refine the wolves' best CH sets with their employed, onlooker and scout phases; and
> whenever the bees find a CH set better than the pack's third leader, it replaces the worst wolf and joins the
> leader set, so it steers every wolf's next move. The best solution of both populations is preserved. The hybrid
> uses half the wolves and half the bees, so it spends the same number of fitness evaluations as GWO or ABC
> alone."**

Concretely, the hybrid combines:

1. **GWO's position update** (α/β/δ-guided, a: 2 → 0, sigmoid) — global exploration;
2. **ABC's three phases** (employed, onlooker, scout) and neighbour moves — local exploitation and diversity;
3. **a two-way exchange every iteration**: GWO → ABC (elite transfer) and ABC → GWO (feedback);
4. **elite preservation**: the best CH set of either population is never lost;
5. **one shared problem definition**: encoding, eligibility, repair and fitness are identical for both parts;
6. **an equal budget**: 10 wolves + 5 food sources = 20 fitness evaluations per iteration (+1 when a scout fires),
   the same as GWO (20 wolves) or ABC (10 + 10 bees).

It is **not** "run GWO, then run ABC" (that sequential version was tested separately in the ablation study and is
worse, see 5.6), and it is **not** just a name: the code counts the exchanges and the tests check that both
directions really happen.

### 5.3 Step by step (one round)

```text
start:  10 random wolves (GWO pack) + 5 random food sources (ABC colony), all valid CH sets, all scored
repeat 30 times:
  1. GWO step         every wolf moves towards α, β, δ (as in §3)                        → global exploration
  2. GWO → ABC        α, β, δ replace the worst food sources if they are better
                      and not already in the colony                                       → elite transfer
  3. Employed bees    refine every food source (including the transferred elites)          → local search
  4. Onlooker bees    refine the most promising sources more often                         → exploitation
  5. Scout bee        replace a source not improved for > 10 tries                         → diversity
  6. ABC → GWO        if the colony's best is better than δ and not already a leader:
                      it replaces the worst wolf and joins α/β/δ                           → feedback
  7. Elite            best so far ← better of (best so far, α, colony best)
return the best CH set → used in this round
```

| Step | Code line (`algorithms/hybrid_gwo_abc.py`) |
|---|---|
| start | [`WolfPack.create`, `BeeColony.create`](../algorithms/hybrid_gwo_abc.py#L55) |
| 1 GWO step | [`pack.step(...)`](../algorithms/hybrid_gwo_abc.py#L62) |
| 2 transfer | [`colony.inject(pack.leaders[:3], ...)`](../algorithms/hybrid_gwo_abc.py#L64) |
| 3–5 bees | [`employed_phase`, `onlooker_phase`, `scout_phase`](../algorithms/hybrid_gwo_abc.py#L65) |
| 6 feedback | [`pack.absorb(colony.best, ...)`](../algorithms/hybrid_gwo_abc.py#L68) |
| 7 elite | [`_elite(...)`](../algorithms/hybrid_gwo_abc.py#L72) |

### 5.4 A real trace (not an illustration)

Round 1 of scenario S1, run 0 (seed 42, 100 nodes), recorded with the real code. "Transfers accepted" = how many
of α, β, δ entered the colony; "feedback" = the bees gave a better CH set back to the wolves.

| Iteration | GWO α | ABC best | Hybrid best | Transfers accepted | Feedback |
|---:|---:|---:|---:|---:|:-:|
| 0 (start) | 0.2386 | 0.3413 | 0.2386 | – | – |
| 1 | 0.2295 | 0.2295 | 0.2295 | 3 | yes |
| 2 | 0.2077 | 0.2077 | 0.2077 | 1 | |
| 3 | 0.1970 | 0.1970 | 0.1970 | 2 | yes |
| 8 | 0.1960 | 0.1960 | 0.1960 | 0 | yes |
| 10 | 0.1892 | 0.1892 | 0.1892 | 0 | yes |
| 13 | 0.1797 | 0.1797 | 0.1797 | 0 | yes |
| 15 | 0.1743 | 0.1743 | 0.1743 | 0 | yes |
| 17 | 0.1669 | 0.1669 | 0.1669 | 0 | yes |
| 18 | 0.1654 | 0.1654 | 0.1654 | 2 | yes |
| 26 | 0.1643 | 0.1643 | 0.1643 | 1 | yes |
| 30 (end) | 0.1643 | 0.1643 | 0.1643 | 0 | |

What it shows: at the start, the bee colony's best (0.3413) is much worse than the wolves' (0.2386). After the
first transfer the bees work on the wolves' best sets and immediately improve them (feedback in iteration 1). From
then on both populations share the best CH set, and improvements alternate between a GWO move (new α transferred
to the bees) and a bee refinement (fed back to the wolves). In total: 18 accepted transfers, 10 feedbacks, fitness
0.2386 → 0.1643 (31 % lower) with 621 fitness evaluations; the chosen CHs were nodes 20, 55, 60, 66 and 70.
Over the 20 networks of the convergence study the hybrid made on average **21.8 transfers and 8.3 feedbacks** per
round's optimisation — the exchange is real and frequent.

### 5.5 Is it better? (short answer, details in [05_RESULTS_AND_GRAPHS.md](05_RESULTS_AND_GRAPHS.md))

* **As an optimiser — yes.** On identical network states and with the same budget, the hybrid's final fitness is
  7.5 % lower than GWO's and 5.2 % lower than ABC's (fresh networks; 6.8 % and 4.7 % after 500 rounds), all
  statistically significant (`results/convergence/`).
* **Against LEACH and Random — yes** on FND, HND, throughput, PDR and energy; **no** on LND (LEACH's last node
  lives longer).
* **Against GWO and ABC alone on network lifetime — no significant difference** in the project's scenarios: all
  three optimisers find nearly equally good CH sets for the network, so the hybrid's better fitness does not turn
  into a longer lifetime there.
* **Against the base paper's DEAI-PSO — see section 6 and the results document.**
* **Cost:** about 1.2–2.3× more computing time per round than GWO or ABC (still below 50 ms).

### 5.6 Evidence that the exchange matters (ablation study)

| Variant | What it is | Final fitness (S1, 10 runs) |
|---|---|---:|
| GWO only | GWO alone | 0.2467 |
| ABC only | ABC alone | 0.2457 |
| GWO → ABC | 15 iterations GWO, then 15 iterations ABC seeded with the wolves | 0.2453 |
| ABC → GWO | the reverse order | 0.2474 |
| **Full Hybrid GWO-ABC** | two-way exchange in every iteration | **0.2439** |

The co-evolutionary hybrid reaches a significantly better fitness than both sequential combinations (+0.60 % and
+1.42 %). Network-lifetime differences between these variants are not significant (`results/ablation/report.md`).

---

## 6. The base paper's DEAI-PSO and the "Eq. 12" variants

**Base paper:** M. Haris and H. Nam, *"Enhancing Energy Efficiency in IoT-WSNs Through Optimized PSO Cluster Head
Selection"*, IEEE Access, vol. 13, 2025, doi:10.1109/ACCESS.2025.3583922 — the **existing system**.

### 6.1 How DEAI-PSO works (`algorithms/deai_pso.py`)

* **Particle Swarm Optimisation (PSO):** a swarm of 36 particles flies over the field. Each particle is a list of K
  points (x, y) — one per CH (K = 10 % of the alive nodes that are not free nodes). Each point is turned into the
  nearest node that has at least average energy and is not already used, so a particle always means K distinct
  CHs.
* **Movement:** each particle is pulled towards its own best position (Pbest) and the swarm's best (Gbest), with
  time-varying pull strengths (c_p 2.5 → 0.5, c_g 0.5 → 2.5).
* **DEAI inertia (the paper's contribution):** how much a particle keeps its old velocity depends on how far it is
  from its personal best and on how many iterations are left: ω = exp(−exp(−d·(T − k))).
* **Objective (Eq. 12):** total predicted round energy plus the spread (standard deviation) of the nodes' residual
  energy, weighted by a.
* **Three-tier network:** nodes closer than 85 m to the BS ("free nodes") send directly to the BS; control packets
  are 200 bits; the BS is at (200, 50), outside the field.

### 6.2 How we compare fairly with it

| Variant (name in the results) | Optimiser | Objective | Purpose |
|---|---|---|---|
| `DEAI-PSO` | the paper's PSO | the paper's Eq. 12 | the existing system |
| `Hybrid GWO-ABC (Eq. 12)` | **our hybrid** | the paper's Eq. 12 | **main comparison**: only the optimiser differs |
| `GWO (Eq. 12)`, `ABC (Eq. 12)` | GWO / ABC alone | Eq. 12 | does the hybridisation help? |
| `Hybrid GWO-ABC` | our hybrid | our 5-term fitness | the full proposed system |
| `DEAI-PSO + proposed fitness`, `… fixed K` | mixtures | — | attribution: which part causes a difference? |

* Same networks, seeds, radio model, packet sizes, 10 % CHs, free nodes, control packets and the same fitness
  budget per round (~620 evaluations; DEAI-PSO gets 648).
* Settings that the paper does not state were tuned **in the base paper's favour** on separate development seeds
  (the chosen setting: a = 0.8, distances in metres). The proposed method was **not** tuned. Final results use 20
  fresh networks.
* The paper's published lifetimes (up to 4,756 rounds) cannot be reproduced: with its own parameters a node can
  live at most 2,500 rounds (0.5 J / (4000 bits × 50 nJ/bit) — even with zero distance). Therefore only the
  same-simulator comparison is valid (details in `results/base_paper/README.md`).

---

## 7. All algorithms side by side

| | Random | LEACH | GWO | ABC | **Hybrid GWO-ABC** | DEAI-PSO |
|---|---|---|---|---|---|---|
| Who decides | BS | each node | BS | BS | BS | BS |
| Uses node energy | no | no | yes | yes | yes | yes |
| Uses distances | no | no | yes | yes | yes | yes |
| Number of CHs | exactly 5 % | random (≈ 5 %) | 50–150 % of 5 % | 50–150 % of 5 % | 50–150 % of 5 % | exactly 10 % |
| Search per round | none | none | 20 wolves × 30 | 20 bees × 30 | 10 wolves + 5 sources × 30 | 36 particles × 17 |
| Fitness evaluations / round | 0 | 0 | 620 | ≈ 620 | ≈ 620 | 648 |
| Objective | — | — | 5-term fitness | 5-term fitness | 5-term fitness | Eq. 12 |
| Time per round (100 nodes)* | ≈ 0 | 0.01 ms | 11.9 ms | 21.5 ms | 27.8 ms | 14.7 ms† |

\* clean sequential benchmark (`results/runtime_benchmark/report.md`), median of 5 seeds.
† measured in the base paper's scenario 1 (`results/base_paper/README.md` §8), where the hybrid on Eq. 12 takes
27.1 ms; for 200 nodes DEAI-PSO is slower (38.0 ms vs 33.4 ms).
