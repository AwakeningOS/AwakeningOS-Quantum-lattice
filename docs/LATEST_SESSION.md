# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_chsh_free_natural_observable_probe
```

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
results/quantum_chsh_free_natural_observable_probe_2026-07-08.md
experiments/quantum_chsh_free_natural_observable_probe_protocol_2026-07-08.md
scripts/audit/quantum_chsh_free_natural_observable_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_chsh_free_natural_observable_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707_summary.csv
```

## Current result

```text
NEGATIVE_CHSH_FREE_NATURAL_OBSERVABLE_REDUCED_ARM2_REPRODUCES
```

Key results:

```text
positive_rows = 0
reduced_arm2_max_abs_diff_overall = 0
matched_replay_max_abs_diff_overall = 0
all tested contexts/gamma values: Arm3 quantum exactly reproduced by separable reduced/product Arm2
```

## Safe claim

```text
When CHSH/entanglement/negativity are excluded from output definitions and reactor dynamics use only natural local one-body boundary observables, the quantum Arm3 is exactly reproduced by a separable product of its reduced local states across all tested contexts and gamma values. This supports the auditor critique: previous measurement-boundary positives were constructed CHSH-switch studies, not evidence of naturally irreducible quantum microreactor dynamics.
```

## Updated classification

```text
constructed CHSH-switch probes: POSITIVE_BUT_CONSTRUCTED
CHSH-free natural observable probe: NEGATIVE
```
