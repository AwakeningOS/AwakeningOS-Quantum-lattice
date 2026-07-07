# Quantum Measurement Terrain Feedback Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_measurement_terrain_feedback_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_measurement_terrain_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv
```

## Purpose

This experiment tests whether a quantum measurement-boundary signal can be written into terrain and later modulate classical-effective reactor dynamics.

It follows the prior CHSH readout transport result:

```text
CHSH/noncommutative readout can exceed the Bell/local classical ceiling and reach transported P_release.
```

This run asks whether that signal can be inscribed into terrain, then affect the next phase.

## Design

Two phases:

```text
Phase 1: measurement/write phase, t = 0..399
Phase 2: terrain-read phase, t = 400..799
```

During Phase 1:

```text
CHSH_excess = max(0, S_CHSH - 2) / (2*sqrt(2) - 2)
measurement_terrain_write = 0.04 * CHSH_excess
```

During Phase 2:

```text
measurement terrain write is off
terrain is read by classical-effective road feedback
next-phase P_release is measured
```

The key false-positive guard is:

```text
S_CHSH <= 2 -> measurement_terrain_write = 0
```

Therefore classical/local correlations cannot create the measurement terrain bonus.

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_TERRAIN_FEEDBACK
```

## Prediction check

### P1 gamma=1 null

Prediction:

```text
gamma=1 has CHSH_excess = 0 and no terrain feedback in all scenarios
```

Result: PASS.

| scenario | gamma | max CHSH phase1 | measurement terrain write | terrain delta | next release dev |
|---|---:|---:|---:|---:|---:|
| normal_context | 1.0 | 0.000000 | 0.000000 | 0.000000 | 0.000000% |
| stress_context | 1.0 | 0.000000 | 0.000000 | 0.000000 | 0.000000% |
| storage_context | 1.0 | 0.000000 | 0.000000 | 0.000000 | 0.000000% |

### P3 main

Prediction:

```text
stress_context at low gamma has CHSH_excess > 0, terrain_delta > 0, and next-phase P_release > Arm2
```

Result: PASS.

Stress context:

| gamma | max CHSH phase1 | measurement terrain write | terrain delta end phase1 | next release dev vs Arm2 |
|---:|---:|---:|---:|---:|
| 0.25 | 2.121320 | 1.657104 | 0.385016 | +5.446770% |
| 0.0 | 2.828427 | 13.184364 | 2.646051 | +21.389922% |

### P4 gamma sensitivity

Prediction:

```text
stress_context effect is destroyed as gamma increases
```

Result: PASS on tested grid.

| gamma | max CHSH phase1 | terrain delta | next release dev |
|---:|---:|---:|---:|
| 1.0 | 0.000000 | 0.000000 | 0.000000% |
| 0.75 | 0.707107 | 0.000000 | 0.000000% |
| 0.5 | 1.414214 | 0.000000 | 0.000000% |
| 0.25 | 2.121320 | 0.385016 | +5.446770% |
| 0.0 | 2.828427 | 2.646051 | +21.389922% |

### P5 localization

Prediction:

```text
stress_context effect is stronger than normal_context and storage_context
```

Result: PASS.

At gamma=0:

| scenario | max CHSH phase1 | terrain delta end phase1 | next release dev |
|---|---:|---:|---:|
| normal_context | 2.032205 | 0.075940 | +0.969169% |
| stress_context | 2.828427 | 2.646051 | +21.389922% |
| storage_context | 2.032205 | 0.075940 | +0.676818% |

## Full summary

