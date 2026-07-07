#!/usr/bin/env python3
"""
Quantum-coupled information microreactor, Step 5:
reactor-like M-C-R product-population synergy.

Layer: quantum-audit

Purpose:
    Move from abstract odd-parity population to a minimal reactor-like product
    population P(M=1,C=1,R=1), while preserving diagonal readout, pairwise
    controls, dephase control, and raw-log reproducibility.

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
    drain_rate: float = 0.8
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
RHO_COHERENT = np.outer(PSI0, np.conjugate(PSI0))
RHO_DEPHASED = np.diag(np.diag(RHO_COHERENT)).astype(np.complex128)
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


def evolved_density(dynamics: str, gamma: float, rho_in: np.ndarray) -> np.ndarray:
    u = unitary_from_hamiltonian(hamiltonian_for(dynamics), gamma)
    return H_ALL @ u @ rho_in @ np.conjugate(u).T @ np.conjugate(H_ALL).T


def diagonal_reactor_metrics(rho_readout: np.ndarray, cfg: Config) -> Dict[str, float]:
    probs = np.real(np.diag(rho_readout))
    p_product = float(probs[7])  # M=1,C=1,R=1
    conversion_success = float(sum(probs[i] for i in range(8) if ((i >> 1) & 1) == 1 and (i & 1) == 1))
    reservoir_fill = float(sum(probs[i] for i in range(8) if (i & 1) == 1))
    membrane_pass = float(sum(probs[i] for i in range(8) if ((i >> 2) & 1) == 1))
    return {
        "P_product_population": p_product,
        "conversion_success": conversion_success,
        "reservoir_fill": reservoir_fill,
        "membrane_pass": membrane_pass,
        "release_population": cfg.drain_rate * p_product,
    }


def gamma_grid() -> List[float]:
    return [0.0, math.pi / 8, math.pi / 4]


def run(seed: int = 0) -> Dict[str, Any]:
    # Seed retained for reproducibility interface; deterministic audit uses no sampling.
    _ = np.random.default_rng(seed)
    cfg = Config(seed=seed)
    rows: List[Dict[str, Any]] = []
    dynamics_order = ["baseline", "pair_MC", "pair_CR", "pair_MR", "pairwise_product", "genuine_3body"]
    input_states = {
        "coherent_input": RHO_COHERENT,
        "dephased_input": RHO_DEPHASED,
    }

    for gamma in gamma_grid():
        for input_mode, rho_in in input_states.items():
            baseline = diagonal_reactor_metrics(evolved_density("baseline", gamma, rho_in), cfg)["P_product_population"]
            pair_values = [
                diagonal_reactor_metrics(evolved_density("pair_MC", gamma, rho_in), cfg)["P_product_population"],
                diagonal_reactor_metrics(evolved_density("pair_CR", gamma, rho_in), cfg)["P_product_population"],
                diagonal_reactor_metrics(evolved_density("pair_MR", gamma, rho_in), cfg)["P_product_population"],
            ]
            pair_pred = sum(pair_values) - 2.0 * baseline

            for dynamics in dynamics_order:
                metrics = diagonal_reactor_metrics(evolved_density(dynamics, gamma, rho_in), cfg)
                is_full = dynamics in {"pairwise_product", "genuine_3body"}
                synergy = metrics["P_product_population"] - pair_pred if is_full else ""
                row: Dict[str, Any] = {
                    "gamma": rf(gamma),
                    "gamma_over_pi": rf(gamma / math.pi),
                    "input_mode": input_mode,
                    "dynamics": dynamics,
                    **{k: rf(v) for k, v in metrics.items()},
                    "pairwise_additive_prediction_P": rf(pair_pred) if is_full else "",
                    "synergy_residual_P": rf(synergy) if is_full else "",
                    "response_readout": "diagonal_P111_population_after_local_H",
                }
                rows.append(row)

    return {
        "experiment": "quantum_coupled_microreactor_step5_reactor_like_population_synergy",
        "date": "2026-07-07",
        "layer": "quantum-audit",
        "model": "3-qubit M-C-R reactor-like P111 product-population synergy with pairwise controls and dephase control",
        "seed": seed,
        "config": asdict(cfg),
        "rows": rows,
        "limitations": [
            "Minimal reactor-like population audit only, not a full microreactor.",
            "Readout is diagonal P111 product population after local H rotations, not natural device throughput.",
            "No explicit source, selective membrane, converter kinetics, reservoir capacity, or sink dynamics are included.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/step5_reactor_like_population_synergy_seed0.json"))
    parser.add_argument("--csv", type=Path, default=Path("data/quantum_microreactor/step5_reactor_like_population_synergy_seed0_summary.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result, args.csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
