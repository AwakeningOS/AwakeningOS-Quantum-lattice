# Quantum-coupled Microreactor Step 4: M-C-R Population Synergy

Date: 2026-07-07

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit`

Generator script:

```text
scripts/audit/quantum_coupled_microreactor_step4_population_synergy.py
```

Raw CSV log:

```text
data/quantum_microreactor/step4_population_synergy_seed0_summary.csv
```

Run command:

```bash
python scripts/audit/quantum_coupled_microreactor_step4_population_synergy.py --seed 0 --csv data/quantum_microreactor/step4_population_synergy_seed0_summary.csv
```

## Purpose

Step 3 established a three-module Svetlichny witness. Step 4 asks a separate functional-order question:

```text
Can a diagonal population response show a three-module residual that is absent under pairwise-product dynamics but present under genuine three-body dynamics?
```

This is still not the full chain:

```text
source -> membrane -> converter -> reservoir -> sink
```

It is a minimal M-C-R population-order audit.

## Initial state

The input is separable:

```text
|+++>
```

The desired response is not built into an initially entangled GHZ state.

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

## Readout

The response is diagonal after local H rotations:

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

The pairwise additive prediction is:

```text
R_pair_pred = R_MC + R_CR + R_MR - 2 R_baseline
```

Synergy residual:

```text
synergy = R_full - R_pair_pred
```

## Main sweep

| gamma/pi | dynamics | odd parity population | pairwise prediction | synergy residual | p000 |
|---:|---|---:|---:|---:|---:|
| 0.0000 | pairwise_product | 0.000000 | 0.000000 | 0.000000 | 1.000000 |
| 0.0000 | genuine_3body | 0.000000 | 0.000000 | 0.000000 | 1.000000 |
| 0.0625 | pairwise_product | 0.000000 | 0.000000 | 0.000000 | 0.890165 |
| 0.0625 | genuine_3body | 0.038060 | 0.000000 | 0.038060 | 0.961940 |
| 0.1250 | pairwise_product | 0.000000 | 0.000000 | 0.000000 | 0.625000 |
| 0.1250 | genuine_3body | 0.146447 | 0.000000 | 0.146447 | 0.853553 |
| 0.2500 | pairwise_product | 0.000000 | 0.000000 | 0.000000 | 0.250000 |
| 0.2500 | genuine_3body | 0.500000 | 0.000000 | 0.500000 | 0.500000 |

## Result pattern

The tested pairwise-product dynamics does change the detailed readout distribution, for example `p000_after_readout` drops from 1.0 to 0.25 at gamma/pi = 0.25.

But for the chosen diagonal odd-parity response:

```text
pairwise_product synergy_residual_odd = 0.0
```

for all tested gamma values.

The genuine three-body dynamics gives a nonzero residual:

```text
gamma/pi = 0.0625 -> synergy 0.038060
gamma/pi = 0.1250 -> synergy 0.146447
gamma/pi = 0.2500 -> synergy 0.500000
```

## Interpretation

This is the first population-order audit where both branches requested by the design are present:

```text
B. pairwise-product dynamics -> zero residual for the chosen response
A. genuine three-body dynamics -> nonzero residual for the chosen response
```

The readout is diagonal population after local H rotations, and the residual is computed by subtracting the additive pairwise prediction.

## Critical audit note

This is still a designed order/synergy witness. It is not natural device throughput and not full microreactor behavior.

The safe claim is:

```text
A minimal M-C-R diagonal odd-parity population response has zero residual under the tested pairwise-product dynamics and nonzero residual under genuine three-body dynamics, using pairwise-control subtraction.
```

## What this does not claim

```text
not a full microreactor
not natural device throughput
not source/sink integration
not membrane dynamics
not quantum advantage
not hardware result
not life-like behavior
```

## Next step

The next stage should attach the same order/synergy discipline to a more reactor-like population response:

```text
whole population response - pairwise response prediction
```

while keeping:

```text
diagonal readout
pairwise-control subtraction
biseparable/Svetlichny audit context
raw-log gate registration
```
