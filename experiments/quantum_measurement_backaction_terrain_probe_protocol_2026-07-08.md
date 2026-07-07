# Quantum Measurement Backaction Terrain Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

Does measurement itself change the later boundary state and thereby alter subsequent terrain and release, even when measurement outcomes are not directly written to terrain?

This differs from the earlier terrain-write line:

```text
previous: measured CHSH excess -> terrain write
this probe: measurement backaction -> later boundary state -> later terrain/release
```

## Model

A persistent two-qubit boundary state is carried across steps.

At each step:

```text
rho_t drifts toward the reactor-implied target state
Bell-excess terrain signal is computed from rho_t
terrain receives only the pre-measurement Bell-excess signal
then the measurement arm applies nonselective local projective/dephasing measurement
```

The measurement outcome is not written to terrain. Any difference in later terrain/release must come from the changed future boundary state.

## Arms

```text
no_measure:
  boundary state evolves without invasive measurement

projective_measure:
  full nonselective local projective measurement in alternating fixed CHSH bases

gentle_measure:
  weak nonselective measurement/dephasing with strength 0.01
```

## Contexts

```text
normal_backaction
stress_backaction
storage_backaction
```

## Gamma values

```text
1.0, 0.0
```

## Success criteria

A model-level backaction positive requires:

```text
1. no_measure has Bell-excess terrain signal
2. measurement arm changes later signal_total
3. measurement arm changes final terrain or release
4. gamma=1 null remains zero
5. normal/storage remain unchanged
```

## Important expected direction

The expected effect is suppressive, not beneficial:

```text
invasive measurement collapses/dephases the boundary state
-> later Bell-excess terrain signal falls
-> final terrain and release decrease
```

## Expected outputs

```text
data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707_summary.csv
data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_measurement_backaction_terrain_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707_summary.csv
```

## Forbidden claims

Do not claim:

```text
hardware result
chemical realism
biological metabolism
universal quantum advantage
measurement improves output
ordinary local population plumbing is quantum-specific
```
