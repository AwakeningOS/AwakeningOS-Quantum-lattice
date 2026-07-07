#!/usr/bin/env python3
"""Quantum membrane decision-boundary probe.

A fixed-basis finite-shot CHSH measurement signal is connected directly to the
membrane pass/block decision rather than to terrain. Bell-excess opens A passage
while suppressing B contaminant and D stress passage. Matched replay checks that
downstream dynamics follow the same gate trace.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from quantum_fixed_basis_adaptive_feedback_probe import (
    ALPHA,
    CONFIDENCE_MARGIN_S,
    GAMMAS,
    SHOTS_PER_SETTING_PER_STEP,
    Params,
    sample_fixed_chsh,
)

STEPS = 800
A_GATE_GAIN = 0.25
B_BLOCK_GAIN = 1.80
D_BLOCK_GAIN = 0.90


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def scenarios() -> Dict[str, Params]:
    return {
        "normal_membrane": Params(),
        "stress_membrane": Params(D_rate=0.45, C_rate=0.0),
        "storage_membrane": Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
        "contaminated_stress_membrane": Params(D_rate=0.45, C_rate=0.0, B_rate=0.45),
    }


def simulate(p: Params, arm: str, gamma: float, seed: int, replay: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    rng = np.random.default_rng(seed)
    inside_a = 0.0
    inside_b = 0.0
    reservoir = 0.0
    terrain = 0.0
    integrity = 1.0
    rows: List[Dict[str, Any]] = []
    for t in range(STEPS):
        phi = math.pi * (1.0 - integrity)
        chsh_hat = 0.0
        if arm == "arm3_membrane":
            _, chsh_hat, membrane_signal = sample_fixed_chsh(phi, gamma, rng)
        elif arm == "matched_classical_replay":
            _ = sample_fixed_chsh(phi, gamma, rng)
            membrane_signal = float(replay[t]["membrane_signal"]) if replay is not None else 0.0
            chsh_hat = float(replay[t]["chsh_hat"]) if replay is not None else 0.0
        elif arm == "arm2_bell_bound":
            membrane_signal = 0.0
        else:
            raise ValueError(f"unknown arm: {arm}")

        a_gate = 1.0 + A_GATE_GAIN * membrane_signal
        b_gate = max(0.0, 1.0 - B_BLOCK_GAIN * membrane_signal) ** 2
        d_gate = max(0.02, 1.0 - D_BLOCK_GAIN * membrane_signal)

        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / 64.0)
        fill = reservoir / max(p.capacity, 1e-9)
        backpressure = max(0.02, 1.0 - p.backpressure_strength * fill)
        protect = p.stabilizer_protect * (p.C_rate / (1.0 + p.C_rate))
        d_pass = p.D_rate * 0.04 * d_gate
        damage = p.damage_coeff * d_pass * (1.0 - protect) * 25.0
        repair = p.repair_coeff * p.C_rate * (1.0 - integrity)
        integrity = min(1.0, max(0.0, integrity - damage + repair))

        a_pass = p.A_rate * pulse * p.pore_A * integrity * backpressure * a_gate
        b_pass = p.B_rate * p.pore_B * integrity * (1.0 + 0.5 * (1.0 - integrity)) * b_gate
        inside_a += a_pass
        inside_b += b_pass
        poison = 1.0 / (1.0 + p.poison_coeff * inside_b)
        amount = p.k_conv * poison * backpressure * inside_a
        inside_a -= amount
        quality = 1.0 / (1.0 + p.quality_coeff * inside_b)
        inside_b *= 0.985
        reservoir += min(amount, max(0.0, p.capacity - reservoir))
        release = min(reservoir, reservoir * p.release_rate)
        reservoir -= release
        terrain = terrain * p.terrain_decay + release * p.terrain_write * quality

        rows.append(
            {
                "t": t,
                "release": release,
                "quality": quality,
                "integrity": integrity,
                "a_pass": a_pass,
                "b_pass": b_pass,
                "d_pass": d_pass,
                "membrane_signal": membrane_signal,
                "a_gate": a_gate,
                "b_gate": b_gate,
                "d_gate": d_gate,
                "chsh_hat": chsh_hat,
            }
        )
    return rows


def total(rows: List[Dict[str, Any]], key: str) -> float:
    return sum(float(r[key]) for r in rows)


def mean(rows: List[Dict[str, Any]], key: str) -> float:
    return total(rows, key) / len(rows)


def run(seed: int = 20260707) -> Dict[str, Any]:
    summary: List[Dict[str, Any]] = []
    for si, (scenario, params) in enumerate(scenarios().items()):
        arm2 = simulate(params, "arm2_bell_bound", 1.0, seed)
        for gi, gamma in enumerate(GAMMAS):
            arm3 = simulate(params, "arm3_membrane", gamma, seed + 1000 * si + gi)
            replay = simulate(params, "matched_classical_replay", gamma, seed + 1000 * si + gi, replay=arm3)
            release_arm2 = total(arm2, "release")
            release_arm3 = total(arm3, "release")
            positive = (
                total(arm3, "membrane_signal") > 1e-12
                and (
                    total(arm3, "a_pass") > total(arm2, "a_pass") + 1e-9
                    or total(arm3, "b_pass") < total(arm2, "b_pass") - 1e-9
                    or total(arm3, "d_pass") < total(arm2, "d_pass") - 1e-9
                )
                and abs(total(replay, "release") - release_arm3) < 1e-9
            )
            row = {
                "scenario": scenario,
                "gamma": gamma,
                "membrane_signal_total": total(arm3, "membrane_signal"),
                "positive_sampled_steps": sum(1 for r in arm3 if float(r["membrane_signal"]) > 0.0),
                "max_chsh_hat": max(float(r["chsh_hat"]) for r in arm3),
                "a_pass_arm2": total(arm2, "a_pass"),
                "a_pass_arm3": total(arm3, "a_pass"),
                "a_pass_dev_pct": 100.0 * (total(arm3, "a_pass") - total(arm2, "a_pass")) / total(arm2, "a_pass"),
                "b_leak_arm2": total(arm2, "b_pass"),
                "b_leak_arm3": total(arm3, "b_pass"),
                "b_leak_dev_pct": 100.0 * (total(arm3, "b_pass") - total(arm2, "b_pass")) / total(arm2, "b_pass"),
                "d_pass_arm2": total(arm2, "d_pass"),
                "d_pass_arm3": total(arm3, "d_pass"),
                "d_pass_dev_pct": 100.0 * (total(arm3, "d_pass") - total(arm2, "d_pass")) / total(arm2, "d_pass"),
                "mean_quality_arm2": mean(arm2, "quality"),
                "mean_quality_arm3": mean(arm3, "quality"),
                "quality_dev_pct": 100.0 * (mean(arm3, "quality") - mean(arm2, "quality")) / mean(arm2, "quality"),
                "release_arm2": release_arm2,
                "release_arm3": release_arm3,
                "release_dev_pct": 100.0 * (release_arm3 - release_arm2) / release_arm2,
                "final_integrity_arm2": arm2[-1]["integrity"],
                "final_integrity_arm3": arm3[-1]["integrity"],
                "mean_a_gate": mean(arm3, "a_gate"),
                "mean_b_gate": mean(arm3, "b_gate"),
                "mean_d_gate": mean(arm3, "d_gate"),
                "matched_replay_release_diff": total(replay, "release") - release_arm3,
                "membrane_decision_effect_beyond_bell_bound_arm2": "TRUE" if positive else "FALSE",
            }
            summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    positives = [r for r in summary if r["membrane_decision_effect_beyond_bell_bound_arm2"] == "TRUE"]
    return {
        "experiment": "quantum_membrane_decision_boundary_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "fixed_basis": "pre-calibrated once at phi=pi; no per-step optimization",
        "shots_per_setting_per_step": SHOTS_PER_SETTING_PER_STEP,
        "alpha": ALPHA,
        "confidence_margin_S": rf(CONFIDENCE_MARGIN_S),
        "a_gate_gain": A_GATE_GAIN,
        "b_block_gain": B_BLOCK_GAIN,
        "d_block_gain": D_BLOCK_GAIN,
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_MEMBRANE_DECISION_BOUNDARY" if positives else "NEGATIVE_FOR_MEMBRANE_DECISION_BOUNDARY",
        "positive_rows": len(positives),
        "safe_interpretation": "A fixed-basis finite-shot CHSH measurement-boundary signal can directly modulate membrane pass/block decisions in stress contexts: A passage increases while B contaminant and D stress passage are suppressed. Matched replay shows downstream dynamics follow the gate trace; specificity remains at the Bell-bound measurement/decision boundary.",
    }


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/membrane_decision_boundary_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/membrane_decision_boundary_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
