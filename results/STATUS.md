# Results reproducibility status

Date: 2026-07-08

## Current latest session

```text
quantum_measurement_backaction_terrain_probe
```

Backed by:

```text
scripts/audit/quantum_measurement_backaction_terrain_probe.py
data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707_summary.csv
results/quantum_measurement_backaction_terrain_probe_2026-07-08.md
```

Status:

```text
RAW_LOG_BACKED
POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_BACKACTION_TERRAIN
```

Scope:

```text
positive for simulated measurement backaction altering later terrain/release in stress gamma=0
suppressive effect: measurement lowers Bell-excess terrain signal and release
normal/storage and gamma=1 remain unchanged
not a hardware result
```

## Current results/ classification

| file | status | action |
|---|---|---|
| `quantum_measurement_backaction_terrain_probe_2026-07-08.md` | RAW_LOG_BACKED | Latest backaction probe. In stress `gamma=0`, projective measurement suppresses Bell-excess terrain signal by 100%, final terrain by 99.958308%, and release by 1.149391%; gentle measurement suppresses signal by 33.013319%, terrain by 32.333922%, and release by 0.635817%. |
| `quantum_fixed_basis_noise_robustness_probe_2026-07-08.md` | RAW_LOG_BACKED | Noise robustness probe. At 2048 shots/setting, stress `gamma=0` survives to 15% depolarizing, 15% phase damping, 10% amplitude damping, and 2% readout error. |
| `quantum_fixed_basis_shot_budget_probe_2026-07-08.md` | RAW_LOG_BACKED | Shot-budget sweep. Stress `gamma=0` remains positive from 32768 down to 512 shots/setting. |
| `quantum_membrane_decision_boundary_probe_2026-07-08.md` | RAW_LOG_BACKED | Membrane decision probe. Stress `gamma=0` shows A pass increase, B leak decrease, D pass decrease, and release increase. |
| `quantum_fixed_basis_adaptive_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Fixed-basis adaptive probe. Stress remains positive without per-step CHSH basis optimization. |
| `quantum_adaptive_measurement_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Adaptive feedback probe using per-step optimized CHSH bases. |
| `quantum_measurement_terrain_memory_probe_2026-07-08.md` | RAW_LOG_BACKED | Terrain-memory probe; matched replay reproduces post-write memory. |

## Latest safe finding

```text
In stress gamma=0, invasive measurement of the boundary state suppresses later Bell-excess terrain signal and lowers downstream release after measurement stops being treated as a passive readout. The effect is backaction-like and negative/suppressive: measurement changes the future boundary state rather than merely reporting it. Normal/storage and gamma=1 null rows remain unchanged.
```
