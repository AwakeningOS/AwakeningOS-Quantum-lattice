# Information Microreactor Backpressure + Contamination Observation Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `classical-effective phenomenology`

## Question

Can the existing information microreactor sandbox be used as a time-resolved observation object rather than only a scenario-summary table?

Specifically, when storage pressure, contaminant leakage, stress, stabilizer input, and terrain/road feedback are placed into one deterministic timeline, do ordered information-material modes appear?

## Layer

```text
classical-effective phenomenology
```

This is not a quantum-audit experiment. It does not test quantum advantage, quantum coherence, entanglement, negativity, or hardware behavior.

## Model

The model extends the existing `information_microreactor_sandbox` components:

```text
source
road / channel
selective membrane
converter A -> P
reservoir
sink / release
terrain writing
B contaminant
D stress
C stabilizer
```

The observation run uses one continuous state trajectory with five phases:

```text
0-199   clean_finite_reactor
200-399 leaky_contamination
400-599 storage_pressure
600-799 stress_collapse
800-999 stabilizer_rescue
```

State is not reset between phases. Reservoir fill, contaminant load, membrane integrity, and terrain carry over.

## Metrics

Summary metrics by phase:

```text
source_A_total
A_in_total
B_in_total
P_generated
P_release
quality_weighted_release
mean_quality
min_quality
mean_reservoir
max_reservoir
mean_fill_fraction
max_fill_fraction
mean_backpressure
min_backpressure
mean_integrity
final_integrity
final_terrain
mean_road_boost
smoothing_ratio
quality_damage_index
stability_window
```

Event metrics:

```text
quality_lt_0_7
quality_lt_0_5
quality_lt_0_3
fill_gt_0_5
fill_gt_0_75
backpressure_lt_0_5
backpressure_lt_0_2
integrity_lt_0_5
integrity_lt_0_1
rescue_integrity_gt_0_5_after_800
```

Timeseries metrics are stored as deterministic 50-step checkpoints plus the final row. Exact threshold crossing times are stored in `events.csv`.

## Controls and comparisons

This is an internal component observation run. The controls are phase contrasts inside one deterministic timeline:

```text
clean_finite_reactor:
  baseline finite-capacity behavior

leaky_contamination:
  contaminant leakage with active flow

storage_pressure:
  lower release and smaller reservoir capacity

stress_collapse:
  stress without stabilizer

stabilizer_rescue:
  same stress load with external stabilizer input
```

The key comparison is temporal ordering, not only phase means.

## Success criteria

A useful observation run should produce at least three of the following without resetting state:

```text
1. product quality collapse before complete flow stoppage
2. reservoir fill increase followed by upstream backpressure reduction
3. stress-driven membrane integrity collapse
4. stabilizer-assisted recovery after stress collapse
5. quality-weighted release diverging from raw release
6. terrain/road feedback remaining inspectable in the timeseries
```

## Failure criteria

The run should be considered weak or uninteresting if:

```text
1. all phases differ only by direct scalar throughput
2. no threshold events are crossed
3. no downstream-to-upstream modulation appears
4. contamination only stops flow without quality-specific degradation
5. stabilizer effect cannot be separated from autonomous self-repair
```

## Seed

```text
seed = 20260707
```

The current model is deterministic. The seed is retained for interface consistency and future stochastic variants.

## Expected raw outputs

```text
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv
```

Auxiliary JSON metadata:

```text
data/microreactor/information_microreactor_backpressure_contamination_seed20260707.json
```

## Run command

```bash
python scripts/phenomenology/information_microreactor_backpressure_contamination.py \
  --seed 20260707 \
  --out data/microreactor/information_microreactor_backpressure_contamination_seed20260707.json \
  --summary-csv data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv \
  --events-csv data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv \
  --timeseries-csv data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv \
  --timeseries-stride 50
```

## Known limitations

```text
Classical-effective deterministic sandbox only.
Not a quantum-witness experiment.
Not biological metabolism.
Not autonomous self-repair.
Not life-like behavior.
Contamination is represented by scalar quality variables.
Stabilizer rescue is externally supplied, not self-generated.
```

## Forbidden claims

Do not claim:

```text
quantum advantage
quantum-specific behavior
life-like behavior
metabolism
autonomous self-repair
autonomous self-regulation
natural physical microreactor
hardware result
```

## Intended use

This experiment is meant to provide paper-writing material for the classical-effective component layer. It should help future agents resume from the correct latest session without confusing this line with the quantum-audit Step 6 line.
