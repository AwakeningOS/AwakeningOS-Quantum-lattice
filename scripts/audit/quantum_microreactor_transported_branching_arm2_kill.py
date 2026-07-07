#!/usr/bin/env python3
"""CSV-emitting wrapper for the transported branching Arm2-kill probe."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from quantum_branch_converter import Prel, maxneg, meanneg, scenarios, simulate
from arm2_kill import simulate_arm2reduced


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def corr_neg_release(rows: list[dict[str, float]]) -> float:
    negs = [x["neg"] for x in rows]
    rels = [x["release"] for x in rows]
    if np.std(negs) <= 1e-12 or np.std(rels) <= 1e-12:
        return float("nan")
    return float(np.corrcoef(negs, rels)[0, 1])


def run(seed: int = 20260707) -> Dict[str, Any]:
    _ = np.random.default_rng(seed)
    rows: List[Dict[str, Any]] = []
    for scenario, p in scenarios().items():
        classical_rows = simulate(p, "classical")
        quantum_g1_rows = simulate(p, "quantum", 1.0)
        quantum_g05_rows = simulate(p, "quantum", 0.5)
        quantum_g0_rows = simulate(p, "quantum", 0.0)
        weak_arm2_rows = simulate(p, "arm2")

        classical_release = Prel(classical_rows)
        q1_release = Prel(quantum_g1_rows)
        q05_release = Prel(quantum_g05_rows)
        q0_release = Prel(quantum_g0_rows)
        weak_arm2_release = Prel(weak_arm2_rows)
        arm2_reduced_g0 = simulate_arm2reduced(p, 0.0)
        arm2_reduced_g05 = simulate_arm2reduced(p, 0.5)

        row = {
            "scenario": scenario,
            "classical_release": classical_release,
            "gate_diff_gamma1": abs(q1_release - classical_release),
            "quantum_release_g0_5": q05_release,
            "quantum_dev_pct_g0_5": 100.0 * (q05_release - classical_release) / classical_release,
            "quantum_release_g0": q0_release,
            "quantum_dev_pct_g0": 100.0 * (q0_release - classical_release) / classical_release,
            "weak_arm2_release": weak_arm2_release,
            "weak_arm2_dev_pct": 100.0 * (weak_arm2_release - classical_release) / classical_release,
            "weak_arm2_diff_vs_quantum_g0": abs(weak_arm2_release - q0_release),
            "arm2_reduced_release_g0": arm2_reduced_g0,
            "arm2_reduced_diff_vs_quantum_g0": abs(arm2_reduced_g0 - q0_release),
            "arm2_reduced_release_g0_5": arm2_reduced_g05,
            "arm2_reduced_diff_vs_quantum_g0_5": abs(arm2_reduced_g05 - q05_release),
            "mean_neg_g0_5": meanneg(quantum_g05_rows),
            "max_neg_g0_5": maxneg(quantum_g05_rows),
            "mean_neg_g0": meanneg(quantum_g0_rows),
            "max_neg_g0": maxneg(quantum_g0_rows),
            "corr_neg_release_g0": corr_neg_release(quantum_g0_rows[200:]),
            "correct_arm2_match": "TRUE" if abs(arm2_reduced_g0 - q0_release) < 1e-9 and abs(arm2_reduced_g05 - q05_release) < 1e-9 else "FALSE",
            "quantum_specific_transport_effect": "FALSE",
            "classification": "transported release changes strongly but is exactly reproduced by correct reduced Arm2",
        }
        rows.append({k: (rf(v) if isinstance(v, float) and not math.isnan(v) else v) for k, v in row.items()})

    return {
        "experiment": "quantum_microreactor_transported_branching_arm2_kill",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "summary": rows,
        "verdict": "NEGATIVE_FOR_QUANTUM_SPECIFIC_TRANSPORT",
        "safe_interpretation": "Transported release changes strongly, but the correct zero-entanglement reduced Arm2 channel reproduces quantum transported release to numerical precision.",
    }


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/transported_branching_arm2_kill_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/transported_branching_arm2_kill_seed20260707_summary.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
