# Quantum Microreactor CHSH Readout Transport Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_microreactor_chsh_readout_transport_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/chsh_readout_transport_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_microreactor_chsh_readout_transport_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/chsh_readout_transport_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv
```

## Purpose

This experiment tests the next logical step after the transported branching Arm2-kill result.

Previous result:

```text
local population transport can move strongly, but it is fully reduced-Arm2-reproducible
```

New test:

```text
add a joint / noncommutative CHSH readout component
use Bell violation itself to drive transported release above the local-classical ceiling
```

## False-positive protection

A single-basis correlation such as:

```text
<Z_C Z_B>
```

is not enough, because classical correlated variables can reproduce it.

Therefore the readout is based on the CHSH bound:

```text
local / separable / classical-correlated systems: S_CHSH <= 2
quantum systems: S_CHSH can exceed 2 up to 2*sqrt(2)
```

The classical release ceiling is:

```text
yb_classical_ceiling = 1 / sqrt(2)
```

The CHSH readout is:

```text
yb = max(2, S_CHSH) / (2 * sqrt(2))
```

Thus only CHSH violation can exceed the classical ceiling.

## Tested scenarios

```text
normal
stress
storage_heavy
```

The reactor context phase is:

```text
phi = pi * (1 - integrity)
```

The C:B state is:

```text
|+>_C
Ry(pi/2) on B
controlled-RZ(phi)
dephase gamma on C:B
```

The CHSH value is computed as the Horodecki maximum CHSH score from the 3x3 two-qubit correlation matrix.

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_CHSH_READOUT_TRANSPORT
```

## Prediction check

### P1 null

```text
gamma=1 has max CHSH <= 2.0 and zero violating post-burn steps
```

Result: PASS.

| scenario | gamma | max CHSH | violating post-burn steps |
|---|---:|---:|---:|
| normal | 1.0 | 0.0 | 0 |
| stress | 1.0 | 0.0 | 0 |
| storage_heavy | 1.0 | 0.0 | 0 |

### P3 main

```text
gamma=0 produces max CHSH > 2.0 at least in stress, and P_release exceeds the classical ceiling reactor
```

Result: PASS.

| scenario | gamma | classical ceiling release | quantum release | dev % | max CHSH |
|---|---:|---:|---:|---:|---:|
| stress | 0.0 | 0.088575 | 0.114642 | +29.429224 | 2.828427 |

### P4 monotonicity

```text
violation and transported excess are destroyed as gamma increases
```

Result: PASS on tested grid.

Stress scenario:

| gamma | max CHSH | release dev % | violating post-burn steps |
|---:|---:|---:|---:|
| 1.0 | 0.000000 | 0.000000 | 0 |
| 0.75 | 0.707107 | 0.000000 | 0 |
| 0.5 | 1.414214 | 0.000000 | 0 |
| 0.25 | 2.121320 | +1.901441 | 600 |
| 0.0 | 2.828427 | +29.429224 | 600 |

### P5 localization

```text
effect concentrates where integrity collapses and phi approaches pi; normal << stress
```

Result: PASS.

At gamma=0:

| scenario | max CHSH | release dev % | max negativity |
|---|---:|---:|---:|
| normal | 2.116663 | +2.332902 | 0.173252 |
| stress | 2.828427 | +29.429224 | 0.500000 |
| storage_heavy | 2.116663 | +0.980337 | 0.173252 |

## Full summary

| scenario | gamma | classical ceiling release | quantum release | dev % | mean CHSH | max CHSH | violating steps | mean neg | max neg | quantum-specific transport? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| normal | 1.0 | 57.953637 | 57.953637 | 0.000000 | 0.000000 | 0.000000 | 0 | 0.000000 | 0.000000 | FALSE |
| normal | 0.75 | 57.953637 | 57.953637 | 0.000000 | 0.513437 | 0.529166 | 0 | 0.000000 | 0.000000 | FALSE |
| normal | 0.5 | 57.953637 | 57.953637 | 0.000000 | 1.026874 | 1.058332 | 0 | 0.000000 | 0.000000 | FALSE |
| normal | 0.25 | 57.953637 | 57.953637 | 0.000000 | 1.540311 | 1.587497 | 0 | 0.024686 | 0.067439 | FALSE |
| normal | 0.0 | 57.953637 | 59.305639 | +2.332902 | 2.053748 | 2.116663 | 600 | 0.111015 | 0.173252 | TRUE |
| stress | 1.0 | 0.088575 | 0.088575 | 0.000000 | 0.000000 | 0.000000 | 0 | 0.000000 | 0.000000 | FALSE |
| stress | 0.75 | 0.088575 | 0.088575 | 0.000000 | 0.707107 | 0.707107 | 0 | 0.000000 | 0.000000 | FALSE |
| stress | 0.5 | 0.088575 | 0.088575 | 0.000000 | 1.414214 | 1.414214 | 0 | 0.125000 | 0.125000 | FALSE |
| stress | 0.25 | 0.088575 | 0.090259 | +1.901441 | 2.121320 | 2.121320 | 600 | 0.312500 | 0.312500 | TRUE |
| stress | 0.0 | 0.088575 | 0.114642 | +29.429224 | 2.828427 | 2.828427 | 600 | 0.500000 | 0.500000 | TRUE |
| storage_heavy | 1.0 | 31.100982 | 31.100982 | 0.000000 | 0.000000 | 0.000000 | 0 | 0.000000 | 0.000000 | FALSE |
| storage_heavy | 0.75 | 31.100982 | 31.100982 | 0.000000 | 0.513437 | 0.529166 | 0 | 0.000000 | 0.000000 | FALSE |
| storage_heavy | 0.5 | 31.100982 | 31.100982 | 0.000000 | 1.026874 | 1.058332 | 0 | 0.000000 | 0.000000 | FALSE |
| storage_heavy | 0.25 | 31.100982 | 31.100982 | 0.000000 | 1.540311 | 1.587497 | 0 | 0.024686 | 0.067439 | FALSE |
| storage_heavy | 0.0 | 31.100982 | 31.405876 | +0.980337 | 2.053748 | 2.116663 | 600 | 0.111015 | 0.173252 | TRUE |

## Interpretation

This is the first positive result in the current reactor line after the Arm2-kill negatives.

But the scope is narrow and important:

```text
positive for a deliberately added CHSH readout component
not positive for ordinary local population plumbing
```

The result says:

```text
if reactor release is driven by a noncommutative joint Bell/CHSH readout,
then CHSH violation can exceed the local-classical release ceiling and reach transported output.
```

This connects the reactor line with the witness line.

## Safe claim

```text
A deliberately added CHSH readout component can make Bell-violating joint correlations exceed the classical release ceiling and reach transported P_release. This is a model-level quantum-audit positive for the measurement/readout component, not for ordinary local population plumbing.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not evidence that local population plumbing is quantum-specific
```

## What this updates

Previously ruled-out routes remain ruled out:

```text
one-path converter coherence
quality-as-coherence auxiliary probe
branch-only phase-dependent product composition
transported local-population branch release
```

The new surviving route is:

```text
joint / noncommutative CHSH readout component coupled to reactor transport
```

## Next boundary to test

The next strict test should ask whether the CHSH readout can be implemented as a plausible component rather than as an explicit oracle-like readout:

```text
measurement backaction changes release or terrain
basis choices are explicit and audited
classical/local bound remains S <= 2
hardware-feasible witness circuit is separated from classical-effective reactor dynamics
```
