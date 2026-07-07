#!/usr/bin/env python3
"""CHSH-free natural observable probe.

Adversarial inverted design: no CHSH, Bell excess, entanglement, negativity, or
joint witness is allowed in the reactor output rule. The reactor may use only
local one-body reduced-state observables. The decisive control is a separable
product of the exact reduced local states.
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
H = (1.0 / math.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)
KET0 = np.array([1, 0], dtype=np.complex128)
STEPS = 800


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


def ptrace_c(rho: np.ndarray) -> np.ndarray:
    return np.array([[rho[0, 0] + rho[1, 1], rho[0, 2] + rho[1, 3]], [rho[2, 0] + rho[3, 1], rho[2, 2] + rho[3, 3]]], dtype=np.complex128)


def ptrace_b(rho: np.ndarray) -> np.ndarray:
    return np.array([[rho[0, 0] + rho[2, 2], rho[0, 1] + rho[2, 3]], [rho[1, 0] + rho[3, 2], rho[1, 1] + rho[3, 3]]], dtype=np.complex128)


def product_reduced(rho: np.ndarray) -> np.ndarray:
    return kron(ptrace_c(rho), ptrace_b(rho))


def diagonal_same_populations(rho: np.ndarray) -> np.ndarray:
    return np.diag(np.diag(rho)).astype(np.complex128)


def expect(rho: np.ndarray, op: np.ndarray) -> float:
    return float(np.real(np.trace(rho @ op)))


def local_features(rho: np.ndarray) -> Dict[str, float]:
    cx = expect(rho, kron(X, I2))
    cy = expect(rho, kron(Y, I2))
    cz = expect(rho, kron(Z, I2))
    bx = expect(rho, kron(I2, X))
    by = expect(rho, kron(I2, Y))
    bz = expect(rho, kron(I2, Z))
    p_b1 = (1.0 - bz) / 2.0
    p_c1 = (1.0 - cz) / 2.0
    local_alignment = 0.5 + 0.22 * bx + 0.14 * cx - 0.08 * abs(by) - 0.04 * abs(cy)
    local_alignment = max(0.0, min(1.0, local_alignment))
    return {"cx": cx, "cy": cy, "cz": cz, "bx": bx, "by": by, "bz": bz, "p_b1": p_b1, "p_c1": p_c1, "local_alignment": local_alignment}


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
        "normal_natural": Params(),
        "stress_natural": Params(D_rate=0.45, C_rate=0.0),
        "storage_natural": Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
        "contaminated_stress_natural": Params(D_rate=0.45, C_rate=0.0, B_rate=0.45),
    }


def select_rho(phi: float, gamma: float, arm: str) -> np.ndarray:
    rho = base_rho(phi, gamma)
    if arm == "arm3_quantum":
        return rho
    if arm == "arm2_reduced_product":
        return product_reduced(rho)
    if arm == "arm2_diagonal":
        return diagonal_same_populations(rho)
    raise ValueError(f"unknown arm: {arm}")


def simulate(p: Params, gamma: float, arm: str, replay_trace: List[Dict[str, float]] | None = None) -> tuple[List[Dict[str, float]], List[Dict[str, float]]]:
    inside_a = 0.0
    inside_b = 0.0
    reservoir = 0.0
    terrain = 0.0
    integrity = 1.0
    rows: List[Dict[str, float]] = []
    trace: List[Dict[str, float]] = []
    for t in range(STEPS):
        phi = math.pi * (1.0 - integrity)
        if arm == "matched_replay":
            if replay_trace is None:
                raise ValueError("matched_replay requires replay_trace")
            f = replay_trace[t]
        else:
            f = local_features(select_rho(phi, gamma, arm))

        align = f["local_alignment"]
        a_gate = 0.90 + 0.25 * align
        b_gate = max(0.20, 1.05 - 0.35 * align)
        d_gate = max(0.25, 1.05 - 0.30 * align)

        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / 64.0)
        road_boost = 1.0 + p.road_source_gain * (terrain / (1.0 + terrain))
        fill = reservoir / max(p.capacity, 1e-9)
        backpressure = max(0.02, 1.0 - p.backpressure_strength * fill)
        protect = p.stabilizer_protect * (p.C_rate / (1.0 + p.C_rate))
        d_pass = p.D_rate * 0.04 * d_gate
        damage = p.damage_coeff * d_pass * (1.0 - protect) * 25.0
        repair = p.repair_coeff * p.C_rate * (1.0 - integrity)
        integrity = min(1.0, max(0.0, integrity - damage + repair))
        a_pass = p.A_rate * pulse * p.pore_A * integrity * backpressure * road_boost * a_gate
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
        rows.append({"t": t, "release": release, "quality": quality, "terrain": terrain, "integrity": integrity, "a_pass": a_pass, "b_pass": b_pass, "d_pass": d_pass, "local_alignment": align})
        trace.append(f)
    return rows, trace


def total(rows: List[Dict[str, float]], key: str) -> float:
    return sum(float(r[key]) for r in rows)


def mean(rows: List[Dict[str, float]], key: str) -> float:
    return total(rows, key) / len(rows)


def pct(new: float, old: float) -> float:
    return 100.0 * (new - old) / old if abs(old) > 1e-12 else 0.0


def run(seed: int = 20260707) -> Dict[str, Any]:
    summary: List[Dict[str, Any]] = []
    for scenario, params in scenarios().items():
        for gamma in [1.0, 0.5, 0.25, 0.0]:
            arm3, trace = simulate(params, gamma, "arm3_quantum")
            reduced, _ = simulate(params, gamma, "arm2_reduced_product")
            diagonal, _ = simulate(params, gamma, "arm2_diagonal")
            replay, _ = simulate(params, gamma, "matched_replay", replay_trace=trace)

            max_abs_reduced = 0.0
            max_abs_replay = 0.0
            max_abs_diagonal = 0.0
            for key in ["release", "quality", "terrain", "integrity", "a_pass", "b_pass", "d_pass"]:
                max_abs_reduced = max(max_abs_reduced, abs(total(arm3, key) - total(reduced, key)))
                max_abs_replay = max(max_abs_replay, abs(total(arm3, key) - total(replay, key)))
                max_abs_diagonal = max(max_abs_diagonal, abs(total(arm3, key) - total(diagonal, key)))

            row = {
                "scenario": scenario,
                "gamma": gamma,
                "release_arm3": total(arm3, "release"),
                "release_arm2_reduced": total(reduced, "release"),
                "release_dev_pct_arm3_vs_reduced": pct(total(arm3, "release"), total(reduced, "release")),
                "quality_mean_arm3": mean(arm3, "quality"),
                "quality_mean_arm2_reduced": mean(reduced, "quality"),
                "quality_dev_pct_arm3_vs_reduced": pct(mean(arm3, "quality"), mean(reduced, "quality")),
                "terrain_final_arm3": arm3[-1]["terrain"],
                "terrain_final_arm2_reduced": reduced[-1]["terrain"],
                "terrain_dev_pct_arm3_vs_reduced": pct(arm3[-1]["terrain"], reduced[-1]["terrain"]),
                "a_pass_dev_pct_arm3_vs_reduced": pct(total(arm3, "a_pass"), total(reduced, "a_pass")),
                "b_leak_dev_pct_arm3_vs_reduced": pct(total(arm3, "b_pass"), total(reduced, "b_pass")),
                "d_pass_dev_pct_arm3_vs_reduced": pct(total(arm3, "d_pass"), total(reduced, "d_pass")),
                "max_abs_metric_diff_vs_reduced": max_abs_reduced,
                "max_abs_metric_diff_vs_replay": max_abs_replay,
                "diagonal_control_release_dev_pct": pct(total(arm3, "release"), total(diagonal, "release")),
                "diagonal_control_max_abs_metric_diff": max_abs_diagonal,
                "irreproducible_by_reduced_arm2": "TRUE" if max_abs_reduced > 1e-9 else "FALSE",
                "classification": "NEGATIVE: natural CHSH-free observables are reproduced by reduced/product Arm2" if max_abs_reduced <= 1e-9 else "POSITIVE: reduced/product Arm2 failed",
            }
            summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})

    return {
        "experiment": "quantum_chsh_free_natural_observable_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit inverted/adversarial probe",
        "seed": seed,
        "design": "CHSH/entanglement/negativity are not used in output definitions; reactor gates depend only on local reduced one-body observables.",
        "summary": summary,
        "verdict": "NEGATIVE_CHSH_FREE_NATURAL_OBSERVABLE_REDUCED_ARM2_REPRODUCES",
        "positive_rows": sum(1 for r in summary if r["irreproducible_by_reduced_arm2"] == "TRUE"),
        "reduced_arm2_max_abs_diff_overall": max(float(r["max_abs_metric_diff_vs_reduced"]) for r in summary),
        "matched_replay_max_abs_diff_overall": max(float(r["max_abs_metric_diff_vs_replay"]) for r in summary),
        "diagonal_control_max_abs_diff_overall": max(float(r["diagonal_control_max_abs_metric_diff"]) for r in summary),
        "safe_interpretation": "When CHSH/entanglement/negativity are excluded from output definitions and reactor dynamics use only natural local one-body boundary observables, the quantum Arm3 is exactly reproduced by a separable product of its reduced local states across all tested contexts and gamma values. This supports the auditor critique: previous measurement-boundary positives were constructed CHSH-switch studies, not evidence of naturally irreducible quantum microreactor dynamics.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/chsh_free_natural_observable_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
