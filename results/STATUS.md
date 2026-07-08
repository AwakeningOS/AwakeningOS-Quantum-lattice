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
| `information_microreactor_whole_state_quantum_sandbox_2026-07-08.md` | RAW_LOG_BACKED | Coarse 10-bit/10-qubit whole-state sandbox comparison. Coherent whole-state evolution differs from dephased/classical finite-state evolution; not a full continuous quantum microreactor and not hardware. |
| `information_microreactor_quantumized_comparison_2026-07-08.md` | RAW_LOG_BACKED | Earlier finite-core comparison. Only M/C/R pass-convert-store core was quantumized; summaries matched classical probability core. |
| `quantum_chsh_free_natural_observable_probe_auditor_correction_2026-07-08.md` | META/AUDIT | Correction note: local one-body observable class makes reduced/product Arm2 reproduction analytic; next fair test must use a joint observable with matched local marginals. |
| `quantum_chsh_free_natural_observable_probe_2026-07-08.md` | RAW_LOG_BACKED | CHSH-free local one-body probe. Arm3 is exactly reproduced by reduced/product Arm2 in every row; classification narrowed to NEGATIVE_BY_OBSERVABLE_CLASS. |
| constructed measurement-boundary probes | RAW_LOG_BACKED | Reclassified as POSITIVE_BUT_CONSTRUCTED / constructed-switch characterization. |

## Whole-state sandbox comparison

```text
information_microreactor_whole_state_quantum_sandbox
```

Backed by:

```text
scripts/phenomenology/information_microreactor_whole_state_quantum_sandbox.py
data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_summary.csv
data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_events.csv
```

Safe finding:

```text
The earlier M/C/R finite-core quantumization was too local and matched the classical probability core.
The whole-state 10-bit/10-qubit coarse quantumization puts A/M/C/R/O/Q/B/T/D/S into one coupled state.
Under the tested coupled dynamics, coherent whole-state evolution differs from dephased/classical finite-state evolution in aggregate observables and event times.
This is a finite-model whole-state coherence/interference effect, not hardware evidence and not a full continuous-variable quantum microreactor.
```

## Latest safe finding

```text
NEGATIVE is correct, but the observable class is local one-body. Local marginal functions are analytically blind to joint correlations, so reduced/product Arm2 reproduction follows from the choice of observable. The fair test is a joint observable, such as total yield across two coupled reactors, with local marginals matched between Arm3 and Arm2.
```
