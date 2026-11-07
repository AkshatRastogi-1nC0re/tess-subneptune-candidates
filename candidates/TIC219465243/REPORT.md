# TIC 219465243.01: Discovery and Vetting Report

## Candidate Summary
- **Host Star**: TIC 219465243 (2MASS, Gaia DR3)
- **Coordinates**: RA 209.268477 deg, Dec +73.269317 deg
- **Stellar Parameters**: Teff = 4005 K, R* = 0.635 R_sun, M* = 0.626 M_sun, Tmag = 12.16, Distance = 108.5 pc
- **Gaia DR3 Astrometry**: RUWE = 1.197 (astrometrically single star)
- **TESS Aperture Contamination**: contratio = 0.0137 (1.37%)
- **Data Coverage**: 11 Sectors (14, 15, 20, 22, 40, 47, 48, 60, 74, 75, 76), 20 clean transits observed (2019-2024)

## Planetary Transit Parameters
- **Orbital Period (P)**: 11.639913 ± 0.000040 days
- **Transit Midpoint (Epoch T0)**: 2458690.488066 ± 0.0018 BJD_TDB (1690.488066 BTJD)
- **Transit Depth**: 778.5 ± 85.0 ppm
- **Transit Duration**: 3.00 ± 0.10 hours
- **Planet Radius (Rp)**: 1.95 ± 0.12 R_earth (Super-Earth / Sub-Neptune)
- **Semi-major Axis (a)**: 0.086 AU
- **Equilibrium Temperature (Teq)**: ~525 K (assuming Bond albedo 0.3)
- **Insolation Flux**: 13.5 S_earth
- **Impact Parameter (b)**: ~0.25
- **Orbital Inclination (i)**: ~89.3 deg

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
- Next transit occurs on **2026-11-11 12:39:22 UTC** (Epoch 229).
