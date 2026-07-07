# Results reproducibility status

Date: 2026-07-08

## Current latest session

```text
quantum_chsh_free_natural_observable_probe
```

Backed by:

```text
scripts/audit/quantum_chsh_free_natural_observable_probe.py
data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707_summary.csv
results/quantum_chsh_free_natural_observable_probe_2026-07-08.md
```

Status:

```text
RAW_LOG_BACKED
NEGATIVE_CHSH_FREE_NATURAL_OBSERVABLE_REDUCED_ARM2_REPRODUCES
```

Scope:

```text
negative for naturally irreducible quantum reactor dynamics under CHSH-free output definitions
Arm3 quantum is exactly reproduced by separable reduced/product Arm2 across tested contexts and gamma values
previous measurement-boundary positives should be classified as constructed CHSH-switch studies
not a hardware result
```

## Current results/ classification

| file | status | action |
|---|---|---|
| `quantum_chsh_free_natural_observable_probe_2026-07-08.md` | RAW_LOG_BACKED | Latest adversarial inverted probe. CHSH/entanglement/negativity are excluded from output definitions; natural local one-body observables are used. Arm3 quantum is exactly reproduced by reduced/product Arm2 in every row; positive_rows=0, max_abs_diff_vs_reduced=0. |
| `quantum_context_order_terrain_probe_2026-07-08.md` | RAW_LOG_BACKED | Reclassified as POSITIVE_BUT_CONSTRUCTED_ORDER_EFFECT: noncommuting order signal is explicitly wired into terrain. |
| `quantum_measurement_backaction_terrain_probe_2026-07-08.md` | RAW_LOG_BACKED | Reclassified as TEXTBOOK_BACKACTION_REEXPRESSED: nonselective projection/dephasing suppresses Bell-excess terrain signal. |
| `quantum_fixed_basis_noise_robustness_probe_2026-07-08.md` | RAW_LOG_BACKED | Characterization of constructed fixed-basis membrane CHSH switch under simple simulated noise. |
| `quantum_fixed_basis_shot_budget_probe_2026-07-08.md` | RAW_LOG_BACKED | Characterization of constructed fixed-basis membrane CHSH switch under simulated shot budgets. |
| `quantum_membrane_decision_boundary_probe_2026-07-08.md` | RAW_LOG_BACKED | Reclassified as POSITIVE_BUT_CONSTRUCTED: Bell-excess signal is wired directly into membrane pass/block gates. |
| `quantum_fixed_basis_adaptive_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Reclassified as POSITIVE_BUT_CONSTRUCTED: Bell/order signal is wired into adaptive gate. |
| `quantum_adaptive_measurement_feedback_probe_2026-07-08.md` | RAW_LOG_BACKED | Reclassified as POSITIVE_BUT_CONSTRUCTED: Bell-excess terrain memory is wired into adaptive readout. |
| `quantum_measurement_terrain_memory_probe_2026-07-08.md` | RAW_LOG_BACKED | Reclassified as POSITIVE_BUT_CONSTRUCTED: Bell-excess signal is wired into terrain. |

## Latest safe finding

```text
When CHSH/entanglement/negativity are excluded from output definitions and reactor dynamics use only natural local one-body boundary observables, the quantum Arm3 is exactly reproduced by a separable product of its reduced local states across all tested contexts and gamma values. This supports the auditor critique: previous measurement-boundary positives were constructed CHSH-switch studies, not evidence of naturally irreducible quantum microreactor dynamics.
```
