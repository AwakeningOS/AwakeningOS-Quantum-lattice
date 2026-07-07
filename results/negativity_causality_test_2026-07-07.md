# Minimal Basis-relative Causality Test

Date: 2026-07-07

Status: `RAW_LOG_BACKED`

Generator script:

```text
scripts/negativity_causality_test.py
```

Raw log:

```text
data/negativity_causality/negativity_causality_test_seed0.json
```

Run command:

```bash
python scripts/negativity_causality_test.py --out data/negativity_causality/negativity_causality_test_seed0.json
```

## Correct layer

This file belongs to the audit/witness inventory, not to the current component-development front line.

It should not be used to claim that the converter, membrane, reservoir, or source-sink components are quantum-specific.

## Question

The audit exposed the key hole in the program:

```text
A witness may be present without being load-bearing for a behavior.
```

This test asks a minimal causal question:

```text
Can a coherent arm change a channel outcome when one-particle marginals are exactly matched against controls?
```

## Design

Three arms are constructed from the same Bell-origin state.

```text
arm1 coherent:
  rho = |Phi+><Phi+|
  |Phi+> = (|00> + |11>) / sqrt(2)

arm2 dephased:
  configuration-basis dephase of arm1
  same rho1/rho2
  N = 0

arm3 product_marginals:
  rho1(arm1) tensor rho2(arm1)
  same rho1/rho2
  N = 0
```

The product arm is mixed. This is intentional: exact marginal matching with a pure product state is impossible for the maximally mixed Bell marginals.

The contact/channel analyzer is:

```text
H tensor H
```

followed by two output channels:

```text
same channel:
  |00><00| + |11><11|

anti channel:
  |01><01| + |10><10|
```

## Marginal audit

The one-particle reductions match exactly.

| comparison | rho1 Frobenius | rho2 Frobenius | rho1 max abs | rho2 max abs |
|---|---:|---:|---:|---:|
| coherent vs dephased | 0.0 | 0.0 | 0.0 | 0.0 |
| coherent vs product_marginals | 0.0 | 0.0 | 0.0 | 0.0 |

## Results

| arm | negativity | P(same channel) | P(anti channel) |
|---|---:|---:|---:|
| coherent | 0.5 | 1.0 | 0.0 |
| dephased | 0.0 | 0.5 | 0.5 |
| product_marginals | 0.0 | 0.5 | 0.5 |

Contrasts:

```text
coherent - dephased P(same) = 0.5
coherent - product P(same)  = 0.5
dephased - product P(same)  = 0.0
```

## Verdict

```text
PASS_MINIMAL_LOAD_BEARING_COHERENCE_BASIS_RELATIVE_CLASSICAL_EFFECTIVE
```

Pattern:

```text
outcome(coherent) != outcome(dephased, N=0) == outcome(product_marginals, N=0)
```

with exact one-particle marginal matching.

## Correct interpretation

This is a minimal positive result for a basis-relative channel analyzer:

```text
matched marginals
coherent arm differs from N=0 controls
channel outcome changes
```

It is not a quantum-specific component claim.

## What this does not prove

This does not prove that previous droplet, history-terrain, membrane, converter, reservoir, source-sink, or information-matter phenomenology requires a quantum witness.

Limitations:

```text
1. minimal two-qubit channel test
2. not a spatial lattice/droplet transport experiment
3. contact analyzer is designed to read the chosen basis relation
4. audit-chapter inventory, not component-development evidence
```

## Current use

Use this file only as a guardrail example for matched controls.

The component-development front line remains classical-effective phenomenology unless a separate witness chapter promotes a substructure with stronger controls.
