"""Light curve download, cleaning, box search and per-signal checks."""
import os, time
import numpy as np, requests
from astropy.io import fits
from astropy.timeseries import BoxLeastSquares
from wotan import flatten

ROOT = r"C:\Users\tfyuk\Jaadu\research\exoplanet"
LC = os.path.join(ROOT, "data", "lc")
TMP = os.path.join(ROOT, "data", "tmp")
RANK = {"SPOC": 0, "TESS-SPOC": 1, "QLP": 2}
DURS_H = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 6.0])
PMIN, PMAX = 0.5, 20.0


def fetch(uri, path):
    url = "https://mast.stsci.edu/api/v0.1/Download/file?uri=" + uri
    for attempt in range(4):
        try:
            # The public AWS mirror is faster for SPOC 2-minute files; MAST remains the fallback.
            if attempt == 0 and uri.startswith("mast:TESS/product/"):
                name = uri.rsplit("/", 1)[1]
                sec, tid = name.split("-")[1], name.split("-")[2]
                s3 = f"https://stpubdata.s3.amazonaws.com/tess/public/tid/{sec}/{tid[:4]}/{tid[4:8]}/{tid[8:12]}/{tid[12:]}/{name}"
                with requests.get(s3, stream=True, timeout=60) as r:
                    if r.status_code == 200:
                        with open(path, "wb") as fh:
                            for chunk in r.iter_content(1 << 16):
                                fh.write(chunk)
                        return True
            with requests.get(url, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(path, "wb") as fh:
                    for chunk in r.iter_content(1 << 16):
                        fh.write(chunk)
            return True
        except Exception:
            time.sleep(5 * (attempt + 1))
    return False


def binlc(t, cols, dt):
    idx = np.floor((t - t.min()) / dt).astype(int)
    u, inv, n = np.unique(idx, return_inverse=True, return_counts=True)
    out = [np.bincount(inv, t) / n]
    for c in cols:
        ok = np.isfinite(c)
        w = np.bincount(inv, ok.astype(float))
        with np.errstate(invalid="ignore", divide="ignore"):
            out.append(np.bincount(inv, np.where(ok, c, 0.0)) / w)
    return out


def read_sector(path, prov, sector):
    with fits.open(path, memmap=False) as h:
        d = h[1].data
        names = d.names
        if "PDCSAP_FLUX" in names:
            flux = np.array(d["PDCSAP_FLUX"], float)
        elif "KSPSAP_FLUX" in names:
            flux = np.array(d["KSPSAP_FLUX"], float)
        else:
            flux = np.array(d["DET_FLUX"], float)
        t = np.array(d["TIME"], float)
        q = np.array(d["QUALITY"], int)
        cx = np.array(d["MOM_CENTR1"] if "MOM_CENTR1" in names else d["SAP_X"], float)
        cy = np.array(d["MOM_CENTR2"] if "MOM_CENTR2" in names else d["SAP_Y"], float)
        bk = np.array(d["SAP_BKG"], float) if "SAP_BKG" in names else np.full(len(t), np.nan)
    ok = np.isfinite(t) & np.isfinite(flux) & (q == 0) & (flux > 0)
    if ok.sum() < 100:
        return None
    t, flux, cx, cy, bk = t[ok], flux[ok], cx[ok], cy[ok], bk[ok]
    flux = flux / np.nanmedian(flux)
    # 10-minute bins are the finest the cache keeps; 30-minute FFIs stay as they are.
    t, flux, cx, cy, bk = binlc(t, [flux, cx, cy, bk], 10.0 / 1440)
    flat, trend = flatten(t, flux, method="biweight", window_length=1.0, edge_cutoff=0.2,
                          break_tolerance=0.3, return_trend=True)
    good = np.isfinite(flat)
    t, flat, raw, cx, cy, bk = t[good], flat[good], flux[good], cx[good], cy[good], bk[good]
    if len(t) < 50:
        return None
    s = 1.4826 * np.median(np.abs(flat - np.median(flat)))
    keep = (flat < 1 + 3.5 * s) & (flat > 1 - 8 * s)
    return dict(t=t[keep], f=flat[keep], raw=raw[keep], cx=cx[keep] - np.nanmedian(cx), cy=cy[keep] - np.nanmedian(cy),
                bk=bk[keep], s=np.full(keep.sum(), sector), rms=np.full(keep.sum(), s))


def load_star(tic, rows):
    """rows: list of (sector, provenance, uri). Returns the cached arrays."""
    path = os.path.join(LC, f"{tic}.npz")
    if os.path.exists(path):
        return dict(np.load(path))
    best = {}
    for sector, prov, uri in rows:
        if sector not in best or RANK.get(prov, 9) < RANK.get(best[sector][0], 9):
            best[sector] = (prov, uri)
    parts, used, lost = [], [], []
    for sector in sorted(best):
        prov, uri = best[sector]
        tmp = os.path.join(TMP, f"{tic}_{sector}_{os.getpid()}.fits")
        if not fetch(uri, tmp):
            lost.append(int(sector))
            continue
        try:
            p = read_sector(tmp, prov, sector)
            if p is not None:
                parts.append(p)
                used.append(f"{sector}:{prov}")
        except Exception:
            lost.append(int(sector))
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
    if not parts:
        return None
    out = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}
    out["used"] = np.array(used)
    # A sector that failed to download or read must not vanish: keep the star uncached so it is retried.
    if lost:
        out["lost"] = np.array(lost)
        return out
    # Written whole then renamed, so a restart mid-write cannot leave a broken cache file.
    part = os.path.join(TMP, f"{tic}_{os.getpid()}.npz")
    np.savez_compressed(part, **out)
    os.replace(part, path)
    return out


