# Information Microreactor Sandbox Protocol

Date: 2026-07-07
Layer: classical-effective phenomenology

## Question

What happens when the currently developed information-matter components are assembled into one small classical-effective microreactor sandbox?

This is an exploratory assembly/play run, not a quantum-witness experiment.

## Components

```text
source
road / channel
selective membrane
converter A -> P
reservoir
sink / release
external terrain write
stress D
stabilizer C
contaminant B
```

## Flow

```text
A source
  -> road/channel bias
  -> selective membrane
  -> converter A -> P
  -> reservoir
  -> release/sink
  -> external terrain write
```

External perturbations:

```text
B contaminant: can leak through membrane and reduce product quality
C stabilizer: reduces D damage and helps membrane integrity
D stress: damages membrane integrity
```

## Simulation layer

This is a deterministic scalar sandbox with classical-effective flows. It is not a quantum circuit and makes no quantum-specific claim.

Each scenario runs a fixed number of steps with a burn-in window. The summary CSV contains post-burn aggregate metrics.

## Scenarios

```text
normal:
  baseline A supply, selective membrane, converter, reservoir, release

high_load:
  high A supply, tests throughput and reservoir pressure

stress:
  high D stress without stabilizer, tests membrane failure

stabilizer:
  high D stress with C stabilizer, tests stress rescue

leaky_membrane:
  high B leakage, tests selectivity and product-quality degradation

road_fed:
  terrain-written road feeds back into A supply

storage_heavy:
  low release / small reservoir, tests fill and backpressure
```

## Metrics

```text
source_A_total
A_in_total
B_in_total
permeability_A
permeability_B
selectivity
P_generated
P_release
P_overflow
release_fraction
overflow_fraction
mean_reservoir
final_reservoir
mean_fill_fraction
mean_backpressure
final_integrity
mean_integrity
mean_quality
terrain_written
efficiency_release_per_A
stability_window
release_cv
source_cv
smoothing_ratio
```

## Interpretation discipline

Allowed:

```text
classical-effective information microreactor sandbox
component assembly behavior
selectivity, conversion, storage, release, stress failure, stabilizer rescue,
road feeding, contaminant poisoning, backpressure
```

Forbidden:

```text
quantum-specific witness
quantum advantage
full biological metabolism
life-like behavior
self-repair/self-regulation claim
hardware result
```

## Promotion rule

The run is `RAW_LOG_BACKED` only if all are present:

```text
script: scripts/phenomenology/information_microreactor_sandbox.py
raw CSV: data/microreactor/information_microreactor_sandbox_seed20260707_summary.csv
report: results/information_microreactor_sandbox_2026-07-07.md
raw-log gate registration
```
