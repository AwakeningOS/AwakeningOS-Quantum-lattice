# Quantum Microreactor CHSH Readout Transport Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

Can a joint, noncommutative CHSH readout component make a quantum-specific witness affect transported reactor output?

This protocol follows the transported branching Arm2-kill result:

```text
local population transport can move strongly but remains fully reduced-Arm2-reproducible
```

The new test changes the readout, not the pipe. Release is driven by a CHSH witness across noncommuting measurement bases.

## False-positive trap

A single joint correlation such as:

```text
<Z_C Z_B>
```

is not enough. Classical correlated coins can produce single-basis correlations.

Therefore the readout uses the Bell/CHSH bound:

```text
separable or local-classical states: S_CHSH <= 2
quantum states: S_CHSH can exceed 2 up to 2*sqrt(2)
```

The classical transport ceiling is:

```text
yb_classical_ceiling = 1 / sqrt(2)
```

The quantum readout is:

```text
yb = max(2, S_CHSH) / (2 * sqrt(2))
```

Thus nonviolating states cannot exceed the classical ceiling. Only CHSH violation can increase transported release.

## Reactor setting

The tested scenarios are:

```text
normal
stress
storage_heavy
```

The reactor context phase remains:

```text
phi = pi * (1 - integrity)
```

The C:B state is built from:

```text
|+>_C
Ry(pi/2) on B
controlled-RZ(phi)
dephase gamma on C:B
```

The CHSH value is the Horodecki maximum CHSH score computed from the two-qubit correlation matrix.

## Gamma values

```text
gamma = 1.0, 0.75, 0.5, 0.25, 0.0
```

## Pre-registered predictions

```text
P1 null:
  gamma=1 has max CHSH <= 2.0 and zero violating post-burn steps.

P3 main:
  gamma=0 produces max CHSH > 2.0 at least in stress, and P_release exceeds the classical ceiling reactor.

P4 monotonicity:
  CHSH violation and transported excess are destroyed as gamma increases.

P5 localization:
  the strongest effect concentrates where integrity collapses and phi approaches pi; stress >> normal.
```

## Success criteria

A quantum-specific transported effect requires:

```text
1. S_CHSH > 2
2. P_release > classical ceiling release
3. both are computed from the same run and scenario
```

Because CHSH <= 2 is the Bell/local bound, no classical correlated reactor can exceed the defined ceiling under this readout.

## Expected raw outputs

```text
data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv
data/quantum_microreactor/chsh_readout_transport_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_microreactor_chsh_readout_transport_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/chsh_readout_transport_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv
```

## Forbidden claims

Do not claim:

```text
hardware result
biological metabolism
chemical realism
universal no-go theorem
general quantum advantage
```

This is a model-level quantum-audit positive only for a deliberately added CHSH readout component.
