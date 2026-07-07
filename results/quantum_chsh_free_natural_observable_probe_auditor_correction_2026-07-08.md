# Auditor Correction: CHSH-Free Natural Observable Probe

Date: 2026-07-08

Related report:

```text
results/quantum_chsh_free_natural_observable_probe_2026-07-08.md
```

## Correction

The result is negative, but the label must be narrowed.

Corrected classification:

```text
NEGATIVE_BY_OBSERVABLE_CLASS
```

Reason:

```text
The output rule used only local one-body observables, i.e. functions of rho_C and rho_B. A product state rho_C x rho_B has the same local marginals as rho_CB, so exact reduced/product Arm2 reproduction is analytically guaranteed for this observable class.
```

Therefore:

```text
This probe confirms that natural local one-body observables do not carry irreducible joint-state information. It does not prove that transport has no advantage for joint observables.
```

## Required next fair test

A fair test must use a joint natural observable while still avoiding CHSH, entanglement, and negativity as output definitions.

Proposed next probe:

```text
quantum_joint_yield_marginal_matched_probe
```

Minimal design:

```text
two coupled reactors: reactor_1 and reactor_2
shared resource: rho_12
natural observable: total_yield = release_1 + release_2
Arm3: joint quantum resource
Arm2: product of the exact local marginals, rho_1 x rho_2
question: can total_yield differ while all local marginals are matched?
```

Pre-registered expectation:

```text
NEGATIVE: the current one-way, noncoherent transport sandbox will probably be reproduced by marginal-matched Arm2.
```

## Safe one-line update

```text
NEGATIVE is correct, but the observable class is local one-body. Local marginal functions are analytically blind to joint correlations, so reduced-Arm2 reproduction follows from the choice of observable. The fair test is a joint observable, such as total yield across two coupled reactors, with local marginals matched between Arm3 and Arm2.
```
