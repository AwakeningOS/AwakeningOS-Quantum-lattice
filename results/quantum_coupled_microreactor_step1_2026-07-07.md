# Quantum-coupled Microreactor Step 1: C-R Module Bond

Date: 2026-07-07

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit`

Generator script:

```text
scripts/audit/quantum_coupled_microreactor_step1.py
```

Raw CSV log:

```text
data/quantum_microreactor/step1_cr_coupling_seed0_summary.csv
```

Run command:

```bash
python scripts/audit/quantum_coupled_microreactor_step1.py --seed 0 --csv data/quantum_microreactor/step1_cr_coupling_seed0_summary.csv
```

## Purpose

This is Step 1 for the proposed quantum-coupled information microreactor.

It does not yet test the full chain:

```text
source -> membrane -> converter -> reservoir -> sink
```

It tests only the smallest witness-bearing bond:

```text
converter C -> reservoir R
```

## Design choice

Use event-dependent C-R coupling rather than always-on generic entanglement.

Reason:

```text
The intended object is conversion-and-storage as one coupled event.
```

## Module allocation

```text
C module: 3 qubits
R module: 3 qubits
Total:    6 qubits
```

Source, membrane, and sink are not included in this step.

## Arms

For each coupling angle theta:

```text
entangled_event:
  |psi(theta)> = cos(theta)|c0,r0> + sin(theta)|c1,r1>
  N(C:R) may be > 0

dephased_correlated:
  configuration-basis dephase of entangled_event
  same rho_C/rho_R and same same-pair population
  N(C:R) = 0

product_marginals:
  rho_C(theta) tensor rho_R(theta)
  same rho_C/rho_R but no C-R correlation
  N(C:R) = 0
```

## Joint analyzer

The joint C-R analyzer is:

```text
|J+> = (|c0,r0> + |c1,r1>) / sqrt(2)
throughput_joint = <J+|rho|J+>
```

This is a joint-state analyzer. It is not a nonlocal signaling claim.

## Marginal audit

For all theta values, the entangled arm and dephased-correlated arm have exact module-marginal matching:

```text
rho_C_frobenius_diff = 0.0
rho_R_frobenius_diff = 0.0
```

The product-marginals arm also has the same single-module reductions by construction.

## Main sweep

| theta/pi | N(C:R) entangled | S2(C) | T_joint entangled | T_joint dephased | T_joint product | bonus vs dephased | bonus - N |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | 0.000 | 0.000 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |
| 0.083 | 0.250 | 0.193 | 0.750 | 0.500 | 0.438 | 0.250 | 0.000 |
| 0.125 | 0.354 | 0.601 | 0.854 | 0.500 | 0.375 | 0.354 | 0.000 |
| 0.167 | 0.433 | 0.811 | 0.933 | 0.500 | 0.312 | 0.433 | 0.000 |
| 0.250 | 0.500 | 1.000 | 1.000 | 0.500 | 0.250 | 0.500 | 0.000 |
| 0.333 | 0.433 | 0.811 | 0.933 | 0.500 | 0.312 | 0.433 | 0.000 |
| 0.375 | 0.354 | 0.601 | 0.854 | 0.500 | 0.375 | 0.354 | 0.000 |
| 0.417 | 0.250 | 0.193 | 0.750 | 0.500 | 0.438 | 0.250 | 0.000 |
| 0.500 | 0.000 | 0.000 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |

## Result pattern

The dephased-correlated arm preserves the classical same-pair population:

```text
same_pair_population = 1.0
```

but its joint throughput stays fixed:

```text
throughput_joint(dephased_correlated) = 0.5
```

The entangled arm has a bonus:

```text
throughput_joint(entangled_event) - throughput_joint(dephased_correlated)
```

and this bonus equals module negativity within rounding:

```text
bonus_minus_negativity = 0.0
```

## Interpretation

This is the first Step 1 C-R bond witness:

```text
matched module marginals
N(C:R) > 0 in the entangled arm
N(C:R) = 0 in the dephased-correlated control
joint throughput bonus tracks N(C:R)
```

The result separates three levels:

```text
independent modules:
  product_marginals

classically correlated modules:
  dephased_correlated

entangled module bond:
  entangled_event
```

The classical correlated control is not zero. That is important: classical coupling already produces a coupled device-like baseline. The entangled bond adds a joint-analyzer bonus above that baseline.

## What this does not claim

```text
not a full microreactor
not source/membrane/sink integration
not nonlocal signaling
not life-like behavior
not quantum advantage
```

## Current safe claim

```text
A 6-qubit C-R module-bond audit shows an entanglement-dependent joint response
under exact module-marginal matching against a dephased N=0 correlated control.
```

## Next step

Step 2 should add a reservoir-capacity/backpressure perturbation while preserving the same three-arm discipline:

```text
product / dephased-correlated / entangled
module-marginal audit
N(C:R)
throughput/backpressure response
```

Only after Step 2 should the membrane module be added.
