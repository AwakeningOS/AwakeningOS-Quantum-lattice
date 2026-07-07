# Quantum Microreactor Gamma Sweep Quality Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_microreactor_gamma_sweep_quality_probe.py
```

Raw logs:

```text
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_microreactor_gamma_sweep_quality_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv \
  --detail-csv data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv
```

## Purpose

This run is the first usefulness probe after the gamma=max validation gate.

Prior gate:

```text
quantum_microreactor_gamma_validation_2026-07-08.md
```

That gate showed:

```text
gamma=max diagonal/population embedding reproduces existing scalar sandbox summaries
7 scenarios × 24 metrics = 168 comparisons
max_abs_error_overall = 0
```

This follow-up asks whether a simple quality-as-coherence auxiliary probe shows any quantum-specific usefulness when compared against a classical complex-wave control.

## Arms

```text
Arm 1: arm1_scalar
  original scalar sandbox summary observables

Arm 2: arm2_complex_wave
  classical complex-wave control

Arm 3: arm3_quantum_dm
  density-matrix quantum proxy with a negativity proxy
```

## Gamma values

```text
1.0   full dephase / classical limit
0.75
0.50
0.25
0.0   coherent limit
```

## Observable discipline

The validated scalar quality observable is preserved:

```text
mean_quality_z = scalar mean_quality
```

The auxiliary probe is:

```text
coherence_quality_proxy = (1 - gamma) * sqrt(mean_quality_z * (1 - mean_quality_z))
```

This proxy is not allowed to replace scalar quality, because doing so would break the gamma=max validation.

## Verdict

```text
NEGATIVE_FOR_QUANTUM_SPECIFIC_EFFECT
```

## Main result

Across all scenarios:

```text
max_abs_diff_P_release_vs_gamma_max = 0
max_abs_diff_quality_z_vs_gamma_max = 0
arm2_matches_arm3_coherence = TRUE
negativity_changes_observable = FALSE
quantum_specific_effect = FALSE
```

The gamma sweep creates gamma-sensitive coherence and Arm3 negativity proxies, but none of the existing sandbox observables change.

## Scenario summary

| scenario | max Arm2 coherence | max Arm3 coherence | max Arm3 negativity | Arm2 matches Arm3? | negativity changes observable? | quantum-specific? |
|---|---:|---:|---:|---|---|---|
| normal | 0.278161 | 0.278161 | 0.278161 | TRUE | FALSE | FALSE |
| high_load | 0.278161 | 0.278161 | 0.278161 | TRUE | FALSE | FALSE |
| stress | 0.042083 | 0.042083 | 0.042083 | TRUE | FALSE | FALSE |
| stabilizer | 0.266889 | 0.266889 | 0.266889 | TRUE | FALSE | FALSE |
| leaky_membrane | 0.453276 | 0.453276 | 0.453276 | TRUE | FALSE | FALSE |
| road_fed | 0.278161 | 0.278161 | 0.278161 | TRUE | FALSE | FALSE |
| storage_heavy | 0.278161 | 0.278161 | 0.278161 | TRUE | FALSE | FALSE |

## Interpretation

The probe found gamma sensitivity in an auxiliary coherence variable, but that sensitivity is reproduced by the classical complex-wave control.

The quantum arm also has a negativity proxy when gamma is low, but the negativity is not coupled to release, quality_z, terrain, backpressure, or conversion.

Therefore:

```text
coherence exists as a probe variable
negativity exists as a proxy variable
neither produces quantum-specific sandbox efficacy
```

## Safe claim

```text
A first gamma sweep of a quality/coherence auxiliary probe does not show quantum-specific usefulness. The only gamma-sensitive signal is reproduced by the Arm2 classical complex-wave control, while existing sandbox observables remain unchanged.
```

## What this does not show

```text
not quantum advantage
not quantum-specific behavior
not functional entanglement
not coherence-driven improvement
not basis noncommutativity
not hardware relevance
```

## Why this result is useful

This result sorts out a weak quantumization route:

```text
quality-as-coherence by itself is not enough
```

To become meaningful, the next model must make the quantum witness do work in an observable.

## Recommended next experiment

```text
quantum_microreactor_negativity_coupled_observable_probe
```

The next probe should test whether Arm3 negativity can be coupled to an observable such as:

```text
quality_weighted_release
conversion efficiency
membrane-converter sensing
basis-dependent quality readout
```

But it must keep:

```text
Arm1 scalar baseline
Arm2 classical complex-wave control
Arm3 density-matrix quantum model
```

and quantum-specific status still requires Arm3 to produce an observable effect that Arm2 cannot reproduce.
