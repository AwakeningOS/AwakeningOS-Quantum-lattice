# Quantum Measurement Backaction Terrain Probe

Date: 2026-07-08

Status: `RAW_LOG_BACKED`
Layer: `quantum-audit probe`

Generator script:

```text
scripts/audit/quantum_measurement_backaction_terrain_probe.py
```

Canonical raw log:

```text
data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707_summary.csv
```

Auxiliary metadata:

```text
data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707.json
```

Run command:

```bash
python scripts/audit/quantum_measurement_backaction_terrain_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707_summary.csv
```

## Purpose

This experiment tests whether measurement itself changes the later boundary state and thereby alters subsequent terrain and release.

This is not another direct terrain-write probe.

```text
previous line:
  measured CHSH excess -> terrain write

this probe:
  measurement backaction -> later boundary state -> later terrain/release
```

## Design

A persistent two-qubit boundary state is carried across steps.

At each step:

```text
rho_t drifts toward the reactor-implied target state
Bell-excess terrain signal is computed from rho_t
terrain receives only the pre-measurement Bell-excess signal
then the measurement arm applies nonselective local projective/dephasing measurement
```

The measurement outcome is not written to terrain. Any later difference must come from the altered future boundary state.

## Arms

```text
no_measure:
  boundary state evolves without invasive measurement

projective_measure:
  full nonselective local projective/dephasing measurement in alternating fixed CHSH bases

gentle_measure:
  weak nonselective measurement/dephasing with strength 0.01
```

## Verdict

```text
POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_BACKACTION_TERRAIN
```

## P1 gamma=1 null

Result: PASS.

| scenario | arm | gamma | signal dev | terrain dev | release dev |
|---|---|---:|---:|---:|---:|
| normal_backaction | projective_measure | 1.0 | 0.000000% | 0.000000% | 0.000000% |
| stress_backaction | projective_measure | 1.0 | 0.000000% | 0.000000% | 0.000000% |
| storage_backaction | projective_measure | 1.0 | 0.000000% | 0.000000% | 0.000000% |

## P2 stress gamma=0 backaction

Result: PASS.

| arm | strength | signal no-measure | signal arm | signal dev | terrain no-measure | terrain arm | terrain dev | release dev |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| projective_measure | 1.00 | 450.740698 | 0.000000 | -100.000000% | 1.278410 | 0.000533 | -99.958308% | -1.149391% |
| gentle_measure | 0.01 | 450.740698 | 301.936232 | -33.013319% | 1.278410 | 0.865050 | -32.333922% | -0.635817% |

The important result is not that measurement improves output. It does not.

The important result is:

```text
measurement changes the future boundary state
-> later Bell-excess terrain signal changes
-> final terrain and release change
```

## P3 normal/storage specificity

Result: PASS.

Normal and storage have no Bell-excess terrain signal in this setup, so measurement backaction has no downstream effect.

At gamma=0:

| scenario | arm | signal no-measure | signal arm | terrain dev | release dev | effect? |
|---|---|---:|---:|---:|---:|---|
| normal_backaction | projective_measure | 0.000000 | 0.000000 | 0.000000% | 0.000000% | FALSE |
| storage_backaction | projective_measure | 0.000000 | 0.000000 | 0.000000% | 0.000000% | FALSE |

## Interpretation

This is a backaction positive, but it is a suppressive positive.

Supported chain:

```text
invasive measurement of the boundary state
-> nonselective local projection/dephasing
-> later Bell-excess signal suppressed
-> terrain memory suppressed
-> downstream release reduced
```

This is closer to a measurement-backaction phenomenon than the previous terrain-write experiments because the measurement result is not directly written to terrain.

## Safe claim

```text
In stress gamma=0, invasive measurement of the boundary state suppresses later Bell-excess terrain signal and lowers downstream release after measurement stops being treated as a passive readout. The effect is backaction-like and negative/suppressive: measurement changes the future boundary state rather than merely reporting it. Normal/storage and gamma=1 null rows remain unchanged.
```

## What this does not show

```text
not hardware result
not chemical realism
not biological metabolism
not universal quantum advantage
not measurement improves output
not ordinary local population plumbing
not proof of consciousness or observer causation
```

## Next boundary

```text
quantum_context_order_terrain_probe
```

The next strict test is order dependence:

```text
same boundary state
basis/order A -> B vs B -> A
terrain/release difference after noncommuting measurement order
```
