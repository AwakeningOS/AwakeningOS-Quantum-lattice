#!/usr/bin/env python3
"""Check RAW_LOG_BACKED files against their generator scripts.

This script turns RAW_LOG_BACKED from a manual label into an executable
invariant. It regenerates known raw logs into a temporary directory and
byte-compares them against the committed canonical raw logs.

Current canonical logs:
  - data/negativity_causality/negativity_causality_test_seed0.json
  - data/converter/converter_core_seed8128_summary.csv

The converter canonical raw log is the CSV summary. The generator can also
write JSON, but the committed RAW_LOG_BACKED report currently points to the
CSV summary as the auditable raw artifact.
"""
from __future__ import annotations

import argparse
import filecmp
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def require_equal(expected: Path, actual: Path) -> None:
    if not expected.exists():
        raise FileNotFoundError(f"missing committed raw log: {expected}")
    if not actual.exists():
        raise FileNotFoundError(f"generator did not produce: {actual}")
    if not filecmp.cmp(expected, actual, shallow=False):
        raise AssertionError(f"RAW_LOG stale: {expected} != regenerated {actual}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-tmp", action="store_true", help="Keep temporary regenerated files for debugging")
    args = parser.parse_args()

    tmp_obj = tempfile.TemporaryDirectory(prefix="raw-log-check-")
    tmp = Path(tmp_obj.name)

    try:
        neg_tmp = tmp / "negativity_causality_test_seed0.json"
        run([
            sys.executable,
            "scripts/negativity_causality_test.py",
            "--out",
            str(neg_tmp),
        ])
        require_equal(
            ROOT / "data/negativity_causality/negativity_causality_test_seed0.json",
            neg_tmp,
        )

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
        require_equal(
            ROOT / "data/converter/converter_core_seed8128_summary.csv",
            conv_tmp_csv,
        )

        print("RAW_LOG check PASS")
        return 0
    finally:
        if args.keep_tmp:
            print(f"kept temp dir: {tmp}")
        else:
            tmp_obj.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
