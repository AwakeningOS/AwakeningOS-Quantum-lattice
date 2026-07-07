#!/usr/bin/env python3
"""
Converter core: code-backed phenomenological information-material component.

Purpose:
    Build the first non-plumbing information-material part:
    a converter that changes identity/meaning, not just location, quantity, or timing.

Component role:
    membrane     -> location/access
    source-sink  -> quantity
    reservoir    -> timing
    converter    -> identity/meaning

This is a classical stochastic phenomenology model, not a quantum witness.
It is intentionally code-backed with fixed seeds and raw JSON output.

Modes:
    linear_control:
        historyless baseline; conversion probability depends smoothly on A stock
        but has no threshold, hysteresis, or product feedback.

    threshold:
        conversion turns on sharply only above an A-stock threshold.

    bistable:
        internal mode switches high/low using hysteresis thresholds.
        This gives memory-dependent P/Q branch behavior.

    inhibition:
        end-product P inhibits further A->P conversion.

Sweeps:
    1. conversion-throughput
    2. fidelity-promiscuity
    3. gating/conditional response
    4. stability/poisoning
    5. bistable hysteresis loop
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Literal

import numpy as np

Mode = Literal["linear_control", "threshold", "bistable", "inhibition"]


@dataclass
class ConverterParams:
    mode: Mode = "linear_control"
    seed: int = 0
    steps: int = 900
    burn_in: int = 250

    # input / converter kinetics
    input_flux: float = 2.0
    base_convert_prob: float = 0.18
    km: float = 25.0
    threshold: float = 30.0
    threshold_width: float = 4.0

    # bistability
    high_threshold: float = 42.0
    low_threshold: float = 18.0
    low_activity: float = 0.25
    high_activity: float = 1.0

    # identity branching and errors
    gate: float = 1.0
    off_target_prob: float = 0.02
    phase_gate_phi: float | None = None

    # poisoning / inhibition / drains
    stress_d: float = 0.0
    product_inhibition_strength: float = 0.0
    product_inhibition_k: float = 60.0
    p_drain: float = 0.06
    q_drain: float = 0.06
    pprime_drain: float = 0.06
    a_leak: float = 0.01


class ConverterCore:
    def __init__(self, params: ConverterParams):
        self.p = params
        self.rng = np.random.default_rng(params.seed)
        self.A = 0
        self.P = 0
        self.Q = 0
        self.Pprime = 0
        self.mode_state = 0  # used by bistable

    def effective_gate(self) -> float:
        if self.p.phase_gate_phi is None:
            return float(np.clip(self.p.gate, 0.0, 1.0))
        # Forward-compatible hook for later phase/coherence tests.
        # Classical-effective interpretation here: a tunable continuous gate.
        return float(np.cos(self.p.phase_gate_phi / 2.0) ** 2)

    @staticmethod
    def sigmoid(x: float) -> float:
        if x > 60:
            return 1.0
        if x < -60:
            return 0.0
        return 1.0 / (1.0 + math.exp(-x))

    def activity(self) -> float:
        p = self.p
        base = self.A / (p.km + max(1.0, float(self.A)))
        stress_factor = max(0.0, 1.0 - 0.75 * p.stress_d)

        if p.mode == "linear_control":
            mode_factor = 1.0
        elif p.mode == "threshold":
            mode_factor = self.sigmoid((self.A - p.threshold) / max(1e-9, p.threshold_width))
        elif p.mode == "bistable":
            if self.mode_state == 0 and self.A >= p.high_threshold:
                self.mode_state = 1
            elif self.mode_state == 1 and self.A <= p.low_threshold:
                self.mode_state = 0
            mode_factor = p.high_activity if self.mode_state else p.low_activity
        elif p.mode == "inhibition":
            inhibition = 1.0 / (1.0 + p.product_inhibition_strength * self.P / max(1e-9, p.product_inhibition_k))
            mode_factor = inhibition
        else:
            raise ValueError(f"unknown mode {p.mode}")

        return float(np.clip(base * mode_factor * stress_factor, 0.0, 1.0))

    def step(self) -> Dict[str, float]:
        p = self.p

        arrivals = int(self.rng.poisson(p.input_flux))
        self.A += arrivals

        # substrate leak before conversion
        a_leak_count = int(self.rng.binomial(self.A, min(max(p.a_leak + 0.03 * p.stress_d, 0.0), 1.0)))
        self.A -= a_leak_count

        act = self.activity()
        p_convert = float(np.clip(p.base_convert_prob * act, 0.0, 1.0))
        converted = int(self.rng.binomial(self.A, p_convert)) if self.A > 0 else 0
        self.A -= converted

        # stress increases off-target/meaning drift
        off_p = float(np.clip(p.off_target_prob * (1.0 + 4.0 * p.stress_d), 0.0, 0.95))
        off_target = int(self.rng.binomial(converted, off_p)) if converted > 0 else 0
        on_target = converted - off_target

        gate = self.effective_gate()
        if p.mode == "bistable":
            # low mode mostly P, high mode mostly Q, with gate still modulating P fraction.
            p_to_p = 0.85 * gate if self.mode_state == 0 else 0.15 * gate
        else:
            p_to_p = gate

        p_count = int(self.rng.binomial(on_target, float(np.clip(p_to_p, 0.0, 1.0)))) if on_target > 0 else 0
        q_count = on_target - p_count

        self.P += p_count
        self.Q += q_count
        self.Pprime += off_target

        p_out = int(self.rng.binomial(self.P, p.p_drain)) if self.P > 0 else 0
        q_out = int(self.rng.binomial(self.Q, p.q_drain)) if self.Q > 0 else 0
        pp_out = int(self.rng.binomial(self.Pprime, p.pprime_drain)) if self.Pprime > 0 else 0
        self.P -= p_out
        self.Q -= q_out
        self.Pprime -= pp_out

        return {
            "arrivals": arrivals,
            "a_leak": a_leak_count,
            "converted": converted,
            "P_created": p_count,
            "Q_created": q_count,
            "Pprime_created": off_target,
            "P_out": p_out,
            "Q_out": q_out,
            "Pprime_out": pp_out,
            "A_stock": self.A,
            "P_stock": self.P,
            "Q_stock": self.Q,
            "Pprime_stock": self.Pprime,
            "activity": act,
            "gate": gate,
            "mode_state": float(self.mode_state),
        }

    def run(self) -> Dict[str, Any]:
        rows: List[Dict[str, float]] = []
        for _ in range(self.p.steps):
            rows.append(self.step())

        tail = rows[self.p.burn_in :]
        sums = {k: float(sum(r[k] for r in tail)) for k in tail[0].keys()}
        n = max(1, len(tail))
        input_total = sums["arrivals"]
        converted = sums["converted"]
        p_created = sums["P_created"]
        q_created = sums["Q_created"]
        pprime_created = sums["Pprime_created"]

        def safe_div(a: float, b: float) -> float:
            return float(a / b) if b else 0.0

        metrics = {
            "input_flux": safe_div(input_total, n),
            "conversion_flux": safe_div(converted, n),
            "P_flux": safe_div(p_created, n),
            "Q_flux": safe_div(q_created, n),
            "Pprime_flux": safe_div(pprime_created, n),
            "conversion_efficiency": safe_div(converted, input_total),
            "fidelity_P_fraction": safe_div(p_created, converted),
            "promiscuity_Pprime_fraction": safe_div(pprime_created, converted),
            "Q_branch_fraction": safe_div(q_created, converted),
            "P_over_Q_ratio": safe_div(p_created, q_created),
            "A_mean": safe_div(sums["A_stock"], n),
            "P_mean": safe_div(sums["P_stock"], n),
            "Q_mean": safe_div(sums["Q_stock"], n),
            "Pprime_mean": safe_div(sums["Pprime_stock"], n),
            "activity_mean": safe_div(sums["activity"], n),
            "mode_state_mean": safe_div(sums["mode_state"], n),
            "P_out_flux": safe_div(sums["P_out"], n),
            "Q_out_flux": safe_div(sums["Q_out"], n),
            "Pprime_out_flux": safe_div(sums["Pprime_out"], n),
        }
        return {
            "params": asdict(self.p),
            "metrics": {k: round(v, 6) for k, v in metrics.items()},
        }


def run_condition(mode: Mode, seed: int, **kwargs: Any) -> Dict[str, Any]:
    params = ConverterParams(mode=mode, seed=seed, **kwargs)
    return ConverterCore(params).run()


def make_sweeps(seed: int) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "experiment": "converter_core",
        "date": "2026-07-07",
        "model": "classical stochastic phenomenology; not quantum",
        "seed": seed,
        "sweeps": {},
    }

    input_fluxes = [0.25, 0.5, 1.0, 2.0, 4.0, 7.0, 10.0]
    out["sweeps"]["conversion_throughput"] = [
        {"mode": mode, "input_flux_setting": f, **run_condition(mode, seed + i + 100 * j, input_flux=f)["metrics"]}
        for j, mode in enumerate(["linear_control", "threshold", "inhibition"])
        for i, f in enumerate(input_fluxes)
    ]

    off_targets = [0.0, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]
    out["sweeps"]["fidelity_promiscuity"] = [
        {
            "off_target_setting": o,
            **run_condition("threshold", seed + 1000 + i, input_flux=4.0, off_target_prob=o)["metrics"],
        }
        for i, o in enumerate(off_targets)
    ]

    gates = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]
    out["sweeps"]["gating_conditional_response"] = [
        {
            "gate_setting": g,
            **run_condition("threshold", seed + 2000 + i, input_flux=4.0, gate=g)["metrics"],
        }
        for i, g in enumerate(gates)
    ]

    phase_gates = [0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4, math.pi]
    out["sweeps"]["phase_gate_hook_classical_effective"] = [
        {
            "phase_phi": round(phi, 6),
            "gate_effective": round(math.cos(phi / 2) ** 2, 6),
            **run_condition("threshold", seed + 2500 + i, input_flux=4.0, phase_gate_phi=phi)["metrics"],
        }
        for i, phi in enumerate(phase_gates)
    ]

    stresses = [0.0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0]
    out["sweeps"]["stability_poisoning"] = [
        {
            "stress_d": d,
            **run_condition("inhibition", seed + 3000 + i, input_flux=4.0, product_inhibition_strength=2.0, stress_d=d)["metrics"],
        }
        for i, d in enumerate(stresses)
    ]

    # Hysteresis loop: sweep input up and down using different seeds but same model.
    up = [0.5, 1.0, 2.0, 4.0, 7.0, 10.0]
    down = list(reversed(up))
    out["sweeps"]["bistable_hysteresis_up"] = [
        {"direction": "up", "input_flux_setting": f, **run_condition("bistable", seed + 4000 + i, input_flux=f)["metrics"]}
        for i, f in enumerate(up)
    ]
    out["sweeps"]["bistable_hysteresis_down"] = [
        {"direction": "down", "input_flux_setting": f, **run_condition("bistable", seed + 5000 + i, input_flux=f)["metrics"]}
        for i, f in enumerate(down)
    ]

    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=8128)
    parser.add_argument("--out", type=Path, default=Path("data/converter/converter_core_seed8128.json"))
    args = parser.parse_args()

    result = make_sweeps(args.seed)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
