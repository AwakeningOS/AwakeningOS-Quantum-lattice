# Quantum Fixed-Basis Shot Budget Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_fixed_basis_shot_budget_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_fixed_basis_shot_budget_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707_summary.csv
```

## Purpose

This experiment tests how far the fixed-basis membrane decision-boundary result can be pushed down in finite-shot budget.

Prior positive:

```text
fixed-basis finite-shot CHSH signal
-> membrane decision boundary
-> A passage increases while B/D passage decreases
```

This probe sweeps:

```text
32768, 8192, 4096, 2048, 1024, 512 shots per CHSH setting
```

## Guard

The conservative margin is recomputed for every shot budget:

```text
margin_S = 4 * sqrt(2 * log(8/alpha) / shots)
alpha = 0.001
```

A row is positive only if all are true:

```text
conservative membrane signal > 0
A pass increases
B contaminant leak decreases
D stress passage decreases
matched replay release diff = 0
```

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_SHOT_BUDGET
```

## Main result: stress gamma=0

Stress gamma=0 survives all tested shot budgets down to 512 shots/setting.

| shots | margin S | signal total | positive steps | A pass dev | B leak dev | D pass dev | release dev | effect? |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 32768 | 0.093683 | 605.133807 | 720 | +26.652139% | -18.766956% | -68.077553% | +26.652139% | TRUE |
| 8192 | 0.187367 | 528.929295 | 715 | +16.692867% | -15.566285% | -59.504546% | +16.692867% | TRUE |
| 4096 | 0.264976 | 465.743303 | 712 | +11.352929% | -13.082747% | -52.396122% | +11.352929% | TRUE |
| 2048 | 0.374733 | 373.290261 | 705 | +6.348237% | -9.168129% | -41.995154% | +6.348237% | TRUE |
| 1024 | 0.529952 | 243.223254 | 696 | +2.491365% | -4.486500% | -27.362616% | +2.491365% | TRUE |
| 512 | 0.749466 | 63.281002 | 589 | +0.156974% | -0.330297% | -7.119113% | +0.156974% | TRUE |

Minimum positive shot budget on the tested grid:

```text
512 shots per setting
```

## Contaminated stress gamma=0

The higher-B case also survives down to 512 shots/setting.

| shots | signal total | A pass dev | B leak dev | D pass dev | release dev | effect? |
|---:|---:|---:|---:|---:|---:|---|
| 32768 | 605.365395 | +26.941056% | -18.879063% | -68.077230% | +26.941056% | TRUE |
| 8192 | 529.791579 | +16.727333% | -15.806164% | -59.525184% | +16.727333% | TRUE |
| 4096 | 465.390600 | +11.452556% | -13.205751% | -52.394534% | +11.452556% | TRUE |
| 2048 | 374.035330 | +6.411884% | -9.167451% | -42.019874% | +6.411884% | TRUE |
| 1024 | 243.510611 | +2.664585% | -4.666109% | -27.397852% | +2.664585% | TRUE |
| 512 | 65.564921 | +0.212657% | -0.434749% | -7.371666% | +0.212657% | TRUE |

## Weak threshold: stress gamma=0.25

The weaker stress signal survives only at the highest tested shot budget.

| shots | signal total | positive steps | release dev | effect? |
|---:|---:|---:|---:|---|
| 32768 | 22.306860 | 666 | +0.025276% | TRUE |
| 8192 | 0.000000 | 0 | 0.000000% | FALSE |
| 4096 | 0.000000 | 0 | 0.000000% | FALSE |
| 2048 | 0.000000 | 0 | 0.000000% | FALSE |
| 1024 | 0.000000 | 0 | 0.000000% | FALSE |
| 512 | 0.000000 | 0 | 0.000000% | FALSE |

## False-positive guard

Normal and storage contexts had zero false positives across all tested shot budgets and gamma values:

```text
false_positive_rows = 0
```

This is important because low-shot sampling did not create spurious membrane decisions in normal/storage contexts.

## Replay specificity

For all rows:

```text
matched_replay_release_diff = 0
```

This preserves the previous interpretation:

```text
specificity is at the Bell-bound measurement/decision boundary
post-gate dynamics follow the gate trace
```

## Interpretation

This result is encouraging for hardware-like feasibility, with a strong caveat.

Supported chain:

```text
fixed-basis finite-shot CHSH signal
-> conservative membrane decision signal
-> A/B/D pass-block selectivity
-> downstream release/quality change
```

Strong stress gamma=0 is robust down to 512 simulated shots per setting on this grid. Weak stress gamma=0.25 is not robust and needs 32768 shots.

## Safe claim

```text
The fixed-basis membrane decision-boundary effect survives down to 512 shots per setting in stress gamma=0, while normal/storage false positives remain zero on the tested grid. The weaker stress gamma=0.25 effect survives only at 32768 shots.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not ordinary local population plumbing
512 shots is a simulated threshold, not a measured QPU threshold
```

## Next boundary

```text
quantum_fixed_basis_noise_robustness_probe
quantum_measurement_backaction_terrain_probe
quantum_context_order_terrain_probe
```
