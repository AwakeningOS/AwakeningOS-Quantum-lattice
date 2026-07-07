# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_fixed_basis_shot_budget_probe
```

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
results/quantum_fixed_basis_shot_budget_probe_2026-07-08.md
experiments/quantum_fixed_basis_shot_budget_probe_protocol_2026-07-08.md
scripts/audit/quantum_fixed_basis_shot_budget_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_fixed_basis_shot_budget_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707_summary.csv
```

## Current result

```text
POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_SHOT_BUDGET
```

Key results:

```text
stress gamma=0 survives from 32768 down to 512 shots per setting
512 shots: A pass +0.156974%, B leak -0.330297%, D pass -7.119113%, release +0.156974%
normal/storage false positives: 0
stress gamma=0.25 survives only at 32768 shots; 8192 and below are zero
matched replay release diff = 0
```

## Safe claim

```text
The fixed-basis membrane decision-boundary effect survives down to 512 shots per setting in stress gamma=0, while normal/storage false positives remain zero on the tested grid. The weaker stress gamma=0.25 effect survives only at 32768 shots.
```

## Next boundary

```text
quantum_fixed_basis_noise_robustness_probe
quantum_measurement_backaction_terrain_probe
quantum_context_order_terrain_probe
```
