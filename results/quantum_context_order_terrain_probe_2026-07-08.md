# Quantum Context Order Terrain Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_context_order_terrain_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/context_order_terrain_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/context_order_terrain_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_context_order_terrain_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/context_order_terrain_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/context_order_terrain_probe_seed20260707_summary.csv
```

## Purpose

This experiment tests whether fixed noncommuting context-read order can change terrain and downstream release.

Previous backaction line:

```text
measurement changes the future boundary state
```

This probe asks:

```text
same boundary state
context order A -> B versus B -> A
terrain/release difference
```

## Design

Two fixed noncommuting context probes are used:

```text
context A: (C_A, B_A)
context B: (C_B, B_B)
```

They are not optimized per step.

At each step, two sequential-measurement probabilities are sampled:

```text
p_AB = probability of context B after context A
p_BA = probability of context A after context B
sampled_delta = p_AB_hat - p_BA_hat
```

The conservative order signals are:

```text
AB_signal = max(0, sampled_delta - margin)
BA_signal = max(0, -sampled_delta - margin)
```

Only this conservative order signal is written to terrain.

Settings:

```text
shots_per_order_probe = 4096
order_margin = 0.127276532414
```

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_CONTEXT_ORDER_TERRAIN
```

## P1 stress gamma=0 order effect

Result: PASS.

| scenario | gamma | AB signal total | BA signal total | AB positive steps | BA positive steps | terrain AB | terrain BA | release AB | release BA | release dev AB vs BA |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| stress_order | 0.0 | 198.363585 | 0.000000 | 683 | 0 | 1.266166 | 0.003792 | 89.280627 | 87.496741 | +2.038803% |

This is the main result:

```text
A -> B creates an order signal
B -> A does not
terrain and release diverge
```

## P2 gamma=1 null

Result: PASS.

| scenario | gamma | AB signal | BA signal | terrain dev | release dev |
|---|---:|---:|---:|---:|---:|
| normal_order | 1.0 | 0.000000 | 0.000000 | 0.000000% | 0.000000% |
| stress_order | 1.0 | 0.000000 | 0.000000 | 0.000000% | 0.000000% |
| storage_order | 1.0 | 0.000000 | 0.000000 | 0.000000% | 0.000000% |

## P3 normal/storage specificity

Result: PASS.

At gamma=0, normal and storage remain null:

| scenario | gamma | AB signal | BA signal | terrain dev | release dev |
|---|---:|---:|---:|---:|---:|
| normal_order | 0.0 | 0.000000 | 0.000000 | 0.000000% | 0.000000% |
| storage_order | 0.0 | 0.000000 | 0.000000 | 0.000000% | 0.000000% |

## P4 matched replay specificity

Result: PASS.

For the positive stress row:

```text
replay_release_diff_vs_ab = 0
```

Interpretation:

```text
post-order terrain/release dynamics follow the order-signal trace
specificity is at the context-order measurement boundary
```

## Full summary

| scenario | gamma | AB signal | BA signal | AB steps | BA steps | max sampled delta | min sampled delta | terrain AB | terrain BA | release AB | release BA | release dev | effect? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| normal_order | 1.0 | 0.000000 | 0.000000 | 0 | 0 | 0.030029 | -0.027832 | 0.182519 | 0.182519 | 406.818208 | 406.818208 | 0.000000% | FALSE |
| normal_order | 0.0 | 0.000000 | 0.000000 | 0 | 0 | 0.068359 | -0.009766 | 0.182519 | 0.182519 | 406.818208 | 406.818208 | 0.000000% | FALSE |
| stress_order | 1.0 | 0.000000 | 0.000000 | 0 | 0 | 0.030029 | -0.027832 | 0.003792 | 0.003792 | 87.496741 | 87.496741 | 0.000000% | FALSE |
| stress_order | 0.0 | 198.363585 | 0.000000 | 683 | 0 | 0.463135 | -0.003662 | 1.266166 | 0.003792 | 89.280627 | 87.496741 | +2.038803% | TRUE |
| storage_order | 1.0 | 0.000000 | 0.000000 | 0 | 0 | 0.030029 | -0.027832 | 0.036296 | 0.036296 | 80.652689 | 80.652689 | 0.000000% | FALSE |
| storage_order | 0.0 | 0.000000 | 0.000000 | 0 | 0 | 0.068359 | -0.009766 | 0.036296 | 0.036296 | 80.652689 | 80.652689 | 0.000000% | FALSE |

## Interpretation

This is the most direct order-dependence result in this sequence.

Supported chain:

```text
fixed noncommuting context probes
-> A->B and B->A have different sampled sequential probabilities
-> conservative AB order signal survives only in stress gamma=0
-> terrain differs
-> downstream release differs
```

The order signal is not a generic output boost. It is null in gamma=1 and in normal/storage.

## Safe claim

```text
With fixed noncommuting context probes and no direct outcome write beyond the conservative order signal, AB and BA read order diverge only in stress gamma=0. AB produces a conservative order signal, higher final terrain, and higher downstream release; BA remains at baseline. Gamma=1 and normal/storage are null. Matched replay reproduces downstream release once the order-signal trace is fixed, so specificity is at the context-order measurement boundary.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not proof of consciousness or observer causation
not ordinary local population plumbing
post-order reactor dynamics are classical-effective once the order trace is fixed
```

## Next boundary

The current sequence has now covered:

```text
terrain feedback
terrain memory
adaptive feedback
fixed-basis adaptive feedback
membrane decision boundary
shot-budget sweep
noise robustness
measurement backaction
context order dependence
```

The next synthesis step is to write an integrated status report separating:

```text
1. negative plumbing results
2. positive measurement-boundary results
3. hardware-likeness constraints
4. safe claims and forbidden claims
```
