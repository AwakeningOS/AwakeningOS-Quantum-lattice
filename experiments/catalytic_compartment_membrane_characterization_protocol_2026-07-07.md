# Catalytic Compartment Membrane Characterization Protocol

Date: 2026-07-07

Purpose: pause higher-level claims such as self-repair, division, or self-regulation, and characterize the current object as a catalytic selective-permeability compartment membrane.

## Correct current stage

The current structure is best treated as:

```text
catalytic compartment membrane
```

not yet:

```text
self-repairing compartment
self-regulating compartment
dividing compartment
metabolic system
```

The immediate task is physical-style characterization.

## Development ladder

Current intended ladder:

```text
1. selective permeability
2. inside/outside concentration difference
3. internal reaction field
4. product accumulation
5. product release
6. external terrain influence
7. membrane-state change
8. long-time stability
```

The previous pilots reached roughly:

```text
1. selective permeability: yes, in selective shell variants
2. inside/outside concentration difference: partial
3. internal reaction field: partial, via X-catalyzed A -> P and inside-law AB fusion
4. weak product release: partial
```

## Measurement targets

### 1. Permeability

For each species S in A/B/C/D:

```text
permeability(S) = crossings_into_inside(S) / contacts_with_shell(S)
```

Record both inward and outward permeability:

```text
P_in(S), P_out(S)
```

### 2. Selectivity

Primary selectivity:

```text
selectivity_A_over_B = P_in(A) / (P_in(B) + eps)
```

Useful-load selectivity:

```text
useful_selectivity = (A_inside + P_inside + 1) / (B_inside + D_inside + 1)
```

### 3. Retention

For each entered species or product:

```text
retention_time(S) = mean time from entry/creation to exit/death/conversion
```

Product retention:

```text
retention_P = mean lifetime of P inside before release or loss
```

### 4. Conversion

For catalytic conversion:

```text
conversion_A_to_P = P_created_inside / A_entered_inside
conversion_rate = P_created_inside / time
```

### 5. Product accumulation

Record:

```text
P_inside_mean
P_inside_max
P_inside_steady_state
```

If no steady state is reached, report slope:

```text
dP_inside/dt over late window
```

### 6. Product release

```text
release_flux_P = P_crossings_out / time
release_fraction_P = P_crossings_out / P_created_inside
```

### 7. Membrane integrity

Cell-level integrity:

```text
integrity_cells = intact_shell_cells / initial_shell_cells
```

Topological integrity:

```text
enclosed_area_exists: true/false
enclosed_area_size
number_of_breaches
breach_duration_mean
```

### 8. Stress response

Under D stress:

```text
D_contact_rate
D_damage_rate
integrity_drop
permeability_shift_after_D
recovery_or_decay_slope
```

Important: call this stress response, not self-repair, unless topological closure is restored and maintained.

## Parameter sweep

Sweep axes:

```text
shell_thickness:      1, 2, 3
pore_density:         0.00, 0.05, 0.10, 0.20
A_affinity:           low, medium, high
B_exclusion:          low, medium, high
C_permeability:       low, medium, high
X_catalyst_strength:  0.00, 0.25, 0.50, 1.00
P_retention:          low, medium, high
P_release_rate:       low, medium, high
D_damage_rate:        0.00, 0.05, 0.10, 0.20
```

Recommended first sweep: do not fully cross all axes. Use staged sweeps.

## Staged experiment plan

### Stage 1: passive membrane characterization

No catalyst, no P.

Vary:

```text
shell_thickness
pore_density
A_affinity
B_exclusion
C_permeability
D_damage_rate
```

Measure:

```text
P_in(A/B/C/D)
selectivity_A_over_B
integrity
stress_response
```

### Stage 2: catalytic conversion

Turn on X catalyst and A -> P conversion.

Vary:

```text
X_catalyst_strength
A_affinity
P_retention
P_release_rate
```

Measure:

```text
conversion_A_to_P
P_inside_mean/max
release_flux_P
retention_P
```

### Stage 3: product release and external terrain influence

Allow P to exit and write weak road/terrain outside.

Measure:

```text
P_export_events
external_P_terrain_sum
external_road_bias
future_A_arrival_rate_near_P_terrain
```

### Stage 4: stress characterization

Add D stress systematically.

Measure:

```text
integrity_drop
D_damage_rate
breach_duration
change in P_in(A/B/C/D) after stress
conversion_loss_after_stress
```

## Expected output format

For each condition:

```json
{
  "condition": "...",
  "P_in": {"A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0},
  "P_out": {"A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0, "P": 0.0},
  "selectivity_A_over_B": 0.0,
  "useful_selectivity": 0.0,
  "retention": {"A": 0.0, "P": 0.0},
  "conversion_A_to_P": 0.0,
  "P_inside_mean": 0.0,
  "P_inside_max": 0.0,
  "release_flux_P": 0.0,
  "integrity_cells": 0.0,
  "enclosed_area_size": 0.0,
  "breach_count": 0,
  "D_damage_rate": 0.0,
  "stress_response": "..."
}
```

## Interpretation discipline

Use these terms:

```text
selective permeability
catalytic conversion
retention
product accumulation
product release
membrane integrity
stress response
external terrain influence
```

Avoid these until demonstrated:

```text
self-repair
self-regulation
homeostasis
division
metabolism
life-like behavior
```

## Best current question

```text
What physical-style membrane properties does this information compartment have?
```

That must be answered before escalating to self-regulation, division, or nested compartments.