def period_grid(baseline):
    """Spacing keeps a 1.5 h box in phase across the whole baseline; wider at long periods."""
    d0 = 0.06
    f, fmax, fs = 1.0 / PMAX, 1.0 / PMIN, []
    while f < fmax:
        fs.append(f)
        p = 1.0 / f
        f += d0 * (p / 3.0) ** (1.0 / 3.0) / (2.0 * p * baseline)
    return 1.0 / np.array(fs)[::-1]


def expected_dur_h(p, rad, mass):
    rad = rad if np.isfinite(rad) else 0.7
    mass = mass if np.isfinite(mass) else 0.7
    return 13.0 * (p / 365.25) ** (1 / 3.0) * (mass / rad ** 3) ** (-1 / 3.0)


def event_table(t, f, e, p, t0, dur):
    n = np.round((t - t0) / p).astype(int)
    intr = np.abs(t - t0 - n * p) < dur / 2
    ev = []
    for k in np.unique(n[intr]):
        m = intr & (n == k)
        if m.sum() * np.median(np.diff(t)) < 0.3 * dur and m.sum() < 2:
            continue
        w = 1 / e[m] ** 2
        ev.append((k, 1 - np.sum(f[m] * w) / w.sum(), 1 / np.sqrt(w.sum())))
    return np.array(ev) if ev else np.zeros((0, 3))


def local_shift(t, y, p, t0, dur):
    """In-transit minus neighbouring out-of-transit mean for a column, stacked over events."""
    n = np.round((t - t0) / p).astype(int)
    x = t - t0 - n * p
    vals = []
    for k in np.unique(n[np.abs(x) < dur / 2]):
        m = n == k
        a = m & (np.abs(x) < dur / 2) & np.isfinite(y)
        b = m & (np.abs(x) > dur) & (np.abs(x) < 3 * dur) & np.isfinite(y)
        if a.sum() >= 2 and b.sum() >= 4:
            vals.append(np.mean(y[a]) - np.mean(y[b]))
    if len(vals) < 3:
        return np.nan, np.nan, len(vals)
    vals = np.array(vals)
    err = 1.4826 * np.median(np.abs(vals - np.median(vals))) / np.sqrt(len(vals))
    return float(np.mean(vals)), float(np.mean(vals) / err) if err > 0 else np.nan, len(vals)


def robust_shift(t, y, p, t0, dur):
    """Like local_shift, but a median with a robust error, so one scattered-light event cannot decide the answer."""
    n = np.round((t - t0) / p).astype(int)
    x = t - t0 - n * p
    vals = []
    for k in np.unique(n[np.abs(x) < dur / 2]):
        m = n == k
        a = m & (np.abs(x) < dur / 2) & np.isfinite(y)
        b = m & (np.abs(x) > dur) & (np.abs(x) < 3 * dur) & np.isfinite(y)
        if a.sum() >= 2 and b.sum() >= 4:
            vals.append(np.mean(y[a]) - np.mean(y[b]))
    if len(vals) < 3:
        return np.nan
    vals = np.array(vals)
    med = np.median(vals)
    sd = 1.4826 * np.median(np.abs(vals - med))
    return float(med / (1.2533 * sd / np.sqrt(len(vals)))) if sd > 0 else np.nan


