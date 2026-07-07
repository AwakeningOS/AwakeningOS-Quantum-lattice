# Quantum KCBS Qutrit Contextuality Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit contextual-boundary probe`

## Question

Can quantum structure be seen as contextuality of questions rather than as transport amount?

## Setup

Single qutrit KCBS pentagon.

Five yes/no projectors are arranged so adjacent projectors are exclusive. The tested observable is the sum of five yes probabilities.

## Bounds

```text
noncontextual bound = 2
quantum value = sqrt(5) = 2.236067977500
```

## Scope

This is not a reactor transport probe and not a downstream switch. It is a standard contextuality witness in the question boundary layer.

## Run command

```bash
python scripts/audit/quantum_kcbs_qutrit_contextuality_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/kcbs_qutrit_contextuality_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/kcbs_qutrit_contextuality_probe_seed20260707_summary.csv
```
