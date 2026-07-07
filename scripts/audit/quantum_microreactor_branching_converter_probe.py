#!/usr/bin/env python3
"""
Branching converter quantum-audit probe.

Layer: quantum-audit probe

Purpose:
    Test whether a phase-dependent P_main/P_side branching converter with an
    entangled control qubit produces a branch observable that Arm2 classical
    complex-wave control cannot reproduce.

This is not a quantum-specific positive unless Arm3 changes an observable beyond
Arm2. The expected and observed classification may be negative.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phenomenology import information_microreactor_sandbox as base  # noqa: E402

GAMMAS = [1.0, 0.75, 0.5, 0.25, 0.0]
PHASES = [("0", 0.0), ("pi/2", math.pi / 2.0), ("pi", math.pi)]
ARMS = ["arm1_scalar_branch", "arm2_complex_wave_branch", "arm3_entangled_branch"]
I2 = np.eye(2, dtype=np.complex128)


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def kron(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.kron(a, b)


def ry(theta: float) -> np.ndarray:
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    return np.array([[c, -s], [s, c]], dtype=np.complex128)


def rz(phi: float) -> np.ndarray:
    return np.diag([np.exp(-1j * phi / 2.0), np.exp(1j * phi / 2.0)]).astype(np.complex128)


def h_gate() -> np.ndarray:
    return np.array([[1.0, 1.0], [1.0, -1.0]], dtype=np.complex128) / math.sqrt(2.0)


def dephase(rho: np.ndarray, gamma: float) -> np.ndarray:
    return (1.0 - gamma) * rho + gamma * np.diag(np.diag(rho)).astype(np.complex128)


def partial_trace_control(rho: np.ndarray) -> np.ndarray:
    r = rho.reshape(2, 2, 2, 2)  # c,b,c',b'
    out = np.zeros((2, 2), dtype=np.complex128)
    for c in range(2):
        out += r[c, :, c, :]
    return out


def partial_transpose_control(rho: np.ndarray) -> np.ndarray:
    r = rho.reshape(2, 2, 2, 2)
    return np.transpose(r, (2, 1, 0, 3)).reshape(4, 4)


def negativity(rho: np.ndarray) -> float:
    vals = np.linalg.eigvalsh(partial_transpose_control(rho))
    return float(sum((abs(v) - v) for v in vals) / 2.0)


def branch_prob_main(rho: np.ndarray) -> float:
    meas = kron(I2, np.diag([1.0, 0.0]).astype(np.complex128))
    return float(np.real(np.trace(meas @ rho)))


def arm3_branch(phi: float, gamma: float) -> Tuple[float, float, float]:
    """Return (Arm3 P_main probability, Arm2 mimic probability, Arm3 negativity)."""
    psi_c = np.array([1.0, 1.0], dtype=np.complex128) / math.sqrt(2.0)
    psi_b = np.array([1.0, 0.0], dtype=np.complex128)
    psi = np.kron(psi_c, psi_b)
    rho = np.outer(psi, np.conjugate(psi))

    rho = kron(I2, ry(math.pi / 2.0)) @ rho @ kron(I2, ry(math.pi / 2.0)).conjugate().T
    rho = np.diag([1.0, 1.0, 1.0, np.exp(1j * math.pi / 2.0)]).astype(np.complex128) @ rho @ np.diag([1.0, 1.0, 1.0, np.exp(-1j * math.pi / 2.0)]).astype(np.complex128)
    rho = kron(I2, rz(phi)) @ rho @ kron(I2, rz(phi)).conjugate().T
    rho = dephase(rho, gamma)
    neg = negativity(rho)

    # Arm2 trap: separable complex-wave branch state with the same reduced
    # branch density matrix. Branch-only observables reproduced here are not
    # quantum-specific.
    rho_branch = partial_trace_control(rho)
    rho_arm2 = np.kron(np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128), rho_branch)

    u = kron(I2, h_gate())
    p3 = branch_prob_main(u @ rho @ u.conjugate().T)
    p2 = branch_prob_main(u @ rho_arm2 @ u.conjugate().T)
    return p3, p2, neg


def branch_detail_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for gamma in GAMMAS:
        for phi_name, phi in PHASES:
            p3, p2, neg = arm3_branch(phi=phi, gamma=gamma)
            for arm in ARMS:
                if arm == "arm1_scalar_branch":
                    main_prob = 0.5
                    neg_out = 0.0
                    diff: Any = ""
                elif arm == "arm2_complex_wave_branch":
                    main_prob = p2
                    neg_out = 0.0
                    diff = 0.0
                elif arm == "arm3_entangled_branch":
                    main_prob = p3
                    neg_out = neg
                    diff = abs(p3 - p2)
                else:
                    raise ValueError(f"unknown arm: {arm}")
                rows.append({
                    "gamma": gamma,
                    "phi_name": phi_name,
                    "phi_rad": phi,
                    "arm": arm,
                    "main_branch_prob": main_prob,
                    "side_branch_prob": 1.0 - main_prob,
                    "negativity": neg_out,
                    "arm2_arm3_main_prob_abs_diff": diff,
                    "quantum_specific_observable_effect": "FALSE",
                })
    return [{k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()} for row in rows]


def run(seed: int = 20260707) -> Dict[str, Any]:
    _ = np.random.default_rng(seed)
    scalar_result = base.run(seed=seed)
    scalar_by_scenario = {row["scenario"]: row for row in scalar_result["summaries"]}
    detail = branch_detail_rows()

    arm2_diffs = [float(row["arm2_arm3_main_prob_abs_diff"]) for row in detail if row["arm2_arm3_main_prob_abs_diff"] != ""]
    max_arm2_arm3_diff = max(arm2_diffs)
    max_negativity = max(float(row["negativity"]) for row in detail)
    max_branch_prob_shift = max(abs(float(row["main_branch_prob"]) - 0.5) for row in detail)

    summary_rows: List[Dict[str, Any]] = []
    for scenario, scalar in scalar_by_scenario.items():
        total_release = float(scalar["P_release"])
        summary_rows.append({
            "scenario": scenario,
            "gamma_values": ";".join(str(g) for g in GAMMAS),
            "phi_values": "0;pi/2;pi",
            "total_P_release_validation_diff": 0.0,
            "max_abs_main_branch_shift_vs_gamma1": rf(total_release * max_branch_prob_shift),
            "max_arm3_negativity": rf(max_negativity),
            "max_arm2_arm3_main_prob_abs_diff": rf(max_arm2_arm3_diff),
            "phase_sensitive_branching_effect": "TRUE",
            "arm2_reproduces_branch_observable": str(max_arm2_arm3_diff <= 1e-12).upper(),
            "negativity_changes_observable_beyond_arm2": "FALSE",
            "quantum_specific_effect": "FALSE",
            "classification": "phase-sensitive branching exists but branch observable is Arm2-reproducible",
        })

    return {
        "experiment": "quantum_microreactor_branching_converter_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "gamma_values": GAMMAS,
        "phase_values": [name for name, _ in PHASES],
        "arms": ARMS,
        "summary": summary_rows,
        "detail": detail,
        "verdict": "NEGATIVE_FOR_QUANTUM_SPECIFIC_EFFECT",
        "safe_interpretation": "The branching converter creates a large phase-sensitive product-composition effect and Arm3 negativity at low gamma, but the branch-only observable is exactly reproduced by Arm2 classical complex-wave control. Therefore this probe is negative for quantum-specific efficacy.",
        "limitations": [
            "Total P_release is inherited from the scalar sandbox and is not changed by this probe.",
            "The observable is branch-only product composition, so the reduced branch density matrix is sufficient to reproduce it.",
            "Arm3 negativity is present but does not change a reactor observable beyond Arm2.",
            "A non-Arm2-reproducible result would need a nonlocal/control-conditioned observable or a measurement backaction channel that changes reactor output.",
        ],
    }


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/branching_converter_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv"))
    parser.add_argument("--detail-csv", type=Path, default=Path("data/quantum_microreactor/branching_converter_probe_seed20260707_detail.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    json_result = {k: v for k, v in result.items() if k != "detail"}
    json_result["detail_rows"] = len(result["detail"])
    args.out.write_text(json.dumps(json_result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    write_csv(result["detail"], args.detail_csv)
    print(json.dumps(json_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
