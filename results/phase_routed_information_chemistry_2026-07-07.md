# Phase-routed Information Chemistry

Date: 2026-07-07

Purpose: keep the classical material behavior as the baseline, then test whether phase/coherence acts as an extra control layer over reaction-channel choice.

## Core idea

The previous information-chemistry core showed that rejection, absorption, surface adsorption, toxicity, and bridging can be generated mostly by compatibility/loss rules. That is not a failure: it is the classical effective material layer.

The next question is narrower:

```text
When several reaction channels remain open,
does relative phase change which channel wins?
```

## Minimal experiment

2D 6x5 lattice, ordered hard-core A/B/C particles.

- A+B start as an AB dimer near the center.
- C approaches from the left through two branches: upper and lower wavepackets.
- Relative phase delta between the upper/lower C branches is varied.
- Channels:
  - fusion: AB intact and C in direct contact
  - shell: AB intact and C at distance 2, surface adsorption-like
  - reject/bypass: AB intact and C not in contact or shell
  - AB broken
- Classical control: incoherent probability mixture of the same upper/lower packets.

Selection is intentionally weak/moderate so the outcome is not forced into a single compatibility channel.

## Results

| C branch phase delta | fusion | shell | reject | AB broken | P_ABC | C contact | sep C-AB | IPR | S2(C:AB) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.308 | 0.227 | 0.333 | 0.132 | 0.324 | 0.361 | 2.917 | 231.7 | 2.083 |
| pi/2 | 0.249 | 0.215 | 0.388 | 0.148 | 0.264 | 0.303 | 3.173 | 345.6 | 2.407 |
| pi | 0.122 | 0.183 | 0.512 | 0.183 | 0.132 | 0.177 | 3.756 | 554.7 | 2.918 |
| 3pi/2 | 0.254 | 0.213 | 0.386 | 0.147 | 0.269 | 0.308 | 3.170 | 325.7 | 2.385 |
| classical incoherent mixture | 0.307 | 0.310 | 0.168 | 0.214 | 0.318 | 0.380 | 2.484 | 86.1 | n/a |

## Main finding

The classical material layer remains. It can form contact/shell/rejection channels using compatibility and loss.

But relative phase strongly changed the channel balance:

```text
delta = 0:
  fusion/contact remains high.

delta = pi:
  fusion/contact is suppressed.
  reject/bypass rises.
  C-AB separation increases.
  IPR rises.
  C:AB Renyi-2 entanglement rises.
```

The phase swing was large:

```text
fusion: 0.308 -> 0.122
P_ABC:  0.324 -> 0.132
reject: 0.333 -> 0.512
IPR:    231.7 -> 554.7
S2:     2.083 -> 2.918
```

## Interpretation

This is the right framing:

```text
Classical layer:
  compatibility/loss creates possible material reaction channels.

Quantum/wave layer:
  relative phase biases which open channel the system enters.
```

This is not yet proof of quantum-only chemistry, because a classical complex wave can also produce phase interference. However, it is a meaningful step beyond classical probability selection:

```text
same compatibility table
same loss rules
same initial probability support
only relative phase changed
reaction-channel weights changed
```

## Best current statement

The pseudo-material itself can be mostly classical-effective. The quantum-like ingredient is a control layer over channel selection:

```text
phase as reaction-channel selector
```

## Next checks

- Add a classical complex-wave control, not just classical probability.
- Add dephase-after-each-step control to kill phase while keeping probabilities.
- Test whether channel selection correlates with negativity or only with wave interference.
- Move from C-only branch interference to interacting two-droplet phase routing.
