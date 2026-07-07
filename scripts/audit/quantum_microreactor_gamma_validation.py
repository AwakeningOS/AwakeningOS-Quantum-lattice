#!/usr/bin/env python3
"""
Gamma=max validation gate for a future quantum-coupled microreactor.

Layer: quantum-audit validation gate

Purpose:
    Validate that a fully dephased diagonal/population embedding reproduces the
    existing classical-effective information_microreactor_sandbox summaries.

This is not a quantum-specific positive result. It only checks the classical
limit required before any gamma sweep, Arm2 classical complex-wave control, or
Arm3 density-matrix quantum model can be interpreted.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.phenomenology import information_microreactor_sandbox as base  # noqa: E402

ABS_TOL = 1e-9
REL_TOL = 1e-9


def rf(x: float) -> float:
    y = round(float(x), 12)
    return 0.0 if abs(y) < 5e-13 else y


def summarize_from_rows(name: str, p: base.Params, cfg: base.Config, rows: List[Dict[str, float]]) -> Dict[str, Any]:
    post = rows[cfg.burn :]

    def total(key: str) -> float:
        return sum(row[key] for row in post)

    def mean(key: str) -> float:
        return total(key) / len(post)

    def std(key: str) -> float:
        m = mean(key)
        return math.sqrt(sum((row[key] - m) ** 2 for row in post) / max(1, len(post) - 1))

    source_A_total = total("source_A")
    source_B_total = total("source_B")
    A_in_total = total("A_in")
    B_in_total = total("B_in")
    P_generated_total = total("P_generated")
    P_release_total = total("release")
    P_overflow_total = total("overflow")

    permeability_A = A_in_total / source_A_total if source_A_total > 0 else 0.0
    permeability_B = B_in_total / source_B_total if source_B_total > 0 else 0.0
    selectivity = permeability_A / (permeability_B + 1e-12)
    release_fraction = P_release_total / (P_generated_total + 1e-9) if P_generated_total > 1e-9 else 0.0
    overflow_fraction = P_overflow_total / (P_generated_total + 1e-9) if P_generated_total > 1e-9 else 0.0
    source_cv = std("source_A") / (mean("source_A") + 1e-9)
    release_cv = std("release") / (mean("release") + 1e-9)

    summary = {
        "scenario": name,
        "source_A_total": source_A_total,
        "A_in_total": A_in_total,
        "B_in_total": B_in_total,
        "permeability_A": permeability_A,
        "permeability_B": permeability_B,
        "selectivity": selectivity,
        "P_generated": P_generated_total,
        "P_release": P_release_total,
        "P_overflow": P_overflow_total,
        "release_fraction": release_fraction,
        "overflow_fraction": overflow_fraction,
        "mean_reservoir": mean("reservoir"),
        "final_reservoir": rows[-1]["reservoir"],
        "mean_fill_fraction": mean("reservoir") / p.capacity,
        "mean_backpressure": mean("backpressure"),
        "final_integrity": rows[-1]["integrity"],
        "mean_integrity": mean("integrity"),
        "mean_quality": mean("quality"),
        "terrain_written": rows[-1]["terrain"],
        "efficiency_release_per_A": P_release_total / (source_A_total + 1e-9),
        "stability_window": mean("integrity") * (1.0 - overflow_fraction) * mean("quality"),
        "release_cv": release_cv,
        "source_cv": source_cv,
        "smoothing_ratio": release_cv / (source_cv + 1e-9),
    }
    return {k: (rf(v) if isinstance(v, float) else v) for k, v in summary.items()}


def simulate_gamma_max_diagonal(name: str, p: base.Params, cfg: base.Config) -> Dict[str, Any]:
    """Run the fully dephased diagonal/population embedding.

    This function intentionally has no active off-diagonal channel. Its job is
    to represent the gamma=max limit and test whether the classical scalar
    sandbox can be embedded without changing its observable summaries.
    """
    diag = {
        "inside_A": 0.0,
        "inside_B": 0.0,
        "reservoir": 0.0,
        "integrity": 1.0,
        "terrain": 0.0,
    }
    rows: List[Dict[str, float]] = []

    for t in range(cfg.steps):
        pulse = 1.0 + p.pulse_amp * math.sin(2.0 * math.pi * t / 64.0)
        road_boost = 1.0 + p.road_source_gain * (diag["terrain"] / (1.0 + diag["terrain"]))
        source_A = p.A_rate * pulse * road_boost
        source_B = p.B_rate
        D = p.D_rate
        C = p.C_rate

        protect = p.stabilizer_protect * (C / (1.0 + C))
        damage = p.damage_coeff * D * (1.0 - protect)
        repair = p.repair_coeff * C * (1.0 - diag["integrity"])
        diag["integrity"] = min(1.0, max(0.0, diag["integrity"] - damage + repair))

        fill_frac_pre = diag["reservoir"] / max(p.capacity, 1e-9)
        backpressure = max(0.02, 1.0 - p.backpressure_strength * fill_frac_pre)

        perm_A = p.pore_A * diag["integrity"] * backpressure
        perm_B = p.pore_B * diag["integrity"] * (1.0 + 0.5 * (1.0 - diag["integrity"]))
        A_in = source_A * perm_A
        B_in = source_B * perm_B

        diag["inside_A"] += A_in
        diag["inside_B"] += B_in

        poison = 1.0 / (1.0 + p.poison_coeff * diag["inside_B"])
        conv_rate = p.k_conv * poison * backpressure
        P_generated = min(diag["inside_A"], conv_rate * diag["inside_A"])
        diag["inside_A"] -= P_generated

        quality = 1.0 / (1.0 + p.quality_coeff * diag["inside_B"])
        diag["inside_B"] *= 0.985

        available = max(0.0, p.capacity - diag["reservoir"])
        P_accept = min(P_generated, available)
        overflow = max(0.0, P_generated - available)
        diag["reservoir"] += P_accept

        release = min(diag["reservoir"], diag["reservoir"] * p.release_rate, p.sink_cap)
        diag["reservoir"] -= release

        diag["terrain"] = diag["terrain"] * p.terrain_decay + release * p.terrain_write * quality

        rows.append(
            {
                "t": float(t),
                "source_A": source_A,
                "source_B": source_B,
                "A_in": A_in,
                "B_in": B_in,
                "P_generated": P_generated,
                "P_accept": P_accept,
                "release": release,
                "overflow": overflow,
                "reservoir": diag["reservoir"],
                "fill_frac": fill_frac_pre,
                "integrity": diag["integrity"],
                "terrain": diag["terrain"],
                "quality": quality,
                "poison": poison,
                "backpressure": backpressure,
                "damage": damage,
                "repair": repair,
            }
        )

    return summarize_from_rows(name, p, cfg, rows)


def compare_summaries(scalar: Dict[str, Any], gamma_max: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    scenario = str(scalar["scenario"])
    for metric, scalar_value in scalar.items():
        if metric == "scenario":
            continue
        s = float(scalar_value)
        g = float(gamma_max[metric])
        abs_error = abs(s - g)
        rel_error = abs_error / (abs(s) + 1e-12)
        passed = abs_error <= ABS_TOL
        rows.append(
            {
                "scenario": scenario,
                "metric": metric,
                "scalar_value": rf(s),
                "gamma_max_value": rf(g),
                "abs_error": rf(abs_error),
                "rel_error": rf(rel_error),
                "pass": str(passed).upper(),
            }
        )
    return rows


def run(seed: int = 20260707) -> Dict[str, Any]:
    # Seed retained for interface consistency. The current models are deterministic.
    _ = np.random.default_rng(seed)
    cfg = base.Config(seed=seed)
    scalar_result = base.run(seed=seed)
    scalar_by_scenario = {row["scenario"]: row for row in scalar_result["summaries"]}

    comparison_rows: List[Dict[str, Any]] = []
    summary_rows: List[Dict[str, Any]] = []

    for name, p in base.scenarios().items():
        scalar = scalar_by_scenario[name]
        gamma_max = simulate_gamma_max_diagonal(name, p, cfg)
        scenario_comparison = compare_summaries(scalar, gamma_max)
        comparison_rows.extend(scenario_comparison)
        failed = [row for row in scenario_comparison if row["pass"] != "TRUE"]
        max_row = max(scenario_comparison, key=lambda row: float(row["abs_error"]))
        summary_rows.append(
            {
                "scenario": name,
                "num_metrics": len(scenario_comparison),
                "max_abs_error": max_row["abs_error"],
                "max_error_metric": "" if float(max_row["abs_error"]) == 0.0 else max_row["metric"],
                "failed_metrics": len(failed),
                "pass": str(len(failed) == 0).upper(),
            }
        )

    failed_scenarios = [row["scenario"] for row in summary_rows if row["pass"] != "TRUE"]
    verdict = "PASS" if not failed_scenarios else "FAIL"
    max_abs_error_overall = max(float(row["max_abs_error"]) for row in summary_rows)

    return {
        "experiment": "quantum_microreactor_gamma_validation",
        "date": "2026-07-08",
        "layer": "quantum-audit validation gate",
        "seed": seed,
        "question": "Does the gamma=max fully-dephased diagonal embedding reproduce the existing classical-effective information_microreactor_sandbox summary?",
        "validation_target": "data/microreactor/information_microreactor_sandbox_seed20260707_summary.csv",
        "generator_script": "scripts/audit/quantum_microreactor_gamma_validation.py",
        "tolerance": {"abs": ABS_TOL, "rel": REL_TOL},
        "summary": summary_rows,
        "comparison_rows": comparison_rows,
        "verdict": verdict,
        "max_abs_error_overall": rf(max_abs_error_overall),
        "failed_scenarios": failed_scenarios,
        "safe_interpretation": "The gamma=max diagonal/population limit reproduces the existing scalar sandbox exactly within tolerance. This validates only the classical-limit embedding and does not establish quantum-specific behavior.",
        "limitations": [
            "This is a validation gate, not a quantum-specific positive result.",
            "The diagonal model intentionally has no active off-diagonal coherence.",
            "A later gamma sweep and Arm2 classical complex-wave control are required before any quantum-specific claim.",
            "Negativity, purity, or basis dependence must be tied to measured observables before promotion.",
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
    parser.add_argument("--out", type=Path, default=Path("data/quantum_microreactor/gamma_validation_seed20260707.json"))
    parser.add_argument("--summary-csv", type=Path, default=Path("data/quantum_microreactor/gamma_validation_seed20260707_summary.csv"))
    parser.add_argument("--comparison-csv", type=Path, default=Path("data/quantum_microreactor/gamma_validation_seed20260707_comparison.csv"))
    args = parser.parse_args()

    result = run(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    json_result = {k: v for k, v in result.items() if k != "comparison_rows"}
    json_result["comparison_rows"] = len(result["comparison_rows"])
    args.out.write_text(json.dumps(json_result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(result["summary"], args.summary_csv)
    write_csv(result["comparison_rows"], args.comparison_csv)
    print(json.dumps(json_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
