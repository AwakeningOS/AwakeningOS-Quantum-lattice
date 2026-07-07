# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_microreactor_branching_converter_probe
```

This is the latest active quantum-audit probe in the classical-effective / quantum-audit boundary line.

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/quantum_microreactor_branching_converter_probe_2026-07-08.md
experiments/quantum_microreactor_branching_converter_probe_protocol_2026-07-08.md
scripts/audit/quantum_microreactor_branching_converter_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_microreactor_branching_converter_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/branching_converter_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

The new canonical log is:

```text
data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv
```

## Current result

The latest run tests:

```text
phase-dependent branching converter
entangled control qubit
Arm1 scalar fixed branch
Arm2 classical complex-wave branch control
Arm3 entangled control+branch density matrix
```

Verdict:

```text
NEGATIVE_FOR_QUANTUM_SPECIFIC_EFFECT
```

Details:

```text
total_P_release_validation_diff = 0
max_arm3_negativity = 0.353553390593
max_arm2_arm3_main_prob_abs_diff = 0
phase_sensitive_branching_effect = TRUE
arm2_reproduces_branch_observable = TRUE
quantum_specific_effect = FALSE
```

## What this means

Safe claim:

```text
The branching converter produces a large phase-sensitive product-composition effect and Arm3 negativity, but the branch-only observable is fully reproduced by Arm2 classical complex-wave control.
```

This is a strong negative filter: branch-only phase-dependent product composition is not enough for quantum-specific efficacy.

## What this does not mean

Do not claim:

```text
quantum advantage
quantum-specific behavior
functional entanglement
hardware feasibility
chemical realism
biological metabolism
```

## Previous sessions

The immediately previous gamma sweep is:

```text
quantum_microreactor_gamma_sweep_quality_probe_2026-07-08.md
```

The previous validation gate is:

```text
quantum_microreactor_gamma_validation_2026-07-08.md
```

The previous classical-effective observation experiment is:

```text
information_microreactor_backpressure_contamination_2026-07-08.md
```

The earlier quantum-audit/component-semantics bridge is:

```text
quantum_coupled_microreactor_step6_explicit_component_chain_2026-07-07.md
```

## Recommended next decision

The current line has now ruled out:

```text
one-path converter coherence
quality-as-coherence auxiliary probe
branch-only phase-dependent product composition
```

A future quantum-specific attempt would need a non-branch-only observable:

```text
control-conditioned product readout
measurement backaction that changes release or terrain
basis-dependent quality readout that Arm2 cannot reproduce
nonlocal witness tied to reactor output
```

Without one of these, entanglement remains present but functionally unused.
