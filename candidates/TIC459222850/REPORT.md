# TIC 459222850.01: Discovery and Vetting Report

## Candidate Summary
- **Host Star**: TIC 459222850 (2MASS, Gaia DR3)
- **Coordinates**: RA 201.924882 deg, Dec +64.470534 deg
- **Stellar Parameters**: Teff = 3752 K, R* = 0.574 R_sun, M* = 0.566 M_sun, Tmag = 12.28, Distance = 98.8 pc
- **Gaia DR3 Astrometry**: RUWE = 1.077 (astrometrically single star)
- **TESS Aperture Contamination**: contratio = 0.0036 (0.36%)
- **Data Coverage**: 9 Sectors (14, 15, 21, 22, 41, 48, 49, 75, 76), 21 clean transits observed (2019-2024)

## Planetary Transit Parameters
- **Orbital Period (P)**: 9.810070 ± 0.000040 days
- **Transit Midpoint (Epoch T0)**: 2458684.939287 ± 0.0015 BJD_TDB (1684.939287 BTJD)
- **Transit Depth**: 1094.0 ± 111.0 ppm
- **Transit Duration**: 2.00 ± 0.10 hours
- **Planet Radius (Rp)**: 2.07 ± 0.10 R_earth (Super-Earth / Sub-Neptune)
- **Semi-major Axis (a)**: 0.076 AU
- **Equilibrium Temperature (Teq)**: ~465 K (assuming Bond albedo 0.3)
- **Insolation Flux**: 10.2 S_earth
- **Impact Parameter (b)**: ~0.38
- **Orbital Inclination (i)**: ~89.1 deg

## False-Positive Vetting Results
1. **Odd vs Even Consistency**: Odd and even transit depths are statistically indistinguishable, ruling out a twice-period eclipsing binary.
2. **Secondary Eclipse Non-Detection**: Deep phase search around phase 0.5 reveals zero significant dip, ruling out a self-luminous companion or grazing stellar binary.
3. **Orbit Gap / Dump Test**: Passed cleanly. Signal does not correlate with TESS orbit gaps or momentum dump epochs; recovers cleanly in gap-scrubbed photometry.
4. **Centroid Motion & Difference Imaging**: In-transit centroid shifts are negligible and on-target; no contamination from nearby stars explains the signal.
5. **Shifted-Sector Null Test**: Zero of multiple shifted-sector null runs achieve comparable SNR to the real transit signal.
6. **Stellar Activity / Rotation**: Lomb-Scargle periodograms show no rotational modulation or stellar harmonic power at the candidate orbital period.
7. **Catalog Cross-Match**: Star is completely uncatalogued on ExoFOP (0 TOIs, 0 cTOIs), NASA Exoplanet Archive, SIMBAD, and arXiv.

## Follow-up Observations & Ephemeris
Predicted transit times for the 2026-2028 observing seasons are compiled in `ephemeris.csv`.
- Next transit occurs on **2026-11-08 18:39:38 UTC** (Epoch 272).
