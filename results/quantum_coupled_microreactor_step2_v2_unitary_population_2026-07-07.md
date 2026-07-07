# Quantum-coupled Microreactor Step 2-v2: Unitary Dynamics + Diagonal Population Readout

Date: 2026-07-07

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit`

Generator script:

```text
scripts/audit/quantum_coupled_microreactor_step2_v2_unitary_population.py
```

Raw CSV log:

```text
data/quantum_microreactor/step2_v2_unitary_population_seed0_summary.csv
```

Run command:

```bash
python scripts/audit/quantum_coupled_microreactor_step2_v2_unitary_population.py --seed 0 --csv data/quantum_microreactor/step2_v2_unitary_population_seed0_summary.csv
```

## Purpose

The previous Step 2 used a capacity-dependent `conversion_effect`, but the effect at capacity 1 was equivalent to a rank-1 Bell-bond projector times `base_rate`. That means it still read coherence directly.

Step 2-v2 fixes the audit target:

```text
initial rho
  -> unitary C-R conversion dynamics
  -> diagonal product-population readout
```

The readout is now a computational-basis population after dynamics, not a Bell-target analyzer.

## Scope

This is still not the full chain:

```text
source -> membrane -> converter -> reservoir -> sink
```

It tests only the C-R submodule.

## Dynamics

Use a coherent conversion Hamiltonian in the C-R Hilbert space:

```text
|c0,r0> ---- g0(capacity) ----\
                                  > |converted_product>
|c1,r1> ---- g1(capacity) ----/
```

with:

```text
g0(capacity) = sqrt(base_rate * capacity)
g1(capacity) = sqrt(base_rate * capacity^2)
```

The fuller reservoir branch is more strongly suppressed at low capacity.

The dynamics is:

```text
rho_out = U(capacity) rho U(capacity)^dagger
U(capacity) = exp(-i H(capacity) t)
```

## Readout

The main functional readout is diagonal after dynamics:

```text
product_population_out = <converted_product|rho_out|converted_product>
```

This is the critical difference from the quarantined Step 2.

## Arms

For each theta and capacity:

```text
entangled_event:
  |psi(theta)> = cos(theta)|c0,r0> + sin(theta)|c1,r1>

dephased_correlated:
  configuration-basis dephase of entangled_event
  same rho_C/rho_R and same same-pair population
  N(C:R) = 0

product_marginals:
  rho_C(theta) tensor rho_R(theta)
  same rho_C/rho_R but no C-R correlation
  N(C:R) = 0
```

## Marginal audit

For all rows, the dephased-correlated arm has exact module-marginal matching against the entangled arm:

```text
marginal_diff_vs_entangled_C_fro = 0.0
marginal_diff_vs_entangled_R_fro = 0.0
```

Product marginals also preserve the single-module reductions by construction.

## Main result at theta/pi = 0.25

| capacity | arm | N(C:R) | product_population_out | release | backpressure |
|---:|---|---:|---:|---:|---:|
| 1.0 | entangled_event | 0.5 | 0.948400 | 0.758720 | 0.000000 |
| 1.0 | dephased_correlated | 0.0 | 0.474200 | 0.379360 | 0.000000 |
| 1.0 | product_marginals | 0.0 | 0.237100 | 0.189680 | 0.000000 |
| 0.5 | entangled_event | 0.5 | 0.520823 | 0.208329 | 0.450841 |
| 0.5 | dephased_correlated | 0.0 | 0.268077 | 0.107231 | 0.434675 |
| 0.5 | product_marginals | 0.0 | 0.134039 | 0.053615 | 0.434675 |
| 0.1 | entangled_event | 0.5 | 0.075422 | 0.006034 | 0.920475 |
| 0.1 | dephased_correlated | 0.0 | 0.047888 | 0.003831 | 0.899013 |
| 0.1 | product_marginals | 0.0 | 0.023944 | 0.001916 | 0.899013 |

## Result pattern

At theta/pi = 0.25, the entangled arm differs from the matched dephased control on a diagonal output population after conversion dynamics:

```text
capacity 1.0:
  entangled - dephased = 0.474200

capacity 0.5:
  entangled - dephased = 0.252745

capacity 0.1:
  entangled - dephased = 0.027534
```

The extra response decreases with reservoir capacity.

## Interpretation

This is the corrected Step 2 pattern:

```text
matched module marginals
N(C:R) > 0 only in entangled_event
unitary C-R dynamics converts coherence into diagonal product population
dephase removes the extra population response
capacity restriction changes both output population and backpressure index
```

The narrow safe claim is:

```text
A designed coherent C-R conversion dynamics converts C-R entanglement/coherence into a diagonal product-population response under exact module-marginal matching against N=0 controls.
```

## Critical audit note

This is still a designed toy dynamics. It does not yet prove that a natural full microreactor uses entanglement to integrate parts.

It does, however, satisfy the key correction missing from the previous Step 2:

```text
readout = diagonal population after dynamics
not a direct Bell-bond projector
```

## What this does not claim

```text
not a full microreactor
not membrane integration
not source/sink integration
not nonlocal signaling
not quantum advantage
not life-like behavior
not hardware result
```

## Next step

If this survives audit, the next meaningful direction is not to reuse coherence projectors, but to test either:

```text
1. robustness under dissipative CPTP conversion
2. M-C-R synergy with population readout and pairwise-control subtraction
```
