# Results reproducibility status

Date: 2026-07-08

## Current latest session

```text
quantum_fixed_basis_adaptive_feedback_probe
```

Backed by:

```text
scripts/audit/quantum_fixed_basis_adaptive_feedback_probe.py
data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707_summary.csv
results/quantum_fixed_basis_adaptive_feedback_probe_2026-07-08.md
```

Status:

```text
RAW_LOG_BACKED
POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_ADAPTIVE_FEEDBACK
```

Scope:

```text
positive for fixed-basis finite-shot CHSH terrain memory shifting later adaptive measurement gates in stress context
no per-step CHSH basis optimization
post-write adaptive dynamics follow the written terrain trace
not positive for ordinary local population plumbing
not a hardware result
```

## Current results/ classification

| file | status | action |
|---|---|---|
| `quantum_fixed_basis_adaptive_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Latest fixed-basis adaptive probe. Uses a single CHSH basis pre-calibrated at `phi=pi`; stress remains positive without per-step basis optimization. `gamma=0` has phase2 release +21.867957% and phase3 release +3.988183%. |
| `quantum_adaptive_measurement_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Adaptive feedback probe using per-step optimized CHSH bases. Phase-1 CHSH terrain memory shifts later adaptive measurement gates in stress context. |
| `quantum_measurement_terrain_memory_probe_2026-07-08.md` | RAW_LOG_BACKED | Terrain-memory probe. Sampled CHSH terrain inscription persists after measurement stops in stress context; matched replay reproduces post-write memory. |
| `quantum_sampled_chsh_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Sampled terrain feedback probe; stress remains positive after conservative finite-shot margin. |
| `quantum_measurement_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Exact CHSH terrain feedback probe. |
| `quantum_microreactor_chsh_readout_transport_probe_2026-07-08.md` | RAW_LOG_BACKED | CHSH readout transport probe. |
| `quantum_microreactor_transported_branching_arm2_kill_2026-07-08.md` | RAW_LOG_BACKED | Local-population transport is Arm2-reproducible. |
| `quantum_microreactor_branching_converter_probe_2026-07-08.md` | RAW_LOG_BACKED | Branch-only observable is Arm2-reproducible. |
| `quantum_microreactor_gamma_sweep_quality_probe_2026-07-08.md` | RAW_LOG_BACKED | Quality/coherence probe is negative for quantum-specific efficacy. |
| `quantum_microreactor_gamma_validation_2026-07-08.md` | RAW_LOG_BACKED | gamma=max validation gate. |

## Latest safe finding

```text
A fixed-basis finite-shot CHSH measurement boundary, pre-calibrated once rather than optimized per step, can still write terrain memory and shift later adaptive measurement gates in stress context. Normal/storage later adaptive activity is not counted positive without phase-1 Bell-excess terrain inscription. This remains model-level and not hardware or ordinary local population plumbing.
```
