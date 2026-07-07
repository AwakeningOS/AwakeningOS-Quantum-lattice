#!/usr/bin/env python3
"""
Quantum-coupled information microreactor, Step 1: C-R module coupling.

Layer: quantum-audit

Purpose:
    Test whether a converter-reservoir (C-R) module bond can show an
    entanglement-dependent joint response after module marginals are matched
    against N=0 controls.

This is not a full source->membrane->converter->reservoir->sink reactor.
It is the smallest audit subexperiment for the converter-reservoir bond.
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
    c0: int = 0b001
    c1: int = 0b110
    r0: int = 0b000
    r1: int = 0b111
    c_dim: int = 8
    r_dim: int = 8

    @property
    def dim(self) -> int:
        return self.c_dim * self.r_dim


def idx(c: int, r: int, cfg: Config) -> int:
    return c * cfg.r_dim + r


def ket(i: int, dim: int) -> np.ndarray:
    v = np.zeros(dim, dtype=np.complex128)
    v[i] = 1.0
    return v


def proj(v: np.ndarray) -> np.ndarray:
    return np.outer(v, np.conjugate(v))


def ptrace(rho: np.ndarray, keep: str, cfg: Config) -> np.ndarray:
    x = rho.reshape(cfg.c_dim, cfg.r_dim, cfg.c_dim, cfg.r_dim)
    if keep == "C":
        return np.einsum("crdr->cd", x)
    if keep == "R":
        return np.einsum("crcs->rs", x)
    raise ValueError("keep must be C or R")


def pt_r(rho: np.ndarray, cfg: Config) -> np.ndarray:
    x = rho.reshape(cfg.c_dim, cfg.r_dim, cfg.c_dim, cfg.r_dim)
    return x.transpose(0, 3, 2, 1).reshape(cfg.dim, cfg.dim)


def negativity(rho: np.ndarray, cfg: Config) -> float:
    vals = np.linalg.eigvalsh(pt_r(rho, cfg))
    return float(np.sum(np.abs(vals[vals < -1e-14])))


def s2(rho_m: np.ndarray) -> float:
    purity = float(np.real(np.trace(rho_m @ rho_m)))
    return float(-math.log(purity, 2)) if purity > 0 else 0.0


def state(theta: float, cfg: Config) -> np.ndarray:
    a = ket(idx(cfg.c0, cfg.r0, cfg), cfg.dim)
    b = ket(idx(cfg.c1, cfg.r1, cfg), cfg.dim)
    return math.cos(theta) * a + math.sin(theta) * b


def dephase(rho: np.ndarray) -> np.ndarray:
    return np.diag(np.diag(rho)).astype(np.complex128)


def product_marginals(rho: np.ndarray, cfg: Config) -> np.ndarray:
    return np.kron(ptrace(rho, "C", cfg), ptrace(rho, "R", cfg))


def joint_projector(cfg: Config) -> np.ndarray:
    a = ket(idx(cfg.c0, cfg.r0, cfg), cfg.dim)
    b = ket(idx(cfg.c1, cfg.r1, cfg), cfg.dim)
    return proj((a + b) / math.sqrt(2.0))


def same_projector(cfg: Config) -> np.ndarray:
    p = np.zeros((cfg.dim, cfg.dim), dtype=np.complex128)
    for c, r in [(cfg.c0, cfg.r0), (cfg.c1, cfg.r1)]:
        p[idx(c, r, cfg), idx(c, r, cfg)] = 1.0
    return p


def arm_metrics(rho: np.ndarray, cfg: Config) -> Dict[str, float]:
    rho_c = ptrace(rho, "C", cfg)
    rho_r = ptrace(rho, "R", cfg)
    return {
        "module_negativity_CR": negativity(rho, cfg),
        "block_S2_C": s2(rho_c),
        "block_S2_R": s2(rho_r),
        "throughput_joint": float(np.real(np.trace(joint_projector(cfg) @ rho))),
        "same_pair_population": float(np.real(np.trace(same_projector(cfg) @ rho))),
    }


def mdiff(a: np.ndarray, b: np.ndarray, cfg: Config) -> Dict[str, float]:
    ac, ar = ptrace(a, "C", cfg), ptrace(a, "R", cfg)
    bc, br = ptrace(b, "C", cfg), ptrace(b, "R", cfg)
    return {
        "C_fro": float(np.linalg.norm(ac - bc)),
        "R_fro": float(np.linalg.norm(ar - br)),
    }


def rf(x: float) -> float:
    return round(float(x), 12)


def theta_grid() -> List[float]:
    return [0.0, math.pi/12, math.pi/8, math.pi/6, math.pi/4, math.pi/3, 3*math.pi/8, 5*math.pi/12, math.pi/2]


def run(seed: int = 0) -> Dict[str, Any]:
    # Seed retained for reproducibility interface; this experiment is deterministic.
    _ = np.random.default_rng(seed)
    cfg = Config(seed=seed)
    rows: List[Dict[str, Any]] = []

    for th in theta_grid():
        ent = proj(state(th, cfg))
        deph = dephase(ent)
        prod = product_marginals(ent, cfg)
        arms = {
            "entangled_event": ent,
            "dephased_correlated": deph,
            "product_marginals": prod,
        }
        summaries = {name: arm_metrics(rho, cfg) for name, rho in arms.items()}
        audit_deph = mdiff(ent, deph, cfg)
        audit_prod = mdiff(ent, prod, cfg)
        bonus_deph = summaries["entangled_event"]["throughput_joint"] - summaries["dephased_correlated"]["throughput_joint"]
        bonus_prod = summaries["entangled_event"]["throughput_joint"] - summaries["product_marginals"]["throughput_joint"]
        neg = summaries["entangled_event"]["module_negativity_CR"]

        for name, met in summaries.items():
            row: Dict[str, Any] = {
                "theta": rf(th),
                "theta_over_pi": rf(th / math.pi),
                "arm": name,
                **{k: rf(v) for k, v in met.items()},
                "marginal_diff_vs_entangled_C_fro": 0.0,
                "marginal_diff_vs_entangled_R_fro": 0.0,
                "throughput_bonus_vs_dephased": "",
                "throughput_bonus_vs_product": "",
                "bonus_minus_negativity": "",
            }
            if name == "dephased_correlated":
                row["marginal_diff_vs_entangled_C_fro"] = rf(audit_deph["C_fro"])
                row["marginal_diff_vs_entangled_R_fro"] = rf(audit_deph["R_fro"])
            elif name == "product_marginals":
                row["marginal_diff_vs_entangled_C_fro"] = rf(audit_prod["C_fro"])
                row["marginal_diff_vs_entangled_R_fro"] = rf(audit_prod["R_fro"])
            elif name == "entangled_event":
                row["throughput_bonus_vs_dephased"] = rf(bonus_deph)
                row["throughput_bonus_vs_product"] = rf(bonus_prod)
                row["bonus_minus_negativity"] = rf(bonus_deph - neg)
            rows.append(row)

    return {
        "experiment": "quantum_coupled_microreactor_step1_CR",
        "date": "2026-07-07",
        "layer": "quantum-audit",
        "model": "6-qubit C-R module bond; 3 qubits per module; deterministic density-matrix calculation",
        "seed": seed,
        "config": asdict(cfg),
        "rows": rows,
        "limitations": [
            "Designed joint analyzer for C-R module bond, not a full microreactor.",
            "No source, membrane, or sink dynamics are included.",
            "No nonlocal signaling claim; all effects are joint-state/analyzer effects.",
            "Classical correlated dephased control is explicitly included and nonzero.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/step1_cr_coupling_seed0.json"))
    parser.add_argument("--csv", type=Path, default=Path("data/quantum_microreactor/step1_cr_coupling_seed0_summary.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result, args.csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
