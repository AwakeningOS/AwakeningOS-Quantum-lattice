# Quantum Fixed-Basis Shot Budget Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

How far can the fixed-basis membrane decision-boundary result be pushed down in finite-shot budget before the stress-context positive disappears?

This follows:

```text
quantum_membrane_decision_boundary_probe
```

That probe used a fixed CHSH basis and 32768 shots per setting. This probe sweeps the shot budget.

## Component tested

The sweep is run on the membrane decision boundary component:

```text
fixed-basis finite-shot CHSH signal
-> membrane pass/block gate
-> A passage, B contaminant leak, D stress passage
-> quality/release
```

## Shot budgets

```text
32768
8192
4096
2048
1024
512
```

The conservative Bell-bound margin changes with shot count:

```text
margin_S = 4 * sqrt(2 * log(8/alpha) / shots)
alpha = 0.001
```

## Contexts

```text
normal_membrane
stress_membrane
storage_membrane
contaminated_stress_membrane
```

## Gamma values

```text
1.0, 0.75, 0.5, 0.25, 0.0
```

## Success criteria

A shot-budget row is positive only if:

```text
1. conservative fixed-basis Bell-excess membrane signal > 0
2. A passage increases versus Bell-bound Arm2
3. B contaminant leak decreases versus Bell-bound Arm2
4. D stress passage decreases versus Bell-bound Arm2
5. matched replay reproduces downstream release
```

## False-positive criterion

A normal/storage row with membrane signal > 0 is counted as a false positive.

## Expected outputs

```text
data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707_summary.csv
data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_fixed_basis_shot_budget_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707_summary.csv
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
