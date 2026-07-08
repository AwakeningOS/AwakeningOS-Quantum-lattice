#!/usr/bin/env python3
"""Check RAW_LOG_BACKED files against their generator scripts."""
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RTOL = 1e-9
DEFAULT_ATOL = 1e-9


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def is_number_string(x: str) -> bool:
    if x == "":
        return False
    try:
        float(x)
        return True
    except ValueError:
        return False


def compare_values(expected: Any, actual: Any, path: str, *, rtol: float, atol: float) -> None:
    if isinstance(expected, bool) or isinstance(actual, bool):
        if expected != actual:
            raise AssertionError(f"value mismatch at {path}: {expected!r} != {actual!r}")
        return
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        if not math.isclose(float(expected), float(actual), rel_tol=rtol, abs_tol=atol):
            raise AssertionError(f"numeric mismatch at {path}: {expected!r} != {actual!r}")
        return
    if isinstance(expected, dict) and isinstance(actual, dict):
        if set(expected.keys()) != set(actual.keys()):
            raise AssertionError(f"dict key mismatch at {path}: {set(expected.keys()) ^ set(actual.keys())}")
        for key in sorted(expected.keys()):
            compare_values(expected[key], actual[key], f"{path}.{key}", rtol=rtol, atol=atol)
        return
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            raise AssertionError(f"list length mismatch at {path}: {len(expected)} != {len(actual)}")
        for i, (e, a) in enumerate(zip(expected, actual)):
            compare_values(e, a, f"{path}[{i}]", rtol=rtol, atol=atol)
        return
    if expected != actual:
        raise AssertionError(f"value mismatch at {path}: {expected!r} != {actual!r}")


def compare_json(expected: Path, actual: Path, *, rtol: float, atol: float) -> None:
    with expected.open("r", encoding="utf-8") as f:
        expected_obj = json.load(f)
    with actual.open("r", encoding="utf-8") as f:
        actual_obj = json.load(f)
    compare_values(expected_obj, actual_obj, str(expected), rtol=rtol, atol=atol)


