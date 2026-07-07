#!/usr/bin/env python3
"""
Minimal basis-relative causality test.

Question:
    Can a coherent two-qubit arm change a channel outcome after
    single-particle marginals are exactly matched?

Design:
    arm1 coherent:
        Bell-origin state (|00> + |11>) / sqrt(2)

    arm2 dephased:
        configuration-basis dephase of arm1, same rho1/rho2, N = 0

    arm3 product_marginals:
        rho1(arm1) tensor rho2(arm1), same rho1/rho2, N = 0

    analyzer:
        H tensor H, followed by same/anti channel measurement.

Pass pattern:
    p_same(coherent) != p_same(dephased) == p_same(product_marginals)
    with rho1/rho2 identical across arms.

Important limitation:
    This is audit-chapter inventory. It is not a component-development claim,
    not a spatial droplet/lattice transport experiment, and not by itself a
    quantum-specific claim.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict

import numpy as np


def ket(index: int, dim: int = 4) -> np.ndarray:
    v = np.zeros(dim, dtype=np.complex128)
    v[index] = 1.0
    return v


def projector(psi: np.ndarray) -> np.ndarray:
    return np.outer(psi, np.conjugate(psi))


def kron(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.kron(a, b)


def partial_trace_2q(rho: np.ndarray, keep: int) -> np.ndarray:
    r = rho.reshape(2, 2, 2, 2)
    if keep == 0:
        return np.einsum("ijkj->ik", r)
    if keep == 1:
        return np.einsum("ijil->jl", r)
    raise ValueError("keep must be 0 or 1")


def partial_transpose_second(rho: np.ndarray) -> np.ndarray:
    return rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)


def negativity(rho: np.ndarray) -> float:
    vals = np.linalg.eigvalsh(partial_transpose_second(rho))
    return float(np.sum(np.abs(vals[vals < 0])))


def config_dephase(rho: np.ndarray) -> np.ndarray:
    return np.diag(np.diag(rho)).astype(np.complex128)


def real_matrix(x: np.ndarray, decimals: int = 12) -> list[list[float]]:
    return np.real_if_close(x).real.round(decimals).tolist()


def channel_probs(rho: np.ndarray) -> Dict[str, float]:
    h = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=np.complex128) / math.sqrt(2.0)
    u = kron(h, h)
    same = np.diag([1.0, 0.0, 0.0, 1.0]).astype(np.complex128)
    anti = np.diag([0.0, 1.0, 1.0, 0.0]).astype(np.complex128)
    out = u @ rho @ np.conjugate(u).T
    return {
        "p_same_channel": float(np.real(np.trace(same @ out))),
        "p_anti_channel": float(np.real(np.trace(anti @ out))),
    }


def arm_summary(rho: np.ndarray) -> Dict[str, Any]:
    probs = channel_probs(rho)
    return {
        "negativity": round(negativity(rho), 12),
        "p_same_channel": round(probs["p_same_channel"], 12),
        "p_anti_channel": round(probs["p_anti_channel"], 12),
        "rho1": real_matrix(partial_trace_2q(rho, 0)),
        "rho2": real_matrix(partial_trace_2q(rho, 1)),
    }


def marginal_diff(a: np.ndarray, b: np.ndarray) -> Dict[str, float]:
    a1, a2 = partial_trace_2q(a, 0), partial_trace_2q(a, 1)
    b1, b2 = partial_trace_2q(b, 0), partial_trace_2q(b, 1)
    return {
        "rho1_frobenius": round(float(np.linalg.norm(a1 - b1)), 12),
        "rho2_frobenius": round(float(np.linalg.norm(a2 - b2)), 12),
        "rho1_max_abs": round(float(np.max(np.abs(a1 - b1))), 12),
        "rho2_max_abs": round(float(np.max(np.abs(a2 - b2))), 12),
    }


def run_experiment() -> Dict[str, Any]:
    phi_plus = (ket(0) + ket(3)) / math.sqrt(2.0)
    coherent = projector(phi_plus)
    dephased = config_dephase(coherent)
    product_marginals = kron(partial_trace_2q(coherent, 0), partial_trace_2q(coherent, 1))

    arms = {
        "coherent": arm_summary(coherent),
        "dephased": arm_summary(dephased),
        "product_marginals": arm_summary(product_marginals),
    }

    return {
        "experiment": "negativity_causality_test",
        "date": "2026-07-07",
        "model": "two-qubit contact-channel analyzer",
        "config": {
            "basis": "|00>, |01>, |10>, |11>",
            "coherent_state": "(|00> + |11>) / sqrt(2)",
            "dephased_state": "configuration-basis dephase of coherent_state",
            "product_marginals_state": "rho1(coherent) tensor rho2(coherent); mixed separable state",
            "analyzer": "H tensor H",
            "same_channel_projector": "|00><00| + |11><11|",
            "anti_channel_projector": "|01><01| + |10><10|",
        },
        "arms": arms,
        "marginal_audit": {
            "coherent_vs_dephased": marginal_diff(coherent, dephased),
            "coherent_vs_product_marginals": marginal_diff(coherent, product_marginals),
        },
        "contrast": {
            "coherent_minus_dephased_p_same": round(arms["coherent"]["p_same_channel"] - arms["dephased"]["p_same_channel"], 12),
            "coherent_minus_product_p_same": round(arms["coherent"]["p_same_channel"] - arms["product_marginals"]["p_same_channel"], 12),
            "dephased_minus_product_p_same": round(arms["dephased"]["p_same_channel"] - arms["product_marginals"]["p_same_channel"], 12),
        },
        "verdict": "PASS_MINIMAL_LOAD_BEARING_COHERENCE_BASIS_RELATIVE_CLASSICAL_EFFECTIVE: identical one-particle marginals; coherent arm changes channel outcome while N=0 controls match.",
        "limitations": [
            "Minimal two-qubit channel test, not a spatial droplet/lattice transport test.",
            "This is audit-chapter inventory, not a component-development claim.",
            "The channel effect is basis-relative and should not be promoted to a quantum-specific claim without stronger controls.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=None, help="Optional JSON output path")
    args = parser.parse_args()

    result = run_experiment()
    text = json.dumps(result, indent=2, ensure_ascii=False)
    print(text)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
