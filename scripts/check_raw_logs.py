#!/usr/bin/env python3
"""Check RAW_LOG_BACKED files against their generator scripts.

This script turns RAW_LOG_BACKED from a manual label into an executable
invariant. It regenerates known raw logs into a temporary directory and
compares their normalized content against the committed canonical raw logs.

Why normalized comparison instead of byte comparison:
    Byte comparison catches stale logs, but it also false-alarms on harmless
    JSON formatting, CSV float spelling, newline, or environment-level float
    representation differences. The goal is to catch scientific/content skew,
    not formatting skew.

Current canonical logs:
  - data/negativity_causality/negativity_causality_test_seed0.json
  - data/converter/converter_core_seed8128_summary.csv
  - data/quantum_microreactor/step1_cr_coupling_seed0_summary.csv
  - data/quantum_microreactor/step2_backpressure_seed0_summary.csv
  - data/quantum_microreactor/step2_v2_unitary_population_seed0_summary.csv
"""
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
            missing = set(expected.keys()) - set(actual.keys())
            extra = set(actual.keys()) - set(expected.keys())
            raise AssertionError(f"dict key mismatch at {path}: missing={missing}, extra={extra}")
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
    if not expected.exists():
        raise FileNotFoundError(f"missing committed raw log: {expected}")
    if not actual.exists():
        raise FileNotFoundError(f"generator did not produce: {actual}")
    with expected.open("r", encoding="utf-8") as f:
        expected_obj = json.load(f)
    with actual.open("r", encoding="utf-8") as f:
        actual_obj = json.load(f)
    compare_values(expected_obj, actual_obj, str(expected), rtol=rtol, atol=atol)


def compare_csv(expected: Path, actual: Path, *, rtol: float, atol: float) -> None:
    if not expected.exists():
        raise FileNotFoundError(f"missing committed raw log: {expected}")
    if not actual.exists():
        raise FileNotFoundError(f"generator did not produce: {actual}")

    with expected.open("r", encoding="utf-8", newline="") as f:
        expected_rows = list(csv.DictReader(f))
        expected_fields = expected_rows[0].keys() if expected_rows else []
    with actual.open("r", encoding="utf-8", newline="") as f:
        actual_rows = list(csv.DictReader(f))
        actual_fields = actual_rows[0].keys() if actual_rows else []

    if list(expected_fields) != list(actual_fields):
        raise AssertionError(f"CSV header mismatch for {expected}: {list(expected_fields)} != {list(actual_fields)}")
    if len(expected_rows) != len(actual_rows):
        raise AssertionError(f"CSV row count mismatch for {expected}: {len(expected_rows)} != {len(actual_rows)}")

    fields = list(expected_fields)
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
    parser.add_argument("--keep-tmp", action="store_true", help="Keep temporary regenerated files for debugging")
    parser.add_argument("--rtol", type=float, default=DEFAULT_RTOL)
    parser.add_argument("--atol", type=float, default=DEFAULT_ATOL)
    args = parser.parse_args()

    tmp_obj = tempfile.TemporaryDirectory(prefix="raw-log-check-")
    tmp = Path(tmp_obj.name)

    try:
        neg_tmp = tmp / "negativity_causality_test_seed0.json"
        run([sys.executable, "scripts/negativity_causality_test.py", "--out", str(neg_tmp)])
        compare_json(ROOT / "data/negativity_causality/negativity_causality_test_seed0.json", neg_tmp, rtol=args.rtol, atol=args.atol)

        conv_tmp_json = tmp / "converter_core_seed8128.json"
        conv_tmp_csv = tmp / "converter_core_seed8128_summary.csv"
        run([
            sys.executable,
            "scripts/phenomenology/converter_core.py",
            "--seed",
            "8128",
            "--out",
            str(conv_tmp_json),
            "--csv",
            str(conv_tmp_csv),
        ])
        compare_csv(ROOT / "data/converter/converter_core_seed8128_summary.csv", conv_tmp_csv, rtol=args.rtol, atol=args.atol)

        micro_tmp_json = tmp / "step1_cr_coupling_seed0.json"
        micro_tmp_csv = tmp / "step1_cr_coupling_seed0_summary.csv"
        run([
            sys.executable,
            "scripts/audit/quantum_coupled_microreactor_step1.py",
            "--seed",
            "0",
            "--out",
            str(micro_tmp_json),
            "--csv",
            str(micro_tmp_csv),
        ])
        compare_csv(ROOT / "data/quantum_microreactor/step1_cr_coupling_seed0_summary.csv", micro_tmp_csv, rtol=args.rtol, atol=args.atol)

        step2_tmp_json = tmp / "step2_backpressure_seed0.json"
        step2_tmp_csv = tmp / "step2_backpressure_seed0_summary.csv"
        run([
            sys.executable,
            "scripts/audit/quantum_coupled_microreactor_step2_backpressure.py",
            "--seed",
            "0",
            "--out",
            str(step2_tmp_json),
            "--csv",
            str(step2_tmp_csv),
        ])
        compare_csv(ROOT / "data/quantum_microreactor/step2_backpressure_seed0_summary.csv", step2_tmp_csv, rtol=args.rtol, atol=args.atol)

        step2_v2_tmp_json = tmp / "step2_v2_unitary_population_seed0.json"
        step2_v2_tmp_csv = tmp / "step2_v2_unitary_population_seed0_summary.csv"
        run([
            sys.executable,
            "scripts/audit/quantum_coupled_microreactor_step2_v2_unitary_population.py",
            "--seed",
            "0",
            "--out",
            str(step2_v2_tmp_json),
            "--csv",
            str(step2_v2_tmp_csv),
        ])
        compare_csv(ROOT / "data/quantum_microreactor/step2_v2_unitary_population_seed0_summary.csv", step2_v2_tmp_csv, rtol=args.rtol, atol=args.atol)

        print("RAW_LOG check PASS")
        return 0
    finally:
        if args.keep_tmp:
            print(f"kept temp dir: {tmp}")
        else:
            tmp_obj.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
