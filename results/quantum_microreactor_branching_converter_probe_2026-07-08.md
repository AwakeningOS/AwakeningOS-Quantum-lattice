# Quantum Microreactor Branching Converter Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_microreactor_branching_converter_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/branching_converter_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_microreactor_branching_converter_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/branching_converter_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv
```

## Purpose

This probe tests the strongest remaining topology for quantum-specific usefulness inside the current information microreactor line:

```text
phase-dependent branching converter + entangled control
```

The motivation is that plumbing-like source, membrane, reservoir, release, and one-path transfer observables are population-only and Arm2-reproducible. If a quantum-specific effect is possible in this sandbox family, it should appear in a converter whose product composition depends on coherent path branching.

## Arms

```text
Arm 1: arm1_scalar_branch
  fixed classical 0.5 / 0.5 branch split

Arm 2: arm2_complex_wave_branch
  separable classical complex-wave branch control

Arm 3: arm3_entangled_branch
  two-qubit control+branch density matrix with entangling controlled phase
```

## Fixed branch circuit

```text
1. initialize |+>_C |0>_B
2. apply Ry(pi/2) to B
3. apply controlled phase diag(1,1,1,exp(i*pi/2))
4. apply branch phase Rz(phi)
5. apply gamma dephase in computational basis
6. apply final branch beamsplitter H on B
7. read P_main = Pr(B=0)
```

Arm2 is explicitly defined from the reduced branch state:

```text
rho_Arm2 = |0><0|_C tensor Tr_C(rho_Arm3)
```

Therefore, if the observable is branch-only, Arm2 should reproduce it whenever no nonlocal/control-conditioned observable is used.

## Gamma and phase sweep

```text
gamma = 1.0, 0.75, 0.5, 0.25, 0.0
phi   = 0, pi/2, pi
```

## Pre-registered prediction

```text
phase-sensitive branching will appear
Arm3 negativity will appear at low gamma
branch-only observables will be reproduced by Arm2
therefore the result will likely be negative for quantum-specific efficacy
```

## Verdict

```text
NEGATIVE_FOR_QUANTUM_SPECIFIC_EFFECT
```

## Main result

The phase-sensitive branching effect is large, but not quantum-specific.

Across all scenarios:

```text
total_P_release_validation_diff = 0
max_arm3_negativity = 0.353553390593
max_arm2_arm3_main_prob_abs_diff = 0
phase_sensitive_branching_effect = TRUE
arm2_reproduces_branch_observable = TRUE
negativity_changes_observable_beyond_arm2 = FALSE
quantum_specific_effect = FALSE
```

## Scenario summary

| scenario | max abs main branch shift vs gamma=1 | max Arm3 negativity | Arm2/Arm3 branch diff | phase-sensitive? | Arm2 reproduces? | quantum-specific? |
|---|---:|---:|---:|---|---|---|
| normal | 20.366591 | 0.353553 | 0 | TRUE | TRUE | FALSE |
| high_load | 49.396942 | 0.353553 | 0 | TRUE | TRUE | FALSE |
| stress | 0.031222 | 0.353553 | 0 | TRUE | TRUE | FALSE |
| stabilizer | 17.533594 | 0.353553 | 0 | TRUE | TRUE | FALSE |
| leaky_membrane | 20.372647 | 0.353553 | 0 | TRUE | TRUE | FALSE |
| road_fed | 42.919970 | 0.353553 | 0 | TRUE | TRUE | FALSE |
| storage_heavy | 9.623718 | 0.353553 | 0 | TRUE | TRUE | FALSE |

## Interpretation

This is sharper than the previous quality/coherence probe.

The converter topology does create a meaningful phase-sensitive product-composition observable:

```text
P_main : P_side changes with gamma and phi
```

Arm3 also has nonzero negativity when gamma is low:

```text
max negativity = 0.353553390593
```

But the branch observable is exactly reproduced by Arm2:

```text
max Arm2/Arm3 branch probability difference = 0
```

Therefore the result is not quantum-specific. The entanglement exists, but it does not do observable work beyond the reduced branch density matrix.

## Safe claim

```text
A phase-dependent branching converter can strongly change product composition, and an entangled Arm3 circuit can carry nonzero negativity, but the product-branch observable is fully reproduced by an Arm2 classical complex-wave control. This probe is therefore negative for quantum-specific efficacy.
```

## What this does not show

```text
not quantum advantage
not quantum-specific behavior
not functional entanglement
not hardware relevance
not chemical realism
not biological metabolism
```

## What has now been ruled out

Within the tested sandbox family, these routes are now classified as classical-effective or Arm2-reproducible:

```text
1. one-path converter coherence
2. quality-as-coherence auxiliary probe
3. branch-only phase-dependent product composition
```

## Remaining possible route

A future positive result would need a non-branch-only observable, for example:

```text
control-conditioned product readout
measurement backaction that changes release or terrain
basis-dependent quality readout that Arm2 cannot reproduce
nonlocal witness tied to reactor output
```

Without one of these, entanglement remains present but functionally unused.
