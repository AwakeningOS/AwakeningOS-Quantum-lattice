#!/usr/bin/env python3
"""
Quantum-coupled information microreactor, Step 4: M-C-R population synergy.

Layer: quantum-audit

Purpose:
    Test whether a diagonal population response has a three-module synergy
    residual that is absent under pairwise-product dynamics but present under
    a genuine three-body dynamics.

Readout discipline:
    The response is odd-parity population after local H rotations and
    computational-basis measurement. It is not GHZ fidelity.

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


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(a, b), c)


I = np.eye(2, dtype=np.complex128)
Z = np.diag([1.0, -1.0]).astype(np.complex128)
H1 = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=np.complex128) / math.sqrt(2.0)
H_ALL = kron3(H1, H1, H1)
PLUS = np.array([1.0, 1.0], dtype=np.complex128) / math.sqrt(2.0)
PSI0 = kron3(PLUS, PLUS, PLUS)
ZZ_MC = kron3(Z, Z, I)
ZZ_CR = kron3(I, Z, Z)
ZZ_MR = kron3(Z, I, Z)
ZZZ = kron3(Z, Z, Z)


def unitary_from_hamiltonian(h: np.ndarray, gamma: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(h)
    return vecs @ np.diag(np.exp(-1j * gamma * vals)) @ np.conjugate(vecs).T


def hamiltonian_for(dynamics: str) -> np.ndarray:
    zero = np.zeros((8, 8), dtype=np.complex128)
    if dynamics == "baseline":
        return zero
    if dynamics == "pair_MC":
        return ZZ_MC
    if dynamics == "pair_CR":
        return ZZ_CR
    if dynamics == "pair_MR":
        return ZZ_MR
    if dynamics == "pairwise_product":
        return ZZ_MC + ZZ_CR + ZZ_MR
    if dynamics == "genuine_3body":
        return ZZZ
    raise ValueError(f"unknown dynamics: {dynamics}")


def evolved_state(dynamics: str, gamma: float) -> np.ndarray:
    return unitary_from_hamiltonian(hamiltonian_for(dynamics), gamma) @ PSI0


def diagonal_readout(psi: np.ndarray) -> Dict[str, float]:
    out = H_ALL @ psi
    probs = np.abs(out) ** 2
    odd = 0.0
    parity = 0.0
    for i, p in enumerate(probs):
        bitcount = bin(i).count("1")
        if bitcount % 2 == 1:
            odd += float(p)
        parity += ((-1) ** bitcount) * float(p)
    return {
        "odd_parity_population": odd,
        "parity_expectation": parity,
        "p000_after_readout": float(probs[0]),
    }


def gamma_grid() -> List[float]:
    return [0.0, math.pi / 16, math.pi / 8, math.pi / 4]


def run(seed: int = 0) -> Dict[str, Any]:
    # Seed retained for reproducibility interface; deterministic audit uses no sampling.
    _ = np.random.default_rng(seed)
    cfg = Config(seed=seed)
    rows: List[Dict[str, Any]] = []
    dynamics_order = ["baseline", "pair_MC", "pair_CR", "pair_MR", "pairwise_product", "genuine_3body"]

    for gamma in gamma_grid():
        baseline = diagonal_readout(evolved_state("baseline", gamma))["odd_parity_population"]
        pair_values = [
            diagonal_readout(evolved_state("pair_MC", gamma))["odd_parity_population"],
            diagonal_readout(evolved_state("pair_CR", gamma))["odd_parity_population"],
            diagonal_readout(evolved_state("pair_MR", gamma))["odd_parity_population"],
        ]
        pair_pred = sum(pair_values) - 2.0 * baseline

        for dynamics in dynamics_order:
            metrics = diagonal_readout(evolved_state(dynamics, gamma))
            is_full = dynamics in {"pairwise_product", "genuine_3body"}
            synergy = metrics["odd_parity_population"] - pair_pred if is_full else ""
            row: Dict[str, Any] = {
                "gamma": rf(gamma),
                "gamma_over_pi": rf(gamma / math.pi),
                "dynamics": dynamics,
                "odd_parity_population": rf(metrics["odd_parity_population"]),
                "parity_expectation": rf(metrics["parity_expectation"]),
                "p000_after_readout": rf(metrics["p000_after_readout"]),
                "pairwise_additive_prediction_odd": rf(pair_pred) if is_full else "",
                "synergy_residual_odd": rf(synergy) if is_full else "",
                "response_readout": "diagonal_odd_parity_population_after_local_H",
            }
            rows.append(row)

    return {
        "experiment": "quantum_coupled_microreactor_step4_population_synergy",
        "date": "2026-07-07",
        "layer": "quantum-audit",
        "model": "3-qubit M-C-R pairwise-product vs genuine-3body dynamics with diagonal odd-parity population readout",
        "seed": seed,
        "config": asdict(cfg),
        "rows": rows,
        "limitations": [
            "Order/synergy audit only, not a full microreactor.",
            "Readout is diagonal odd-parity population after local H rotations, not natural device throughput.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/step4_population_synergy_seed0.json"))
    parser.add_argument("--csv", type=Path, default=Path("data/quantum_microreactor/step4_population_synergy_seed0_summary.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result, args.csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
