# Syntax-driven Information Matter

Date: 2026-07-07

Purpose: add a new axis to the virtual material: reactions are not decided only by species compatibility or terrain, but by **local syntax / motif shape**.

## Framing

Earlier information chemistry used rules like:

```text
A-B compatible
A-C toxic
AB surface attracts C
forbidden terrain repels particles
```

This experiment changes the rule type:

```text
local arrangement -> reaction law
```

The goal is not quantum verification. The goal is to evolve the virtual information material from species chemistry to shape grammar.

## Syntax rules

2D grid, base tokens A/B/C/D/E, terrain memory, stochastic motion/pump/death.

Local syntax rules:

```text
A-B-C line or C-B-A line
  -> ABC syntax fusion

A-B-C L-shape, with B at the corner
  -> B ejects / corner churn

A-B dimer parallel to C-D dimer
  -> bridge terrain / rare ABCD node

occupied 2x2 square with >=3 distinct tokens
  -> closed-loop stabilization / rare LOOP marker

empty hole surrounded by >=5 occupied neighbors and >=3 token types
  -> shell terrain / rare SHELL marker

ABC next to E
  -> stop/decompose rule

ABC next to D and E
  -> toxic stop / forbidden terrain

D-E-D line
  -> road terrain
```

## Sweep

- 30 seeds: 300-329
- 14x14 grid
- 520 steps per seed
- no success condition
- structures classified after the run

## Main outcome

The local syntax rules did not simply extend species chemistry. They created a new dominant attractor:

```text
closed-loop + shell grammar
```

Across the 30-seed sweep:

```text
hole_shell_grammar:      30/30
closed_loop_stabilizer:  30/30
ABC_line_polymer:         5/30
syntax_stop_rule:         2/30
corner_eject_grammar:     2/30
syntax_bridge_road:       0/30 under strict syntax
```

## Interpretation

The strongest syntax-driven behavior was not bridge-road continuation from the previous ecology. It was **topological closure**:

```text
2x2 occupied loops stabilize
holes surrounded by mixed tokens become shell-writing centers
loop/shell markers spread into large connected grammar bodies
```

So shape grammar did something different from compatibility chemistry:

```text
species chemistry -> reaction roads / composite families
syntax grammar    -> closed-loop + hole-shell bodies
```

## Collected structures

### 1. Seed 323: loop-shell syntax body with stop rule

```text
total population: 188
largest component: 188
types: 7
LOOP cells: 132
SHELL cells: 24
max holes: 24
closed_square_stabilize: 2568
hole_shell_write: 824
ABC_E_stop: 6
```

Event transition summary:

```text
shell -> shell: 8
shell -> loop:  1
loop  -> loop:  11
```

Interpretation: the world converged into a single large syntax body dominated by LOOP/SHELL states. This is not molecular diversity; it is grammar crystallization.

### 2. Seed 305: line polymerization absorbed into loop-shell body

```text
total population: 188
largest component: 188
LOOP cells: 126
SHELL cells: 38
line_ABC_fusion: 9
closed_square_stabilize: 2485
hole_shell_write: 814
max holes: 28
```

Interpretation: A-B-C line fusion occurred, but the long-lived structure was still captured by loop/shell syntax.

### 3. Seed 318: corner-eject grammar inside loop-shell body

```text
total population: 187
largest component: 187
LOOP cells: 129
SHELL cells: 32
L_ABC_eject_B: 10
closed_square_stabilize: 2628
hole_shell_write: 692
max holes: 30
```

Interpretation: L-shape grammar produced corner churn, but closure/shell rules dominated the final morphology.

### 4. Seed 327: strongest shell terrain cluster

```text
total population: 184
largest component: 184
LOOP cells: 119
SHELL cells: 32
hole_shell_write: 892
closed_square_stabilize: 2221
shell terrain max connected component: 15
max holes: 26
```

Interpretation: shell-writing was strong and spatially clustered, but this is still not a clean core-shell morphology. It is a shell grammar field.

## Important negative result

The strict syntax version suppressed the previous bridge-road behavior.

```text
AB-CD parallel bridge events existed only weakly.
stable bridge-road label did not appear in the 30-seed sweep.
```

This suggests bridge roads are easier when driven by reaction-written terrain and compatibility, while strict local syntax can pull the system into closure/shell attractors instead.

## Current best statement

```text
Local syntax rules can dominate species chemistry.
The first strong syntax attractor was not a molecule, road, or reaction soup.
It was a loop-shell grammar body.
```

## New layer

The new hierarchy is:

```text
species chemistry:
  what reacts with what

reaction-written terrain ecology:
  where reactions happened before

syntax-driven information matter:
  what local shape means
```

## Caution

The current grammar is too biased toward closure. Closed-square stabilization and hole-shell writing were strong enough that almost every seed became a LOOP/SHELL body.

So this result is real but not balanced.

Correct interpretation:

```text
syntax can create robust morphology,
but the first grammar over-crystallized into closure/shell dominance.
```

## Next adjustment

Run a balanced grammar sweep:

```text
weaken closed-square stabilization
make shell writing require longer persistence
strengthen line/bridge/stop grammars
track motif lifetime before creating LOOP/SHELL markers
add lineage for local motifs
```

Target structures to collect next:

```text
mobile glyphs
reproducing motifs
stable holes without global loop crystallization
boundary-only reaction bodies
syntax roads
true core-shell syntax bodies
reaction-stopping grammatical punctuation
```