| scenario | gamma | Arm2 next release | Arm3 next release | dev % | max CHSH | CHSH excess total | measurement write | terrain delta | mean road boost Arm2 | mean road boost Arm3 | effect? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| normal_context | 1.0 | 97.880477 | 97.880477 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 1.699016 | 1.699016 | FALSE |
| normal_context | 0.75 | 97.880477 | 97.880477 | 0.000000 | 0.508051 | 0.000000 | 0.000000 | 0.000000 | 1.699016 | 1.699016 | FALSE |
| normal_context | 0.5 | 97.880477 | 97.880477 | 0.000000 | 1.016102 | 0.000000 | 0.000000 | 0.000000 | 1.699016 | 1.699016 | FALSE |
| normal_context | 0.25 | 97.880477 | 97.880477 | 0.000000 | 1.524153 | 0.000000 | 0.000000 | 0.000000 | 1.699016 | 1.699016 | FALSE |
| normal_context | 0.0 | 97.880477 | 98.829104 | +0.969169 | 2.032205 | 5.304734 | 0.212189 | 0.075940 | 1.699016 | 1.715959 | TRUE |
| stress_context | 1.0 | 66.236923 | 66.236923 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 1.435235 | 1.435235 | FALSE |
| stress_context | 0.75 | 66.236923 | 66.236923 | 0.000000 | 0.707107 | 0.000000 | 0.000000 | 0.000000 | 1.435235 | 1.435235 | FALSE |
| stress_context | 0.5 | 66.236923 | 66.236923 | 0.000000 | 1.414214 | 0.000000 | 0.000000 | 0.000000 | 1.435235 | 1.435235 | FALSE |
| stress_context | 0.25 | 66.236923 | 69.844696 | +5.446770 | 2.121320 | 41.427599 | 1.657104 | 0.385016 | 1.435235 | 1.553789 | TRUE |
| stress_context | 0.0 | 66.236923 | 80.404950 | +21.389922 | 2.828427 | 329.609092 | 13.184364 | 2.646051 | 1.435235 | 1.864160 | TRUE |
| storage_context | 1.0 | 29.986585 | 29.986585 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 1.297734 | 1.297734 | FALSE |
| storage_context | 0.75 | 29.986585 | 29.986585 | 0.000000 | 0.508051 | 0.000000 | 0.000000 | 0.000000 | 1.297734 | 1.297734 | FALSE |
| storage_context | 0.5 | 29.986585 | 29.986585 | 0.000000 | 1.016102 | 0.000000 | 0.000000 | 0.000000 | 1.297734 | 1.297734 | FALSE |
| storage_context | 0.25 | 29.986585 | 29.986585 | 0.000000 | 1.524153 | 0.000000 | 0.000000 | 0.000000 | 1.297734 | 1.297734 | FALSE |
| storage_context | 0.0 | 29.986585 | 30.189539 | +0.676818 | 2.032205 | 5.304734 | 0.212189 | 0.075940 | 1.297734 | 1.317533 | TRUE |

## Interpretation

This is the clearest match so far to the measurement-boundary interpretation.

Previous local-population transport remained reduced-Arm2 reproducible. Here, the reactor is not claiming ordinary plumbing became quantum-specific. Instead:

```text
CHSH violation is converted into an inscription signal
that signal modifies terrain
terrain then modulates later classical-effective flow through road_boost
```

The important causal chain is:

```text
noncommutative joint readout
-> CHSH_excess
-> terrain inscription
-> later road_boost change
-> next-phase P_release change
```

## Safe claim

```text
A deliberately added CHSH measurement-boundary signal can be written into terrain and later modulate classical-effective reactor dynamics. This is a model-level positive for measurement-boundary terrain feedback, not for ordinary local population plumbing.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not evidence that local population plumbing is quantum-specific
```

## What this updates

The surviving path is now:

```text
joint / noncommutative readout
-> terrain writeback
-> later classical-effective modulation
```

This connects the witness line to the reactor line through terrain inscription, not through quantum plumbing.

## Next boundary

The next strict boundary is whether the terrain inscription can be made less oracle-like:

```text
basis choices explicit and audited
CHSH measurements sampled rather than directly read from density matrix
measurement backaction separated from terrain write
hardware-feasible witness circuit separated from classical-effective reactor dynamics
```
