# Three New Transiting Sub-Neptune / Super-Earth Exoplanet Candidates from a 2,173-Star TESS Survey

**Principal Investigator / Discoverer**: Akshat Rastogi  
**Affiliation**: DigiKarmi AI Research / Independent Exoplanet Research  
**Survey Baseline**: NASA TESS Photometry (Sectors 14–76, spanning 2019–2024)  
**Survey Footprint**: 2,173 nearby K and M dwarfs in Ursa Major and Draco (RA 150°–240°, Dec +50°–+75°)  

---

## Executive Summary

We report the independent detection and multi-diagnostic vetting of **three new transiting exoplanet candidates** (all Sub-Neptunes and Super-Earths) discovered in public NASA Transiting Exoplanet Survey Satellite (TESS) photometry. 

These candidates were discovered through a systematic automated survey of **2,173 nearby K/M dwarf stars** in Ursa Major and Draco. All 2,173 stars were processed through our detection and validation pipeline. 

### Summary of New Exoplanet Candidates

| Candidate | Host Star | Sp. Type | Dist (pc) | Tmag | Period (d) | Epoch (BJD_TDB) | Depth (ppm) | Radius (R⊕) | Teq (K) | Sectors | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TIC 459222850.01** | TIC 459222850 | Early M | 98.8 | 12.28 | **9.810070** | 2458684.9393 | 1,094 | **2.07 ± 0.10** | 465 | 9 | **Viable New Candidate** |
| **TIC 141875706.01** | TIC 141875706 | K dwarf | 101.2 | 11.45 | **10.694749** | 2458713.7201 | 1,211* | **2.64 ± 0.15** | 595 | 6 | **Viable New Candidate** |
| **TIC 219465243.01** | TIC 219465243 | Early M | 108.5 | 12.16 | **11.639913** | 2458690.4881 | 778.5 | **1.95 ± 0.12** | 525 | 11 | **Viable New Candidate** |

*\* TIC 141875706 transit depth is dilution-corrected for a physical co-moving M companion at 12.6 arcsec separation (7.2% flux).*

None of these three candidates are registered on ExoFOP (0 TOIs, 0 cTOIs), the NASA Exoplanet Archive, SIMBAD, or published in the literature. None had SPOC Data Validation alerts.

---

## Survey Methodology & Pipeline Verification

1. **Target Selection**:
   - 2,173 K and M dwarf stars within ~115 pc in Ursa Major and Draco (RA 150°–240°, Dec +50°–+75°).
   - Scanned in order of proximity, covering TESS Sectors 14 through 76 (2-minute SPOC and 10/30-minute FFI cadence).
2. **Transit Search**:
   - Box Least Squares (BLS) periodogram search over periods from 0.5 to 20.0 days.
   - Outlier rejection, robust running-median filtering, and sector-by-sector noise normalization.
3. **Recovery / Honesty Check**:
   - 46 known exoplanets and cTOIs exist in the target sample within the 0.5–20 day search range.
   - The pipeline cleanly recovered **41 of 46 known systems (89.1% recovery rate)** at their exact known orbital periods (e.g. TOI-1266 b/c, TOI-1179.01, CTOI 355828331.01).
   - The unrecovered systems are known non-transiting radial-velocity planets (such as HD 238090 b) or shallow signals lacking TESS transit SNR.
4. **False Positive Vetting Suite**:
   - **Odd / Even Transit Consistency**: Tested across all epochs; rules out eclipsing binaries with twice the true orbital period.
   - **Secondary Eclipse Phase Scan**: Deep search at phase 0.5 and throughout the orbit; rules out occultations of self-luminous stars or grazing eclipsing binaries.
   - **Orbit Gap & Momentum Dump Test**: Signals with transits hugging TESS data gaps or orbital edges are isolated and rejected. Blind searches on gap-scrubbed data must independently recover the candidate.
   - **Astrometric Centroid Motion Check**: In-transit versus out-of-transit difference images confirm the dip originates on the target star and not a background eclipsing binary.
   - **Shifted-Sector Null Tests**: 10–20 randomized sector shifts confirm that background red noise does not create spurious detections.
   - **Stellar Rotation & Lomb-Scargle Periodograms**: Raw unflattened light curves are analyzed to ensure transit signals are not harmonics of starspot rotation.
   - **Gaia DR3 Astrometric RUWE**: All three hosts have RUWE < 1.20, indicating clean single-star astrometric solutions.

---

## Upcoming Transit Ephemeris & Observing Windows (2026–2028)

Detailed predictions with 1σ timing uncertainties are provided in `ephemeris.csv` within each candidate's directory. Immediate upcoming opportunities:

- **TIC 459222850.01**: Epoch 272 — **2026-11-08 18:39 UTC** (Duration: 2.0 h, Depth: 1.09 ppt)
- **TIC 141875706.01**: Epoch 247 — **2026-11-10 19:44 UTC** (Duration: 2.0 h, Depth: 1.21 ppt)
- **TIC 219465243.01**: Epoch 229 — **2026-11-11 12:39 UTC** (Duration: 3.0 h, Depth: 0.78 ppt)

Observers are encouraged to perform high-resolution imaging (speckle / AO) and ground-based transit follow-up observations to confirm and refine parameters.

---

## License & Citation

Data from the NASA Transiting Exoplanet Survey Satellite (TESS) was accessed via MAST.  
If utilizing these candidates or software in academic work, please cite:  
*Akshat Rastogi (2026), "Three New Transiting Exoplanet Candidates from TESS Photometry in Ursa Major and Draco", GitHub repository.*
