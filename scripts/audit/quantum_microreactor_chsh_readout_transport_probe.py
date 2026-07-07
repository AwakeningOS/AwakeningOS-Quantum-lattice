#!/usr/bin/env python3
"""CHSH-readout transport probe for the information microreactor line.

Layer: quantum-audit probe

This script adds a deliberately nonlocal / noncommutative readout component. The
reactor release multiplier is driven by a CHSH witness rather than local branch
population. Classical/local correlations are bounded by S_CHSH <= 2, which maps
to the release ceiling yb = 1/sqrt(2). Only S_CHSH > 2 can exceed that ceiling.
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


def scenarios() -> Dict[str, Params]:
    return {
        "normal": Params(),
        "stress": Params(D_rate=0.45, C_rate=0.0),
        "storage_heavy": Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
    }


STEPS = 800
BURN = 200
GAMMAS = [1.0, 0.75, 0.5, 0.25, 0.0]
I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
PAULIS = [X, Y, Z]


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def ry(theta: float) -> np.ndarray:
    c, s = math.cos(theta / 2.0), math.sin(theta / 2.0)
    return np.array([[c, -s], [s, c]], dtype=np.complex128)


def rz(theta: float) -> np.ndarray:
    return np.array([[np.exp(-1j * theta / 2.0), 0], [0, np.exp(1j * theta / 2.0)]], dtype=np.complex128)


H = (1.0 / math.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)


def kron(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.kron(a, b)


def dephase(rho: np.ndarray, gamma: float) -> np.ndarray:
    mask = np.ones((4, 4), dtype=np.float64) * (1.0 - gamma) + np.eye(4)
    mask[np.diag_indices(4)] = 1.0
    return rho * mask


def rho_cb(phi: float, gamma: float) -> np.ndarray:
    psi = kron(H @ np.array([1, 0], dtype=np.complex128), ry(math.pi / 2.0) @ np.array([1, 0], dtype=np.complex128))
    rho = np.outer(psi, np.conjugate(psi))
    cu = np.zeros((4, 4), dtype=np.complex128)
    cu[0:2, 0:2] = I2
    cu[2:4, 2:4] = rz(phi)
    rho = cu @ rho @ np.conjugate(cu).T
    return dephase(rho, gamma)


def partial_transpose_b(rho: np.ndarray) -> np.ndarray:
    pt = np.zeros_like(rho)
    for c in range(2):
        for cp in range(2):
            for b in range(2):
                for bp in range(2):
                    pt[2 * c + b, 2 * cp + bp] = rho[2 * c + bp, 2 * cp + b]
    return pt


def negativity(rho: np.ndarray) -> float:
    eig = np.linalg.eigvalsh((partial_transpose_b(rho) + np.conjugate(partial_transpose_b(rho)).T) / 2.0)
    return float(sum(abs(v) for v in eig if v < 0.0))


def chsh_max(rho: np.ndarray) -> float:
    t = np.zeros((3, 3), dtype=np.float64)
    for i, p in enumerate(PAULIS):
        for j, q in enumerate(PAULIS):
            t[i, j] = float(np.real(np.trace(rho @ kron(p, q))))
    vals = np.linalg.eigvalsh(t.T @ t)
    vals = np.sort(vals)[::-1]
    return float(2.0 * math.sqrt(max(0.0, vals[0] + vals[1])))


def chsh_readout(phi: float, gamma: float) -> tuple[float, float, float, bool]:
    rho = rho_cb(phi, gamma)
    s = chsh_max(rho)
    n = negativity(rho)
    yb = max(2.0, s) / (2.0 * math.sqrt(2.0))
    return yb, s, n, s > 2.0 + 1e-12


def simulate(p: Params, mode: str, gamma: float = 1.0) -> List[Dict[str, Any]]:
    inside_a = 0.0
    inside_b = 0.0
    reservoir = 0.0
    terrain = 0.0
    integrity = 1.0
    rows: List[Dict[str, Any]] = []
    for t in range(STEPS):
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
        phi = math.pi * (1.0 - integrity)
        if mode == "classical_ceiling":
            yb = 1.0 / math.sqrt(2.0)
            s = 2.0
            neg = 0.0
            violation = False
        elif mode == "quantum_chsh":
            yb, s, neg, violation = chsh_readout(phi, gamma)
        else:
            raise ValueError(mode)
        inside_a -= amount
        quality = 1.0 / (1.0 + p.quality_coeff * inside_b)
        inside_b *= 0.985
        available = max(0.0, p.capacity - reservoir)
        reservoir += min(amount * yb, available)
        release = min(reservoir, reservoir * p.release_rate, p.sink_cap)
        reservoir -= release
        terrain = terrain * p.terrain_decay + release * p.terrain_write * quality
        rows.append({"t": t, "release": release, "integrity": integrity, "phi": phi, "chsh": s, "negativity": neg, "yb": yb, "violation": int(violation)})
    return rows


def post(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return rows[BURN:]


def total_release(rows: List[Dict[str, Any]]) -> float:
    return sum(r["release"] for r in post(rows))


def mean(rows: List[Dict[str, Any]], key: str) -> float:
    p = post(rows)
    return sum(float(r[key]) for r in p) / len(p)


def maxv(rows: List[Dict[str, Any]], key: str) -> float:
    return max(float(r[key]) for r in post(rows))


def first_violation_step(rows: List[Dict[str, Any]]) -> Any:
    for r in rows:
        if r["violation"]:
            return r["t"]
    return ""


def run(seed: int = 20260707) -> Dict[str, Any]:
    _ = np.random.default_rng(seed)
    summary: List[Dict[str, Any]] = []
    for scenario, p in scenarios().items():
        base_rows = simulate(p, "classical_ceiling")
        base_release = total_release(base_rows)
        for gamma in GAMMAS:
            qrows = simulate(p, "quantum_chsh", gamma)
            qrelease = total_release(qrows)
            max_chsh = maxv(qrows, "chsh")
            row = {
                "scenario": scenario,
                "gamma": gamma,
                "classical_ceiling_release": base_release,
                "quantum_release": qrelease,
                "dev_pct_vs_classical_ceiling": 100.0 * (qrelease - base_release) / base_release,
                "mean_chsh": mean(qrows, "chsh"),
                "max_chsh": max_chsh,
                "violating_steps_post_burn": sum(int(r["violation"]) for r in post(qrows)),
                "first_violation_step": first_violation_step(qrows),
                "mean_negativity": mean(qrows, "negativity"),
                "max_negativity": maxv(qrows, "negativity"),
                "passes_chsh_violation": "TRUE" if max_chsh > 2.0 + 1e-12 else "FALSE",
                "exceeds_classical_release_ceiling": "TRUE" if qrelease > base_release + 1e-9 else "FALSE",
                "quantum_specific_transport_effect": "TRUE" if (max_chsh > 2.0 + 1e-12 and qrelease > base_release + 1e-9) else "FALSE",
            }
            summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    positive = [r for r in summary if r["quantum_specific_transport_effect"] == "TRUE"]
    return {
        "experiment": "quantum_microreactor_chsh_readout_transport_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "readout": "yb = max(2, S_CHSH) / (2*sqrt(2)); classical ceiling yb=1/sqrt(2)",
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_CHSH_READOUT_TRANSPORT" if positive else "NEGATIVE_FOR_CHSH_READOUT_TRANSPORT",
        "positive_rows": len(positive),
        "safe_interpretation": "A deliberately added CHSH readout component can make Bell-violating joint correlations exceed the classical release ceiling and reach transported P_release. This is a model-level quantum-audit positive for the measurement/readout component, not for ordinary local population plumbing.",
        "limitations": [
            "This is not a hardware result.",
            "This is not chemical realism or biological metabolism.",
            "The positive result depends on adding a CHSH/noncommutative readout component.",
            "It does not rescue local population plumbing, which remains reduced-state/Arm2 reproducible."
        ],
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/chsh_readout_transport_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