def compare_csv(expected: Path, actual: Path, *, rtol: float, atol: float) -> None:
    with expected.open("r", encoding="utf-8", newline="") as f:
        expected_rows = list(csv.DictReader(f))
    with actual.open("r", encoding="utf-8", newline="") as f:
        actual_rows = list(csv.DictReader(f))
    if not expected_rows and not actual_rows:
        return
    if list(expected_rows[0].keys()) != list(actual_rows[0].keys()):
        raise AssertionError(f"CSV header mismatch for {expected}")
    if len(expected_rows) != len(actual_rows):
        raise AssertionError(f"CSV row count mismatch for {expected}: {len(expected_rows)} != {len(actual_rows)}")
    fields = list(expected_rows[0].keys())
    for row_i, (e_row, a_row) in enumerate(zip(expected_rows, actual_rows)):
        for field in fields:
            e = e_row[field]
            a = a_row[field]
            loc = f"{expected}:row{row_i}:{field}"
            if is_number_string(e) and is_number_string(a):
                if not math.isclose(float(e), float(a), rel_tol=rtol, abs_tol=atol):
                    raise AssertionError(f"CSV numeric mismatch at {loc}: {e!r} != {a!r}")
            elif e != a:
                raise AssertionError(f"CSV value mismatch at {loc}: {e!r} != {a!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-tmp", action="store_true")
    parser.add_argument("--rtol", type=float, default=DEFAULT_RTOL)
    parser.add_argument("--atol", type=float, default=DEFAULT_ATOL)
    args = parser.parse_args()
    tmp_obj = tempfile.TemporaryDirectory(prefix="raw-log-check-")
    tmp = Path(tmp_obj.name)
    try:
        neg_tmp = tmp / "negativity_causality_test_seed0.json"
        run([sys.executable, "scripts/negativity_causality_test.py", "--out", str(neg_tmp)])
        compare_json(ROOT / "data/negativity_causality/negativity_causality_test_seed0.json", neg_tmp, rtol=args.rtol, atol=args.atol)
        csv_specs = [
            ("scripts/phenomenology/converter_core.py", ["--seed", "8128", "--out", str(tmp / "converter_core_seed8128.json"), "--csv", str(tmp / "converter_core_seed8128_summary.csv")], "data/converter/converter_core_seed8128_summary.csv", tmp / "converter_core_seed8128_summary.csv"),
            ("scripts/phenomenology/information_microreactor_sandbox.py", ["--seed", "20260707", "--out", str(tmp / "information_microreactor_sandbox_seed20260707.json"), "--csv", str(tmp / "information_microreactor_sandbox_seed20260707_summary.csv")], "data/microreactor/information_microreactor_sandbox_seed20260707_summary.csv", tmp / "information_microreactor_sandbox_seed20260707_summary.csv"),
            ("scripts/phenomenology/information_microreactor_quantumized_comparison.py", ["--seed", "20260707", "--out", str(tmp / "information_microreactor_quantumized_comparison_seed20260707.json"), "--csv", str(tmp / "information_microreactor_quantumized_comparison_seed20260707_summary.csv")], "data/microreactor/information_microreactor_quantumized_comparison_seed20260707_summary.csv", tmp / "information_microreactor_quantumized_comparison_seed20260707_summary.csv"),
        ]
        for script, extra_args, expected, actual in csv_specs:
            run([sys.executable, script, *extra_args])
            compare_csv(ROOT / expected, actual, rtol=args.rtol, atol=args.atol)

        whole_json = tmp / "information_microreactor_whole_state_quantum_sandbox_seed20260707.json"
        whole_summary = tmp / "information_microreactor_whole_state_quantum_sandbox_seed20260707_summary.csv"
        whole_events = tmp / "information_microreactor_whole_state_quantum_sandbox_seed20260707_events.csv"
        run([
            sys.executable,
            "scripts/phenomenology/information_microreactor_whole_state_quantum_sandbox.py",
            "--seed",
            "20260707",
            "--out",
            str(whole_json),
            "--summary-csv",
            str(whole_summary),
            "--events-csv",
            str(whole_events),
        ])
        compare_csv(ROOT / "data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_summary.csv", whole_summary, rtol=args.rtol, atol=args.atol)
        compare_csv(ROOT / "data/microreactor/information_microreactor_whole_state_quantum_sandbox_seed20260707_events.csv", whole_events, rtol=args.rtol, atol=args.atol)

        obs_json = tmp / "information_microreactor_backpressure_contamination_seed20260707.json"
        obs_summary = tmp / "information_microreactor_backpressure_contamination_seed20260707_summary.csv"
        obs_events = tmp / "information_microreactor_backpressure_contamination_seed20260707_events.csv"
        obs_timeseries = tmp / "information_microreactor_backpressure_contamination_seed20260707_timeseries.csv"
        run([sys.executable, "scripts/phenomenology/information_microreactor_backpressure_contamination.py", "--seed", "20260707", "--out", str(obs_json), "--summary-csv", str(obs_summary), "--events-csv", str(obs_events), "--timeseries-csv", str(obs_timeseries), "--timeseries-stride", "50"])
        compare_csv(ROOT / "data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv", obs_summary, rtol=args.rtol, atol=args.atol)
        compare_csv(ROOT / "data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv", obs_events, rtol=args.rtol, atol=args.atol)
        compare_csv(ROOT / "data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv", obs_timeseries, rtol=args.rtol, atol=args.atol)
        audit_specs = [
            ("quantum_microreactor_gamma_validation.py", "gamma_validation_seed20260707", ["--comparison-csv", str(tmp / "gamma_validation_seed20260707_comparison.csv")], ["data/quantum_microreactor/gamma_validation_seed20260707_summary.csv", "data/quantum_microreactor/gamma_validation_seed20260707_comparison.csv"]),
            ("quantum_microreactor_gamma_sweep_quality_probe.py", "gamma_sweep_quality_probe_seed20260707", ["--detail-csv", str(tmp / "gamma_sweep_quality_probe_seed20260707_detail.csv")], ["data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv", "data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv"]),
            ("quantum_microreactor_branching_converter_probe.py", "branching_converter_probe_seed20260707", [], ["data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv"]),
            ("quantum_microreactor_transported_branching_arm2_kill.py", "transported_branching_arm2_kill_seed20260707", [], ["data/quantum_microreactor/transported_branching_arm2_kill_seed20260707_summary.csv"]),
            ("quantum_microreactor_chsh_readout_transport_probe.py", "chsh_readout_transport_probe_seed20260707", [], ["data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv"]),
            ("quantum_measurement_terrain_feedback_probe.py", "measurement_terrain_feedback_probe_seed20260707", [], ["data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv"]),
            ("quantum_sampled_chsh_terrain_feedback_probe.py", "sampled_chsh_terrain_feedback_probe_seed20260707", [], ["data/quantum_microreactor/sampled_chsh_terrain_feedback_probe_seed20260707_summary.csv"]),
            ("quantum_measurement_terrain_memory_probe.py", "measurement_terrain_memory_probe_seed20260707", [], ["data/quantum_microreactor/measurement_terrain_memory_probe_seed20260707_summary.csv"]),
            ("quantum_adaptive_measurement_feedback_probe.py", "adaptive_measurement_feedback_probe_seed20260707", [], ["data/quantum_microreactor/adaptive_measurement_feedback_probe_seed20260707_summary.csv"]),
            ("quantum_fixed_basis_adaptive_feedback_probe.py", "fixed_basis_adaptive_feedback_probe_seed20260707", [], ["data/quantum_microreactor/fixed_basis_adaptive_feedback_probe_seed20260707_summary.csv"]),
        ]
        for script, stem, extra_args, expected_paths in audit_specs:
            out_json = tmp / f"{stem}.json"
            summary_csv = tmp / f"{stem}_summary.csv"
            run([sys.executable, f"scripts/audit/{script}", "--seed", "20260707", "--out", str(out_json), "--summary-csv", str(summary_csv), *extra_args])
            compare_csv(ROOT / expected_paths[0], summary_csv, rtol=args.rtol, atol=args.atol)
            for expected_path in expected_paths[1:]:
                compare_csv(ROOT / expected_path, tmp / Path(expected_path).name, rtol=args.rtol, atol=args.atol)
        print("RAW_LOG check PASS")
        return 0
    finally:
        if args.keep_tmp:
            print(f"kept temp dir: {tmp}")
        else:
            tmp_obj.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
