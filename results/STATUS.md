# Results reproducibility status

Date: 2026-07-08

## Current latest session

```text
quantum_context_order_terrain_probe
```

Backed by:

```text
scripts/audit/quantum_context_order_terrain_probe.py
data/quantum_microreactor/context_order_terrain_probe_seed20260707_summary.csv
results/quantum_context_order_terrain_probe_2026-07-08.md
```

Status:

```text
RAW_LOG_BACKED
POSITIVE_FOR_MODEL_LEVEL_CONTEXT_ORDER_TERRAIN
```

Scope:

```text
positive for fixed noncommuting context-read order changing terrain/release in stress gamma=0
AB order produces conservative order signal; BA order remains zero
normal/storage and gamma=1 remain null
not a hardware result
```

## Current results/ classification

| file | status | action |
|---|---|---|
| `quantum_context_order_terrain_probe_2026-07-08.md` | RAW_LOG_BACKED | Latest context-order probe. In stress `gamma=0`, AB order signal total is 198.363585 across 683 steps while BA is zero; final terrain is 1.266166 vs 0.003792, and release is +2.038803% for AB vs BA. |
| `quantum_measurement_backaction_terrain_probe_2026-07-08.md` | RAW_LOG_BACKED | Backaction probe. In stress `gamma=0`, projective measurement suppresses Bell-excess terrain signal by 100% and release by 1.149391%. |
| `quantum_fixed_basis_noise_robustness_probe_2026-07-08.md` | RAW_LOG_BACKED | Noise robustness probe. At 2048 shots/setting, stress `gamma=0` survives to 15% depolarizing, 15% phase damping, 10% amplitude damping, and 2% readout error. |
| `quantum_fixed_basis_shot_budget_probe_2026-07-08.md` | RAW_LOG_BACKED | Shot-budget sweep. Stress `gamma=0` remains positive from 32768 down to 512 shots/setting. |
| `quantum_membrane_decision_boundary_probe_2026-07-08.md` | RAW_LOG_BACKED | Membrane decision probe. Stress `gamma=0` shows A pass increase, B leak decrease, D pass decrease, and release increase. |
| `quantum_fixed_basis_adaptive_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Fixed-basis adaptive probe. Stress remains positive without per-step CHSH basis optimization. |
| `quantum_adaptive_measurement_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Adaptive feedback probe using per-step optimized CHSH bases. |
| `quantum_measurement_terrain_memory_probe_2026-07-08.md` | RAW_LOG_BACKED | Terrain-memory probe; matched replay reproduces post-write memory. |

## Latest safe finding

```text
With fixed noncommuting context probes and no direct outcome write beyond the conservative order signal, AB and BA read order diverge only in stress gamma=0. AB produces a conservative order signal, higher final terrain, and higher downstream release; BA remains at baseline. Gamma=1 and normal/storage are null. Matched replay reproduces downstream release once the order-signal trace is fixed, so specificity is at the context-order measurement boundary.
```
