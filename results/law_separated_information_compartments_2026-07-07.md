# Law-separated Information Compartments

Date: 2026-07-07

Purpose: move beyond membrane as filter. Test whether a shell can create a region where the same species have different meanings inside and outside.

## Core question

The membrane is not only useful because it protects or filters. The stronger question is:

```text
Can the inside run a different information-physics law from the outside?
```

In this pilot, the outside and inside use the same species A/B/C/D/E, but different local rules.

## Law split

Outside law:

```text
A+B: mostly neutral contact
C: toxic / pruning
D: road/adsorption writer
```

Inside law:

```text
A+B: strong fusion into AB / higher composites
C: catalyst that helps AB become P
D: repair material near shell damage
P: internal product that may export and write road terrain
```

This means the same token can change meaning depending on whether it is outside or inside the shell.

## Pilot modes

8 seeds per mode.

```text
membrane_same_law:
  membrane exists, but inside and outside laws are not meaningfully separated

inside_law:
  inside and outside laws are different

inside_feedback:
  internal P changes membrane permeability

nested_shell:
  internal P/E activity can create a second inner shell
```

## Results table

| mode | selectivity | shell integrity | A pass | B pass | C pass | internal AB fusion | internal C catalysis | external C toxic | P export / road | inner shell cells |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| membrane_same_law | 2.30 | 0.75 | 77.4 | 41.9 | 44.3 | 0.0 | 0.0 | 1303.9 | 0.0 | 0.0 |
| inside_law | 6.63 | 0.75 | 166.1 | 7.5 | 75.4 | 23.6 | 5.6 | 1300.0 | 5.8 | 0.0 |
| inside_feedback | 5.69 | 0.78 | 195.5 | 5.0 | 32.8 | 21.4 | 2.9 | 1319.4 | 3.1 | 0.0 |
| nested_shell | 6.03 | 0.80 | 172.9 | 3.9 | 79.3 | 17.5 | 4.5 | 1296.3 | 5.0 | 5.9 |

## What appeared

### 1. Inside/outside law separation worked

In the same-law membrane, there was no internal AB fusion or internal C catalysis:

```text
internal AB fusion = 0.0
internal C catalysis = 0.0
```

With inside-law separation:

```text
internal AB fusion = 23.6
internal C catalysis = 5.6
```

Outside C remained toxic at roughly the same scale:

```text
external C toxic ≈ 1300 events
```

Interpretation: the same token C behaved as a toxic pruning species outside, but as a catalytic helper inside.

### 2. The shell became a meaning boundary

The membrane did not merely select input. It changed the interpretation of symbols after entry:

```text
outside A+B: contact without fusion
inside A+B: fusion/composite formation
outside C: toxic
inside C: catalytic
inside D: repair-like material
```

This is the most important result of the pilot.

### 3. Internal product exported weakly and wrote outside terrain

Inside-law modes produced P and exported a small amount:

```text
inside_law P export / road = 5.8
inside_feedback P export / road = 3.1
nested_shell P export / road = 5.0
```

Interpretation: internal chemistry can write back to the outside, but the effect is still weak.

Correct phrase:

```text
weak inside-to-outside terrain writing
```

not yet:

```text
strong external control by internal state
```

### 4. Internal feedback was present but not cleanly closed-loop yet

The feedback mode made membrane permeability depend on internal P:

```text
P high -> A closes down, C opens up
```

However, P levels were modest in this pilot, so the feedback loop did not become a strong oscillatory regulator. It improved selectivity and kept B low, but did not yet produce a clean homeostatic cycle.

Correct phrase:

```text
weak internal-state-dependent membrane tuning
```

not yet:

```text
self-regulating compartment
```

### 5. Inner membrane formation appeared as a weak nested-compartment hint

The nested-shell mode produced inner shell cells:

```text
inner shell cells = 5.9 average
inner integrity ≈ 0.33
```

This is not a complete inner compartment. But it is a first hint that internal chemistry can start writing a second boundary.

Correct phrase:

```text
partial inner-shell nucleation
```

not yet:

```text
stable nested compartment
```

## Current best statement

```text
The membrane can act as a law boundary.
The same token can have different reaction meaning inside and outside.
This turns shell from a filter into a meaning-transforming compartment.
```

## Hierarchy update

```text
reaction road:
  flow infrastructure

membrane-like information matter:
  selective boundary

law-separated information compartment:
  inside and outside obey different local laws
```

## What is still missing

```text
strong internal product control of membrane permeability
stable nested inner membrane
clear inside/outside chemical divergence over long time
exported P rewriting external road networks at scale
self-regulating internal cycle
```

## Next collection target

Do not return to pore-checklists. The next collection target should be:

```text
inside product controls membrane and terrain
```

Specifically:

```text
P accumulation closes A pores and opens C/D repair pores
P export writes external road to attract/repel future particles
internal P drop reopens A pores
```

The desired survivor is not just a membrane. It is an information compartment whose inner state changes how the outside couples to it.
