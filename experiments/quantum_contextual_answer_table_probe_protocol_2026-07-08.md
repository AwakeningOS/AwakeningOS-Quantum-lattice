# Quantum Contextual Answer Table Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit contextual-boundary probe`

## Question

Can quantum structure be seen at the boundary of questions rather than in physical transport amount?

This probe asks whether one context-independent answer table can satisfy all compatible question contexts.

## Setup

Use the Peres-Mermin two-qubit square:

```text
XI, IX, XX
IY, YI, YY
XY, YX, ZZ
```

Compatible context products:

```text
row1 = +1
row2 = +1
row3 = +1
col1 = +1
col2 = +1
col3 = -1
```

A quantum context arm satisfies all six product constraints. A noncontextual fixed answer table cannot satisfy all six at once.

## Arms

```text
quantum_context
noncontextual_answer_table
context_indexed_replay
```

## Success criteria

```text
quantum_context: 6/6 constraints
best noncontextual fixed table: 5/6 constraints
inequality score: quantum 6, noncontextual bound 4
context-indexed replay: 6/6 but only by allowing context-dependent answers
```

## Run command

```bash
python scripts/audit/quantum_contextual_answer_table_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/contextual_answer_table_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/contextual_answer_table_probe_seed20260707_summary.csv
```

## Scope

This is not a transport-advantage probe. It is a contextual question-boundary witness.
