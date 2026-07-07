# Quantum Microreactor Transported Branching Arm2-Kill Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator scripts:

```text
scripts/audit/quantum_branch_converter.py
scripts/audit/arm2_kill.py
```

Canonical raw log:

```text
data/quantum_microreactor/transported_branching_arm2_kill_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/transported_branching_arm2_kill_seed20260707.json
```

Run commands:

```bash
python scripts/audit/quantum_branch_converter.py
python scripts/audit/arm2_kill.py
```

## Purpose

This experiment directly attacks the strongest remaining possibility in the current microreactor line:

```text
Can a phase-dependent branching converter with entangled control move a quantum-specific effect into transported P_release?
```

Unlike the previous branch-only probe, this one sends only the `B=0` branch to the reservoir. Therefore the phase-dependent branch ratio is transported into `P_release`.

## Design

```text
C = reactor context qubit
B = product branch qubit
B=0 -> P goes to reservoir
B=1 -> P' is discarded
```

The reactor context phase is:

```text
phi = pi * (1 - integrity)
```

The quantum branch converter applies:

```text
|+>_C
Ry(pi/2) on B
controlled-RZ(phi)
dephase gamma on C:B
Ry(-pi/2) on B
read B=0 into reservoir
```

## Critical Arm2 correction

The weak Arm2 control uses a mean-field branch phase:

```text
phi / 2
```

That control fails to reproduce quantum gamma=0 and would create a false positive.

The correct Arm2 control traces out C first:

```text
rho_B = 0.5 * U0 rho0 U0^dagger + 0.5 * U1 rho0 U1^dagger
```

This is a single-qubit B channel with no entanglement. It is the correct zero-entanglement control for any transported observable that depends only on local B population.

## Gate

```text
quantum(gamma=1) release == classical 50/50 branch release
```

Gate result:

| scenario | gamma=1 release diff | pass |
|---|---:|---|
| normal | 1.42108547152e-14 | TRUE |
| stress | 0.0 | TRUE |
| storage_heavy | 3.552713678801e-15 | TRUE |

## Main transported release result

The transported observable moves strongly:

| scenario | classical release | quantum g=0.5 release | dev % | quantum g=0 release | dev % |
|---|---:|---:|---:|---:|---:|
| normal | 41.155340 | 60.443542 | +46.866828 | 79.541638 | +93.271732 |
| stress | 0.062766 | 0.072312 | +15.209479 | 0.081812 | +30.345232 |
| storage_heavy | 24.380048 | 32.108941 | +31.701711 | 38.149691 | +56.479145 |

This is the strongest positive-looking transported effect so far.

## False-positive trap: weak Arm2

The weak mean-field Arm2 does not match quantum gamma=0:

| scenario | quantum g=0 | weak Arm2 | abs diff |
|---|---:|---:|---:|
| normal | 79.541638 | 80.487036 | 0.945398 |
| stress | 0.081812 | 0.092901 | 0.011089 |
| storage_heavy | 38.149691 | 38.320472 | 0.170781 |

If this were the only Arm2 control, it could be misread as a quantum-specific transported effect. It is not.

## Correct Arm2 kill

The correct reduced single-qubit Arm2 reproduces quantum transported release to numerical precision:

| scenario | gamma | quantum release | Arm2 reduced release | abs diff | match |
|---|---:|---:|---:|---:|---|
| normal | 0.0 | 79.541638 | 79.541638 | 2.84217094304e-14 | TRUE |
| normal | 0.5 | 60.443542 | 60.443542 | 7.105427357601e-15 | TRUE |
| stress | 0.0 | 0.081812 | 0.081812 | 0.0 | TRUE |
| stress | 0.5 | 0.072312 | 0.072312 | 0.0 | TRUE |
| storage_heavy | 0.0 | 38.149691 | 38.149691 | 0.0 | TRUE |
| storage_heavy | 0.5 | 32.108941 | 32.108941 | 0.0 | TRUE |

## Negativity

Entanglement is real in the quantum branch circuit:

| scenario | mean neg g=0.5 | max neg g=0.5 | mean neg g=0 | max neg g=0 |
|---|---:|---:|---:|---:|
| normal | 0.0 | 0.0 | 0.111000 | 0.173300 |
| stress | 0.125000 | 0.125000 | 0.500000 | 0.500000 |
| storage_heavy | 0.0 | 0.0 | 0.111000 | 0.173300 |

The stress scenario reaches Bell-level maximum negativity at gamma=0.

But this does not make the transported release quantum-specific.

## Structural interpretation

The transported release depends only on the local branch population:

```text
P_to_reservoir = amount * Pr(B=0)
```

That means the reactor plumbing reads only the reduced density matrix of B:

```text
rho_B = Tr_C(rho_CB)
```

Entanglement and negativity are properties of the joint state `rho_CB`. A local B-population observable is blind to them once the reduced B channel is fixed.

Therefore:

```text
transported release changes strongly
C:B negativity can be nonzero
but correct reduced Arm2 reproduces transported release exactly
```

## Verdict

```text
NEGATIVE_FOR_QUANTUM_SPECIFIC_TRANSPORT
```

## Safe claim

```text
A phase-dependent branching converter can transport a large phase-dependent effect into P_release, and the C:B state can become entangled. However, the transported observable depends only on local B population, so a zero-entanglement reduced Arm2 channel reproduces P_release exactly. This is negative for quantum-specific transport.
```

## What this does not show

```text
not quantum advantage
not quantum-specific transported effect
not functional entanglement in the reactor plumbing
not hardware relevance
not chemical realism
not biological metabolism
```

## What this does show

This result joins the reactor and witness lines:

```text
population transport is local reduced-state plumbing
quantum-specific effects require joint / noncommutative / basis-sensitive readout
```

The current reactor plumbing does not read joint observables. It reads local populations.

## Remaining route

A future positive test must add a measurement/readout component, not another pipe:

```text
release depends on <Z_C Z_B>
control-conditioned product readout
basis-dependent quality readout that Arm2 cannot reproduce
measurement backaction that changes release or terrain
```

Without such a component, entanglement can exist but remains functionally unused by the reactor output.
