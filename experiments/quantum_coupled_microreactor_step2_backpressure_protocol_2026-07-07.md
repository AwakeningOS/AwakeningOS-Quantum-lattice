# Quantum-coupled Microreactor Step 2 Protocol: Dynamic Backpressure

Date: 2026-07-07
Layer: quantum-audit

## Question

Does C-R entanglement change a backpressure/conversion response that is defined independently from the entanglement witness?

Step 1 established only a designed static C-R bond witness. Step 2 asks whether the C-R bond changes a functional response of the converter-reservoir pair.

## Design choice

Use dynamic backpressure, not a static reservoir constraint.

```text
choice: B
```

Reason:

```text
The intended device behavior is that conversion depends on downstream reservoir availability.
If R is nearly full, C->R conversion should become harder.
```

## Scope

This is still not the full chain:

```text
source -> membrane -> converter -> reservoir -> sink
```

It tests only the C-R bond with a capacity-dependent conversion/release operator.

## Module allocation

```text
C module: 3 qubits
R module: 3 qubits
Total:    6 qubits
```

Source, membrane, and sink remain classical boundary conditions or are absent.

## Arms

For each theta and reservoir capacity setting:

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

## Capacity-dependent conversion operator

The functional observable is not a Bell-target analyzer.

The model defines a conversion effect:

```text
E_convert(capacity) = K(capacity)^dagger K(capacity)
```

where the two C-R conversion paths have capacity-dependent openness:

```text
open_empty_path = capacity
open_fuller_path = capacity^2
```

The fuller reservoir branch is more strongly suppressed under low capacity.

The measured functional observables are:

```text
conversion_probability = Tr(E_convert(capacity) rho)
release_probability    = conversion_probability * drain_rate * capacity
backpressure_index     = 1 - conversion_probability(capacity) / conversion_probability(capacity=1)
```

These are device-response metrics, not entanglement-targeting projectors.

## Required audits

For every theta:

```text
rho_C(entangled_event) == rho_C(dephased_correlated)
rho_R(entangled_event) == rho_R(dephased_correlated)
```

Report marginal differences.

## Main metrics

```text
module_negativity_CR
block_S2_C
block_S2_R
conversion_probability
release_probability
same_pair_population
backpressure_index
entangled_conversion_bonus_vs_dephased
entangled_conversion_bonus_vs_product
bonus_per_negativity
```

## Success pattern

A useful Step 2 pattern is:

```text
1. module marginals match across entangled and dephased arms
2. N(C:R) > 0 only in entangled_event
3. conversion_probability or backpressure_index differs between entangled_event and dephased_correlated
4. the difference changes with capacity
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
```

Allowed claim if passed:

```text
A capacity-dependent C-R conversion response differs between an entangled C-R bond and N=0 correlated controls under module-marginal matching.
```

## Next step if passed

Add membrane module M and test whether M-C-R synergy exceeds independent component prediction while preserving the same raw-log and control discipline.
