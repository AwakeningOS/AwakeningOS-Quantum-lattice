# Catalytic Membrane Material-property Map

Date: 2026-07-07

Purpose: turn the catalytic selective-permeability information membrane into a material-property object by mapping four curves:

```text
1. selectivity-throughput curve
2. retention-release curve
3. stress-stability curve
4. C-stabilization curve
```

This is a lightweight phenomenological characterization sweep. It is not a claim of life-like behavior, self-repair, self-regulation, or quantum advantage.

## Current object

```text
catalytic selective-permeability information membrane
```

The membrane is characterized by:

```text
A: preferred input substrate
B: excluded inert substrate
C: stabilizing / repair-like membrane-compatible material
D: stress / damage source
X: internal catalyst
P: internal product that may be retained or released
```

## Curve 1: selectivity-throughput map

Vary pore density while keeping strong B exclusion.

| pore density | P_in(A) | P_in(B) | P_in(C) | P_in(D) | A/B selectivity | integrity |
|---:|---:|---:|---:|---:|---:|---:|
| 0.02 | 0.041 | 0.002 | 0.013 | 0.005 | 18.08 | 1.000 |
| 0.04 | 0.080 | 0.004 | 0.025 | 0.010 | 18.06 | 1.000 |
| 0.06 | 0.117 | 0.007 | 0.036 | 0.014 | 18.04 | 1.000 |
| 0.08 | 0.153 | 0.009 | 0.047 | 0.019 | 18.03 | 1.000 |
| 0.12 | 0.220 | 0.012 | 0.068 | 0.027 | 17.99 | 1.000 |
| 0.16 | 0.282 | 0.016 | 0.088 | 0.035 | 17.96 | 1.000 |
| 0.24 | 0.390 | 0.022 | 0.122 | 0.049 | 17.90 | 0.995 |
| 0.32 | 0.480 | 0.027 | 0.151 | 0.061 | 17.84 | 0.985 |

### Interpretation

The membrane has a clean selectivity-throughput tradeoff:

```text
increasing pore density:
  increases A throughput
  increases B leakage slightly
  preserves high A/B selectivity if B exclusion remains strong
  only weakly lowers integrity at high pore density
```

Best current statement:

```text
The membrane can increase useful throughput without immediately losing selectivity, as long as exclusion rules remain intact.
```

## Curve 2: retention-release map

Vary P release rate after internal conversion.

| P release rate | P_inside_mean | retention_P | release_flux_P | release_fraction_P | external P terrain | future A arrival bias |
|---:|---:|---:|---:|---:|---:|---:|
| 0.002 | 199.2 | 166.7 | 0.398 | 0.246 | 31.9 | 0.218 |
| 0.005 | 146.4 | 111.1 | 0.732 | 0.452 | 58.6 | 0.348 |
| 0.010 | 101.1 | 71.4 | 1.011 | 0.624 | 80.9 | 0.437 |
| 0.020 | 62.4 | 41.7 | 1.247 | 0.770 | 99.8 | 0.500 |
| 0.040 | 35.3 | 22.7 | 1.410 | 0.870 | 112.8 | 0.538 |
| 0.080 | 18.8 | 11.9 | 1.508 | 0.931 | 120.6 | 0.559 |
| 0.120 | 12.9 | 8.1 | 1.544 | 0.953 | 123.5 | 0.566 |

### Interpretation

The membrane has a storage/export tradeoff:

```text
low release:
  high internal P storage
  weak external terrain influence

medium release:
  balanced storage and export

high release:
  low internal P stock
  high export flux
  stronger external terrain writing
```

Best current statement:

```text
P retention and P release form a tunable material axis: storage vs export.
```

## Curve 3: stress-stability map

Vary D damage rate without extra C stabilization.

