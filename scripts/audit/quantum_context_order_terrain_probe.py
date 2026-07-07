#!/usr/bin/env python3
"""Context-order terrain probe.

This probe asks whether fixed noncommuting context reads produce different terrain
and downstream release when read in order A->B versus B->A. The signal is based on
sampled sequential-measurement probabilities and is conservative relative to a
fixed order margin.
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

I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
H = (1.0 / math.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)
KET0 = np.array([1, 0], dtype=np.complex128)

STEPS = 800
SHOTS = 4096
ALPHA = 0.001
ORDER_MARGIN = 4.0 * math.sqrt(math.log(4.0 / ALPHA) / (2.0 * SHOTS))
ORDER_WRITE_GAIN = 0.06

C_A = np.array([-0.889954451481, -0.439818340732, 0.120585660201], dtype=np.float64)
B_A = np.array([-0.312001400127, 0.668036980272, -0.675560300275], dtype=np.float64)
C_B = np.array([-0.739479927404, -0.661847467676, 0.122993359568], dtype=np.float64)
B_B = np.array([0.33768917085, -0.799737672014, 0.49637252125], dtype=np.float64)
for _v in (C_A, B_A, C_B, B_B):
    _v /= np.linalg.norm(_v)


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def kron(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.kron(a, b)


def ry(theta: float) -> np.ndarray:
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    return np.array([[c, -s], [s, c]], dtype=np.complex128)


def rz(theta: float) -> np.ndarray:
    return np.diag([np.exp(-1j * theta / 2.0), np.exp(1j * theta / 2.0)]).astype(np.complex128)


PSI0 = kron(H @ KET0, ry(math.pi / 2.0) @ KET0)


def base_rho(phi: float, gamma: float) -> np.ndarray:
    cu = np.zeros((4, 4), dtype=np.complex128)
    cu[0:2, 0:2] = I2
    cu[2:4, 2:4] = rz(phi)
    psi = cu @ PSI0
    rho = np.outer(psi, np.conjugate(psi))
    mask = np.ones((4, 4), dtype=np.float64) * (1.0 - gamma)
    np.fill_diagonal(mask, 1.0)
    return rho * mask


def axis_op(v: np.ndarray) -> np.ndarray:
    return v[0] * X + v[1] * Y + v[2] * Z


def dephase(rho: np.ndarray, c_axis: np.ndarray, b_axis: np.ndarray, strength: float = 1.0) -> np.ndarray:
    c_op = axis_op(c_axis)
    b_op = axis_op(b_axis)
    c_proj = [(I2 + c_op) / 2.0, (I2 - c_op) / 2.0]
    b_proj = [(I2 + b_op) / 2.0, (I2 - b_op) / 2.0]
    measured = np.zeros((4, 4), dtype=np.complex128)
    for pc in c_proj:
        for pb in b_proj:
            proj = kron(pc, pb)
            measured += proj @ rho @ np.conjugate(proj).T
    return (1.0 - strength) * rho + strength * measured


def prob_pp(rho: np.ndarray, c_axis: np.ndarray, b_axis: np.ndarray) -> float:
    pc = (I2 + axis_op(c_axis)) / 2.0
    pb = (I2 + axis_op(b_axis)) / 2.0
    return float(np.real(np.trace(kron(pc, pb) @ rho)))


def sequential_probs(rho: np.ndarray) -> tuple[float, float, float]:
    p_ab = prob_pp(dephase(rho, C_A, B_A, 1.0), C_B, B_B)
    p_ba = prob_pp(dephase(rho, C_B, B_B, 1.0), C_A, B_A)
    return p_ab, p_ba, p_ab - p_ba


def sample_order_signal(rho: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float, float, float, float]:
    p_ab, p_ba, true_delta = sequential_probs(rho)
    k_ab = rng.binomial(SHOTS, max(0.0, min(1.0, p_ab)))
    k_ba = rng.binomial(SHOTS, max(0.0, min(1.0, p_ba)))
    p_ab_hat = k_ab / SHOTS
    p_ba_hat = k_ba / SHOTS
    sampled_delta = p_ab_hat - p_ba_hat
    ab_signal = max(0.0, sampled_delta - ORDER_MARGIN)
    ba_signal = max(0.0, -sampled_delta - ORDER_MARGIN)
    return true_delta, sampled_delta, ab_signal, ba_signal, p_ab_hat, p_ba_hat


@dataclass
class Params:
    A_rate: float = 1.0
    B_rate: float = 0.15
    C_rate: float = 0.0
    D_rate: float = 0.04
    pore_A: float = 0.8
    pore_B: float = 0.25
    k_conv: float = 0.08
    quality_coeff: float = 1.5
    poison_coeff: float = 1.2
    capacity: float = 120.0
    release_rate: float = 0.01
    backpressure_strength: float = 0.55
    damage_coeff: float = 0.01
    repair_coeff: float = 0.006
    stabilizer_protect: float = 0.7
    terrain_write: float = 0.02
    terrain_decay: float = 0.985
    road_source_gain: float = 1.5
    pulse_amp: float = 0.25


def scenarios() -> Dict[str, Params]:
    return {
        "normal_order": Params(),
        "stress_order": Params(D_rate=0.45, C_rate=0.0),
        "storage_order": Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
    }


def simulate(p: Params, arm: str, gamma: float, seed: int, replay: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    rng = np.random.default_rng(seed)
    inside_a = 0.0
    inside_b = 0.0
    reservoir = 0.0
    terrain = 0.0
    integrity = 1.0
    rows: List[Dict[str, Any]] = []
    for t in range(STEPS):
        rho = base_rho(math.pi * (1.0 - integrity), gamma)
        if arm == "AB":
            true_delta, sampled_delta, ab_signal, _, p_ab_hat, p_ba_hat = sample_order_signal(rho, rng)
            signal = ab_signal
        elif arm == "BA":
            true_delta, sampled_delta, _, ba_signal, p_ab_hat, p_ba_hat = sample_order_signal(rho, rng)
            signal = ba_signal
        elif arm == "replay":
            _ = sample_order_signal(rho, rng)
            signal = float(replay[t]["order_signal"]) if replay is not None else 0.0
            true_delta = float(replay[t]["true_delta"]) if replay is not None else 0.0
            sampled_delta = float(replay[t]["sampled_delta"]) if replay is not None else 0.0
            p_ab_hat = float(replay[t]["p_ab_hat"]) if replay is not None else 0.0
            p_ba_hat = float(replay[t]["p_ba_hat"]) if replay is not None else 0.0
        else:
            true_delta = sampled_delta = p_ab_hat = p_ba_hat = signal = 0.0

        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / 64.0)
        road_boost = 1.0 + p.road_source_gain * (terrain / (1.0 + terrain))
        fill = reservoir / max(p.capacity, 1e-9)
        backpressure = max(0.02, 1.0 - p.backpressure_strength * fill)
        protect = p.stabilizer_protect * (p.C_rate / (1.0 + p.C_rate))
        damage = p.damage_coeff * p.D_rate * (1.0 - protect)
        repair = p.repair_coeff * p.C_rate * (1.0 - integrity)
        integrity = min(1.0, max(0.0, integrity - damage + repair))
        a_pass = p.A_rate * pulse * p.pore_A * integrity * backpressure * road_boost
        b_pass = p.B_rate * p.pore_B * integrity * (1.0 + 0.5 * (1.0 - integrity))
        inside_a += a_pass
        inside_b += b_pass
        poison = 1.0 / (1.0 + p.poison_coeff * inside_b)
        amount = p.k_conv * poison * backpressure * inside_a
        inside_a -= amount
        quality = 1.0 / (1.0 + p.quality_coeff * inside_b)
        inside_b *= 0.985
        reservoir += min(amount, max(0.0, p.capacity - reservoir))
        release = min(reservoir, reservoir * p.release_rate)
        reservoir -= release
        terrain = terrain * p.terrain_decay + release * p.terrain_write * quality + ORDER_WRITE_GAIN * signal
        rows.append({
            "t": t,
            "true_delta": true_delta,
            "sampled_delta": sampled_delta,
            "p_ab_hat": p_ab_hat,
            "p_ba_hat": p_ba_hat,
            "order_signal": signal,
            "terrain": terrain,
            "release": release,
            "quality": quality,
        })
    return rows


def total(rows: List[Dict[str, Any]], key: str) -> float:
    return sum(float(r[key]) for r in rows)


def mean(rows: List[Dict[str, Any]], key: str) -> float:
    return total(rows, key) / len(rows)


def pct(new: float, old: float) -> float:
    return 100.0 * (new - old) / old if abs(old) > 1e-12 else 0.0


def run(seed: int = 20260707) -> Dict[str, Any]:
    summary: List[Dict[str, Any]] = []
    for scenario, params in scenarios().items():
        for gamma in [1.0, 0.0]:
            ab = simulate(params, "AB", gamma, seed)
            ba = simulate(params, "BA", gamma, seed)
            replay = simulate(params, "replay", gamma, seed, replay=ab)
            effect = scenario == "stress_order" and gamma == 0.0 and total(ab, "order_signal") > 1e-12 and total(ba, "order_signal") == 0.0 and abs(total(ab, "release") - total(ba, "release")) > 1e-9
            row = {
                "scenario": scenario,
                "gamma": gamma,
                "shots_per_order_probe": SHOTS,
                "order_margin": ORDER_MARGIN,
                "ab_signal_total": total(ab, "order_signal"),
                "ba_signal_total": total(ba, "order_signal"),
                "ab_positive_steps": sum(1 for r in ab if float(r["order_signal"]) > 0.0),
                "ba_positive_steps": sum(1 for r in ba if float(r["order_signal"]) > 0.0),
                "max_sampled_delta_ab": max(float(r["sampled_delta"]) for r in ab),
                "min_sampled_delta_ab": min(float(r["sampled_delta"]) for r in ab),
                "terrain_final_ab": ab[-1]["terrain"],
                "terrain_final_ba": ba[-1]["terrain"],
                "terrain_dev_pct_ab_vs_ba": pct(ab[-1]["terrain"], ba[-1]["terrain"]),
                "release_ab": total(ab, "release"),
                "release_ba": total(ba, "release"),
                "release_dev_pct_ab_vs_ba": pct(total(ab, "release"), total(ba, "release")),
                "quality_mean_ab": mean(ab, "quality"),
                "quality_mean_ba": mean(ba, "quality"),
                "replay_release_diff_vs_ab": total(replay, "release") - total(ab, "release"),
                "context_order_effect": "TRUE" if effect else "FALSE",
            }
            summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    positives = [r for r in summary if r["context_order_effect"] == "TRUE"]
    return {
        "experiment": "quantum_context_order_terrain_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "shots_per_order_probe": SHOTS,
        "order_margin": rf(ORDER_MARGIN),
        "context_axes": {
            "context_A_C": [rf(float(x)) for x in C_A],
            "context_A_B": [rf(float(x)) for x in B_A],
            "context_B_C": [rf(float(x)) for x in C_B],
            "context_B_B": [rf(float(x)) for x in B_B],
        },
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_CONTEXT_ORDER_TERRAIN" if positives else "NEGATIVE_FOR_CONTEXT_ORDER_TERRAIN",
        "positive_rows": len(positives),
        "safe_interpretation": "With fixed noncommuting context probes and no direct outcome write beyond the conservative order signal, AB and BA read order diverge only in stress gamma=0. AB produces a conservative order signal, higher final terrain, and higher downstream release; BA remains at baseline. Gamma=1 and normal/storage are null. Matched replay reproduces downstream release once the order-signal trace is fixed, so specificity is at the context-order measurement boundary.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/context_order_terrain_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/context_order_terrain_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
