# Quantum-coupled Microreactor Step 3 Protocol: M-C-R Svetlichny Audit

Date: 2026-07-07
Layer: quantum-audit

## Question

Can a three-module M-C-R state show a response that exceeds all biseparable / two-module-hidden descriptions?

Step 2-v2 reached the best meaningful two-module point: diagonal population readout after dynamics can witness C-R entanglement, but in a two-branch/two-module system the response remains a one-parameter coherence witness.

Step 3 therefore moves to the smallest setting where pairwise explanations can be separated from genuinely three-module structure.

## Design choice

Use Svetlichny as the main witness.

```text
primary witness: Svetlichny S
secondary state metric: bipartition negativities and geometric mean
```

Reason:

```text
Svetlichny violation has a clear biseparable bound.
It tests whether the M-C-R response exceeds all two-module-hidden / biseparable explanations.
```

## Scope

This is not a full source -> membrane -> converter -> reservoir -> sink microreactor.

It is a three-module audit witness for M-C-R inseparability.

## Module allocation

```text
M module: 1 qubit
C module: 1 qubit
R module: 1 qubit
Total:    3 qubits
```

This is intentionally minimal.

## State family

Use a GHZ-family state as the positive arm:

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

## Dynamics and readout discipline

The readout is not GHZ fidelity.

Each Svetlichny correlator is implemented as:

```text
local basis rotations
-> computational-basis population readout
-> diagonal parity calculation
```

This keeps readout diagonal after local measurement dynamics.

## Svetlichny settings

Use equatorial settings:

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

Quantum GHZ maximum:

```text
|S| = 4 * sqrt(2)
```

## Metrics

```text
N_M:CR
N_C:MR
N_R:MC
tripartite_negativity_geom
Svetlichny_S
Svetlichny_violation = max(0, |S| - 4)
Mermin_M
Mermin_violation = max(0, |M| - 2)
module-marginal audit
```

## Success pattern

A valid Step 3 positive pattern is:

```text
1. dephased and product controls have the same single-module marginals as the entangled arm
2. entangled arm has nonzero bipartition negativities
3. |Svetlichny_S| > 4 for sufficiently large theta
4. dephased and product controls do not violate the bound
5. readout is diagonal parity after local basis rotations, not GHZ-fidelity projection
```

## Forbidden claims

Do not claim:

```text
full microreactor
natural device throughput
source/sink integration
membrane dynamics
quantum advantage
hardware result
life-like behavior
```

Allowed claim if passed:

```text
A minimal M-C-R audit shows a Svetlichny violation under diagonal population readout after local basis rotations, separating genuine three-module correlation from biseparable controls.
```

## Next step if passed

Only after this should M-C-R population-dynamics synergy be attempted:

```text
whole response - pairwise response prediction
```

with diagonal readout and raw-log registration.
