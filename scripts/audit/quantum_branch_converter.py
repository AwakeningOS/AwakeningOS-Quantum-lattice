#!/usr/bin/env python3
"""
Phase-dependent branching converter with entangled control (C:B), embedded in the
microreactor. Tests whether quantum coherence/entanglement reaches a TRANSPORTED
observable (P_release), or only lives in a channel (negativity) the plumbing ignores.

gamma = dephasing on the C-B system. gamma=1 -> classical 50/50 branch (gate).
"""
from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass

@dataclass(frozen=True)
class Params:
    A_rate: float=2.0; B_rate: float=0.15; D_rate: float=0.02; C_rate: float=0.02
    pore_A: float=0.08; pore_B: float=0.005; capacity: float=120.0
    release_rate: float=0.035; sink_cap: float=999.0; k_conv: float=0.65
    damage_coeff: float=0.015; repair_coeff: float=0.006; stabilizer_protect: float=0.80
    poison_coeff: float=1.2; quality_coeff: float=2.0; backpressure_strength: float=0.65
    road_source_gain: float=0.0; terrain_write: float=0.04; terrain_decay: float=0.985
    pulse_amp: float=0.25

def scenarios():
    return {"normal":Params(),"stress":Params(D_rate=0.45,C_rate=0.0),
            "storage_heavy":Params(capacity=40.0,release_rate=0.003,backpressure_strength=0.9)}

STEPS=800; BURN=200

I2=np.eye(2,dtype=complex); Z=np.array([[1,0],[0,-1]],dtype=complex)
def Ry(t): c,s=math.cos(t/2),math.sin(t/2); return np.array([[c,-s],[s,c]],dtype=complex)
def RZ(t): return np.array([[np.exp(-1j*t/2),0],[0,np.exp(1j*t/2)]],dtype=complex)
H=(1/math.sqrt(2))*np.array([[1,1],[1,-1]],dtype=complex)
def kron(a,b): return np.kron(a,b)

def dephase(rho,g):
    M=np.ones((4,4))*(1-g)+np.eye(4)*g   # off-diag *= (1-g), diag *=1
    return rho*M

def negativity(rho):
    # partial transpose on subsystem B (qubit index 1), basis (c,b)->2c+b
    pt=np.zeros_like(rho)
    for c in range(2):
        for cp in range(2):
            for b in range(2):
                for bp in range(2):
                    pt[2*c+b,2*cp+bp]=rho[2*c+bp,2*cp+b]
    ev=np.linalg.eigvalsh((pt+pt.conj().T)/2)
    return float(sum(abs(e) for e in ev if e<0))

def quantum_branch(phi,gamma):
    """Return (P_B0, negativity, ZZ) for one converter application."""
    psi=kron(H@np.array([1,0],dtype=complex), Ry(math.pi/2)@np.array([1,0],dtype=complex))
    rho=np.outer(psi,psi.conj())
    # controlled-RZ(phi): RZ on B iff C=1
    CU=np.zeros((4,4),dtype=complex); CU[0:2,0:2]=I2; CU[2:4,2:4]=RZ(phi)
    rho=CU@rho@CU.conj().T
    rho=dephase(rho,gamma)
    Ub=kron(I2,Ry(-math.pi/2)); rho=Ub@rho@Ub.conj().T
    projB0=kron(I2,np.array([[1,0],[0,0]],dtype=complex))
    P_B0=float(np.real(np.trace(rho@projB0)))
    ZZ=float(np.real(np.trace(rho@kron(Z,Z))))
    return P_B0,negativity(rho),ZZ

def classical_branch(phi):
    return 0.5  # independent baseline: dephased MZ -> maximally mixed B -> 50/50

def arm2_branch(phi):
    """single-qubit complex wave (no control C), phase = mean-field <C=1>*phi = phi/2."""
    b=Ry(-math.pi/2)@RZ(phi/2)@Ry(math.pi/2)@np.array([1,0],dtype=complex)
    return float(abs(b[0])**2)

