# Information Storage Reservoir

Date: 2026-07-07

Purpose: add a non-membrane information-material part: a storage reservoir. The goal is not self-regulation or life-like behavior, but a physical-style component that can store product P, leak/release it, smooth pulses, overflow, and write weak downstream terrain.

## Current framing

The membrane component is an entrance/boundary. The reservoir component is an internal-state holder.

```text
membrane:
  separates and filters

reservoir:
  stores, delays, leaks, releases, overflows
```

This experiment treats the reservoir as a scalar stochastic P-store with:

```text
capacity C
input flux P_in
retention / passive leak
controlled release
overflow when full
released P writing weak road terrain
```

This is a phenomenological component test, not a quantum witness and not a biological claim.

## Metrics

```text
S_mean: mean stored P after burn-in
S_max: maximum stored P
fill_fraction: S_mean / capacity
release_flux: mean P released per step
overflow_flux: mean P lost by overflow per step
overflow_fraction: total overflow / total input
road_mean: downstream terrain written by released P
future_A_arrival: arrival rate biased by downstream terrain
input_cv: coefficient of variation of input
release_cv: coefficient of variation of output
smoothing_ratio: release_cv / input_cv
```

Lower `smoothing_ratio` means stronger buffering/smoothing.

## Sweep 1: capacity / overflow curve

Fixed input and release settings; vary reservoir capacity.

| capacity | S_mean | fill_fraction | release_flux | overflow_flux | overflow_fraction | late_slope |
|---:|---:|---:|---:|---:|---:|---:|
| 25 | 24.64 | 0.985 | 0.257 | 1.700 | 0.844 | 0.0001 |
| 50 | 49.21 | 0.984 | 0.513 | 1.412 | 0.693 | 0.0003 |
| 75 | 73.70 | 0.983 | 0.758 | 1.141 | 0.547 | 0.0001 |
| 100 | 97.98 | 0.980 | 0.997 | 0.857 | 0.404 | 0.0005 |
| 150 | 144.51 | 0.963 | 1.464 | 0.332 | 0.144 | 0.0013 |
| 200 | 171.11 | 0.856 | 1.736 | 0.010 | 0.004 | 0.0145 |
| 300 | 171.81 | 0.573 | 1.743 | 0.000 | 0.000 | 0.0196 |

### Interpretation

The reservoir shows a clear capacity/overflow transition:

```text
capacity <= 100:
  reservoir saturates and loses much input by overflow

capacity around 150:
  still nearly full, but overflow strongly decreases

capacity >= 200:
  overflow almost disappears under this input/release setting
```

Best phrase:

```text
finite-capacity storage with overflow threshold
```

not:

```text
homeostatic storage
```

## Sweep 2: retention / release curve

Fixed high capacity; vary controlled release rate.

| release rate | S_mean | fill_fraction | release_flux | release_fraction | road_mean | future_A_arrival | late_slope |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.002 | 298.21 | 0.994 | 0.611 | 0.280 | 3.33 | 1.04 | 0.0003 |
| 0.005 | 285.12 | 0.950 | 1.448 | 0.653 | 7.83 | 2.16 | 0.0008 |
| 0.010 | 171.75 | 0.572 | 1.728 | 0.808 | 9.52 | 2.58 | 0.0028 |
| 0.020 | 91.82 | 0.306 | 1.870 | 0.895 | 10.48 | 2.82 | 0.0006 |
| 0.040 | 46.92 | 0.156 | 1.945 | 0.946 | 10.99 | 2.95 | 0.0058 |
| 0.080 | 22.90 | 0.076 | 1.982 | 0.974 | 11.25 | 3.01 | 0.0022 |
| 0.120 | 14.72 | 0.049 | 1.994 | 0.983 | 11.33 | 3.02 | 0.0010 |

### Interpretation

The reservoir has a tunable storage/export axis:

```text
low release:
  high stored P, weak downstream effect

medium release:
  stores a meaningful stock while releasing substantial flux

high release:
  low stored P, high road-writing output
```

