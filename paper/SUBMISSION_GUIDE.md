# RNAAS Manuscript Submission Guide for Akshat Rastogi

## Target Venue: Research Notes of the American Astronomical Society (RNAAS)
- **Publisher**: American Astronomical Society (AAS) / IOP Publishing
- **Format**: Research Note (Rapid communication, <= 1,500 words, single composite display item)
- **Turnaround Time**: Typically moderated and published within 72 hours (3 business days)
- **Indexing**: Fully citable, assigned a permanent DOI, indexed in NASA Astrophysics Data System (ADS) and Web of Science
- **Significance for ExoFOP**: Explicitly fulfills IPAC/ExoFOP's requirement for peer-reviewed / moderated publication to unlock **candidate submitter privileges** for username `rastogi`.

---

## Manuscript Details
- **Title**: *Three New Transiting Sub-Neptune and Super-Earth Candidates Orbiting Nearby K and M Dwarfs in TESS Photometry*
- **Author**: Akshat Rastogi
- **Affiliation**: None (Independent Researcher / No affiliation)
- **Email**: akshat28vivek@gmail.com
- **Repository**: https://github.com/AkshatRastogi-1nC0re/tess-subneptune-candidates
- **Candidates Reported**:
  1. **TIC 459222850.01**: P = 9.81007 d, Rp = 2.07 +/- 0.10 R_earth (Super-Earth / Sub-Neptune), M dwarf at 98.8 pc
  2. **TIC 141875706.01**: P = 10.69475 d, Rp = 2.64 +/- 0.15 R_earth (Warm Sub-Neptune), K dwarf in binary at 101.2 pc
  3. **TIC 219465243.01**: P = 11.63991 d, Rp = 1.95 +/- 0.12 R_earth (Super-Earth), M dwarf at 108.5 pc

---

## Package Files Location
All files are prepared in: `C:\Users\tfyuk\Jaadu\research\exoplanet\publication\paper\`
1. **`rnaas_submission_package.zip`**: Complete submission bundle containing:
   - `rnaas_exoplanets.tex`: LaTeX source using `aastex631`
   - `figure1.pdf` and `figure1.png`: 300 DPI composite 3-panel publication figure
   - `references.bib`: Full BibTeX bibliography
   - `rnaas_exoplanets.pdf`: Pre-compiled publication draft
2. **`rnaas_exoplanets.pdf`**: Direct PDF view of the paper.

---

## Step-by-Step Submission Instructions

### Step 1: Open the AAS Submission Portal
1. Navigate to: **https://aas.msubmit.net**
2. Log in using your ORCID ID or AAS credentials (create an account if first time).

### Step 2: Start New Submission
1. Click **Submit a Manuscript**.
2. Select Journal: **Research Notes of the AAS (RNAAS)**.
3. Select Manuscript Type: **Research Note**.

### Step 3: Upload Files
1. Upload `rnaas_exoplanets.tex` as **Manuscript File**.
2. Upload `figure1.pdf` (or `figure1.png`) as **Figure 1**.
3. Upload `references.bib` as **Bibliography File**.
*(Alternatively, upload `rnaas_submission_package.zip` if prompted for archive upload).*

### Step 4: Metadata & Author Information
- **Title**: Three New Transiting Sub-Neptune and Super-Earth Candidates Orbiting Nearby K and M Dwarfs in TESS Photometry
- **Abstract**: (Copy from `rnaas_exoplanets.tex` or `rnaas_exoplanets.html`)
- **Keywords**: Exoplanet astronomy (486); Planetary system candidates (1258); Transit photometry (1709); Super Earths (1655); M dwarf stars (982); K dwarf stars (882)
- **Author**: Akshat Rastogi (Independent / No affiliation)

### Step 5: Review PDF & Final Submission
1. Build the system PDF preview, confirm formatting of Figure 1 and references.
2. Click **Submit Manuscript**.

---

## Post-Acceptance Next Step for ExoFOP
As soon as the RNAAS DOI or acceptance notice arrives (~72 hours):
1. Reply to Melanie A. Swain / IPAC Helpdesk (exofopsd@caltech.edu / Ticket ESD-3985):
   > "Hi Melanie, our Research Note reporting the discovery and vetting of the three TESS candidates (TIC 459222850, TIC 141875706, TIC 219465243) has been accepted/published in RNAAS (DOI: [insert DOI]). The supporting light curves and vetting summaries are already uploaded under tag 20261112_rastogi_exoplanet-candidates_001. Please enable candidate submitter privileges for username 'rastogi' so we can finalize the cTOI table entries."
2. ExoFOP activates candidate submitter approval.
3. Jaadu automatically pushes the cTOI table parameters via `params_planet_20261107_001.txt`.
