#!/usr/bin/env python3
"""
Minimal math core for v2 quantum lattice experiments.

Checks:
- opposite/same phase wall
- quantum vs classical-wave equivalence in the single-excitation sector
- two-particle collision statistics
- adjacent-pair negativity witness
"""
from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple

import numpy as np


def bit(x: int, q: int) -> int:
    return (x >> q) & 1


def flip2(x: int, a: int, b: int) -> int:
    return x ^ (1 << a) ^ (1 << b)


def chain_bonds(n: int) -> List[Tuple[int, int]]:
    return [(i, i + 1) for i in range(n - 1)]


def ordered_chain_bonds(n: int) -> List[List[Tuple[int, int]]]:
    bonds = chain_bonds(n)
    return [bonds[0::2], bonds[1::2]]


@dataclass
class QuantumChain:
    n: int = 9
    theta: float = 0.15

    def __post_init__(self) -> None:
        self.dim = 1 << self.n

    def basis_state(self, occupied: Sequence[int]) -> np.ndarray:
        idx = 0
        for q in occupied:
            idx |= 1 << q
        psi = np.zeros(self.dim, dtype=np.complex128)
        psi[idx] = 1.0
        return psi

    def one_excitation_superposition(self, terms: Sequence[Tuple[int, complex]]) -> np.ndarray:
        psi = np.zeros(self.dim, dtype=np.complex128)
        for q, amp in terms:
            psi[1 << q] += amp
        norm = np.linalg.norm(psi)
        return psi / norm if norm else psi

    def apply_exch(self, psi: np.ndarray, a: int, b: int, theta: float | None = None) -> np.ndarray:
        if theta is None:
            theta = self.theta
        c, s = math.cos(theta), math.sin(theta)
        out = psi.copy()
        for x in range(self.dim):
            if bit(x, a) == 1 and bit(x, b) == 0:
                y = flip2(x, a, b)
                ax, ay = psi[x], psi[y]
                out[x] = c * ax - 1j * s * ay
                out[y] = c * ay - 1j * s * ax
        return out

    def apply_zz(self, psi: np.ndarray, phi: float) -> np.ndarray:
        if abs(phi) < 1e-15:
            return psi
        phase = np.ones(self.dim, dtype=np.complex128)
        for x in range(self.dim):
            adjacent = sum(bit(x, i) * bit(x, i + 1) for i in range(self.n - 1))
            phase[x] = np.exp(-1j * phi * adjacent)
        return psi * phase

    def step(self, psi: np.ndarray, phi: float = 0.0) -> np.ndarray:
        for group in ordered_chain_bonds(self.n):
            for a, b in group:
                psi = self.apply_exch(psi, a, b)
        psi = self.apply_zz(psi, phi)
        return psi / np.linalg.norm(psi)

    def evolve(self, psi: np.ndarray, steps: int, phi: float = 0.0) -> np.ndarray:
        for _ in range(steps):
            psi = self.step(psi, phi=phi)
        return psi

    def p1(self, psi: np.ndarray, q: int) -> float:
        probs = np.abs(psi) ** 2
        return float(sum(probs[x] for x in range(self.dim) if bit(x, q)))

    def two_particle_distribution(self, psi: np.ndarray) -> np.ndarray:
        dist = np.zeros((self.n, self.n), dtype=float)
        probs = np.abs(psi) ** 2
        for x, p in enumerate(probs):
            if p == 0:
                continue
            occ = [q for q in range(self.n) if bit(x, q)]
            if len(occ) == 2:
                i, j = occ
                dist[i, j] += p
                dist[j, i] += p
        return dist

    def same_side_probability(self, psi: np.ndarray, center: int = 4) -> float:
        dist = self.two_particle_distribution(psi)
        same = 0.0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if (i < center and j < center) or (i > center and j > center):
                    same += dist[i, j]
        return float(same)

    def center_involving_probability(self, psi: np.ndarray, center: int = 4) -> float:
        dist = self.two_particle_distribution(psi)
        return float(sum(dist[min(center, j), max(center, j)] for j in range(self.n) if j != center))

    def reduced_pair(self, psi: np.ndarray, a: int, b: int) -> np.ndarray:
        rho = np.zeros((4, 4), dtype=np.complex128)
        rest_mask = ~((1 << a) | (1 << b))
        for x in range(self.dim):
            ix = (bit(x, a) << 1) | bit(x, b)
            rx = x & rest_mask
            for y in range(self.dim):
                if (y & rest_mask) != rx:
                    continue
                iy = (bit(y, a) << 1) | bit(y, b)
                rho[ix, iy] += psi[x] * np.conjugate(psi[y])
        return rho

    @staticmethod
    def negativity_from_rho2(rho2: np.ndarray) -> float:
        pt = np.zeros_like(rho2)
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    for d in range(2):
                        pt[a * 2 + b, c * 2 + d] = rho2[a * 2 + d, c * 2 + b]
        vals = np.linalg.eigvalsh(pt)
        return float(np.sum(np.abs(vals[vals < 0])))

    def bond_negativities(self, psi: np.ndarray) -> List[float]:
        return [self.negativity_from_rho2(self.reduced_pair(psi, a, b)) for a, b in chain_bonds(self.n)]


