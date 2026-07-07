#!/usr/bin/env python3
"""
Quantum-coupled information microreactor, Step 3: M-C-R Svetlichny audit.

Layer: quantum-audit

Purpose:
    Test whether a minimal three-module M-C-R state exceeds biseparable /
    two-module-hidden descriptions using a Svetlichny inequality.

Readout discipline:
    This script does not use GHZ fidelity as the main readout. Each correlator
    is measured by local basis rotations followed by computational-basis
    population readout and diagonal parity calculation.

This is not a full source->membrane->converter->reservoir->sink reactor.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

import numpy as np


@dataclass(frozen=True)
class Config:
    seed: int = 0
    dim: int = 8
    modules: tuple[str, str, str] = ("M", "C", "R")


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def ket(i: int, dim: int = 8) -> np.ndarray:
    v = np.zeros(dim, dtype=np.complex128)
    v[i] = 1.0
    return v


def proj(v: np.ndarray) -> np.ndarray:
    return np.outer(v, np.conjugate(v))


def ghz_state(theta: float) -> np.ndarray:
    return math.cos(theta) * ket(0) + math.sin(theta) * ket(7)


def dephase(rho: np.ndarray) -> np.ndarray:
    return np.diag(np.diag(rho)).astype(np.complex128)


def ptrace_1q(rho: np.ndarray, keep: str) -> np.ndarray:
    x = rho.reshape(2, 2, 2, 2, 2, 2)
    if keep == "M":
        return np.einsum("abcdbc->ad", x)
    if keep == "C":
        return np.einsum("abcaec->be", x)
    if keep == "R":
        return np.einsum("abcabf->cf", x)
    raise ValueError("keep must be M, C, or R")


def product_marginals(rho: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(ptrace_1q(rho, "M"), ptrace_1q(rho, "C")), ptrace_1q(rho, "R"))


def partial_transpose_partition(rho: np.ndarray, part: int) -> np.ndarray:
    x = rho.reshape(2, 2, 2, 2, 2, 2)
    axes = list(range(6))
    axes[part], axes[part + 3] = axes[part + 3], axes[part]
    return x.transpose(axes).reshape(8, 8)


def bipartition_negativity(rho: np.ndarray, part: int) -> float:
    vals = np.linalg.eigvalsh(partial_transpose_partition(rho, part))
    return float(np.sum(np.abs(vals[vals < -1e-14])))


def local_basis_rotation(phi: float) -> np.ndarray:
    # Rows are the +/- eigenbasis of cos(phi)X + sin(phi)Y.
    return np.array(
        [[1.0, np.exp(-1j * phi)], [1.0, -np.exp(-1j * phi)]],
        dtype=np.complex128,
    ) / math.sqrt(2.0)


def diagonal_parity_after_rotations(rho: np.ndarray, phis: tuple[float, float, float]) -> float:
    u = np.kron(np.kron(local_basis_rotation(phis[0]), local_basis_rotation(phis[1])), local_basis_rotation(phis[2]))
    rotated = u @ rho @ np.conjugate(u).T
    probs = np.real(np.diag(rotated))
    value = 0.0
    for i, p in enumerate(probs):
        parity = (-1) ** (bin(i).count("1"))
        value += parity * p
    return float(value)


SVETLICHNY_TERMS = [
    (1, 0.0, 0.0, -math.pi / 4),
    (1, 0.0, 0.0, math.pi / 4),
    (1, 0.0, math.pi / 2, -math.pi / 4),
    (-1, 0.0, math.pi / 2, math.pi / 4),
    (1, math.pi / 2, 0.0, -math.pi / 4),
    (-1, math.pi / 2, 0.0, math.pi / 4),
    (-1, math.pi / 2, math.pi / 2, -math.pi / 4),
    (-1, math.pi / 2, math.pi / 2, math.pi / 4),
]

MERMIN_TERMS = [
    (1, 0.0, 0.0, 0.0),
    (-1, 0.0, math.pi / 2, math.pi / 2),
    (-1, math.pi / 2, 0.0, math.pi / 2),
    (-1, math.pi / 2, math.pi / 2, 0.0),
]


def svetlichny_value(rho: np.ndarray) -> float:
    return float(sum(sign * diagonal_parity_after_rotations(rho, (m, c, r)) for sign, m, c, r in SVETLICHNY_TERMS))


def mermin_value(rho: np.ndarray) -> float:
    return float(sum(sign * diagonal_parity_after_rotations(rho, (m, c, r)) for sign, m, c, r in MERMIN_TERMS))


def theta_grid() -> List[float]:
    return [0.0, math.pi / 12, math.pi / 8, math.pi / 6, math.pi / 4]


def arm_metrics(rho: np.ndarray) -> Dict[str, float | str]:
    n_m = bipartition_negativity(rho, 0)
    n_c = bipartition_negativity(rho, 1)
    n_r = bipartition_negativity(rho, 2)
    geo = (n_m * n_c * n_r) ** (1.0 / 3.0) if n_m * n_c * n_r > 0 else 0.0
    s = svetlichny_value(rho)
    m = mermin_value(rho)
    return {
        "N_M_CR": n_m,
        "N_C_MR": n_c,
        "N_R_MC": n_r,
        "tripartite_negativity_geom": geo,
        "Svetlichny_S": s,
        "abs_Svetlichny_S": abs(s),
        "Svetlichny_biseparable_bound": 4.0,
        "Svetlichny_violation": max(0.0, abs(s) - 4.0),
        "Mermin_M": m,
        "Mermin_local_bound": 2.0,
        "Mermin_violation": max(0.0, abs(m) - 2.0),
        "readout": "diagonal_parity_after_local_basis_rotations",
    }


def marginal_diffs(reference: np.ndarray, rho: np.ndarray) -> Dict[str, float]:
    return {
        "marginal_diff_vs_entangled_M_fro": float(np.linalg.norm(ptrace_1q(reference, "M") - ptrace_1q(rho, "M"))),
        "marginal_diff_vs_entangled_C_fro": float(np.linalg.norm(ptrace_1q(reference, "C") - ptrace_1q(rho, "C"))),
        "marginal_diff_vs_entangled_R_fro": float(np.linalg.norm(ptrace_1q(reference, "R") - ptrace_1q(rho, "R"))),
    }


def run(seed: int = 0) -> Dict[str, Any]:
    # Seed retained for reproducibility interface; deterministic audit uses no sampling.
    _ = np.random.default_rng(seed)
    cfg = Config(seed=seed)
    rows: List[Dict[str, Any]] = []

    for theta in theta_grid():
        ent = proj(ghz_state(theta))
        arms = {
            "entangled_GHZ": ent,
            "dephased_correlated": dephase(ent),
            "product_marginals": product_marginals(ent),
        }
        for name, rho in arms.items():
            metrics = arm_metrics(rho)
            diffs = marginal_diffs(ent, rho)
            row = {
                "theta": rf(theta),
                "theta_over_pi": rf(theta / math.pi),
                "arm": name,
                **{k: (rf(v) if isinstance(v, float) else v) for k, v in metrics.items()},
                **{k: rf(v) for k, v in diffs.items()},
            }
            rows.append(row)

    return {
        "experiment": "quantum_coupled_microreactor_step3_svetlichny",
        "date": "2026-07-07",
        "layer": "quantum-audit",
        "model": "3-qubit M-C-R GHZ-family state with diagonal-parity Svetlichny readout",
        "seed": seed,
        "config": asdict(cfg),
        "rows": rows,
        "limitations": [
            "Svetlichny audit only, not a full microreactor.",
            "Readout is diagonal parity after local basis rotations, not natural device throughput.",
            "No source, membrane, converter dynamics, reservoir dynamics, or sink dynamics are included.",
            "No hardware result and no quantum advantage claim.",
        ],
    }


def write_csv(result: Dict[str, Any], path: Path) -> None:
    rows = result["rows"]
    fields = list(rows[0].keys())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/step3_svetlichny_seed0.json"))
    parser.add_argument("--csv", type=Path, default=Path("data/quantum_microreactor/step3_svetlichny_seed0_summary.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result, args.csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