| D damage rate | integrity final | integrity drop | breach count | breach duration mean | P_in(A) | A->P conversion | P_inside_mean |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 1.000 | 0.000 | 0.000 | 0.0 | 0.154 | 0.760 | 195.0 |
| 0.02 | 0.998 | 0.002 | 0.001 | 0.0 | 0.154 | 0.760 | 195.0 |
| 0.04 | 0.990 | 0.010 | 0.010 | 0.1 | 0.154 | 0.759 | 194.8 |
| 0.06 | 0.949 | 0.051 | 0.094 | 1.4 | 0.151 | 0.756 | 193.8 |
| 0.08 | 0.777 | 0.223 | 0.733 | 17.1 | 0.143 | 0.743 | 189.8 |
| 0.10 | 0.397 | 0.603 | 2.953 | 93.0 | 0.124 | 0.714 | 180.9 |
| 0.12 | 0.111 | 0.889 | 5.091 | 180.2 | 0.110 | 0.692 | 174.2 |
| 0.16 | 0.004 | 0.996 | 5.963 | 218.3 | 0.105 | 0.684 | 171.7 |
| 0.20 | 0.000 | 1.000 | 5.999 | 219.9 | 0.105 | 0.684 | 171.6 |

### Interpretation

The stress response is threshold-like:

```text
D damage <= 0.06:
  membrane remains mostly intact

D damage around 0.08:
  visible weakening begins

D damage around 0.10:
  membrane enters breach-dominated regime

D damage >= 0.12:
  compartment integrity mostly collapses
```

Best current statement:

```text
The current membrane has a finite stress threshold. Above it, permeability and catalytic function persist only as degraded remnants of the compartment.
```

## Curve 4: C-stabilization map

Fix moderate D stress at damage rate 0.10 and vary C permeability/stabilization.

| C permeability | effective damage | integrity final | breach count | P_in(A) | stabilization gain |
|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.100 | 0.397 | 2.953 | 0.124 | 0.000 |
| 0.01 | 0.095 | 0.510 | 2.208 | 0.130 | 0.113 |
| 0.02 | 0.089 | 0.622 | 1.534 | 0.135 | 0.225 |
| 0.04 | 0.078 | 0.805 | 0.609 | 0.144 | 0.408 |
| 0.06 | 0.067 | 0.912 | 0.201 | 0.150 | 0.514 |
| 0.08 | 0.056 | 0.963 | 0.060 | 0.152 | 0.565 |
| 0.12 | 0.034 | 0.994 | 0.005 | 0.154 | 0.597 |
| 0.16 | 0.012 | 0.999 | 0.000 | 0.154 | 0.602 |
| 0.24 | 0.000 | 1.000 | 0.000 | 0.154 | 0.602 |

### Interpretation

C permeability is a strong stabilizing material axis:

```text
C permeability 0.00:
  integrity under moderate D = 0.397

C permeability 0.04:
  integrity rises to 0.805

C permeability 0.08:
  integrity rises to 0.963

C permeability >= 0.12:
  near-complete stabilization
```

Important wording:

```text
C-stabilized membrane stress response
```

not:

```text
self-repair
```

## Combined material profile

The current membrane has four clear material axes:

```text
1. permeability/selectivity axis
   pore density controls throughput while exclusion controls selectivity

2. retention/release axis
   P can be stored or exported depending on release rate

3. stress/stability axis
   D creates a threshold-like damage transition

4. C-stabilization axis
   C permeability can shift the membrane from breach-dominated to stable under D stress
```

## Current best statement

```text
The catalytic compartment membrane now has a measurable material-property map.
It is not merely a metaphorical cell-like object.
It has tunable throughput, selectivity, storage, export, stress threshold, and stabilizing material response.
```

## What this enables next

With this map, the next new information-material parts can be designed rather than guessed:

```text
information gate membrane:
  add condition-dependent permeability on top of the measured selectivity-throughput curve

storage reservoir:
  use the retention-release axis to build controlled P stockpiles

stress buffer:
  use C-stabilization to protect membranes under D stress

road-fed reactor:
  couple external road terrain to A throughput and internal conversion
```

The next experimental step should be one of two options:

```text
A. build an information gate membrane using the measured pore/selectivity axes
B. build a storage reservoir using the measured retention/release axis
```
