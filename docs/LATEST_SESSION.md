# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_measurement_terrain_memory_probe
```

This is the latest active quantum-audit probe in the classical-effective / quantum-audit boundary line.

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/quantum_measurement_terrain_memory_probe_2026-07-08.md
experiments/quantum_measurement_terrain_memory_probe_protocol_2026-07-08.md
scripts/audit/quantum_measurement_terrain_memory_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_measurement_terrain_memory_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

The new canonical log is:

```text
data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv
```

## Current result

The latest run tests:

```text
Phase 1: finite-shot sampled CHSH writes conservative Bell excess into terrain
Phase 2: measurement stops; terrain memory is read by road_boost
Phase 3: challenge phase tests residual memory
matched classical replay checks post-write specificity
```

Verdict:

```text
POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_TERRAIN_MEMORY
```

Key results:

```text
P1 gamma=1 null: PASS; no write, no terrain delta, no later release difference
stress gamma=0.25: terrain half-life 50 steps, phase2 release +1.438596%, phase3 +0.088855%
stress gamma=0: terrain half-life 47 steps, phase2 release +19.998558%, phase3 +1.427578%
normal/storage: filtered to zero by finite-shot margin
matched classical replay: phase2/phase3 release diff vs Arm3 = 0
```

## Safe claim

```text
A finite-shot sampled CHSH measurement-boundary signal can be written into terrain, persist after measurement stops, and weakly affect a later challenge phase in stress context. The post-write memory dynamics are classical terrain dynamics: a matched classical replay of the same write trajectory reproduces them. This is model-level positive for measurement-boundary terrain memory, not for quantum-specific post-write terrain physics or ordinary local population plumbing.
```

## What this does not mean

Do not claim:

```text
hardware result
chemical realism
biological metabolism
universal quantum advantage
quantum-specific terrain decay
local population plumbing is quantum-specific
```

## Previous sessions

The immediately previous sampled feedback test is:

```text
quantum_sampled_chsh_terrain_feedback_probe_2026-07-08.md
```

The exact terrain feedback test is:

```text
quantum_measurement_terrain_feedback_probe_2026-07-08.md
```

## Recommended next boundary

The next strict boundary is adaptive feedback:

```text
measurement-boundary terrain memory
-> changes next measurement basis or membrane gate
-> changes later CHSH/readout statistics
```
