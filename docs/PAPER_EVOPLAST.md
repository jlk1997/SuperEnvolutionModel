# Evolving Plasticity: The Baldwin Effect and Learning Acceleration in Language Models

Draft. The language-model census is registered and not yet run. Numbers below are from the reference organism unless a sentence says otherwise. Do not cite them as language-model results.

Target venues: ICML 2027 (stretch, late January 2027) and NeurIPS 2027 (main, May 2027).

## Abstract

Deployed language models are frozen after training. We study a different object: not the weights, but the rules that change the weights during deployment. A genome of 56 numbers specifies which layers, which projections, and which timescale may be written, and how fast. Evolution searches that genome. Within a life the model learns from verified outcomes. Across generations only the genome is inherited, unless a Lamarckian control copies practiced skills into the birth prior.

The claim has three parts. Learning speed on families the model has never seen increases over a life (acceleration ratio above 1). That speed survives a change of base (heritability). A population selected on post-learning performance shows the Baldwin pattern: post-learning fitness rises more than birth fitness, and frequent families become innate faster than rare ones.

We demonstrate the selection pressure on a deterministic reference organism, where fitness noise cannot fake the result. On that organism, evolution strategies raise held-out acceleration from the in-context baseline of 1 to the measurement cap, and the plasticity map concentrates on the site the task stream actually uses. The language-model experiment is specified, powered, and not yet executed.

## 1. What "evolution" is

Three orders, plus an open-ended consequence:

1. Competence. Families already seen get better. Continual fine-tuning does this. It is not the claim.
2. Acceleration. Let `N_t(f)` be the number of verified interactions a model needs to reach a fixed competence on a family `f` that is new at time `t`. Acceleration is `AR = N(first) / N(later)`. A learner that does not transfer sits near 1.
3. Heritability. `h = (AR_transferred - AR_floor) / (AR_source - AR_floor)`. The genome, not a checkpoint, is what moves to the new base.

Birth fitness is performance before within-life learning. Post fitness is performance after it. The Baldwin prediction is that selection on post fitness raises post fitness more than birth fitness. Genetic assimilation is the further prediction that birth success rises for families that dominate the lifetime, and not for families that barely appear. Lamarckian inheritance writes the practiced skill into the offspring genome directly. Darwinian selection scores the birth state and never learns during the evaluation.

## 2. Related work

The positioning table is in `docs/LITERATURE.md`. The nearest neighbors, and the reason they are not this paper:

- Self-edits and self-generated data (SEAL, Absolute Zero, STaR, ReST) change what is trained on. They do not evolve the learning rule, and they do not measure acceleration on held-out families.
- Fast weights and test-time training (TTT, Titans, Nested Learning, Gated DeltaNet) put a fixed learning rule in the architecture. We treat DeltaNet state as one gene, a carry bit, not as the contribution.
- Agent self-modification (Darwin Gödel Machine, AlphaEvolve, Voyager) evolves code or a skill library outside the weights.
- Evolution strategies at billion-parameter scale (Qiu et al., 2025) and evolutionary model merging search weights or merge coefficients offline. We search a 56-dimensional learning rule, online, under a lifetime fitness.
- Evolved plasticity and online meta-learning (Miconi; Najarro and Risi; OML; ANML) are the algorithmic ancestors. They were not run on a pretrained language model with an executor-graded tool stream, and they did not separate Baldwin, Lamarck, and Darwin inheritance.

Hinton and Nowlan (1987) showed that learning can smooth a fitness landscape so that evolution finds an innate solution. Waddington's genetic assimilation is the same idea read along the time axis of the environment: traits that must be learned in every generation become congenital when the environment is stable. Complementary learning systems (McClelland et al., 1995) are the pattern we hope the plasticity map rediscovers, a fast state and a slow weight, rather than a pattern we hard-code as the only legal write.

## 3. Method

### Genome

Four layer groups (early, mid, late, last), three sites (attention, DeltaNet, MLP), three timescales (fast, mid, slow): 36 learning-rate genes. Four task clusters each have an allocation gene and an innate gene. Twelve memory genes gate carry, decay, consolidation, replay, a KL anchor, the number of successes before a write, birth scale, per-timescale mix, a surprise gate, and a forgetting penalty. The last layer group carries three quarters of a site's expressed plasticity, so one coordinate can move a site. A flat average across four groups washed the signal out in early runs.

### Within a life

The reference organism's competence on a family is birth prior plus cluster skill plus family skill plus a fast state. Mid-timescale updates write the family. Slow-timescale updates write the cluster, which is what the next family in that cluster inherits. The fast state is keyed by family and dies with it. This is the in-context baseline when the slow and mid genes are shut off. A forgetting gene decays skills the current family is not using.

The language-model life uses the same genome to set per-site AdamW rates. A batch smaller than 8 is raised to 8. A non-positive temperature is replaced with 0.7. Correct samples from the model are the update. If none are correct, the executor's target is used and labeled `verifier`, not `on_policy`. The carry gene decides whether the DeltaNet cache is kept across episodes. Rates under `1e-4` skip that site.

### Across generations

OpenAI-ES with antithetic Gaussian noise and centered ranks, and a diagonal CMA-ES as a second optimizer. Fitness for the strategy is learning-curve area minus birth competence, minus a small cost on sites the stream does not use. Subtracting birth competence matters: without it, the strategy raises the innate gene and the acceleration ratio collapses because every family is solved before learning. Every individual in a search shares one task seed.

