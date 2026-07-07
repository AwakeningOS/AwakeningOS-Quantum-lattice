# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_fixed_basis_noise_robustness_probe
```

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
results/quantum_fixed_basis_noise_robustness_probe_2026-07-08.md
experiments/quantum_fixed_basis_noise_robustness_probe_protocol_2026-07-08.md
scripts/audit/quantum_fixed_basis_noise_robustness_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_fixed_basis_noise_robustness_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/fixed_basis_noise_robustness_probe_seed20260707_summary.csv
```

## Current result

```text
POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_NOISE_ROBUSTNESS
```

Key results at 2048 simulated shots per setting:

```text
stress gamma=0 survives to 15% depolarizing noise and fails by 20%
stress gamma=0 survives to 15% phase damping and fails by 20%
stress gamma=0 survives to 10% amplitude damping and fails by 15%
stress gamma=0 survives to 2% readout error and fails by 5%
normal/storage false positives = 0
```

## Safe claim

```text
At 2048 simulated shots per setting, the fixed-basis membrane decision-boundary effect survives stress gamma=0 through 15% depolarizing and phase-damping noise, 10% amplitude damping, and 2% readout error on the tested grid; normal/storage false positives remain zero. These are simulated thresholds, not hardware thresholds.
```

## Next boundary

```text
quantum_measurement_backaction_terrain_probe
quantum_context_order_terrain_probe
```
