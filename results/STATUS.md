# Results reproducibility status

Date: 2026-07-08

## Current latest session

```text
quantum_membrane_decision_boundary_probe
```

Backed by:

```text
scripts/audit/quantum_membrane_decision_boundary_probe.py
data/quantum_microreactor/membrane_decision_boundary_probe_seed20260707_summary.csv
results/quantum_membrane_decision_boundary_probe_2026-07-08.md
```

Status:

```text
RAW_LOG_BACKED
POSITIVE_FOR_MODEL_LEVEL_MEMBRANE_DECISION_BOUNDARY
```

Scope:

```text
positive for fixed-basis finite-shot CHSH signal directly modulating membrane pass/block decisions in stress contexts
A passage increases while B contaminant and D stress passage are suppressed
matched replay shows downstream dynamics follow the membrane gate trace
not hardware, not biological membrane realism
```

## Current results/ classification

| file | status | action |
|---|---|---|
| `quantum_membrane_decision_boundary_probe_2026-07-08.md` | RAW_LOG_BACKED | Latest membrane decision probe. Stress `gamma=0` shows A pass +26.657798%, B leak -18.877682%, D pass -68.046074%, release +26.657798%. Contaminated-stress `gamma=0` shows A pass +26.894291%, B leak -18.794025%, D pass -68.066804%, release +26.894291%. |
| `quantum_fixed_basis_adaptive_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Fixed-basis adaptive probe. Stress remains positive without per-step CHSH basis optimization. |
| `quantum_adaptive_measurement_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Adaptive feedback probe using per-step optimized CHSH bases. |
| `quantum_measurement_terrain_memory_probe_2026-07-08.md` | RAW_LOG_BACKED | Terrain-memory probe; matched replay reproduces post-write memory. |
| `quantum_sampled_chsh_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Sampled terrain feedback probe. |
| `quantum_measurement_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Exact CHSH terrain feedback probe. |
| `quantum_microreactor_chsh_readout_transport_probe_2026-07-08.md` | RAW_LOG_BACKED | CHSH readout transport probe. |
| `quantum_microreactor_transported_branching_arm2_kill_2026-07-08.md` | RAW_LOG_BACKED | Local-population transport is Arm2-reproducible. |

## Latest safe finding

```text
A fixed-basis finite-shot CHSH measurement-boundary signal can directly modulate membrane pass/block decisions in stress contexts: A passage increases while B contaminant and D stress passage are suppressed. Matched replay shows downstream dynamics follow the gate trace; specificity remains at the Bell-bound measurement/decision boundary.
```
