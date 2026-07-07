# Phenomenology scripts

This directory is reserved for generator scripts for the information-matter phenomenology layer.

Until a report has a script here, plus seed/config/raw logs, it should remain `PHENOMENOLOGY_NOTE` in `results/STATUS.md`.

Planned generators:

```text
membrane_characterization.py
storage_reservoir.py
source_sink_pair.py
converter.py
reaction_written_terrain.py
syntax_driven_information_matter.py
```

Required script behavior:

```text
1. accept explicit seed/config arguments
2. write raw json/csv/jsonl logs
3. write or print summary tables generated from raw logs
4. avoid hand-coded result tables
5. state whether the model is quantum, classical probability, classical wave, or phenomenological stochastic
```
