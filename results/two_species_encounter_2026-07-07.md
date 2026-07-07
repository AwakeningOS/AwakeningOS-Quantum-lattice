# Two-species droplet encounter core

Date: 2026-07-07

Purpose: test what happens when an exploring droplet encounters a same-compatible or heterogeneous droplet.

## Core

Small 2D lattice, two hard-core species A/B.

- A droplet: 2 A excitations
- B droplet: 2 B excitations
- Hopping: EXCH-like hard-core motion
- Interactions: AA, BB, AB phases
- Loss: surface-selective no-jump filter
- Classical ablation: probability transition using the same loss weights, no phase

This is still an exploratory no-jump/postselective core, not a final Lindblad model.

## Outcomes

| condition | Q P_all_connected | C P_all_connected | Q AB_contact | interpretation |
|---|---:|---:|---:|---|
| neutral | 0.553 | 0.151 | 0.874 | quantum mixing/contact appears, but not robust full merging |
| same-compatible | 0.850 | 0.799 | 3.343 | same-compatible droplets merge into one mixed cluster |
| hetero-repulsive | 0.012 | 0.001 | 0.065 | heterogeneous droplets remain separated / interface avoided |
| hetero-toxic | 0.008 | 0.001 | 0.048 | stronger avoidance, AB contact suppressed |
| hetero-complement | 0.962 | 0.927 | 3.917 | complementary heterogeneity forms a composite droplet |

## Main interpretation

The first encounter split is not simply same vs different.

```text
same-compatible -> merge
hetero-repulsive/toxic -> separate / avoid interface
hetero-complement -> composite droplet
```

So the relevant physical parameter is not identity itself, but compatibility of the interface.

## Important caveat

In this minimal encounter core, phase/momentum tests were mostly washed out by the strong surface-loss selection. Phase affected the neutral/weaker cases slightly, but in compatible/repulsive/complement regimes the loss/interfacial selection dominated.

This means the next phase-sensitive target should not be simple merging probability. It should be path choice in a 2D edge-memory terrain, where multiple routes remain available.

## Next

Move to:

```text
phase-routed encounter on edge-memory terrain
```

Record:

- merge probability
- separation index
- AB contact/interface length
- A/B cluster integrity
- COM trajectories
- classical probability ablation
- phase dependence in weak-selection and branched 2D terrains
