# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_measurement_backaction_terrain_probe
```

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
results/quantum_measurement_backaction_terrain_probe_2026-07-08.md
experiments/quantum_measurement_backaction_terrain_probe_protocol_2026-07-08.md
scripts/audit/quantum_measurement_backaction_terrain_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_measurement_backaction_terrain_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707_summary.csv
```

## Current result

```text
POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_BACKACTION_TERRAIN
```

Key results:

```text
stress gamma=0 projective measurement: signal -100%, terrain -99.958308%, release -1.149391%
stress gamma=0 gentle measurement: signal -33.013319%, terrain -32.333922%, release -0.635817%
gamma=1 null: no effect
normal/storage: no effect
```

## Safe claim

```text
In stress gamma=0, invasive measurement of the boundary state suppresses later Bell-excess terrain signal and lowers downstream release after measurement stops being treated as a passive readout. The effect is backaction-like and negative/suppressive: measurement changes the future boundary state rather than merely reporting it. Normal/storage and gamma=1 null rows remain unchanged.
```

## Next boundary

```text
quantum_context_order_terrain_probe
```
