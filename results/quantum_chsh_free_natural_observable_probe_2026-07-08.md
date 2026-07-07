# Quantum CHSH-Free Natural Observable Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit inverted/adversarial probe`

Generator script:

```text
scripts/audit/quantum_chsh_free_natural_observable_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_chsh_free_natural_observable_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707_summary.csv
```

## Purpose

This is the auditor-requested inverted/adversarial test.

It asks whether natural reactor observables show an irreducible quantum effect when CHSH / entanglement / negativity are not used in the output definition.

Previous constructed-positive line:

```text
CHSH/Bell-excess signal -> terrain/membrane/release
```

This probe removes that construction.

## Output rule restrictions

The output rule does not use:

```text
CHSH
Bell excess
entanglement
negativity
mutual information
joint noncommuting witness scores
```

The reactor may use only local one-body reduced-state observables:

```text
<C_X>, <C_Y>, <C_Z>
<B_X>, <B_Y>, <B_Z>
local reduced populations
local reduced coherences
```

## Arms

```text
Arm3 quantum:
  full two-qubit boundary state rho_CB

Arm2 reduced/product:
  rho_C ⊗ rho_B, where rho_C and rho_B are the exact marginals of Arm3

Arm2 diagonal:
  diagonal-only state with the same computational-basis populations

Matched replay:
  exact replay of the local natural gate trace
```

The decisive control is Arm2 reduced/product, not the weaker diagonal-only control.

## Natural reactor rule

A local alignment signal is computed from one-body observables only:

```text
local_alignment = clamp(0.5 + 0.22*<B_X> + 0.14*<C_X> - 0.08*|<B_Y>| - 0.04*|<C_Y>|)
```

Then:

```text
A gate = 0.90 + 0.25 * local_alignment
B gate = max(0.20, 1.05 - 0.35 * local_alignment)
D gate = max(0.25, 1.05 - 0.30 * local_alignment)
```

No CHSH-derived quantity enters the output rule.

## Verdict

```text
NEGATIVE_CHSH_FREE_NATURAL_OBSERVABLE_REDUCED_ARM2_REPRODUCES
```

## Main result

Across all tested contexts and gamma values:

```text
positive_rows = 0
reduced_arm2_max_abs_diff_overall = 0
matched_replay_max_abs_diff_overall = 0
```

Meaning:

```text
Arm3 quantum is exactly reproduced by Arm2 reduced/product.
```

## Context summary

| scenario | gamma values | max diff vs reduced/product Arm2 | irreproducible? |
|---|---|---:|---|
| normal_natural | 1.0, 0.5, 0.25, 0.0 | 0.000000 | FALSE |
| stress_natural | 1.0, 0.5, 0.25, 0.0 | 0.000000 | FALSE |
| storage_natural | 1.0, 0.5, 0.25, 0.0 | 0.000000 | FALSE |
| contaminated_stress_natural | 1.0, 0.5, 0.25, 0.0 | 0.000000 | FALSE |

## Stress rows

The stress rows are especially important because previous constructed positives concentrated there.

| scenario | gamma | release Arm3 | release Arm2 reduced | release dev | terrain Arm3 | terrain Arm2 reduced | classification |
|---|---:|---:|---:|---:|---:|---:|---|
| stress_natural | 1.0 | 83.701208 | 83.701208 | 0.000000% | 0.003597 | 0.003597 | NEGATIVE |
| stress_natural | 0.5 | 83.701208 | 83.701208 | 0.000000% | 0.003597 | 0.003597 | NEGATIVE |
| stress_natural | 0.25 | 83.701208 | 83.701208 | 0.000000% | 0.003597 | 0.003597 | NEGATIVE |
| stress_natural | 0.0 | 83.701208 | 83.701208 | 0.000000% | 0.003597 | 0.003597 | NEGATIVE |

## Diagonal control note

The diagonal-only control can differ in some non-stress rows:

```text
diagonal_control_max_abs_diff_overall = 71.308358583029
```

This does not rescue a positive result, because the stronger separable control `rho_C ⊗ rho_B` exactly reproduces Arm3. The diagonal-only control is too weak when the natural output rule uses local coherences.

## Interpretation

This is the first genuinely informative result after the auditor challenge.

It supports the auditor critique:

```text
Previous measurement-boundary positives were constructed CHSH-switch studies.
When CHSH/entanglement/negativity are removed from output definitions, natural reactor observables are fully reproduced by a separable reduced/product Arm2.
```

## Safe claim

```text
When CHSH/entanglement/negativity are excluded from output definitions and reactor dynamics use only natural local one-body boundary observables, the quantum Arm3 is exactly reproduced by a separable product of its reduced local states across all tested contexts and gamma values. This supports the auditor critique: previous measurement-boundary positives were constructed CHSH-switch studies, not evidence of naturally irreducible quantum microreactor dynamics.
```

## Updated classification implication

```text
constructed CHSH-switch probes: POSITIVE_BUT_CONSTRUCTED
CHSH-free natural observable probe: NEGATIVE
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal proof that all possible CHSH-free observables are classical
not a denial of Bell/noncommuting measurement physics
```

## Next step

The current measurement-boundary line should be synthesized as:

```text
1. Negative for ordinary/local/natural reactor observables.
2. Positive only when Bell/CHSH/noncommuting witness signals are explicitly wired into the boundary.
3. Therefore the honest status is constructed-switch characterization, not discovery of naturally irreducible reactor dynamics.
```
