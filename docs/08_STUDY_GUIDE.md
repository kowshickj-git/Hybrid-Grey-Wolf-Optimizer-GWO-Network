# IF I KNOW NOTHING ABOUT THIS PROJECT, STUDY IN THIS ORDER

23 small steps. Each step has a short explanation, a picture or example, one sentence to **remember**, and a
**check yourself** question (answer below it). Do them in order; each step uses the previous ones. When a step
links to another document, the link is for later — you can understand the step without it.

---

### Step 1 — What is a sensor?

A sensor is a small electronic device that **measures** something — temperature, humidity, smoke, vibration — and
can **send** the measurement by radio. It runs on a small battery that usually cannot be replaced.

```text
   [ sensor ]  measures 24 °C  →  ((( radio )))  →  sends "24 °C"
   battery: 0.5 J
```

**Remember:** a sensor node = measure + send + small battery.
**Check yourself:** why is the battery a problem? → *Because every radio message uses energy and the battery cannot
be recharged; when it is empty, the sensor stops working.*

### Step 2 — What is a Wireless Sensor Network (WSN)?

Many sensors spread over an area (a farm, a forest, a factory) that send their measurements wirelessly to one
collection point. Together they watch the whole area.

**Remember:** WSN = many battery sensors + wireless + one collection point.
**Check yourself:** in this project, how many sensors and how large an area? → *100 sensors in 100 m × 100 m by
default (also 160, 200 and 300 sensors in other tests).*

### Step 3 — What is a Base Station (BS)?

The collection point that receives all data and passes it to people (a computer, the internet). It is plugged into
the mains, so its energy is unlimited.

**Remember:** the BS only receives and never runs out of energy.
**Check yourself:** where is the BS? → *At the centre (50, 50) by default; also on the edge, outside the field, and
at (200, 50) in the base paper's tests.*

![architecture](figures/fig01_wsn_architecture.png)

### Step 4 — What is energy consumption?

Every radio action costs energy: **sending** (more over longer distances), **receiving**, and **combining**
packets. Sending far is very expensive: 20 m costs 0.216 mJ, 150 m costs 2.833 mJ (13 times more).

**Remember:** distance is expensive — short hops save energy.
**Check yourself:** why not let every sensor send directly to a far BS? → *Each one would pay the expensive long
distance every round and the network would die quickly.*

### Step 5 — What is a cluster?

A group of nearby sensors that send their data to one local leader instead of each sending to the far BS.

```text
   ●  ●            ●  ●
     ▲   ← cluster   ▲      ▲ = cluster head, ● = member
   ●  ●            ●
```

**Remember:** cluster = neighbours that share one leader.
**Check yourself:** how does a sensor know which cluster to join? → *It joins the nearest cluster head.*

### Step 6 — What is a Cluster Head (CH)?

The leader of a cluster. It **receives** its members' packets, **combines** them with its own into one packet, and
**sends** that one packet to the BS.

**Remember:** CH = collect + combine + forward.
**Check yourself:** who pays more energy, a member or a CH? → *The CH — about 21 times more in a typical cluster
(4.464 mJ vs 0.216 mJ per round).*

### Step 7 — Why Cluster Heads are required

Without clusters, 100 sensors make 100 long trips to the BS every round. With 5 clusters: 95 short trips to the
CHs + 5 long trips to the BS. Far less energy in total.

But because the CH job is expensive, it must **move to other nodes** every round, and it should go to nodes that
can afford it (enough energy, good position).

**Remember:** clusters save energy; the CH job must rotate and be given to the right nodes.
**Check yourself:** what happens if the same node is CH every round? → *Its battery empties quickly and it dies
early.*

### Step 8 — Why optimisation is required

Choosing the CHs well is hard: with 100 nodes there are about **200 billion** possible CH sets. We cannot try them
all every round. Optimisation = a smart search that finds a very good set quickly (here: by checking about 620
candidate sets per round).

**Remember:** too many choices → we need a smart search, not a full check.
**Check yourself:** what does the smart search need in order to compare two CH sets? → *A score: the fitness
function (step 12).*

### Step 9 — What is GWO?

**Grey Wolf Optimizer.** Imagine 20 wolves hunting. Each wolf is one guess of the CH set. The three best guesses
lead the pack — **alpha, beta, delta**; all other wolves (**omega**) move towards them. Early moves are big
(exploring), later moves are small (closing in on the prey = the best CH set).

![GWO](figures/fig05_gwo_concept.png)

**Remember:** GWO = follow the three best leaders; big steps first, small steps later.
**Check yourself:** what is a "wolf" in this project? → *A candidate list of cluster heads.*

