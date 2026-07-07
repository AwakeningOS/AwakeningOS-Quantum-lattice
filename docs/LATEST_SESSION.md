# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
information_microreactor_backpressure_contamination
```

This is the latest active experiment in the classical-effective information microreactor line.

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/information_microreactor_backpressure_contamination_2026-07-08.md
experiments/information_microreactor_backpressure_contamination_protocol_2026-07-08.md
scripts/phenomenology/information_microreactor_backpressure_contamination.py
```

## Reproduction command

```bash
python scripts/phenomenology/information_microreactor_backpressure_contamination.py \
  --seed 20260707 \
  --out data/microreactor/information_microreactor_backpressure_contamination_seed20260707.json \
  --summary-csv data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv \
  --events-csv data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv \
  --timeseries-csv data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv \
  --timeseries-stride 50
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

The new canonical logs are:

```text
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv
```

## Current observation

The latest run combines:

```text
clean finite reactor
leaky contamination
storage pressure
stress collapse
stabilizer rescue
```

in one continuous state trajectory.

Main observed order:

```text
quality collapse first
reservoir/backpressure second
membrane integrity collapse third
stabilizer-assisted recovery fourth
```

Key event times:

```text
quality < 0.7: t=206
quality < 0.5: t=218
quality < 0.3: t=259
backpressure < 0.5: t=410
fill > 0.5: t=420
backpressure < 0.2: t=462
fill > 0.75: t=510
integrity < 0.5: t=648
integrity < 0.1: t=708
rescue integrity > 0.5 after t=800: t=893
```

## Do not confuse with Step 6

The immediately previous quantum-audit/component-semantics bridge is:

```text
quantum_coupled_microreactor_step6_explicit_component_chain_2026-07-07.md
```

Step 6 concluded that its explicit three-body boost survived dephase and was therefore classical-effective, not a quantum-specific witness.

The latest line is not Step 6. The latest line is:

```text
classical-effective information microreactor observation sandbox
```

## Safe claim

```text
A code-backed classical-effective observation sandbox shows ordered failure/recovery modes: contamination degrades quality before flow stops; reservoir saturation produces upstream backpressure; stress collapses membrane integrity; and external stabilizer input partially restores membrane integrity.
```

## Forbidden claims

Do not claim:

```text
quantum advantage
quantum-specific effect
hardware result
life-like behavior
metabolism
autonomous self-repair
autonomous self-regulation
```

## Recommended next experiment

```text
information_microreactor_backpressure_contamination_ablation
```

Suggested ablations:

```text
no_backpressure_feedback
no_B_contaminant_effect
no_terrain_write
no_stabilizer_repair
```

The next useful output should keep:

```text
summary.csv
events.csv
timeseries.csv
```

because event timing is now part of the result, not a side note.
