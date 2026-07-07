#!/usr/bin/env python3
"""Correct Arm2 reduced-channel control for transported branching converter."""
import math
import numpy as np
from quantum_branch_converter import Params, scenarios, simulate, Prel, I2, Ry, RZ, STEPS, BURN

# Correct Arm2: single-qubit B channel = C-averaged (C traced out).
# This is a classical mixture of unitaries + dephasing on ONE qubit => negativity impossible.
def arm2_reduced_branch(phi,gamma):
    psi_b=Ry(math.pi/2)@np.array([1,0],dtype=complex)
    rho0=np.outer(psi_b,psi_b.conj())
    U0=I2; U1=RZ(phi)
    rho_b=0.5*(U0@rho0@U0.conj().T)+0.5*(U1@rho0@U1.conj().T)   # trace over C=+/- => avg over C=0/1
    rho_b=rho_b*(np.ones((2,2))*(1-gamma)+np.eye(2)*gamma)      # dephase B
    Ub=Ry(-math.pi/2); rho_b=Ub@rho_b@Ub.conj().T
    return float(np.real(rho_b[0,0]))

# Rebuild loop with arm2_reduced for transported observable comparison.
def simulate_arm2reduced(p,gamma):
    inside_A=inside_B=reservoir=terrain=0.0; integrity=1.0; rows=[]
    for t in range(STEPS):
        pulse=1.0+p.pulse_amp*math.sin(2*math.pi*t/64.0)
        road_boost=1.0+p.road_source_gain*(terrain/(1.0+terrain))
        source_A=p.A_rate*pulse*road_boost
        protect=p.stabilizer_protect*(p.C_rate/(1.0+p.C_rate))
        damage=p.damage_coeff*p.D_rate*(1.0-protect); repair=p.repair_coeff*p.C_rate*(1.0-integrity)
        integrity=min(1.0,max(0.0,integrity-damage+repair))
        fill=reservoir/max(p.capacity,1e-9); backpressure=max(0.02,1.0-p.backpressure_strength*fill)
        perm_A=p.pore_A*integrity*backpressure; perm_B=p.pore_B*integrity*(1.0+0.5*(1.0-integrity))
        inside_A+=source_A*perm_A; inside_B+=p.B_rate*perm_B
        poison=1.0/(1.0+p.poison_coeff*inside_B); conv_rate=p.k_conv*poison*backpressure
        amount=conv_rate*inside_A; phi=math.pi*(1.0-integrity)
        yb=arm2_reduced_branch(phi,gamma)
        inside_A-=amount
        quality=1.0/(1.0+p.quality_coeff*inside_B); inside_B*=0.985
        available=max(0.0,p.capacity-reservoir); reservoir+=min(amount*yb,available)
        release=min(reservoir,reservoir*p.release_rate,p.sink_cap); reservoir-=release
        terrain=terrain*p.terrain_decay+release*p.terrain_write*quality
        rows.append(dict(release=release))
    return sum(r["release"] for r in rows[BURN:])

if __name__ == "__main__":
    print("="*72)
    print("CORRECT Arm2 (single-qubit reduced, zero-entanglement) vs quantum, TRANSPORTED release")
    print("="*72)
    for n,p in scenarios().items():
        for g in [0.0,0.5]:
            q=Prel(simulate(p,"quantum",g)); a=simulate_arm2reduced(p,g)
            print(f"  {n:14s} g={g:.1f}  quantum={q:9.4f}  Arm2_reduced={a:9.4f}  |diff|={abs(q-a):.2e}  match={'YES' if abs(q-a)<1e-9 else 'NO'}")
