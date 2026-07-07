# Quantum Fixed-Basis Noise Robustness Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_fixed_basis_noise_robustness_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_fixed_basis_noise_robustness_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707_summary.csv
```

## Purpose

This experiment tests the fixed-basis membrane decision-boundary result under simple simulated noise models.

Prior positive:

```text
fixed-basis finite-shot CHSH signal
-> membrane decision boundary
-> A passage increases while B/D passage decreases
```

This probe fixes:

```text
shots_per_setting = 2048
margin_S = 0.374733172169
```

and sweeps:

```text
depolarizing
phase_damping
amplitude_damping
readout_error
```

Noise grid:

```text
0.0, 0.005, 0.01, 0.02, 0.05, 0.10, 0.15, 0.20
```

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_NOISE_ROBUSTNESS
```

## Main thresholds: stress gamma=0

| noise type | max positive rate | first failure rate | release dev at max positive | B leak dev at max positive | D pass dev at max positive | signal total at max positive |
|---|---:|---:|---:|---:|---:|---:|
| depolarizing | 0.15 | 0.20 | +0.040553% | -0.099983% | -2.666375% | 23.701108 |
| phase_damping | 0.15 | 0.20 | +0.026408% | -0.064046% | -2.667713% | 23.713006 |
| amplitude_damping | 0.10 | 0.15 | +0.297878% | -0.695977% | -8.741207% | 77.699614 |
| readout_error | 0.02 | 0.05 | +1.345439% | -2.952383% | -19.233312% | 170.962771 |

## Contaminated stress gamma=0

| noise type | max positive rate | first failure rate | release dev at max positive | B leak dev at max positive | D pass dev at max positive | signal total at max positive |
|---|---:|---:|---:|---:|---:|---:|
| depolarizing | 0.15 | 0.20 | +0.050923% | -0.124628% | -2.704099% | 24.036440 |
| phase_damping | 0.15 | 0.20 | +0.048895% | -0.123128% | -2.607710% | 23.179647 |
| amplitude_damping | 0.10 | 0.15 | +0.248680% | -0.603796% | -8.546200% | 75.966221 |
| readout_error | 0.02 | 0.05 | +1.435003% | -3.149419% | -19.501921% | 173.350407 |

## False-positive guard

Normal/storage false positives remain zero across the tested noise grid:

```text
false_positive_rows = 0
```

## Interpretation

Readout error is the tightest tested bottleneck:

```text
readout_error survives to 0.02 and fails by 0.05
```

Depolarizing and phase damping are less destructive on this grid:

```text
survive to 0.15 and fail by 0.20
```

Amplitude damping is intermediate:

```text
survives to 0.10 and fails by 0.15
```

## Safe claim

```text
At 2048 simulated shots per setting, the fixed-basis membrane decision-boundary effect survives stress gamma=0 through 15% depolarizing and phase-damping noise, 10% amplitude damping, and 2% readout error on the tested grid; normal/storage false positives remain zero. These are simulated thresholds, not hardware thresholds.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not ordinary local population plumbing
noise models are simple simulated channels
```

## Next boundary

```text
quantum_measurement_backaction_terrain_probe
quantum_context_order_terrain_probe
```