@dataclass
class ClassicalWaveChain:
    n: int = 9
    theta: float = 0.15

    def superposition(self, terms: Sequence[Tuple[int, complex]]) -> np.ndarray:
        psi = np.zeros(self.n, dtype=np.complex128)
        for q, amp in terms:
            psi[q] += amp
        norm = np.linalg.norm(psi)
        return psi / norm if norm else psi

    def apply_exch(self, psi: np.ndarray, a: int, b: int) -> np.ndarray:
        c, s = math.cos(self.theta), math.sin(self.theta)
        out = psi.copy()
        aa, bb = psi[a], psi[b]
        out[a] = c * aa - 1j * s * bb
        out[b] = c * bb - 1j * s * aa
        return out

    def step(self, psi: np.ndarray) -> np.ndarray:
        for group in ordered_chain_bonds(self.n):
            for a, b in group:
                psi = self.apply_exch(psi, a, b)
        norm = np.linalg.norm(psi)
        return psi / norm if norm else psi

    def evolve(self, psi: np.ndarray, steps: int) -> np.ndarray:
        for _ in range(steps):
            psi = self.step(psi)
        return psi


def experiment_phase_wall() -> None:
    qc = QuantumChain(theta=0.15)
    wc = ClassicalWaveChain(theta=0.15)
    q_opp = qc.one_excitation_superposition([(1, 1.0), (7, -1.0)])
    q_same = qc.one_excitation_superposition([(1, 1.0), (7, 1.0)])
    w_opp = wc.superposition([(1, 1.0), (7, -1.0)])
    print("\n[A] opposite/same phase wall: center P(q4)")
    for t in [5, 10, 15, 20, 25]:
        qo = qc.evolve(q_opp.copy(), t)
        qs = qc.evolve(q_same.copy(), t)
        wo = wc.evolve(w_opp.copy(), t)
        err = abs(qc.p1(qo, 4) - abs(wo[4]) ** 2)
        print(f"tick {t:2d}: opposite={qc.p1(qo,4):.9f} same={qc.p1(qs,4):.9f} q-wave err={err:.2e}")
    print("判定: 位相壁は古典波動でも出る。量子証拠ではない。")


def experiment_two_particle_and_negativity() -> None:
    qc = QuantumChain(theta=0.15)
    psi0 = qc.basis_state([1, 7])
    print("\n[B/C] two-particle collision and negativity")
    for t in [2, 3, 4, 12, 20, 27, 42, 50]:
        psi = qc.evolve(psi0.copy(), t)
        negs = qc.bond_negativities(psi)
        print(
            f"tick {t:2d}: same_side={qc.same_side_probability(psi):.3f} "
            f"center_pair={qc.center_involving_probability(psi):.3f} "
            f"maxN={max(negs):.4f} sumN={sum(negs):.4f}"
        )
    print("判定: 主witnessは隣接negativity。古典波動/CAでは定義上ゼロ。")


def run_all() -> None:
    experiment_phase_wall()
    experiment_two_particle_and_negativity()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="run all experiments")
    ap.add_argument("--phase-wall", action="store_true")
    ap.add_argument("--two-particle", action="store_true")
    args = ap.parse_args()
    if args.all or (not args.phase_wall and not args.two_particle):
        run_all()
    else:
        if args.phase_wall:
            experiment_phase_wall()
        if args.two_particle:
            experiment_two_particle_and_negativity()


if __name__ == "__main__":
    main()
