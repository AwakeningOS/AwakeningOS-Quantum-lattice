#!/usr/bin/env python3
"""Quantum measurement-boundary terrain feedback probe.

Layer: quantum-audit probe

A deliberately added CHSH readout writes only Bell-violating excess into terrain
in phase 1. Phase 2 reads terrain through classical-effective road feedback. This
tests whether a quantum measurement-boundary signal can be inscribed into terrain
and later modulate classical-effective dynamics.
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


@dataclass(frozen=True)
class Params:
    A_rate: float = 2.0
    B_rate: float = 0.15
    D_rate: float = 0.02
    C_rate: float = 0.02
    pore_A: float = 0.08
    pore_B: float = 0.005
    capacity: float = 120.0
    release_rate: float = 0.035
    sink_cap: float = 999.0
    k_conv: float = 0.65
    damage_coeff: float = 0.015
    repair_coeff: float = 0.006
    stabilizer_protect: float = 0.80
    poison_coeff: float = 1.2
    quality_coeff: float = 2.0
    backpressure_strength: float = 0.65
    road_source_gain: float = 0.0
    terrain_write: float = 0.04
    terrain_decay: float = 0.985
    pulse_amp: float = 0.25


PHASE1_STEPS = 400
STEPS = 800
MEASUREMENT_WRITE_GAIN = 0.04
GAMMAS = [1.0, 0.75, 0.5, 0.25, 0.0]

I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
PAULIS = [X, Y, Z]
H = (1.0 / math.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)


def scenarios() -> Dict[str, tuple[Params, Params]]:
    return {
        "normal_context": (Params(), Params(C_rate=2.0, road_source_gain=2.0)),
        "stress_context": (Params(D_rate=0.45, C_rate=0.0), Params(C_rate=2.0, road_source_gain=2.0)),
        "storage_context": (
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9, C_rate=2.0, road_source_gain=2.0),
        ),
    }


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


def chsh_max(rho: np.ndarray) -> float:
    corr = np.zeros((3, 3), dtype=np.float64)
    for i, p in enumerate(PAULIS):
        for j, q in enumerate(PAULIS):
            corr[i, j] = float(np.real(np.trace(rho @ kron(p, q))))
    vals = np.sort(np.linalg.eigvalsh(corr.T @ corr))[::-1]
    return float(2.0 * math.sqrt(max(0.0, vals[0] + vals[1])))


def chsh_excess(phi: float, gamma: float) -> tuple[float, float]:
    s = chsh_max(rho_cb(phi, gamma))
    excess = max(0.0, s - 2.0) / (2.0 * math.sqrt(2.0) - 2.0)
    return s, excess


def simulate(phase1: Params, phase2: Params, arm: str, gamma: float = 1.0) -> List[Dict[str, Any]]:
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
        if arm == "arm3_quantum_chsh":
            chsh, excess = chsh_excess(phi, gamma)
        elif arm == "arm2_bell_bound":
            chsh, excess = 0.0, 0.0
        else:
            raise ValueError(f"unknown arm: {arm}")
        measurement_write = MEASUREMENT_WRITE_GAIN * excess if arm == "arm3_quantum_chsh" and t < PHASE1_STEPS else 0.0
        terrain = terrain * p.terrain_decay + terrain_standard + measurement_write
        rows.append(
            {
                "t": t,
                "phase": 1 if t < PHASE1_STEPS else 2,
                "release": release,
                "terrain": terrain,
                "terrain_standard": terrain_standard,
                "measurement_write": measurement_write,
                "integrity": integrity,
                "road_boost": road_boost,
                "conv_rate": conv_rate,
                "quality": quality,
                "chsh": chsh,
                "chsh_excess": excess,
            }
        )
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


def first_violation(rows: List[Dict[str, Any]]) -> Any:
    for r in rows_between(rows, 0, PHASE1_STEPS):
        if float(r["chsh"]) > 2.0 + 1e-12:
            return r["t"]
    return ""


def run(seed: int = 20260707) -> Dict[str, Any]:
    _ = np.random.default_rng(seed)
    summary: List[Dict[str, Any]] = []
    for scenario, (phase1, phase2) in scenarios().items():
        arm2 = simulate(phase1, phase2, "arm2_bell_bound", gamma=1.0)
        arm2_next_release = total(arm2, "release", PHASE1_STEPS, STEPS)
        arm2_terrain_end = arm2[PHASE1_STEPS - 1]["terrain"]
        arm2_road_boost = mean(arm2, "road_boost", PHASE1_STEPS, STEPS)
        arm2_quality = mean(arm2, "quality", PHASE1_STEPS, STEPS)
        for gamma in GAMMAS:
            arm3 = simulate(phase1, phase2, "arm3_quantum_chsh", gamma=gamma)
            arm3_next_release = total(arm3, "release", PHASE1_STEPS, STEPS)
            max_chsh = maxv(arm3, "chsh", 0, PHASE1_STEPS)
            terrain_end = arm3[PHASE1_STEPS - 1]["terrain"]
            positive = (
                max_chsh > 2.0 + 1e-12
                and total(arm3, "measurement_write", 0, PHASE1_STEPS) > 1e-12
                and terrain_end > arm2_terrain_end + 1e-12
                and arm3_next_release > arm2_next_release + 1e-9
            )
            row = {
                "scenario": scenario,
                "gamma": gamma,
                "arm2_next_phase_release": arm2_next_release,
                "arm3_next_phase_release": arm3_next_release,
                "dev_pct_vs_arm2": 100.0 * (arm3_next_release - arm2_next_release) / arm2_next_release,
                "max_chsh_phase1": max_chsh,
                "violating_steps_phase1": sum(1 for r in rows_between(arm3, 0, PHASE1_STEPS) if float(r["chsh"]) > 2.0 + 1e-12),
                "first_violation_step_phase1": first_violation(arm3),
                "chsh_excess_total_phase1": total(arm3, "chsh_excess", 0, PHASE1_STEPS),
                "measurement_terrain_write_phase1": total(arm3, "measurement_write", 0, PHASE1_STEPS),
                "terrain_end_phase1_arm2": arm2_terrain_end,
                "terrain_end_phase1_arm3": terrain_end,
                "terrain_delta_end_phase1": terrain_end - arm2_terrain_end,
                "mean_road_boost_phase2_arm2": arm2_road_boost,
                "mean_road_boost_phase2_arm3": mean(arm3, "road_boost", PHASE1_STEPS, STEPS),
                "mean_quality_phase2_arm2": arm2_quality,
                "mean_quality_phase2_arm3": mean(arm3, "quality", PHASE1_STEPS, STEPS),
                "quantum_specific_feedback_effect": "TRUE" if positive else "FALSE",
                "classification": "CHSH-excess terrain feedback changes next-phase dynamics beyond Bell-bound Arm2" if positive else "no CHSH-excess terrain feedback beyond Arm2",
            }
            summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    positive_rows = [row for row in summary if row["quantum_specific_feedback_effect"] == "TRUE"]
    return {
        "experiment": "quantum_measurement_terrain_feedback_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "phase1_steps": PHASE1_STEPS,
        "phase2_steps": STEPS - PHASE1_STEPS,
        "measurement_write_gain": MEASUREMENT_WRITE_GAIN,
        "readout": "CHSH_excess = max(0, S_CHSH - 2)/(2*sqrt(2)-2); measurement terrain write occurs only during phase 1",
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_TERRAIN_FEEDBACK" if positive_rows else "NEGATIVE_FOR_MEASUREMENT_TERRAIN_FEEDBACK",
        "positive_rows": len(positive_rows),
        "safe_interpretation": "A deliberately added CHSH measurement-boundary signal can be written into terrain and later modulate classical-effective reactor dynamics. This is a model-level positive for measurement-boundary terrain feedback, not for ordinary local population plumbing.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
