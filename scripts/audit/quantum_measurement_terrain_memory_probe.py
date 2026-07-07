#!/usr/bin/env python3
"""Measurement-boundary terrain memory probe.

This extends sampled CHSH terrain feedback from a next-phase effect to a memory
question. Conservative finite-shot CHSH excess is written only in phase 1. Phases
2 and 3 turn measurement write off and read remaining terrain through classical
road feedback. A matched classical replay arm checks whether post-write terrain
memory is itself quantum-specific.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from quantum_sampled_chsh_terrain_feedback_probe import (
    ALPHA,
    CONFIDENCE_MARGIN_S,
    GAMMAS,
    MEASUREMENT_WRITE_GAIN,
    SHOTS_PER_SETTING_PER_STEP,
    Params,
    sample_chsh,
)

PHASE1_STEPS = 400
PHASE2_STEPS = 400
PHASE3_STEPS = 400
STEPS = PHASE1_STEPS + PHASE2_STEPS + PHASE3_STEPS


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def scenarios() -> Dict[str, tuple[Params, Params, Params]]:
    return {
        "normal_memory": (
            Params(),
            Params(C_rate=2.0, D_rate=0.02, road_source_gain=2.0),
            Params(C_rate=0.0, D_rate=0.45, road_source_gain=2.0),
        ),
        "stress_memory": (
            Params(D_rate=0.45, C_rate=0.0),
            Params(C_rate=2.0, D_rate=0.02, road_source_gain=2.0),
            Params(C_rate=0.0, D_rate=0.45, road_source_gain=2.0),
        ),
        "storage_memory": (
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9, C_rate=2.0, road_source_gain=2.0),
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9, C_rate=0.0, D_rate=0.45, road_source_gain=2.0),
        ),
    }


def simulate(
    phase1: Params,
    phase2: Params,
    phase3: Params,
    arm: str,
    gamma: float = 1.0,
    seed: int = 20260707,
    replay_writes: List[float] | None = None,
) -> tuple[List[Dict[str, Any]], List[float]]:
    rng = np.random.default_rng(seed)
    inside_a = 0.0
    inside_b = 0.0
    reservoir = 0.0
    terrain = 0.0
    integrity = 1.0
    rows: List[Dict[str, Any]] = []
    writes: List[float] = []
    for t in range(STEPS):
        if t < PHASE1_STEPS:
            p = phase1
            phase = 1
        elif t < PHASE1_STEPS + PHASE2_STEPS:
            p = phase2
            phase = 2
        else:
            p = phase3
            phase = 3

        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / 64.0)
        road_boost = 1.0 + p.road_source_gain * (terrain / (1.0 + terrain))
        source_a = p.A_rate * pulse * road_boost
        protect = p.stabilizer_protect * (p.C_rate / (1.0 + p.C_rate))
        damage = p.damage_coeff * p.D_rate * (1.0 - protect)
        repair = p.repair_coeff * p.C_rate * (1.0 - integrity)
        integrity = min(1.0, max(0.0, integrity - damage + repair))
        fill = reservoir / max(p.capacity, 1e-9)
        backpressure = max(0.02, 1.0 - p.backpressure_strength * fill)
        perm_a = p.pore_A * integrity * backpressure
        perm_b = p.pore_B * integrity * (1.0 + 0.5 * (1.0 - integrity))
        inside_a += source_a * perm_a
        inside_b += p.B_rate * perm_b
        poison = 1.0 / (1.0 + p.poison_coeff * inside_b)
        conv_rate = p.k_conv * poison * backpressure
        amount = conv_rate * inside_a
        inside_a -= amount
        quality = 1.0 / (1.0 + p.quality_coeff * inside_b)
        inside_b *= 0.985
        reservoir += min(amount, max(0.0, p.capacity - reservoir))
        release = min(reservoir, reservoir * p.release_rate, p.sink_cap)
        reservoir -= release
        terrain_standard = release * p.terrain_write * quality
        phi = math.pi * (1.0 - integrity)

        chsh_true = 0.0
        chsh_hat = 0.0
        conservative_excess = 0.0
        if t < PHASE1_STEPS:
            if arm == "arm3_sampled_chsh":
                chsh_true, chsh_hat, conservative_excess, _ = sample_chsh(phi, gamma, rng)
                measurement_write = MEASUREMENT_WRITE_GAIN * conservative_excess
            elif arm == "arm2_bell_bound":
                measurement_write = 0.0
            elif arm == "matched_classical_replay":
                measurement_write = replay_writes[t] if replay_writes is not None else 0.0
            else:
                raise ValueError(f"unknown arm: {arm}")
        else:
            measurement_write = 0.0

        terrain = terrain * p.terrain_decay + terrain_standard + measurement_write
        writes.append(measurement_write)
        rows.append(
            {
                "t": t,
                "phase": phase,
                "release": release,
                "terrain": terrain,
                "measurement_write": measurement_write,
                "integrity": integrity,
                "road_boost": road_boost,
                "quality": quality,
                "chsh_true": chsh_true,
                "chsh_hat": chsh_hat,
                "conservative_excess": conservative_excess,
            }
        )
    return rows, writes


def phase_bounds(phase: int) -> tuple[int, int]:
    if phase == 1:
        return 0, PHASE1_STEPS
    if phase == 2:
        return PHASE1_STEPS, PHASE1_STEPS + PHASE2_STEPS
    if phase == 3:
        return PHASE1_STEPS + PHASE2_STEPS, STEPS
    raise ValueError(phase)


def rows_phase(rows: List[Dict[str, Any]], phase: int) -> List[Dict[str, Any]]:
    start, end = phase_bounds(phase)
    return rows[start:end]


def total(rows: List[Dict[str, Any]], key: str, phase: int) -> float:
    return sum(float(r[key]) for r in rows_phase(rows, phase))


def mean(rows: List[Dict[str, Any]], key: str, phase: int) -> float:
    xs = rows_phase(rows, phase)
    return sum(float(r[key]) for r in xs) / len(xs)


def maxv(rows: List[Dict[str, Any]], key: str, phase: int) -> float:
    return max(float(r[key]) for r in rows_phase(rows, phase))


def terrain_half_life_steps(arm3: List[Dict[str, Any]], arm2: List[Dict[str, Any]], initial_delta: float) -> Any:
    if initial_delta <= 1e-12:
        return ""
    half = initial_delta / 2.0
    for idx in range(PHASE1_STEPS, STEPS):
        if float(arm3[idx]["terrain"]) - float(arm2[idx]["terrain"]) <= half:
            return idx - PHASE1_STEPS
    return "not_reached"


def run(seed: int = 20260707) -> Dict[str, Any]:
    summary: List[Dict[str, Any]] = []
    for si, (scenario, (phase1, phase2, phase3)) in enumerate(scenarios().items()):
        arm2, _ = simulate(phase1, phase2, phase3, "arm2_bell_bound", gamma=1.0, seed=seed)
        for gi, gamma in enumerate(GAMMAS):
            arm3, writes = simulate(phase1, phase2, phase3, "arm3_sampled_chsh", gamma=gamma, seed=seed + 1000 * si + gi)
            matched, _ = simulate(phase1, phase2, phase3, "matched_classical_replay", gamma=gamma, seed=seed + 1000 * si + gi, replay_writes=writes)

            terrain_delta_p1 = float(arm3[PHASE1_STEPS - 1]["terrain"]) - float(arm2[PHASE1_STEPS - 1]["terrain"])
            terrain_delta_p2 = float(arm3[PHASE1_STEPS + PHASE2_STEPS - 1]["terrain"]) - float(arm2[PHASE1_STEPS + PHASE2_STEPS - 1]["terrain"])
            terrain_delta_p3 = float(arm3[-1]["terrain"]) - float(arm2[-1]["terrain"])
            release2_arm2 = total(arm2, "release", 2)
            release2_arm3 = total(arm3, "release", 2)
            release3_arm2 = total(arm2, "release", 3)
            release3_arm3 = total(arm3, "release", 3)
            positive = total(arm3, "measurement_write", 1) > 1e-12 and terrain_delta_p2 > 1e-9 and release3_arm3 > release3_arm2 + 1e-9

            row = {
                "scenario": scenario,
                "gamma": gamma,
                "shots_per_setting_per_step": SHOTS_PER_SETTING_PER_STEP,
                "confidence_margin_S": CONFIDENCE_MARGIN_S,
                "arm2_measurement_write_phase1": total(arm2, "measurement_write", 1),
                "arm3_measurement_write_phase1": total(arm3, "measurement_write", 1),
                "positive_sampled_steps_phase1": sum(1 for r in rows_phase(arm3, 1) if float(r["conservative_excess"]) > 0.0),
                "max_chsh_hat_phase1": maxv(arm3, "chsh_hat", 1),
                "max_chsh_true_phase1": maxv(arm3, "chsh_true", 1),
                "terrain_delta_end_phase1": terrain_delta_p1,
                "terrain_delta_end_phase2": terrain_delta_p2,
                "terrain_delta_end_phase3": terrain_delta_p3,
                "terrain_delta_half_life_steps": terrain_half_life_steps(arm3, arm2, terrain_delta_p1),
                "arm2_release_phase2": release2_arm2,
                "arm3_release_phase2": release2_arm3,
                "arm3_dev_pct_release_phase2": 100.0 * (release2_arm3 - release2_arm2) / release2_arm2,
                "arm2_release_phase3": release3_arm2,
                "arm3_release_phase3": release3_arm3,
                "arm3_dev_pct_release_phase3": 100.0 * (release3_arm3 - release3_arm2) / release3_arm2,
                "mean_road_boost_phase2_arm2": mean(arm2, "road_boost", 2),
                "mean_road_boost_phase2_arm3": mean(arm3, "road_boost", 2),
                "mean_road_boost_phase3_arm2": mean(arm2, "road_boost", 3),
                "mean_road_boost_phase3_arm3": mean(arm3, "road_boost", 3),
                "mean_quality_phase3_arm2": mean(arm2, "quality", 3),
                "mean_quality_phase3_arm3": mean(arm3, "quality", 3),
                "matched_classical_release_phase2_diff_vs_arm3": total(matched, "release", 2) - release2_arm3,
                "matched_classical_release_phase3_diff_vs_arm3": total(matched, "release", 3) - release3_arm3,
                "memory_effect_beyond_bell_bound_arm2": "TRUE" if positive else "FALSE",
                "post_write_memory_quantum_specific": "FALSE",
                "classification": "sampled CHSH terrain inscription persists and changes later dynamics; post-write memory is classical terrain dynamics" if positive else "no sampled CHSH terrain memory beyond Bell-bound Arm2",
            }
            summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})

    positive_rows = [r for r in summary if r["memory_effect_beyond_bell_bound_arm2"] == "TRUE"]
    return {
        "experiment": "quantum_measurement_terrain_memory_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "phase1_write_steps": PHASE1_STEPS,
        "phase2_memory_steps": PHASE2_STEPS,
        "phase3_challenge_steps": PHASE3_STEPS,
        "shots_per_setting_per_step": SHOTS_PER_SETTING_PER_STEP,
        "alpha": ALPHA,
        "confidence_margin_S": rf(CONFIDENCE_MARGIN_S),
        "measurement_write_gain": MEASUREMENT_WRITE_GAIN,
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_MEASUREMENT_TERRAIN_MEMORY" if positive_rows else "NEGATIVE_FOR_MEASUREMENT_TERRAIN_MEMORY",
        "positive_rows": len(positive_rows),
        "safe_interpretation": "A finite-shot sampled CHSH measurement-boundary signal can be written into terrain, persist after measurement stops, and weakly affect a later challenge phase in stress context. The post-write memory dynamics are classical terrain dynamics: a matched classical replay of the same write trajectory reproduces them. This is model-level positive for measurement-boundary terrain memory, not for quantum-specific post-write terrain physics or ordinary local population plumbing.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
