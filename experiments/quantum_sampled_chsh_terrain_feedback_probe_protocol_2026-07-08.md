# Quantum Sampled CHSH Terrain Feedback Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

Does the measurement-boundary terrain feedback result survive when CHSH is not read directly from the density matrix, but estimated from explicit finite-shot CHSH measurements?

This tightens the previous result:

```text
quantum_measurement_terrain_feedback_probe
```

The previous probe used exact CHSH values. This one samples four CHSH correlators at each step and writes only conservative Bell-violating excess into terrain.

## False-positive guard

For each step, CHSH is estimated from four finite-shot correlators:

```text
E00, E01, E10, E11
S_hat = E00 + E01 + E10 - E11
```

Shots:

```text
shots_per_setting_per_step = 32768
```

A conservative margin is subtracted:

```text
margin_S = 4 * sqrt(2 * log(8/alpha) / shots)
alpha = 0.001
margin_S = 0.093683293042
```

The terrain write signal is:

```text
conservative_excess = max(0, S_hat - 2 - margin_S) / (2*sqrt(2) - 2)
measurement_terrain_write = 0.04 * conservative_excess
```

Thus finite-shot noise must clear a Bell-bound margin before it can affect terrain.

## Design

Same two-phase design as the prior exact-CHSH terrain feedback probe:

```text
Phase 1: measurement/write phase, t = 0..399
Phase 2: terrain-read phase, t = 400..799
```

During Phase 1, only conservative sampled CHSH excess can write additional terrain.
During Phase 2, measurement write is off and terrain is read by classical-effective road feedback.

## Arms

```text
Arm2/Bell-bound control:
  no Bell-violating excess is available
  measurement terrain write = 0

Arm3 sampled CHSH:
  four CHSH correlators are sampled with finite shots
  only conservative excess over S <= 2 writes terrain
```

## Success criteria

A positive sampled measurement-boundary feedback result requires:

```text
1. conservative_chsh_excess_total_phase1 > 0
2. measurement_terrain_write_phase1 > 0
3. terrain_end_phase1 Arm3 > Arm2
4. next-phase P_release Arm3 > Arm2
5. gamma=1 removes the effect
```

## Pre-registered predictions

```text
P1 gamma=1 null:
  conservative sampled excess = 0 in all scenarios.

P2 noise guard:
  normal/storage should not pass merely from sample noise.

P3 main:
  stress_context at gamma=0 survives the sampled conservative margin.

P4 threshold:
  stress_context gamma=0.25 may survive weakly; gamma>=0.5 should not.
```

## Expected raw outputs

```text
data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv
data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_sampled_chsh_terrain_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv
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

This is a model-level sampled-measurement positive only if the conservative sampled CHSH excess changes terrain and later dynamics beyond the Bell-bound control.
