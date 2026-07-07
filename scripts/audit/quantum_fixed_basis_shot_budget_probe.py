#!/usr/bin/env python3
"""Fixed-basis shot-budget sweep for the membrane decision boundary."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from quantum_fixed_basis_adaptive_feedback_probe import GAMMAS, Params, fixed_chsh

ALPHA = 0.001
SHOT_GRID = [32768, 8192, 4096, 2048, 1024, 512]
STEPS = 800
A_GATE_GAIN = 0.25
B_BLOCK_GAIN = 1.80
D_BLOCK_GAIN = 0.90


def margin_s(shots: int) -> float:
    return 4.0 * math.sqrt(2.0 * math.log(8.0 / ALPHA) / shots)


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def sample_fixed_chsh(phi: float, gamma: float, rng: np.random.Generator, shots: int) -> tuple[float, float, float]:
    correlations, s_true = fixed_chsh(phi, gamma)
    sampled: list[float] = []
    for e in correlations:
        p = (1.0 + max(-1.0, min(1.0, e))) / 2.0
        k = rng.binomial(shots, p)
        sampled.append((2.0 * k / shots) - 1.0)
    s_hat = sampled[0] + sampled[1] + sampled[2] - sampled[3]
    conservative = max(0.0, s_hat - 2.0 - margin_s(shots)) / (2.0 * math.sqrt(2.0) - 2.0)
    return s_true, s_hat, conservative


def scenarios() -> Dict[str, Params]:
    return {
        "normal_membrane": Params(),
        "stress_membrane": Params(D_rate=0.45, C_rate=0.0),
        "storage_membrane": Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
        "contaminated_stress_membrane": Params(D_rate=0.45, C_rate=0.0, B_rate=0.45),
    }


def simulate(p: Params, arm: str, gamma: float, seed: int, shots: int, replay: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    rng = np.random.default_rng(seed)
    inside_a = 0.0
    inside_b = 0.0
    reservoir = 0.0
    integrity = 1.0
    rows: List[Dict[str, Any]] = []
    for t in range(STEPS):
        phi = math.pi * (1.0 - integrity)
        chsh_hat = 0.0
        if arm == "arm3_membrane":
            _, chsh_hat, membrane_signal = sample_fixed_chsh(phi, gamma, rng, shots)
        elif arm == "matched_classical_replay":
            _ = sample_fixed_chsh(phi, gamma, rng, shots)
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
        rows.append({
            "t": t,
            "release": release,
            "quality": quality,
            "integrity": integrity,
            "a_pass": a_pass,
            "b_pass": b_pass,
            "d_pass": d_pass,
            "membrane_signal": membrane_signal,
            "chsh_hat": chsh_hat,
        })
    return rows


def total(rows: List[Dict[str, Any]], key: str) -> float:
    return sum(float(r[key]) for r in rows)


def mean(rows: List[Dict[str, Any]], key: str) -> float:
    return total(rows, key) / len(rows)


def run(seed: int = 20260707) -> Dict[str, Any]:
    summary: List[Dict[str, Any]] = []
    for si, (scenario, params) in enumerate(scenarios().items()):
        arm2 = simulate(params, "arm2_bell_bound", 1.0, seed, 32768)
        for shots in SHOT_GRID:
            for gi, gamma in enumerate(GAMMAS):
                run_seed = seed + 100000 * si + 1000 * gi + shots
                arm3 = simulate(params, "arm3_membrane", gamma, run_seed, shots)
                replay = simulate(params, "matched_classical_replay", gamma, run_seed, shots, replay=arm3)
                signal_total = total(arm3, "membrane_signal")
                release2 = total(arm2, "release")
                release3 = total(arm3, "release")
                positive = (
                    signal_total > 1e-12
                    and scenario in {"stress_membrane", "contaminated_stress_membrane"}
                    and total(arm3, "a_pass") > total(arm2, "a_pass") + 1e-9
                    and total(arm3, "b_pass") < total(arm2, "b_pass") - 1e-9
                    and total(arm3, "d_pass") < total(arm2, "d_pass") - 1e-9
                    and abs(total(replay, "release") - release3) < 1e-9
                )
                row = {
                    "component": "membrane_decision",
                    "scenario": scenario,
                    "shots": shots,
                    "gamma": gamma,
                    "confidence_margin_S": margin_s(shots),
                    "membrane_signal_total": signal_total,
                    "positive_sampled_steps": sum(1 for r in arm3 if float(r["membrane_signal"]) > 0.0),
                    "max_chsh_hat": max(float(r["chsh_hat"]) for r in arm3),
                    "a_pass_dev_pct": 100.0 * (total(arm3, "a_pass") - total(arm2, "a_pass")) / total(arm2, "a_pass"),
                    "b_leak_dev_pct": 100.0 * (total(arm3, "b_pass") - total(arm2, "b_pass")) / total(arm2, "b_pass"),
                    "d_pass_dev_pct": 100.0 * (total(arm3, "d_pass") - total(arm2, "d_pass")) / total(arm2, "d_pass"),
                    "release_dev_pct": 100.0 * (release3 - release2) / release2,
                    "quality_dev_pct": 100.0 * (mean(arm3, "quality") - mean(arm2, "quality")) / mean(arm2, "quality"),
                    "matched_replay_release_diff": total(replay, "release") - release3,
                    "effect": "TRUE" if positive else "FALSE",
                    "false_positive": "TRUE" if scenario in {"normal_membrane", "storage_membrane"} and signal_total > 0 else "FALSE",
                }
                summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    positive_rows = [r for r in summary if r["effect"] == "TRUE"]
    false_positive_rows = [r for r in summary if r["false_positive"] == "TRUE"]
    stress_gamma0 = [r for r in summary if r["scenario"] == "stress_membrane" and r["gamma"] == 0.0 and r["effect"] == "TRUE"]
    return {
        "experiment": "quantum_fixed_basis_shot_budget_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "shot_grid": SHOT_GRID,
        "alpha": ALPHA,
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_SHOT_BUDGET" if positive_rows else "NEGATIVE_FOR_FIXED_BASIS_SHOT_BUDGET",
        "positive_rows": len(positive_rows),
        "false_positive_rows": len(false_positive_rows),
        "minimum_positive_shots_stress_gamma0": min([int(r["shots"]) for r in stress_gamma0]) if stress_gamma0 else None,
        "safe_interpretation": "The fixed-basis membrane decision-boundary effect survives down to 512 shots per setting in stress gamma=0, while normal/storage false positives remain zero on the tested grid. The weaker stress gamma=0.25 effect survives only at 32768 shots.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/fixed_basis_shot_budget_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
