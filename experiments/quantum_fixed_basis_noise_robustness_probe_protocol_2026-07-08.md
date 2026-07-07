# Quantum Fixed-Basis Noise Robustness Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

How robust is the fixed-basis membrane decision-boundary effect under simple simulated noise models?

This follows:

```text
quantum_fixed_basis_shot_budget_probe
```

That probe found that the strong stress gamma=0 membrane decision signal survives down to 512 simulated shots per setting on the tested grid. This probe fixes shots at 2048 and sweeps simple noise channels.

## Component tested

```text
fixed-basis finite-shot CHSH signal
-> conservative membrane decision signal
-> A/B/D pass-block selectivity
-> downstream release/quality change
```

## Fixed settings

```text
shots_per_setting = 2048
alpha = 0.001
margin_S = 0.374733172169
fixed CHSH basis pre-calibrated at phi=pi, gamma=0
```

## Noise models

```text
depolarizing
phase_damping
amplitude_damping
readout_error
```

Noise rates:

```text
0.0, 0.005, 0.01, 0.02, 0.05, 0.10, 0.15, 0.20
```

## Success criteria

A row remains positive only if:

```text
conservative membrane signal > 0
A passage increases
B contaminant leak decreases
D stress passage decreases
matched replay release diff = 0
```

## False-positive criterion

Normal/storage rows with conservative membrane signal > 0 are counted as false positives.

## Expected outputs

```text
data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707_summary.csv
data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_fixed_basis_noise_robustness_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707_summary.csv
```

## Forbidden claims

Do not claim:

```text
hardware result
chemical realism
biological metabolism
universal quantum advantage
ordinary local population plumbing is quantum-specific
```
