# Source-Sink Pair Component

Date: 2026-07-07

Purpose: add another non-membrane information-material part: a source-sink pair. The goal is to create and characterize a non-equilibrium supply/removal component that can feed reservoirs, membranes, roads, and converters.

## Framing

The reservoir stores and delays. The source-sink pair maintains flow.

```text
source:
  injects substrate A into the system

converter:
  turns A into product P

sink:
  removes P so the system does not simply saturate
```

This component is not self-regulation, metabolism, or life-like behavior. It is a passive/parameterized non-equilibrium driver.

## Minimal model

A stochastic queue-like model was used:

```text
A source -> delayed road/channel -> A stock -> converter A->P -> P stock -> P sink
```

Tracked quantities:

```text
input_flux
conversion_flux
sink_flux
A_mean
P_mean
stock_mean
overflow_flux
throughput_efficiency
sink_balance = P_removed / P_created
late_stock_slope
source_cv
sink_cv
smoothing_ratio
```

Lower smoothing_ratio means the sink/output is smoother than the source/input.

## Sweep 1: sink-capacity curve

Source rate fixed near 2.0. Converter strength fixed. Sink capacity varied.

| sink capacity | input flux | conversion flux | sink flux | P_mean | stock_mean | sink balance | throughput efficiency | overflow flux |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 2.019 | 0.744 | 0.495 | 248.73 | 249.33 | 0.665 | 0.245 | 1.264 |
| 1.0 | 2.003 | 1.245 | 0.998 | 247.21 | 248.32 | 0.801 | 0.498 | 0.748 |
| 1.5 | 2.006 | 1.732 | 1.486 | 243.27 | 244.91 | 0.858 | 0.741 | 0.264 |
| 2.0 | 2.008 | 1.996 | 1.953 | 41.42 | 43.59 | 0.979 | 0.973 | 0.000 |
| 3.0 | 2.007 | 1.995 | 1.993 | 1.83 | 4.03 | 0.999 | 0.993 | 0.000 |
| 4.0 | 2.006 | 1.994 | 1.993 | 0.96 | 3.17 | 0.999 | 0.994 | 0.000 |
| 6.0 | 2.002 | 1.989 | 1.988 | 0.61 | 2.81 | 1.000 | 0.993 | 0.000 |

### Interpretation

The source-sink pair has a clear sink-capacity transition.

```text
sink capacity < source/conversion flux:
  P accumulates near capacity
  overflow appears
  throughput is low

sink capacity around source flux:
  backlog falls sharply
  overflow disappears
  throughput becomes high

sink capacity well above source flux:
  P stock remains low
  sink follows production closely
```

Best phrase:

```text
non-equilibrium flow maintained by matched source and sink capacity
```

not:

```text
metabolism
```

## Sweep 2: source-loading curve

Sink capacity fixed at 2.5. Source rate varied.

| source rate | input flux | conversion flux | sink flux | A_mean | P_mean | stock_mean | throughput efficiency | overflow flux |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.508 | 0.504 | 0.504 | 0.61 | 0.26 | 0.87 | 0.993 | 0.000 |
| 1.0 | 1.013 | 1.008 | 1.007 | 1.13 | 0.63 | 1.76 | 0.994 | 0.000 |
| 1.5 | 1.502 | 1.492 | 1.491 | 1.67 | 1.41 | 3.07 | 0.993 | 0.000 |
| 2.0 | 2.000 | 1.988 | 1.985 | 2.21 | 3.76 | 5.97 | 0.993 | 0.000 |
| 3.0 | 3.007 | 2.717 | 2.475 | 2.77 | 237.75 | 240.51 | 0.823 | 0.274 |
| 4.0 | 4.015 | 2.730 | 2.487 | 2.80 | 243.65 | 246.45 | 0.620 | 1.263 |
| 6.0 | 6.011 | 2.743 | 2.498 | 2.77 | 244.46 | 247.23 | 0.416 | 3.236 |

### Interpretation

The source-sink pair has a loading threshold.

```text
source rate <= 2.0:
  near-steady non-equilibrium flow
  high throughput
  low stock
  no overflow

source rate >= 3.0:
  converter/sink cannot absorb supply
  P stock saturates
  overflow appears
  throughput efficiency falls
```

