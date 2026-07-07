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
data/quantum_microreactor/step1_cr_coupling_seed0_summary.csv
data/quantum_microreactor/step2_backpressure_seed0_summary.csv
data/quantum_microreactor/step2_v2_unitary_population_seed0_summary.csv
data/quantum_microreactor/step3_svetlichny_seed0_summary.csv
data/quantum_microreactor/step4_population_synergy_seed0_summary.csv
data/quantum_microreactor/step5_reactor_like_population_synergy_seed0_summary.csv
data/quantum_microreactor/step6_explicit_component_chain_seed0_summary.csv
```

## Latest comparison log

The latest comparison is:

```text
information_microreactor_quantumized_comparison
```

It adds one summary raw CSV log:

```text
data/microreactor/information_microreactor_quantumized_comparison_seed20260707_summary.csv
```

This log compares:

```text
classical_probability_core
quantum_dephased_core
quantum_coherent_core
```

for the finite M/C/R pass-convert-store core embedded in the classical sandbox environment.

## Latest observation logs

The latest time-resolved observation experiment is:

```text
information_microreactor_backpressure_contamination
```

It adds three first-class raw CSV logs:

```text
summary.csv:
  phase-level totals and means

events.csv:
  threshold crossing times for quality, fill, backpressure, integrity, and rescue

timeseries.csv:
  deterministic 50-step checkpoints plus final row
```

These logs are required because the result depends on temporal ordering, not only phase averages. Exact threshold times live in events.csv; timeseries.csv keeps compact trajectory checkpoints.

## Comparison policy

The gate uses normalized content comparison, not byte comparison.

```text
JSON:
  parse with json.load
  compare structure recursively
  compare numeric leaves with tolerance

CSV:
  parse with csv.DictReader
  compare headers and row count exactly
  compare numeric cells with tolerance
  compare nonnumeric cells exactly
```

Default tolerance:

```text
rtol = 1e-9
atol = 1e-9
```

Rationale:

```text
Byte comparison catches stale logs but also false-alarms on harmless JSON
formatting, CSV float spelling, newline, or environment-level float representation
differences. The goal is to catch scientific/content skew, not formatting skew.
```

## Local pre-commit options

Option A: use pre-commit.

```bash
pip install pre-commit
pre-commit install
```

This uses `.pre-commit-config.yaml`.

Option B: install a plain git hook.

```bash
bash scripts/install_pre_commit_hook.sh
```

This writes `.git/hooks/pre-commit` to run:

```bash
python scripts/check_raw_logs.py
```

## Rule

A result must not be labeled `RAW_LOG_BACKED` unless this gate passes or the report documents an equivalent reproducibility check.
