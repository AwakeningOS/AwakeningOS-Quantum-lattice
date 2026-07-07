# Quantum Microreactor Gamma Sweep Quality Probe Protocol

Date: 2026-07-08

Status: `PROTOCOL`
Layer: `quantum-audit probe`

## Question

After the gamma=max validation gate passed, does a first gamma sweep reveal any quantum-specific usefulness of a quality-as-coherence probe?

The test is deliberately conservative:

```text
Arm 1: scalar classical sandbox
Arm 2: classical complex-wave control
Arm 3: density-matrix quantum proxy
```

A gamma-sensitive effect is not quantum-specific if Arm 2 reproduces it.

## Prior gate

The prerequisite gate is:

```text
quantum_microreactor_gamma_validation_2026-07-08.md
```

That gate passed:

```text
7 scenarios
24 metrics per scenario
168 comparisons
max_abs_error_overall = 0
gamma=max diagonal/population embedding reproduces the scalar sandbox summaries
```

## Layer

```text
quantum-audit probe
```

This is not a quantum-specific positive result unless Arm 3 shows an observable effect that Arm 2 cannot reproduce.

## Model

The probe imports the existing scalar sandbox summaries from:

```text
scripts/phenomenology/information_microreactor_sandbox.py
```

For each scenario, the scalar `mean_quality` is treated as the validated Z/population quality observable:

```text
mean_quality_z = scalar mean_quality
```

The auxiliary coherence probe is:

```text
coherence_quality_proxy = (1 - gamma) * sqrt(mean_quality_z * (1 - mean_quality_z))
```

This is added only as an auxiliary probe. It does not replace scalar quality, because replacing scalar quality with pure coherence would fail gamma=max validation.

## Gamma values

```text
gamma = 1.0   full dephase / classical limit
gamma = 0.75
gamma = 0.50
gamma = 0.25
gamma = 0.0   coherent limit
```

## Arms

```text
arm1_scalar:
  original scalar sandbox summary observables
  coherence_quality_proxy = 0
  negativity = 0

arm2_complex_wave:
  classical complex-wave control with the same coherence_quality_proxy
  negativity = 0

arm3_quantum_dm:
  density-matrix proxy with the same coherence_quality_proxy
  negativity proxy = coherence_quality_proxy
```

## Observables

```text
P_release
mean_quality_z
coherence_quality_proxy
purity_proxy
negativity
```

The important existing sandbox observables are:

```text
P_release
mean_quality_z
```

## Success criteria for quantum-specific usefulness

A positive quantum-specific result would require all of the following:

```text
1. Arm 3 changes an existing observable such as P_release or mean_quality_z
2. The change varies with gamma
3. Arm 2 cannot reproduce the same observable change
4. Arm 3 has a witness such as negativity/purity/basis dependence tied to that observable change
```

## Failure / negative criteria

The result is not quantum-specific if any of these happen:

```text
1. only auxiliary coherence changes while P_release and mean_quality_z stay fixed
2. Arm 2 reproduces the same coherence proxy
3. Arm 3 negativity exists but does not change any existing observable
4. gamma sensitivity appears only in an auxiliary variable that is not coupled back into the sandbox
```

## Expected raw outputs

```text
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv
data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707.json
```

## Run command

```bash
python scripts/audit/quantum_microreactor_gamma_sweep_quality_probe.py \
  --seed 20260707 \
  --out data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707.json \
  --summary-csv data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_summary.csv \
  --detail-csv data/quantum_microreactor/gamma_sweep_quality_probe_seed20260707_detail.csv
```

## Forbidden claims

Do not claim:

```text
quantum advantage
quantum-specific behavior
coherence improves release
negativity is functionally active
quality is proven to be quantum coherence
hardware relevance
```

## Intended interpretation

This is an early screening probe. A negative result is useful because it sorts out a naive or Arm2-reproducible quantumization route before spending effort on heavier density-matrix or hardware experiments.