This confirms a reservoir-specific material axis distinct from membrane selectivity:

```text
storage stock vs downstream supply
```

## Sweep 3: pulse smoothing / buffer behavior

Input alternates between high and low phases. Measure whether the reservoir smooths output.

| condition | input_flux | release_flux | S_mean | input_cv | release_cv | smoothing_ratio | overflow_flux |
|---|---:|---:|---:|---:|---:|---:|---:|
| C50_r0.01 | 2.453 | 0.416 | 41.11 | 1.169 | 1.555 | 1.331 | 1.999 |
| C100_r0.01 | 2.458 | 0.781 | 76.95 | 1.171 | 1.166 | 0.996 | 1.629 |
| C200_r0.01 | 2.456 | 1.454 | 144.67 | 1.171 | 0.893 | 0.762 | 0.933 |
| C300_r0.01 | 2.450 | 2.046 | 202.05 | 1.177 | 0.784 | 0.666 | 0.290 |
| C200_r0.005 | 2.462 | 0.840 | 167.51 | 1.171 | 1.101 | 0.940 | 1.469 |
| C200_r0.02 | 2.450 | 2.292 | 112.76 | 1.172 | 0.854 | 0.729 | 0.146 |

### Interpretation

The reservoir can act as a buffer, but only when capacity and release are in the right range.

```text
small capacity:
  saturates and overflows; output can be noisier than input

larger capacity:
  lower output CV; pulse smoothing appears

high enough release:
  reduces overflow while still smoothing output
```

Best phrase:

```text
pulse-buffering reservoir
```

not:

```text
active regulation
```

## Sweep 4: burst absorption / overflow response

Apply a transient high-input burst and measure storage/overflow/output.

| condition | S_max | S_mean | release_flux | overflow_flux | overflow_fraction | release_cv | road_mean | future_A_arrival |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C50_r0.01 | 50.00 | 42.49 | 0.425 | 0.152 | 0.541 | 1.524 | 1.60 | 0.60 |
| C100_r0.01 | 99.95 | 50.13 | 0.501 | 0.121 | 0.463 | 1.429 | 1.98 | 0.69 |
| C200_r0.01 | 199.55 | 59.34 | 0.595 | 0.112 | 0.346 | 1.400 | 2.50 | 0.82 |
| C300_r0.01 | 298.85 | 69.81 | 0.699 | 0.097 | 0.233 | 1.415 | 3.03 | 0.97 |
| C200_r0.005 | 199.95 | 100.30 | 0.499 | 0.117 | 0.396 | 1.450 | 1.95 | 0.68 |
| C200_r0.02 | 198.40 | 33.21 | 0.675 | 0.089 | 0.257 | 1.506 | 3.14 | 0.99 |

### Interpretation

The burst test separates capacity from release:

```text
larger capacity:
  absorbs more of the burst and reduces overflow fraction

higher release:
  lowers stored stock and increases downstream terrain output

lower release:
  stores more but exports less
```

This is a reservoir behavior, not a membrane behavior.

## Current component profile

The information storage reservoir has these properties:

```text
storage capacity:
  finite and measurable

overflow threshold:
  present

retention/release axis:
  tunable

pulse buffering:
  present when capacity is large enough

burst absorption:
  present but capacity-limited

downstream terrain writing:
  present through released P

future arrival bias:
  weak but measurable through road terrain
```

## Current best statement

```text
The information storage reservoir is a non-membrane information-material component.
It stores P, delays output, smooths input pulses, overflows when saturated, and releases P to write downstream terrain.
It is not a self-regulating store; it is a passive/parameterized reservoir with measurable material properties.
```

## Component table update

```text
membrane:
  filters and separates

reservoir:
  stores and delays

road:
  transports and biases future arrival

converter:
  changes species/product type

buffer:
  smooths flux and stress
```

The next useful non-membrane component after reservoir is probably:

```text
source-sink pair:
  maintains non-equilibrium supply and removal

or

converter:
  turns stored P into Q/R with different terrain effect
```
