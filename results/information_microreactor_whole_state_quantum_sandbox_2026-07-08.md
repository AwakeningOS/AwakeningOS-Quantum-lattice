# Information Microreactor Whole-State Quantum Sandbox

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `classical-effective / whole-state quantumization audit`

Generator script:

```text
scripts/phenomenology/information_microreactor_whole_state_quantum_sandbox.py
```

Raw CSV logs:

```text
data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_summary.csv
data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_events.csv
```

Run command:

```bash
python scripts/phenomenology/information_microreactor_whole_state_quantum_sandbox.py --seed 20260707 --summary-csv data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_summary.csv --events-csv data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_events.csv
```

## Question

If the whole information microreactor sandbox is coarse-grained into one finite state space and evolved as a coupled global state, does coherent whole-state evolution differ from dephased/classical finite-state evolution?

## What is quantumized

This is not a local component replacement.

The main sandbox variables are placed into one finite state:

```text
A = source/input activity
M = membrane/open integrity
C = converter/product activity
R = reservoir/fill activity
O = output/release activity
Q = quality/intact state
B = contaminant state
T = terrain/road state
D = stress/damage state
S = stabilizer/protection state
```

This is a 10-bit / 10-qubit coarse whole-state sandbox.

## Compared modes

```text
classical_finite_state:
  probability vector over 2^10 states; gates act as dephased stochastic transitions

dephased_whole_state:
  same as classical finite state; explicit dephase control

coherent_whole_state:
  complex state vector over 2^10 states; same controlled rotations and global couplings without dephase
```

## Result summary

| mode | mean output | mean quality | mean output quality | mean reservoir | mean membrane | mean terrain | final output | final quality | final terrain |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| classical_finite_state | 0.255132 | 0.625312 | 0.150476 | 0.293715 | 0.648579 | 0.269608 | 0.398474 | 0.514829 | 0.414490 |
| dephased_whole_state | 0.255132 | 0.625312 | 0.150476 | 0.293715 | 0.648579 | 0.269608 | 0.398474 | 0.514829 | 0.414490 |
| coherent_whole_state | 0.494194 | 0.484017 | 0.239350 | 0.478655 | 0.491800 | 0.480830 | 0.472929 | 0.470247 | 0.508345 |

## Event comparison

| mode | event | time | value |
|---|---|---:|---:|
| classical_finite_state | quality_below_0.7 | 76 | 0.697453 |
| classical_finite_state | quality_below_0.5 |  |  |
| classical_finite_state | reservoir_above_0.5 |  |  |
| classical_finite_state | membrane_below_0.5 |  |  |
| classical_finite_state | terrain_above_0.5 |  |  |
| classical_finite_state | output_above_0.5 |  |  |
| dephased_whole_state | quality_below_0.7 | 76 | 0.697453 |
| dephased_whole_state | quality_below_0.5 |  |  |
| dephased_whole_state | reservoir_above_0.5 |  |  |
| dephased_whole_state | membrane_below_0.5 |  |  |
| dephased_whole_state | terrain_above_0.5 |  |  |
| dephased_whole_state | output_above_0.5 |  |  |
| coherent_whole_state | quality_below_0.7 | 11 | 0.679689 |
| coherent_whole_state | quality_below_0.5 | 26 | 0.497680 |
| coherent_whole_state | reservoir_above_0.5 | 26 | 0.503779 |
| coherent_whole_state | membrane_below_0.5 | 15 | 0.499955 |
| coherent_whole_state | terrain_above_0.5 | 134 | 0.505771 |
| coherent_whole_state | output_above_0.5 | 124 | 0.500937 |

## Interpretation

This corrects the earlier finite-core comparison.

The earlier comparison only quantumized the local M/C/R pass-convert-store core and left most sandbox variables classical. It did not test the user's intended whole-state idea.

Here, the main sandbox variables are coarse-grained into one coupled state. Under that whole-state construction, coherent evolution differs from the dephased/classical finite-state control.

The main qualitative pattern is:

```text
classical/dephased:
  slow quality degradation only; no 0.5-threshold reservoir, membrane, terrain, or output events

coherent whole-state:
  earlier quality collapse
  reservoir threshold appears
  membrane threshold appears
  terrain threshold appears later
  output threshold appears later
```

## Safe claim

```text
A coarse 10-qubit whole-state quantumization of the information microreactor sandbox differs from the dephased/classical finite-state control under the tested coupled dynamics. This shows that putting the sandbox variables into one coherent global state can change event ordering and aggregate observables, unlike the earlier local finite-core quantumization.
```

## What this does not claim

```text
not a full continuous-variable quantum microreactor
not a hardware result
not quantum advantage
not biological metabolism
not life-like behavior
not a no-go or universal positive result
```

## Audit note

The coherent difference is a finite-model whole-state coherence/interference effect. It should not be confused with natural device throughput or hardware evidence.
