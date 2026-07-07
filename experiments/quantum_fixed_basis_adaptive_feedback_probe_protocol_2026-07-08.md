# Quantum Fixed-Basis Adaptive Feedback Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

Does the adaptive measurement-feedback result survive when CHSH measurement bases are fixed in advance rather than optimized at each step?

This tightens:

```text
quantum_adaptive_measurement_feedback_probe
```

The previous adaptive probe used a sampled CHSH estimate but still used per-state optimized CHSH bases. This probe removes that oracle-like step.

## Fixed basis

A single CHSH basis set is pre-calibrated once at the stress/Bell point:

```text
phi = pi
gamma = 0
```

The same four observables are then used for all contexts, all steps, and all gamma values.

No per-step optimization is allowed.

## Design

Three phases:

```text
Phase 1: write phase, t = 0..399
Phase 2: adaptive readout phase, t = 400..799
Phase 3: challenge/adaptive phase, t = 800..1199
```

During Phase 1:

```text
fixed-basis CHSH is sampled
conservative_excess = max(0, S_hat - 2 - margin) / (2*sqrt(2)-2)
measurement_terrain_write = 0.04 * conservative_excess
```

During Phases 2 and 3:

```text
measurement write is off
terrain memory shifts later fixed-basis measurement context
adaptive_phase_shift = 1.25 * terrain / (1 + terrain)
adaptive_gate = 1 + 0.18 * conservative_adaptive_excess
```

## Success criteria

A model-level fixed-basis adaptive positive requires:

```text
1. phase1 measurement write > 0
2. terrain_delta_end_phase1 > 0
3. later fixed-basis adaptive positive sampled steps > 0
4. later release Arm3 > Bell-bound Arm2
5. gamma=1 removes the effect
```

Normal/storage later adaptive activity is not sufficient without Phase-1 Bell-excess terrain inscription.

## Expected outputs

```text
data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707_summary.csv
data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_fixed_basis_adaptive_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707_summary.csv
```

## Forbidden claims

Do not claim:

```text
hardware result
chemical realism
biological metabolism
universal quantum advantage
ordinary local population plumbing is quantum-specific
post-write terrain physics is quantum-specific
```
