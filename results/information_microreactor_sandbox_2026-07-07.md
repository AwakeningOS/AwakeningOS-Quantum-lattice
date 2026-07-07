# Information Microreactor Sandbox

Date: 2026-07-07

Status: `RAW_LOG_BACKED`
Layer: `classical-effective phenomenology`

Generator script:

```text
scripts/phenomenology/information_microreactor_sandbox.py
```

Raw CSV log:

```text
data/microreactor/information_microreactor_sandbox_seed20260707_summary.csv
```

Run command:

```bash
python scripts/phenomenology/information_microreactor_sandbox.py --seed 20260707 --csv data/microreactor/information_microreactor_sandbox_seed20260707_summary.csv
```

## Purpose

This run assembles the current classical-effective information-matter components into a single sandbox:

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

This is an exploratory assembly/play run. It is not a quantum-witness result.

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
B contaminant: leaks through membrane and reduces product quality
C stabilizer: reduces D stress damage and supports membrane integrity
D stress: damages membrane integrity
```

## Scenarios

```text
normal
high_load
stress
stabilizer
leaky_membrane
road_fed
storage_heavy
```

## Main summary

| scenario | selectivity | P generated | P release | mean fill | backpressure | final integrity | quality | terrain | efficiency | smoothing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| normal | 14.645 | 81.216 | 81.466 | 0.031 | 0.980 | 0.775 | 0.915 | 0.309 | 0.067 | 0.463 |
| high_load | 14.211 | 197.020 | 197.588 | 0.076 | 0.951 | 0.775 | 0.915 | 0.752 | 0.065 | 0.456 |
| stress | 0.000 | 0.000 | 0.125 | 0.000 | 1.000 | 0.000 | 0.998 | 0.000 | 0.000 | 17.670 |
| stabilizer | 13.917 | 70.396 | 70.134 | 0.027 | 0.983 | 0.738 | 0.923 | 0.287 | 0.058 | 0.347 |
| leaky_membrane | 1.465 | 81.295 | 81.491 | 0.031 | 0.980 | 0.775 | 0.289 | 0.100 | 0.067 | 0.450 |
| road_fed | 14.310 | 171.489 | 171.680 | 0.066 | 0.957 | 0.775 | 0.915 | 1.297 | 0.066 | 0.455 |
| storage_heavy | 7.804 | 43.285 | 38.495 | 0.533 | 0.520 | 0.775 | 0.915 | 0.162 | 0.032 | 0.315 |

## What appeared

The assembled object behaves like a classical-effective catalytic information microreactor:

```text
selective intake
A -> P conversion
reservoir storage
release/sink output
terrain writing
stress failure
stabilizer rescue
contaminant poisoning
road-fed supply amplification
storage-induced backpressure
```

## Scenario observations

### normal

The sandbox runs stably:

```text
selectivity = 14.645
P_release = 81.466
mean_fill_fraction = 0.031
final_integrity = 0.775
quality = 0.915
```

The reservoir smooths output relative to source variation:

```text
smoothing_ratio = 0.463
```

### high_load

High A supply increases throughput:

```text
P_release: 81.466 -> 197.588
terrain_written: 0.309 -> 0.752
```

Backpressure increases but does not choke the system:

```text
mean_backpressure = 0.951
mean_fill_fraction = 0.076
```

### stress

High D stress without stabilizer collapses the membrane:

```text
final_integrity = 0.000
A_in_total = 0.000
P_generated = 0.000
```

This is a failure mode, not a self-repair result.

### stabilizer

Under the same high D stress, C stabilizer preserves function:

```text
final_integrity = 0.738
P_release = 70.134
selectivity = 13.917
```

This is stabilizer-assisted survival of the membrane function, not autonomous self-repair.

### leaky_membrane

B leakage destroys product quality while throughput remains high:

```text
selectivity: 14.645 -> 1.465
quality: 0.915 -> 0.289
stability_window: 0.785 -> 0.248
```

This is the clearest contaminant-poisoning mode.

### road_fed

Terrain-written road feedback increases supply and output:

```text
source_A_total: 1208.864 -> 2612.306
P_release: 81.466 -> 171.680
terrain_written: 0.309 -> 1.297
```

This is road-fed amplification, not a quantum effect.

### storage_heavy

Low release and small effective reservoir create backpressure:

```text
mean_fill_fraction = 0.533
mean_backpressure = 0.520
P_generated = 43.285
P_release = 38.495
```

The system smooths release more strongly, but throughput drops:

```text
smoothing_ratio = 0.315
efficiency_release_per_A = 0.032
```

## Interpretation

The current assembled object is best described as:

```text
classical-effective information microreactor sandbox
```

It is not yet a biological/autopoietic object. It does not self-regulate in a strong sense. It does show modular information-matter behavior when source, membrane, converter, reservoir, sink, road, contaminant, stress, and stabilizer are assembled.

## Safe claim

```text
A code-backed classical-effective sandbox assembles source, road, selective membrane, converter, reservoir, sink/release, terrain writing, stress, stabilizer, and contaminant into one information microreactor-like system. The sandbox shows stable conversion/release, stress failure, stabilizer rescue, contaminant poisoning, road-fed amplification, and storage-induced backpressure.
```

## What this does not claim

```text
not quantum-specific
not quantum advantage
not full biological metabolism
not life-like behavior
not self-repair
not self-regulation
not hardware result
```

## Next play directions

```text
classical-effective branch:
  add explicit finite-capacity backpressure loops
  add source/sink schedules
  add spatial membrane/road geometry
  add event logs and per-step traces for interesting scenarios

quantum-witness branch:
  pick one coupling site such as membrane-converter or converter-reservoir
  replace only that bond with a quantum/audit submodule
  keep classical sandbox as the environment/control
```
