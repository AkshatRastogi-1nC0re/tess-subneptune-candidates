"""Scan the patch star by star, nearest first. Safe to restart: finished stars are skipped."""
import os, sys, json, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("NUMBA_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import multiprocessing as mp
import numpy as np, pandas as pd, requests

ROOT = r"C:\Users\tfyuk\Jaadu\research\exoplanet"
OUT = os.path.join(ROOT, "results", "scan.jsonl")
DONE = os.path.join(ROOT, "results", "scan.finished")
BLOCKED = os.path.join(ROOT, "results", "scan.blocked")
MILESTONE = os.path.join(ROOT, "results", "scan.milestone")
MIN_STARS = 2000  # The patch has 2,173; far fewer means the target list or index is broken.
MAX_BAD = 0.05  # Above this share without a clean result (say a network outage), do not call it finished.


def work(a):
    import scanlib
    tic, rows, rad, mass = a
    t0 = time.time()
    try:
        lc = scanlib.load_star(tic, rows)
        if lc is None:
            return dict(tic=tic, status="nodata", secs=time.time() - t0)
        sig, info = scanlib.search(lc, rad, mass)
        res = dict(tic=tic, status="ok", info=info, signals=sig, used=[str(u) for u in lc["used"]], secs=time.time() - t0)
        if "lost" in lc:
            # Reviewed like any other result, but not counted as clean, so it is retried on the next start.
            res.update(status="partial", lost=[int(x) for x in lc["lost"]])
        return res
    except Exception as e:
        return dict(tic=tic, status="fail", why=repr(e)[:300], secs=time.time() - t0)


def wake(title, text):
    u, tok = os.environ.get("DIGIKARMI_INBOX_URL"), os.environ.get("DIGIKARMI_INBOX_TOKEN")
    if u and tok:
        try:
            requests.post(u + "/events", json=dict(kind="exoplanet-scan", title=title, text=text),
                          headers={"Authorization": "Bearer " + tok}, timeout=30)
        except Exception as e:
            print("wake failed", e, flush=True)


def fail(why):
    """Stop without claiming a finish. The owner side hears once per distinct reason, not on every restart."""
    print("SCAN BLOCKED:", why, flush=True)
    old = open(BLOCKED, encoding="utf-8").read() if os.path.exists(BLOCKED) else None
    if old != why:
        open(BLOCKED, "w", encoding="utf-8").write(why)
        wake("Exoplanet scan blocked", why)
    sys.exit(2)


def last_milestone():
    try:
        return int(open(MILESTONE).read())
    except (OSError, ValueError):
        return 0


def read_ok():
    """Stars with a clean result. nodata and fail rows are retried on the next start."""
    ok = set()
    if os.path.exists(OUT):
        for line in open(OUT, encoding="utf-8"):
            try:
                r = json.loads(line)
                if r["status"] == "ok":
                    ok.add(r["tic"])
            except Exception:
                pass
    return ok


def main():
    # Below-normal priority (children inherit it) so the PC stays usable during the scan.
    import ctypes
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000)
    from scanlib import LC, TMP
    os.makedirs(LC, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    try:
        tic = pd.read_csv(os.path.join(ROOT, "data", "patch_tic.csv")).sort_values("d")
        tic["ID"] = tic.ID.astype(str)
        idx = pd.read_csv(os.path.join(ROOT, "data", "lc_index.csv"))
        # Light curves only: the index also holds SPOC _dvt report files, which share sector numbers and hid real sectors.
        idx = idx[idx.dataURL.astype(str).str.endswith(("_lc.fits", "_llc.fits"))]
        groups = {str(k): g for k, g in idx.groupby(idx.target_name.astype(str))}
    except Exception as e:
        fail(f"could not read the target list or index: {e!r}"[:300])
    if len(tic) < MIN_STARS:
        fail(f"target list has only {len(tic)} stars, expected at least {MIN_STARS}")
    targets = tic[tic.ID.isin(groups)]
    total = len(targets)
    if total < MIN_STARS:
        fail(f"only {total} of {len(tic)} target stars are in the light curve index")
    ok = read_ok()
    n = int(targets.ID.isin(ok).sum())
    if os.path.exists(DONE):
        if total - n <= MAX_BAD * total:
            while True:
                time.sleep(3600)
        print("finished marker is wrong:", n, "of", total, "clean; setting it aside", flush=True)
        os.replace(DONE, DONE + ".invalid")
    if os.path.exists(BLOCKED):
        os.remove(BLOCKED)
    jobs = []
    for _, s in targets[~targets.ID.isin(ok)].iterrows():
        g = groups[s.ID]
        rows = [(int(a), str(b), str(c)) for a, b, c in zip(g.sequence_number, g.provenance_name, g.dataURL)]
        jobs.append((s.ID, rows, float(s.rad), float(s.mass)))
    print("to do", len(jobs), "of", total, flush=True)
    hits, t0 = 0, time.time()
    with mp.Pool(3) as pool, open(OUT, "a", encoding="utf-8") as fh:
        for r in pool.imap_unordered(work, jobs):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            n += 1
            hits += sum(1 for x in r.get("signals", []) if x["snr"] >= 7.1)
            if n % 25 == 0:
                print(n, "/", total, "signals", hits, "elapsed min", round((time.time() - t0) / 60), flush=True)
            # Requeued stars can bring the count back past a milestone; each one wakes the review only once.
            if n % 300 == 0 and n > last_milestone():
                open(MILESTONE, "w").write(str(n))
                wake("Exoplanet scan progress", f"{n} of {total} stars scanned. Run the candidate review on results/scan.jsonl.")
    good = int(targets.ID.isin(read_ok()).sum())
    if total - good > MAX_BAD * total:
        fail(f"only {good} of {total} stars have a clean result; retrying the rest")
    open(DONE, "w").write(time.ctime())
    wake("Exoplanet scan finished", f"{good} of {total} stars scanned cleanly, {total - good} without usable data. Run the full candidate review on results/scan.jsonl.")
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
