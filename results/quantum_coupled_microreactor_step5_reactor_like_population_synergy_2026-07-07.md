# Quantum-coupled Microreactor Step 5: Reactor-like Population Synergy

Date: 2026-07-07

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit`

Generator script:

```text
scripts/audit/quantum_coupled_microreactor_step5_reactor_like_population_synergy.py
```

Raw CSV log:

```text
data/quantum_microreactor/step5_reactor_like_population_synergy_seed0_summary.csv
```

Run command:

```bash
python scripts/audit/quantum_coupled_microreactor_step5_reactor_like_population_synergy.py --seed 0 --csv data/quantum_microreactor/step5_reactor_like_population_synergy_seed0_summary.csv
```

## Purpose

Step 4 showed a three-body residual for an abstract odd-parity population. Step 5 asks whether the same order/synergy discipline survives in a more reactor-like product population:

```text
M = membrane/pass flag
C = converter/product flag
R = reservoir/storage flag
```

Main output:

```text
P_product_population = P(M=1, C=1, R=1)
```

This is still not the full chain:

```text
source -> membrane -> converter -> reservoir -> sink
```

## Design constraints

This run enforces the requested constraints:

```text
1. readout is diagonal product population
2. no GHZ/Bell projector as the readout
3. pairwise controls are included
4. dephase control is included
5. no initial three-body entanglement is used
6. raw log is registered in the reproducibility gate
```

## Initial states

Coherent input:

```text
|+++>
```

This is separable, not initially entangled.

Dephase control:

```text
computational-basis dephase of |+++><+++|
```

## Dynamics compared

Single pair controls:

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

## Readout and metrics

After dynamics:

```text
rho_out = H^⊗3 U rho U† H^⊗3
```

The main readout is diagonal:

```text
P_product_population = P(111)
```

Additional reactor-like metrics:

```text
conversion_success = P(C=1 and R=1)
reservoir_fill     = P(R=1)
membrane_pass      = P(M=1)
release_population = 0.8 * P_product_population
```

## Pairwise prediction

```text
R_pair_pred = R_MC + R_CR + R_MR - 2 R_baseline
synergy     = R_full - R_pair_pred
```

where R is `P_product_population`.

## Main coherent-input sweep

| gamma/pi | dynamics | P product | conversion | reservoir fill | release | pairwise prediction | synergy |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0.000 | pairwise_product | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 0.000 | genuine_3body | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 0.125 | pairwise_product | 0.000000 | 0.125000 | 0.250000 | 0.000000 | 0.000000 | 0.000000 |
| 0.125 | genuine_3body | 0.146447 | 0.146447 | 0.146447 | 0.117157 | 0.000000 | 0.146447 |
| 0.250 | pairwise_product | 0.000000 | 0.250000 | 0.500000 | 0.000000 | 0.000000 | 0.000000 |
| 0.250 | genuine_3body | 0.500000 | 0.500000 | 0.500000 | 0.400000 | 0.000000 | 0.500000 |

## Dephase control

For dephased input, the product residual collapses to zero for both pairwise-product and genuine three-body dynamics.

At gamma/pi = 0.25:

```text
pairwise_product:
  P_product_population = 0.125
  pairwise_prediction  = 0.125
  synergy_residual_P   = 0.000

genuine_3body:
  P_product_population = 0.125
  pairwise_prediction  = 0.125
  synergy_residual_P   = 0.000
```

## Result pattern

For coherent input:

```text
pairwise_product:
  product residual = 0.0 for tested gamma values

genuine_3body:
  gamma/pi = 0.125 -> product residual 0.146447
  gamma/pi = 0.250 -> product residual 0.500000
```

The pairwise-product dynamics does change component-like marginals. For example at gamma/pi = 0.25, it reaches:

```text
conversion_success = 0.25
reservoir_fill     = 0.50
```

But it does not produce the full M=C=R=1 product population residual for the chosen readout.

## Interpretation

This is the first reactor-like population audit in this sequence:

```text
P_product_population = P(M=1,C=1,R=1)
```

The tested pairwise-product dynamics has zero residual for this product response, while genuine three-body dynamics has nonzero residual. Computational-basis dephase removes the residual.

## Critical audit note

This is still a minimal semantic model, not a full microreactor.

The dynamics is still a designed phase-interaction model with local H readout. It does not include explicit source, selective membrane kinetics, A-to-P chemical kinetics, finite reservoir capacity, or sink/release dynamics.

## Safe claim

```text
A minimal M-C-R reactor-like product population P(M=1,C=1,R=1) has zero residual under the tested pairwise-product dynamics and nonzero residual under genuine three-body dynamics; computational-basis dephase removes the residual.
```

## What this does not claim

```text
not a full microreactor
not natural device throughput
not explicit source/sink integration
not selective membrane dynamics
not metabolism
not quantum advantage
not hardware result
not life-like behavior
```

## Next step

A future Step 6 should replace the symbolic phase-interaction model with explicit component semantics:

```text
source A -> membrane pass -> converter A/P flag -> reservoir fill -> sink/release
```

while preserving:

```text
diagonal product readout
pairwise-control subtraction
dephase control
biseparable/Svetlichny audit context
raw-log gate registration
```