### Step 10 — What is ABC?

**Artificial Bee Colony.** Each *food source* is a guess of the CH set. **Employed bees** try small changes to
their source and keep improvements; **onlooker bees** visit the best sources more often; a **scout bee** throws
away a source that stopped improving and tries a random new one.

**Remember:** ABC = improve good guesses in small steps; abandon dead ends.
**Check yourself:** which bee keeps the search from getting stuck? → *The scout bee.*

### Step 11 — Why combine GWO and ABC?

GWO finds good regions fast but its wolves crowd around the leaders. ABC improves carefully but starts from random
guesses. In the **Hybrid GWO-ABC** they work at the same time and **swap their best guesses every iteration**:
the wolves' three leaders go to the bees, the bees polish them, and a better polished guess goes back to the
wolves as a new leader. It uses half the wolves and half the bees, so the total effort is the same as GWO or ABC
alone.

![hybrid](figures/fig08_hybrid_gwo_abc.png)

**Remember:** wolves explore, bees polish, and they exchange their best solutions every iteration.
**Check yourself:** what exactly is exchanged? → *GWO → ABC: alpha, beta, delta replace the worst food sources;
ABC → GWO: the bees' best replaces the worst wolf and becomes a leader if it beats delta.*

### Step 12 — What is the fitness function?

A score for a CH set; **lower is better**. It adds five parts, each between 0 and 1:

| Part | Weight | Asks |
|---|---:|---|
| energy | 0.30 | do the CHs have plenty of energy, and is this round cheap? |
| member → CH distance | 0.25 | are members close to their CH? |
| CH → BS distance | 0.20 | are the CHs close to the BS? |
| cluster balance | 0.15 | are the clusters of similar size? |
| CH count | 0.10 | is the number of CHs near the target (5 %)? |

An impossible set (no CH, too many/few CHs, a CH that cannot afford its work) gets +10.

![fitness](figures/fig04_fitness_example.png)

**Remember:** fitness = weighted score of energy, distances, balance and count; lower wins.
**Check yourself:** in the picture, why does choice A win? → *One CH per group: short member links and equal
clusters (F = 0.2495 vs 0.4919).*

### Step 13 — How the simulation works

The program builds a virtual network (positions, batteries, BS), then repeats rounds until all nodes are dead.
It does this for every algorithm on the **same** networks, then compares them.

![flowchart](figures/fig02_simulation_flowchart.png)

**Remember:** set up once → repeat rounds → measure → compare.
**Check yourself:** why use the same networks for every algorithm? → *So that only the algorithm differs — a fair
comparison.*

### Step 14 — What one simulation round means

One round = one cycle of the network's work:

```text
choose CHs → form clusters → every alive node sends one reading → subtract energy → mark dead nodes → record
```

**Remember:** one round = one "report cycle"; lifetime is counted in rounds.
**Check yourself:** how many rounds does the default network live? → *About 1,100–1,300 rounds until the last node
dies.*

### Step 15 — How Cluster Heads are selected

Each algorithm has its own rule (the only thing that differs between them):

* **Random:** 5 random alive nodes.
* **LEACH:** each node rolls a die; the chance rises during a 20-round cycle so that everybody serves once.
* **GWO / ABC / Hybrid:** search ~620 candidate sets with the fitness function and use the best; only nodes with at
  least average energy may be chosen.
* **DEAI-PSO** (base paper): a particle swarm searches CH positions with its own score (Eq. 12).

**Remember:** same network, same rules for everything else — only the CH choice differs.
**Check yourself:** which algorithms use node energy when choosing? → *GWO, ABC, Hybrid, DEAI-PSO (not Random,
not LEACH).*

### Step 16 — How data transmission is simulated

Members send their 4000-bit reading to their CH; each CH receives them, combines them with its own reading and
sends one packet to the BS. A packet counts as **delivered** only when it reaches the BS.

**Remember:** member → CH → BS; delivered = arrived at the BS.
**Check yourself:** when is data lost? → *When a CH runs out of energy before forwarding, or a node dies while
sending.*

### Step 17 — How energy is consumed

The program uses the standard *first-order radio model*: sending = electronics + amplifier (grows with distance²,
or distance⁴ beyond 87.7 m); receiving = electronics; combining = a little processing. Each cost is subtracted from
the node's battery.

![energy](figures/fig03_energy_model.png)

**Remember:** send costs depend on distance; receive costs do not.
**Check yourself:** why is 150 m so much more expensive than 20 m? → *Beyond 87.7 m the cost grows with d⁴.*

