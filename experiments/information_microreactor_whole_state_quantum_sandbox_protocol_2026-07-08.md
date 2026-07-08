# Information Microreactor Whole-State Quantum Sandbox Protocol

Date: 2026-07-08
Layer: classical-effective / whole-state quantumization audit

## Question

If the whole information microreactor sandbox is coarse-grained into one finite state space and evolved as a coupled global state, does coherent whole-state evolution differ from dephased/classical finite-state evolution?

## Why this differs from finite-core quantumization

The previous quantumized comparison only replaced the M/C/R pass-convert-store core with qubits while keeping road, terrain, quality, contaminant load, integrity, reservoir amount, and stress/stabilizer as classical environment variables.

This experiment instead puts the main sandbox variables into one finite state:

```text
A = source/input activity
M = membrane/open integrity
C = converter/product activity
R = reservoir/fill activity
O = output/release activity
Q = quality/intact state
B = contaminant state
T = terrain/road state
D = stress/damage state
S = stabilizer/protection state
```

This is a 10-bit / 10-qubit coarse-grained whole-state sandbox.

## Compared modes

```text
classical_finite_state:
  probability vector over 2^10 states; gates act as dephased stochastic transitions

dephased_whole_state:
  same as classical finite state; included as the explicit dephase control

coherent_whole_state:
  complex state vector over 2^10 states; same controlled rotations and global couplings without dephase
```

## Dynamics

Each timestep applies:

```text
source / road drive
contaminant, stress, and stabilizer drives
membrane modulation by stabilizer, stress, contaminant, and reservoir
conversion modulation by source, membrane, quality, contaminant, and reservoir
reservoir fill by converter and membrane
release/output by reservoir and quality
quality degradation/restoration by contaminant, stress, and stabilizer
terrain writing by output and quality
global ring coupling across all state variables
```

The global ring coupling is what makes this a whole-state test rather than a local component replacement.

## Episode phases

```text
0-39: clean
40-79: contamination
80-119: pressure
120-159: stress
160-199: rescue
```

## Observables

All observables are diagonal marginals of the final state distribution or state-vector probabilities:

```text
mean_output
mean_quality
mean_output_quality
mean_reservoir
mean_membrane
mean_terrain
final_output
final_quality
final_terrain
```

Events:

```text
quality_below_0.7
quality_below_0.5
reservoir_above_0.5
membrane_below_0.5
terrain_above_0.5
output_above_0.5
```

## Scope limit

This is not a full continuous-variable quantum microreactor. It is a coarse whole-state finite-state audit.

It is also not a hardware result and not a quantum advantage claim.

## Safe claim if coherent differs

```text
A coarse whole-state quantumization of the information microreactor sandbox can differ from the dephased/classical finite-state version when the sandbox variables are evolved as one coupled global state. This is a whole-state coherence/interference effect in the finite sandbox model, not a hardware result and not a full continuous quantum microreactor.
```
