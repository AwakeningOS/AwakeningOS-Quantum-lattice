#!/usr/bin/env python3
"""Fixed-basis adaptive measurement feedback probe.

This tightens the adaptive feedback line by removing per-step CHSH basis
optimization. A single CHSH basis is calibrated once at phi=pi, gamma=0 and reused
for every step, context, and gamma value.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from quantum_sampled_chsh_terrain_feedback_probe import (
    ALPHA,
    CONFIDENCE_MARGIN_S,
    GAMMAS,
    MEASUREMENT_WRITE_GAIN,
    SHOTS_PER_SETTING_PER_STEP,
    Params,
)

PHASE1_STEPS = 400
PHASE2_STEPS = 400
PHASE3_STEPS = 400
STEPS = PHASE1_STEPS + PHASE2_STEPS + PHASE3_STEPS
ADAPTIVE_PHASE_GAIN = 1.25
ADAPTIVE_GATE_GAIN = 0.18

I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
PAULIS = [X, Y, Z]
H = (1.0 / math.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def kron(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.kron(a, b)


def ry(theta: float) -> np.ndarray:
    c, s = math.cos(theta / 2.0), math.sin(theta / 2.0)
    return np.array([[c, -s], [s, c]], dtype=np.complex128)


def rz(theta: float) -> np.ndarray:
    return np.diag([np.exp(-1j * theta / 2.0), np.exp(1j * theta / 2.0)]).astype(np.complex128)


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


def fixed_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    t = correlation_matrix(rho_cb(math.pi, 0.0))
    vals, vecs = np.linalg.eigh(t.T @ t)
    idx = np.argsort(vals)[::-1]
    u1 = max(float(vals[idx[0]]), 0.0)
    u2 = max(float(vals[idx[1]]), 0.0)
    v1 = vecs[:, idx[0]]
    v2 = vecs[:, idx[1]]
    denom = math.sqrt(u1 + u2)
    c, s = math.sqrt(u1) / denom, math.sqrt(u2) / denom
    b0 = c * v1 + s * v2
    b1 = c * v1 - s * v2

    def normed(x: np.ndarray) -> np.ndarray:
        n = np.linalg.norm(x)
        return x / n if n > 1e-12 else x

    a0 = normed(t @ (b0 + b1))
    a1 = normed(t @ (b0 - b1))
    return a0, a1, b0, b1


FIXED_A0, FIXED_A1, FIXED_B0, FIXED_B1 = fixed_basis()


def fixed_chsh(phi: float, gamma: float) -> tuple[list[float], float]:
    t = correlation_matrix(rho_cb(phi, gamma))
    e00 = float(FIXED_A0 @ t @ FIXED_B0)
    e01 = float(FIXED_A0 @ t @ FIXED_B1)
    e10 = float(FIXED_A1 @ t @ FIXED_B0)
    e11 = float(FIXED_A1 @ t @ FIXED_B1)
    return [e00, e01, e10, e11], e00 + e01 + e10 - e11


def sample_fixed_chsh(phi: float, gamma: float, rng: np.random.Generator) -> tuple[float, float, float]:
    corr, s_true = fixed_chsh(phi, gamma)
    sampled: list[float] = []
    for e in corr:
        p = (1.0 + max(-1.0, min(1.0, e))) / 2.0
        k = rng.binomial(SHOTS_PER_SETTING_PER_STEP, p)
        sampled.append(2.0 * k / SHOTS_PER_SETTING_PER_STEP - 1.0)
    s_hat = sampled[0] + sampled[1] + sampled[2] - sampled[3]
    conservative = max(0.0, s_hat - 2.0 - CONFIDENCE_MARGIN_S) / (2.0 * math.sqrt(2.0) - 2.0)
    return s_true, s_hat, conservative


def scenarios() -> Dict[str, tuple[Params, Params, Params]]:
    return {
        "normal_fixed_adaptive": (Params(), Params(C_rate=2.0, D_rate=0.02, road_source_gain=2.0), Params(C_rate=0.0, D_rate=0.45, road_source_gain=2.0)),
        "stress_fixed_adaptive": (Params(D_rate=0.45, C_rate=0.0), Params(C_rate=2.0, D_rate=0.02, road_source_gain=2.0), Params(C_rate=0.0, D_rate=0.45, road_source_gain=2.0)),
        "storage_fixed_adaptive": (
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9, C_rate=2.0, D_rate=0.02, road_source_gain=2.0),
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9, C_rate=0.0, D_rate=0.45, road_source_gain=2.0),
        ),
    }


def simulate(phase1: Params, phase2: Params, phase3: Params, arm: str, gamma: float, seed: int, replay_writes: List[float] | None = None) -> tuple[List[Dict[str, Any]], List[float]]:
    rng = np.random.default_rng(seed)
    inside_a = inside_b = reservoir = terrain = 0.0
    integrity = 1.0
    rows: List[Dict[str, Any]] = []
    writes: List[float] = []
    for t in range(STEPS):
        if t < PHASE1_STEPS:
            p, phase = phase1, 1
        elif t < PHASE1_STEPS + PHASE2_STEPS:
            p, phase = phase2, 2
        else:
            p, phase = phase3, 3
        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / 64.0)
        road_boost = 1.0 + p.road_source_gain * (terrain / (1.0 + terrain))
        phi_pre = math.pi * (1.0 - integrity)
        adaptive_shift = ADAPTIVE_PHASE_GAIN * (terrain / (1.0 + terrain)) if phase >= 2 else 0.0
        adaptive_gate = 1.0
        adaptive_hat = 0.0
        adaptive_excess = 0.0
        if arm in {"arm3_fixed_adaptive_chsh", "matched_classical_replay"} and phase >= 2:
            _, adaptive_hat, adaptive_excess = sample_fixed_chsh(min(math.pi, phi_pre + adaptive_shift), gamma, rng)
            adaptive_gate = 1.0 + ADAPTIVE_GATE_GAIN * adaptive_excess
        source_a = p.A_rate * pulse * road_boost * adaptive_gate
        protect = p.stabilizer_protect * (p.C_rate / (1.0 + p.C_rate))
        damage = p.damage_coeff * p.D_rate * (1.0 - protect)
        repair = p.repair_coeff * p.C_rate * (1.0 - integrity)
        integrity = min(1.0, max(0.0, integrity - damage + repair))
        fill = reservoir / max(p.capacity, 1e-9)
        backpressure = max(0.02, 1.0 - p.backpressure_strength * fill)
        inside_a += source_a * p.pore_A * integrity * backpressure
        inside_b += p.B_rate * p.pore_B * integrity * (1.0 + 0.5 * (1.0 - integrity))
        poison = 1.0 / (1.0 + p.poison_coeff * inside_b)
        amount = p.k_conv * poison * backpressure * inside_a
        inside_a -= amount
        quality = 1.0 / (1.0 + p.quality_coeff * inside_b)
        inside_b *= 0.985
        reservoir += min(amount, max(0.0, p.capacity - reservoir))
        release = min(reservoir, reservoir * p.release_rate, p.sink_cap)
        reservoir -= release
        measurement_write = 0.0
        phase1_hat = 0.0
        phase1_excess = 0.0
        if phase == 1:
            phi = math.pi * (1.0 - integrity)
            if arm == "arm3_fixed_adaptive_chsh":
                _, phase1_hat, phase1_excess = sample_fixed_chsh(phi, gamma, rng)
                measurement_write = MEASUREMENT_WRITE_GAIN * phase1_excess
            elif arm == "matched_classical_replay":
                _ = sample_fixed_chsh(phi, gamma, rng)
                measurement_write = replay_writes[t] if replay_writes is not None else 0.0
        terrain = terrain * p.terrain_decay + release * p.terrain_write * quality + measurement_write
        writes.append(measurement_write)
        rows.append({
            "t": t, "phase": phase, "release": release, "terrain": terrain,
            "measurement_write": measurement_write, "phase1_chsh_hat": phase1_hat,
            "phase1_conservative_excess": phase1_excess, "adaptive_chsh_hat": adaptive_hat,
            "adaptive_conservative_excess": adaptive_excess, "adaptive_gate": adaptive_gate,
        })
    return rows, writes


def phase_rows(rows: List[Dict[str, Any]], phase: int) -> List[Dict[str, Any]]:
    return [r for r in rows if int(r["phase"]) == phase]


def total(rows: List[Dict[str, Any]], key: str, phase: int) -> float:
    return sum(float(r[key]) for r in phase_rows(rows, phase))


def mean(rows: List[Dict[str, Any]], key: str, phase: int) -> float:
    xs = phase_rows(rows, phase)
    return sum(float(r[key]) for r in xs) / len(xs)


def maxv(rows: List[Dict[str, Any]], key: str, phase: int) -> float:
    return max(float(r[key]) for r in phase_rows(rows, phase))


def run(seed: int = 20260707) -> Dict[str, Any]:
    summary: List[Dict[str, Any]] = []
    for si, (scenario, phases) in enumerate(scenarios().items()):
        phase1, phase2, phase3 = phases
        arm2, _ = simulate(phase1, phase2, phase3, "arm2_bell_bound", 1.0, seed)
        for gi, gamma in enumerate(GAMMAS):
            arm3, writes = simulate(phase1, phase2, phase3, "arm3_fixed_adaptive_chsh", gamma, seed + 1000 * si + gi)
            replay, _ = simulate(phase1, phase2, phase3, "matched_classical_replay", gamma, seed + 1000 * si + gi, writes)
            rel2_a2, rel2_a3 = total(arm2, "release", 2), total(arm3, "release", 2)
            rel3_a2, rel3_a3 = total(arm2, "release", 3), total(arm3, "release", 3)
            positive = total(arm3, "measurement_write", 1) > 1e-12 and (maxv(arm3, "adaptive_conservative_excess", 2) > 0.0 or maxv(arm3, "adaptive_conservative_excess", 3) > 0.0) and rel2_a3 > rel2_a2 + 1e-9
            row = {
                "scenario": scenario,
                "gamma": gamma,
                "phase1_measurement_write": total(arm3, "measurement_write", 1),
                "terrain_delta_end_phase1": arm3[PHASE1_STEPS - 1]["terrain"] - arm2[PHASE1_STEPS - 1]["terrain"],
                "terrain_delta_end_phase2": arm3[PHASE1_STEPS + PHASE2_STEPS - 1]["terrain"] - arm2[PHASE1_STEPS + PHASE2_STEPS - 1]["terrain"],
                "phase1_positive_sampled_steps": sum(1 for r in phase_rows(arm3, 1) if float(r["phase1_conservative_excess"]) > 0.0),
                "phase2_adaptive_positive_steps": sum(1 for r in phase_rows(arm3, 2) if float(r["adaptive_conservative_excess"]) > 0.0),
                "phase3_adaptive_positive_steps": sum(1 for r in phase_rows(arm3, 3) if float(r["adaptive_conservative_excess"]) > 0.0),
                "max_phase1_chsh_hat": maxv(arm3, "phase1_chsh_hat", 1),
                "max_adaptive_chsh_hat_phase2": maxv(arm3, "adaptive_chsh_hat", 2),
                "max_adaptive_chsh_hat_phase3": maxv(arm3, "adaptive_chsh_hat", 3),
                "mean_adaptive_gate_phase2_arm2": mean(arm2, "adaptive_gate", 2),
                "mean_adaptive_gate_phase2_arm3": mean(arm3, "adaptive_gate", 2),
                "mean_adaptive_gate_phase3_arm2": mean(arm2, "adaptive_gate", 3),
                "mean_adaptive_gate_phase3_arm3": mean(arm3, "adaptive_gate", 3),
                "arm2_release_phase2": rel2_a2,
                "arm3_release_phase2": rel2_a3,
                "arm3_dev_pct_release_phase2": 100.0 * (rel2_a3 - rel2_a2) / rel2_a2,
                "arm2_release_phase3": rel3_a2,
                "arm3_release_phase3": rel3_a3,
                "arm3_dev_pct_release_phase3": 100.0 * (rel3_a3 - rel3_a2) / rel3_a2,
                "matched_replay_phase2_diff_vs_arm3": total(replay, "release", 2) - rel2_a3,
                "matched_replay_phase3_diff_vs_arm3": total(replay, "release", 3) - rel3_a3,
                "fixed_basis_adaptive_effect_beyond_bell_bound_arm2": "TRUE" if positive else "FALSE",
            }
            summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    positives = [r for r in summary if r["fixed_basis_adaptive_effect_beyond_bell_bound_arm2"] == "TRUE"]
    return {
        "experiment": "quantum_fixed_basis_adaptive_feedback_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "fixed_basis": "pre-calibrated once at phi=pi; no per-step optimization",
        "shots_per_setting_per_step": SHOTS_PER_SETTING_PER_STEP,
        "alpha": ALPHA,
        "confidence_margin_S": rf(CONFIDENCE_MARGIN_S),
        "adaptive_phase_gain": ADAPTIVE_PHASE_GAIN,
        "adaptive_gate_gain": ADAPTIVE_GATE_GAIN,
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_FIXED_BASIS_ADAPTIVE_FEEDBACK" if positives else "NEGATIVE_FOR_FIXED_BASIS_ADAPTIVE_FEEDBACK",
        "positive_rows": len(positives),
        "safe_interpretation": "A fixed-basis finite-shot CHSH measurement boundary, pre-calibrated once rather than optimized per step, can still write terrain memory and shift later adaptive measurement gates in stress context. Normal/storage later adaptive activity is not counted positive without phase-1 Bell-excess terrain inscription. This remains model-level and not hardware or ordinary local population plumbing.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
