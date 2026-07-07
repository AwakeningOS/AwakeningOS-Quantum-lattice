# Latest Session Handoff

Updated: 2026-07-08

## Current latest experiment

```text
quantum_fixed_basis_adaptive_feedback_probe
```

## Files to read first

```text
README.md
SKILLS.md
results/STATUS.md
docs/RAW_LOG_GATE.md
results/quantum_fixed_basis_adaptive_feedback_probe_2026-07-08.md
experiments/quantum_fixed_basis_adaptive_feedback_probe_protocol_2026-07-08.md
scripts/audit/quantum_fixed_basis_adaptive_feedback_probe.py
```

## Reproduction command

```bash
python scripts/audit/quantum_fixed_basis_adaptive_feedback_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707_summary.csv
```

## RAW_LOG gate

Run:

```bash
python scripts/check_raw_logs.py
```

New canonical log:

```text
data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707_summary.csv
```

## Current result

```text
POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_ADAPTIVE_FEEDBACK
```

Key results:

```text
stress gamma=0.25: phase1 write 0.360060, phase2 adaptive steps 12, phase3 adaptive steps 289, phase2 release +1.438670%, phase3 +0.105794%
stress gamma=0: phase1 write 10.580120, phase2 adaptive steps 90, phase3 adaptive steps 346, phase2 release +21.867957%, phase3 +3.988183%
gamma>=0.5: no positive fixed-basis adaptive effect
normal/storage: later adaptive activity alone is not counted positive without phase1 Bell-excess terrain inscription
matched replay: phase2/phase3 diff vs Arm3 = 0
```

## Safe claim

```text
A fixed-basis finite-shot CHSH measurement boundary, pre-calibrated once rather than optimized per step, can still write terrain memory and shift later adaptive measurement gates in stress context. Normal/storage later adaptive activity is not counted positive without phase-1 Bell-excess terrain inscription. This remains model-level and not hardware or ordinary local population plumbing.
```

## Next boundary

```text
membrane decision boundary using adaptive terrain memory
pre-registered hardware shot budget
explicit QPU candidate circuit
noise-model robustness
```
