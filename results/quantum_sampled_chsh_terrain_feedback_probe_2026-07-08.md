# Quantum Sampled CHSH Terrain Feedback Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_sampled_chsh_terrain_feedback_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_sampled_chsh_terrain_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv
```

## Purpose

This experiment tightens the previous exact-CHSH terrain feedback probe.

Previous positive:

```text
CHSH_excess from the density matrix can be written into terrain and later modulate classical-effective dynamics.
```

This probe asks whether the result survives when CHSH is estimated from finite-shot measurements.

## Sampling rule

At each phase-1 step, four CHSH correlators are sampled:

```text
E00, E01, E10, E11
S_hat = E00 + E01 + E10 - E11
```

Sampling configuration:

```text
shots_per_setting_per_step = 32768
alpha = 0.001
confidence_margin_S = 0.093683293042
```

The terrain write uses only conservative sampled excess:

```text
conservative_excess = max(0, S_hat - 2 - confidence_margin_S) / (2*sqrt(2) - 2)
measurement_terrain_write = 0.04 * conservative_excess
```

Therefore finite-shot noise must clear a Bell-bound margin before it can affect terrain.

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_SAMPLED_CHSH_TERRAIN_FEEDBACK
```

## Prediction check

### P1 gamma=1 null

Prediction:

```text
gamma=1 has no conservative sampled excess and no terrain feedback in all scenarios
```

Result: PASS.

| scenario | gamma | max CHSH hat | positive sampled steps | measurement write | next release dev |
|---|---:|---:|---:|---:|---:|
| normal_context | 1.0 | 0.032471 | 0 | 0.000000 | 0.000000% |
| stress_context | 1.0 | 0.034485 | 0 | 0.000000 | 0.000000% |
| storage_context | 1.0 | 0.028503 | 0 | 0.000000 | 0.000000% |

### P2 noise guard

Prediction:

```text
normal/storage should not pass merely from sample noise
```

Result: PASS.

At gamma=0, both normal and storage have small true CHSH violation, but after finite-shot conservative margin they do not write terrain:

| scenario | max CHSH true | max CHSH hat | positive sampled steps | conservative excess total | next release dev |
|---|---:|---:|---:|---:|---:|
| normal_context | 2.032205 | 2.049927 | 0 | 0.000000 | 0.000000% |
| storage_context | 2.032205 | 2.045837 | 0 | 0.000000 | 0.000000% |

### P3 main

Prediction:

```text
stress_context at gamma=0 survives the sampled conservative margin
```

Result: PASS.

| scenario | gamma | max CHSH true | max CHSH hat | positive sampled steps | conservative excess total | terrain delta | next release dev |
|---|---:|---:|---:|---:|---:|---:|---:|
| stress_context | 0.0 | 2.828427 | 2.847168 | 371 | 286.556163 | 2.347412 | +19.998558% |

### P4 threshold

Prediction:

```text
stress_context gamma=0.25 may survive weakly; gamma>=0.5 should not
```

Result: PASS.

| gamma | max CHSH true | max CHSH hat | positive sampled steps | terrain delta | next release dev |
|---:|---:|---:|---:|---:|---:|
| 1.0 | 0.000000 | 0.034485 | 0 | 0.000000 | 0.000000% |
| 0.75 | 0.707107 | 0.733582 | 0 | 0.000000 | 0.000000% |
| 0.5 | 1.414214 | 1.443237 | 0 | 0.000000 | 0.000000% |
| 0.25 | 2.121320 | 2.144775 | 273 | 0.089583 | +1.438596% |
| 0.0 | 2.828427 | 2.847168 | 371 | 2.347412 | +19.998558% |

## Full summary