def simulate(p,mode,gamma=1.0):
    inside_A=inside_B=reservoir=terrain=0.0; integrity=1.0
    rows=[]
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
        amount=conv_rate*inside_A
        phi=math.pi*(1.0-integrity)   # reactor context -> branch phase
        neg=0.0
        if mode=="classical": yb=classical_branch(phi)
        elif mode=="quantum": yb,neg,_=quantum_branch(phi,gamma)
        elif mode=="arm2":     yb=arm2_branch(phi)
        else: raise ValueError
        P_to_reservoir=amount*yb
        inside_A-=amount
        quality=1.0/(1.0+p.quality_coeff*inside_B); inside_B*=0.985
        available=max(0.0,p.capacity-reservoir); P_accept=min(P_to_reservoir,available)
        reservoir+=P_accept
        release=min(reservoir,reservoir*p.release_rate,p.sink_cap); reservoir-=release
        terrain=terrain*p.terrain_decay+release*p.terrain_write*quality
        rows.append(dict(t=t,release=release,reservoir=reservoir,integrity=integrity,
                         quality=quality,yb=yb,neg=neg,phi=phi))
    return rows

def Prel(rows): return sum(r["release"] for r in rows[BURN:])
def meanneg(rows): return sum(r["neg"] for r in rows[BURN:])/len(rows[BURN:])
def maxneg(rows): return max(r["neg"] for r in rows[BURN:])

if __name__=="__main__":
    # sanity: Bell state negativity should be 0.5
    bell=np.array([1,0,0,1],dtype=complex)/math.sqrt(2); rb=np.outer(bell,bell.conj())
    print(f"[sanity] Bell negativity = {negativity(rb):.4f} (expect 0.5)")
    print(f"[sanity] quantum(gamma=1) P_B0 for phi=0..pi: "
          f"{[round(quantum_branch(x,1.0)[0],3) for x in [0,math.pi/2,math.pi]]} (expect all 0.5)\n")

    scs=scenarios()
    print("="*72); print("GATE: quantum(gamma=1) release vs classical release"); print("="*72)
    for n,p in scs.items():
        d=abs(Prel(simulate(p,"quantum",1.0))-Prel(simulate(p,"classical")))
        print(f"  {n:14s} |diff|={d:.2e}  {'PASS' if d<1e-9 else 'FAIL'}")

    print("\n"+"="*72)
    print("CH1 TRANSPORTED (P_release): quantum dev% from classical, + Arm2 dev%")
    print("="*72)
    gammas=[1.0,0.5,0.0]
    for n,p in scs.items():
        base=Prel(simulate(p,"classical")); a2=Prel(simulate(p,"arm2"))
        qs=[100*(Prel(simulate(p,"quantum",g))-base)/base for g in gammas]
        a2dev=100*(a2-base)/base
        print(f"  {n:14s} quantum[g=1,.5,0]={qs[0]:+6.1f}%{qs[1]:+6.1f}%{qs[2]:+6.1f}%   Arm2={a2dev:+6.1f}%")

    print("\n"+"="*72)
    print("Arm2 vs quantum(g=0) on TRANSPORTED release: can classical wave match it?")
    print("="*72)
    for n,p in scs.items():
        q0=Prel(simulate(p,"quantum",0.0)); a2=Prel(simulate(p,"arm2"))
        print(f"  {n:14s} quantum(g=0)={q0:8.3f}  Arm2={a2:8.3f}  |diff|={abs(q0-a2):.3e}  match={'YES' if abs(q0-a2)<1e-9 else 'NO'}")

    print("\n"+"="*72)
    print("CH2 QUANTUM-SPECIFIC (negativity C:B): does entanglement exist? does it transport?")
    print("="*72)
    for n,p in scs.items():
        for g in gammas:
            r=simulate(p,"quantum",g)
            print(f"  {n:14s} g={g:.1f}  mean_neg={meanneg(r):.4f}  max_neg={maxneg(r):.4f}")
        # correlation between negativity and what gets transported:
        r0=simulate(p,"quantum",0.0)
        negs=[x["neg"] for x in r0[BURN:]]; rels=[x["release"] for x in r0[BURN:]]
        if np.std(negs)>1e-12 and np.std(rels)>1e-12:
            corr=np.corrcoef(negs,rels)[0,1]
        else: corr=float("nan")
        print(f"  {n:14s} corr(negativity, release) @g=0 = {corr:+.3f}\n")
