# Information Microreactor Quantumized Comparison

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `classical-effective / quantum-audit boundary`

Generator script:

```text
scripts/phenomenology/information_microreactor_quantumized_comparison.py
```

Raw CSV log:

```text
data/microreactor/information_microreactor_quantumized_comparison_seed20260707_summary.csv
```

Run command:

```bash
python scripts/phenomenology/information_microreactor_quantumized_comparison.py --seed 20260707 --csv data/microreactor/information_microreactor_quantumized_comparison_seed20260707_summary.csv
```

## Question

If the finite pass / conversion / storage flags of the information microreactor sandbox are represented as quantum states, does the sandbox behavior change relative to the corresponding classical probability core?

## Scope

This is not a full quantumization of all sandbox variables.

Quantumized finite core:

```text
M = membrane pass flag
C = converter/product flag
R = reservoir/storage flag
```

Classical environment variables retained:

```text
road / terrain
membrane integrity
contaminant load
quality
reservoir amount
backpressure
stress / stabilizer rates
sink / release amount
```

## Compared modes

```text
classical_probability_core:
  P_product = p_pass * p_convert * p_store

quantum_dephased_core:
  3-qubit density matrix with dephase after every component gate

quantum_coherent_core:
  same 3-qubit component gates without dephase
```

All modes use diagonal product-population readout:

```text
P_product = P(M=1,C=1,R=1)
```

## Result summary

Across all tested scenarios, the three modes match to the stored precision.

| scenario | P release classical | P release dephased | P release coherent | coherent - classical |
|---|---:|---:|---:|---:|
| normal | 49.008664 | 49.008664 | 49.008664 | 0.000000 |
| high_load | 115.314034 | 115.314034 | 115.314034 | 0.000000 |
| stress | 0.076205 | 0.076205 | 0.076205 | 0.000000 |
| stabilizer | 42.547110 | 42.547110 | 42.547110 | 0.000000 |
| leaky_membrane | 21.388579 | 21.388579 | 21.388579 | 0.000000 |
| road_fed | 86.212309 | 86.212309 | 86.212309 | 0.000000 |
| storage_heavy | 19.520900 | 19.520900 | 19.520900 | 0.000000 |

The raw CSV also records zero difference for generated product and terrain written:

```text
diff_P_release_vs_classical = 0.0
diff_P_generated_vs_classical = 0.0
diff_terrain_vs_classical = 0.0
diff_P_release_vs_dephased = 0.0
```

## Interpretation

This is a negative/clarifying result.

For this pass-convert-store component core:

```text
Ry pass on M
controlled Ry conversion on C
controlled Ry storage on R
diagonal P111 readout
```

coherent quantum evolution, dephased quantum evolution, and the corresponding classical probability core give the same sandbox-level observables.

That means straightforward quantumization of the finite component flags does not change the current sandbox behavior.

## Why this happens

The component operations are controlled rotations whose final observable is a diagonal product population. No noncommuting witness-bearing readout or interference-sensitive device observable is used. Therefore the coherent amplitudes do not create a sandbox-level advantage over the dephased/classical probability implementation.

## Safe claim

```text
For the current diagonal pass-convert-store component core, quantum coherent, quantum dephased, and classical probability implementations produce identical sandbox summaries across the tested scenarios. The current information microreactor sandbox remains classical-effective under this straightforward finite-core quantumization.
```

## What this does not claim

```text
not a full quantum sandbox
not a no-go theorem for all possible quantum-bond replacements
not quantum advantage
not hardware result
not life-like behavior
```

## Next step

If a quantum-specific difference is desired, it must be inserted as a targeted witness-bearing submodule rather than by straightforwardly replacing diagonal pass/conversion/storage flags with qubits.

Candidate sites:

```text
membrane-converter bond
converter-reservoir bond
M-C-R joint module
```

But the classical sandbox should remain the environment/control.
