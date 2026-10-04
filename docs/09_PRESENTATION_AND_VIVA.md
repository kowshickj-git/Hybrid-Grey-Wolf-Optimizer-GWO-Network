# 9. Presentation and viva preparation

All numbers are measured results from `results/` (see [05_RESULTS_AND_GRAPHS.md](05_RESULTS_AND_GRAPHS.md)).
Learn the **short answers** by heart; use the explanations when the examiner asks "why?" or "how?".

Contents: [30–60 s explanation](#1-the-3060-second-explanation-memorise-this) ·
[Technical explanation](#2-technical-explanation-for-a-professor-23-minutes) · [Demo plan](#3-demonstration-plan-10-minutes) ·
[Slide outline](#4-slide-outline) · [Basic questions](#5-basic-questions) · [Intermediate questions](#6-intermediate-questions) ·
[Difficult questions](#7-difficult-questions-that-challenge-the-project) · [Limitations and future scope](#8-limitations-and-future-scope) ·
[Final conclusion](#9-final-conclusion)

---

## 1. The 30–60 second explanation (memorise this)

> "Wireless sensor networks are made of small battery-powered sensors that send their data to a base station.
> To save energy, the sensors are grouped into clusters, and in every round one node per cluster — the cluster
> head — collects the data and forwards it. Being a cluster head costs about twenty times more energy than being a
> normal sensor, so choosing the right cluster heads decides how long the network lives.
>
> My project selects the cluster heads with a hybrid of two nature-inspired optimisers: the Grey Wolf Optimizer,
> which searches globally by following the three best solutions, and the Artificial Bee Colony, which refines
> solutions locally. The two run together and exchange their best solutions in every iteration. A fitness function
> scores each choice by energy, distances and cluster balance.
>
> I built the whole simulation in Python and compared the method fairly with random selection, LEACH, GWO, ABC and
> the method of my base paper on the same networks. The hybrid is the best optimiser, keeps all nodes alive about
> 25 to 37 percent longer than LEACH, and on the base paper's own problem it beats the base paper's method on
> 18 of 24 measurements, with every claim checked statistically."

## 2. Technical explanation (for a professor, 2–3 minutes)

1. **System model.** N nodes uniformly deployed (100 in 100 m × 100 m by default), 0.5 J each, one BS; first-order
   radio model (E_elec 50 nJ/bit, ε_fs 10 pJ/bit/m², ε_mp 0.0013 pJ/bit/m⁴, d0 ≈ 87.7 m, E_DA 5 nJ/bit); one
   4000-bit reading per alive node per round; single-hop member → CH → BS with aggregation at the CH. Node death at
   0 J; packets of a CH that dies mid-round are lost.
2. **Problem.** Every round, choose the CH set among the alive nodes — about 2 × 10¹¹ possibilities for 100 nodes —
   centrally at the BS.
3. **Objective.** A minimised five-term fitness, each term normalised to [0, 1]: energy (CH residual energy and
   predicted round consumption, w = 0.30), member → CH distance (0.25), CH → BS distance (0.20), cluster-size
   imbalance (0.15), deviation from the target CH count (0.10), plus a penalty of 10 for infeasible sets. CH
   candidates must have at least the mean residual energy (LEACH-C rule).
4. **Proposed optimiser.** A co-evolutionary Hybrid GWO-ABC: a binary GWO pack (sigmoid transfer, a: 2 → 0) and a
   discrete ABC colony (employed/onlooker/scout, neighbour moves by information sharing and local search) run in
   the same loop; each iteration GWO's α, β, δ replace the worst food sources, and the colony's best replaces the
   worst wolf when it beats δ; elitism keeps the global best. Half the wolves and half the bees give the same
   evaluation budget as GWO or ABC alone (≈ 620 per round).
5. **Evaluation.** Paired runs (20 seeds in the main scenario), five scenarios, ablation, one-factor sensitivity,
   convergence and runtime studies; Wilcoxon signed-rank tests with Holm correction and Cliff's δ.
6. **Results.** All optimisers beat Random and LEACH on FND (+25–37 % vs LEACH), HND, throughput, PDR and energy;
   LEACH keeps a later LND because its drain is uneven. The hybrid reaches a 4.7–7.5 % better fitness than GWO and
   ABC, but lifetime is statistically equal to theirs in the BS-centre scenarios. On the base paper's problem and
   objective, the hybrid beats DEAI-PSO in 18 of 24 tests (HND +3.0–7.4 %, throughput +2.2–7.2 %); FND is not
   better; most of the gain comes from adapting the CH count.

## 3. Demonstration plan (10 minutes)

| Time | Show | Say |
|---|---|---|
| 1 min | `docs/figures/fig01_wsn_architecture.png` | the problem: sensors → CHs → BS, CHs cost 21× more |
| 2 min | GUI: `python main.py`, choose *Hybrid GWO-ABC*, **Run**, then **Pause** | live network: CHs change every round, energy shading, nodes dying; the dashboard numbers |
| 1 min | `docs/figures/fig08_hybrid_gwo_abc.png` | what exactly is combined (two-way exchange) |
| 2 min | `results/scenarios/S1_100nodes/result_table.md`, `09_alive_vs_rounds.png`, `18_lifetime_fnd_hnd_lnd.png` | main comparison and lifetime |
| 1 min | `11_residual_energy_vs_rounds.png` | energy efficiency |
| 1 min | `results/convergence/conv_all_round0.png` | the hybrid is the best optimiser |
| 1 min | `results/base_paper/fig_improvement_vs_base_paper.png` | improvement over the base paper, with the honest exceptions |
| 1 min | `python -m pytest` (or its saved result) and `reproducibility_check_run0.csv` | it is tested and reproducible |

## 4. Slide outline

1. Title, name, guide.
2. Problem: energy in WSNs; why CH selection matters (fig 01, fig 03).
3. Base paper and its limitation (DEAI-PSO, fixed 10 % CHs, PSO only).
4. Objective of the project.
5. System model: network, radio model, round (fig 02).
6. Fitness function (fig 04).
7. GWO and ABC in one slide each (figs 05, 07).
8. Proposed Hybrid GWO-ABC (fig 08) — "what is combined".
9. Experimental set-up: algorithms, scenarios, 20 paired runs, statistics, MATLAB → Python note.
10. Results: S1 table + alive-nodes graph + lifetime bars.
11. Results: convergence + energy.
12. Results: improvement over the base paper (bar chart) + attribution.
13. Limitations and future work.
14. Conclusion.

---

## 5. Basic questions

**B1. What is a Wireless Sensor Network?**
* *Short answer:* Many small battery-powered sensors that measure something and send the data wirelessly to a base
  station.
* *Simple explanation:* like many weather volunteers with walkie-talkies reporting to one office.
* *Technical:* nodes with sensing, processing and radio units; energy-constrained, usually not rechargeable;
  here 100–300 nodes in a square field with one BS.

**B2. What is inside a sensor node?**
* *Short answer:* a sensor, a small processor, a radio and a battery.
* *Technical:* the program models what matters for energy: position, residual energy, alive/dead status, CH role,
  cluster membership and packet counters (`models/node.py`).

**B3. What is the Base Station?**
* *Short answer:* the collection point that receives all data; it is mains-powered.
* *Technical:* its energy is not modelled; the centralised algorithms (GWO, ABC, Hybrid, DEAI-PSO) run at the BS.

**B4. Why is energy efficiency important?**
* *Short answer:* batteries cannot be replaced, so saving energy directly extends the network's life.
* *Simple explanation:* when the batteries are empty the area is no longer monitored.
* *Technical:* radio communication dominates consumption; transmit energy grows with d² or d⁴, so the topology
  (who sends to whom) determines the lifetime.

**B5. What is clustering?**
* *Short answer:* grouping nearby nodes so they send to a local leader instead of each sending to the far BS.
* *Technical:* replaces N long transmissions by N − K short ones plus K long ones per round, with aggregation.

**B6. What is a cluster head and what does it do?**
* *Short answer:* the cluster leader: it receives its members' packets, aggregates them and sends one packet to the
  BS.
* *Technical:* its cost per round is n·(E_rx + E_DA) + E_DA + E_tx(k, d_CH,BS) — about 4.46 mJ for 19 members at
  40 m from the BS, versus 0.216 mJ for a member at 20 m.

**B7. Why must the CH role rotate?**
* *Short answer:* because a CH spends about 21 times more energy; a permanent CH would die very quickly.
* *Technical:* rotation spreads the load; the optimisers additionally restrict CHs to nodes with at least average
  energy.

**B8. What is LEACH?**
* *Short answer:* the classic clustering protocol: each node becomes CH at random with a probability that rotates
  the role.
* *Technical:* T(n) = p / (1 − p·(r mod 1/p)) for nodes not yet CH in the current epoch; distributed, no energy or
  position information, random CH count.

**B9. What is optimisation and why do you need it?**
* *Short answer:* searching for the best choice according to a score; there are about 2 × 10¹¹ possible CH sets,
  too many to check.
* *Technical:* CH selection is a combinatorial problem solved every round; metaheuristics find near-optimal sets
  with about 620 evaluations.

**B10. What is GWO?**
* *Short answer:* an optimiser inspired by grey wolves: candidate solutions move towards the three best ones
  (alpha, beta, delta).
* *Technical:* X_L = L − A·|C·L − X| for each leader, new position = average; a decreases from 2 to 0 to move from
  exploration to exploitation (Mirjalili et al., 2014).

**B11. What are alpha, beta, delta and omega?**
* *Short answer:* alpha, beta and delta are the three best solutions found so far; all others are omega wolves that
  follow them.
* *Technical:* in this project they are the three best **different** CH sets found so far (elitist).

**B12. What is ABC?**
* *Short answer:* an optimiser inspired by honey bees: bees improve good food sources (solutions) and abandon
  exhausted ones.
* *Technical:* employed, onlooker and scout phases; greedy selection; trial counter with limit 10 (Karaboga, 2005).

**B13. What do the employed, onlooker and scout bees do?**
* *Short answer:* employed bees improve their own source, onlookers improve the best sources more often, scouts
  replace sources that stopped improving.
* *Technical:* onlooker probability p_i = (1/(1+F_i)) / Σ(1/(1+F_s)); scout if trial > limit.

**B14. What is your proposed method?**
* *Short answer:* a Hybrid GWO-ABC that selects cluster heads; GWO explores globally, ABC refines locally, and they
  exchange their best solutions every iteration.
* *Technical:* see question I9.

**B15. What is a fitness function?**
* *Short answer:* the score of a CH set; here lower is better.
* *Technical:* F = 0.30·energy + 0.25·member→CH distance + 0.20·CH→BS distance + 0.15·imbalance + 0.10·count
  deviation (+10 if infeasible), each term in [0, 1].

**B16. What are FND, HND and LND?**
* *Short answer:* the rounds in which the first node, half of the nodes and the last node died.
* *Technical:* FND = min death round; HND = ⌈N/2⌉-th death; LND = max death round. In S1: Hybrid
  1,128 / 1,138 / 1,158, LEACH 892 / 1,104 / 1,287.

**B17. What is residual energy?**
* *Short answer:* the total energy left in all nodes at a given round (here round 500).
* *Technical:* S1 at round 500: Hybrid 28.10 J of 50 J, LEACH 27.40 J.

**B18. What are throughput and PDR?**
* *Short answer:* throughput = how many readings reached the BS in total; PDR = delivered ÷ generated.
* *Technical:* S1: Hybrid 113,662 readings, PDR 0.9982; LEACH 108,883, PDR 0.9892.

**B19. Which language did you use? Do you need MATLAB?**
* *Short answer:* Python 3 with NumPy, pandas, Matplotlib and SciPy. MATLAB is not needed anywhere.
* *Technical:* see question I20 and [06_MATLAB_TO_PYTHON.md](06_MATLAB_TO_PYTHON.md).

**B20. What is one simulation round?**
* *Short answer:* choose CHs → form clusters → every alive node sends one reading → subtract energy → mark dead
  nodes → record.

---

## 6. Intermediate questions

**I1. Explain the radio energy model.**
* *Short answer:* sending k bits over d metres costs E_elec·k + ε_fs·k·d² below d0 and E_elec·k + ε_mp·k·d⁴ above;
  receiving costs E_elec·k; aggregation costs E_DA·k.
* *Simple explanation:* talking near is cheap, shouting far is very expensive.
* *Technical:* d0 = √(ε_fs/ε_mp) ≈ 87.7 m; 4000 bits over 20 m = 0.216 mJ, over 150 m = 2.833 mJ.

**I2. What is d0 and why does it matter?**
* *Short answer:* the crossover distance (87.7 m) where the amplifier cost changes from d² to d⁴.
* *Technical:* when the BS is far (S5, base-paper scenarios), CH → BS links are in the d⁴ region, so the number and
  position of CHs matter much more.

**I3. Explain your fitness function and why these factors.**
* *Short answer:* five normalised terms — energy, member→CH distance, CH→BS distance, cluster balance, CH count —
  weighted 0.30/0.25/0.20/0.15/0.10, plus a penalty for infeasible sets.
* *Simple explanation:* choose rich, central, well-spread CHs with similar-sized clusters.
* *Technical:* each factor addresses a failure mode (low-energy CHs, long member links, long CH→BS links, overloaded
  CHs, wrong CH count); the ablation and sensitivity studies measure their effects (worked example in
  [03_MATHEMATICS.md §7](03_MATHEMATICS.md#7-the-fitness-function)).

**I4. Why is lower fitness better, and what about invalid solutions?**
* *Short answer:* every term is a cost; invalid sets (no CH, wrong count, a CH that cannot afford its work) get
  +10, so they always lose.

**I5. How is a CH solution represented?**
* *Short answer:* a 0/1 vector over the alive nodes; 1 = cluster head.
* *Technical:* a repair step keeps only eligible nodes (energy ≥ mean) and clips the number of CHs to
  [K_min, K_max] = K_opt·(1 ± 0.5); dead nodes are not in the vector.

**I6. GWO is continuous — how did you use it for a 0/1 problem?**
* *Short answer:* binary GWO: the continuous position is turned into a probability with a sigmoid, then into 0/1.
* *Technical:* S(y) = 1/(1 + e^(−10(y − 0.5))); bit = 1 with probability S(y); repair keeps the highest-S nodes
  (Emary et al., 2016).

**I7. Explain a and A in GWO.**
* *Short answer:* a falls from 2 to 0; A = 2a·r1 − a. |A| > 1 lets wolves move away (exploration), |A| < 1 pulls
  them towards the leaders (exploitation).

**I8. How does ABC create a new solution?**
* *Short answer:* by a small change: swap a CH with a partner's CH, move a CH role to a nearby node, or add/remove
  one CH.
* *Technical:* a discrete analogue of v = x + φ(x − x_k); the new set is kept only if its fitness is better.

**I9. What exactly did you combine? (most important question)**
* *Short answer:* "A GWO wolf pack and an ABC bee colony run together on the same CH-selection problem; in every
  iteration GWO's three best solutions are injected into the bee colony, the bees refine them, and the bees' best
  solution is fed back into the wolf pack as a new leader. The best of both is kept. The budget is the same as
  for GWO or ABC alone."
* *Simple explanation:* wolves find good areas fast, bees polish them, and each tells the other about its best
  find every iteration.
* *Technical:* steps: (1) GWO position update, (2) α/β/δ replace the worst food sources if better and not
  duplicates, (3–5) employed, onlooker, scout phases, (6) if the colony's best beats δ it replaces the worst wolf
  and enters the leader set, (7) elitism. 10 wolves + 5 food sources = 20 evaluations per iteration. In a real
  trace there were 18 transfers and 10 feedbacks in one round's 30 iterations (on average 21.8 and 8.3). The
  code is `algorithms/hybrid_gwo_abc.py`; tests verify both directions.

**I10. Why should the hybrid perform better than GWO or ABC alone?**
* *Short answer:* because each covers the other's weakness: GWO gives ABC good starting points, ABC gives GWO
  refined new leaders, so the search does not stagnate.
* *Technical:* confirmed at the optimisation level: 7.5 % lower fitness than GWO and 5.2 % lower than ABC on fresh
  networks (6.8 % and 4.7 % after 500 rounds), p < 0.01, same budget. At the network level the lifetime gain over
  GWO/ABC is not significant in the BS-centre scenarios (see D1).

**I11. How did you make the comparison fair?**
* *Short answer:* same networks (seeds), same radio model, packets, rounds, clustering code and the same number of
  fitness evaluations for every optimiser; the base paper's method was even tuned in its own favour.

**I12. Why 20 runs, and what are paired runs?**
* *Short answer:* run r of every algorithm uses the same random network (seed 42 + r), so differences come from
  the algorithm, not from luck; 20 runs give reliable means and tests.
* *Technical:* with 20 pairs the Wilcoxon test can detect consistent differences (minimum p ≈ 2 × 10⁻⁶); with 5 the
  smallest possible p is 0.0625.

**I13. Which statistical test did you use and why?**
* *Short answer:* the paired Wilcoxon signed-rank test with Holm correction, plus Cliff's δ as effect size.
* *Technical:* non-parametric (no normality assumption), uses the pairing; Holm controls the family-wise error;
  differences < 1 % are flagged as practically negligible.

**I14. What is the CH eligibility rule and why did you add it?**
* *Short answer:* optimisers may only choose nodes with at least the average energy.
* *Technical:* a pilot run showed that without it the CH→BS distance term re-elected nodes near the BS until they
  died early (FND 533–617 vs 887 for LEACH). The rule (as in LEACH-C) applies to all optimisers equally and is
  disclosed; switching it off cuts FND by ≈ 42 % but raises LND by ≈ 12 %.

**I15. How are clusters formed and how do nodes die?**
* *Short answer:* every alive non-CH node joins its nearest CH; a node with 0 J is dead forever.
* *Technical:* a node that cannot afford an operation spends what it has, its packet is lost, and it is marked dead
  at the end of the round; a CH that dies while receiving loses its cluster's data (counted in PDR).

**I16. What happens when the network size changes?**
* *Short answer:* more nodes share the CH duty, so lifetime increases a little; the hybrid stays ahead of LEACH on
  FND; computation grows.
* *Technical:* Hybrid FND 1,080 / 1,130 / 1,155 / 1,163 for 50 / 100 / 150 / 200 nodes (LEACH 954 / 884 / 913 /
  931); S3 (300 nodes): Hybrid FND 1,173 vs LEACH 940 (+24.9 %). Runtime per round 27.8 / 35.9 / 45.8 ms for 100 /
  200 / 300 nodes.

**I17. What happens when the initial energy changes?**
* *Short answer:* lifetime scales roughly in proportion to the energy; the ranking stays the same.
* *Technical:* 0.25 J: Hybrid FND 563 vs LEACH 417; 1.0 J: every node of the optimisers survives the 2000-round
  horizon (LEACH FND 1,829).

**I18. What happens if the BS position changes?**
* *Short answer:* the farther the BS, the shorter the lifetime and the larger the advantage of the optimisers over
  LEACH.
* *Technical:* Hybrid FND 1,130 (centre) / 1,118 (edge) / 1,050 (50, 150) in the sensitivity runs; scenario S5 (BS at
  (50, 175)): FND 963 vs LEACH 703 (+37 %), because CH → BS links enter the d⁴ region and CH placement matters more.

**I19. What happens if the optimisation parameters change?**
* *Short answer:* population, colony size and iterations barely change the lifetime; the CH percentage and the
  fitness weights matter more.
* *Technical:* GWO population 10–40, ABC colony 10–40 and 10–50 iterations change the hybrid's mean FND/HND by at
  most a few rounds (FND 1,128–1,131) while runtime grows with the budget; CH percentage 3 % → 10 % raises FND
  1,067 → 1,184; energy-heavy weights give the best FND (1,136), distance-heavy the best LND (1,196).

**I20. Why did you replace MATLAB with Python? Would MATLAB give the same results?**
* *Short answer:* only the tool changed, not the model: Python is free, reproducible and has equivalent numerical
  libraries. MATLAB would not give bit-identical numbers (different random-number generators), but the conclusions,
  based on 20 paired runs and significance tests, would be expected to hold.
* *Technical:* see [06_MATLAB_TO_PYTHON.md](06_MATLAB_TO_PYTHON.md); the base paper itself used MATLAB R2023a and
  was re-implemented in Python for a same-simulator comparison.

---

## 7. Difficult questions that challenge the project

**D1. Your hybrid is not better than GWO or ABC in network lifetime. What is your contribution then?**
* *Short answer:* the hybrid is the better optimiser (4.7–7.5 % better fitness at equal cost), and on the base
  paper's problem it improves the existing system significantly; in the simple BS-centre scenarios all three
  optimisers already find nearly equally good CH sets, so the better fitness does not become a longer lifetime
  there. I report this honestly.
* *Technical:* under the eligibility rule and the energy term, GWO and ABC are already near the best achievable
  lifetime in S1–S5; the hybrid's extra fitness comes mostly from cluster balance, which the ablation shows costs a
  little energy; and per-round optimisation is myopic (a better score this round is not a better long-term plan).

**D2. LEACH has a later Last Node Death. Isn't your method worse?**
* *Short answer:* it is a trade-off: my method keeps **all** nodes alive 25–37 % longer (FND) and delivers more
  data; LEACH lets some nodes die very early and a few survive longer.
* *Technical:* the optimisers drain energy evenly (LND − FND ≈ 31 rounds for the hybrid vs 395 for LEACH in S1).
  For applications that need full coverage, FND/HND matter more than LND.

**D3. How can I trust that your results are not fabricated?**
* *Short answer:* every number is produced by the code from saved seeds and can be regenerated with one command;
  run 0 of every experiment was re-simulated and is identical; 93 automatic tests check the model.
* *Technical:* `config.json` + `experiment.json` (seeds, versions) in each folder; `python main.py reproduce
  <folder>`; `reproducibility_check_run0.csv`; the reports state losses as well as gains.

**D4. Did you tune parameters until your method won?**
* *Short answer:* no. The proposed method uses the documented defaults in every experiment and was never tuned on
  test seeds; the only tuning was done **for the base paper's method**, in its favour, on separate seeds.

**D5. The base paper reports FND 1,700 and LND 4,178; you get about 630 and 700. Did you implement it wrongly?**
* *Short answer:* the paper's published numbers are physically impossible with its own parameters: a 0.5 J node can
  send at most 2,500 packets of 4000 bits (0.2 mJ each just for the electronics), so no node can live 3,400–4,756
  rounds. That is why I compare both methods in the same simulator.
* *Technical:* with the BS at (200, 50), CH → BS links of 100–200 m are in the d⁴ regime and 200-bit control packets
  are sent every round, which explains lifetimes of ~600–1,500 rounds in our simulator.

**D6. How do you know your DEAI-PSO re-implementation is faithful?**
* *Short answer:* it follows the paper's equations (velocity, time-varying coefficients, the double-exponential
  inertia, Eq. 12), its Table 3 parameters and its three-tier model; Eq. 12 is unit-tested against a hand
  calculation; unspecified details were tuned in its favour.

**D7. Isn't it unfair that your hybrid may choose the number of CHs while DEAI-PSO uses exactly 10 %?**
* *Short answer:* it is part of the proposed design and it is disclosed and measured: with the CH count fixed at
  10 % the hybrid still beats DEAI-PSO (node-rounds +0.44 %, FND +0.77 %, p < 0.001), so most of the gain comes from
  the adaptive count and a smaller part from the better search.

**D8. The paper used 5000 iterations. Didn't you weaken DEAI-PSO by giving it fewer?**
* *Short answer:* every method received the same budget per round (about 620 fitness evaluations; DEAI-PSO 648), so
  differences reflect the methods, not the effort; this is the standard way to compare optimisers fairly.

**D9. Why didn't FND improve against the base paper (and even got 1.2 % worse in BP3)?**
* *Short answer:* FND is decided by the single weakest node; the base paper's Eq. 12 objective does not protect the
  weakest node explicitly. Using fewer CHs saves energy overall but each CH serves more members. I report FND
  honestly as "not improved".

**D10. Some of your "significant" differences are 0.05 %. Are they meaningful?**
* *Short answer:* statistically real but practically negligible — the reports flag every difference below 1 % as
  practically negligible, and I do not claim them as improvements.

**D11. The hybrid is slower. Is it practical?**
* *Short answer:* yes: about 28–46 ms per round on a laptop for 100–300 nodes, done once per round at a mains-powered
  BS.
* *Technical:* 1.2–2.3× GWO/ABC at the same number of fitness evaluations (two populations, more operators); for 200
  nodes it is even faster than DEAI-PSO (33.4 vs 38.0 ms).

**D12. Aren't your fitness weights arbitrary?**
* *Short answer:* they are a documented starting point, not proven optima; the sensitivity analysis tests five
  weight presets and reports their effect, and every algorithm is scored with the same weights.

**D13. The channel is ideal — no collisions or retransmissions. Is that realistic?**
* *Short answer:* it is the standard assumption of the LEACH literature and applied equally to all algorithms, so
  the comparison is fair; absolute lifetimes in a real network would be lower. It is listed as a limitation.

**D14. Real networks use multi-hop routing. Why single hop?**
* *Short answer:* single-hop member → CH → BS is the model of LEACH and of the base paper's data-transmission
  section; multi-hop is future work.

**D15. Isn't the eligibility rule an unfair advantage over LEACH?**
* *Short answer:* it uses information LEACH does not have (global energy knowledge at the BS), exactly like LEACH-C
  and the base paper's PSO-C rule; it is a property of centralised CH selection, it is disclosed, and its effect is
  measured.

**D16. What is the computational complexity?**
* *Short answer:* per round O(T · P · K · N) for the optimisers (T iterations, P candidates, K CHs, N nodes); about
  620 fitness evaluations per round; LEACH is O(N).

**D17. Why not exhaustive search or an exact solver?**
* *Short answer:* ~2 × 10¹¹ CH sets per round for 100 nodes; checking them all would take days per round.
  Metaheuristics give near-optimal sets in milliseconds.

**D18. How do you prove the hybrid is a real combination, not just a name?**
* *Short answer:* the code counts the exchanges (on average 21.8 transfers and 8.3 feedbacks per round), the tests
  check both directions, and the ablation shows the two-way hybrid beats running GWO then ABC (or the reverse).

**D19. Your multi-objective hybrid had an earlier FND than DEAI-PSO in BP1 and BP3. Why?**
* *Short answer:* the project's energy term divides the round energy by a worst-case bound; when the BS is
  100–200 m away, that bound is huge, so real d⁴ energy differences barely change the score. The base paper's Eq. 12
  measures Joules directly. It is a lesson for future fitness design, and I report it.

**D20. Are the results general, or only true for seed 42?**
* *Short answer:* each result is the mean of 10–20 different random networks, tested statistically, across five
  scenarios and ten sensitivity factors; the main conclusions hold in all of them.

**D20b. Why include a Random baseline, and why does Random beat LEACH on some metrics?**
* *Short answer:* Random shows what CH selection without any intelligence achieves; the hybrid beats it on FND by
  39.8 % and on HND, throughput, energy and PDR. Random beats LEACH on HND, LND and energy because it always uses
  exactly 5 CHs, while LEACH's CH count jumps from round to round; LEACH's rotation only protects the first death
  (FND 892 vs 807).
* *Technical:* LEACH's per-round CH count has a standard deviation of 2.2 (rounds with 0 or 10+ CHs cost energy);
  Random's is 0. This is a measured result, reported as it is.

**D21. How did you validate the simulator itself?**
* *Short answer:* automated tests check the energy formulas exactly, that energy only decreases through
  communication, that dead nodes never participate, that clusters use the nearest CH, that every algorithm returns
  valid CHs, and that results reproduce exactly.

---

## 8. Limitations and future scope

**Limitations (say them before the examiner does):**
* single-hop topology, ideal channel (no collisions/retransmissions), one packet per node per round;
* uniform random deployments and homogeneous initial energy;
* fitness weights and the eligibility rule are design choices (their effects are measured);
* per-round (myopic) optimisation: a better score in one round is not always a better long-term plan;
* the hybrid's lifetime advantage over GWO/ABC is not significant in the BS-centre scenarios;
* DEAI-PSO is a re-implementation; the paper's published numbers cannot be reproduced (physical bound);
* runtimes are pure Python on one laptop.

**Future scope:**
* a fitness designed for lifetime (multi-round look-ahead, residual-energy variance, Joule-based energy term as in
  Eq. 12);
* multi-hop CH → CH → BS routing, realistic MAC/channel models, mobile or multiple base stations;
* heterogeneous energy and clustered deployments;
* adaptive weights or parameter self-tuning; other hybrids (e.g., with PSO or WOA);
* hardware testbed or a network simulator (ns-3, OMNeT++) for validation.

## 9. Final conclusion

> "The project shows that optimised, energy-aware cluster-head selection extends the stable life of a wireless
> sensor network substantially compared with conventional LEACH — about 25–37 % later first node death — and
> delivers more data with less energy. The proposed Hybrid GWO-ABC is a genuine co-evolutionary combination that
> finds better cluster-head sets than GWO or ABC alone with the same effort. In the simple scenarios this does not
> translate into a longer lifetime than GWO or ABC, which I report honestly. On the base paper's own problem and
> objective, it improves on the existing DEAI-PSO system in 18 of 24 statistically tested measurements — half-node
> lifetime, throughput and energy — while the first node death is not improved. All results are produced by a
> reproducible Python simulation, tested automatically, and do not depend on MATLAB."
