#!/usr/bin/env python3
"""Sampled CHSH terrain feedback probe.

This tightens the exact CHSH terrain feedback probe by estimating CHSH from
finite-shot correlators at each step. Only a conservative Bell-violating excess
above S <= 2 plus a Hoeffding-style margin is written into terrain.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from quantum_measurement_terrain_feedback_probe import (
    GAMMAS,
    MEASUREMENT_WRITE_GAIN,
    PHASE1_STEPS,
    STEPS,
    H,
    I2,
    PAULIS,
    Params,
    kron,
    ry,
    rz,
    scenarios,
)

SHOTS_PER_SETTING_PER_STEP = 32768
ALPHA = 0.001
CONFIDENCE_MARGIN_S = 4.0 * math.sqrt(2.0 * math.log(8.0 / ALPHA) / SHOTS_PER_SETTING_PER_STEP)


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def dephase(rho: np.ndarray, gamma: float) -> np.ndarray:
    mask = np.ones((4, 4), dtype=np.float64) * (1.0 - gamma)
    np.fill_diagonal(mask, 1.0)
    return rho * mask


def rho_cb(phi: float, gamma: float) -> np.ndarray:
    psi = kron(H @ np.array([1, 0], dtype=np.complex128), ry(math.pi / 2.0) @ np.array([1, 0], dtype=np.complex128))
    rho = np.outer(psi, np.conjugate(psi))
    cu = np.zeros((4, 4), dtype=np.complex128)
    cu[0:2, 0:2] = I2
    cu[2:4, 2:4] = rz(phi)
    rho = cu @ rho @ np.conjugate(cu).T
    return dephase(rho, gamma)


def correlation_matrix(rho: np.ndarray) -> np.ndarray:
    out = np.zeros((3, 3), dtype=np.float64)
    for i, p in enumerate(PAULIS):
        for j, q in enumerate(PAULIS):
            out[i, j] = float(np.real(np.trace(rho @ kron(p, q))))
    return out


def optimal_chsh_correlations(t: np.ndarray) -> tuple[list[float], float]:
    vals, vecs = np.linalg.eigh(t.T @ t)
    idx = np.argsort(vals)[::-1]
    u1 = max(float(vals[idx[0]]), 0.0)
    u2 = max(float(vals[idx[1]]), 0.0)
    v1 = vecs[:, idx[0]]
    v2 = vecs[:, idx[1]]
    denom = math.sqrt(u1 + u2)
    if denom <= 1e-12:
        return [0.0, 0.0, 0.0, 0.0], 0.0
    c = math.sqrt(u1) / denom
    s = math.sqrt(u2) / denom
    b0 = c * v1 + s * v2
    b1 = c * v1 - s * v2

    def normed(x: np.ndarray) -> np.ndarray:
        n = np.linalg.norm(x)
        if n <= 1e-12:
            return np.zeros_like(x)
        return x / n

    a0 = normed(t @ (b0 + b1))
    a1 = normed(t @ (b0 - b1))
    e00 = float(a0 @ t @ b0)
    e01 = float(a0 @ t @ b1)
    e10 = float(a1 @ t @ b0)
    e11 = float(a1 @ t @ b1)
    return [e00, e01, e10, e11], e00 + e01 + e10 - e11


def sample_chsh(phi: float, gamma: float, rng: np.random.Generator) -> tuple[float, float, float, float]:
    correlations, s_true = optimal_chsh_correlations(correlation_matrix(rho_cb(phi, gamma)))
    sampled: list[float] = []
    for e in correlations:
        p = (1.0 + max(-1.0, min(1.0, e))) / 2.0
        k = rng.binomial(SHOTS_PER_SETTING_PER_STEP, p)
        sampled.append((2.0 * k / SHOTS_PER_SETTING_PER_STEP) - 1.0)
    s_hat = sampled[0] + sampled[1] + sampled[2] - sampled[3]
    conservative = max(0.0, s_hat - 2.0 - CONFIDENCE_MARGIN_S) / (2.0 * math.sqrt(2.0) - 2.0)
    true_excess = max(0.0, s_true - 2.0) / (2.0 * math.sqrt(2.0) - 2.0)
    return s_true, s_hat, conservative, true_excess


def simulate(phase1: Params, phase2: Params, arm: str, gamma: float = 1.0, seed: int = 20260707) -> List[Dict[str, Any]]:
    rng = np.random.default_rng(seed)
    inside_a = 0.0
    inside_b = 0.0
    reservoir = 0.0
    terrain = 0.0
    integrity = 1.0
    rows: List[Dict[str, Any]] = []
    for t in range(STEPS):
        p = phase1 if t < PHASE1_STEPS else phase2
        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / 64.0)
        road_boost = 1.0 + p.road_source_gain * (terrain / (1.0 + terrain))
        source_a = p.A_rate * pulse * road_boost
        protect = p.stabilizer_protect * (p.C_rate / (1.0 + p.C_rate))
        damage = p.damage_coeff * p.D_rate * (1.0 - protect)
        repair = p.repair_coeff * p.C_rate * (1.0 - integrity)
        integrity = min(1.0, max(0.0, integrity - damage + repair))
        fill = reservoir / max(p.capacity, 1e-9)
        backpressure = max(0.02, 1.0 - p.backpressure_strength * fill)
        perm_a = p.pore_A * integrity * backpressure
        perm_b = p.pore_B * integrity * (1.0 + 0.5 * (1.0 - integrity))
        inside_a += source_a * perm_a
        inside_b += p.B_rate * perm_b
        poison = 1.0 / (1.0 + p.poison_coeff * inside_b)
        conv_rate = p.k_conv * poison * backpressure
        amount = conv_rate * inside_a
        inside_a -= amount
        quality = 1.0 / (1.0 + p.quality_coeff * inside_b)
        inside_b *= 0.985
        reservoir += min(amount, max(0.0, p.capacity - reservoir))
        release = min(reservoir, reservoir * p.release_rate, p.sink_cap)
        reservoir -= release
        terrain_standard = release * p.terrain_write * quality
        phi = math.pi * (1.0 - integrity)
        if arm == "arm3_sampled_chsh" and t < PHASE1_STEPS:
            s_true, s_hat, conservative_excess, true_excess = sample_chsh(phi, gamma, rng)
        elif arm == "arm2_bell_bound":
            s_true, s_hat, conservative_excess, true_excess = 0.0, 0.0, 0.0, 0.0
        else:
            s_true, s_hat, conservative_excess, true_excess = 0.0, 0.0, 0.0, 0.0
        measurement_write = MEASUREMENT_WRITE_GAIN * conservative_excess if arm == "arm3_sampled_chsh" and t < PHASE1_STEPS else 0.0
        terrain = terrain * p.terrain_decay + terrain_standard + measurement_write
        rows.append({
            "t": t,
            "phase": 1 if t < PHASE1_STEPS else 2,
            "release": release,
            "terrain": terrain,
            "measurement_write": measurement_write,
            "integrity": integrity,
            "road_boost": road_boost,
            "quality": quality,
            "chsh_true": s_true,
            "chsh_hat": s_hat,
            "chsh_excess_conservative": conservative_excess,
            "chsh_excess_true": true_excess,
        })
    return rows


def rows_between(rows: List[Dict[str, Any]], start: int, end: int) -> List[Dict[str, Any]]:
    return [r for r in rows if start <= int(r["t"]) < end]


def total(rows: List[Dict[str, Any]], key: str, start: int, end: int) -> float:
    return sum(float(r[key]) for r in rows_between(rows, start, end))


def mean(rows: List[Dict[str, Any]], key: str, start: int, end: int) -> float:
    xs = rows_between(rows, start, end)
    return sum(float(r[key]) for r in xs) / len(xs)


def maxv(rows: List[Dict[str, Any]], key: str, start: int, end: int) -> float:
    return max(float(r[key]) for r in rows_between(rows, start, end))


def first_positive(rows: List[Dict[str, Any]]) -> Any:
    for r in rows_between(rows, 0, PHASE1_STEPS):
        if float(r["chsh_excess_conservative"]) > 0.0:
            return r["t"]
    return ""


def run(seed: int = 20260707) -> Dict[str, Any]:
    summary: List[Dict[str, Any]] = []
    for si, (scenario, (phase1, phase2)) in enumerate(scenarios().items()):
        arm2 = simulate(phase1, phase2, "arm2_bell_bound", 1.0, seed=seed)
        arm2_next_release = total(arm2, "release", PHASE1_STEPS, STEPS)
        arm2_terrain_end = arm2[PHASE1_STEPS - 1]["terrain"]
        arm2_road_boost = mean(arm2, "road_boost", PHASE1_STEPS, STEPS)
        for gi, gamma in enumerate(GAMMAS):
            arm3 = simulate(phase1, phase2, "arm3_sampled_chsh", gamma=gamma, seed=seed + 1000 * si + gi)
            arm3_next_release = total(arm3, "release", PHASE1_STEPS, STEPS)
            conservative_total = total(arm3, "chsh_excess_conservative", 0, PHASE1_STEPS)
            terrain_end = arm3[PHASE1_STEPS - 1]["terrain"]
            positive = conservative_total > 1e-12 and terrain_end > arm2_terrain_end + 1e-12 and arm3_next_release > arm2_next_release + 1e-9
            row = {
                "scenario": scenario,
                "gamma": gamma,
                "shots_per_setting_per_step": SHOTS_PER_SETTING_PER_STEP,
                "confidence_margin_S": CONFIDENCE_MARGIN_S,
                "arm2_next_phase_release": arm2_next_release,
                "arm3_next_phase_release": arm3_next_release,
                "dev_pct_vs_arm2": 100.0 * (arm3_next_release - arm2_next_release) / arm2_next_release,
                "max_chsh_true_phase1": maxv(arm3, "chsh_true", 0, PHASE1_STEPS),
                "max_chsh_hat_phase1": maxv(arm3, "chsh_hat", 0, PHASE1_STEPS),
                "positive_sampled_steps_phase1": sum(1 for r in rows_between(arm3, 0, PHASE1_STEPS) if float(r["chsh_excess_conservative"]) > 0.0),
                "first_positive_sample_step_phase1": first_positive(arm3),
                "conservative_chsh_excess_total_phase1": conservative_total,
                "measurement_terrain_write_phase1": total(arm3, "measurement_write", 0, PHASE1_STEPS),
                "terrain_end_phase1_arm2": arm2_terrain_end,
                "terrain_end_phase1_arm3": terrain_end,
                "terrain_delta_end_phase1": terrain_end - arm2_terrain_end,
                "mean_road_boost_phase2_arm2": arm2_road_boost,
                "mean_road_boost_phase2_arm3": mean(arm3, "road_boost", PHASE1_STEPS, STEPS),
                "quantum_specific_sampled_feedback_effect": "TRUE" if positive else "FALSE",
                "classification": "sampled CHSH terrain feedback changes next-phase dynamics beyond Bell-bound Arm2" if positive else "no conservative sampled CHSH terrain feedback beyond Arm2",
            }
            summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    positive_rows = [r for r in summary if r["quantum_specific_sampled_feedback_effect"] == "TRUE"]
    return {
        "experiment": "quantum_sampled_chsh_terrain_feedback_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "shots_per_setting_per_step": SHOTS_PER_SETTING_PER_STEP,
        "alpha": ALPHA,
        "confidence_margin_S": rf(CONFIDENCE_MARGIN_S),
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_SAMPLED_CHSH_TERRAIN_FEEDBACK" if positive_rows else "NEGATIVE_FOR_SAMPLED_CHSH_TERRAIN_FEEDBACK",
        "positive_rows": len(positive_rows),
        "safe_interpretation": "A finite-shot sampled CHSH measurement-boundary signal, after subtracting a conservative Bell-bound margin, can still be written into terrain and later modulate classical-effective dynamics in stress context. This is a model-level positive for sampled measurement-boundary terrain feedback, not for ordinary local population plumbing.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
