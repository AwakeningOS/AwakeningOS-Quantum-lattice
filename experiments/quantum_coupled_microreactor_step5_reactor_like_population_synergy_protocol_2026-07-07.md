# Quantum-coupled Microreactor Step 5 Protocol: Reactor-like Population Synergy

Date: 2026-07-07
Layer: quantum-audit

## Question

Can a minimal M-C-R model show a pairwise-unexplained residual in a reactor-like product population?

Step 4 showed a three-body residual for abstract odd-parity population. Step 5 moves the response closer to component semantics:

```text
M = membrane/pass flag
C = converter/product flag
R = reservoir/storage flag
```

Main output:

```text
P_product_population = P(M=1, C=1, R=1)
```

This is still not a full source -> membrane -> converter -> reservoir -> sink microreactor.

## Design constraints

Mandatory constraints:

```text
1. readout is diagonal product population
2. no GHZ/Bell projector as the readout
3. pairwise controls are included
4. dephase control is included
5. no initial three-body entanglement is used
6. raw log is registered in the reproducibility gate
```

## Initial state

Use a separable coherent input:

```text
|+++>
```

Interpretation:

```text
M/C/R flags are driven coherently but not initially entangled.
```

Dephase control:

```text
computational-basis dephase of |+++><+++|
```

## Dynamics families

Pairwise single-coupling controls:

```text
U_MC = exp(-i gamma Z_M Z_C)
U_CR = exp(-i gamma Z_C Z_R)
U_MR = exp(-i gamma Z_M Z_R)
```

Pairwise product dynamics:

```text
U_pairwise = exp[-i gamma (Z_M Z_C + Z_C Z_R + Z_M Z_R)]
```

Genuine three-body dynamics:

```text
U_3body = exp(-i gamma Z_M Z_C Z_R)
```

## Readout

After dynamics, use local H rotations and computational-basis population readout:

```text
rho_out = H^⊗3 U rho U† H^⊗3
```

Main reactor-like product population:

```text
P_product_population = P(111)
```

Additional component-like metrics:

```text
conversion_success = P(C=1 and R=1)
reservoir_fill     = P(R=1)
membrane_pass      = P(M=1)
release_population = drain_rate * P_product_population
```

## Pairwise prediction

Use the same subtraction discipline as Step 4:

```text
R_pair_pred = R_MC + R_CR + R_MR - 2 R_baseline
synergy     = R_full - R_pair_pred
```

where R is `P_product_population`.

## Success pattern

A clean positive Step 5 pattern is:

```text
coherent input:
  pairwise_product synergy ≈ 0
  genuine_3body synergy > 0

dephased input:
  genuine_3body synergy collapses toward 0
```

## Forbidden claims

Do not claim:

```text
full microreactor
natural device throughput
source/sink integration
selective membrane dynamics
metabolism
quantum advantage
hardware result
life-like behavior
```

Allowed claim if passed:

```text
A minimal M-C-R reactor-like product population has zero residual under tested pairwise-product dynamics and nonzero residual under genuine three-body dynamics, while computational-basis dephase removes the residual.
```

## Next step if passed

Attach explicit source/sink and membrane/converter semantics only after preserving:

```text
diagonal product readout
pairwise-control subtraction
dephase control
biseparable/Svetlichny audit context
raw-log registration
```
