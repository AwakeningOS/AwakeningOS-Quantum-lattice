# Quantum-coupled Microreactor Step 1 Protocol

Date: 2026-07-07
Layer: quantum-audit

## Question

Can the converter-reservoir bond show a module-level joint response that depends on C-R entanglement after module marginals are matched against N=0 controls?

This is not the full source -> membrane -> converter -> reservoir -> sink device. It is the smallest witness-bearing subexperiment for the proposed quantum-coupled information microreactor.

## Design choice

Use event-dependent C-R coupling.

Reason:

```text
The intended meaning is not generic always-on entanglement.
The intended meaning is: when conversion and storage become one coupled event,
C and R may become a single joint state.
```

Step 1 therefore tests only the C-R module bond.

## Minimal module allocation

```text
C module: 3 qubits
R module: 3 qubits
Total:    6 qubits
```

Source and sink are not quantized in this step. Membrane is not included in this step.

## Arms

For each coupling angle theta:

```text
arm1 entangled_event:
  |psi(theta)> = cos(theta)|c0,r0> + sin(theta)|c1,r1>
  N(C:R) may be > 0

arm2 dephased_correlated:
  configuration-basis dephase of arm1
  same rho_C/rho_R and same same-pair population
  N(C:R) = 0

arm3 product_marginals:
  rho_C(theta) tensor rho_R(theta)
  same rho_C/rho_R, but no C-R correlation
  N(C:R) = 0
```

## Audit invariant

For every theta:

```text
rho_C(entangled_event) == rho_C(dephased_correlated)
rho_R(entangled_event) == rho_R(dephased_correlated)
```

The marginal difference must be reported.

## Main metrics

```text
module_negativity_CR
block_S2_C
block_S2_R
throughput_joint
same_pair_population
throughput_bonus_vs_dephased
throughput_bonus_vs_product
bonus_minus_negativity
marginal_diff_vs_entangled_C_fro
marginal_diff_vs_entangled_R_fro
```

## Joint analyzer

Use a designed C-R joint analyzer:

```text
|J+> = (|c0,r0> + |c1,r1>) / sqrt(2)
throughput_joint = <J+|rho|J+>
```

This is a joint-state analyzer, not a nonlocal signaling test.

## Success pattern

The strongest Step 1 pattern is:

```text
marginal_diff(entangled, dephased) = 0
N(C:R) > 0 for entangled_event
N(C:R) = 0 for dephased_correlated
throughput_joint(entangled) > throughput_joint(dephased)
throughput_bonus_vs_dephased tracks N(C:R)
```

## Controls

```text
dephased_correlated:
  same module marginals and same classical same-pair population, but no entanglement

product_marginals:
  same module marginals, but no C-R correlation
```

These controls separate:

```text
independent modules
classically correlated modules
entangled modules
```

## Forbidden claims

Do not claim:

```text
full microreactor behavior
nonlocal signaling
life-like behavior
quantum advantage
source-sink-membrane integration
```

Allowed claim if the test passes:

```text
A designed C-R module-bond analyzer shows an entanglement-dependent joint response
under exact module-marginal matching against a dephased N=0 control.
```

## Next steps if passed

```text
Step 2: add reservoir capacity/backpressure perturbation
Step 3: add membrane module M
Step 4: compare full M-C-R synergy against independent predictions
Step 5: dephase/noise controls and only then possible hardware candidate
```
