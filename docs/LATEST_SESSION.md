# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_context_order_terrain_probe
```

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
results/quantum_context_order_terrain_probe_2026-07-08.md
experiments/quantum_context_order_terrain_probe_protocol_2026-07-08.md
scripts/audit/quantum_context_order_terrain_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_context_order_terrain_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/context_order_terrain_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/context_order_terrain_probe_seed20260707_summary.csv
```

## Current result

```text
POSITIVE_FOR_MODEL_LEVEL_CONTEXT_ORDER_TERRAIN
```

Key results:

```text
stress gamma=0: AB signal total 198.363585, BA signal total 0
stress gamma=0: AB positive steps 683, BA positive steps 0
stress gamma=0: final terrain 1.266166 vs 0.003792
stress gamma=0: release AB +2.038803% vs BA
gamma=1 null: no effect
normal/storage: no effect
matched replay release diff vs AB = 0
```

## Safe claim

```text
With fixed noncommuting context probes and no direct outcome write beyond the conservative order signal, AB and BA read order diverge only in stress gamma=0. AB produces a conservative order signal, higher final terrain, and higher downstream release; BA remains at baseline. Gamma=1 and normal/storage are null. Matched replay reproduces downstream release once the order-signal trace is fixed, so specificity is at the context-order measurement boundary.
```

## Next boundary

```text
integrated status report / synthesis
separate negative plumbing results from positive measurement-boundary results
```
