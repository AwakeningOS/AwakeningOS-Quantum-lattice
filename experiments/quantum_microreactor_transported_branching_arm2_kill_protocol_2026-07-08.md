# Quantum Microreactor Transported Branching Arm2-Kill Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

Can a phase-dependent branching converter with entangled control make a quantum effect reach a transported reactor observable, specifically `P_release`?

This protocol is a direct attempt to falsify the earlier negative conclusion that branch-only observables are Arm2-reproducible.

## Core idea

The converter is minimally modified while the rest of the reactor remains classical-effective:

```text
C = reactor context control qubit
B = branch qubit
B=0 -> P goes to reservoir
B=1 -> P' is discarded
```

The reactor context phase is:

```text
phi = pi * (1 - integrity)
```

The converter applies a controlled branch phase and sends only the `B=0` branch to the reservoir. This means the phase-dependent branch ratio is transported into `P_release`.

## Arms

```text
classical:
  fixed 50/50 branch to reservoir

quantum:
  two-qubit C:B density state with controlled-RZ(phi), dephase gamma, and B readout

weak Arm2:
  single-qubit mean-field complex wave using phase phi/2
  included only to demonstrate the false-positive trap

correct Arm2 reduced:
  trace out C first, producing a single-qubit B channel with no entanglement
  compare transported release against quantum
```

## Pre-registered prediction

The run is expected to show:

```text
1. gamma=1 gate returns to the classical 50/50 branch
2. transported P_release changes strongly for low gamma
3. weak mean-field Arm2 may fail to match quantum and create a false positive
4. correct Arm2 reduced channel should match quantum transported release if the effect is not quantum-specific
5. negativity can be nonzero but still fail to do causal work if release depends only on local B population
```

## Success criteria for quantum-specific transport

A positive result requires:

```text
1. P_release changes with gamma
2. Arm3 / quantum C:B state has negativity > 0
3. correct Arm2 reduced channel cannot reproduce P_release
```

## Negative criteria

The result is negative for quantum-specific transport if:

```text
1. P_release changes with gamma
2. negativity appears
3. correct Arm2 reduced channel reproduces P_release to numerical precision
```

## Tested scenarios

```text
normal
stress
storage_heavy
```

These were chosen because they cover baseline, integrity collapse, and backpressure/storage-heavy transport.

## Expected raw outputs

```text
data/quantum_microreactor/transported_branching_arm2_kill_seed20260707_summary.csv
data/quantum_microreactor/transported_branching_arm2_kill_seed20260707.json
```

## Run commands

```bash
python scripts/audit/quantum_branch_converter.py
python scripts/audit/arm2_kill.py
```

## Forbidden claims

Do not claim:

```text
quantum advantage
quantum-specific transported effect
functional entanglement
hardware relevance
chemical realism
biological metabolism
```

unless the correct Arm2 reduced channel fails to reproduce the transported observable.
