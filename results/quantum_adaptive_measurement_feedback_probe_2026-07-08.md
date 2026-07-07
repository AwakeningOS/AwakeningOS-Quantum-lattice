# Quantum Adaptive Measurement Feedback Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_adaptive_measurement_feedback_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_adaptive_measurement_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707_summary.csv
```

## Purpose

This experiment tests whether measurement-boundary terrain memory can shift later measurement/readout gates and alter later reactor output.

It follows:

```text
quantum_measurement_terrain_memory_probe
```

The earlier result showed terrain memory. This probe asks whether that memory can become part of an adaptive measurement loop.

## Design

Three phases:

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
terrain memory shifts later measurement context
adaptive_phase_shift = 1.25 * terrain / (1 + terrain)
adaptive CHSH is sampled from phi + adaptive_phase_shift
adaptive_gate = 1 + 0.18 * conservative_adaptive_excess
adaptive_gate modulates later throughput
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
  replays exact Arm3 phase-1 write trajectory and keeps the later sampling stream aligned
```

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_ADAPTIVE_MEASUREMENT_FEEDBACK
```

## Prediction check

### P1 gamma=1 null

Result: PASS.

| scenario | gamma | phase1 write | phase2 adaptive steps | phase2 release dev | phase3 release dev |
|---|---:|---:|---:|---:|---:|
| normal_adaptive | 1.0 | 0.000000 | 0 | 0.000000% | 0.000000% |
| stress_adaptive | 1.0 | 0.000000 | 0 | 0.000000% | 0.000000% |
| storage_adaptive | 1.0 | 0.000000 | 0 | 0.000000% | 0.000000% |

### P2 stress adaptive loop

Result: PASS.

| gamma | phase1 write | terrain delta p1 | phase2 adaptive steps | phase3 adaptive steps | mean gate p2 Arm3 | phase2 release dev | phase3 release dev |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.25 | 0.365920 | 0.089583 | 17 | 294 | 1.000168 | +1.441263% | +0.115964% |
| 0.0 | 11.462247 | 2.347412 | 276 | 395 | 1.041792 | +24.458321% | +6.921294% |

The stress context is the main positive.

### P3 localization / strict positivity

Normal and storage can show later adaptive CHSH activity in phase3, but they are not counted positive because they have no phase-1 Bell-excess terrain inscription.

At gamma=0:

| scenario | phase1 write | phase2 adaptive steps | phase3 adaptive steps | phase2 release dev | phase3 release dev | positive? |
|---|---:|---:|---:|---:|---:|---|
| normal_adaptive | 0.000000 | 21 | 395 | +0.015319% | +5.167638% | FALSE |
| stress_adaptive | 11.462247 | 276 | 395 | +24.458321% | +6.921294% | TRUE |
| storage_adaptive | 0.000000 | 0 | 381 | 0.000000% | +0.884951% | FALSE |

This is intentional. The experiment requires:

```text
phase-1 Bell-excess terrain write
-> later adaptive readout/gate shift
-> later output change
```

A later adaptive readout alone is not enough.

### P4 matched replay specificity

Result: PASS.

For all stress positive rows:

```text
matched_replay_phase2_diff_vs_arm3 = 0
matched_replay_phase3_diff_vs_arm3 = 0
```

Interpretation:

```text
post-write adaptive dynamics follow the written terrain trace
quantum-specificity remains at the Bell-bound measurement/write/readout boundary
```

## Stress full summary

| gamma | phase1 write | terrain delta p1 | terrain delta p2 | p2 adaptive steps | p3 adaptive steps | max S_hat p2 | max S_hat p3 | mean gate p2 | mean gate p3 | p2 dev | p3 dev | effect? |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1.0 | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 0.035278 | 0.038208 | 1.000000 | 1.000000 | 0.000000% | 0.000000% | FALSE |
| 0.75 | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 0.722900 | 0.737488 | 1.000000 | 1.000000 | 0.000000% | 0.000000% | FALSE |
| 0.5 | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 1.423584 | 1.454590 | 1.000000 | 1.000000 | 0.000000% | 0.000000% | FALSE |
| 0.25 | 0.365920 | 0.089583 | 0.002333 | 17 | 294 | 2.129211 | 2.145630 | 1.000168 | 1.004186 | +1.441263% | +0.115964% | TRUE |
| 0.0 | 11.462247 | 2.347412 | 0.043638 | 276 | 395 | 2.841492 | 2.847656 | 1.041792 | 1.138419 | +24.458321% | +6.921294% | TRUE |

## Interpretation

This is a model-level positive for an adaptive measurement-boundary feedback loop.

Supported chain:

```text
finite-shot sampled CHSH write
-> terrain memory
-> later adaptive measurement context shift
-> conservative adaptive CHSH gate
-> later output modulation
```

But the scope remains narrow:

```text
not ordinary plumbing
not quantum-specific terrain physics
not hardware
```

Matched replay shows the post-write dynamics follow the written terrain trace. The quantum-specific filter is still the Bell-bound measurement/write/readout rule.

## Safe claim

```text
Finite-shot sampled CHSH terrain memory can shift later adaptive measurement/readout gates and alter later reactor output in stress context. The matched replay shows the post-write adaptive dynamics follow the written terrain trace; quantum-specificity remains at the Bell-bound measurement/write/readout boundary, not in ordinary local population plumbing.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not ordinary local population plumbing
not quantum-specific post-write terrain physics
```

## Next boundary

The next boundary is either:

```text
1. fixed-basis / hardware-like adaptive circuit
2. membrane decision boundary using the same adaptive terrain memory
3. adaptive basis schedule pre-registered without per-step optimization
```
