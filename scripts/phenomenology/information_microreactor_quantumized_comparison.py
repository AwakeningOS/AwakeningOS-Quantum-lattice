#!/usr/bin/env python3
"""
Information microreactor quantumized comparison.

Layer: classical-effective / quantum-audit boundary

Purpose:
    Compare a classical probability pass-convert-store core against a
    quantum-dephased and quantum-coherent 3-qubit core embedded inside the
    information microreactor sandbox environment.

This is not a full quantumization of all continuous environment variables.
Road, terrain, membrane integrity, contaminant load, reservoir amount,
backpressure, stress/stabilizer, and release remain classical state variables.
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


@dataclass(frozen=True)
class Config:
    seed: int = 20260707
    steps: int = 800
    burn: int = 200


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def scenarios() -> Dict[str, Params]:
    return {
        "normal": Params(),
        "high_load": Params(A_rate=5.0),
        "stress": Params(D_rate=0.45, C_rate=0.0),
        "stabilizer": Params(D_rate=0.45, C_rate=2.0),
        "leaky_membrane": Params(pore_B=0.05, B_rate=0.4),
        "road_fed": Params(road_source_gain=2.0, terrain_write=0.08),
        "storage_heavy": Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
    }


I = np.eye(2, dtype=np.complex128)
P0 = np.diag([1.0, 0.0]).astype(np.complex128)
P1 = np.diag([0.0, 1.0]).astype(np.complex128)
PSI0 = np.zeros(8, dtype=np.complex128)
PSI0[0] = 1.0
RHO0 = np.outer(PSI0, np.conjugate(PSI0))


def ry(theta: float) -> np.ndarray:
    return np.array(
        [[math.cos(theta / 2), -math.sin(theta / 2)], [math.sin(theta / 2), math.cos(theta / 2)]],
        dtype=np.complex128,
    )


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(a, b), c)


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


def dephase(rho: np.ndarray) -> np.ndarray:
    return np.diag(np.diag(rho)).astype(np.complex128)


def angle_from_prob(p: float) -> float:
    p = max(0.0, min(1.0, float(p)))
    return 2.0 * math.asin(math.sqrt(p))


def qcore_product(p_pass: float, p_convert: float, p_store: float, mode: str) -> float:
    if mode == "classical_probability_core":
        return float(p_pass * p_convert * p_store)

    rho = RHO0.copy()
    gates = [
        single_gate(ry(angle_from_prob(p_pass)), 0),
        controlled_gate(0, 1, ry(angle_from_prob(p_convert))),
        controlled_gate(1, 2, ry(angle_from_prob(p_store))),
    ]
    for u in gates:
        rho = u @ rho @ np.conjugate(u).T
        if mode == "quantum_dephased_core":
            rho = dephase(rho)
    if mode not in {"quantum_dephased_core", "quantum_coherent_core"}:
        raise ValueError(f"unknown mode: {mode}")
    return float(np.real(rho[7, 7]))


def simulate(name: str, p: Params, cfg: Config, mode: str) -> Dict[str, Any]:
    inside_B = 0.0
    reservoir = 0.0
    terrain = 0.0
    integrity = 1.0
    rows: List[Dict[str, float]] = []

    for t in range(cfg.steps):
        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / 64.0)
        road_boost = 1.0 + p.road_source_gain * (terrain / (1.0 + terrain))
        source_A = p.A_rate * pulse * road_boost
        source_B = p.B_rate
        D = p.D_rate
        C = p.C_rate

        protect = p.stabilizer_protect * (C / (1.0 + C))
        damage = p.damage_coeff * D * (1.0 - protect)
        repair = p.repair_coeff * C * (1.0 - integrity)
        integrity = min(1.0, max(0.0, integrity - damage + repair))

        fill_frac_pre = reservoir / max(p.capacity, 1e-9)
        backpressure = max(0.02, 1.0 - p.backpressure_strength * fill_frac_pre)
        perm_A = p.pore_A * integrity * backpressure
        perm_B = p.pore_B * integrity * (1.0 + 0.5 * (1.0 - integrity))

        B_in = source_B * perm_B
        inside_B += B_in

        poison = 1.0 / (1.0 + p.poison_coeff * inside_B)
        quality = 1.0 / (1.0 + p.quality_coeff * inside_B)
        conv_rate = p.k_conv * poison * backpressure
        p_store = max(0.0, min(1.0, 1.0 - fill_frac_pre))
        p_pass = max(0.0, min(1.0, perm_A))
        p_convert = max(0.0, min(1.0, conv_rate))
        core_product = qcore_product(p_pass, p_convert, p_store, mode)
        P_generated = source_A * core_product
        A_in = source_A * p_pass

        inside_B *= 0.985
        available = max(0.0, p.capacity - reservoir)
        P_accept = min(P_generated, available)
        overflow = max(0.0, P_generated - available)
        reservoir += P_accept
        release = min(reservoir, reservoir * p.release_rate, p.sink_cap)
        reservoir -= release
        terrain = terrain * p.terrain_decay + release * p.terrain_write * quality

        rows.append(
            {
                "source_A": source_A,
                "A_in": A_in,
                "B_in": B_in,
                "P_generated": P_generated,
                "release": release,
                "overflow": overflow,
                "reservoir": reservoir,
                "fill_frac": fill_frac_pre,
                "integrity": integrity,
                "terrain": terrain,
                "quality": quality,
                "backpressure": backpressure,
            }
        )

    post = rows[cfg.burn :]

    def total(key: str) -> float:
        return sum(row[key] for row in post)

    def mean(key: str) -> float:
        return total(key) / len(post)

    def std(key: str) -> float:
        m = mean(key)
        return math.sqrt(sum((row[key] - m) ** 2 for row in post) / max(1, len(post) - 1))

    release_cv = std("release") / (mean("release") + 1e-9)
    source_cv = std("source_A") / (mean("source_A") + 1e-9)

    return {
        "scenario": name,
        "mode": mode,
        "source_A_total": total("source_A"),
        "A_in_total": total("A_in"),
        "P_generated": total("P_generated"),
        "P_release": total("release"),
        "mean_reservoir": mean("reservoir"),
        "mean_fill_fraction": mean("reservoir") / p.capacity,
        "mean_backpressure": mean("backpressure"),
        "final_integrity": rows[-1]["integrity"],
        "mean_quality": mean("quality"),
        "terrain_written": rows[-1]["terrain"],
        "release_cv": release_cv,
        "source_cv": source_cv,
        "smoothing_ratio": release_cv / (source_cv + 1e-9),
    }


def run(seed: int = 20260707) -> Dict[str, Any]:
    # Seed retained for interface consistency. This simulation is deterministic.
    _ = np.random.default_rng(seed)
    cfg = Config(seed=seed)
    modes = ["classical_probability_core", "quantum_dephased_core", "quantum_coherent_core"]
    rows: List[Dict[str, Any]] = []

    for scenario, params in scenarios().items():
        scenario_rows = [simulate(scenario, params, cfg, mode) for mode in modes]
        classical = scenario_rows[0]
        dephased = scenario_rows[1]
        for row in scenario_rows:
            row["diff_P_release_vs_classical"] = row["P_release"] - classical["P_release"]
            row["diff_P_generated_vs_classical"] = row["P_generated"] - classical["P_generated"]
            row["diff_terrain_vs_classical"] = row["terrain_written"] - classical["terrain_written"]
            row["diff_P_release_vs_dephased"] = row["P_release"] - dephased["P_release"]
            rows.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})

    return {
        "experiment": "information_microreactor_quantumized_comparison",
        "date": "2026-07-08",
        "layer": "classical-effective / quantum-audit boundary",
        "seed": seed,
        "config": asdict(cfg),
        "modes": modes,
        "summaries": rows,
        "limitations": [
            "Only the finite M/C/R pass-convert-store core is quantumized.",
            "Road, terrain, integrity, contaminant, quality, reservoir amount, backpressure, stress/stabilizer, and release remain classical variables.",
            "Diagonal product-population readout is used.",
            "No quantum advantage or quantum-specific sandbox behavior is claimed.",
        ],
    }


def write_csv(result: Dict[str, Any], path: Path) -> None:
    rows = result["summaries"]
    fields = list(rows[0].keys())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--out", type=Path, default=Path("data/microreactor/information_microreactor_quantumized_comparison_seed20260707.json"))
    parser.add_argument("--csv", type=Path, default=Path("data/microreactor/information_microreactor_quantumized_comparison_seed20260707_summary.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result, args.csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