def search(lc, rad, mass, max_signals=3, snr_min=6.5):
    """Iterative box search on 30-minute bins. Returns one dict per signal."""
    t0_, f, s = lc["t"], lc["f"], lc["s"]
    order = np.argsort(t0_)
    t0_, f, s = t0_[order], f[order], s[order]
    tb, fb, sb = binlc(t0_, [f, s.astype(float)], 30.0 / 1440)
    ok = np.isfinite(fb)
    tb, fb, sb = tb[ok], fb[ok], np.round(sb[ok]).astype(int)
    eb = np.empty_like(fb)
    for sec in np.unique(sb):
        m = sb == sec
        eb[m] = max(1.4826 * np.median(np.abs(fb[m] - np.median(fb[m]))), 1e-6)
    if len(tb) < 300:
        return [], dict(n=len(tb))
    baseline = tb.max() - tb.min()
    periods = period_grid(max(baseline, 27.0))
    durs = DURS_H / 24.0
    out, mask = [], np.ones(len(tb), bool)
    info = dict(n=len(tb), baseline=float(baseline), nper=len(periods), sectors=int(len(np.unique(sb))),
                rms_ppm=float(np.median(eb) * 1e6))
    for i in range(max_signals):
        bls = BoxLeastSquares(tb[mask], fb[mask], eb[mask])
        r = bls.power(periods, durs, objective="snr", oversample=3)
        snr = np.nan_to_num(r.depth_snr)
        snr[r.depth <= 0] = 0
        k = int(np.argmax(snr))
        med = np.median(snr)
        sde = (snr[k] - med) / (1.4826 * np.median(np.abs(snr - med)) + 1e-9)
        p, t0, dur = float(r.period[k]), float(r.transit_time[k]), float(r.duration[k])
        if snr[k] < snr_min:
            break
        st = bls.compute_stats(p, dur, t0)
        ev = event_table(tb[mask], fb[mask], eb[mask], p, t0, dur)
        chi = (ev[:, 1] / ev[:, 2]) ** 2 * np.sign(ev[:, 1]) if len(ev) else np.array([0.0])
        pos = np.clip(chi, 0, None)
        sec_depths = {}
        nb = np.round((tb - t0) / p).astype(int)
        intr = np.abs(tb - t0 - nb * p) < dur / 2
        for sec in np.unique(sb):
            m = (sb == sec) & intr & mask
            if m.sum() >= 3:
                sec_depths[int(sec)] = [round(float(1 - np.mean(fb[m])) * 1e6, 1),
                                        round(float(eb[sb == sec][0] / np.sqrt(m.sum())) * 1e6, 1)]
        cx = local_shift(lc["t"], lc["cx"], p, t0, dur)
        cy = local_shift(lc["t"], lc["cy"], p, t0, dur)
        bk = local_shift(lc["t"], lc["bk"], p, t0, dur)
        out.append(dict(
            signal=i, period=p, t0=t0, dur_h=dur * 24, depth_ppm=float(r.depth[k] * 1e6), snr=float(snr[k]), sde=float(sde),
            n_events=int(len(ev)), max_event_frac=float(pos.max() / max(pos.sum(), 1e-9)),
            snr_wo_top=float(np.sqrt(max(pos.sum() - pos.max(), 0))),
            depth_odd=float(st["depth_odd"][0] * 1e6), err_odd=float(st["depth_odd"][1] * 1e6),
            depth_even=float(st["depth_even"][0] * 1e6), err_even=float(st["depth_even"][1] * 1e6),
            depth_sec=float(st["depth_half"][0] * 1e6), err_sec=float(st["depth_half"][1] * 1e6),
            depth_phased=float(st["depth_phased"][0] * 1e6), err_phased=float(st["depth_phased"][1] * 1e6),
            exp_dur_h=float(expected_dur_h(p, rad, mass)), cen_x_sig=cx[1], cen_y_sig=cy[1],
            cen_x=cx[0], cen_y=cy[0], bkg_sig=bk[1], sector_depths=sec_depths,
        ))
        m2 = np.abs(tb - t0 - np.round((tb - t0) / p) * p) > 0.75 * dur
        mask &= m2
    return out, info
