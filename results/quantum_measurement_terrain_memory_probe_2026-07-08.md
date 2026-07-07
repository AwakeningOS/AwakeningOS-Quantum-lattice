# Quantum Measurement Terrain Memory Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_measurement_terrain_memory_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_measurement_terrain_memory_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv
```

## Purpose

This experiment tests whether terrain written by a finite-shot sampled CHSH measurement-boundary signal persists after measurement stops, and whether it alters later reactor response.

It follows:

```text
quantum_sampled_chsh_terrain_feedback_probe
```

The earlier result showed next-phase feedback. This result asks whether the terrain behaves as a longer-lived history or memory trace.

## Design

Three phases:

```text
Phase 1: measurement/write phase, t = 0..399
Phase 2: memory/read phase, t = 400..799
Phase 3: challenge phase, t = 800..1199
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
terrain decays normally
terrain is read through road_boost
```

## Arms

```text
Arm2/Bell-bound control:
  no CHSH excess terrain write

Arm3 sampled CHSH:
  conservative sampled Bell excess writes terrain in Phase 1

Matched classical replay:
  replay the exact Arm3 write trajectory as a classical external terrain write
```

The matched replay arm tests whether post-write memory dynamics are themselves quantum-specific.

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_TERRAIN_MEMORY
```

## Prediction check

### P1 gamma=1 null

Prediction:

```text
gamma=1 has zero sampled CHSH write, terrain delta, and later release difference
```

Result: PASS.

| scenario | gamma | measurement write | terrain delta phase1 | phase2 release dev | phase3 release dev |
|---|---:|---:|---:|---:|---:|
| normal_memory | 1.0 | 0.000000 | 0.000000 | 0.000000% | 0.000000% |
| stress_memory | 1.0 | 0.000000 | 0.000000 | 0.000000% | 0.000000% |
| storage_memory | 1.0 | 0.000000 | 0.000000 | 0.000000% | 0.000000% |

### P2 terrain memory persistence

Prediction:

```text
CHSH-written terrain persists into phase2 after measurement stops
```

Result: PASS in stress_memory.

| scenario | gamma | measurement write phase1 | terrain delta end phase1 | terrain delta end phase2 | half-life steps | phase2 release dev |
|---|---:|---:|---:|---:|---:|---:|
| stress_memory | 0.25 | 0.365920 | 0.089583 | 0.002331 | 50 | +1.438596% |
| stress_memory | 0.0 | 11.462247 | 2.347412 | 0.038348 | 47 | +19.998558% |

### P3 later challenge memory

Prediction:

```text
residual terrain memory affects a later challenge phase
```

Result: PASS, but weak.

| scenario | gamma | terrain delta end phase3 | phase3 release dev |
|---|---:|---:|---:|
| stress_memory | 0.25 | 0.000117 | +0.088855% |
| stress_memory | 0.0 | 0.001749 | +1.427578% |

The memory trace is real but decays strongly.

### P4 localization

Prediction:

```text
finite-shot conservative write survives only in the high-violation stress context
```

Result: PASS.

At gamma=0:

| scenario | measurement write phase1 | positive sampled steps | terrain delta phase1 | phase2 release dev | phase3 release dev |
|---|---:|---:|---:|---:|---:|
| normal_memory | 0.000000 | 0 | 0.000000 | 0.000000% | 0.000000% |
| stress_memory | 11.462247 | 371 | 2.347412 | +19.998558% | +1.427578% |
| storage_memory | 0.000000 | 0 | 0.000000 | 0.000000% | 0.000000% |

### P5 post-write specificity

Prediction:

```text
matched classical replay reproduces post-write memory dynamics
```

Result: PASS.

For all rows, the matched classical replay release differences versus Arm3 are:

```text
phase2 diff = 0
phase3 diff = 0
```

This is the critical interpretation guard:

```text
quantum-specificity is in the write eligibility, not in terrain decay/readout after inscription
```

## Full stress-memory summary

| gamma | write phase1 | positive steps | terrain delta p1 | terrain delta p2 | terrain delta p3 | half-life | phase2 dev | phase3 dev | matched replay diff p3 | effect? |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1.0 | 0.000000 | 0 | 0.000000 | 0.000000 | 0.000000 |  | 0.000000% | 0.000000% | 0.000000 | FALSE |
| 0.75 | 0.000000 | 0 | 0.000000 | 0.000000 | 0.000000 |  | 0.000000% | 0.000000% | 0.000000 | FALSE |
| 0.5 | 0.000000 | 0 | 0.000000 | 0.000000 | 0.000000 |  | 0.000000% | 0.000000% | 0.000000 | FALSE |
| 0.25 | 0.365920 | 273 | 0.089583 | 0.002331 | 0.000117 | 50 | +1.438596% | +0.088855% | 0.000000 | TRUE |
| 0.0 | 11.462247 | 371 | 2.347412 | 0.038348 | 0.001749 | 47 | +19.998558% | +1.427578% | 0.000000 | TRUE |

## Interpretation

This result is narrower than a broad quantum-memory claim, and that is good.

The supported chain is:

```text
finite-shot sampled CHSH readout
-> conservative Bell-excess write
-> terrain inscription
-> terrain persistence after measurement stops
-> later road_boost / P_release modulation
```

But the post-write terrain dynamics are not quantum-specific. The matched classical replay reproduces them exactly.

Therefore the correct interpretation is:

```text
measurement-boundary write eligibility is quantum-specific
terrain memory after inscription is classical-effective
```

## Safe claim

```text
A finite-shot sampled CHSH measurement-boundary signal can be written into terrain, persist after measurement stops, and weakly affect a later challenge phase in stress context. The post-write memory dynamics are classical terrain dynamics: a matched classical replay of the same write trajectory reproduces them. This is model-level positive for measurement-boundary terrain memory, not for quantum-specific post-write terrain physics or ordinary local population plumbing.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not quantum-specific terrain decay
not evidence that local population plumbing is quantum-specific
```

## Next boundary

The next strict boundary is adaptive feedback:

```text
measurement-boundary terrain memory
-> changes next measurement basis or membrane gate
-> changes later CHSH/readout statistics
```

That would test whether the terrain memory becomes part of an adaptive measurement loop rather than only a passive inscription.
