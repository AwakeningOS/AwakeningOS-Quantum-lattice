# Phase-channel controls

Date: 2026-07-07

Purpose: after framing the pseudo-material as mostly classical-effective, test whether the phase-routed reaction-channel effect survives stronger controls.

## Question

The correct question is not:

```text
Is the whole pseudo-material quantum?
```

The better question is:

```text
Given classical-effective reaction channels,
does phase/coherence add an extra control layer over channel choice?
```

## Controls applied

### 1. Classical probability control

Same initial support and same loss/compatibility rules, but no complex phase.

Result: no phase dependence is possible. It gives a single material baseline.

### 2. Per-step dephase control

After each step, phase coherence is killed in the configuration basis, then the same loss/compatibility rule is applied.

Result: delta-dependent channel differences collapse. This means the phase-routing effect is coherence-dependent.

### 3. Classical complex-wave control

Allow a complex wave over the same configuration graph, with the same phase, same loss, and same compatibility rules.

Result: the phase-routing effect is reproduced by the complex-wave control. Therefore the channel shift is not uniquely quantum by itself.

### 4. Entanglement/negativity check

C:AB block entanglement and related coherence measures can change with the channel balance, but in this control set they do not prove that channel selection requires many-body entanglement.

## Verdict

The previous phrase:

```text
phase as reaction-channel selector
```

survives against classical probability/dephase controls, but does **not** survive as a uniquely quantum claim against classical complex-wave control.

Corrected statement:

```text
The pseudo-material channels are classical-effective.
Coherence/phase can bias channel selection.
That phase bias is wave-like and coherence-dependent.
To claim a quantum-specific effect, it must be tied to negativity, nonseparability, measurement backaction, or dephase-sensitive many-body entanglement, not phase alone.
```

## Important shift

This is not a failure. It clarifies the architecture:

```text
classical-effective material layer:
  liquid droplets, interfaces, surface adsorption, toxicity, bridges, reaction channels

coherence/phase layer:
  route/channel bias among open channels

strict quantum layer:
  negativity, block entanglement, measurement-induced reconfiguration, dephase-killed effects
```

## Next experiment target

Move from phase-only routing to a stricter witness:

```text
coherence-gated chemistry with negativity witness
```

Look for cases where:

1. classical probability cannot reproduce the channel shift,
2. classical complex wave reproduces phase but has no negativity witness,
3. dephase kills the channel shift,
4. channel selection correlates with pair negativity or block entanglement in a way not reducible to single-particle interference.

Possible minimal setup:

```text
Two C-like incoming droplets with opposite phases
AB surface with two possible reaction sites
reaction occurs only when an entangled two-particle contact state forms
compare:
  coherent many-body state
  dephased probability state
  separable complex-wave control
```
