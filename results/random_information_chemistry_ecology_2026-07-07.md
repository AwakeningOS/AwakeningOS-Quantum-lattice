# Random Information Chemistry Ecology

Date: 2026-07-07

Purpose: stop treating classical explanation as failure and instead let the pseudo-material evolve as a virtual material. The question was not `is this uniquely quantum?` but `what structures appear if we randomize information-chemistry rules and let the system run?`

## Core

Exploratory stochastic lattice ecology.

- 2D grid: 14x14
- base species: A/B/C/D/E
- each cell may hold a base species or composite species such as AB, CDE, ABCE
- random compatibility matrix per world
- movement biased by local compatibility and reaction terrain
- fusion creates composite patches
- toxic contact erodes/kills and writes negative terrain
- adsorption writes weak terrain without fusion
- weak drive/pump from edges
- weak death/dissipation

This run is intentionally classical-effective. It is an information-material ecology, not a quantum witness test.

## Sweep

- 80 random worlds were attempted in two parameter bands.
- 40 baseline worlds, 40 higher-complexity worlds with max composite size up to 4.
- Each world ran for 260 steps.
- No success condition was imposed. Afterward, survivors were classified by observed structure.

## What appeared

### 1. Giant mixed continent

Seed 9 produced a large connected structure:

```text
total population: 125
largest connected structure: 113
species/molecule types: 12
composite cells: 77
triple-composite cells: 49
fusion events: 74
toxic events: 3
```

Dominant products:

```text
CDE: 36
B:   22
AD:  13
CE:  12
E:   10
A:   10
```

Interpretation: a large mixed information-material continent. It did not collapse into one molecule; it maintained a chemically mixed but structured population.

### 2. High-diversity reaction soup

Seed 34 produced a high-diversity ecology:

```text
total population: 97
largest structure: 37
types: 15
composite cells: 78
triple-composite cells: 35
fusion events: 71
toxic events: 0
```

Dominant products:

```text
DE, ABD, BCE, CE, AD
```

Interpretation: no single product wins. Several molecular families coexist. This is closer to an information-chemistry soup than a droplet.

### 3. Two-family coexistence

Seed 23 produced two major molecular families:

```text
AB: 37
DE: 27
C:  24
```

The system did not produce one global composite. It separated into two main compatible families with C remaining as a background/adsorbing species.

Interpretation: information-chemical phase coexistence.

### 4. Non-reactive adsorption world

Seed 29 produced no composites at all:

```text
fusion events: 0
composite population: 0
adsorption events: 265
```

Dominant base populations remained:

```text
B, D, E, C, A
```

Interpretation: a world can have many contacts and terrain-writing events but no actual fusion. This is a stable adsorption-only regime.

### 5. Toxic sculpting / pruning worlds

Seeds 70 and 73 showed high toxic-event regimes:

```text
seed 73 toxic events: 30
seed 70 toxic events: 29
```

These worlds did not become rich composite ecologies. Toxic contacts pruned possible structures before they could grow large.

Interpretation: toxicity acts less like dramatic destruction and more like a sculpting/pruning field.

### 6. Higher-order composites

In the higher-complexity band, four-species composites appeared.

Examples:

```text
seed 53: ABDE appeared
seed 61: ABCE appeared with high population
```

Seed 61:

```text
ABCE: 31
CD:   26
ABE:  16
fusion events: 93
```

Interpretation: beyond AB/ABC molecules, the system can make higher-order composite phases. These are not automatically better; some become dominant, others coexist with lower-order species.

## Post-hoc structure classes

The random ecology produced these classes:

```text
mixed continent
reaction soup
family coexistence
adsorption-only material
toxic pruning field
higher-order composite phase
rough shell/interface candidates
```

## Important correction

No strict quantum claim is made here. This was deliberately not a quantum-witness experiment.

The result is instead:

```text
A virtual information material can develop classical-effective chemistry-like organization when compatibility, fusion, toxicity, adsorption, terrain writing, drive, and dissipation are allowed to interact.
```

## Best current interpretation

This suggests a new working layer:

```text
information material ecology
```

Below quantum-specific questions, there is a valid virtual-material question:

```text
What kinds of persistent structures appear when information-chemical compatibility rules interact with drive, dissipation, and reaction-written terrain?
```

## Next direction

Do not immediately reduce this to a verification test.

Next exploratory sweep should add:

- explicit reaction-written terrains:
  - fusion site -> attract terrain
  - rejection site -> repel terrain
  - toxic contact -> forbidden terrain
- composite statefulness:
  - AB before D rejects C
  - AB after D absorbs C
- shell rules:
  - core product attracts shell species but rejects fusion
- true catalyst trials:
  - A + C + B -> AB + C
- longer runs with survival-based collection rather than success criteria

The next run should collect strange survivors rather than prove a hypothesis.
