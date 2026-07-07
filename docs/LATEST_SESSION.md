# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_measurement_terrain_feedback_probe
```

This is the latest active quantum-audit probe in the classical-effective / quantum-audit boundary line.

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/quantum_measurement_terrain_feedback_probe_2026-07-08.md
experiments/quantum_measurement_terrain_feedback_probe_protocol_2026-07-08.md
scripts/audit/quantum_measurement_terrain_feedback_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_measurement_terrain_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

The new canonical log is:

```text
data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv
```

## Current result

The latest run tests:

```text
Phase 1: CHSH measurement-boundary signal writes only Bell-violating excess into terrain
Phase 2: terrain is read by classical-effective road feedback
observable: next-phase P_release
```

Verdict:

```text
POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_TERRAIN_FEEDBACK
```

Key results:

```text
P1 gamma=1 null: PASS; CHSH excess, terrain delta, and next-release difference are zero
P3 stress gamma=0.25: PASS; max CHSH=2.121320, terrain delta=0.385016, next-release +5.446770%
P3 stress gamma=0: PASS; max CHSH=2.828427, terrain delta=2.646051, next-release +21.389922%
P4 gamma sensitivity: PASS; stress effect is zero through gamma=0.5, appears at 0.25, strengthens at 0
P5 localization: PASS; stress +21.39% >> normal +0.97% and storage +0.68%
```

## Safe claim

```text
A deliberately added CHSH measurement-boundary signal can be written into terrain and later modulate classical-effective reactor dynamics. This is a model-level positive for measurement-boundary terrain feedback, not for ordinary local population plumbing.
```

## What this does not mean

Do not claim:

```text
hardware result
chemical realism
biological metabolism
universal quantum advantage
local population plumbing is quantum-specific
```

## Previous sessions

The immediately previous readout transport test is:

```text
quantum_microreactor_chsh_readout_transport_probe_2026-07-08.md
```

The previous local-population transport test is:

```text
quantum_microreactor_transported_branching_arm2_kill_2026-07-08.md
```

That result remains negative for local population transport because correct reduced Arm2 reproduces the transported observable exactly.

## Recommended next boundary

The next boundary is whether this terrain inscription can be made less oracle-like:

```text
basis choices explicit and audited
CHSH measurements sampled rather than directly read from density matrix
measurement backaction separated from terrain write
hardware-feasible witness circuit separated from classical-effective reactor dynamics
```
