# Catalytic Compartment Membrane Characterization

Date: 2026-07-07

Purpose: characterize the current shell object as a catalytic selective-permeability membrane, not as a self-repairing/dividing/self-regulating system.

## Framing

The correct current object is:

```text
catalytic compartment membrane
```

The experiment measures physical-style properties:

```text
permeability
selectivity
retention
conversion
product accumulation
product release
membrane integrity
stress response
external terrain influence
```

This is a phenomenological stochastic membrane model. It is intended as a characterization core, not a claim of life-like behavior.

## Stage 1: passive membrane permeability

No catalyst. No product P. Measure only membrane crossing and selectivity.

| condition | P_in(A) | P_in(B) | P_in(C) | P_in(D) | A/B selectivity | integrity |
|---|---:|---:|---:|---:|---:|---:|
| thin_open | 0.441 | 0.340 | 0.233 | 0.111 | 1.30 | 1.00 |
| selective_base | 0.153 | 0.009 | 0.053 | 0.024 | 17.45 | 1.00 |
| thick_selective | 0.096 | 0.005 | 0.032 | 0.015 | 18.16 | 1.00 |
| low_pore_selective | 0.077 | 0.004 | 0.026 | 0.013 | 17.73 | 1.00 |
| high_pore_selective | 0.308 | 0.018 | 0.106 | 0.048 | 17.20 | 1.00 |
| weak_B_exclusion | 0.153 | 0.078 | 0.053 | 0.025 | 1.96 | 1.00 |

### Interpretation

The passive membrane has a clear permeability/selectivity tradeoff.

```text
open/thin membrane:
  high throughput, low selectivity

selective membrane:
  lower A throughput, strong A/B separation

higher pore density:
  restores throughput while preserving selectivity if B exclusion remains strong

weak B exclusion:
  selectivity collapses
```

This confirms that the shell can be characterized as a selective-permeability object.

## Stage 2: catalytic conversion A -> P

Turn on internal catalyst X. Measure conversion, accumulation, retention, and release.

| condition | P_in(A) | A/B selectivity | A->P conversion | P_inside_mean | retention_P | P release flux | P release fraction |
|---|---:|---:|---:|---:|---:|---:|---:|
| no_catalyst | 0.153 | 16.53 | 0.000 | 0.0 | 0.0 | 0.000 | 0.000 |
| weak_catalyst | 0.153 | 16.75 | 0.612 | 152.6 | 109.6 | 0.793 | 0.469 |
| medium_catalyst | 0.155 | 17.70 | 0.753 | 185.1 | 108.7 | 0.958 | 0.468 |
| strong_catalyst | 0.155 | 17.02 | 0.861 | 209.4 | 108.6 | 1.082 | 0.469 |

### Interpretation

Internal catalyst strength primarily controls conversion and P accumulation:

```text
X strength 0.25 -> conversion 0.612
X strength 0.50 -> conversion 0.753
X strength 1.00 -> conversion 0.861
```

The membrane permeability itself remains stable across catalyst settings. This means the current object separates two roles:

```text
membrane:
  controls input selectivity

internal catalyst:
  controls conversion and accumulation
```

## Stage 3: product retention, release, and external terrain influence

Allow P to leave the compartment and write weak external terrain.

| condition | A->P conversion | P_inside_mean | retention_P | P release flux | P release fraction | P export events | external P terrain | future A arrival near P terrain |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| high_retention_low_release | 0.762 | 319.1 | 198.4 | 0.324 | 0.148 | 259.1 | 36.4 | 0.336 |
| balanced_release | 0.763 | 235.1 | 108.9 | 1.215 | 0.471 | 972.1 | 135.8 | 1.283 |
| low_retention_high_release | 0.761 | 141.7 | 51.9 | 2.153 | 0.727 | 1722.8 | 223.9 | 2.192 |

### Interpretation

The retention/release axis behaves cleanly:

```text
high retention:
  P accumulates strongly inside but weakly affects outside

balanced release:
  moderate P accumulation and moderate terrain writing

high release:
  lower P stock, stronger export and stronger external terrain influence
```

This is a real material-style tradeoff:

```text
storage vs export
```

The external effect is still modest, but measurable.

## Stage 4: D stress response

D is treated as membrane stress, not as a normal substrate.

| condition | integrity final | integrity min | integrity drop | breach count | breach duration mean | D contact rate | empirical D damage | P_in(A) | P_in(D) | A->P conversion | P_inside_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| no_D_stress | 1.000 | 1.000 | 0.000 | 0.00 | 0.0 | 0.0 | 0.000 | 0.154 | 0.025 | 0.760 | 192.9 |
| very_mild_D | 1.000 | 0.992 | 0.000 | 0.00 | 0.0 | 20.2 | 0.029 | 0.155 | 0.025 | 0.761 | 195.0 |
| mild_D | 0.998 | 0.979 | 0.002 | 0.00 | 0.0 | 20.2 | 0.057 | 0.153 | 0.025 | 0.764 | 191.8 |
| moderate_D | 0.429 | 0.378 | 0.571 | 3.75 | 162.7 | 20.7 | 0.094 | 0.109 | 0.018 | 0.774 | 187.0 |
| moderate_D_high_C | 0.997 | 0.967 | 0.003 | 0.00 | 0.0 | 20.1 | 0.114 | 0.154 | 0.025 | 0.764 | 191.0 |

### Interpretation

There is a stress threshold.

```text
very mild / mild D:
  membrane integrity remains high
  permeability is mostly preserved

moderate D:
  integrity collapses to 0.429
  breaches persist
  P_in(A) drops from ~0.154 to 0.109

moderate D with higher C permeability:
  integrity remains near 0.997
```

This supports the interpretation of C as a repair/stabilizing material in the membrane characterization model.

Important wording:

```text
stress response and stabilizing C permeability
```

not yet:

```text
self-repair
```

## Current material profile

The characterized membrane has these properties:

```text
selective permeability:
  present

A/B selectivity:
  strong when B exclusion is high

A throughput:
  tunable by pore density and shell thickness

internal catalytic conversion:
  present and controlled by X strength

P accumulation:
  present and controlled by retention/release setting

P release:
  present and tunable

external terrain influence:
  weak but measurable

D stress response:
  threshold-like; C permeability can stabilize the shell

long-time integrity:
  good under no/mild stress; not robust under moderate D unless C stabilization is enabled
```

## Best current statement

```text
The current virtual object is a catalytic selective-permeability information membrane.
It can filter input, sustain an internal catalytic reaction field, accumulate product, release product, and respond to stress.
It is not yet a self-regulating, self-repairing, or dividing compartment.
```

## Next measurement target

Before escalating to self-regulation, the next useful characterization is a denser parameter map:

```text
selectivity-throughput curve:
  A throughput vs A/B selectivity

retention-release curve:
  P_inside_mean vs release_flux_P

stress-stability curve:
  D_damage_rate vs integrity_final

C-stabilization curve:
  C_permeability vs integrity under D stress
```

This would turn the current toy into a material-property map rather than a story of high-level behavior.
