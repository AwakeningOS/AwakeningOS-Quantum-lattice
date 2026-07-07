# Quantum Adaptive Measurement Feedback Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

Can measurement-boundary terrain memory change later measurement/readout statistics and thereby alter later reactor output?

This follows:

```text
quantum_measurement_terrain_memory_probe
```

That probe showed that sampled CHSH terrain inscription can persist after measurement stops. This probe asks whether that memory can become part of an adaptive measurement loop.

## Core distinction

This probe does not claim ordinary plumbing is quantum-specific.

It separates:

```text
1. Phase-1 write eligibility:
   only conservative sampled CHSH excess over the Bell bound can write terrain

2. Later adaptive loop:
   terrain memory shifts later measurement context / gate strength

3. Post-write specificity:
   matched replay tests whether later dynamics follow the terrain trace rather than a new quantum terrain physics
```

## Three-phase design

```text
Phase 1: write phase, t = 0..399
Phase 2: adaptive readout phase, t = 400..799
Phase 3: challenge/adaptive phase, t = 800..1199
```

During Phase 1:

```text
finite-shot CHSH is sampled
conservative_excess = max(0, S_hat - 2 - margin) / (2*sqrt(2)-2)
measurement_terrain_write = 0.04 * conservative_excess
```

During Phases 2 and 3:

```text
measurement write is off
terrain memory shifts the later measurement context
adaptive_phase_shift = adaptive_phase_gain * terrain / (1 + terrain)
adaptive CHSH is sampled from phi + adaptive_phase_shift
adaptive_gate = 1 + adaptive_gate_gain * conservative_adaptive_excess
adaptive_gate modulates later source/permeability throughput
```

Constants:

```text
adaptive_phase_gain = 1.25
adaptive_gate_gain = 0.18
shots_per_setting_per_step = 32768
confidence_margin_S = 0.093683293042
```

## Arms

```text
Arm2/Bell-bound control:
  no phase-1 CHSH terrain write
  no adaptive CHSH excess gate

Arm3 adaptive sampled CHSH:
  phase-1 conservative Bell excess writes terrain
  later terrain shifts adaptive measurement context
  conservative adaptive CHSH excess opens adaptive gate

Matched classical replay:
  replays the exact Arm3 phase-1 write trajectory and uses the same later adaptive sampling stream
```

## Success criteria

A model-level adaptive measurement feedback positive requires:

```text
1. phase1 measurement write > 0
2. terrain_delta_end_phase1 > 0
3. later adaptive positive sampled steps > 0
4. mean adaptive gate in Arm3 > Arm2
5. later P_release Arm3 > Arm2
6. gamma=1 removes the effect
```

## Specificity criterion

If matched classical replay reproduces Arm3 after replaying the same write trace, then:

```text
quantum-specificity remains in the measurement-boundary write/readout eligibility
post-write terrain/adaptive dynamics follow the written terrain trace
```

## Tested contexts

```text
normal_adaptive
stress_adaptive
storage_adaptive
```

## Expected raw outputs

```text
data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707_summary.csv
data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_adaptive_measurement_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707_summary.csv
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
