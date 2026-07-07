# Quantum Measurement Terrain Memory Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

Does terrain written by a quantum measurement-boundary signal persist as reactor memory after measurement stops, and does it alter later reactor response?

This follows:

```text
quantum_sampled_chsh_terrain_feedback_probe
```

That result showed that sampled CHSH excess can be written into terrain and modulate the next phase. This protocol asks whether the written terrain behaves as a longer-lived history / memory trace.

## Key distinction

This protocol separates two claims:

```text
1. quantum-specific write eligibility:
   only conservative CHSH excess over the Bell bound may write terrain

2. post-write memory dynamics:
   once written, terrain is a classical-effective memory variable
```

A matched classical replay arm is included to test whether the post-write memory itself is quantum-specific. If replaying the same write trajectory reproduces later dynamics, then the quantum-specific part is the write boundary, not the decay/readout of terrain.

## Three-phase design

```text
Phase 1: measurement/write phase, t = 0..399
Phase 2: memory/read phase, t = 400..799
Phase 3: challenge phase, t = 800..1199
```

During Phase 1:

```text
finite-shot CHSH is sampled
conservative_excess = max(0, S_hat - 2 - margin) / (2*sqrt(2)-2)
measurement_terrain_write = 0.04 * conservative_excess
```

During Phases 2 and 3:

```text
measurement write is off
terrain decays normally
terrain is read through road_boost
```

## Arms

```text
Arm2/Bell-bound control:
  no CHSH excess write

Arm3 sampled CHSH:
  conservative sampled Bell excess can write terrain in Phase 1

Matched classical replay:
  replay the exact Arm3 terrain write trajectory as a classical external write
```

## Success criteria

A model-level terrain-memory positive requires:

```text
1. conservative sampled CHSH write > 0 in Phase 1
2. terrain_delta_end_phase1 > 0 versus Arm2
3. terrain_delta_end_phase2 > 0 after measurement has stopped
4. Phase 2 or Phase 3 release differs from Arm2
5. gamma=1 removes the effect
```

## Specificity criteria

Post-write memory is not quantum-specific if:

```text
matched classical replay reproduces Arm3 Phase 2 and Phase 3 release
```

That outcome means:

```text
quantum-specificity is at the measurement/write boundary
terrain memory itself is classical-effective once inscribed
```

## Tested contexts

```text
normal_memory
stress_memory
storage_memory
```

## Expected raw outputs

```text
data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv
data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_measurement_terrain_memory_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv
```

## Forbidden claims

Do not claim:

```text
hardware result
chemical realism
biological metabolism
universal quantum advantage
post-write terrain decay is quantum-specific
ordinary local population plumbing is quantum-specific
```
