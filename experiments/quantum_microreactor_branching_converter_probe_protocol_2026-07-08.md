# Quantum Microreactor Branching Converter Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

After the one-path converter and quality/coherence probes returned classical-effective or Arm2-reproducible behavior, does a phase-dependent branching converter produce a quantum-specific observable effect?

The tested idea is:

```text
A converter has two product exits: P_main and P_side.
A coherent phase can change the P_main:P_side branching ratio.
An entangled control qubit can create Arm3 negativity.
```

The hard question is not whether phase changes a branch ratio. The hard question is whether Arm3 changes a branch observable that Arm2 classical complex-wave control cannot reproduce.

## Prior findings motivating this protocol

```text
1. gamma=max validation passed for the scalar sandbox.
2. one-path quantumized M/C/R finite core did not change sandbox summaries.
3. quality-as-coherence gamma sweep produced a coherence/negativity proxy, but Arm2 reproduced it and no existing observable changed.
```

This protocol therefore stops quantizing plumbing and tests only the converter branching topology.

## Layer

```text
quantum-audit probe
```

This is not a component-layer result and not a quantum-specific positive unless Arm3 survives Arm2 control.

## Arms

```text
Arm 1: arm1_scalar_branch
  classical branch ratio fixed at 0.5 / 0.5

Arm 2: arm2_complex_wave_branch
  separable classical complex-wave branch control
  reproduces branch-only interference without entanglement

Arm 3: arm3_entangled_branch
  two-qubit control+branch density matrix
  entangling controlled phase creates negativity when gamma is low
```

## Circuit / probe structure

The branch probe uses two qubits:

```text
C = control qubit
B = branch qubit where B=0 means P_main and B=1 means P_side
```

Fixed circuit:

```text
1. initialize |+>_C |0>_B
2. apply Ry(pi/2) to B to create a balanced branch superposition
3. apply controlled phase diag(1,1,1,exp(i*pi/2)) to entangle C and B
4. apply branch phase Rz(phi) on B
5. apply dephase gamma in the computational basis
6. apply a final branch beam splitter H on B
7. read P_main = Pr(B=0)
```

Arm2 is defined as the separable reduced-branch control:

```text
rho_Arm2 = |0><0|_C tensor Tr_C(rho_Arm3)
```

This makes the Arm2 trap explicit: any branch-only observable that depends only on the reduced branch density matrix is classical-wave reproducible.

## Gamma values

```text
gamma = 1.0
0.75
0.50
0.25
0.0
```

## Phase values

```text
phi = 0
phi = pi/2
phi = pi
```

## Validation rule

The total scalar sandbox release is never changed in this probe:

```text
P_release_total = existing scalar P_release
P_main_release + P_side_release = P_release_total
```

At gamma=1, all arms reduce to the fixed classical branch ratio:

```text
P_main = P_side = 0.5 * P_release_total
```

## Observables

```text
total_P_release
main_branch_prob
side_branch_prob
main_P_release
side_P_release
branch_shift_vs_gamma1
Arm3 negativity
Arm2 vs Arm3 branch observable difference
```

## Success criteria for quantum-specific usefulness

A positive quantum-specific result requires all:

```text
1. gamma or phi changes P_main:P_side branch ratio
2. Arm3 has negativity > 0
3. Arm3 branch observable differs from Arm2 branch observable
4. the difference changes an observable such as main_P_release or quality-weighted release
```

## Negative criteria

The result is not quantum-specific if:

```text
1. phase changes the branch ratio but Arm2 reproduces it
2. Arm3 has negativity but branch-only observables match Arm2
3. total release remains validated but only product composition changes in an Arm2-reproducible way
```

## Pre-registered prediction

Prediction before running:

```text
phase-sensitive branching will appear
Arm3 negativity will appear at low gamma
branch-only observables will be reproduced by Arm2
therefore the result will likely be classical-effective / negative for quantum-specific efficacy
```

## Expected raw outputs

Canonical raw log:

```text
data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/branching_converter_probe_seed20260707.json
```

The script can also regenerate a compact branch detail table internally, but the canonical committed raw log for this result is the summary CSV because all reported claims are summary-level claims.

## Run command

```bash
python scripts/audit/quantum_microreactor_branching_converter_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/branching_converter_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv
```

## Forbidden claims

Do not claim:

```text
quantum advantage
quantum-specific behavior
functional entanglement
hardware relevance
chemical realism
biological metabolism
```

unless the Arm2 control fails to reproduce an Arm3 observable effect.
