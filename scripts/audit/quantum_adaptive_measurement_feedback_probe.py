#!/usr/bin/env python3
"""Adaptive measurement-boundary feedback probe.

Phase 1 writes conservative finite-shot CHSH excess into terrain. Later phases turn
writeback off, but terrain memory shifts the adaptive measurement context and a
conservative sampled CHSH excess opens an adaptive gate. This tests whether the
terrain memory becomes part of an adaptive measurement/readout loop.
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
ADAPTIVE_PHASE_GAIN = 1.25
ADAPTIVE_GATE_GAIN = 0.18


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def scenarios() -> Dict[str, tuple[Params, Params, Params]]:
    return {
        "normal_adaptive": (
            Params(),
            Params(C_rate=2.0, D_rate=0.02, road_source_gain=2.0),
            Params(C_rate=0.0, D_rate=0.45, road_source_gain=2.0),
        ),
        "stress_adaptive": (
            Params(D_rate=0.45, C_rate=0.0),
            Params(C_rate=2.0, D_rate=0.02, road_source_gain=2.0),
            Params(C_rate=0.0, D_rate=0.45, road_source_gain=2.0),
        ),
        "storage_adaptive": (
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9),
            Params(capacity=40.0, release_rate=0.003, backpressure_strength=0.9, C_rate=2.0, D_rate=0.02, road_source_gain=2.0),
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
        phi_pre = math.pi * (1.0 - integrity)
        adaptive_phase_shift = ADAPTIVE_PHASE_GAIN * (terrain / (1.0 + terrain)) if phase >= 2 else 0.0
        adaptive_chsh_true = 0.0
        adaptive_chsh_hat = 0.0
        adaptive_excess = 0.0
        adaptive_gate = 1.0
        if arm in {"arm3_adaptive_chsh", "matched_classical_replay"} and phase >= 2:
            adaptive_chsh_true, adaptive_chsh_hat, adaptive_excess, _ = sample_chsh(min(math.pi, phi_pre + adaptive_phase_shift), gamma, rng)
            adaptive_gate = 1.0 + ADAPTIVE_GATE_GAIN * adaptive_excess

        source_a = p.A_rate * pulse * road_boost * adaptive_gate
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

        measurement_write = 0.0
        if phase == 1:
            phi = math.pi * (1.0 - integrity)
            if arm == "arm3_adaptive_chsh":
                _, _, conservative_excess, _ = sample_chsh(phi, gamma, rng)
                measurement_write = MEASUREMENT_WRITE_GAIN * conservative_excess
            elif arm == "matched_classical_replay":
                # consume the same random sample to keep later adaptive sampling aligned
                _ = sample_chsh(phi, gamma, rng)
                measurement_write = replay_writes[t] if replay_writes is not None else 0.0
            elif arm == "arm2_bell_bound":
                measurement_write = 0.0
            else:
                raise ValueError(f"unknown arm: {arm}")

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
                "adaptive_phase_shift": adaptive_phase_shift,
                "adaptive_gate": adaptive_gate,
                "adaptive_chsh_true": adaptive_chsh_true,
                "adaptive_chsh_hat": adaptive_chsh_hat,
                "adaptive_conservative_excess": adaptive_excess,
            }
        )
    return rows, writes


def rows_phase(rows: List[Dict[str, Any]], phase: int) -> List[Dict[str, Any]]:
    return [r for r in rows if int(r["phase"]) == phase]


def total(rows: List[Dict[str, Any]], key: str, phase: int) -> float:
    return sum(float(r[key]) for r in rows_phase(rows, phase))


def mean(rows: List[Dict[str, Any]], key: str, phase: int) -> float:
    xs = rows_phase(rows, phase)
    return sum(float(r[key]) for r in xs) / len(xs)


def maxv(rows: List[Dict[str, Any]], key: str, phase: int) -> float:
    return max(float(r[key]) for r in rows_phase(rows, phase))


def run(seed: int = 20260707) -> Dict[str, Any]:
    summary: List[Dict[str, Any]] = []
    for si, (scenario, (phase1, phase2, phase3)) in enumerate(scenarios().items()):
        arm2, _ = simulate(phase1, phase2, phase3, "arm2_bell_bound", gamma=1.0, seed=seed)
        for gi, gamma in enumerate(GAMMAS):
            arm3, writes = simulate(phase1, phase2, phase3, "arm3_adaptive_chsh", gamma=gamma, seed=seed + 1000 * si + gi)
            replay, _ = simulate(phase1, phase2, phase3, "matched_classical_replay", gamma=gamma, seed=seed + 1000 * si + gi, replay_writes=writes)
            release2_arm2 = total(arm2, "release", 2)
            release2_arm3 = total(arm3, "release", 2)
            release3_arm2 = total(arm2, "release", 3)
            release3_arm3 = total(arm3, "release", 3)
            terrain_delta_p1 = float(arm3[PHASE1_STEPS - 1]["terrain"]) - float(arm2[PHASE1_STEPS - 1]["terrain"])
            terrain_delta_p2 = float(arm3[PHASE1_STEPS + PHASE2_STEPS - 1]["terrain"]) - float(arm2[PHASE1_STEPS + PHASE2_STEPS - 1]["terrain"])
            positive = (
                total(arm3, "measurement_write", 1) > 1e-12
                and (maxv(arm3, "adaptive_conservative_excess", 2) > 0.0 or maxv(arm3, "adaptive_conservative_excess", 3) > 0.0)
                and release2_arm3 > release2_arm2 + 1e-9
            )
            row = {
                "scenario": scenario,
                "gamma": gamma,
                "phase1_measurement_write": total(arm3, "measurement_write", 1),
                "terrain_delta_end_phase1": terrain_delta_p1,
                "terrain_delta_end_phase2": terrain_delta_p2,
                "phase2_adaptive_positive_steps": sum(1 for r in rows_phase(arm3, 2) if float(r["adaptive_conservative_excess"]) > 0.0),
                "phase3_adaptive_positive_steps": sum(1 for r in rows_phase(arm3, 3) if float(r["adaptive_conservative_excess"]) > 0.0),
                "max_adaptive_chsh_hat_phase2": maxv(arm3, "adaptive_chsh_hat", 2),
                "max_adaptive_chsh_hat_phase3": maxv(arm3, "adaptive_chsh_hat", 3),
                "mean_adaptive_gate_phase2_arm2": mean(arm2, "adaptive_gate", 2),
                "mean_adaptive_gate_phase2_arm3": mean(arm3, "adaptive_gate", 2),
                "mean_adaptive_gate_phase3_arm2": mean(arm2, "adaptive_gate", 3),
                "mean_adaptive_gate_phase3_arm3": mean(arm3, "adaptive_gate", 3),
                "arm2_release_phase2": release2_arm2,
                "arm3_release_phase2": release2_arm3,
                "arm3_dev_pct_release_phase2": 100.0 * (release2_arm3 - release2_arm2) / release2_arm2,
                "arm2_release_phase3": release3_arm2,
                "arm3_release_phase3": release3_arm3,
                "arm3_dev_pct_release_phase3": 100.0 * (release3_arm3 - release3_arm2) / release3_arm2,
                "matched_replay_phase2_diff_vs_arm3": total(replay, "release", 2) - release2_arm3,
                "matched_replay_phase3_diff_vs_arm3": total(replay, "release", 3) - release3_arm3,
                "adaptive_loop_effect_beyond_bell_bound_arm2": "TRUE" if positive else "FALSE",
                "post_write_adaptive_dynamics_quantum_specific": "FALSE",
                "classification": "sampled CHSH terrain memory shifts later adaptive measurement gate; replay shows post-write dynamics follow terrain trace" if positive else "no adaptive loop effect beyond Bell-bound Arm2",
            }
            summary.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    positives = [r for r in summary if r["adaptive_loop_effect_beyond_bell_bound_arm2"] == "TRUE"]
    return {
        "experiment": "quantum_adaptive_measurement_feedback_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "adaptive_phase_gain": ADAPTIVE_PHASE_GAIN,
        "adaptive_gate_gain": ADAPTIVE_GATE_GAIN,
        "shots_per_setting_per_step": SHOTS_PER_SETTING_PER_STEP,
        "alpha": ALPHA,
        "confidence_margin_S": rf(CONFIDENCE_MARGIN_S),
        "summary": summary,
        "verdict": "POSITIVE_FOR_MODEL_LEVEL_ADAPTIVE_MEASUREMENT_FEEDBACK" if positives else "NEGATIVE_FOR_ADAPTIVE_MEASUREMENT_FEEDBACK",
        "positive_rows": len(positives),
        "safe_interpretation": "Finite-shot sampled CHSH terrain memory can shift later adaptive measurement/readout gates and alter later reactor output in stress context. The matched replay shows the post-write adaptive dynamics follow the written terrain trace; quantum-specificity remains at the Bell-bound measurement/write/readout boundary, not in ordinary local population plumbing.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707_summary.csv"))
    args = parser.parse_args()
    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
