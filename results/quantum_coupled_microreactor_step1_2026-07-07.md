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

This is a joint-state analyzer. It is not a nonlocal signaling claim. It is also not yet a natural device throughput metric; it is a deliberately chosen bond witness.

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
| 0.125 | 0.354 | 0.415 | 0.854 | 0.500 | 0.375 | 0.354 | 0.000 |
| 0.167 | 0.433 | 0.678 | 0.933 | 0.500 | 0.312 | 0.433 | 0.000 |
| 0.250 | 0.500 | 1.000 | 1.000 | 0.500 | 0.250 | 0.500 | 0.000 |
| 0.333 | 0.433 | 0.678 | 0.933 | 0.500 | 0.312 | 0.433 | 0.000 |
| 0.375 | 0.354 | 0.415 | 0.854 | 0.500 | 0.375 | 0.354 | 0.000 |
| 0.417 | 0.250 | 0.193 | 0.750 | 0.500 | 0.438 | 0.250 | 0.000 |
| 0.500 | 0.000 | 0.000 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |

## Result pattern

The dephased-correlated arm preserves the classical same-pair population:

```text
same_pair_population = 1.0
```

but its joint analyzer value stays fixed:

```text
throughput_joint(dephased_correlated) = 0.5
```

The entangled arm has a joint-analyzer bonus:

```text
throughput_joint(entangled_event) - throughput_joint(dephased_correlated)
```

For this specific construction, the bonus equals module negativity within rounding:

```text
bonus_minus_negativity = 0.0
```

## Critical audit note: bonus = N is an analytic identity

This equality is not an independent empirical discovery.

For the state

```text
|psi(theta)> = cos(theta)|c0,r0> + sin(theta)|c1,r1>
```

and the analyzer

```text
|J+> = (|c0,r0> + |c1,r1>) / sqrt(2)
```

both quantities reduce to the same analytic factor:

```text
throughput_joint(entangled) - throughput_joint(dephased) = sin(theta)cos(theta)
N(C:R) for this pure two-branch state                         = sin(theta)cos(theta)
```

Therefore `bonus = N` should be interpreted as a sanity check of the designed witness, not as an independent functional finding.

## What remains useful

The useful part is not that `bonus = N` is surprising. It is not surprising.

The useful part is that the three arms separate:

```text
independent modules:
  product_marginals

classically correlated modules:
  dephased_correlated

entangled module bond:
  entangled_event
```

and the N=0 controls do not reproduce the designed Bell-bond analyzer value. At theta/pi = 0.25:

```text
entangled_event:      N = 0.5, T_joint = 1.0
dephased_correlated: N = 0.0, T_joint = 0.5
product_marginals:   N = 0.0, T_joint = 0.25
```

This supports a narrow witness claim: the C-R bond analyzer detects a joint entangled module state under exact module-marginal matching.

## What this does not claim

```text
not a full microreactor
not source/membrane/sink integration
not nonlocal signaling
not life-like behavior
not quantum advantage
not evidence that a natural device throughput is controlled by entanglement
```

## Current safe claim

```text
A 6-qubit C-R module-bond audit shows that a designed joint analyzer distinguishes
an entangled C-R module bond from N=0 correlated and product controls under exact
module-marginal matching.
```

## Step 2 requirement

Step 2 must not reuse a Bell-target analyzer as the main functional observable.

The main observable must be defined independently from the entanglement witness, for example:

```text
reservoir-capacity perturbation -> change in conversion/release/backpressure response
```

Then test whether:

```text
entangled arm differs from dephased/product controls
response difference correlates with N(C:R)
response difference disappears under dephase
```

Only after that should the membrane module be added.
