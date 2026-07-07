# Quantum Fixed-Basis Adaptive Feedback Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_fixed_basis_adaptive_feedback_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_fixed_basis_adaptive_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707_summary.csv
```

## Purpose

This experiment tightens the adaptive measurement-feedback line by removing per-step CHSH basis optimization.

A single fixed CHSH basis is pre-calibrated once at:

```text
phi = pi
gamma = 0
```

The same four measurement settings are used for all contexts, steps, and gamma values.

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_ADAPTIVE_FEEDBACK
```

## Key guard

This probe is stricter than the prior adaptive probe:

```text
previous: per-step optimized CHSH bases
this probe: fixed basis reused everywhere
```

Normal/storage later adaptive activity is not counted positive without phase-1 Bell-excess terrain inscription.

## P1 gamma=1 null

Result: PASS.

| scenario | gamma | phase1 write | phase2 adaptive steps | phase2 release dev | phase3 release dev |
|---|---:|---:|---:|---:|---:|
| normal_fixed_adaptive | 1.0 | 0.000000 | 0 | 0.000000% | 0.000000% |
| stress_fixed_adaptive | 1.0 | 0.000000 | 0 | 0.000000% | 0.000000% |
| storage_fixed_adaptive | 1.0 | 0.000000 | 0 | 0.000000% | 0.000000% |

## P2 fixed-basis stress positive

Result: PASS.

| gamma | phase1 write | terrain delta p1 | phase2 adaptive steps | phase3 adaptive steps | mean gate p2 Arm3 | phase2 release dev | phase3 release dev |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.25 | 0.360060 | 0.089478 | 12 | 289 | 1.000129 | +1.438670% | +0.105794% |
| 0.0 | 10.580120 | 2.340440 | 90 | 346 | 1.024985 | +21.867957% | +3.988183% |

The fixed-basis effect is weaker than the per-step optimized adaptive probe, but it survives.

## P3 strict positivity

At gamma=0:

| scenario | phase1 write | phase2 adaptive steps | phase3 adaptive steps | phase2 release dev | phase3 release dev | positive? |
|---|---:|---:|---:|---:|---:|---|
| normal_fixed_adaptive | 0.000000 | 0 | 345 | 0.000000% | +2.458360% | FALSE |
| stress_fixed_adaptive | 10.580120 | 90 | 346 | +21.867957% | +3.988183% | TRUE |
| storage_fixed_adaptive | 0.000000 | 0 | 332 | 0.000000% | +0.418648% | FALSE |

Later adaptive activity alone is not sufficient. The required chain is:

```text
phase-1 Bell-excess terrain write
-> fixed-basis adaptive readout/gate shift
-> later output change
```

## P4 matched replay specificity

Matched replay reproduces the post-write dynamics:

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

| gamma | phase1 write | terrain delta p1 | terrain delta p2 | p1 sampled steps | p2 adaptive steps | p3 adaptive steps | max S_hat p1 | max S_hat p2 | max S_hat p3 | mean gate p2 | mean gate p3 | p2 dev | p3 dev | effect? |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1.0 | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 0 | 0.034485 | 0.035278 | 0.038208 | 1.000000 | 1.000000 | 0.000000% | 0.000000% | FALSE |
| 0.75 | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 0 | 0.734985 | 0.718018 | 0.737488 | 1.000000 | 1.000000 | 0.000000% | 0.000000% | FALSE |
| 0.5 | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 0 | 1.447632 | 1.430786 | 1.445435 | 1.000000 | 1.000000 | 0.000000% | 0.000000% | FALSE |
| 0.25 | 0.360060 | 0.089478 | 0.002330 | 267 | 12 | 289 | 2.144531 | 2.129150 | 2.147278 | 1.000129 | 1.004086 | +1.438670% | +0.105794% | TRUE |
| 0.0 | 10.580120 | 2.340440 | 0.039577 | 322 | 90 | 346 | 2.848999 | 2.844482 | 2.847656 | 1.024985 | 1.128145 | +21.867957% | +3.988183% | TRUE |

## Interpretation

The adaptive measurement-feedback result survives a fixed-basis constraint.

Supported chain:

```text
fixed-basis sampled CHSH write
-> terrain memory
-> later fixed-basis adaptive measurement context shift
-> conservative adaptive CHSH gate
-> later output modulation
```

The result is narrower and more hardware-like than the per-step optimized version, but still model-level.

## Safe claim

```text
A fixed-basis finite-shot CHSH measurement boundary, pre-calibrated once rather than optimized per step, can still write terrain memory and shift later adaptive measurement gates in stress context. Normal/storage later adaptive activity is not counted positive without phase-1 Bell-excess terrain inscription. This remains model-level and not hardware or ordinary local population plumbing.
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

The next boundaries are:

```text
membrane decision boundary using adaptive terrain memory
pre-registered hardware shot budget
explicit QPU candidate circuit
noise-model robustness
```
