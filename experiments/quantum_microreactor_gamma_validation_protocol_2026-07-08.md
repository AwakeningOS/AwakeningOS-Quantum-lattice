# Quantum Microreactor Gamma Validation Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit validation gate`

## Question

Before building a quantum-coupled information microreactor, can a fully dephased diagonal/population embedding reproduce the existing classical-effective sandbox exactly?

The validation target is:

```text
data/microreactor/information_microreactor_sandbox_seed20260707_summary.csv
```

## Why this gate exists

A naive rewrite of scalar variables as amplitudes can produce a quantum-looking model that is only a classical complex-wave or population model in disguise. This protocol prevents that mistake by requiring the `gamma=max` fully dephased limit to reproduce the existing classical sandbox first.

If this gate fails, gamma sweeps, negativity checks, purity checks, and Arm2/Arm3 comparisons are not valid.

## Layer

```text
quantum-audit validation gate
```

This is not a quantum-specific positive result. It is a classical-limit validation for later quantum-coupled experiments.

## Arms for the later full program

```text
Arm 1:
  existing scalar classical-effective sandbox

Arm 2:
  classical complex-wave / single-excitation coherent control

Arm 3:
  density-matrix quantum model with entangling converter or multi-excitation contextual sensing
```

This protocol only tests the prerequisite:

```text
gamma=max fully dephased diagonal/population embedding == Arm 1 scalar sandbox
```

## Model

The validation script imports the existing sandbox definitions from:

```text
scripts/phenomenology/information_microreactor_sandbox.py
```

It then runs a separate diagonal/population embedding with the same component semantics:

```text
source
road / channel
selective membrane
converter A -> P
reservoir
sink / release
terrain writing
B contaminant
D stress
C stabilizer
```

The diagonal embedding has no active off-diagonal coherence. It represents the gamma=max limit only.

## Scenarios

The validation covers all existing sandbox scenarios:

```text
normal
high_load
stress
stabilizer
leaky_membrane
road_fed
storage_heavy
```

## Metrics

All summary metrics from the existing sandbox are compared:

```text
source_A_total
A_in_total
B_in_total
permeability_A
permeability_B
selectivity
P_generated
P_release
P_overflow
release_fraction
overflow_fraction
mean_reservoir
final_reservoir
mean_fill_fraction
mean_backpressure
final_integrity
mean_integrity
mean_quality
terrain_written
efficiency_release_per_A
stability_window
release_cv
source_cv
smoothing_ratio
```

## Success criteria

For every scenario and every metric:

```text
abs(scalar_value - gamma_max_value) <= 1e-9
```

The gate passes only if every compared metric passes.

## Failure criteria

The gate fails if any metric differs beyond tolerance.

If the gate fails:

```text
1. stop the quantum comparison program
2. do not run gamma sweep as if it were matched
3. mark the mapping as invalid or negative validation
4. revise the mapping until gamma=max reproduces the scalar sandbox
```

## Seed

```text
seed = 20260707
```

The current sandbox is deterministic. The seed is retained for interface consistency and future stochastic variants.

## Expected raw outputs

```text
data/quantum_microreactor/gamma_validation_seed20260707_summary.csv
data/quantum_microreactor/gamma_validation_seed20260707_comparison.csv
data/quantum_microreactor/gamma_validation_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_microreactor_gamma_validation.py \
  --seed 20260707 \
  --out data/quantum_microreactor/gamma_validation_seed20260707.json \
  --summary-csv data/quantum_microreactor/gamma_validation_seed20260707_summary.csv \
  --comparison-csv data/quantum_microreactor/gamma_validation_seed20260707_comparison.csv
```

## Forbidden claims

Do not claim:

```text
quantum advantage
quantum-specific behavior
hardware result
entanglement is functionally active
coherence improves the microreactor
quality is quantum coherence
```

This validation can only claim that the gamma=max diagonal/population limit reproduces the existing scalar sandbox.

## Next step if PASS

If this gate passes, the next experiment may build the matched gamma sweep:

```text
gamma = max -> scalar/dephased limit
gamma = 0   -> coherent density-matrix model
intermediate gamma values -> dephasing sensitivity
```

But quantum-specific status still requires Arm2 classical complex-wave control and an observable that Arm2 cannot reproduce.
