# Quantum-coupled Microreactor Step 2: Dynamic C-R Backpressure

Date: 2026-07-07

Status: `QUARANTINED_CLAIM`
Layer: `quantum-audit`

Generator script:

```text
scripts/audit/quantum_coupled_microreactor_step2_backpressure.py
```

Raw CSV log:

```text
data/quantum_microreactor/step2_backpressure_seed0_summary.csv
```

Run command:

```bash
python scripts/audit/quantum_coupled_microreactor_step2_backpressure.py --seed 0 --csv data/quantum_microreactor/step2_backpressure_seed0_summary.csv
```

## Quarantine reason

This report is reproducible, but the functional interpretation failed audit.

The intended claim was:

```text
capacity-dependent conversion/release response is independent from the entanglement witness
```

But the implementation does not satisfy that requirement.

## Critical audit finding

The `conversion_effect(capacity=1)` used here is equivalent to the Step 1 Bell-bond projector times `base_rate`:

```text
conversion_effect(capacity=1) == base_rate * |J+><J+|
```

where:

```text
|J+> = (|c0,r0> + |c1,r1>) / sqrt(2)
```

Therefore the reported conversion bonus is still a coherence/Bell-bond readout in disguise.

## Why the claim is invalid

The previous report stated that the observable was not a Bell-target analyzer. That was wrong.

The capacity factor changes the branch weights, but the effect remains a rank-1 coherence-sensitive projector. It does not provide an independent functional population readout.

The observed bonus is therefore a scaled version of the same Step 1 structure, not evidence that a natural device conversion/backpressure function is controlled by entanglement.

## What remains useful

This file remains useful as a negative audit case:

```text
Renaming a Bell-bond projector as conversion_effect does not make it an independent device observable.
```

The lesson for future Step 2 work is:

```text
coherence sensitivity must occur in the dynamics
final readout must be diagonal population after dynamics
```

## Superseding file

The corrected follow-up is:

```text
results/quantum_coupled_microreactor_step2_v2_unitary_population_2026-07-07.md
```

That version uses explicit unitary C-R conversion dynamics and reads only the final diagonal product population.

## What this does not claim

```text
not a valid Step 2 functional witness
not a full microreactor
not membrane integration
not source/sink integration
not nonlocal signaling
not quantum advantage
not life-like behavior
not hardware result
```
