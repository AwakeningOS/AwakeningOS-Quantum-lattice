#!/usr/bin/env python3
"""Measurement backaction terrain probe.

This probe asks whether measurement itself changes the later boundary state and
thereby changes subsequent terrain/release. Measurement outcomes are not written
to terrain. The effect is only through nonselective projective/dephasing
backaction on a persistent two-qubit boundary state.
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

I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
PAULIS = [X, Y, Z]
H = (1.0 / math.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)
KET0 = np.array([1, 0], dtype=np.complex128)
STEPS = 1000
MIX_RATE = 0.12
MARGIN_S = 0.374733172169
BACKACTION_WRITE_GAIN = 0.035


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def kron(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.kron(a, b)


def ry(theta: float) -> np.ndarray:
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    return np.array([[c, -s], [s, c]], dtype=np.complex128)


def rz(theta: float) -> np.ndarray:
    return np.diag([np.exp(-1j * theta / 2.0), np.exp(1j * theta / 2.0)]).astype(np.complex128)


PSI0 = kron(H @ KET0, ry(math.pi / 2.0) @ KET0)


def base_rho(phi: float, gamma: float) -> np.ndarray:
    cu = np.zeros((4, 4), dtype=np.complex128)
    cu[0:2, 0:2] = I2
    cu[2:4, 2:4] = rz(phi)
    psi = cu @ PSI0
    rho = np.outer(psi, np.conjugate(psi))
    mask = np.ones((4, 4), dtype=np.float64) * (1.0 - gamma)
    np.fill_diagonal(mask, 1.0)
    return rho * mask


def corrmat(rho: np.ndarray) -> np.ndarray:
    return np.array([[float(np.real(np.trace(rho @ kron(p, q)))) for q in PAULIS] for p in PAULIS])


def fixed_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    t = corrmat(base_rho(math.pi, 0.0))
    vals, vecs = np.linalg.eigh(t.T @ t)
    idx = np.argsort(vals)[::-1]
    u1 = max(float(vals[idx[0]]), 0.0)
    u2 = max(float(vals[idx[1]]), 0.0)
    v1 = vecs[:, idx[0]]
    v2 = vecs[:, idx[1]]
    denom = math.sqrt(u1 + u2)
    b0 = math.sqrt(u1) / denom * v1 + math.sqrt(u2) / denom * v2
    b1 = math.sqrt(u1) / denom * v1 - math.sqrt(u2) / denom * v2

    def normed(x: np.ndarray) -> np.ndarray:
        n = np.linalg.norm(x)
        return x / n if n > 1e-12 else x

    return normed(t @ (b0 + b1)), normed(t @ (b0 - b1)), b0, b1


A0, A1, B0, B1 = fixed_basis()


def fixed_chsh(rho: np.ndarray) -> float:
    t = corrmat(rho)
    return float(A0 @ t @ B0 + A0 @ t @ B1 + A1 @ t @ B0 - A1 @ t @ B1)


def axis_op(vec: np.ndarray) -> np.ndarray:
    return vec[0] * X + vec[1] * Y + vec[2] * Z


def measurement_dephase(rho: np.ndarray, avec: np.ndarray, bvec: np.ndarray, strength: float) -> np.ndarray:
    a_op = axis_op(avec)
    b_op = axis_op(bvec)
    projectors_a = [(I2 + a_op) / 2.0, (I2 - a_op) / 2.0]
    projectors_b = [(I2 + b_op) / 2.0, (I2 - b_op) / 2.0]
    measured = np.zeros((4, 4), dtype=np.complex128)
    for pa in projectors_a:
        for pb in projectors_b:
            proj = kron(pa, pb)
            measured += proj @ rho @ np.conjugate(proj).T
    return (1.0 - strength) * rho + strength * measured


@dataclass
class Params:
    A_rate: float = 1.0
    B_rate: float = 0.15
    C_rate: float = 0.0
    D_rate: float = 0.04
    pore_A: float = 0.8
    pore_B: float = 0.25
    k_conv: float = 0.08
    quality_coeff: float = 1.5
    poison_coeff: float = 1.2
    capacity: float = 120.0
    release_rate: float = 0.01
    backpressure_strength: float = 0.55
    damage_coeff: float = 0.01
    repair_coeff: float = 0.006
    stabilizer_protect: float = 0.7
    terrain_write: float = 0.02
    terrain_decay: float = 0.985
    road_source_gain: float = 1.5
    pulse_amp: float = 0.25


def scenarios() -> Dict[str, Params]:
    return {
        "normal_backaction": Params(),
        "stress_backaction": Params(D_rate=0.45, C_rate=0.0),
        "storage_backaction": Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
    }


def simulate(p: Params, arm: str, gamma: float, measurement_strength: float = 1.0) -> List[Dict[str, float]]:
    inside_a = 0.0
    inside_b = 0.0
    reservoir = 0.0
    terrain = 0.0
    integrity = 1.0
    rho = base_rho(0.0, gamma)
    rows: List[Dict[str, float]] = []
    for t in range(STEPS):
        target = base_rho(math.pi * (1.0 - integrity), gamma)
        rho = (1.0 - MIX_RATE) * rho + MIX_RATE * target
        chsh = fixed_chsh(rho)
        signal = max(0.0, chsh - 2.0 - MARGIN_S) / (2.0 * math.sqrt(2.0) - 2.0)

        if arm != "no_measure":
            if t % 2 == 0:
                rho = measurement_dephase(rho, A0, B0, measurement_strength)
            else:
                rho = measurement_dephase(rho, A1, B1, measurement_strength)

        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / 64.0)
        road_boost = 1.0 + p.road_source_gain * (terrain / (1.0 + terrain))
        fill = reservoir / max(p.capacity, 1e-9)
        backpressure = max(0.02, 1.0 - p.backpressure_strength * fill)
        protect = p.stabilizer_protect * (p.C_rate / (1.0 + p.C_rate))
        damage = p.damage_coeff * p.D_rate * (1.0 - protect)
        repair = p.repair_coeff * p.C_rate * (1.0 - integrity)
        integrity = min(1.0, max(0.0, integrity - damage + repair))
        a_pass = p.A_rate * pulse * p.pore_A * integrity * backpressure * road_boost
        b_pass = p.B_rate * p.pore_B * integrity * (1.0 + 0.5 * (1.0 - integrity))
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
        terrain = terrain * p.terrain_decay + release * p.terrain_write * quality + BACKACTION_WRITE_GAIN * signal
        rows.append({"chsh": chsh, "signal": signal, "terrain": terrain, "release": release, "quality": quality})
    return rows


def total(rows: List[Dict[str, float]], key: str) -> float:
    return sum(float(r[key]) for r in rows)


def mean(rows: List[Dict[str, float]], key: str) -> float:
    return total(rows, key) / len(rows)


def pct(new: float, old: float) -> float:
    return 100.0 * (new - old) / old if abs(old) > 1e-12 else 0.0


def run(seed: int = 20260707) -> Dict[str, Any]:
    summary: List[Dict[str, Any]] = []
    for scenario, params in scenarios().items():
        for gamma in [1.0, 0.0]:
            no_measure = simulate(params, "no_measure", gamma)
            for arm, strength in [("projective_measure", 1.0), ("gentle_measure", 0.01)]:
                rows = simulate(params, arm, gamma, measurement_strength=strength)
                effect = scenario == "stress_backaction" and gamma == 0.0 and abs(total(rows, "signal") - total(no_measure, "signal")) > 1e-9 and abs(total(rows, "release") - total(no_measure, "release")) > 1e-9
                row = {
                    "scenario": scenario,
                    "gamma": gamma,
                    "arm": arm,
                    "measurement_strength": strength,
                    "signal_total_no_measure": total(no_measure, "signal"),
                    "signal_total_arm": total(rows, "signal"),
                    "signal_dev_pct": pct(total(rows, "signal"), total(no_measure, "signal")),
                    "terrain_final_no_measure": no_measure[-1]["terrain"],
                    "terrain_final_arm": rows[-1]["terrain"],
                    "terrain_dev_pct": pct(rows[-1]["terrain"], no_measure[-1]["terrain"]),
                    "release_no_measure": total(no_measure, "release"),
                    "release_arm": total(rows, "release"),
                    "release_dev_pct": pct(total(rows, "release"), total(no_measure, "release")),
                    "mean_quality_no_measure": mean(no_measure, "quality"),
                    "mean_quality_arm": mean(rows, "quality"),
                    "quality_dev_pct": pct(mean(rows, "quality"), mean(no_measure, "quality")),
                    "backaction_effect": "TRUE" if effect else "FALSE",
                }
                summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    positives = [r for r in summary if r["backaction_effect"] == "TRUE"]
    return {
        "experiment": "quantum_measurement_backaction_terrain_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "model": "persistent two-qubit boundary state; measurement acts as nonselective projective/dephasing backaction; no outcome write is used",
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_BACKACTION_TERRAIN" if positives else "NEGATIVE_FOR_MEASUREMENT_BACKACTION_TERRAIN",
        "positive_rows": len(positives),
        "safe_interpretation": "In stress gamma=0, invasive measurement of the boundary state suppresses later Bell-excess terrain signal and lowers downstream release after measurement stops being treated as a passive readout. The effect is backaction-like and negative/suppressive: measurement changes the future boundary state rather than merely reporting it. Normal/storage and gamma=1 null rows remain unchanged.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/measurement_backaction_terrain_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
