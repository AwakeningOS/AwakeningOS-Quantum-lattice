# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_sampled_chsh_terrain_feedback_probe
```

This is the latest active quantum-audit probe in the classical-effective / quantum-audit boundary line.

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/quantum_sampled_chsh_terrain_feedback_probe_2026-07-08.md
experiments/quantum_sampled_chsh_terrain_feedback_probe_protocol_2026-07-08.md
scripts/audit/quantum_sampled_chsh_terrain_feedback_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_sampled_chsh_terrain_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

The new canonical log is:

```text
data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv
```

## Current result

The latest run tests:

```text
finite-shot sampled CHSH terrain feedback
32768 shots per CHSH setting per step
confidence margin S = 0.093683293042
conservative terrain write = max(0, S_hat - 2 - margin) only
observable: next-phase P_release
```

Verdict:

```text
POSITIVE_FOR_MODEL_LEVEL_SAMPLED_CHSH_TERRAIN_FEEDBACK
```

Key results:

```text
P1 gamma=1 null: PASS; no conservative sampled excess and no terrain feedback
P2 noise guard: PASS; normal/storage gamma=0 are filtered to zero despite small true CHSH > 2
P3 stress gamma=0: PASS; 371 positive sampled steps, terrain delta=2.347412, next-release +19.998558%
P4 threshold: PASS; stress gamma=0.25 survives weakly (+1.438596%), gamma>=0.5 does not
```

## Safe claim

```text
A finite-shot sampled CHSH measurement-boundary signal, after subtracting a conservative Bell-bound margin, can still be written into terrain and later modulate classical-effective dynamics in stress context. This is a model-level positive for sampled measurement-boundary terrain feedback, not for ordinary local population plumbing.
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

The immediately previous exact terrain feedback test is:

```text
quantum_measurement_terrain_feedback_probe_2026-07-08.md
```

The previous readout transport test is:

```text
quantum_microreactor_chsh_readout_transport_probe_2026-07-08.md
```

The local-population transport negative remains:

```text
quantum_microreactor_transported_branching_arm2_kill_2026-07-08.md
```

## Recommended next boundary

The next boundary is hardware-likeness:

```text
fixed measurement bases instead of per-step optimized bases
explicit basis schedule
separate witness sampling from terrain writeback
shot budget close to QPU constraints
noise model or real QPU candidate circuit
```
