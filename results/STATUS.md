# Results reproducibility status

Date: 2026-07-08

## Current latest session

```text
quantum_adaptive_measurement_feedback_probe
```

Backed by:

```text
scripts/audit/quantum_adaptive_measurement_feedback_probe.py
data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707_summary.csv
results/quantum_adaptive_measurement_feedback_probe_2026-07-08.md
```

Status:

```text
RAW_LOG_BACKED
POSITIVE_FOR_MODEL_LEVEL_ADAPTIVE_MEASUREMENT_FEEDBACK
```

Scope:

```text
positive for finite-shot sampled CHSH terrain memory shifting later adaptive measurement/readout gates in stress context
post-write adaptive dynamics follow the written terrain trace
not positive for ordinary local population plumbing
not a hardware result
```

## Current results/ classification

| file | status | action |
|---|---|---|
| `quantum_adaptive_measurement_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Latest adaptive feedback probe. Phase-1 CHSH terrain memory shifts later adaptive measurement gates in stress context; `gamma=0` has phase2 release +24.458321% and phase3 release +6.921294%. Normal/storage later adaptive activity is not counted positive without phase-1 Bell-excess terrain inscription. |
| `quantum_measurement_terrain_memory_probe_2026-07-08.md` | RAW_LOG_BACKED | Terrain-memory probe. Sampled CHSH terrain inscription persists after measurement stops in stress context; `gamma=0` has phase2 release +19.998558% and phase3 release +1.427578%. Matched replay reproduces post-write memory. |
| `quantum_sampled_chsh_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Sampled terrain feedback probe; stress remains positive after conservative finite-shot margin. |
| `quantum_measurement_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Exact CHSH terrain feedback probe. |
| `quantum_microreactor_chsh_readout_transport_probe_2026-07-08.md` | RAW_LOG_BACKED | CHSH readout transport probe. |
| `quantum_microreactor_transported_branching_arm2_kill_2026-07-08.md` | RAW_LOG_BACKED | Local-population transport is Arm2-reproducible. |
| `quantum_microreactor_branching_converter_probe_2026-07-08.md` | RAW_LOG_BACKED | Branch-only observable is Arm2-reproducible. |
| `quantum_microreactor_gamma_sweep_quality_probe_2026-07-08.md` | RAW_LOG_BACKED | Quality/coherence probe is negative for quantum-specific efficacy. |
| `quantum_microreactor_gamma_validation_2026-07-08.md` | RAW_LOG_BACKED | gamma=max validation gate. |

## Latest safe finding

```text
Finite-shot sampled CHSH terrain memory can shift later adaptive measurement/readout gates and alter later reactor output in stress context. The matched replay shows the post-write adaptive dynamics follow the written terrain trace; quantum-specificity remains at the Bell-bound measurement/write/readout boundary, not in ordinary local population plumbing.
```
