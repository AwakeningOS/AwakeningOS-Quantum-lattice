#!/usr/bin/env python3
"""
Gamma sweep quality/coherence probe for the information microreactor line.

Layer: quantum-audit probe

Purpose:
    After the gamma=max validation gate passes, test whether a first gamma sweep
    shows any quantum-specific usefulness in a quality-as-coherence auxiliary
    probe.

This script deliberately includes Arm2 classical complex-wave control. If Arm2
reproduces the same gamma-sensitive coherence proxy, the effect is not classified
as quantum-specific even if Arm3 has a negativity proxy.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phenomenology import information_microreactor_sandbox as base  # noqa: E402


GAMMAS = [1.0, 0.75, 0.5, 0.25, 0.0]
ARMS = ["arm1_scalar", "arm2_complex_wave", "arm3_quantum_dm"]


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def purity_proxy(q: float, coherence: float) -> float:
    return q * q + (1.0 - q) * (1.0 - q) + 2.0 * coherence * coherence


def arm_metrics(scenario: str, gamma: float, arm: str, scalar_summary: Dict[str, Any]) -> Dict[str, Any]:
    q = float(scalar_summary["mean_quality"])
    p_release = float(scalar_summary["P_release"])
    coherence_seed = math.sqrt(max(0.0, q * (1.0 - q)))

    if arm == "arm1_scalar":
        coherence = 0.0
        negativity = 0.0
    elif arm == "arm2_complex_wave":
        coherence = (1.0 - gamma) * coherence_seed
        negativity = 0.0
    elif arm == "arm3_quantum_dm":
        coherence = (1.0 - gamma) * coherence_seed
        negativity = coherence
    else:
        raise ValueError(f"unknown arm: {arm}")

    return {
        "scenario": scenario,
        "gamma": gamma,
        "arm": arm,
        "P_release": p_release,
        "mean_quality_z": q,
        "coherence_quality_proxy": coherence,
        "purity_proxy": purity_proxy(q, coherence),
        "negativity": negativity,
        "diff_P_release_vs_gamma_max": 0.0,
        "diff_quality_z_vs_gamma_max": 0.0,
        "quantum_specific_observable_effect": "FALSE",
    }


def run(seed: int = 20260707) -> Dict[str, Any]:
    # Seed retained for interface consistency. The current probe is deterministic.
    _ = np.random.default_rng(seed)
    scalar_result = base.run(seed=seed)
    scalar_by_scenario = {row["scenario"]: row for row in scalar_result["summaries"]}

    detail_rows: List[Dict[str, Any]] = []
    summary_rows: List[Dict[str, Any]] = []

    for scenario, scalar in scalar_by_scenario.items():
        scenario_rows: List[Dict[str, Any]] = []
        for gamma in GAMMAS:
            for arm in ARMS:
                row = arm_metrics(scenario, gamma, arm, scalar)
                row = {k: (rf(v) if isinstance(v, float) else v) for k, v in row.items()}
                scenario_rows.append(row)
                detail_rows.append(row)

        arm2_coherence = [float(row["coherence_quality_proxy"]) for row in scenario_rows if row["arm"] == "arm2_complex_wave"]
        arm3_coherence = [float(row["coherence_quality_proxy"]) for row in scenario_rows if row["arm"] == "arm3_quantum_dm"]
        arm3_negativity = [float(row["negativity"]) for row in scenario_rows if row["arm"] == "arm3_quantum_dm"]
        max_arm2_arm3_diff = max(abs(a - b) for a, b in zip(arm2_coherence, arm3_coherence))

        summary_rows.append(
            {
                "scenario": scenario,
                "gamma_values": ";".join(str(g) for g in GAMMAS),
                "max_abs_diff_P_release_vs_gamma_max": 0.0,
                "max_abs_diff_quality_z_vs_gamma_max": 0.0,
                "max_arm2_coherence_proxy": rf(max(arm2_coherence)),
                "max_arm3_coherence_proxy": rf(max(arm3_coherence)),
                "max_arm3_negativity": rf(max(arm3_negativity)),
                "arm2_matches_arm3_coherence": str(max_arm2_arm3_diff <= 1e-12).upper(),
                "negativity_changes_observable": "FALSE",
                "quantum_specific_effect": "FALSE",
                "classification": "gamma-sensitive coherence proxy but no quantum-specific observable advantage",
            }
        )

    return {
        "experiment": "quantum_microreactor_gamma_sweep_quality_probe",
        "date": "2026-07-08",
        "layer": "quantum-audit probe",
        "seed": seed,
        "gamma_values": GAMMAS,
        "arms": ARMS,
        "validation_anchor": "gamma=1.0 preserves existing scalar P_release and mean_quality_z",
        "summary": summary_rows,
        "detail": detail_rows,
        "verdict": "NEGATIVE_FOR_QUANTUM_SPECIFIC_EFFECT",
        "safe_interpretation": (
            "The probe creates gamma-sensitive coherence and Arm3 negativity proxies, "
            "but all existing observable sandbox outputs remain unchanged and the coherence "
            "proxy is reproduced by Arm2 classical complex-wave control. Therefore this is "
            "not quantum-specific efficacy."
        ),
        "limitations": [
            "Quality is read as the original scalar Z/population observable to preserve gamma=max validation.",
            "The coherence_quality_proxy is an auxiliary probe, not a replacement for scalar quality.",
            "Arm3 negativity is not coupled back into release, backpressure, terrain, or conversion in this probe.",
            "Because Arm2 reproduces the same coherence proxy, the effect is classified as classical-wave reproducible.",
        ],
    }


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv"))
    parser.add_argument("--detail-csv", type=Path, default=Path("data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    json_result = {k: v for k, v in result.items() if k != "detail"}
    json_result["detail_rows"] = len(result["detail"])
    args.out.write_text(json.dumps(json_result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    write_csv(result["detail"], args.detail_csv)
    print(json.dumps(json_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
