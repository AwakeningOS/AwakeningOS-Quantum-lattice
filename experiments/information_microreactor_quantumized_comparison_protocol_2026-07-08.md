# Information Microreactor Quantumized Comparison Protocol

Date: 2026-07-08
Layer: classical-effective / quantum-audit boundary

## Question

If the finite pass / conversion / storage flags of the information microreactor sandbox are represented as quantum states, does the sandbox behavior change relative to the corresponding classical probability core?

## Important scope limit

This is not a full quantumization of every scalar/environment variable.

The following remain classical environment variables:

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

The finite component core is quantumized:

```text
M = membrane pass flag
C = converter/product flag
R = reservoir/storage flag
```

## Compared modes

```text
classical_probability_core:
  P_product = p_pass * p_convert * p_store

quantum_dephased_core:
  3-qubit density matrix with source/pass, converter, and storage gates
  computational-basis dephase after every component gate

quantum_coherent_core:
  same 3-qubit component gates without dephase
```

All modes use diagonal product-population readout:

```text
P_product = P(M=1,C=1,R=1)
```

## Component mapping

At each timestep:

```text
p_pass    = membrane permeability for A
p_convert = converter probability after poison and backpressure
p_store   = available reservoir fraction
```

The quantum core implements:

```text
Ry(p_pass) on M
controlled Ry(p_convert) on C, controlled by M
controlled Ry(p_store) on R, controlled by C
```

where each rotation angle is chosen so that `sin^2(theta/2) = p`.

## Scenarios

```text
normal
high_load
stress
stabilizer
leaky_membrane
road_fed
storage_heavy
```

## Expected audit logic

Because the operations are controlled rotations and the readout is diagonal in the product basis, this is expected to be classically simulable. If coherent and dephased results match the classical probability core, the correct conclusion is:

```text
straightforward quantumization of the finite component flags does not change sandbox behavior
```

This is a valid negative/clarifying result.

## Forbidden claims

Do not claim:

```text
quantum advantage
quantum-specific microreactor behavior
full quantum sandbox
hardware result
life-like behavior
```

Allowed claim if results match:

```text
For this diagonal pass-convert-store component core, coherent quantum, dephased quantum, and classical probability implementations produce the same sandbox-level observables. Any future quantum-specific effect must introduce a nonclassical witness-bearing submodule beyond this straightforward diagonal component quantumization.
```
