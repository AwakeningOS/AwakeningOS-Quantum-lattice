# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_microreactor_gamma_sweep_quality_probe
```

This is the latest active quantum-audit probe in the classical-effective / quantum-audit boundary line.

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/quantum_microreactor_gamma_sweep_quality_probe_2026-07-08.md
experiments/quantum_microreactor_gamma_sweep_quality_probe_protocol_2026-07-08.md
scripts/audit/quantum_microreactor_gamma_sweep_quality_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_microreactor_gamma_sweep_quality_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv \
  --detail-csv data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

The new canonical logs are:

```text
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv
```

## Current result

The latest run tests:

```text
quality/coherence auxiliary probe
with gamma sweep
Arm1 scalar baseline
Arm2 classical complex-wave control
Arm3 density-matrix quantum proxy
```

Verdict:

```text
NEGATIVE_FOR_QUANTUM_SPECIFIC_EFFECT
```

Details:

```text
max_abs_diff_P_release_vs_gamma_max = 0
max_abs_diff_quality_z_vs_gamma_max = 0
arm2_matches_arm3_coherence = TRUE
negativity_changes_observable = FALSE
quantum_specific_effect = FALSE
```

## What this means

Safe claim:

```text
The first quality/coherence gamma sweep does not show quantum-specific usefulness. Gamma-sensitive coherence appears, but Arm2 reproduces it and existing sandbox observables do not change.
```

This is a useful negative filter: quality-as-coherence alone is not enough.

## What this does not mean

Do not claim:

```text
quantum advantage
quantum-specific behavior
functional entanglement
coherence-driven improvement
basis noncommutativity
hardware feasibility
```

## Previous sessions

The immediately previous validation gate is:

```text
quantum_microreactor_gamma_validation_2026-07-08.md
```

The previous comparison is:

```text
information_microreactor_quantumized_comparison_2026-07-08.md
```

The previous classical-effective observation experiment is:

```text
information_microreactor_backpressure_contamination_2026-07-08.md
```

The earlier quantum-audit/component-semantics bridge is:

```text
quantum_coupled_microreactor_step6_explicit_component_chain_2026-07-07.md
```

## Recommended next experiment

```text
quantum_microreactor_negativity_coupled_observable_probe
```

Required discipline:

```text
Arm 1: scalar classical sandbox
Arm 2: classical complex-wave control
Arm 3: density-matrix quantum model
```

The next probe must make the witness do work in an observable, for example:

```text
quality_weighted_release
conversion efficiency
membrane-converter sensing
basis-dependent quality readout
```

Quantum-specific status still requires Arm3 to produce an observable effect that Arm2 cannot reproduce.
