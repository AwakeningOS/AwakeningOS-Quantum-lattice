# Results reproducibility status

Date: 2026-07-08

## Current latest session

```text
quantum_fixed_basis_shot_budget_probe
```

Backed by:

```text
scripts/audit/quantum_fixed_basis_shot_budget_probe.py
data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707_summary.csv
results/quantum_fixed_basis_shot_budget_probe_2026-07-08.md
```

Status:

```text
RAW_LOG_BACKED
POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_SHOT_BUDGET
```

Scope:

```text
positive for fixed-basis membrane decision-boundary shot-budget robustness in stress gamma=0
stress gamma=0 survives down to 512 simulated shots per setting
normal/storage false positives are zero on the tested grid
not a hardware result
```

## Current results/ classification

| file | status | action |
|---|---|---|
| `quantum_fixed_basis_shot_budget_probe_2026-07-08.md` | RAW_LOG_BACKED | Latest shot-budget sweep. Stress `gamma=0` remains positive from 32768 down to 512 shots/setting; at 512 shots: A pass +0.156974%, B leak -0.330297%, D pass -7.119113%, release +0.156974%. Normal/storage false positives are zero. |
| `quantum_membrane_decision_boundary_probe_2026-07-08.md` | RAW_LOG_BACKED | Membrane decision probe. Stress `gamma=0` shows A pass +26.657798%, B leak -18.877682%, D pass -68.046074%, release +26.657798%. |
| `quantum_fixed_basis_adaptive_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Fixed-basis adaptive probe. Stress remains positive without per-step CHSH basis optimization. |
| `quantum_adaptive_measurement_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Adaptive feedback probe using per-step optimized CHSH bases. |
| `quantum_measurement_terrain_memory_probe_2026-07-08.md` | RAW_LOG_BACKED | Terrain-memory probe; matched replay reproduces post-write memory. |
| `quantum_sampled_chsh_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Sampled terrain feedback probe. |
| `quantum_measurement_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Exact CHSH terrain feedback probe. |
| `quantum_microreactor_chsh_readout_transport_probe_2026-07-08.md` | RAW_LOG_BACKED | CHSH readout transport probe. |

## Latest safe finding

```text
The fixed-basis membrane decision-boundary effect survives down to 512 shots per setting in stress gamma=0, while normal/storage false positives remain zero on the tested grid. The weaker stress gamma=0.25 effect survives only at 32768 shots.
```
