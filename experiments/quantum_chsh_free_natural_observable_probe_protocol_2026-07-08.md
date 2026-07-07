# Quantum CHSH-Free Natural Observable Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit inverted/adversarial probe`

## Question

If CHSH / entanglement / negativity are not used in the output definition, do natural reactor observables show any irreducible quantum effect beyond a separable reduced/product Arm2?

This is the auditor-requested inverted design.

## Why this probe exists

Earlier measurement-boundary positives wired Bell/CHSH excess into downstream reactor variables. Those are now classified as constructed switch studies, not discovery of natural irreducible quantum reactor dynamics.

This probe removes that construction.

## Forbidden output inputs

The reactor output rule must not use:

```text
CHSH
Bell excess
entanglement
negativity
mutual information
joint noncommuting witness scores
```

## Allowed natural observables

The reactor may use only local one-body reduced-state observables:

```text
<C_X>, <C_Y>, <C_Z>
<B_X>, <B_Y>, <B_Z>
local reduced populations
local reduced coherences
```

These are natural local boundary observables and are reproducible by a separable product of the reduced local states if no genuinely joint information is required.

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

The decisive control is Arm2 reduced/product. If it reproduces Arm3, then natural observables are not irreducibly quantum in this sandbox.

## Contexts

```text
normal_natural
stress_natural
storage_natural
contaminated_stress_natural
```

## Gamma values

```text
1.0, 0.5, 0.25, 0.0
```

## Natural reactor rule

A local alignment signal is computed from local one-body observables only:

```text
local_alignment = clamp(0.5 + 0.22*<B_X> + 0.14*<C_X> - 0.08*|<B_Y>| - 0.04*|<C_Y>|)
```

Then:

```text
A gate = 0.90 + 0.25 * local_alignment
B gate = max(0.20, 1.05 - 0.35 * local_alignment)
D gate = max(0.25, 1.05 - 0.30 * local_alignment)
```

No CHSH or entanglement-derived quantity enters the output rule.

## Success criterion for a true positive

A true positive would require:

```text
Arm3 quantum differs from Arm2 reduced/product on release, quality, terrain, or membrane selectivity.
```

## Expected result

Pre-registered expectation:

```text
NEGATIVE: Arm2 reduced/product reproduces Arm3 exactly.
```

## Expected outputs

```text
data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707_summary.csv
data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_chsh_free_natural_observable_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707_summary.csv
```
