# Membrane-like Information Matter

Date: 2026-07-07

Purpose: treat the strong loop/shell attractor not as a nuisance to weaken, but as a candidate membrane. The question is whether a closed information structure can create an inside/outside distinction and selective exchange.

## Correction from previous syntax run

The previous syntax-driven sweep produced a dominant `closed-loop + shell grammar body`. The first reaction was to say the closure rule was too strong. That was the wrong framing.

Correct framing:

```text
road  -> moves reactions through space
shell -> creates an inside
```

So the next question is:

```text
Can loop/shell act as a membrane-like information material?
```

## Pilot stress test

This was a small mechanistic pilot, not a broad ecology sweep.

- 2D grid: 40x32
- pre-existing loop/shell ring used as a membrane candidate
- exterior pump: A/B/C/D particles
- inside catalyst X converts A -> P
- shell interactions:
  - A: preferred permeating nutrient
  - B: mostly blocked inert particle
  - C: absorbed as repair/shell reinforcement
  - D: toxic shell-damaging particle
- variants:
  - no_shell
  - nonselective shell
  - selective shell
  - damage_repair shell
  - road_connected shell
  - growth_like shell

10 seeds per variant, 300 steps.

## Main metrics

`selectivity` means approximate internal useful-load ratio:

```text
(A_inside + P_inside + 1) / (B_inside + D_inside + 1)
```

The metric uses the original shell interior region as the comparison region. Enclosed-area topology was also tracked separately.

## Results table

| mode | selectivity | integrity final | A pass | B pass | D pass | repair / C absorbed | shell breach | P inside | growth buds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| no_shell | 1.20 | 0.00 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 5.39 | 0.0 |
| nonselective | 1.02 | 0.98 | 18.4 | 46.7 | 0.0 | 28.6 | 0.7 | 3.89 | 0.0 |
| selective | 2.16 | 0.97 | 46.7 | 8.4 | 0.0 | 29.4 | 1.9 | 4.61 | 0.0 |
| damage_repair | 2.04 | 0.84 | 42.7 | 7.6 | 0.0 | 29.8 | 9.0 | 5.36 | 0.0 |
| road_connected | 2.53 | 0.93 | 62.5 | 6.0 | 0.0 | 21.6 | 3.5 | 4.53 | 0.0 |
| growth_like | 2.48 | 0.95 | 55.2 | 6.0 | 0.0 | 30.7 | 3.8 | 5.39 | 8.4 |

## What worked

### 1. Selective membrane function appeared

The nonselective shell was almost not selective:

```text
selectivity = 1.02
A pass = 18.4
B pass = 46.7
```

The selective shell changed the exchange pattern:

```text
selectivity = 2.16
A pass = 46.7
B pass = 8.4
D pass = 0.0
```

Interpretation: the shell can act as a selective boundary when its local syntax is tied to pass/block/repair/damage operations.

### 2. Shell as protected inside/outside separator is plausible but fragile

Selective shells maintained high membrane integrity:

```text
selective integrity final = 0.97
road-connected integrity final = 0.93
growth-like integrity final = 0.95
```

But topological enclosure was fragile under damage. In the damage-repair case, cell-level integrity partly recovered, but the enclosed area often failed to remain topologically closed.

Interpretation: local shell repair is easier than global compartment repair.

### 3. Shell + road connection improved selective intake

Road-connected shell increased A entry and kept B low:

```text
A pass = 62.5
B pass = 6.0
selectivity = 2.53
```

Interpretation: the two previous structures can couple:

```text
bridge/road -> feeds shell
shell -> filters road input
```

This is a strong next direction.

### 4. Toxic particles became membrane stressors rather than normal entrants

D did not pass the shell in the pilot:

```text
D pass = 0.0 across shell variants
```

Instead it damaged the shell and produced breaches.

Interpretation: toxicity becomes a membrane stress channel, not merely a species interaction.

### 5. Growth-like budding appeared, but not clean division

The growth-like variant produced shell bud events:

```text
growth buds = 8.4 average
```

But the morphology did not become clean division. It is only a budding/growth hint.

## What did not yet work

### 1. True core-shell morphology is still not proven

The system can write and maintain shell cells, and it can filter exchange, but a clean stable core/shell/outer-shell morphology was not yet demonstrated.

### 2. Damage repair is incomplete

The damage-repair variant showed repair events and a mean repair-time signal around 25 steps, but the final topological enclosure often failed.

Correct phrase:

```text
local membrane repair
```

not yet:

```text
global compartment self-repair
```

### 3. Internal chemistry was not dramatically amplified

Internal product P did not explode simply because a shell existed. Selectivity improved, but productivity depends on pump/road/catalyst tuning.

## Current best statement

```text
Loop/shell syntax can be interpreted as the beginning of membrane-like information matter.
It can separate inside/outside and selectively filter exchange.
But robust compartment maintenance, clean core-shell morphology, and shell division are not established yet.
```

## New hierarchy

```text
reaction road:
  spatial infrastructure for flow

loop/shell body:
  closure and potential container

membrane-like information matter:
  selective boundary + internal environment + repair stress
```

## Next experiment target

Do not weaken closure. Instead, make membrane function more explicit and measure it:

```text
1. Shell pore syntax
   specific local motifs open/close selective pores

2. Shell repair topology
   repair must restore connected enclosure, not just local cells

3. Road-shell coupling
   reaction road feeds a shell gate

4. Internal/external chemistry split
   same species outside and inside should undergo different reactions

5. Shell fission/budding
   growth should produce two enclosed compartments or a persistent bud
```

Best next phrase:

```text
information membrane and internal environment
```
