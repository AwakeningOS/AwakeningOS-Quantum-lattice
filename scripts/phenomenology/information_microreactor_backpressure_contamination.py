#!/usr/bin/env python3
"""
Classical-effective information microreactor observation sandbox.

Layer: classical-effective phenomenology

Purpose:
    Extend the information microreactor sandbox from a scenario-summary run into
    a time-resolved observation run. This script combines backpressure,
    contamination, stress, stabilizer rescue, and road/terrain feedback in one
    deterministic timeline and writes summary, event, and timeseries raw logs.

This is not a quantum-witness experiment and makes no quantum-specific claim.
It is not autonomous self-repair, metabolism, or life-like behavior.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

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
    steps: int = 1000
    pulse_period: float = 64.0


@dataclass(frozen=True)
class Phase:
    name: str
    start: int
    end: int
    params: Params
    note: str


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def phases() -> List[Phase]:
    """Return the deterministic v2 observation timeline.

    The phase order is intentionally interpretable rather than optimized:
      1. clean finite reactor
      2. contaminant leakage while flow remains active
      3. storage pressure / low release
      4. stress collapse
      5. stabilizer-assisted recovery
    """
    return [
        Phase(
            "clean_finite_reactor",
            0,
            199,
            Params(capacity=80.0, release_rate=0.025, backpressure_strength=0.75, road_source_gain=1.0, terrain_write=0.06),
            "Clean finite-capacity baseline with mild terrain-fed supply.",
        ),
        Phase(
            "leaky_contamination",
            200,
            399,
            Params(B_rate=0.50, pore_B=0.06, capacity=80.0, release_rate=0.025, backpressure_strength=0.75, road_source_gain=1.0, terrain_write=0.06),
            "B contaminant leaks through the membrane and degrades product quality while throughput can continue.",
        ),
        Phase(
            "storage_pressure",
            400,
            599,
            Params(A_rate=4.0, B_rate=0.40, pore_B=0.05, capacity=18.0, release_rate=0.001, backpressure_strength=1.20, road_source_gain=1.0, terrain_write=0.06),
            "Low release and smaller capacity create reservoir saturation and upstream backpressure.",
        ),
        Phase(
            "stress_collapse",
            600,
            799,
            Params(A_rate=3.0, B_rate=0.30, pore_B=0.04, D_rate=0.45, C_rate=0.0, capacity=18.0, release_rate=0.001, backpressure_strength=1.20, road_source_gain=1.0, terrain_write=0.06),
            "D stress damages membrane integrity without stabilizer input.",
        ),
        Phase(
            "stabilizer_rescue",
            800,
            999,
            Params(B_rate=0.15, pore_B=0.01, D_rate=0.45, C_rate=2.0, capacity=80.0, release_rate=0.020, backpressure_strength=0.75, road_source_gain=1.0, terrain_write=0.06),
            "External C stabilizer partially restores membrane integrity under the same stress load.",
        ),
    ]


def phase_for_t(t: int, timeline: Iterable[Phase]) -> Phase:
    for ph in timeline:
        if ph.start <= t <= ph.end:
            return ph
    raise ValueError(f"no phase defined for t={t}")


def simulate(cfg: Config) -> Tuple[List[Dict[str, Any]], List[Phase]]:
    # Seed retained for interface consistency. This observation run is deterministic.
    _ = np.random.default_rng(cfg.seed)

    inside_A = 0.0
    inside_B = 0.0
    reservoir = 0.0
    integrity = 1.0
    terrain = 0.0
    rows: List[Dict[str, Any]] = []
    timeline = phases()

    for t in range(cfg.steps):
        ph = phase_for_t(t, timeline)
        p = ph.params

        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / cfg.pulse_period)
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
        A_in = source_A * perm_A
        B_in = source_B * perm_B

        inside_A += A_in
        inside_B += B_in

        poison = 1.0 / (1.0 + p.poison_coeff * inside_B)
        conv_rate = p.k_conv * poison * backpressure
        P_generated = min(inside_A, conv_rate * inside_A)
        inside_A -= P_generated

        quality = 1.0 / (1.0 + p.quality_coeff * inside_B)
        inside_B *= 0.985

        available = max(0.0, p.capacity - reservoir)
        P_accept = min(P_generated, available)
        overflow = max(0.0, P_generated - available)
        reservoir += P_accept

        release = min(reservoir, reservoir * p.release_rate, p.sink_cap)
        reservoir -= release

        terrain_write_effective = release * p.terrain_write * quality
        terrain = terrain * p.terrain_decay + terrain_write_effective

        rows.append(
            {
                "t": t,
                "phase": ph.name,
                "source_A": source_A,
                "source_B": source_B,
                "road_boost": road_boost,
                "A_in": A_in,
                "B_in": B_in,
                "P_generated": P_generated,
                "P_accept": P_accept,
                "release": release,
                "quality_weighted_release": release * quality,
                "overflow": overflow,
                "reservoir": reservoir,
                "capacity": p.capacity,
                "fill_frac": fill_frac_pre,
                "integrity": integrity,
                "terrain": terrain,
                "terrain_write_effective": terrain_write_effective,
                "quality": quality,
                "poison": poison,
                "backpressure": backpressure,
                "damage": damage,
                "repair": repair,
                "A_rate": p.A_rate,
                "B_rate": p.B_rate,
                "D_rate": p.D_rate,
                "C_rate": p.C_rate,
                "pore_B": p.pore_B,
                "release_rate": p.release_rate,
                "backpressure_strength": p.backpressure_strength,
            }
        )

    return rows, timeline


def summarize(rows: List[Dict[str, Any]], timeline: List[Phase]) -> List[Dict[str, Any]]:
    summaries: List[Dict[str, Any]] = []

    def total(rs: List[Dict[str, Any]], key: str) -> float:
        return float(sum(float(row[key]) for row in rs))

    def mean(rs: List[Dict[str, Any]], key: str) -> float:
        return total(rs, key) / len(rs) if rs else 0.0

    def std(rs: List[Dict[str, Any]], key: str) -> float:
        if len(rs) <= 1:
            return 0.0
        m = mean(rs, key)
        return math.sqrt(sum((float(row[key]) - m) ** 2 for row in rs) / (len(rs) - 1))

    for ph in timeline:
        rs = [row for row in rows if row["phase"] == ph.name]
        source_cv = std(rs, "source_A") / (mean(rs, "source_A") + 1e-9)
        release_cv = std(rs, "release") / (mean(rs, "release") + 1e-9)
        P_generated = total(rs, "P_generated")
        P_release = total(rs, "release")
        overflow = total(rs, "overflow")
        summaries.append(
            {
                "phase": ph.name,
                "t_start": ph.start,
                "t_end": ph.end,
                "note": ph.note,
                "source_A_total": total(rs, "source_A"),
                "A_in_total": total(rs, "A_in"),
                "B_in_total": total(rs, "B_in"),
                "P_generated": P_generated,
                "P_release": P_release,
                "quality_weighted_release": total(rs, "quality_weighted_release"),
                "P_overflow": overflow,
                "release_fraction": P_release / (P_generated + 1e-9) if P_generated > 1e-9 else 0.0,
                "overflow_fraction": overflow / (P_generated + 1e-9) if P_generated > 1e-9 else 0.0,
                "mean_reservoir": mean(rs, "reservoir"),
                "max_reservoir": max(float(row["reservoir"]) for row in rs),
                "mean_fill_fraction": mean(rs, "fill_frac"),
                "max_fill_fraction": max(float(row["fill_frac"]) for row in rs),
                "mean_backpressure": mean(rs, "backpressure"),
                "min_backpressure": min(float(row["backpressure"]) for row in rs),
                "mean_integrity": mean(rs, "integrity"),
                "final_integrity": float(rs[-1]["integrity"]),
                "mean_quality": mean(rs, "quality"),
                "min_quality": min(float(row["quality"]) for row in rs),
                "final_terrain": float(rs[-1]["terrain"]),
                "mean_road_boost": mean(rs, "road_boost"),
                "source_cv": source_cv,
                "release_cv": release_cv,
                "smoothing_ratio": release_cv / (source_cv + 1e-9),
                "quality_damage_index": 1.0 - mean(rs, "quality"),
                "stability_window": mean(rs, "integrity") * (1.0 - (overflow / (P_generated + 1e-9) if P_generated > 1e-9 else 0.0)) * mean(rs, "quality"),
            }
        )

    return summaries


def event_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    checks = [
        ("quality_lt_0_7", lambda r: float(r["quality"]) < 0.7, "Product quality first drops below 0.7."),
        ("quality_lt_0_5", lambda r: float(r["quality"]) < 0.5, "Product quality first drops below 0.5."),
        ("quality_lt_0_3", lambda r: float(r["quality"]) < 0.3, "Product quality first drops below 0.3."),
        ("fill_gt_0_5", lambda r: float(r["fill_frac"]) > 0.5, "Reservoir fill fraction first exceeds 0.5."),
        ("fill_gt_0_75", lambda r: float(r["fill_frac"]) > 0.75, "Reservoir fill fraction first exceeds 0.75."),
        ("backpressure_lt_0_5", lambda r: float(r["backpressure"]) < 0.5, "Backpressure first drops below 0.5."),
        ("backpressure_lt_0_2", lambda r: float(r["backpressure"]) < 0.2, "Backpressure first drops below 0.2."),
        ("integrity_lt_0_5", lambda r: float(r["integrity"]) < 0.5, "Membrane integrity first drops below 0.5."),
        ("integrity_lt_0_1", lambda r: float(r["integrity"]) < 0.1, "Membrane integrity first drops below 0.1."),
        (
            "rescue_integrity_gt_0_5_after_800",
            lambda r: int(r["t"]) >= 800 and float(r["integrity"]) > 0.5,
            "During stabilizer phase, membrane integrity first returns above 0.5.",
        ),
    ]

    out: List[Dict[str, Any]] = []
    for event, pred, description in checks:
        hit = next((row for row in rows if pred(row)), None)
        if hit is None:
            out.append(
                {
                    "event": event,
                    "t": "",
                    "phase": "",
                    "description": description,
                    "quality": "",
                    "fill_frac": "",
                    "backpressure": "",
                    "integrity": "",
                    "release": "",
                    "terrain": "",
                }
            )
        else:
            out.append(
                {
                    "event": event,
                    "t": hit["t"],
                    "phase": hit["phase"],
                    "description": description,
                    "quality": hit["quality"],
                    "fill_frac": hit["fill_frac"],
                    "backpressure": hit["backpressure"],
                    "integrity": hit["integrity"],
                    "release": hit["release"],
                    "terrain": hit["terrain"],
                }
            )
    return out


def rounded_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for row in rows:
        out.append({k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()})
    return out


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(seed: int = 20260707) -> Dict[str, Any]:
    cfg = Config(seed=seed)
    rows, timeline = simulate(cfg)
    summary = rounded_rows(summarize(rows, timeline))
    events = rounded_rows(event_rows(rows))
    timeseries = rounded_rows(rows)

    return {
        "experiment": "information_microreactor_backpressure_contamination",
        "date": "2026-07-08",
        "layer": "classical-effective phenomenology",
        "model": "time-resolved source-road-membrane-converter-reservoir-sink terrain sandbox",
        "seed": seed,
        "config": asdict(cfg),
        "phases": [
            {
                "name": ph.name,
                "start": ph.start,
                "end": ph.end,
                "note": ph.note,
                "params": asdict(ph.params),
            }
            for ph in timeline
        ],
        "summary": summary,
        "events": events,
        "limitations": [
            "Classical-effective deterministic observation sandbox, not a quantum-witness experiment.",
            "No quantum advantage or quantum-specific claim.",
            "Not biological metabolism, autonomous self-repair, self-regulation, or life-like behavior.",
            "Stabilizer rescue is external stabilizer-assisted recovery, not autonomous repair.",
            "Contamination is represented by scalar quality/poison variables and should not be overinterpreted.",
        ],
        "safe_claim": (
            "A time-resolved classical-effective sandbox shows ordered failure and recovery modes: "
            "contamination can degrade product quality before flow stops, reservoir saturation can "
            "produce upstream backpressure, stress can collapse membrane integrity, and external "
            "stabilizer input can partially restore membrane integrity."
        ),
        "timeseries": timeseries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--out", type=Path, default=Path("data/microreactor/information_microreactor_backpressure_contamination_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv"))
    parser.add_argument("--events-csv", type=Path, default=Path("data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv"))
    parser.add_argument("--timeseries-csv", type=Path, default=Path("data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    result_for_json = {k: v for k, v in result.items() if k != "timeseries"}
    result_for_json["timeseries_rows"] = len(result["timeseries"])
    args.out.write_text(json.dumps(result_for_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write_csv(result["summary"], args.summary_csv)
    write_csv(result["events"], args.events_csv)
    write_csv(result["timeseries"], args.timeseries_csv)

    print(json.dumps(result_for_json, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
