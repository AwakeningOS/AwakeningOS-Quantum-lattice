#!/usr/bin/env python3
"""
Quantum-coupled information microreactor, Step 2-v2:
unitary C-R conversion dynamics + diagonal population readout.

Layer: quantum-audit

Purpose:
    Test whether a converter-reservoir (C-R) bond changes a functional output
    population after explicit C-R conversion dynamics.

Audit correction:
    Previous Step 2 used a rank-1 coherence/Bell-like conversion effect.
    This version moves coherence sensitivity into the unitary dynamics and reads
    only a diagonal output product population after the dynamics.

This is not a full source->membrane->converter->reservoir->sink reactor.
It is a 6-qubit C-R subexperiment.
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
    out_c: int = 0b011
    out_r: int = 0b100
    c_dim: int = 8
    r_dim: int = 8
    base_rate: float = 0.9
    drain_rate: float = 0.8
    unitary_time: float = 1.0

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


def conversion_unitary(capacity: float, cfg: Config) -> np.ndarray:
    """C-R conversion dynamics.

    Two input branches flow coherently into a common converted product state.
    Final readout is diagonal product population after this unitary.
    """
    g0 = math.sqrt(cfg.base_rate * capacity)
    g1 = math.sqrt(cfg.base_rate * capacity ** 2)
    h = np.zeros((cfg.dim, cfg.dim), dtype=np.complex128)
    a = idx(cfg.c0, cfg.r0, cfg)
    b = idx(cfg.c1, cfg.r1, cfg)
    out = idx(cfg.out_c, cfg.out_r, cfg)
    h[out, a] = h[a, out] = g0
    h[out, b] = h[b, out] = g1
    vals, vecs = np.linalg.eigh(h)
    return vecs @ np.diag(np.exp(-1j * vals * cfg.unitary_time)) @ np.conjugate(vecs).T


def same_pair_population(rho: np.ndarray, cfg: Config) -> float:
    a = idx(cfg.c0, cfg.r0, cfg)
    b = idx(cfg.c1, cfg.r1, cfg)
    return float(np.real(rho[a, a] + rho[b, b]))


def theta_grid() -> List[float]:
    return [0.0, math.pi / 8, math.pi / 4, 3 * math.pi / 8, math.pi / 2]


def capacity_grid() -> List[float]:
    return [1.0, 0.5, 0.1]


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def mdiff(a: np.ndarray, b: np.ndarray, cfg: Config) -> tuple[float, float]:
    ac, ar = ptrace(a, "C", cfg), ptrace(a, "R", cfg)
    bc, br = ptrace(b, "C", cfg), ptrace(b, "R", cfg)
    return float(np.linalg.norm(ac - bc)), float(np.linalg.norm(ar - br))


def arm_metrics(rho: np.ndarray, capacity: float, cfg: Config) -> Dict[str, float]:
    u = conversion_unitary(capacity, cfg)
    rho_out = u @ rho @ np.conjugate(u).T
    out = idx(cfg.out_c, cfg.out_r, cfg)
    product_population = float(np.real(rho_out[out, out]))
    return {
        "module_negativity_CR": negativity(rho, cfg),
        "block_S2_C": s2(ptrace(rho, "C", cfg)),
        "block_S2_R": s2(ptrace(rho, "R", cfg)),
        "product_population_out": product_population,
        "release_probability": product_population * cfg.drain_rate * capacity,
        "same_pair_population_in": same_pair_population(rho, cfg),
    }


def run(seed: int = 0) -> Dict[str, Any]:
    # Seed retained for a stable interface; this deterministic audit uses no sampling.
    _ = np.random.default_rng(seed)
    cfg = Config(seed=seed)
    rows: List[Dict[str, Any]] = []
    cap1_lookup: Dict[tuple[float, str], float] = {}

    for th in theta_grid():
        ent = proj(state(th, cfg))
        arms = {
            "entangled_event": ent,
            "dephased_correlated": dephase(ent),
            "product_marginals": product_marginals(ent, cfg),
        }
        audits = {name: mdiff(ent, rho, cfg) for name, rho in arms.items()}

        for cap in capacity_grid():
            summaries = {name: arm_metrics(rho, cap, cfg) for name, rho in arms.items()}
            for name, met in summaries.items():
                if cap == 1.0:
                    cap1_lookup[(rf(th), name)] = met["product_population_out"]

            ent_pop = summaries["entangled_event"]["product_population_out"]
            deph_pop = summaries["dephased_correlated"]["product_population_out"]
            prod_pop = summaries["product_marginals"]["product_population_out"]

            for name, met in summaries.items():
                base = cap1_lookup.get((rf(th), name), met["product_population_out"])
                row: Dict[str, Any] = {
                    "theta": rf(th),
                    "theta_over_pi": rf(th / math.pi),
                    "capacity": rf(cap),
                    "arm": name,
                    **{k: rf(v) for k, v in met.items()},
                    "marginal_diff_vs_entangled_C_fro": rf(audits[name][0]),
                    "marginal_diff_vs_entangled_R_fro": rf(audits[name][1]),
                    "backpressure_index": rf(1.0 - met["product_population_out"] / base) if base else 0.0,
                    "entangled_population_bonus_vs_dephased": "",
                    "entangled_population_bonus_vs_product": "",
                    "bonus_per_negativity": "",
                }
                if name == "entangled_event":
                    neg = met["module_negativity_CR"]
                    bonus_deph = ent_pop - deph_pop
                    bonus_prod = ent_pop - prod_pop
                    row["entangled_population_bonus_vs_dephased"] = rf(bonus_deph)
                    row["entangled_population_bonus_vs_product"] = rf(bonus_prod)
                    row["bonus_per_negativity"] = rf(bonus_deph / neg) if abs(neg) > 1e-12 else ""
                rows.append(row)

    return {
        "experiment": "quantum_coupled_microreactor_step2_v2_unitary_population",
        "date": "2026-07-07",
        "layer": "quantum-audit",
        "model": "6-qubit C-R unitary conversion dynamics with diagonal product-population readout",
        "seed": seed,
        "config": asdict(cfg),
        "readout": "diagonal product population after unitary dynamics",
        "rows": rows,
        "limitations": [
            "Designed C-R subexperiment, not a full microreactor.",
            "No source, membrane, or sink module dynamics are included.",
            "Coherent conversion dynamics is a designed toy model, not a hardware circuit.",
            "No nonlocal signaling claim.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/step2_v2_unitary_population_seed0.json"))
    parser.add_argument("--csv", type=Path, default=Path("data/quantum_microreactor/step2_v2_unitary_population_seed0_summary.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result, args.csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
