# Quantum Context Order Terrain Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

Can the order of noncommuting context reads change terrain and later release?

This follows:

```text
quantum_measurement_backaction_terrain_probe
```

The backaction probe showed that measurement can change the future boundary state. This probe asks a stricter order question:

```text
same boundary state
context order A -> B versus B -> A
terrain/release difference
```

## Context probes

Two fixed noncommuting context probes are used. Their axes are preselected and then fixed:

```text
context A: (C_A, B_A)
context B: (C_B, B_B)
```

They are not optimized per step.

## Signal rule

At each step, two sequential nonselective measurement probabilities are sampled:

```text
p_AB = probability of context B after context A
p_BA = probability of context A after context B
sampled_delta = p_AB_hat - p_BA_hat
```

The order signal is conservative:

```text
AB_signal = max(0, sampled_delta - margin)
BA_signal = max(0, -sampled_delta - margin)
```

Only the conservative order signal is written to terrain.

## Shot setting

```text
shots_per_order_probe = 4096
order_margin = 0.127276532414
```

## Arms

```text
AB_order:
  context A then context B

BA_order:
  context B then context A

matched replay:
  replay the AB order-signal trace and check downstream reproduction
```

## Success criteria

A model-level context-order positive requires:

```text
1. AB and BA use the same boundary state and fixed context probes
2. stress gamma=0 produces AB order signal but not BA order signal
3. final terrain differs between AB and BA
4. downstream release differs between AB and BA
5. gamma=1 null remains zero
6. normal/storage remain zero
7. matched replay reproduces downstream release once the order-signal trace is fixed
```

## Expected outputs

```text
data/quantum_microreactor/context_order_terrain_probe_seed20260707_summary.csv
data/quantum_microreactor/context_order_terrain_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_context_order_terrain_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/context_order_terrain_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/context_order_terrain_probe_seed20260707_summary.csv
```

## Forbidden claims

Do not claim:

```text
hardware result
chemical realism
biological metabolism
universal quantum advantage
proof of consciousness or observer causation
ordinary local population plumbing is quantum-specific
```
