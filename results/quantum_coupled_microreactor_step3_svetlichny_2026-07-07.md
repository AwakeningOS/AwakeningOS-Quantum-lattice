# Quantum-coupled Microreactor Step 3: M-C-R Svetlichny Audit

Date: 2026-07-07

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit`

Generator script:

```text
scripts/audit/quantum_coupled_microreactor_step3_svetlichny.py
```

Raw CSV log:

```text
data/quantum_microreactor/step3_svetlichny_seed0_summary.csv
```

Run command:

```bash
python scripts/audit/quantum_coupled_microreactor_step3_svetlichny.py --seed 0 --csv data/quantum_microreactor/step3_svetlichny_seed0_summary.csv
```

## Purpose

Step 2-v2 showed the best meaningful two-module result: a coherent C-R conversion dynamics can convert C-R coherence into a diagonal output population. But in a two-branch/two-module system, the response is still one-parameter and cannot separate function from the single available coherence witness.

Step 3 moves to the smallest setting where the question of pairwise explanation becomes nontrivial:

```text
M-C-R
```

The primary witness is Svetlichny violation, not GHZ fidelity.

## Scope

This is not the full chain:

```text
source -> membrane -> converter -> reservoir -> sink
```

It is a three-module audit witness.

## State family

Positive arm:

```text
|psi(theta)> = cos(theta)|000> + sin(theta)|111>
```

Controls:

```text
dephased_correlated:
  configuration-basis dephase of |psi(theta)><psi(theta)|
  same single-module marginals and same classical 000/111 correlation

product_marginals:
  rho_M(theta) tensor rho_C(theta) tensor rho_R(theta)
  same single-module marginals but no module correlation
```

## Readout discipline

This report does not use GHZ-fidelity projection as the main readout.

Each Svetlichny correlator is measured as:

```text
local basis rotations
-> computational-basis population readout
-> diagonal parity calculation
```

The `readout` field in the raw CSV is:

```text
diagonal_parity_after_local_basis_rotations
```

## Svetlichny settings

```text
M0 = X
M1 = Y
C0 = X
C1 = Y
R0 = (X - Y) / sqrt(2)
R1 = (X + Y) / sqrt(2)
```

Svetlichny expression:

```text
S = E000 + E001 + E010 - E011 + E100 - E101 - E110 - E111
```

Biseparable bound:

```text
|S| <= 4
```

## Main sweep

| theta/pi | arm | N geom | Svetlichny | violation | Mermin |
|---:|---|---:|---:|---:|---:|
| 0.000 | entangled_GHZ | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.000 | dephased_correlated | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.000 | product_marginals | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.083 | entangled_GHZ | 0.250 | 2.828 | 0.000 | 2.000 |
| 0.083 | dephased_correlated | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.083 | product_marginals | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.125 | entangled_GHZ | 0.354 | 4.000 | 0.000 | 2.828 |
| 0.125 | dephased_correlated | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.125 | product_marginals | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.167 | entangled_GHZ | 0.433 | 4.899 | 0.899 | 3.464 |
| 0.167 | dephased_correlated | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.167 | product_marginals | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.250 | entangled_GHZ | 0.500 | 5.657 | 1.657 | 4.000 |
| 0.250 | dephased_correlated | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.250 | product_marginals | 0.000 | 0.000 | 0.000 | 0.000 |

## Result pattern

For theta/pi = 0.25:

```text
entangled_GHZ:
  Svetlichny_S = 5.656854
  biseparable bound = 4.0
  violation = 1.656854
  tripartite negativity geom = 0.5

dephased_correlated:
  Svetlichny_S = 0.0
  violation = 0.0

product_marginals:
  Svetlichny_S = 0.0
  violation = 0.0
```

The violation begins above the biseparable bound for theta/pi > 0.125. At theta/pi = 0.125 the value reaches the bound but does not exceed it.

## Interpretation

This is the first M-C-R audit that directly targets the two-module-hidden / biseparable boundary:

```text
readout is diagonal parity after local basis rotations
Svetlichny violation exceeds the biseparable bound only in the entangled arm
dephased and product controls do not violate
bipartition negativities co-vary with the violation
```

This is stronger than a GHZ-fidelity check because the primary threshold is an inequality bound:

```text
|S| <= 4 for biseparable descriptions
```

## Critical audit note

This is still a witness experiment, not device throughput and not full microreactor behavior.

It answers a narrower question:

```text
Can M-C-R exhibit a three-module correlation that cannot be reduced to biseparable / two-module-hidden structure?
```

For the tested GHZ-family state and settings, yes.

## What this does not claim

```text
not a full microreactor
not source/sink integration
not membrane dynamics
not natural device throughput
not quantum advantage
not hardware result
not life-like behavior
```

## Next step

Only after this survives audit should the next stage attempt true M-C-R synergy:

```text
whole population response - pairwise response prediction
```

That next stage must preserve:

```text
diagonal readout
pairwise-control subtraction
Svetlichny or biseparable-bound audit
raw-log gate registration
```
