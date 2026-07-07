# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_adaptive_measurement_feedback_probe
```

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/quantum_adaptive_measurement_feedback_probe_2026-07-08.md
experiments/quantum_adaptive_measurement_feedback_probe_protocol_2026-07-08.md
scripts/audit/quantum_adaptive_measurement_feedback_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_adaptive_measurement_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707_summary.csv
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

New canonical log:

```text
data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707_summary.csv
```

## Current result

```text
POSITIVE_FOR_MODEL_LEVEL_ADAPTIVE_MEASUREMENT_FEEDBACK
```

Key results:

```text
stress gamma=0.25: phase1 write 0.365920, phase2 adaptive steps 17, phase3 adaptive steps 294, phase2 release +1.441263%, phase3 +0.115964%
stress gamma=0: phase1 write 11.462247, phase2 adaptive steps 276, phase3 adaptive steps 395, phase2 release +24.458321%, phase3 +6.921294%
gamma>=0.5: no positive adaptive loop effect
normal/storage: later adaptive activity alone is not counted positive without phase1 Bell-excess terrain inscription
matched replay: phase2/phase3 diff vs Arm3 = 0
```

## Safe claim

```text
Finite-shot sampled CHSH terrain memory can shift later adaptive measurement/readout gates and alter later reactor output in stress context. The matched replay shows the post-write adaptive dynamics follow the written terrain trace; quantum-specificity remains at the Bell-bound measurement/write/readout boundary, not in ordinary local population plumbing.
```

## Next boundary

```text
fixed-basis / hardware-like adaptive circuit
membrane decision boundary using adaptive terrain memory
adaptive basis schedule pre-registered without per-step optimization
```
