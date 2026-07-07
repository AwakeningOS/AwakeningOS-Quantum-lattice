# RAW_LOG gate policy

The RAW_LOG gate protects `RAW_LOG_BACKED` reports from stale or unreproducible raw logs.

## Current gate

Run:

```bash
python scripts/check_raw_logs.py
```

The script regenerates canonical raw logs into a temporary directory and compares them against the committed raw logs.

## Current canonical logs

```text
data/negativity_causality/negativity_causality_test_seed0.json
data/converter/converter_core_seed8128_summary.csv
data/microreactor/information_microreactor_sandbox_seed20260707_summary.csv
data/microreactor/information_microreactor_quantumized_comparison_seed20260707_summary.csv
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv
data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv
data/quantum_microreactor/gamma_validation_seed20260707_summary.csv
data/quantum_microreactor/gamma_validation_seed20260707_comparison.csv
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv
data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv
data/quantum_microreactor/transported_branching_arm2_kill_seed20260707_summary.csv
data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv
data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv
data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv
data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv
data/quantum_microreactor/step1_cr_coupling_seed0_summary.csv
data/quantum_microreactor/step2_backpressure_seed0_summary.csv
data/quantum_microreactor/step2_v2_unitary_population_seed0_summary.csv
data/quantum_microreactor/step3_svetlichny_seed0_summary.csv
data/quantum_microreactor/step4_population_synergy_seed0_summary.csv
data/quantum_microreactor/step5_reactor_like_population_synergy_seed0_summary.csv
data/quantum_microreactor/step6_explicit_component_chain_seed0_summary.csv
```

## Latest terrain memory probe

```text
quantum_measurement_terrain_memory_probe
```

Canonical raw log:

```text
data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv
```

Meaning:

```text
Finite-shot sampled CHSH terrain inscription persists after measurement stops in stress context and weakly affects a later challenge phase. Matched classical replay shows post-write memory itself is classical-effective.
```

## Previous sampled terrain feedback probe

```text
quantum_sampled_chsh_terrain_feedback_probe
```

Canonical raw log:

```text
data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv
```

Meaning:

```text
Finite-shot sampled CHSH, after a conservative Bell-bound margin, writes terrain only in the high-violation stress context.
```

## Comparison policy

The gate uses normalized content comparison, not byte comparison.

```text
JSON: parse and compare structure/numeric leaves with tolerance.
CSV: compare headers, row counts, numeric cells, and nonnumeric cells.
```

Default tolerance:

```text
rtol = 1e-9
atol = 1e-9
```

## Rule

A result must not be labeled `RAW_LOG_BACKED` unless this gate passes or the report documents an equivalent reproducibility check.
