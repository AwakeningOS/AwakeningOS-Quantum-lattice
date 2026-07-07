# Results reproducibility status

Date: 2026-07-08

## Current latest session

```text
quantum_fixed_basis_noise_robustness_probe
```

Backed by:

```text
scripts/audit/quantum_fixed_basis_noise_robustness_probe.py
data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707_summary.csv
results/quantum_fixed_basis_noise_robustness_probe_2026-07-08.md
```

Status:

```text
RAW_LOG_BACKED
POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_NOISE_ROBUSTNESS
```

Scope:

```text
positive for fixed-basis membrane decision-boundary robustness under simple simulated noise at 2048 shots per setting
stress gamma=0 survives to 15% depolarizing/phase damping, 10% amplitude damping, and 2% readout error on the tested grid
normal/storage false positives are zero
not a hardware result
```

## Current results/ classification

| file | status | action |
|---|---|---|
| `quantum_fixed_basis_noise_robustness_probe_2026-07-08.md` | RAW_LOG_BACKED | Latest noise robustness probe. At 2048 shots/setting, stress `gamma=0` survives to 15% depolarizing, 15% phase damping, 10% amplitude damping, and 2% readout error; normal/storage false positives are zero. |
| `quantum_fixed_basis_shot_budget_probe_2026-07-08.md` | RAW_LOG_BACKED | Shot-budget sweep. Stress `gamma=0` remains positive from 32768 down to 512 shots/setting. |
| `quantum_membrane_decision_boundary_probe_2026-07-08.md` | RAW_LOG_BACKED | Membrane decision probe. Stress `gamma=0` shows A pass increase, B leak decrease, D pass decrease, and release increase. |
| `quantum_fixed_basis_adaptive_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Fixed-basis adaptive probe. Stress remains positive without per-step CHSH basis optimization. |
| `quantum_adaptive_measurement_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Adaptive feedback probe using per-step optimized CHSH bases. |
| `quantum_measurement_terrain_memory_probe_2026-07-08.md` | RAW_LOG_BACKED | Terrain-memory probe; matched replay reproduces post-write memory. |
| `quantum_sampled_chsh_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Sampled terrain feedback probe. |
| `quantum_measurement_terrain_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Exact CHSH terrain feedback probe. |

## Latest safe finding

```text
At 2048 simulated shots per setting, the fixed-basis membrane decision-boundary effect survives stress gamma=0 through 15% depolarizing and phase-damping noise, 10% amplitude damping, and 2% readout error on the tested grid; normal/storage false positives remain zero. These are simulated thresholds, not hardware thresholds.
```
