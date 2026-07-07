# Information Chemistry Core

Date: 2026-07-07

Purpose: test whether composite informational droplets can behave like simple reaction products: `A+B -> AB`, then `AB+C -> ?`.

## Core

Small 2D hard-core three-species model.

- Ordered species: A, B, C
- Hopping: EXCH-like local motion
- Pair compatibility: AB / AC / BC contact weights
- Dissipation: no-jump/postselective surface/contact loss
- Composite memory: AB-contact can write an AB-surface terrain that C may be attracted to or repelled by
- Classical ablation: probability transition with the same loss weights, no phase

This is not a final Lindblad simulator. It is a mechanism-finding core.

## Main result

A small information-chemistry split appeared:

```text
A+B stable, C rejected        -> AB molecule / C outside
A+B stable, C compatible      -> ABC composite droplet
A+B stable, C toxic           -> contact suppressed before AB breaks
A-B not stable, C binds both  -> C-bridged complex
AB surface memory + C         -> adsorption shell / guided contact, depending pair compatibility
```

## Scenario table

| scenario | Q P_AB | Q P_ABC_connected | Q C_attached | Q C-AB sep | Classical P_ABC | interpretation |
|---|---:|---:|---:|---:|---:|---|
| pairwise_reject_C | 0.982 | 0.001 | 0.002 | 3.520 | 0.012 | AB stays intact, C rejected |
| pairwise_absorb_C | 0.959 | 0.981 | 0.987 | 1.494 | 0.933 | ABC composite droplet |
| AB_surface_attracts_C with AC/BC repulsive | 0.976 | 0.033 | 0.037 | 2.883 | 0.152 | C occupies/feels AB surface terrain but does not fuse: adsorption shell |
| AB_surface_guides_C_neutral | 0.985 | 0.527 | 0.531 | 2.088 | 0.865 | AB surface can guide/contact C, but classical effect is stronger here |
| C_toxic_to_AB | 0.972 | 0.003 | 0.015 | 3.359 | 0.006 | contact is suppressed; toxicity acts as avoidance in this setting |
| C_bridge_catalyst | 0.011 | 0.980 | 0.997 | 0.715 | 0.941 | C bridges A and B while AB itself is not intact |

## Interpretation

The interesting jump is not merely bigger clusters. The core produced reaction classes:

```text
rejection
absorption
surface adsorption
surface-guided contact
contact toxicity / avoidance
bridging complex
```

This is the first minimal version of `information chemistry`.

## Important caveat

Most of these reaction classes are still heavily rule/compatibility driven and often survive classical ablation. Therefore they are not quantum evidence by themselves.

The remaining quantum target is not `does ABC form?` but:

```text
Does phase change which reaction channel wins when multiple channels remain open?
```

Strong selection washes out phase. To test phase properly, the next core needs weaker selection and branched 2D terrain where different paths/reaction channels compete.

## Next target

```text
phase-routed information chemistry
```

Minimal next experiment:

```text
A+B creates AB surface memory
C approaches with different phase signatures
The terrain allows at least two reaction channels:
  1. adsorption without fusion
  2. full ABC fusion
  3. bypass/rejection
Compare quantum phase routing vs classical probability routing
```
