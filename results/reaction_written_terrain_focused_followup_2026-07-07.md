# Reaction-written Terrain Ecology: Focused Follow-up

Date: 2026-07-07

Purpose: take the strange survivors from the reaction-written terrain ecology and perturb them slightly, not to prove a quantum claim, but to see which virtual-material structures remain robust.

## Setup

Focused families:

- seed 123: repair-like refill candidate
- seed 120: bridge-road candidate
- seed 103: weak pulse/period candidate
- seed 125: multi-terrain / higher-order composite candidate
- seed 101: toxic pruning / high-diversity soup candidate

For each family, seven nearby parameter variants were run for 1000 steps:

```text
base
long_memory
short_memory
strong_terrain
strong_toxic
low_pump
high_pump
```

The goal was not a pass/fail test. The goal was to see what keeps reappearing.

## Robust patterns

### 1. Bridge roads were the most robust survivor

Every focused family retained bridge-road structure in all 7/7 variants.

```text
seed 123: bridge_road 7/7
seed 120: bridge_road 7/7
seed 103: bridge_road 7/7
seed 125: bridge_road 7/7
seed 101: bridge_road 7/7
```

Largest bridge-event examples:

```text
seed 103 high_pump:      bridge 33463
seed 125 high_pump:      bridge 28514
seed 123 strong_terrain: bridge 25237
seed 123 strong_toxic:   bridge 24908
seed 103 strong_toxic:   bridge 23938
```

Interpretation: once bridge terrain exists, it tends to become a reaction corridor. This is currently the most reliable reaction-written structure.

### 2. Higher-order composites were robust

All focused families kept higher-order composites in every variant.

```text
seed 123: higher_order_composites 7/7
seed 120: higher_order_composites 7/7
seed 103: higher_order_composites 7/7
seed 125: higher_order_composites 7/7
seed 101: higher_order_composites 7/7
```

Strongest quad-composite examples:

```text
seed 125 strong_toxic:   quad cells 20
seed 103 high_pump:      quad cells 19
seed 125 strong_terrain: quad cells 18
seed 125 high_pump:      quad cells 18
seed 123 strong_terrain: quad cells 17
```

Interpretation: reaction-written terrain does not merely preserve AB/ABC molecules. It often supports four-species composite phases.

### 3. Repair-like refill stayed broad, but the metric is loose

Every focused family showed self-repair-candidate events in all variants.

Top examples:

```text
seed 101 high_pump:    self_repair 20575
seed 120 high_pump:    self_repair 17676
seed 120 short_memory: self_repair 17141
seed 103 high_pump:    self_repair 16669
seed 101 base:         self_repair 16430
```

Interpretation: toxic contacts are often followed by nearby fusion/adsorption/bridge events. This supports the repair-like refill idea, but the current metric is permissive. It detects local refill after damage, not true self-repair of a named structure.

Correct phrase:

```text
repair-like refill after toxic pruning
```

not yet:

```text
true self-repair
```

### 4. Periodic / pulsed behavior appeared, but was not cleanly stable

Best periodicity scores:

```text
seed 125 low_pump:      0.690
seed 123 strong_toxic:  0.626
seed 120 base:          0.617
seed 123 low_pump:      0.555
seed 125 strong_toxic:  0.503
```

Robustness by family:

```text
seed 123: periodic_candidate 4/7
seed 120: periodic_candidate 3/7
seed 103: periodic_candidate 2/7
seed 125: periodic_candidate 5/7
seed 101: periodic_candidate 5/7
```

Interpretation: pulsed event patterns exist, especially under low pump or stronger toxic/terrain regimes, but this is not yet a clean reaction cycle.

Best phrase:

```text
terrain-mediated pulsing
```

not yet:

```text
stable oscillator
```

### 5. Forbidden bands appeared, but less robust than bridge roads

Forbidden-band labels appeared in only part of the focused variants:

```text
seed 120: forbidden_band 3/7
seed 103: forbidden_band 2/7
seed 101: forbidden_band 2/7
seed 123: forbidden_band 0/7
seed 125: forbidden_band 0/7
```

Largest forbidden terrain connected components:

```text
seed 101 strong_terrain: max forbidden cc 6
seed 120 strong_toxic:   max forbidden cc 5
seed 103 base:           max forbidden cc 5
seed 120 base:           max forbidden cc 4
seed 120 high_pump:      max forbidden cc 4
```

Interpretation: toxicity can write local exclusion zones, but it does not automatically become a clean phase-separating belt.

### 6. Shell terrain was common, but true core-shell structure is still unproven

Shell-candidate labels appeared in all focused variants, and shell terrain often accumulated strongly.

Strong shell-terrain examples:

```text
seed 101 strong_terrain: shell sum 605.15
seed 101 long_memory:    shell sum 564.73
seed 123 long_memory:    shell sum 564.55
seed 101 high_pump:      shell sum 557.81
seed 120 long_memory:    shell sum 555.70
```

Interpretation: adsorption/shell terrain is robust, but the current metric does not prove a stable core-shell morphology. It proves shell-writing activity, not a clean layered object.

## Current best hierarchy

```text
very robust:
  bridge roads
  higher-order composites
  shell-writing activity
  repair-like refill after toxic damage

moderately robust:
  terrain-mediated pulsing
  toxic pruning fields

not yet clean:
  true core-shell morphology
  true catalyst pattern A + C + B -> AB + C
  stable reaction oscillator
  named-structure self-repair
```

## Interpretation

The strongest emergent structure is not a molecule. It is a **reaction road**:

```text
bridge event -> bridge terrain -> more bridge/contact/fusion nearby -> higher-order composites
```

This suggests that reaction-written terrain can turn repeated events into spatial reaction infrastructure.

The second strongest structure is **repair-like refill**:

```text
toxic event -> local forbidden/damage terrain -> nearby adsorption/bridge/fusion refill
```

But this needs lineage tracking before calling it self-repair.

## Next exploratory move

The next run should not merely increase seed count. It should add lineage and morphology tracking:

```text
lineage tracking:
  which composite family occupied a damaged site before and after toxic pruning?

road tracking:
  do bridge terrains form continuous corridors with repeated event flow?

shell tracking:
  is shell terrain radially arranged around a persistent core product?

cycle tracking:
  do the same local regions repeatedly pass through fusion -> shell -> toxic -> refill?
```

The current best target is:

```text
reaction roads and repair-like refill as spatial infrastructure in information-material ecology
```
