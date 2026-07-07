# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_microreactor_chsh_readout_transport_probe
```

This is the latest active quantum-audit probe in the classical-effective / quantum-audit boundary line.

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/quantum_microreactor_chsh_readout_transport_probe_2026-07-08.md
experiments/quantum_microreactor_chsh_readout_transport_probe_protocol_2026-07-08.md
scripts/audit/quantum_microreactor_chsh_readout_transport_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_microreactor_chsh_readout_transport_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/chsh_readout_transport_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

The new canonical log is:

```text
data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv
```

## Current result

The latest run tests:

```text
joint / noncommutative CHSH readout component
classical ceiling yb = 1/sqrt(2)
quantum readout yb = max(2, S_CHSH) / (2*sqrt(2))
transported P_release observable
```

Verdict:

```text
POSITIVE_FOR_MODEL_LEVEL_CHSH_READOUT_TRANSPORT
```

Key results:

```text
P1 gamma=1 null: PASS; max_chsh=0 and zero violating steps in all scenarios
P3 stress gamma=0: PASS; max_chsh=2.828427 and P_release exceeds ceiling by +29.429224%
P4 monotonicity: PASS on tested grid; stress violation appears at gamma=0.25 and strengthens at gamma=0
P5 localization: PASS; stress +29.43% >> normal +2.33% and storage_heavy +0.98%
```

## Safe claim

```text
A deliberately added CHSH readout component can make Bell-violating joint correlations exceed the classical release ceiling and reach transported P_release. This is a model-level quantum-audit positive for the measurement/readout component, not for ordinary local population plumbing.
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

The immediately previous transported local-population test is:

```text
quantum_microreactor_transported_branching_arm2_kill_2026-07-08.md
```

That result remains negative for local population transport because correct reduced Arm2 reproduces the transported observable exactly.

## Recommended next boundary

The next boundary is not another pipe. It is whether this readout can be made into a plausible component:

```text
measurement backaction changes release or terrain
basis choices are explicit and audited
classical/local bound remains S <= 2
hardware-feasible witness circuit is separated from classical-effective reactor dynamics
```
