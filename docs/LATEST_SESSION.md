# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_microreactor_transported_branching_arm2_kill
```

This is the latest active quantum-audit probe in the classical-effective / quantum-audit boundary line.

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/quantum_microreactor_transported_branching_arm2_kill_2026-07-08.md
experiments/quantum_microreactor_transported_branching_arm2_kill_protocol_2026-07-08.md
scripts/audit/quantum_branch_converter.py
scripts/audit/arm2_kill.py
scripts/audit/quantum_microreactor_transported_branching_arm2_kill.py
```

## Reproduction commands

Display harnesses:

```bash
python scripts/audit/quantum_branch_converter.py
python scripts/audit/arm2_kill.py
```

Canonical CSV generator:

```bash
python scripts/audit/quantum_microreactor_transported_branching_arm2_kill.py \
  --seed 20260707 \
  --out data/quantum_microreactor/transported_branching_arm2_kill_seed20260707.json \
  --summary-csv data/quantum_microreactor/transported_branching_arm2_kill_seed20260707_summary.csv
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

The new canonical log is:

```text
data/quantum_microreactor/transported_branching_arm2_kill_seed20260707_summary.csv
```

## Current result

The latest run tests:

```text
phase-dependent branching converter where B=0 is transported to reservoir
entangled C:B branch circuit
weak Arm2 mean-field control
correct Arm2 reduced single-qubit control
transported P_release observable
```

Verdict:

```text
NEGATIVE_FOR_QUANTUM_SPECIFIC_TRANSPORT
```

Details:

```text
gamma=1 gate passes to machine precision
P_release moves strongly with gamma
normal g=0: +93.27%
stress g=0: +30.35%
storage_heavy g=0: +56.48%
weak Arm2 creates a false-positive-looking mismatch
correct reduced Arm2 matches quantum transported release to machine precision
max negativity reaches 0.5 in stress at gamma=0
quantum_specific_transport_effect = FALSE
```

## What this means

Safe claim:

```text
Transported release can move strongly, and C:B entanglement can exist, but local population transport is fully determined by the reduced B channel and is exactly Arm2-reproducible.
```

This is the strongest negative filter so far: even when the quantum branch affects `P_release`, it is still not quantum-specific if the reactor reads only local branch population.

## What this does not mean

Do not claim:

```text
quantum advantage
quantum-specific transported effect
functional entanglement in reactor plumbing
hardware feasibility
chemical realism
biological metabolism
```

## Previous sessions

The immediately previous branch-only probe is:

```text
quantum_microreactor_branching_converter_probe_2026-07-08.md
```

The previous gamma sweep is:

```text
quantum_microreactor_gamma_sweep_quality_probe_2026-07-08.md
```

The previous validation gate is:

```text
quantum_microreactor_gamma_validation_2026-07-08.md
```

The previous classical-effective observation experiment is:

```text
information_microreactor_backpressure_contamination_2026-07-08.md
```

## Recommended next decision

The reactor line has now ruled out:

```text
one-path converter coherence
quality-as-coherence auxiliary probe
branch-only phase-dependent product composition
transported local-population branch release
```

A future quantum-specific attempt needs a measurement/readout component, not another pipe:

```text
release depends on <Z_C Z_B>
control-conditioned product readout
basis-dependent quality readout that Arm2 cannot reproduce
measurement backaction that changes release or terrain
```

Without such a component, entanglement remains present but functionally unused by reactor output.