This gives a useful design rule:

```text
source flux must be matched to converter + sink capacity.
```

## Sweep 3: pulsed source smoothing

A pulsed source alternates between high and low phases. Sink capacity varied.

| sink capacity | input flux | sink flux | P_mean | source CV | sink CV | smoothing ratio | overflow flux | throughput efficiency |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 1.841 | 0.996 | 286.98 | 1.104 | 0.997 | 0.904 | 0.573 | 0.541 |
| 1.5 | 1.835 | 1.497 | 251.62 | 1.103 | 0.818 | 0.743 | 0.089 | 0.816 |
| 2.0 | 1.837 | 1.826 | 33.34 | 1.110 | 0.784 | 0.707 | 0.000 | 0.994 |
| 3.0 | 1.840 | 1.837 | 8.38 | 1.102 | 0.994 | 0.902 | 0.000 | 0.998 |
| 4.0 | 1.840 | 1.838 | 1.95 | 1.106 | 1.092 | 0.988 | 0.000 | 0.999 |

### Interpretation

Pulsed input exposes three regimes:

```text
underpowered sink:
  smooths output but loses throughput and accumulates P

matched sink around capacity 2.0:
  high throughput, zero overflow, and strongest smoothing

overpowered sink:
  low storage and high throughput, but output follows input more closely
```

Best phrase:

```text
matched source-sink buffering
```

not:

```text
active regulation
```

## Sweep 4: sink specificity / substrate drain

Sink should remove P without draining useful substrate A. A-leak into sink was varied.

| A leak probability | input flux | conversion flux | sink flux | A leak flux | conversion efficiency | throughput efficiency | A_mean | P_mean |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | 2.000 | 1.988 | 1.985 | 0.000 | 0.994 | 0.993 | 2.21 | 3.76 |
| 0.005 | 2.006 | 1.982 | 1.978 | 0.013 | 0.988 | 0.986 | 2.12 | 3.79 |
| 0.010 | 2.005 | 1.971 | 1.966 | 0.022 | 0.983 | 0.981 | 2.11 | 3.56 |
| 0.020 | 2.010 | 1.954 | 1.950 | 0.044 | 0.972 | 0.970 | 2.09 | 3.44 |
| 0.050 | 2.007 | 1.892 | 1.890 | 0.102 | 0.943 | 0.942 | 1.95 | 2.91 |
| 0.100 | 2.011 | 1.806 | 1.803 | 0.193 | 0.898 | 0.897 | 1.78 | 2.52 |

### Interpretation

Sink specificity is a real component property.

```text
selective P sink:
  preserves A for conversion
  high conversion efficiency

leaky sink:
  drains A before conversion
  reduces conversion and throughput
```

This makes the sink more than a deletion operation. It has selectivity and side effects.

## Current component profile

The source-sink pair has these material properties:

```text
supply flux:
  tunable by source rate

removal capacity:
  tunable by sink capacity

loading threshold:
  appears when source exceeds converter/sink capacity

backlog/stock:
  increases sharply under sink/source mismatch

pulse buffering:
  strongest at matched sink capacity

sink specificity:
  needed to avoid draining substrate A

non-equilibrium maintenance:
  present when source, converter, and sink are balanced
```

## Current best statement

```text
The source-sink pair is a non-membrane information-material component that maintains directed non-equilibrium flow.
It supplies substrate, removes product, prevents simple saturation when matched, and creates controlled backlog/overflow when mismatched.
It is not metabolism or self-regulation; it is a passive flow-driving component with measurable material parameters.
```

## Component table update

```text
membrane:
  filters and separates

reservoir:
  stores, delays, leaks, releases, overflows

source-sink pair:
  drives non-equilibrium supply/removal

road:
  transports and biases future arrival

converter:
  changes species/product type

buffer:
  smooths flux and stress
```

## What this enables next

The next useful composed systems are:

```text
source -> membrane -> converter -> reservoir -> sink

source -> road -> membrane -> reservoir

source -> converter -> reservoir -> road export
```

But before composition, the next single component worth characterizing is probably:

```text
converter:
  A -> P
  P -> Q
  C+D -> R
  with product-specific terrain effects
```

The source-sink pair makes converters meaningful because it supplies input and removes output, preventing trivial saturation.
