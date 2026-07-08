#!/usr/bin/env python3
"""
Information microreactor whole-state quantum sandbox.

Layer: classical-effective / whole-state quantumization audit

Purpose:
    Coarse-grain the main sandbox variables into one finite 10-bit/10-qubit
    state and compare classical/dephased finite-state evolution against coherent
    whole-state evolution.

This is not a full continuous-variable quantum microreactor and not a hardware
or quantum-advantage result.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np


@dataclass(frozen=True)
class Config:
    seed: int = 20260707
    steps: int = 200
    burn: int = 40
    qubits: Tuple[str, ...] = ("A", "M", "C", "R", "O", "Q", "B", "T", "D", "S")


NAMES = ("A", "M", "C", "R", "O", "Q", "B", "T", "D", "S")
IDX = {name: i for i, name in enumerate(NAMES)}
N = len(NAMES)
DIM = 1 << N
BIT_CACHE = np.zeros((DIM, N), dtype=np.int8)
for _i in range(DIM):
    for _q in range(N):
        BIT_CACHE[_i, _q] = (_i >> (N - 1 - _q)) & 1

PAIR_CACHE: Dict[Tuple[int, Tuple[Tuple[int, int], ...]], Tuple[np.ndarray, np.ndarray]] = {}
XX_PAIR_CACHE: Dict[Tuple[int, int], Tuple[np.ndarray, np.ndarray]] = {}

GLOBAL_PAIRS = [
    (IDX["A"], IDX["M"]),
    (IDX["M"], IDX["C"]),
    (IDX["C"], IDX["R"]),
    (IDX["R"], IDX["O"]),
    (IDX["O"], IDX["Q"]),
    (IDX["Q"], IDX["B"]),
    (IDX["B"], IDX["T"]),
    (IDX["T"], IDX["D"]),
    (IDX["D"], IDX["S"]),
    (IDX["S"], IDX["A"]),
]


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def bit(i: int, q: int) -> int:
    return (i >> (N - 1 - q)) & 1


def initial(mode: str) -> np.ndarray:
    # Start with membrane open and quality intact: M=1, Q=1.
    index = 0
    for q in (IDX["M"], IDX["Q"]):
        index |= 1 << (N - 1 - q)
    if mode == "coherent_whole_state":
        state = np.zeros(DIM, dtype=np.complex128)
    else:
        state = np.zeros(DIM, dtype=np.float64)
    state[index] = 1.0
    return state


def phase(t: int) -> str:
    if t < 40:
        return "clean"
    if t < 80:
        return "contamination"
    if t < 120:
        return "pressure"
    if t < 160:
        return "stress"
    return "rescue"


def get_pairs(target: int, controls: Sequence[Tuple[int, int]]) -> Tuple[np.ndarray, np.ndarray]:
    key = (target, tuple(controls))
    if key in PAIR_CACHE:
        return PAIR_CACHE[key]
    mask = BIT_CACHE[:, target] == 0
    for q, value in controls:
        mask &= BIT_CACHE[:, q] == value
    lows = np.nonzero(mask)[0]
    highs = lows | (1 << (N - 1 - target))
    PAIR_CACHE[key] = (lows, highs)
    return lows, highs


def apply_ry(state: np.ndarray, target: int, theta: float, controls: Sequence[Tuple[int, int]], coherent: bool) -> np.ndarray:
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    lows, highs = get_pairs(target, controls)
    out = state.copy()
    a = state[lows].copy()
    b = state[highs].copy()
    if coherent:
        out[lows] = c * a - s * b
        out[highs] = s * a + c * b
    else:
        c2 = c * c
        s2 = s * s
        out[lows] = c2 * a + s2 * b
        out[highs] = s2 * a + c2 * b
    return out


def get_xx_pairs(q1: int, q2: int) -> Tuple[np.ndarray, np.ndarray]:
    key = (q1, q2)
    if key in XX_PAIR_CACHE:
        return XX_PAIR_CACHE[key]
    mask = (1 << (N - 1 - q1)) | (1 << (N - 1 - q2))
    lows: List[int] = []
    highs: List[int] = []
    for i in range(DIM):
        j = i ^ mask
        if i < j:
            lows.append(i)
            highs.append(j)
    XX_PAIR_CACHE[key] = (np.array(lows), np.array(highs))
    return XX_PAIR_CACHE[key]


def apply_xx(state: np.ndarray, q1: int, q2: int, theta: float, coherent: bool) -> np.ndarray:
    lows, highs = get_xx_pairs(q1, q2)
    out = state.copy()
    a = state[lows].copy()
    b = state[highs].copy()
    if coherent:
        c = math.cos(theta)
        s = -1j * math.sin(theta)
        out[lows] = c * a + s * b
        out[highs] = s * a + c * b
    else:
        c2 = math.cos(theta) ** 2
        s2 = math.sin(theta) ** 2
        out[lows] = c2 * a + s2 * b
        out[highs] = s2 * a + c2 * b
    return out


def step(state: np.ndarray, t: int, mode: str) -> np.ndarray:
    coherent = mode == "coherent_whole_state"
    ph = phase(t)

    def ry(target_name: str, theta: float, controls: Sequence[Tuple[str, int]] = ()) -> None:
        nonlocal state
        state = apply_ry(state, IDX[target_name], theta, tuple((IDX[name], value) for name, value in controls), coherent)

    source_theta = 0.16 + (0.08 if ph in {"clean", "contamination"} else 0.04)
    ry("A", source_theta)
    ry("A", 0.14, (("T", 1),))

    ry("B", 0.32 if ph == "contamination" else 0.04)
    ry("D", 0.34 if ph == "stress" else 0.04)
    ry("S", 0.36 if ph == "rescue" else 0.03)

    ry("M", 0.18, (("S", 1),))
    ry("M", 0.28, (("D", 1),))
    ry("M", 0.12, (("B", 1),))

    ry("C", 0.30, (("A", 1), ("M", 1), ("Q", 1)))
    ry("C", 0.12, (("B", 1),))

    ry("R", 0.30, (("C", 1), ("M", 1)))
    ry("A", 0.10, (("R", 1),))
    ry("M", 0.10, (("R", 1),))
    ry("C", 0.08, (("R", 1),))

    release_theta = 0.08 if ph == "pressure" else 0.24
    ry("O", release_theta, (("R", 1), ("Q", 1)))

    ry("Q", 0.30, (("B", 1),))
    ry("Q", 0.20, (("D", 1),))
    ry("Q", 0.22, (("S", 1),))

    ry("T", 0.25, (("O", 1), ("Q", 1)))

    coupling = 0.055 if ph == "stress" else 0.045 if ph == "rescue" else 0.035
    for q1, q2 in GLOBAL_PAIRS:
        state = apply_xx(state, q1, q2, coupling, coherent)

    return state


def marginals(state: np.ndarray, mode: str) -> Dict[str, float]:
    probs = np.abs(state) ** 2 if mode == "coherent_whole_state" else state
    out: Dict[str, float] = {}
    for name, q in IDX.items():
        out[name] = float(probs[BIT_CACHE[:, q] == 1].sum())
    out["quality_bad"] = 1.0 - out["Q"]
    out["output_quality"] = out["O"] * out["Q"]
    return out


def simulate(mode: str, cfg: Config) -> List[Dict[str, Any]]:
    state = initial(mode)
    rows: List[Dict[str, Any]] = []
    for t in range(cfg.steps):
        state = step(state, t, mode)
        rows.append({"t": t, "phase": phase(t), **marginals(state, mode)})
    return rows


def summarize(rows: List[Dict[str, Any]], mode: str, cfg: Config) -> Dict[str, Any]:
    post = [row for row in rows if row["t"] >= cfg.burn]

    def mean(key: str) -> float:
        return sum(float(row[key]) for row in post) / len(post)

    final = rows[-1]
    return {
        "mode": mode,
        "mean_output": mean("O"),
        "mean_quality": mean("Q"),
        "mean_output_quality": mean("output_quality"),
        "mean_reservoir": mean("R"),
        "mean_membrane": mean("M"),
        "mean_terrain": mean("T"),
        "final_output": float(final["O"]),
        "final_quality": float(final["Q"]),
        "final_terrain": float(final["T"]),
    }


def event_rows(rows_by_mode: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    specs = [
        ("quality_below_0.7", "Q", "below", 0.7),
        ("quality_below_0.5", "Q", "below", 0.5),
        ("reservoir_above_0.5", "R", "above", 0.5),
        ("membrane_below_0.5", "M", "below", 0.5),
        ("terrain_above_0.5", "T", "above", 0.5),
        ("output_above_0.5", "O", "above", 0.5),
    ]
    out: List[Dict[str, Any]] = []
    for mode, rows in rows_by_mode.items():
        for event, key, direction, threshold in specs:
            hit = None
            for row in rows:
                value = float(row[key])
                if (direction == "below" and value < threshold) or (direction == "above" and value > threshold):
                    hit = row
                    break
            out.append(
                {
                    "mode": mode,
                    "event": event,
                    "threshold": threshold,
                    "time": "" if hit is None else hit["t"],
                    "value": "" if hit is None else float(hit[key]),
                }
            )
    return out


def run(seed: int = 20260707) -> Dict[str, Any]:
    # Seed retained for interface consistency. This model is deterministic.
    _ = np.random.default_rng(seed)
    cfg = Config(seed=seed)
    modes = ["classical_finite_state", "dephased_whole_state", "coherent_whole_state"]
    rows_by_mode = {mode: simulate(mode, cfg) for mode in modes}
    summaries = [{k: (rf(v) if isinstance(v, float) else v) for k, v in summarize(rows, mode, cfg).items()} for mode, rows in rows_by_mode.items()]
    events = [{k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()} for row in event_rows(rows_by_mode)]
    return {
        "experiment": "information_microreactor_whole_state_quantum_sandbox",
        "date": "2026-07-08",
        "layer": "classical-effective / whole-state quantumization audit",
        "seed": seed,
        "config": asdict(cfg),
        "modes": modes,
        "summaries": summaries,
        "events": events,
        "limitations": [
            "Coarse 10-bit/10-qubit whole-state sandbox, not a full continuous-variable quantum microreactor.",
            "Classical finite-state and dephased whole-state modes are expected to match by construction.",
            "Coherent differences are finite-model coherence/interference effects, not hardware results or quantum advantage claims.",
        ],
    }


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--out", type=Path, default=Path("data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_summary.csv"))
    parser.add_argument("--events-csv", type=Path, default=Path("data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_events.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summaries"], args.summary_csv)
    write_csv(result["events"], args.events_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
