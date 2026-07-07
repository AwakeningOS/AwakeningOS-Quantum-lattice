# Negativity Causality Test

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

## Question

The audit exposed the key hole in the program:

```text
negativity exists, but has not yet been shown to be load-bearing for behavior.
```

This test asks a minimal causal question:

```text
Can an N>0 arm change a channel outcome when one-particle marginals are exactly matched against N=0 controls?
```

## Design

Three arms are constructed from the same Bell-origin state.

```text
arm1 coherent:
  rho = |Phi+><Phi+|
  |Phi+> = (|00> + |11>) / sqrt(2)
  N > 0

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
PASS_MINIMAL_LOAD_BEARING_NEGATIVITY
```

Pattern:

```text
outcome(coherent, N>0) != outcome(dephased, N=0) == outcome(product_marginals, N=0)
```

with exact one-particle marginal matching.

This is a minimal positive result: Bell coherence/negativity can be load-bearing for a designed channel outcome after marginal differences are eliminated.

## What this does not prove

This does not yet prove that previous droplet, history-terrain, membrane, or information-matter phenomenology required negativity.

Limitations:

```text
1. minimal two-qubit channel test
2. not yet a spatial lattice/droplet transport experiment
3. contact analyzer is designed to read Bell coherence
4. next step must embed the same three-arm control discipline into lattice contact or droplet scattering
```

## Why this matters

The previous repo state had a valid quantum witness, but no causal role for it.

This file establishes the first code-backed causal pattern:

```text
matched marginals
N>0 vs N=0
channel outcome changes only in the N>0 arm
```

The next audit-safe target is:

```text
lattice negativity causality test:
  same marginal-matching discipline
  spatial EXCH/ZZ contact region
  dephase/product controls
  channel output or reaction probability
```
