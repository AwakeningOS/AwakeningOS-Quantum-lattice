# Reaction-written Terrain Ecology

Date: 2026-07-07

Purpose: explore a virtual information-material ecology where reactions do not merely transform molecules; they also write the environment, and the written environment biases later reactions.

## Framing

This run intentionally does **not** ask whether the behavior is uniquely quantum. It treats the pseudo-material as a classical-effective information material and asks:

```text
If reactions write terrain, what structures survive?
```

## Core

- 2D grid: 16x16
- base species: A/B/C/D/E
- composite species allowed up to 4 components
- random compatibility matrix per seed
- edge pump / weak death / movement
- reaction-written terrains:
  - fusion -> attract terrain
  - reject/bypass -> repel terrain
  - toxic contact -> forbidden terrain
  - adsorption -> shell terrain
  - bridge contact -> bridge terrain
- terrains decay and weakly diffuse
- no success condition was imposed

## Sweep

- 30 seeds: 100-129
- 800 steps each
- structures were classified after the run

## Major structures collected

### 1. Reaction-written multi-terrain world: seed 125

```text
total population: 33
types: 16
composite cells: 16
triple composites: 12
quad composites: 9
largest component: 6
fusion: 490
adsorb: 477
bridge: 581
toxic: 28
self-repair candidates: 11
```

Labels:

```text
toxic_pruning
higher_order_composites
forbidden_band
shell_candidate
reaction_nest
bridge_road
self_repair_candidate
```

Dominant products:

```text
A: 6
D: 4
E: 4
ABCD: 3
BCDE: 2
B: 2
ACD: 2
ABDE: 2
```

Interpretation: this was the best all-in-one ecology. Fusion, bridge, adsorption, toxicity, and higher-order composites coexisted. It looked less like one molecule and more like a reaction landscape containing several local reaction fields.

### 2. Periodic / pulsed reaction candidate: seed 103

```text
total population: 27
types: 12
fusion: 321
adsorb: 1398
bridge: 1871
toxic: 182
self-repair candidates: 90
periodicity score: 0.456
```

Labels:

```text
toxic_pruning
forbidden_band
self_repair_candidate
periodic_candidate
```

Interpretation: not a clean oscillator, but event windows showed a weak repeated pulse pattern. The dominant cycle is closer to terrain-mediated alternation than to a designed clock.

### 3. Strong self-repair candidate: seed 123

```text
total population: 24
types: 11
fusion: 394
adsorb: 1088
bridge: 1436
toxic: 176
self-repair candidates: 117
```

Labels:

```text
toxic_pruning
shell_candidate
bridge_road
self_repair_candidate
```

Interpretation: toxic contacts were often followed nearby by fusion/adsorption/bridge events. This suggests a crude repair-like pattern: damage writes forbidden terrain, but the surrounding reaction field continues filling/rewiring nearby sites.

### 4. Bridge-road world: seed 120

```text
total population: 22
types: 11
fusion: 526
adsorb: 1597
bridge: 3033
toxic: 0
quad composites: 8
periodicity score: 0.431
```

Labels:

```text
higher_order_composites
bridge_road
```

Interpretation: bridge contacts dominated without toxic pruning. This is a mostly constructive world where bridge terrain acted like a reaction corridor for higher-order composites.

### 5. Toxic pruning / high-diversity soup: seed 101

```text
total population: 23
types: 13
fusion: 500
toxic: 52
adsorb: 534
bridge: 415
self-repair candidates: 18
```

Labels:

```text
reaction_soup
toxic_pruning
higher_order_composites
forbidden_band
shell_candidate
bridge_road
self_repair_candidate
```

Interpretation: a noisy but rich world. Toxicity did not simply end the system; it pruned some paths while fusion and adsorption continued elsewhere.

## What appeared

The reaction-written terrain ecology produced:

```text
reaction nests
bridge roads
forbidden bands
shell-like adsorption regions
higher-order composite phases
toxic pruning fields
repair-like refill after toxic damage
weak periodic/pulsed event patterns
```

## Important observation

The most important change from the previous random ecology is that reaction history became spatially active:

```text
reaction event -> terrain
terrain -> later movement/contact/fusion/rejection
later reaction -> new terrain
```

This made the environment into a memory layer rather than a passive background.

## Interpretation

This is still not a claim of life, agency, or quantum specificity. The current best description is:

```text
reaction-written information-material ecology
```

The interesting behavior is that the pseudo-material can create local reaction fields out of its own event history.

## Next collection targets

- cleaner reaction roads
- clear forbidden belts that divide phases
- core-shell structures that persist for long runs
- true catalyst-like pattern: A + C + B -> AB + C
- stronger self-repair: toxic gap later filled by a consistent species/family
- stable cycles: fusion -> adsorption -> toxic pruning -> fusion
- moving reaction fronts

## Note

The classifications are post-hoc. They are not success claims. The purpose is to collect strange survivors first, then isolate/reproduce the interesting ones later.