The inheritance comparison is a truncation GA, because Lamarckian copy is not an ES gradient. Baldwin children inherit the genome only. Darwin children are selected on birth performance and do not learn during the evaluation. Lamarck children inherit the genome after practiced cluster skill is written into the innate genes.

### Tasks

All three domains are graded by a program.

- A fictional tool DSL. Twelve training families and 32 held-out families, four clusters. Held-out families use a disjoint primitive list. Some of them use a branch template the training families never show. Tool names are random syllables.
- Reasoning Gym when the package is installed, otherwise a builtin set of equations, modular arithmetic, and counting tasks with the same grade.
- Office work. The four development packs are training families. Sealed packs are not imported. Eight synthetic industries, names that do not appear in the sealed files, supply 32 held-out families.

### Metrics and the pre-registered language-model test

`AR` is capped at 50 so a later family that is competent on arrival does not produce an infinity. The evolution index is the negative slope of log samples-to-competence across successive families. Forgetting is the drop in durable competence on an anchor family after a distractor block. Power is a paired bootstrap of "later families beat the first." At success rates 0.75 versus 0.45, 30 families have power about 0.60 and 60 families about 0.88 (80 simulations). The language-model paper is registered at 60 held-out families, 3 seeds, paired intervals, equal interaction budgets across baselines.

Baselines, matched on evaluations: a frozen base with in-context carry only; the hand-set genome; the weak genome the search starts from; random search with the same number of fitness calls; Lamarck and Darwin inheritance.

## 4. Reference organism

Command: `python -m evo plast --stage all`, seed 0. The organism is not a language model. Trajectories are a function of the genome.

Within-life learning exists. The hand-set genome starts at 0.126 and reaches 1.0 within 20 episodes, crossing 0.6 at episode 2.

The genome matters more than noise. A strong genome's learning-curve area is 0.690. The same genome measured twice differs by 0. A weak genome scores 0.018.

Evolution strategies, 14 generations, 16 antithetic pairs, 448 evaluations, one shared task seed. Mean fitness moves from 0.157 to 0.425. Held-out samples-to-competence on five text families are 3, 1, 0, 0, 0. `AR` hits the cap of 50 and the evolution index is 0.43. The in-context baseline needs 2 episodes on every family (`AR` 1.0). The weak genome's `AR` is 8. Random search with the same budget has median 0.149 and best 0.292, both below the evolved mean. The plasticity map on this text stream is delta 0.433, attention 0.298, MLP 0.294. The stream's primary site is delta. Attention and MLP are the ones the fitness charges a cost for using.

Baldwin, Lamarck, and Darwin, population 16, 14 generations, same seed. Baldwin post-learning area moves from 0.324 to 0.918. Balanced birth competence moves from 0.115 to 0.349. The post-learning gain is larger. Birth competence on the frequent cluster moves from 0.112 to 0.569, and on the rare cluster from 0.110 to 0.446. Lamarck writes the frequent cluster into offspring at 0.676, above Baldwin's 0.569. Darwin, on this seed, drops the rare cluster's birth competence to 0.003 while raising the frequent cluster to 0.702, and its post-learning area is 0.784.

Across seeds 0, 1, and 2 at 12 generations, three comparisons held: the post-learning gain exceeded the balanced-birth gain; frequent birth exceeded rare birth by more than 0.1; Lamarck's inherited frequent birth exceeded Baldwin's. Darwin's deletion of the rare gene did not hold on every seed, so it is not a claim.

Heritability of the evolved genome from a 0.6 gain base to a 1.0 gain base is 1.0. Both bases hit the `AR` cap of 50, and the weak genome on the target base has `AR` 8. The cap means this number says the genome was not lost in the transfer. It does not say the larger base accelerated further. A language-model transfer that also saturates will be reported the same way, not as a stronger result.

## 5. Language-model experiment

Not run. The runner is `actor: model` on the M0 config, then the same ES on DSL families graded by the executor, with the office and reasoning streams as further held-out domains. Stop-loss: if a hand-set learner does not move from below 0.2 to at least 0.6 within 20 episodes, switch the base to Qwen3.5-2B or 4B, or recalibrate difficulty until the first episode lands between 0.1 and 0.4. The gate does not move.

**Engineering note (Epoch A-2):** The language-model M0 reproduce command is `python -m evo plast --stage m0 --config configs/evoplast_fit.yaml`. Judge success by `m0.model.passed` / `m0.lm_passed`, not by the reference-organism field `m0.passed` alone. The gate stays at 0.6; see `docs/RUNTIME.md`.


What the paper will claim only if those runs clear their intervals:

- H1. Evolved `AR` above 1 with an interval that excludes 1, and above the in-context and hand-set baselines.
- H2. Post-learning fitness rises across generations by more than birth fitness.
- H3. Birth success on high-frequency families rises more than on low-frequency families.
- H4. The plasticity map is stable across seeds and matches the sites the stream uses.
- H5. A genome evolved on one base keeps at least half of its acceleration on the next base.

## 6. What this draft does not say

It does not say a language model has shown the Baldwin effect. It does not say the reference organism's cap of 50 is a measured ratio of 50; later families were competent on arrival, and the metric caps there. It does not say evolution strategies for fine-tuning large models are new. It does not say DeltaNet is a new architecture. The frozen engineering around the earlier office loop, the studio, the fleet, and the procedure templates, is not part of the claim.

**Stack curriculum note (Epoch A eng.):** Affine second skills achieve birth &lt; 0.5 on Qwen2.5-1.5B, but MLP-only LoRA did not reach report ≥ 0.6 in the registered budget. Treat stack as open engineering; addition M0 is the cleared within-life LM gate. Do not lower 0.6.

