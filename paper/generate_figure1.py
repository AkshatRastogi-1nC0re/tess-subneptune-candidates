import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PUB_DIR = r"C:\Users\tfyuk\Jaadu\research\exoplanet\publication"
PAPER_DIR = os.path.join(PUB_DIR, "paper")
os.makedirs(PAPER_DIR, exist_ok=True)

targets = [
    {
        "tic": "459222850",
        "label": "TIC 459222850.01 (Candidate Super-Earth)",
        "p": 9.810070,
        "t0": 1684.939287,
        "depth": 1094.0,
        "dur": 2.0,
        "rp": "2.07 +/- 0.10 R_earth",
        "host": "M dwarf (Teff 3752 K, d = 98.8 pc)",
        "sectors": "9 sectors (21 transits, SNR 9.85)",
        "ruwe": "1.077"
    },
    {
        "tic": "141875706",
        "label": "TIC 141875706.01 (Candidate Warm Sub-Neptune)",
        "p": 10.694749,
        "t0": 1713.720068,
        "depth": 1211.0,
        "dur": 2.0,
        "rp": "2.64 +/- 0.15 R_earth",
        "host": "K dwarf (Teff 4274 K, d = 101.2 pc)",
        "sectors": "6 sectors (11 transits, SNR 11.71)",
        "ruwe": "1.109"
    },
    {
        "tic": "219465243",
        "label": "TIC 219465243.01 (Candidate Super-Earth)",
        "p": 11.639913,
        "t0": 1690.488066,
        "depth": 778.5,
        "dur": 3.0,
        "rp": "1.95 +/- 0.12 R_earth",
        "host": "M dwarf (Teff 4005 K, d = 108.5 pc)",
        "sectors": "11 sectors (20 transits, SNR 9.79)",
        "ruwe": "1.197"
    }
]

fig, axes = plt.subplots(3, 1, figsize=(9.5, 11), sharex=False)
plt.subplots_adjust(hspace=0.38)

for idx, (ax, tgt) in enumerate(zip(axes, targets)):
    tic = tgt["tic"]
    lc_file = os.path.join(PUB_DIR, "candidates", f"TIC{tic}", "lightcurve.csv")
    df = pd.read_csv(lc_file)
    
    t = df["time_btjd"].values
    f = df["normalized_flux"].values
    
    # Calculate phase in hours from mid-transit
    phase = ((t - tgt["t0"]) % tgt["p"]) / tgt["p"]
    phase[phase > 0.5] -= 1.0
    phase_hours = phase * tgt["p"] * 24.0
    
    # Filter to transit window: [-8h, +8h]
    mask = np.abs(phase_hours) <= 8.0
    ph_w = phase_hours[mask]
    f_w = f[mask]
    
    # Plot individual cadences
    ax.scatter(ph_w, f_w, color="#94a3b8", alpha=0.35, s=12, label="TESS 2-min cadences", rasterized=True)
    
    # Phase binning (18 min bins = 0.30 hours)
    bins = np.arange(-8.0, 8.1, 0.30)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    binned_flux = []
    binned_err = []
    valid_centers = []
    for b_low, b_high, bc in zip(bins[:-1], bins[1:], bin_centers):
        b_mask = (ph_w >= b_low) & (ph_w < b_high)
        if np.sum(b_mask) >= 3:
            pts = f_w[b_mask]
            binned_flux.append(np.median(pts))
            binned_err.append(np.std(pts) / np.sqrt(len(pts)))
            valid_centers.append(bc)
    
    valid_centers = np.array(valid_centers)
    binned_flux = np.array(binned_flux)
    binned_err = np.array(binned_err)
    
    ax.errorbar(valid_centers, binned_flux, yerr=binned_err, fmt="o", color="#0f172a", 
                 ecolor="#1e293b", elinewidth=1.2, capsize=2.5, markersize=4.5, zorder=5, label="Phase binned (18 min)")
    
    # Simple trapezoidal / box transit model
    dur_h = tgt["dur"]
    depth_frac = tgt["depth"] / 1e6
    model_t = np.linspace(-8.0, 8.0, 1000)
    model_f = np.ones_like(model_t)
    ingress = 0.25 * dur_h
    flat_dur = dur_h - 2 * ingress
    for i, mt in enumerate(model_t):
        amt = abs(mt)
        if amt <= flat_dur / 2.0:
            model_f[i] = 1.0 - depth_frac
        elif amt < dur_h / 2.0:
            frac = (dur_h / 2.0 - amt) / ingress
            model_f[i] = 1.0 - depth_frac * frac
    
    ax.plot(model_t, model_f, color="#dc2626", lw=2.4, zorder=6, label="Fitted transit model")
    
    ax.set_xlim(-7.5, 7.5)
    ymin = 1.0 - (depth_frac * 2.5)
    ymax = 1.0 + (depth_frac * 1.8)
    ax.set_ylim(ymin, ymax)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.5, lw=0.9)
    ax.axhline(1.0, color="gray", linestyle=":", alpha=0.5, lw=0.9)
    
    ax.set_ylabel("Relative Flux", fontsize=11, fontweight="bold")
    if idx == 2:
        ax.set_xlabel("Time from Mid-Transit (hours)", fontsize=11, fontweight="bold")
    
    panel_letter = chr(ord("a") + idx)
    ax.set_title(f"({panel_letter}) {tgt['label']}", fontsize=12, fontweight="bold", loc="left", pad=7)
    
    info_text = (
        f"P = {tgt['p']:.4f} d | T0 = {tgt['t0']:.2f} BTJD\n"
        f"Depth = {tgt['depth']:.0f} ppm | Dur = {tgt['dur']:.1f} h\n"
        f"Rp = {tgt['rp']} | RUWE = {tgt['ruwe']}\n"
        f"{tgt['host']}"
    )
    ax.text(0.985, 0.05, info_text, transform=ax.transAxes, fontsize=9,
            verticalalignment="bottom", horizontalalignment="right",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f1f5f9", edgecolor="#cbd5e1", alpha=0.92))

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.96, 0.985), ncol=3, frameon=True, fontsize=9.5)

out_png = os.path.join(PAPER_DIR, "figure1.png")
out_pdf = os.path.join(PAPER_DIR, "figure1.pdf")
plt.savefig(out_png, dpi=300, bbox_inches="tight")
plt.savefig(out_pdf, bbox_inches="tight")
plt.close()
print("SUCCESS: Generated figure1.png and figure1.pdf")
