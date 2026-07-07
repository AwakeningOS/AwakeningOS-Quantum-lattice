# Converter Core

Date: 2026-07-07

Status: `RAW_LOG_BACKED`

Generator script:

```text
scripts/phenomenology/converter_core.py
```

Raw log:

```text
data/converter/converter_core_seed8128.json
```

Run command:

```bash
python scripts/phenomenology/converter_core.py --seed 8128 --out data/converter/converter_core_seed8128.json
```

## Purpose

The converter is the first information-material component whose job is not access, quantity, or timing, but identity/meaning change.

```text
membrane     : location/access
source-sink  : quantity
reservoir    : timing
converter    : identity/meaning
```

This is a classical stochastic phenomenology model, not a quantum witness.

## Modes

The committed generator implements four modes:

```text
linear_control:
  historyless baseline

threshold:
  conversion turns on sharply above an A-stock threshold

bistable:
  internal mode switches by hysteresis thresholds, changing P/Q branch behavior

inhibition:
  end-product P inhibits further A->P conversion
```

## Sweep 1: conversion-throughput

Input flux was swept across three modes.

| mode | input | conv_eff | conv_flux | activity | P_flux |
|---|---|---|---|---|---|
| linear_control | 0.500 | 0.787 | 0.382 | 0.255 | 0.378 |
| linear_control | 2.000 | 0.896 | 1.838 | 0.454 | 1.808 |
| linear_control | 4.000 | 0.913 | 3.477 | 0.569 | 3.412 |
| linear_control | 10.000 | 0.931 | 9.317 | 0.736 | 9.131 |
| threshold | 0.500 | 0.529 | 0.291 | 0.065 | 0.285 |
| threshold | 2.000 | 0.851 | 1.678 | 0.293 | 1.651 |
| threshold | 4.000 | 0.898 | 3.517 | 0.512 | 3.448 |
| threshold | 10.000 | 0.931 | 9.580 | 0.739 | 9.365 |
| inhibition | 0.500 | 0.832 | 0.372 | 0.236 | 0.365 |
| inhibition | 2.000 | 0.890 | 1.825 | 0.466 | 1.789 |
| inhibition | 4.000 | 0.914 | 3.738 | 0.576 | 3.678 |
| inhibition | 10.000 | 0.930 | 9.486 | 0.735 | 9.303 |

### Interpretation

The converter has a throughput curve and the threshold mode is visibly nonlinear at low input:

```text
threshold mode at input 0.5:
  conversion_efficiency = 0.529

threshold mode at input 4.0:
  conversion_efficiency = 0.898
```

The threshold converter is therefore not merely a constant rate placeholder. It behaves like an input-dependent identity-transform component.

## Sweep 2: fidelity-promiscuity

Off-target probability was swept to measure meaning drift into Pprime.

| off_target | fidelity_P | promiscuity_Pprime | Pprime_flux |
|---|---|---|---|
| 0.000 | 1.000 | 0.000 | 0.000 |
| 0.005 | 0.992 | 0.008 | 0.029 |
| 0.010 | 0.989 | 0.011 | 0.040 |
| 0.020 | 0.982 | 0.018 | 0.065 |
| 0.050 | 0.947 | 0.053 | 0.189 |
| 0.100 | 0.903 | 0.097 | 0.351 |
| 0.200 | 0.796 | 0.204 | 0.737 |

### Interpretation

This is the converter-specific axis.

```text
off_target 0.000:
  fidelity_P = 1.000
  promiscuity = 0.000

off_target 0.200:
  fidelity_P = 0.796
  promiscuity = 0.204
```

The converter can be evaluated as a meaning-preserving or meaning-drifting transform.

## Sweep 3: gating / conditional response

Gate value controls whether converted material becomes P or Q.

| gate | P_flux | Q_flux | P_fraction | Q_fraction | P/Q |
|---|---|---|---|---|---|
| 0.000 | 0.000 | 3.515 | 0.000 | 0.977 | 0.000 |
| 0.100 | 0.349 | 3.238 | 0.096 | 0.889 | 0.108 |
| 0.250 | 0.960 | 2.617 | 0.263 | 0.717 | 0.367 |
| 0.500 | 1.832 | 1.738 | 0.502 | 0.477 | 1.054 |
| 0.750 | 2.720 | 0.855 | 0.742 | 0.233 | 3.180 |
| 0.900 | 3.109 | 0.329 | 0.887 | 0.094 | 9.444 |
| 1.000 | 3.594 | 0.000 | 0.978 | 0.000 | 0.000 |

