# Quantum-coupled Microreactor Step 2-v2 Protocol: Unitary Dynamics + Diagonal Population Readout

Date: 2026-07-07
Layer: quantum-audit

## Question

Can C-R entanglement change a functional output population after actual C-R conversion dynamics, when the final readout is diagonal in the computational basis?

This protocol replaces the previous Step 2 capacity-effect model because its conversion effect was a rank-1 coherence/Bell-like projector in disguise.

## Core correction

Previous Step 2 failure mode:

```text
conversion_effect(capacity=1) == base_rate * Step1 Bell-bond projector
```

Therefore the previous conversion bonus read coherence directly and did not satisfy the independent-observable requirement.

Step 2-v2 moves coherence sensitivity into the dynamics and makes the final readout diagonal:

```text
initial rho
  -> unitary C-R conversion dynamics U(capacity)
  -> diagonal population readout on converted output state
```

## Scope

This is still not the full chain:

```text
source -> membrane -> converter -> reservoir -> sink
```

It tests only the C-R submodule.

## Module allocation

```text
C module: 3 qubits
R module: 3 qubits
Total:    6 qubits
```

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

## Conversion dynamics

Use a 3-state coherent conversion Hamiltonian inside the 64-dimensional C-R Hilbert space:

```text
|c0,r0> ---- g0(capacity) ----\
                                  > |converted_product>
|c1,r1> ---- g1(capacity) ----/
```

where:

```text
g0(capacity) = sqrt(base_rate * capacity)
g1(capacity) = sqrt(base_rate * capacity^2)
```

The fuller reservoir branch is more strongly suppressed at low capacity.

Time evolution:

```text
rho_out = U(capacity) rho U(capacity)^dagger
U(capacity) = exp(-i H(capacity) t)
```

## Readout

The main readout is diagonal after dynamics:

```text
product_population_out = <converted_product|rho_out|converted_product>
```

This is the key audit requirement.

Coherence may affect the result only by being converted into population by the dynamics, not by a final Bell-target projector.

## Metrics

```text
module_negativity_CR
block_S2_C
block_S2_R
product_population_out
release_probability
same_pair_population_in
backpressure_index
entangled_population_bonus_vs_dephased
entangled_population_bonus_vs_product
bonus_per_negativity
marginal_diff_vs_entangled_C_fro
marginal_diff_vs_entangled_R_fro
```

## Success pattern

A useful Step 2-v2 pattern is:

```text
1. module marginals match across entangled and dephased arms
2. N(C:R) > 0 only in entangled_event
3. final diagonal product population differs between entangled_event and dephased_correlated
4. capacity changes the population response and the entangled bonus
5. dephase removes the extra response
```

## Forbidden claims

Do not claim:

```text
full microreactor
membrane integration
source/sink integration
nonlocal signaling
quantum advantage
life-like behavior
hardware result
```

Allowed claim if passed:

```text
A coherent C-R conversion dynamics converts C-R coherence/entanglement into a diagonal product population response under exact module-marginal matching against N=0 controls.
```

## Next step if passed

Only after this survives audit should M-C-R synergy be tested.
