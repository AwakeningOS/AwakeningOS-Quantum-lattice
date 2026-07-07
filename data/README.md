# Raw data and logs

Raw experiment outputs should be committed here when they are needed to support a result.

Recommended layout:

```text
data/quantum_core/
data/history_droplet/
data/membrane/
data/reservoir/
data/source_sink/
data/converter/
```

Allowed formats:

```text
json
jsonl
csv
npz metadata summaries
```

A Markdown report in `results/` should cite or name the raw data file and the generator script used to produce it.

A report without raw data and generator script remains a `PHENOMENOLOGY_NOTE` or `QUARANTINED_CLAIM`.