### Interpretation

The gate cleanly moves output identity between Q and P.

```text
gate = 0.0:
  P_flux = 0.000
  Q_flux = 3.515

gate = 0.5:
  P_flux = 1.832
  Q_flux = 1.738

gate = 1.0:
  P_flux = 3.594
  Q_flux = 0.000
```

This is the first component axis that directly changes output meaning.

## Forward-compatible phase gate hook

The script includes a classical-effective phase-gate hook:

```text
gate_effective = cos(phi / 2)^2
```

This is not a quantum claim. It is only a future interface so the same converter can later be tested with coherence / negativity controls.

| phi | gate_eff | P_flux | Q_flux | P_fraction | Q_fraction |
|---|---|---|---|---|---|
| 0.000 | 1.000 | 3.586 | 0.000 | 0.983 | 0.000 |
| 0.785 | 0.854 | 2.925 | 0.520 | 0.833 | 0.148 |
| 1.571 | 0.500 | 1.815 | 1.918 | 0.478 | 0.505 |
| 2.356 | 0.146 | 0.508 | 3.031 | 0.141 | 0.839 |
| 3.142 | 0.000 | 0.000 | 3.446 | 0.000 | 0.977 |

## Sweep 4: stability / poisoning

D-like stress and product inhibition reduce throughput and increase off-target drift.

| stress_D | conv_eff | conv_flux | fidelity_P | promiscuity | A_mean |
|---|---|---|---|---|---|
| 0.000 | 0.822 | 3.334 | 0.978 | 0.022 | 65.414 |
| 0.050 | 0.807 | 3.178 | 0.981 | 0.019 | 60.666 |
| 0.100 | 0.790 | 3.214 | 0.975 | 0.025 | 66.675 |
| 0.200 | 0.732 | 2.914 | 0.960 | 0.040 | 61.991 |
| 0.350 | 0.662 | 2.629 | 0.951 | 0.049 | 58.858 |
| 0.500 | 0.574 | 2.294 | 0.946 | 0.054 | 56.108 |
| 0.750 | 0.399 | 1.562 | 0.902 | 0.098 | 47.042 |
| 1.000 | 0.210 | 0.837 | 0.825 | 0.175 | 36.531 |

### Interpretation

The converter has a poisoning/stability curve.

```text
stress 0.00:
  conversion_efficiency = 0.822
  fidelity_P = 0.978

stress 1.00:
  conversion_efficiency = 0.210
  fidelity_P = 0.825
  promiscuity = 0.175
```

Under stress, the converter does not simply slow down; it also becomes less faithful.

## Sweep 5: bistable hysteresis

The bistable mode has an internal state that changes the P/Q output branch.

| dir | input | mode_state | P_flux | Q_flux | Q_fraction |
|---|---|---|---|---|---|
| up | 0.500 | 0.000 | 0.237 | 0.045 | 0.157 |
| up | 1.000 | 0.000 | 0.585 | 0.097 | 0.140 |
| up | 2.000 | 0.515 | 0.517 | 1.160 | 0.679 |
| up | 4.000 | 1.000 | 0.502 | 3.108 | 0.843 |
| up | 7.000 | 1.000 | 0.957 | 5.200 | 0.826 |
| up | 10.000 | 1.000 | 1.379 | 7.725 | 0.833 |
| down | 10.000 | 1.000 | 1.408 | 7.732 | 0.830 |
| down | 7.000 | 1.000 | 0.989 | 5.345 | 0.831 |
| down | 4.000 | 1.000 | 0.614 | 3.085 | 0.818 |
| down | 2.000 | 0.528 | 0.523 | 1.222 | 0.692 |
| down | 1.000 | 0.000 | 0.568 | 0.106 | 0.155 |
| down | 0.500 | 0.000 | 0.285 | 0.038 | 0.117 |

### Interpretation

The bistable converter acts like a history-dependent meaning switch.

```text
low mode:
  mostly P

high mode:
  mostly Q
```

This is the first committed converter mode with explicit internal state.

## Current component statement

```text
The converter is a code-backed classical phenomenology component that changes identity/meaning.
It has measurable throughput, fidelity/promiscuity, conditional branching, poisoning, and bistable hysteresis axes.
```

## What this does not claim

```text
not quantum
not metabolism
not self-regulation
not a living component
not evidence that negativity is load-bearing in information matter
```

## Next step

The next component-level target is to compose:

```text
source -> converter -> reservoir -> sink
```

using only code-backed components and raw logs.
