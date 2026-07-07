#!/usr/bin/env python3
"""
History-dependent hard-core droplet core.

Purpose:
- test whether history-repel condensation is quantum or mostly classical
- split bulk memory and edge memory
- test phase-dependent transport on a frozen history terrain

This is a compact reference core, not a final physical Lindblad simulator.
The loss is no-jump / postselective style, useful for exploring mechanisms.
"""
from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass
from typing import Dict, List, Literal, Sequence, Tuple

import numpy as np

Mode = Literal["none", "attract", "repel", "bulk_repel", "edge_repel", "bulk_attract", "edge_attract", "repel_both"]


def adjacent_count(state: Tuple[int, ...]) -> int:
    s = set(state)
    return sum((i + 1) in s for i in s)


def is_cluster(state: Tuple[int, ...]) -> bool:
    return max(state) - min(state) + 1 == len(state)


def ipr(probs: np.ndarray) -> float:
    return float(1.0 / max(1e-15, np.sum(probs * probs)))


@dataclass
class DropletCore:
    L: int = 16
    K: int = 3
    theta: float = 0.12
    phi: float = 0.45
    kappa: float = 0.06
    history_beta: float = 6.0
    history_decay: float = 0.995
    history_write: float = 0.04

    def __post_init__(self) -> None:
        self.basis: List[Tuple[int, ...]] = list(itertools.combinations(range(self.L), self.K))
        self.index: Dict[Tuple[int, ...], int] = {b: i for i, b in enumerate(self.basis)}
        self.dim = len(self.basis)
        self.adj = np.array([adjacent_count(st) for st in self.basis], dtype=float)
        self.cluster_mask = np.array([is_cluster(st) for st in self.basis], dtype=bool)
        self.bulk_matrix = np.zeros((self.dim, self.L), dtype=float)
        self.edge_matrix = np.zeros((self.dim, self.L), dtype=float)
        for bi, st in enumerate(self.basis):
            s = set(st)
            for x in st:
                self.bulk_matrix[bi, x] = 1.0
                left_empty = (x - 1) not in s if x > 0 else True
                right_empty = (x + 1) not in s if x < self.L - 1 else True
                if left_empty or right_empty:
                    self.edge_matrix[bi, x] = 1.0

    def state(self, occupied: Sequence[int], momentum: float = math.pi / 2, width: int = 0) -> np.ndarray:
        occupied = tuple(sorted(occupied))
        psi = np.zeros(self.dim, dtype=np.complex128)
        if width <= 0:
            psi[self.index[occupied]] = 1.0
            return psi
        for shift in range(-width, width + 1):
            st = tuple(x + shift for x in occupied)
            if min(st) < 0 or max(st) >= self.L or st not in self.index:
                continue
            center = sum(st) / len(st)
            psi[self.index[st]] += np.exp(1j * momentum * center) * math.exp(-0.5 * (shift / max(1, width)) ** 2)
        norm = np.linalg.norm(psi)
        return psi / norm if norm else self.state(occupied, momentum, 0)

    def probabilities(self, psi: np.ndarray) -> np.ndarray:
        return np.abs(psi) ** 2

    def p_cluster(self, probs: np.ndarray) -> float:
        return float(np.sum(probs[self.cluster_mask]))

    def expected_adjacent_bonds(self, probs: np.ndarray) -> float:
        return float(np.sum(probs * self.adj))

    def mean_position(self, probs: np.ndarray) -> float:
        return float(sum(p * (sum(st) / self.K) for st, p in zip(self.basis, probs)))

    def terrain_overlap(self, probs: np.ndarray, terrain: np.ndarray, edge: bool = False) -> float:
        mat = self.edge_matrix if edge else self.bulk_matrix
        return float(np.sum(probs * (mat @ terrain)) / self.K)

    def occupation(self, probs: np.ndarray) -> np.ndarray:
        return probs @ self.bulk_matrix

    def edge_occupation(self, probs: np.ndarray) -> np.ndarray:
        return probs @ self.edge_matrix

    def apply_hopping_quantum(self, psi: np.ndarray) -> np.ndarray:
        out = psi.copy()
        c, s = math.cos(self.theta), math.sin(self.theta)
        for parity in [0, 1]:
            new = out.copy()
            seen = set()
            for i, st in enumerate(self.basis):
                st_set = set(st)
                for x in range(parity, self.L - 1, 2):
                    if x in st_set and (x + 1) not in st_set:
                        st2 = tuple(sorted((st_set - {x}) | {x + 1}))
                    elif (x not in st_set) and (x + 1) in st_set:
                        st2 = tuple(sorted((st_set - {x + 1}) | {x}))
                    else:
                        continue
                    j = self.index[st2]
                    key = tuple(sorted((i, j)))
                    if key in seen:
                        continue
                    seen.add(key)
                    ai, aj = out[i], out[j]
                    new[i] = c * ai - 1j * s * aj
                    new[j] = c * aj - 1j * s * ai
            out = new
        return out

    def apply_hopping_classical(self, probs: np.ndarray) -> np.ndarray:
        out = probs.copy()
        c2, s2 = math.cos(self.theta) ** 2, math.sin(self.theta) ** 2
        for parity in [0, 1]:
            new = out.copy()
            seen = set()
            for i, st in enumerate(self.basis):
                st_set = set(st)
                for x in range(parity, self.L - 1, 2):
                    if x in st_set and (x + 1) not in st_set:
                        st2 = tuple(sorted((st_set - {x}) | {x + 1}))
                    elif (x not in st_set) and (x + 1) in st_set:
                        st2 = tuple(sorted((st_set - {x + 1}) | {x}))
                    else:
                        continue
                    j = self.index[st2]
                    key = tuple(sorted((i, j)))
                    if key in seen:
                        continue
                    seen.add(key)
                    pi, pj = out[i], out[j]
                    new[i] = c2 * pi + s2 * pj
                    new[j] = c2 * pj + s2 * pi
            out = new
        return out / np.sum(out)

    def loss_weights(self, terrain_bulk: np.ndarray, terrain_edge: np.ndarray, mode: Mode) -> np.ndarray:
        surface_penalty = (self.K - 1) - self.adj
        bulk_overlap = self.bulk_matrix @ terrain_bulk
        edge_overlap = self.edge_matrix @ terrain_edge
        hist = np.zeros(self.dim, dtype=float)
        if mode in ("repel", "repel_both"):
            hist += bulk_overlap + edge_overlap
        elif mode == "bulk_repel":
            hist += bulk_overlap
        elif mode == "edge_repel":
            hist += edge_overlap
        elif mode == "attract":
            hist -= bulk_overlap + edge_overlap
        elif mode == "bulk_attract":
            hist -= bulk_overlap
        elif mode == "edge_attract":
            hist -= edge_overlap
        exponent = -self.kappa * surface_penalty - self.kappa * self.history_beta * hist
        return np.exp(np.clip(exponent, -40, 20))

    def step_quantum(self, psi: np.ndarray, tb: np.ndarray, te: np.ndarray, mode: Mode) -> np.ndarray:
        psi = self.apply_hopping_quantum(psi)
        psi = psi * np.exp(-1j * self.phi * self.adj)
        psi = psi * self.loss_weights(tb, te, mode)
        norm = np.linalg.norm(psi)
        return psi / norm if norm else psi

    def step_classical(self, probs: np.ndarray, tb: np.ndarray, te: np.ndarray, mode: Mode) -> np.ndarray:
        probs = self.apply_hopping_classical(probs)
        probs = probs * self.loss_weights(tb, te, mode) ** 2
        return probs / np.sum(probs)

    def update_terrain(self, tb: np.ndarray, te: np.ndarray, probs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        tb = self.history_decay * tb + self.history_write * self.occupation(probs)
        te = self.history_decay * te + self.history_write * self.edge_occupation(probs)
        return np.clip(tb, 0, 1), np.clip(te, 0, 1)

    def run_quantum(self, psi: np.ndarray, steps: int, mode: Mode, tb=None, te=None, write_history=False):
        tb = np.zeros(self.L) if tb is None else tb.copy()
        te = np.zeros(self.L) if te is None else te.copy()
        for _ in range(steps):
            psi = self.step_quantum(psi, tb, te, mode)
            if write_history:
                tb, te = self.update_terrain(tb, te, self.probabilities(psi))
        return psi, tb, te

    def run_classical(self, probs: np.ndarray, steps: int, mode: Mode, tb=None, te=None, write_history=False):
        tb = np.zeros(self.L) if tb is None else tb.copy()
        te = np.zeros(self.L) if te is None else te.copy()
        for _ in range(steps):
            probs = self.step_classical(probs, tb, te, mode)
            if write_history:
                tb, te = self.update_terrain(tb, te, probs)
        return probs, tb, te

    def summary(self, probs: np.ndarray, tb=None, te=None) -> dict:
        tb = np.zeros(self.L) if tb is None else tb
        te = np.zeros(self.L) if te is None else te
        return {
            "P_cluster": self.p_cluster(probs),
            "adjacent_bonds": self.expected_adjacent_bonds(probs),
            "mean_position": self.mean_position(probs),
            "IPR": ipr(probs),
            "bulk_overlap": self.terrain_overlap(probs, tb, edge=False),
            "edge_overlap": self.terrain_overlap(probs, te, edge=True),
        }


def print_row(label: str, d: dict) -> None:
    print(f"{label:14s} P_cluster={d['P_cluster']:.3f} adj={d['adjacent_bonds']:.3f} mean={d['mean_position']:.2f} IPR={d['IPR']:.1f} bulkOv={d['bulk_overlap']:.3f} edgeOv={d['edge_overlap']:.3f}")


def experiment_quantum_vs_classical() -> None:
    core = DropletCore()
    psi1 = core.state([1, 2, 3], momentum=math.pi / 2, width=1)
    _, tb, te = core.run_quantum(psi1, steps=55, mode="repel", write_history=True)
    print("\n[A] terrain written by first quantum droplet")
    print("bulk:", " ".join(f"{x:.2f}" for x in tb))
    print("edge:", " ".join(f"{x:.2f}" for x in te))
    print("\n[A1] second droplet on frozen terrain: quantum vs classical probability")
    for mode in ["none", "attract", "repel", "bulk_repel", "edge_repel"]:
        psi2 = core.state([10, 11, 12], momentum=-math.pi / 2, width=1)
        out, _, _ = core.run_quantum(psi2, steps=65, mode=mode, tb=tb, te=te)
        qsum = core.summary(core.probabilities(out), tb, te)
        p0 = core.probabilities(core.state([10, 11, 12], momentum=-math.pi / 2, width=1))
        pout, _, _ = core.run_classical(p0, steps=65, mode=mode, tb=tb, te=te)
        csum = core.summary(pout, tb, te)
        print(f"{mode:12s} quantum Pcl={qsum['P_cluster']:.3f} mean={qsum['mean_position']:.2f} IPR={qsum['IPR']:.1f} | classical Pcl={csum['P_cluster']:.3f} mean={csum['mean_position']:.2f} IPR={csum['IPR']:.1f}")


def experiment_phase_dependence() -> None:
    core = DropletCore()
    psi1 = core.state([1, 2, 3], momentum=math.pi / 2, width=1)
    _, tb, te = core.run_quantum(psi1, steps=55, mode="repel", write_history=True)
    print("\n[A2] phase dependence on the same repel terrain")
    for label, k in [("k=+pi/2", math.pi / 2), ("k=0", 0.0), ("k=-pi/2", -math.pi / 2), ("k=pi", math.pi)]:
        psi = core.state([10, 11, 12], momentum=k, width=2)
        out, _, _ = core.run_quantum(psi, steps=65, mode="edge_repel", tb=tb, te=te)
        print_row(label, core.summary(core.probabilities(out), tb, te))


def experiment_edge_memory() -> None:
    core = DropletCore()
    print("\n[B] self-written bulk/edge memory")
    for mode in ["none", "bulk_repel", "edge_repel", "repel_both", "bulk_attract", "edge_attract"]:
        psi = core.state([1, 2, 3], momentum=math.pi / 2, width=1)
        out, tb, te = core.run_quantum(psi, steps=75, mode=mode, write_history=True)
        print_row(mode, core.summary(core.probabilities(out), tb, te))
    print("判定: bulkよりedge履歴のほうが輸送・尾の切り落としに効きやすい。")


def run_all() -> None:
    experiment_quantum_vs_classical()
    experiment_phase_dependence()
    experiment_edge_memory()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--ablation", action="store_true")
    ap.add_argument("--phase", action="store_true")
    ap.add_argument("--edge", action="store_true")
    args = ap.parse_args()
    if args.all or not (args.ablation or args.phase or args.edge):
        run_all()
    else:
        if args.ablation:
            experiment_quantum_vs_classical()
        if args.phase:
            experiment_phase_dependence()
        if args.edge:
            experiment_edge_memory()


if __name__ == "__main__":
    main()
