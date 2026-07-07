# Quantum-coupled Microreactor Step 6: Explicit Component Chain Audit

Date: 2026-07-07

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit / component-semantics bridge`

Generator script:

```text
scripts/audit/quantum_coupled_microreactor_step6_explicit_component_chain.py
```

Raw CSV log:

```text
data/quantum_microreactor/step6_explicit_component_chain_seed0_summary.csv
```

Run command:

```bash
python scripts/audit/quantum_coupled_microreactor_step6_explicit_component_chain.py --seed 0 --csv data/quantum_microreactor/step6_explicit_component_chain_seed0_summary.csv
```

## Purpose

Step 5 showed a reactor-like product population using symbolic phase-interaction dynamics. Step 6 replaces that symbolic dynamics with an explicit minimal component chain:

```text
source A -> membrane pass -> converter A/P flag -> reservoir fill -> sink/release
```

This is still not the full physical or stochastic microreactor. It is a 3-qubit component-semantics bridge.

## Qubit semantics

```text
M qubit = membrane/pass flag
C qubit = converter/product flag
R qubit = reservoir/storage flag
```

State `111` means:

```text
M=1: A passed membrane
C=1: product generated
R=1: product stored
```

Main readout:

```text
P_product_population = P(M=1,C=1,R=1)
```

## Source and dephase control

Start from:

```text
|000>
```

Apply source drive:

```text
Ry(pi/2) on M
```

This creates a pass/no-pass source amplitude but no initial entanglement.

Dephase control:

```text
computational-basis dephase immediately after source drive
```

## Component operations

Converter:

```text
controlled Ry(gamma) on C, controlled by M
```

Reservoir fill:

```text
controlled Ry(gamma) on R, controlled by C
```

Leak/control pair:

```text
controlled Ry(gamma) on R, controlled by M
```

Genuine three-body boost:

```text
controlled-controlled Ry(gamma) on R, controlled by M and C
```

## Dynamics arms

```text
baseline:
  source only

pair_MC:
  source + M->C converter

pair_CR:
  source + C->R reservoir fill

pair_MR:
  source + M->R direct fill/leak control

pairwise_chain:
  source + M->C + C->R

genuine_3body_boost:
  source + M->C + C->R + MC->R three-body boost
```

## Readout metrics

All readouts are diagonal computational-basis populations:

```text
P_product_population = P(111)
conversion_success   = P(C=1)
reservoir_fill       = P(R=1)
product_stored       = P(C=1,R=1)
membrane_pass        = P(M=1)
release_population   = 0.8 * P_product_population
```

## Pairwise controls

Two predictions are tracked:

```text
pairwise_additive_prediction_P = P_MC + P_CR + P_MR - 2*P_baseline
pairwise_chain_prediction_P    = P_pairwise_chain
```

The stricter reactor-like control is `pairwise_chain_prediction_P`, because a serial component chain naturally allows pairwise M->C and C->R propagation.

## Main coherent-input sweep

| gamma/pi | dynamics | P product | conversion | reservoir fill | product stored | release | pairwise chain prediction | residual vs chain |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | pairwise_chain | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |  |  |
| 0.000 | genuine_3body_boost | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 0.250 | pairwise_chain | 0.010723 | 0.073223 | 0.010723 | 0.010723 | 0.008579 |  |  |
| 0.250 | genuine_3body_boost | 0.036612 | 0.073223 | 0.036612 | 0.036612 | 0.029289 | 0.010723 | 0.025888 |
| 0.500 | pairwise_chain | 0.125000 | 0.250000 | 0.125000 | 0.125000 | 0.100000 |  |  |
| 0.500 | genuine_3body_boost | 0.250000 | 0.250000 | 0.250000 | 0.250000 | 0.200000 | 0.125000 | 0.125000 |

## Dephase control

The dephased-after-source input gives the same product response as the coherent-after-source input for this explicit component chain.

At gamma/pi = 0.5:

```text
coherent_after_source:
  pairwise_chain P_product = 0.125
  genuine_3body_boost P_product = 0.250
  residual_vs_pairwise_chain = 0.125

dephased_after_source:
  pairwise_chain P_product = 0.125
  genuine_3body_boost P_product = 0.250
  residual_vs_pairwise_chain = 0.125
```

## Interpretation

This is an important negative/clarifying result for the quantum-audit layer.

The explicit component chain works as a minimal reactor-like semantic model:

```text
M pass -> C product -> R storage -> release metric
```

The genuine three-body boost increases the product population beyond the serial pairwise chain.

However, computational-basis dephase does not remove the boost. Therefore the boost is not a quantum-specific/coherence-dependent effect in this model. It is best interpreted as an explicit three-body component rule that can be described classically at the population level.

## Safe claim

```text
A minimal explicit M-C-R component chain produces diagonal P111 product population through pairwise M->C and C->R operations. Adding an explicit MC->R three-body boost increases product/storage/release population, but the increase survives dephase and is therefore classical-effective rather than a quantum-specific witness.
```

## What this does not claim

```text
not a full microreactor
not natural device throughput
not selective membrane material
not metabolism
not self-regulation
not quantum advantage
not hardware result
not life-like behavior
```

## Next step

The next useful branch is to split the program again:

```text
classical-effective branch:
  promote explicit component chain as a classical-effective microreactor skeleton
  add source/sink rates, finite reservoir capacity, and backpressure

quantum-witness branch:
  search for explicit component dynamics where dephase removes a P111 synergy residual
  keep diagonal readout and pairwise-chain control
```
