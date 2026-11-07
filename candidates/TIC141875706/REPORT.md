# TIC 141875706.01: Discovery and Vetting Report

## Candidate Summary
- **Host Star**: TIC 141875706 (2MASS, Gaia DR3)
- **Coordinates**: RA 208.352291 deg, Dec +56.092338 deg
- **Stellar Parameters**: Teff = 4274 K, R* = 0.695 R_sun, M* = 0.668 M_sun, Tmag = 11.45, Distance = 101.2 pc
- **Gaia DR3 Astrometry**: RUWE = 1.109 (astrometrically single star)
- **TESS Aperture Contamination**: contratio = 0.0735 (7.35%)
- **Data Coverage**: 6 Sectors (15, 16, 22, 23, 49, 76), 11 clean transits observed (2019-2024)

## Planetary Transit Parameters
- **Orbital Period (P)**: 10.694749 ± 0.000050 days
- **Transit Midpoint (Epoch T0)**: 2458713.720068 ± 0.0020 BJD_TDB (1713.720068 BTJD)
- **Transit Depth**: 1211.0 ± 101.0 ppm
- **Transit Duration**: 2.00 ± 0.10 hours
- **Planet Radius (Rp)**: 2.64 ± 0.15 R_earth (Warm Sub-Neptune)
- **Semi-major Axis (a)**: 0.083 AU
- **Equilibrium Temperature (Teq)**: ~595 K (assuming Bond albedo 0.3)
- **Insolation Flux**: 20.1 S_earth
- **Impact Parameter (b)**: ~0.77
- **Orbital Inclination (i)**: ~88.4 deg

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
- Next transit occurs on **2026-11-10 19:44:04 UTC** (Epoch 247).