### Step 18 — How nodes die

When a node's battery reaches 0 J it becomes **DEAD**. The round number is stored. A dead node is never chosen,
clustered or used again.

**Remember:** 0 J = dead forever.
**Check yourself:** what does a node do if it cannot afford a send? → *It spends what it has left, the packet is
lost, and it is marked dead at the end of the round.*

### Step 19 — How network lifetime is measured

![lifetime](figures/fig10_lifetime_metrics.png)

* **FND** — round when the **first** node died (end of full coverage);
* **HND** — round when **half** of the nodes were dead;
* **LND** — round when the **last** node died;
* **node-rounds** — the area under the "alive nodes" curve.

**Remember:** FND / HND / LND = first / half / last death; higher is better.
**Check yourself:** in the picture, which method has the later FND and which the later LND? → *Hybrid: later FND
(1,132 vs 887). LEACH: later LND (1,297 vs 1,160).*

### Step 20 — How results are generated

After all runs, the program calculates every metric for every run, the averages and spreads, the statistical
tests, then writes CSV files, graphs (PNG) and a `report.md` into a folder under `results\`. Nothing is typed in by
hand.

**Remember:** results = automatic output of the simulation (CSV + PNG + report).
**Check yourself:** which file contains the final table? → *`result_table.md` (and `.csv`) in the experiment
folder.*

### Step 21 — How to read the graphs

For every graph ask: what is on the X-axis (usually the round), what is on the Y-axis (alive nodes, energy,
packets…), which line is which algorithm (legend), and is "higher" or "lower" better? Then compare the lines at the
same round. [05_RESULTS_AND_GRAPHS.md](05_RESULTS_AND_GRAPHS.md) does this for every important graph.

**Remember:** axes → legend → better direction → compare at the same round.
**Check yourself:** in "residual energy vs rounds", is a higher line better? → *Yes — more energy left at the same
round.*

### Step 22 — How to compare the algorithms

1. Same 20 networks for every algorithm (paired runs).
2. Mean ± standard deviation over the 20 runs.
3. Improvement % = how much better the proposed method is (positive = better).
4. Wilcoxon test + Holm correction: is the difference **real** (p < 0.05) or luck?
5. Differences below 1 % are called *practically negligible* even when real.

**Remember:** a difference counts only if it is significant, and is called important only if it is large enough.
**Check yourself:** the hybrid's FND vs GWO is +0.12 %, not significant. Can you claim an improvement? → *No.*

### Step 23 — What the final conclusion means

In plain words (all numbers are measured; details in [05_RESULTS_AND_GRAPHS.md](05_RESULTS_AND_GRAPHS.md)):

1. **Optimised CH selection works.** In every scenario, the Hybrid GWO-ABC (and also GWO and ABC) keeps all nodes
   alive much longer than LEACH (first node death 25–37 % later), delivers more data and spends less energy.
   Random selection is the worst for the first node death (807 rounds in S1; the hybrid lasts 40 % longer).
   LEACH's and Random's last node survives longer, because they drain nodes unevenly.
2. **The hybrid is the best optimiser.** With the same effort it finds CH sets with a 4.7–7.5 % better fitness than
   GWO or ABC alone. In the project's own scenarios this does **not** give a significantly longer network lifetime
   than GWO or ABC — all three already find nearly equally good CH sets there.
3. **The hybrid improves on the base paper.** On the base paper's own problem and objective, replacing its
   DEAI-PSO optimiser with the Hybrid GWO-ABC gives significantly better results in 18 of 24 paired comparisons
   (half-node death +3–7 %, throughput +2–7 %, energy left at round 300 +1.3–5.5 %). The first node does not die later
   (not significant in two scenarios, 1.2 % earlier in the 200-node scenario). Most of the gain comes from the
   hybrid choosing fewer, better cluster heads per round.
4. **The price:** more computation per round (about 28 ms instead of 12–22 ms for 100 nodes), which a base station
   can easily afford.

**Remember:** better than the conventional protocol and better than the base paper's optimiser on most metrics;
the best optimiser of the three; honest about where it is not better.
**Check yourself:** name one metric where the proposed method is *not* better. → *LND against LEACH; FND against
DEAI-PSO; lifetime against GWO/ABC in the BS-centre scenarios.*

---

When you can answer every "check yourself" question, continue with [02_CONCEPTS.md](02_CONCEPTS.md) (details),
[04_ALGORITHMS.md](04_ALGORITHMS.md) (algorithms) and [09_PRESENTATION_AND_VIVA.md](09_PRESENTATION_AND_VIVA.md)
(presentation and viva).
