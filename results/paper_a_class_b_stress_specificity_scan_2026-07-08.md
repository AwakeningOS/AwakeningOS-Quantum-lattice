# Paper A Class B Stress-Specificity Scan

Date: 2026-07-08

Purpose: close the Paper A Section 4.3 audit hole. The question is whether the stress-specific CHSH positives follow from the implemented phase/state map, or whether the paper must downgrade the claim.

## Source definitions

The CHSH-readout probe defines the two-qubit state as `rho_cb(phi, gamma)`, applies a controlled Rz(phi), then applies global computational dephasing with off-diagonal scale `1-gamma`.

The simulator uses:

```text
phi = pi * (1 - integrity)
```

Thus stress lowering integrity drives phi toward pi.

## Closed form at gamma = 0

For gamma = 0, the implemented pure state has concurrence

```text
C(phi) = |sin(phi/2)|
```

and therefore

```text
Negativity(phi, 0) = 0.5 * |sin(phi/2)|
S_CHSH(phi, 0) = 2 * sqrt(1 + sin(phi/2)^2)
```

This gives:

```text
phi = 0  -> S = 2,       N = 0
phi = pi -> S = 2sqrt(2), N = 0.5
```

## Gamma scan result

For the implemented dephasing map, the CHSH value follows the numeric closed form:

```text
S_CHSH(phi, gamma) = 2 * (1 - gamma) * sqrt(1 + sin(phi/2)^2)
```

Therefore the global maximum over phi in [0, pi] and gamma in [0, 1] is at:

```text
phi = pi
gamma = 0
S_CHSH = 2.828427124746
Negativity = 0.5
```

## Grid check

Coarse scan: phi grid 401 points, gamma grid 201 points.

```text
max S_CHSH = 2.828427124746 at phi/pi = 1.0, gamma = 0.0
max Negativity = 0.5 at phi/pi = 1.0, gamma = 0.0
```

Reference table, entries are `(S_CHSH, Negativity)`:

```text
gamma=0.00: phi=0 (2.000000,0.000000), pi/4 (2.141445,0.191342), pi/2 (2.449490,0.353553), 3pi/4 (2.722905,0.461940), pi (2.828427,0.500000)
gamma=0.25: phi=0 (1.500000,0.000000), pi/4 (1.606084,0.081006), pi/2 (1.837117,0.202665), 3pi/4 (2.042179,0.283955), pi (2.121320,0.312500)
gamma=0.50: phi=0 (1.000000,0.000000), pi/4 (1.070722,0.000000), pi/2 (1.224745,0.051777), 3pi/4 (1.361453,0.105970), pi (1.414214,0.125000)
gamma=0.75: phi=0 (0.500000,0.000000), pi/4 (0.535361,0.000000), pi/2 (0.612372,0.000000), 3pi/4 (0.680726,0.000000), pi (0.707107,0.000000)
gamma=1.00: all listed phi values (0.000000,0.000000)
```

## Auditor-facing conclusion

The strong Section 4.3 statement is allowed, but only as a statement about the implemented sandbox map:

```text
Stress specificity is induced by the implemented phase schedule phi=pi*(1-integrity). Under the implemented rho_cb(phi,gamma) map, S_CHSH is maximized at phi=pi and gamma=0, with S=2sqrt(2) and negativity=0.5. Therefore stress-specific CHSH positives are a consequence of the phase schedule plus witness routing, not an independent discovery about ordinary transport.
```

Do not generalize this beyond the implemented state map.
