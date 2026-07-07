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
        run([sys.executable, "scripts/phenomenology/converter_core.py", "--seed", "8128", "--out", str(conv_tmp_json), "--csv", str(conv_tmp_csv)])
        compare_csv(ROOT / "data/converter/converter_core_seed8128_summary.csv", conv_tmp_csv, rtol=args.rtol, atol=args.atol)

        sandbox_tmp_json = tmp / "information_microreactor_sandbox_seed20260707.json"
        sandbox_tmp_csv = tmp / "information_microreactor_sandbox_seed20260707_summary.csv"
        run([sys.executable, "scripts/phenomenology/information_microreactor_sandbox.py", "--seed", "20260707", "--out", str(sandbox_tmp_json), "--csv", str(sandbox_tmp_csv)])
        compare_csv(ROOT / "data/microreactor/information_microreactor_sandbox_seed20260707_summary.csv", sandbox_tmp_csv, rtol=args.rtol, atol=args.atol)

        quantumized_tmp_json = tmp / "information_microreactor_quantumized_comparison_seed20260707.json"
        quantumized_tmp_csv = tmp / "information_microreactor_quantumized_comparison_seed20260707_summary.csv"
        run([sys.executable, "scripts/phenomenology/information_microreactor_quantumized_comparison.py", "--seed", "20260707", "--out", str(quantumized_tmp_json), "--csv", str(quantumized_tmp_csv)])
        compare_csv(ROOT / "data/microreactor/information_microreactor_quantumized_comparison_seed20260707_summary.csv", quantumized_tmp_csv, rtol=args.rtol, atol=args.atol)

        obs_tmp_json = tmp / "information_microreactor_backpressure_contamination_seed20260707.json"
        obs_tmp_summary = tmp / "information_microreactor_backpressure_contamination_seed20260707_summary.csv"
        obs_tmp_events = tmp / "information_microreactor_backpressure_contamination_seed20260707_events.csv"
        obs_tmp_timeseries = tmp / "information_microreactor_backpressure_contamination_seed20260707_timeseries.csv"
        run([sys.executable, "scripts/phenomenology/information_microreactor_backpressure_contamination.py", "--seed", "20260707", "--out", str(obs_tmp_json), "--summary-csv", str(obs_tmp_summary), "--events-csv", str(obs_tmp_events), "--timeseries-csv", str(obs_tmp_timeseries), "--timeseries-stride", "50"])
        compare_csv(ROOT / "data/microreactor/information_microreactor_backpressure_contamination_seed20260707_summary.csv", obs_tmp_summary, rtol=args.rtol, atol=args.atol)
        compare_csv(ROOT / "data/microreactor/information_microreactor_backpressure_contamination_seed20260707_events.csv", obs_tmp_events, rtol=args.rtol, atol=args.atol)
        compare_csv(ROOT / "data/microreactor/information_microreactor_backpressure_contamination_seed20260707_timeseries.csv", obs_tmp_timeseries, rtol=args.rtol, atol=args.atol)

        gamma_tmp_json = tmp / "gamma_validation_seed20260707.json"
        gamma_tmp_summary = tmp / "gamma_validation_seed20260707_summary.csv"
        gamma_tmp_comparison = tmp / "gamma_validation_seed20260707_comparison.csv"
        run([sys.executable, "scripts/audit/quantum_microreactor_gamma_validation.py", "--seed", "20260707", "--out", str(gamma_tmp_json), "--summary-csv", str(gamma_tmp_summary), "--comparison-csv", str(gamma_tmp_comparison)])
        compare_csv(ROOT / "data/quantum_microreactor/gamma_validation_seed20260707_summary.csv", gamma_tmp_summary, rtol=args.rtol, atol=args.atol)
        compare_csv(ROOT / "data/quantum_microreactor/gamma_validation_seed20260707_comparison.csv", gamma_tmp_comparison, rtol=args.rtol, atol=args.atol)

        gamma_sweep_tmp_json = tmp / "gamma_sweep_quality_probe_seed20260707.json"
        gamma_sweep_tmp_summary = tmp / "gamma_sweep_quality_probe_seed20260707_summary.csv"
        gamma_sweep_tmp_detail = tmp / "gamma_sweep_quality_probe_seed20260707_detail.csv"
        run([sys.executable, "scripts/audit/quantum_microreactor_gamma_sweep_quality_probe.py", "--seed", "20260707", "--out", str(gamma_sweep_tmp_json), "--summary-csv", str(gamma_sweep_tmp_summary), "--detail-csv", str(gamma_sweep_tmp_detail)])
        compare_csv(ROOT / "data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv", gamma_sweep_tmp_summary, rtol=args.rtol, atol=args.atol)
        compare_csv(ROOT / "data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv", gamma_sweep_tmp_detail, rtol=args.rtol, atol=args.atol)

        branch_tmp_json = tmp / "branching_converter_probe_seed20260707.json"
        branch_tmp_summary = tmp / "branching_converter_probe_seed20260707_summary.csv"
        run([sys.executable, "scripts/audit/quantum_microreactor_branching_converter_probe.py", "--seed", "20260707", "--out", str(branch_tmp_json), "--summary-csv", str(branch_tmp_summary)])
        compare_csv(ROOT / "data/quantum_microreactor/branching_converter_probe_seed20260707_summary.csv", branch_tmp_summary, rtol=args.rtol, atol=args.atol)

        transport_tmp_json = tmp / "transported_branching_arm2_kill_seed20260707.json"
        transport_tmp_summary = tmp / "transported_branching_arm2_kill_seed20260707_summary.csv"
        run([sys.executable, "scripts/audit/quantum_microreactor_transported_branching_arm2_kill.py", "--seed", "20260707", "--out", str(transport_tmp_json), "--summary-csv", str(transport_tmp_summary)])
        compare_csv(ROOT / "data/quantum_microreactor/transported_branching_arm2_kill_seed20260707_summary.csv", transport_tmp_summary, rtol=args.rtol, atol=args.atol)

        chsh_tmp_json = tmp / "chsh_readout_transport_probe_seed20260707.json"
        chsh_tmp_summary = tmp / "chsh_readout_transport_probe_seed20260707_summary.csv"
        run([sys.executable, "scripts/audit/quantum_microreactor_chsh_readout_transport_probe.py", "--seed", "20260707", "--out", str(chsh_tmp_json), "--summary-csv", str(chsh_tmp_summary)])
        compare_csv(ROOT / "data/quantum_microreactor/chsh_readout_transport_probe_seed20260707_summary.csv", chsh_tmp_summary, rtol=args.rtol, atol=args.atol)

        terrain_tmp_json = tmp / "measurement_terrain_feedback_probe_seed20260707.json"
        terrain_tmp_summary = tmp / "measurement_terrain_feedback_probe_seed20260707_summary.csv"
        run([sys.executable, "scripts/audit/quantum_measurement_terrain_feedback_probe.py", "--seed", "20260707", "--out", str(terrain_tmp_json), "--summary-csv", str(terrain_tmp_summary)])
        compare_csv(ROOT / "data/quantum_microreactor/measurement_terrain_feedback_probe_seed20260707_summary.csv", terrain_tmp_summary, rtol=args.rtol, atol=args.atol)

        audit_specs = [
            ("scripts/audit/quantum_coupled_microreactor_step1.py", "step1_cr_coupling_seed0", "data/quantum_microreactor/step1_cr_coupling_seed0_summary.csv"),
            ("scripts/audit/quantum_coupled_microreactor_step2_backpressure.py", "step2_backpressure_seed0", "data/quantum_microreactor/step2_backpressure_seed0_summary.csv"),
            ("scripts/audit/quantum_coupled_microreactor_step2_v2_unitary_population.py", "step2_v2_unitary_population_seed0", "data/quantum_microreactor/step2_v2_unitary_population_seed0_summary.csv"),
            ("scripts/audit/quantum_coupled_microreactor_step3_svetlichny.py", "step3_svetlichny_seed0", "data/quantum_microreactor/step3_svetlichny_seed0_summary.csv"),
            ("scripts/audit/quantum_coupled_microreactor_step4_population_synergy.py", "step4_population_synergy_seed0", "data/quantum_microreactor/step4_population_synergy_seed0_summary.csv"),
            ("scripts/audit/quantum_coupled_microreactor_step5_reactor_like_population_synergy.py", "step5_reactor_like_population_synergy_seed0", "data/quantum_microreactor/step5_reactor_like_population_synergy_seed0_summary.csv"),
            ("scripts/audit/quantum_coupled_microreactor_step6_explicit_component_chain.py", "step6_explicit_component_chain_seed0", "data/quantum_microreactor/step6_explicit_component_chain_seed0_summary.csv"),
        ]

        for script, stem, expected_csv in audit_specs:
            tmp_json = tmp / f"{stem}.json"
            tmp_csv = tmp / f"{stem}_summary.csv"
            run([sys.executable, script, "--seed", "0", "--out", str(tmp_json), "--csv", str(tmp_csv)])
            compare_csv(ROOT / expected_csv, tmp_csv, rtol=args.rtol, atol=args.atol)

        print("RAW_LOG check PASS")
        return 0
    finally:
        if args.keep_tmp:
            print(f"kept temp dir: {tmp}")
        else:
            tmp_obj.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
