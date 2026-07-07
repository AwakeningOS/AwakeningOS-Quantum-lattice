# Quantum-coupled Microreactor Step 2: Dynamic C-R Backpressure

Date: 2026-07-07

Status: `RAW_LOG_BACKED`
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

## Purpose

Step 1 established a designed static C-R bond witness.

Step 2 asks whether the C-R bond changes a functional response:

```text
reservoir capacity -> conversion probability -> release probability -> backpressure index
```

This is still not the full chain:

```text
source -> membrane -> converter -> reservoir -> sink
```

It tests only the C-R submodule.

## Design choice

Use dynamic backpressure.

```text
open_empty_path  = capacity
open_fuller_path = capacity^2
```

The fuller reservoir branch is more strongly suppressed when capacity is low.

## Functional observables

The main observables are defined by the capacity-dependent conversion effect, not by the entanglement witness.

```text
conversion_probability = Tr(E_convert(capacity) rho)
release_probability    = conversion_probability * drain_rate * capacity
backpressure_index     = 1 - conversion_probability(capacity) / conversion_probability(capacity=1)
```

This is not a Bell-target analyzer.

## Arms

For each theta and capacity:

```text
entangled_event:
  |psi(theta)> = cos(theta)|c0,r0> + sin(theta)|c1,r1>

dephased_correlated:
  configuration-basis dephase of entangled_event
  same rho_C/rho_R and same same-pair population
  N(C:R) = 0

product_marginals:
  rho_C(theta) tensor rho_R(theta)
  same rho_C/rho_R but no C-R correlation
  N(C:R) = 0
```

## Marginal audit

For all theta and capacity rows:

```text
marginal_diff_vs_entangled_C_fro = 0.0
marginal_diff_vs_entangled_R_fro = 0.0
```

for the dephased-correlated arm. Product marginals also preserve the single-module reductions by construction.

## Main result at theta/pi = 0.25

| capacity | arm | N(C:R) | conversion | release | backpressure |
|---:|---|---:|---:|---:|---:|
| 1.0 | entangled_event | 0.5 | 0.900000 | 0.720000 | 0.000000 |
| 1.0 | dephased_correlated | 0.0 | 0.450000 | 0.360000 | 0.000000 |
| 1.0 | product_marginals | 0.0 | 0.225000 | 0.180000 | 0.000000 |
| 0.5 | entangled_event | 0.5 | 0.327849 | 0.131140 | 0.635723 |
| 0.5 | dephased_correlated | 0.0 | 0.168750 | 0.067500 | 0.625000 |
| 0.5 | product_marginals | 0.0 | 0.084375 | 0.033750 | 0.625000 |
| 0.1 | entangled_event | 0.5 | 0.038980 | 0.003118 | 0.956689 |
| 0.1 | dephased_correlated | 0.0 | 0.024750 | 0.001980 | 0.945000 |
| 0.1 | product_marginals | 0.0 | 0.012375 | 0.000990 | 0.945000 |

## Result pattern

At theta/pi = 0.25, the entangled C-R bond gives a conversion bonus over the matched dephased control:

```text
capacity 1.0:
  entangled - dephased = 0.450000

capacity 0.5:
  entangled - dephased = 0.159099

capacity 0.1:
  entangled - dephased = 0.014230
```

The bonus decreases as reservoir capacity is restricted.

This is different from Step 1: the observable is not the static C-R Bell-bond analyzer. It is a capacity-dependent conversion/release response.

## Backpressure behavior

The backpressure index rises as capacity is restricted.

At theta/pi = 0.25:

```text
entangled_event:
  capacity 0.5 -> backpressure_index 0.635723
  capacity 0.1 -> backpressure_index 0.956689

dephased_correlated:
  capacity 0.5 -> backpressure_index 0.625000
  capacity 0.1 -> backpressure_index 0.945000
```

Both arms feel backpressure. The entangled arm retains an extra conversion response above the dephased control, but this extra response is also squeezed by low capacity.

## Interpretation

Step 2 shows a designed capacity-dependent C-R conversion response:

```text
matched module marginals
N(C:R) > 0 only in the entangled arm
conversion/release response differs from N=0 controls
capacity restriction changes both response and entangled bonus
```

The result supports a narrow claim:

```text
A capacity-dependent C-R conversion response differs between an entangled C-R bond and N=0 correlated controls under module-marginal matching.
```

## Critical audit note

This is still a designed 6-qubit C-R effect model.

It does not yet prove that a natural full microreactor uses entanglement to integrate parts. It does show that once the functional observable is defined independently of the entanglement witness, the entangled and dephased arms remain distinguishable under backpressure.

## What this does not claim

```text
not a full microreactor
not membrane integration
not source/sink integration
not nonlocal signaling
not quantum advantage
not life-like behavior
not hardware result
```

## Next step

Add the membrane module M only after this C-R backpressure result survives audit.

The next experiment should test:

```text
M-C-R synergy
whole-system response minus independent-component prediction
same module-marginal/dephase discipline
raw-log gate registration
```
