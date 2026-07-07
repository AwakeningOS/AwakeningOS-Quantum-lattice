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
results/quantum_chsh_free_natural_observable_probe_auditor_correction_2026-07-08.md
```

Status:

```text
RAW_LOG_BACKED
NEGATIVE_BY_OBSERVABLE_CLASS
```

Scope:

```text
negative only for CHSH-free local one-body output observables
reduced/product Arm2 reproduction is analytically expected for functions of local marginals
this does not rule out a joint-observable transport effect
not a hardware result
```

## Current results/ classification

| file | status | action |
|---|---|---|
| `quantum_chsh_free_natural_observable_probe_auditor_correction_2026-07-08.md` | META/AUDIT | Correction note: local one-body observable class makes reduced/product Arm2 reproduction analytic; next fair test must use a joint observable with matched local marginals. |
| `quantum_chsh_free_natural_observable_probe_2026-07-08.md` | RAW_LOG_BACKED | CHSH-free local one-body probe. Arm3 is exactly reproduced by reduced/product Arm2 in every row; classification narrowed to NEGATIVE_BY_OBSERVABLE_CLASS. |
| constructed measurement-boundary probes | RAW_LOG_BACKED | Reclassified as POSITIVE_BUT_CONSTRUCTED / constructed-switch characterization. |

## Latest safe finding

```text
NEGATIVE is correct, but the observable class is local one-body. Local marginal functions are analytically blind to joint correlations, so reduced/product Arm2 reproduction follows from the choice of observable. The fair test is a joint observable, such as total yield across two coupled reactors, with local marginals matched between Arm3 and Arm2.
```
