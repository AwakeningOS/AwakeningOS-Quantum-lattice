# Information Microreactor Backpressure + Contamination Observation

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `classical-effective phenomenology`

Generator script:

```text
scripts/phenomenology/information_microreactor_backpressure_contamination.py
```

Raw logs:

```text
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv
```

Timeseries note:

```text
timeseries.csv uses deterministic 50-step checkpoints plus final row.
Exact threshold times are preserved in events.csv.
```

Auxiliary metadata:

```text
data/microreactor/information_microreactor_backpressure_contamination_seed20260707.json
```

Run command:

```bash
python scripts/phenomenology/information_microreactor_backpressure_contamination.py \
  --seed 20260707 \
  --out data/microreactor/information_microreactor_backpressure_contamination_seed20260707.json \
  --summary-csv data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv \
  --events-csv data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv \
  --timeseries-csv data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv \
  --timeseries-stride 50
```

## Purpose

The previous `information_microreactor_sandbox` showed that source, road/channel, selective membrane, converter, reservoir, sink/release, terrain writing, stress, stabilizer, and contaminant can be assembled into a classical-effective information microreactor-like sandbox.

This follow-up changes the focus from scenario means to time-resolved observation.

The question is:

```text
When backpressure, contamination, stress, stabilizer rescue, and road/terrain feedback are combined into one continuous state trajectory, do ordered information-material failure and recovery modes appear?
```

## Timeline

The run is one continuous trajectory. State is not reset between phases.

```text
0-199   clean_finite_reactor
200-399 leaky_contamination
400-599 storage_pressure
600-799 stress_collapse
800-999 stabilizer_rescue
```

## Main phase summary

| phase | P release | mean quality | max fill | min backpressure | final integrity | quality-weighted release | stability window |
|---|---:|---:|---:|---:|---:|---:|---:|
| clean_finite_reactor | 28.989639 | 0.936917 | 0.095452 | 0.928411 | 0.941641 | 26.954639 | 0.909332 |
| leaky_contamination | 35.037259 | 0.304214 | 0.096665 | 0.927501 | 0.884666 | 10.864410 | 0.277716 |
| storage_pressure | 2.484825 | 0.263681 | 0.785492 | 0.057409 | 0.829042 | 0.662932 | 0.225870 |
| stress_collapse | 2.785647 | 0.495080 | 0.788261 | 0.054086 | 0.000000 | 1.369839 | 0.125002 |
| stabilizer_rescue | 24.808685 | 0.865466 | 0.164113 | 0.876915 | 0.671560 | 21.303883 | 0.399015 |

## Event log

| event | t | phase | quality | fill | backpressure | integrity | release |
|---|---:|---|---:|---:|---:|---:|---:|
| quality_lt_0_7 | 206 | leaky_contamination | 0.679076 | 0.091646 | 0.931265 | 0.939623 | 0.188954 |
| quality_lt_0_5 | 218 | leaky_contamination | 0.491227 | 0.096237 | 0.927823 | 0.936169 | 0.197772 |
| quality_lt_0_3 | 259 | leaky_contamination | 0.299837 | 0.083750 | 0.937188 | 0.924404 | 0.171959 |
| backpressure_lt_0_5 | 410 | storage_pressure | 0.225672 | 0.424526 | 0.490568 | 0.881571 | 0.007806 |
| fill_gt_0_5 | 420 | storage_pressure | 0.232621 | 0.503026 | 0.396369 | 0.878762 | 0.009183 |
| backpressure_lt_0_2 | 462 | storage_pressure | 0.255665 | 0.668195 | 0.198166 | 0.867000 | 0.012090 |
| fill_gt_0_75 | 510 | storage_pressure | 0.272125 | 0.750611 | 0.099267 | 0.853630 | 0.013539 |
| integrity_lt_0_5 | 648 | stress_collapse | 0.355511 | 0.787915 | 0.054502 | 0.498292 | 0.014196 |
| integrity_lt_0_1 | 708 | stress_collapse | 0.483511 | 0.779457 | 0.064651 | 0.093292 | 0.014039 |
| rescue_integrity_gt_0_5_after_800 | 893 | stabilizer_rescue | 0.880029 | 0.057719 | 0.956711 | 0.500409 | 0.094091 |

## Observations

### 1. Contamination first degrades quality while flow continues

During `leaky_contamination`, raw release remains high, but quality-weighted release falls sharply.

```text
clean_finite_reactor:
  P_release = 28.989639
  quality_weighted_release = 26.954639
  mean_quality = 0.936917

leaky_contamination:
  P_release = 35.037259
  quality_weighted_release = 10.864410
  mean_quality = 0.304214
```

Threshold events occur early:

```text
quality < 0.7 at t=206
quality < 0.5 at t=218
quality < 0.3 at t=259
```

This is a throughput-preserving quality degradation mode.

### 2. Storage pressure produces downstream-to-upstream modulation

During `storage_pressure`, the reservoir fills and backpressure throttles the upstream intake/conversion path.

```text
max_fill_fraction = 0.785492
min_backpressure = 0.057409
P_release = 2.484825
```

Threshold events:

```text
backpressure < 0.5 at t=410
fill > 0.5 at t=420
backpressure < 0.2 at t=462
fill > 0.75 at t=510
```

This is the cleanest device-like behavior in the run: downstream storage state changes upstream flow.

### 3. Stress collapse is distinct from contamination

During `stress_collapse`, membrane integrity collapses.

```text
final_integrity = 0.000000
min_backpressure = 0.054086
P_release = 2.785647
```

Events:

```text
integrity < 0.5 at t=648
integrity < 0.1 at t=708
```

This is a membrane-failure mode, not just product-quality degradation.

### 4. External stabilizer partially restores membrane integrity

During `stabilizer_rescue`, the same stress load is present, but external C stabilizer is supplied.

```text
final_integrity = 0.671560
mean_quality = 0.865466
P_release = 24.808685
quality_weighted_release = 21.303883
```

Event:

```text
integrity > 0.5 after rescue starts at t=893
```

This is stabilizer-assisted recovery, not autonomous self-repair.

## Safe claim

```text
A code-backed classical-effective observation sandbox shows temporally ordered information-material modes. Contamination degrades product quality before flow stops; reservoir saturation produces upstream backpressure; stress collapses membrane integrity; and external stabilizer input partially restores membrane integrity. These are classical-effective component dynamics, not quantum-specific effects.
```

## What this does not claim

```text
not quantum-specific
not quantum advantage
not hardware result
not biological metabolism
not life-like behavior
not autonomous self-repair
not autonomous self-regulation
```

## Current latest-session note

This is the current latest experiment after `information_microreactor_sandbox_2026-07-07.md`.

The immediately previous quantum-audit/component-semantics bridge remains:

```text
results/quantum_coupled_microreactor_step6_explicit_component_chain_2026-07-07.md
```

But the current front line is the classical-effective observation branch:

```text
information_microreactor_backpressure_contamination
```

## Next useful continuation

```text
1. split contamination from backpressure in controlled 2x2 sweeps
2. add per-step causal ablations:
   - no terrain write
   - no B poison
   - no backpressure feedback
   - no stabilizer repair
3. map the reservoir capacity × release_rate × B leakage phase diagram
4. preserve event logs as first-class data, not only phase summaries
```
