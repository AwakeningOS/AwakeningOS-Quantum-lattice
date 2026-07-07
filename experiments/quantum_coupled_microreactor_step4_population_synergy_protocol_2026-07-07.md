# Quantum-coupled Microreactor Step 4 Protocol: M-C-R Population Synergy

Date: 2026-07-07
Layer: quantum-audit

## Question

Can a diagonal population response show a three-module synergy residual that is absent under pairwise-product dynamics but present under a genuine three-body dynamics?

Step 3 established a Svetlichny witness for genuine three-module correlation. Step 4 asks a separate question: can a population response distinguish pairwise dynamics from a genuine three-body module coupling?

## Design choice

Implement both controls:

```text
A. genuine_3body dynamics
B. pairwise_product dynamics
```

Reason:

```text
A alone would leave open the objection that the response is just complexity.
B tests whether the same response appears under composed pairwise couplings.
```

## Scope

This is still not a full source -> membrane -> converter -> reservoir -> sink microreactor.

It is a three-qubit M-C-R order/synergy audit.

## Initial state

Use a separable input state:

```text
|+++>
```

This avoids building the desired response into an initially entangled GHZ state.

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

The readout is diagonal after local H rotations:

```text
U(gamma)|+++>
  -> H_M H_C H_R
  -> computational-basis population readout
  -> odd-parity population
```

Main response:

```text
R = P(odd parity after local H readout)
```

This is not GHZ fidelity and not a projector onto a GHZ state.

## Pairwise prediction

Use inclusion/additive prediction from the three single-pair controls:

```text
R_pair_pred = R_MC + R_CR + R_MR - 2 R_baseline
```

Synergy residual:

```text
synergy = R_full - R_pair_pred
```

## Success pattern

A clean Step 4 pattern is:

```text
pairwise_product dynamics:
  synergy ≈ 0

genuine_3body dynamics:
  synergy > 0
```

This would show that the chosen diagonal population response is sensitive to genuine three-body dynamics and not reproduced by the tested pairwise-product dynamics.

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
A minimal M-C-R population response has zero residual under tested pairwise-product dynamics and nonzero residual under genuine three-body dynamics, using diagonal population readout and pairwise-control subtraction.
```

## Next step if passed

Attach this order/synergy pattern to a more reactor-like component model only after preserving:

```text
diagonal readout
pairwise-control subtraction
biseparable/Svetlichny audit context
raw-log gate registration
```
