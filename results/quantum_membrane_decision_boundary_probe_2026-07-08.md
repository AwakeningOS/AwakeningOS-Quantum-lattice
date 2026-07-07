# Quantum Membrane Decision Boundary Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_membrane_decision_boundary_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/membrane_decision_boundary_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/membrane_decision_boundary_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_membrane_decision_boundary_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/membrane_decision_boundary_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/membrane_decision_boundary_probe_seed20260707_summary.csv
```

## Purpose

This experiment tests whether a fixed-basis finite-shot CHSH measurement-boundary signal can modulate the membrane pass/block decision directly.

Previous positive line:

```text
measurement boundary -> terrain -> later release/adaptive gate
```

This probe moves closer to the reactor body:

```text
measurement boundary -> membrane decision -> A/B/D passage -> quality/release
```

## Design

A conservative fixed-basis CHSH excess is sampled at each step.

If the Bell-bound margin is exceeded, the membrane gate changes:

```text
A gate opens:      a_gate = 1 + 0.25 * signal
B gate closes:     b_gate = max(0, 1 - 1.80 * signal)^2
D gate closes:     d_gate = max(0.02, 1 - 0.90 * signal)
```

The basis is fixed in advance from the stress/Bell point and reused everywhere. There is no per-step basis optimization.

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_MEMBRANE_DECISION_BOUNDARY
```

## P1 gamma=1 null

Result: PASS.

| scenario | gamma | membrane signal | A pass dev | B leak dev | D pass dev | release dev |
|---|---:|---:|---:|---:|---:|---:|
| normal_membrane | 1.0 | 0.000000 | 0.000000% | 0.000000% | 0.000000% | 0.000000% |
| stress_membrane | 1.0 | 0.000000 | 0.000000% | 0.000000% | 0.000000% | 0.000000% |
| storage_membrane | 1.0 | 0.000000 | 0.000000% | 0.000000% | 0.000000% | 0.000000% |
| contaminated_stress_membrane | 1.0 | 0.000000 | 0.000000% | 0.000000% | 0.000000% | 0.000000% |

## P2 stress membrane selectivity

Result: PASS.

| gamma | membrane signal total | positive steps | A pass dev | B leak dev | D pass dev | quality dev | release dev |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.25 | 22.057835 | 666 | +0.027953% | -0.057986% | -2.481506% | +0.000604% | +0.027953% |
| 0.0 | 604.853992 | 721 | +26.657798% | -18.877682% | -68.046074% | +0.194860% | +26.657798% |

The stress context shows the intended selection pattern:

```text
A passage increases
B contaminant leak decreases
D stress passage decreases
release increases
```

## P3 contaminated stress membrane

Result: PASS.

A higher-B stress case was included to make the contaminant decision visible.

| gamma | membrane signal total | positive steps | A pass dev | B leak dev | D pass dev | quality dev | release dev |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.25 | 22.655554 | 664 | +0.017283% | -0.035271% | -2.548750% | +0.001043% | +0.017283% |
| 0.0 | 605.038256 | 721 | +26.894291% | -18.794025% | -68.066804% | +0.540460% | +26.894291% |

## P4 normal/storage specificity

Result: PASS.

At gamma=0, normal and storage do not create the membrane decision signal:

| scenario | membrane signal total | positive steps | A pass dev | B leak dev | D pass dev | release dev |
|---|---:|---:|---:|---:|---:|---:|
| normal_membrane | 0.000000 | 0 | 0.000000% | 0.000000% | 0.000000% | 0.000000% |
| storage_membrane | 0.000000 | 0 | 0.000000% | 0.000000% | 0.000000% | 0.000000% |

## P5 matched replay specificity

Result: PASS.

For all rows:

```text
matched_replay_release_diff = 0
```

Interpretation:

```text
post-gate reactor dynamics follow the membrane gate trace
specificity remains at the Bell-bound measurement/decision boundary
```

## Full stress summaries

### stress_membrane

| gamma | signal | steps | max S_hat | A dev | B dev | D dev | quality dev | release dev | mean A gate | mean B gate | mean D gate | effect? |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1.0 | 0.000000 | 0 | 0.035278 | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 1.000000 | 1.000000 | 1.000000 | FALSE |
| 0.75 | 0.000000 | 0 | 0.743042 | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 1.000000 | 1.000000 | 1.000000 | FALSE |
| 0.5 | 0.000000 | 0 | 1.444458 | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 1.000000 | 1.000000 | 1.000000 | FALSE |
| 0.25 | 22.057835 | 666 | 2.148438 | +0.027953% | -0.057986% | -2.481506% | +0.000604% | +0.027953% | 1.006893 | 0.904051 | 0.975185 | TRUE |
| 0.0 | 604.853992 | 721 | 2.854492 | +26.657798% | -18.877682% | -68.046074% | +0.194860% | +26.657798% | 1.189017 | 0.110804 | 0.319539 | TRUE |

### contaminated_stress_membrane

| gamma | signal | steps | max S_hat | A dev | B dev | D dev | quality dev | release dev | mean A gate | mean B gate | mean D gate | effect? |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1.0 | 0.000000 | 0 | 0.033630 | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 1.000000 | 1.000000 | 1.000000 | FALSE |
| 0.75 | 0.000000 | 0 | 0.741089 | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 1.000000 | 1.000000 | 1.000000 | FALSE |
| 0.5 | 0.000000 | 0 | 1.446899 | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 0.000000% | 1.000000 | 1.000000 | 1.000000 | FALSE |
| 0.25 | 22.655554 | 664 | 2.148010 | +0.017283% | -0.035271% | -2.548750% | +0.001043% | +0.017283% | 1.007080 | 0.901536 | 0.974513 | TRUE |
| 0.0 | 605.038256 | 721 | 2.848389 | +26.894291% | -18.794025% | -68.066804% | +0.540460% | +26.894291% | 1.189074 | 0.110967 | 0.319332 | TRUE |

## Interpretation

This is the clearest membrane-boundary result so far.

Supported chain:

```text
fixed-basis finite-shot CHSH signal
-> membrane decision boundary
-> A passage increases
-> B contaminant and D stress passage decrease
-> downstream release and quality change
```

This differs from terrain feedback because the measurement-boundary signal acts at the input selection boundary rather than after output inscription.

## Safe claim

```text
A fixed-basis finite-shot CHSH measurement-boundary signal can directly modulate membrane pass/block decisions in stress contexts: A passage increases while B contaminant and D stress passage are suppressed. Matched replay shows downstream dynamics follow the gate trace; specificity remains at the Bell-bound measurement/decision boundary.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not ordinary local population plumbing
not quantum-specific post-gate reactor physics
```

## Next boundary

The next planned experiments are:

```text
quantum_fixed_basis_shot_budget_probe
quantum_fixed_basis_noise_robustness_probe
quantum_measurement_backaction_terrain_probe
quantum_context_order_terrain_probe
```