| scenario | gamma | shots | margin S | Arm2 next release | Arm3 next release | dev % | max S true | max S hat | positive steps | conservative excess total | terrain delta | mean road boost Arm2 | mean road boost Arm3 | effect? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| normal_context | 1.0 | 32768 | 0.093683 | 97.880477 | 97.880477 | 0.000000 | 0.000000 | 0.032471 | 0 | 0.000000 | 0.000000 | 1.699016 | 1.699016 | FALSE |
| normal_context | 0.75 | 32768 | 0.093683 | 97.880477 | 97.880477 | 0.000000 | 0.508051 | 0.536133 | 0 | 0.000000 | 0.000000 | 1.699016 | 1.699016 | FALSE |
| normal_context | 0.5 | 32768 | 0.093683 | 97.880477 | 97.880477 | 0.000000 | 1.016102 | 1.050537 | 0 | 0.000000 | 0.000000 | 1.699016 | 1.699016 | FALSE |
| normal_context | 0.25 | 32768 | 0.093683 | 97.880477 | 97.880477 | 0.000000 | 1.524153 | 1.540833 | 0 | 0.000000 | 0.000000 | 1.699016 | 1.699016 | FALSE |
| normal_context | 0.0 | 32768 | 0.093683 | 97.880477 | 97.880477 | 0.000000 | 2.032205 | 2.049927 | 0 | 0.000000 | 0.000000 | 1.699016 | 1.699016 | FALSE |
| stress_context | 1.0 | 32768 | 0.093683 | 66.236923 | 66.236923 | 0.000000 | 0.000000 | 0.034485 | 0 | 0.000000 | 0.000000 | 1.435235 | 1.435235 | FALSE |
| stress_context | 0.75 | 32768 | 0.093683 | 66.236923 | 66.236923 | 0.000000 | 0.707107 | 0.733582 | 0 | 0.000000 | 0.000000 | 1.435235 | 1.435235 | FALSE |
| stress_context | 0.5 | 32768 | 0.093683 | 66.236923 | 66.236923 | 0.000000 | 1.414214 | 1.443237 | 0 | 0.000000 | 0.000000 | 1.435235 | 1.435235 | FALSE |
| stress_context | 0.25 | 32768 | 0.093683 | 66.236923 | 67.189805 | +1.438596 | 2.121320 | 2.144775 | 273 | 9.148002 | 0.089583 | 1.435235 | 1.467216 | TRUE |
| stress_context | 0.0 | 32768 | 0.093683 | 66.236923 | 79.483353 | +19.998558 | 2.828427 | 2.847168 | 371 | 286.556163 | 2.347412 | 1.435235 | 1.839035 | TRUE |
| storage_context | 1.0 | 32768 | 0.093683 | 29.986585 | 29.986585 | 0.000000 | 0.000000 | 0.028503 | 0 | 0.000000 | 0.000000 | 1.297734 | 1.297734 | FALSE |
| storage_context | 0.75 | 32768 | 0.093683 | 29.986585 | 29.986585 | 0.000000 | 0.508051 | 0.531128 | 0 | 0.000000 | 0.000000 | 1.297734 | 1.297734 | FALSE |
| storage_context | 0.5 | 32768 | 0.093683 | 29.986585 | 29.986585 | 0.000000 | 1.016102 | 1.041138 | 0 | 0.000000 | 0.000000 | 1.297734 | 1.297734 | FALSE |
| storage_context | 0.25 | 32768 | 0.093683 | 29.986585 | 29.986585 | 0.000000 | 1.524153 | 1.541077 | 0 | 0.000000 | 0.000000 | 1.297734 | 1.297734 | FALSE |
| storage_context | 0.0 | 32768 | 0.093683 | 29.986585 | 29.986585 | 0.000000 | 2.032205 | 2.045837 | 0 | 0.000000 | 0.000000 | 1.297734 | 1.297734 | FALSE |

## Interpretation

The exact-CHSH terrain feedback positive survives finite-shot sampling in the stress context.

The key chain remains:

```text
sampled noncommutative CHSH readout
-> conservative Bell-excess signal
-> terrain inscription
-> later road_boost change
-> next-phase P_release change
```

But the finite-shot guard removes weak positives in normal and storage contexts. This makes the result narrower and cleaner:

```text
only the high-violation stress boundary survives the sampled conservative margin
```

## Safe claim

```text
A finite-shot sampled CHSH measurement-boundary signal, after subtracting a conservative Bell-bound margin, can still be written into terrain and later modulate classical-effective dynamics in stress context. This is a model-level positive for sampled measurement-boundary terrain feedback, not for ordinary local population plumbing.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not evidence that local population plumbing is quantum-specific
```

## Next boundary

The next strict boundary is hardware-likeness:

```text
fixed measurement bases instead of per-step optimized bases
explicit basis schedule
separate witness sampling from terrain writeback
shot budget close to QPU constraints
noise model or real QPU candidate circuit
```
