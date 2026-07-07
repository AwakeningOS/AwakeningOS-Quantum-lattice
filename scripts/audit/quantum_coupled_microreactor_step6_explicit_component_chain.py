#!/usr/bin/env python3
"""
Quantum-coupled information microreactor, Step 6:
explicit minimal component chain.

Layer: quantum-audit / component-semantics bridge

Purpose:
    Replace the symbolic Step 5 phase-interaction model with explicit minimal
    operations for source, membrane/pass, converter, reservoir fill, and
    sink/release metrics.

This is still not a full source->membrane->converter->reservoir->sink reactor.
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
    source_angle: float = math.pi / 2
    drain_rate: float = 0.8
    modules: tuple[str, str, str] = ("M", "C", "R")


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def ry(theta: float) -> np.ndarray:
    return np.array(
        [[math.cos(theta / 2), -math.sin(theta / 2)], [math.sin(theta / 2), math.cos(theta / 2)]],
        dtype=np.complex128,
    )


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(a, b), c)


I = np.eye(2, dtype=np.complex128)
P0 = np.diag([1.0, 0.0]).astype(np.complex128)
P1 = np.diag([0.0, 1.0]).astype(np.complex128)
PSI_ZERO = np.zeros(8, dtype=np.complex128)
PSI_ZERO[0] = 1.0


def single_gate(gate: np.ndarray, target: int) -> np.ndarray:
    ops = [I, I, I]
    ops[target] = gate
    return kron3(*ops)


def controlled_gate(control: int, target: int, gate: np.ndarray) -> np.ndarray:
    ops0 = [I, I, I]
    ops1 = [I, I, I]
    ops0[control] = P0
    ops1[control] = P1
    ops1[target] = gate
    return kron3(*ops0) + kron3(*ops1)


def cc_gate(control_a: int, control_b: int, target: int, gate: np.ndarray) -> np.ndarray:
    out = np.zeros((8, 8), dtype=np.complex128)
    for i in range(8):
        bits = [(i >> 2) & 1, (i >> 1) & 1, i & 1]
        if bits[control_a] == 1 and bits[control_b] == 1:
            for target_bit in (0, 1):
                bits2 = list(bits)
                bits2[target] = target_bit
                j = (bits2[0] << 2) | (bits2[1] << 1) | bits2[2]
                out[j, i] = gate[target_bit, bits[target]]
        else:
            out[i, i] = 1.0
    return out


def dephase(rho: np.ndarray) -> np.ndarray:
    return np.diag(np.diag(rho)).astype(np.complex128)


def source_state(cfg: Config, dephased: bool) -> np.ndarray:
    source = single_gate(ry(cfg.source_angle), target=0)
    rho = source @ np.outer(PSI_ZERO, np.conjugate(PSI_ZERO)) @ np.conjugate(source).T
    return dephase(rho) if dephased else rho


def unitary_for(dynamics: str, gamma: float) -> np.ndarray:
    u_mc = controlled_gate(0, 1, ry(gamma))  # M -> C converter
    u_cr = controlled_gate(1, 2, ry(gamma))  # C -> R reservoir fill
    u_mr = controlled_gate(0, 2, ry(gamma))  # M -> R leak/control pair
    u_3 = cc_gate(0, 1, 2, ry(gamma))        # MC -> R three-body boost

    if dynamics == "baseline":
        return np.eye(8, dtype=np.complex128)
    if dynamics == "pair_MC":
        return u_mc
    if dynamics == "pair_CR":
        return u_cr
    if dynamics == "pair_MR":
        return u_mr
    if dynamics == "pairwise_chain":
        return u_cr @ u_mc
    if dynamics == "genuine_3body_boost":
        return u_3 @ u_cr @ u_mc
    raise ValueError(f"unknown dynamics: {dynamics}")


def evolve(gamma: float, dynamics: str, input_mode: str, cfg: Config) -> np.ndarray:
    rho = source_state(cfg, dephased=(input_mode == "dephased_after_source"))
    u = unitary_for(dynamics, gamma)
    return u @ rho @ np.conjugate(u).T


def diagonal_metrics(rho: np.ndarray, cfg: Config) -> Dict[str, float]:
    probs = np.real(np.diag(rho))
    p_product = float(probs[7])
    conversion_success = float(sum(probs[i] for i in range(8) if ((i >> 1) & 1) == 1))
    reservoir_fill = float(sum(probs[i] for i in range(8) if (i & 1) == 1))
    product_stored = float(sum(probs[i] for i in range(8) if ((i >> 1) & 1) == 1 and (i & 1) == 1))
    membrane_pass = float(sum(probs[i] for i in range(8) if ((i >> 2) & 1) == 1))
    return {
        "P_product_population": p_product,
        "conversion_success": conversion_success,
        "reservoir_fill": reservoir_fill,
        "product_stored": product_stored,
        "membrane_pass": membrane_pass,
        "release_population": cfg.drain_rate * p_product,
    }


def gamma_grid() -> List[float]:
    return [0.0, math.pi / 4, math.pi / 2]


def run(seed: int = 0) -> Dict[str, Any]:
    # Seed retained for reproducibility interface; deterministic audit uses no sampling.
    _ = np.random.default_rng(seed)
    cfg = Config(seed=seed)
    rows: List[Dict[str, Any]] = []
    dynamics_order = ["baseline", "pair_MC", "pair_CR", "pair_MR", "pairwise_chain", "genuine_3body_boost"]
    input_modes = ["coherent_after_source", "dephased_after_source"]

    for gamma in gamma_grid():
        for input_mode in input_modes:
            metrics_by_arm = {d: diagonal_metrics(evolve(gamma, d, input_mode, cfg), cfg) for d in dynamics_order}
            baseline = metrics_by_arm["baseline"]["P_product_population"]
            pair_pred = (
                metrics_by_arm["pair_MC"]["P_product_population"]
                + metrics_by_arm["pair_CR"]["P_product_population"]
                + metrics_by_arm["pair_MR"]["P_product_population"]
                - 2.0 * baseline
            )
            chain_pred = metrics_by_arm["pairwise_chain"]["P_product_population"]

            for dynamics in dynamics_order:
                metrics = metrics_by_arm[dynamics]
                is_full = dynamics in {"pairwise_chain", "genuine_3body_boost"}
                row: Dict[str, Any] = {
                    "gamma": rf(gamma),
                    "gamma_over_pi": rf(gamma / math.pi),
                    "input_mode": input_mode,
                    "dynamics": dynamics,
                    **{k: rf(v) for k, v in metrics.items()},
                    "pairwise_additive_prediction_P": rf(pair_pred) if is_full else "",
                    "residual_vs_pairwise_additive": rf(metrics["P_product_population"] - pair_pred) if is_full else "",
                    "pairwise_chain_prediction_P": rf(chain_pred) if dynamics == "genuine_3body_boost" else "",
                    "residual_vs_pairwise_chain": rf(metrics["P_product_population"] - chain_pred) if dynamics == "genuine_3body_boost" else "",
                    "response_readout": "diagonal_P111_population",
                }
                rows.append(row)

    return {
        "experiment": "quantum_coupled_microreactor_step6_explicit_component_chain",
        "date": "2026-07-07",
        "layer": "quantum-audit/component-semantics-bridge",
        "model": "3-qubit explicit source->membrane/pass->converter->reservoir chain with diagonal P111 readout",
        "seed": seed,
        "config": asdict(cfg),
        "rows": rows,
        "limitations": [
            "Minimal explicit component-chain audit only, not a full microreactor.",
            "No spatial membrane, no finite reservoir capacity, and no stochastic source/sink environment are included.",
            "The three-body boost is an explicit designed component rule, not a natural device throughput result.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/step6_explicit_component_chain_seed0.json"))
    parser.add_argument("--csv", type=Path, default=Path("data/quantum_microreactor/step6_explicit_component_chain_seed0_summary.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result, args.csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
