# Quantum Measurement Terrain Feedback Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

Can a quantum measurement-boundary signal be written into terrain and later modulate classical-effective reactor dynamics?

This tests the proposed boundary interpretation:

```text
quantum-specific effects do not act as ordinary material flow
but can appear at measurement/readout boundaries
and can affect later material dynamics if the readout signal is inscribed into terrain
```

## Prior result

The immediately prior positive was:

```text
quantum_microreactor_chsh_readout_transport_probe
```

It showed that a deliberately added CHSH readout component can push transported `P_release` beyond the Bell/local classical ceiling.

This experiment asks whether that readout signal can be written back into terrain, then affect later classical-effective dynamics.

## Two-phase design

```text
Phase 1: measurement/write phase, t = 0..399
Phase 2: terrain-read phase, t = 400..799
```

During Phase 1:

```text
C:B joint state is built from reactor context
S_CHSH is computed
CHSH_excess = max(0, S_CHSH - 2) / (2*sqrt(2) - 2)
terrain receives an additional write only from CHSH_excess
```

During Phase 2:

```text
no additional CHSH terrain write is applied
terrain is read by the classical-effective reactor through road_boost
next-phase P_release is measured
```

## Arms

```text
Arm2/Bell-bound control:
  no CHSH excess is available
  measurement terrain write = 0

Arm3 quantum CHSH readout:
  CHSH_excess can write terrain only if S_CHSH > 2
```

This uses the Bell/local bound as the control, not a weak mean-field Arm2.

## Readout and write rule

```text
CHSH_excess = max(0, S_CHSH - 2) / (2*sqrt(2) - 2)
measurement_terrain_write = measurement_write_gain * CHSH_excess
measurement_write_gain = 0.04
```

This ensures:

```text
S_CHSH <= 2  -> no measurement terrain bonus
S_CHSH > 2   -> only Bell-violating excess is written
```

## Scenarios

```text
normal_context
stress_context
storage_context
```

Phase 2 uses terrain-sensitive road feedback so that terrain inscription can modulate later classical dynamics.

## Gamma values

```text
gamma = 1.0, 0.75, 0.5, 0.25, 0.0
```

## Pre-registered predictions

```text
P1 gamma=1 null:
  CHSH_excess = 0 and terrain_delta = 0 in all scenarios.

P2 Arm2/Bell-bound:
  control has no CHSH terrain bonus.

P3 main:
  stress_context at low gamma has CHSH_excess > 0, terrain_delta > 0, and next-phase P_release > Arm2.

P4 gamma sensitivity:
  stress_context effect is destroyed as gamma increases.

P5 localization:
  stress_context effect is stronger than normal_context and storage_context.
```

## Success criteria

A model-level measurement-boundary feedback positive requires:

```text
1. CHSH_excess > 0
2. measurement terrain write > 0
3. terrain_end_phase1 Arm3 > terrain_end_phase1 Arm2
4. next-phase P_release Arm3 > Arm2
5. gamma=1 removes the effect
```

## Forbidden claims

Do not claim:

```text
hardware result
chemical realism
biological metabolism
universal quantum advantage
ordinary local population plumbing is quantum-specific
```

This is only a model-level positive for a deliberately added CHSH measurement-boundary terrain feedback component.

## Expected raw outputs

```text
data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv
data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_measurement_terrain_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv
```
