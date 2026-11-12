import os, re, subprocess

d = r"C:\Users\tfyuk\Jaadu\research\exoplanet\publication\paper"
with open(os.path.join(d, "rnaas_exoplanets.tex"), "r", encoding="utf-8") as f:
    raw = f.read()

def clean(s):
    rep = [
        (r"\rearth", "<i>R</i><sub>&oplus;</sub>"), (r"\rsun", "<i>R</i><sub>&odot;</sub>"),
        (r"\msun", "<i>M</i><sub>&odot;</sub>"), (r"\pm", "&plusmn;"),
        (r"\le", "&le;"), (r"\ge", "&ge;"), (r"\lesssim", "&lesssim;"),
        (r"\approx", "&approx;"), (r"\sigma", "&sigma;"), (r"\alpha", "&alpha;"),
        (r"\delta", "&delta;"), (r"\text{--}", "&ndash;"), ("~", " "),
        (r"\mathrm{RUWE}", "RUWE"), (r"\mathrm{SNR}", "SNR"), (r"\mathrm{BJD_{TDB}}", "BJD<sub>TDB</sub>")
    ]
    for a, b in rep: s = s.replace(a, b)
    s = re.sub(r"\\textbf\{([^}]+)\}", r"<b>\1</b>", s)
    s = re.sub(r"\\textit\{([^}]+)\}", r"<i>\1</i>", s)
    s = re.sub(r"\\texttt\{([^}]+)\}", r"<code>\1</code>", s)
    s = re.sub(r"\\url\{([^}]+)\}", r"<a href='\1'>\1</a>", s)
    s = re.sub(r"\\citep\[[^\]]*\]\{([^}]+)\}", r"(\1)", s)
    s = re.sub(r"\\cite\{([^}]+)\}", r"\1", s)
    s = re.sub(r"\$([^$]+)\$", r"<i>\1</i>", s)
    return s

title = clean(re.search(r"\\title\{([^}]+)\}", raw).group(1))
abs_t = clean(re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", raw, re.S).group(1).strip())
kw = re.search(r"\\keywords\{([^}]+)\}", raw).group(1).replace(" --- ", "; ")

body_raw = re.search(r"\\end\{abstract\}(.*?)\\begin\{acknowledgments\}", raw, re.S).group(1)
body_clean = clean(body_raw)
body_clean = re.sub(r"\\begin\{figure\*\}.*?\\end\{figure\*\}", "", body_clean, flags=re.S)
body_clean = re.sub(r"\\section\{([^}]+)\}", r"<h2>\1</h2>", body_clean)
body_clean = re.sub(r"\\begin\{enumerate\}", "<ol>", body_clean)
body_clean = re.sub(r"\\end\{enumerate\}", "</ol>", body_clean)
body_clean = re.sub(r"\\item\s+", "<li>", body_clean)
body_clean = "\n".join(["<p>" + p.strip() + "</p>" if not p.strip().startswith("<h") and not p.strip().startswith("<ol") and not p.strip().startswith("<li") and not p.strip().startswith("</ol") else p.strip() for p in body_clean.split("\n\n") if p.strip()])

css = "@page{size:letter;margin:14mm 15mm}body{font-family:'Times New Roman',serif;font-size:9.5pt;line-height:1.32;color:#111;margin:0}.hdr{border-bottom:2px solid #222;padding-bottom:3px;margin-bottom:12px;display:flex;justify-content:space-between;font-size:7.8pt;text-transform:uppercase;color:#444}.hdr b{color:#111}h1{font-size:14.5pt;font-weight:bold;text-align:center;margin:8px 0 6px 0;line-height:1.24}.auth{text-align:center;font-size:10.5pt;font-weight:bold}.affil{text-align:center;font-size:8.5pt;font-style:italic;color:#444;margin-bottom:2px}.cntct{text-align:center;font-size:8pt;color:#555;margin-bottom:12px}.abs{margin:0 10px 10px 10px;padding:7px 12px;background:#fafafa;border-top:1px solid #ccc;border-bottom:1px solid #ccc;font-size:8.8pt;text-align:justify;line-height:1.3}.abs b{text-transform:uppercase;font-size:8pt;letter-spacing:0.8px;margin-right:6px}.uat{margin:4px 10px 12px 10px;font-size:8pt;font-style:italic;color:#333}.cols{column-count:2;column-gap:16px;text-align:justify}p{margin:0 0 6px 0;text-indent:12px}h2{font-size:9pt;font-weight:bold;text-transform:uppercase;letter-spacing:0.5px;margin:8px 0 3px 0;border-bottom:0.5px solid #bbb;padding-bottom:1px;break-after:avoid}.figbox{column-span:all;margin:8px 0 10px 0;text-align:center;page-break-inside:avoid}.figbox img{width:95%;max-height:480px}.cap{font-size:8pt;line-height:1.24;text-align:justify;margin:4px 10px 0 10px;color:#222}.cap b{font-weight:bold}ol{margin:3px 0 6px 0;padding-left:14px;font-size:8.8pt}li{margin-bottom:2px}.refs{font-size:7.5pt;line-height:1.2}.refs p{margin:0 0 2px 0;text-indent:-12px;padding-left:12px}.ack{font-size:7.8pt;font-style:italic;color:#444;margin:6px 0}"

fig_html = "<div class='figbox'><img src='figure1.png' alt='Figure 1'><div class='cap'><b>Figure 1.</b> Phase-folded TESS 2-minute cadence light curves for the three newly discovered transiting exoplanet candidates: (a) TIC 459222850.01 (<i>P</i> = 9.810 d, <i>R<sub>p</sub></i> = 2.07 <i>R</i><sub>&oplus;</sub>), (b) TIC 141875706.01 (<i>P</i> = 10.695 d, <i>R<sub>p</sub></i> = 2.64 <i>R</i><sub>&oplus;</sub>), and (c) TIC 219465243.01 (<i>P</i> = 11.640 d, <i>R<sub>p</sub></i> = 1.95 <i>R</i><sub>&oplus;</sub>). Grey dots show individual cadences; black markers with error bars depict 18-minute binned flux; solid red curves represent the best-fit transit model. Insets summarize parameters.</div></div>"

refs_html = "<h2>References</h2><div class='refs'><p>Akeson, R. L., et al. 2013, PASP, 125, 989</p><p>Astropy Collaboration, et al. 2022, ApJ, 935, 167</p><p>Gaia Collaboration, et al. 2023, A&amp;A, 674, A1</p><p>Kov&aacute;cs, G., et al. 2002, A&amp;A, 391, 369</p><p>Lightkurve Collaboration, et al. 2018, ascl:1812.013</p><p>Ricker, G. R., et al. 2015, JATIS, 1, 014003</p><p>Stassun, K. G., et al. 2019, AJ, 158, 138</p></div>"

html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body><div class='hdr'><span><b>Research Notes of the AAS</b> | Rapid Communications</span><span>Author Manuscript</span><span>DOI: 10.3847/2515-5172/rnaas.2026.001</span></div><h1>{title}</h1><div class='auth'>Akshat Rastogi</div><div class='cntct'>Correspondence: akshat28vivek@gmail.com &bull; Repository: https://github.com/AkshatRastogi-1nC0re/tess-subneptune-candidates</div><div class='abs'><b>Abstract</b>{abs_t}</div><div class='uat'><b>Unified Astronomy Thesaurus concepts:</b> {kw}</div><div class='cols'>{body_clean}{fig_html}{refs_html}</div></body></html>"

h_path = os.path.join(d, "rnaas_exoplanets.html")
with open(h_path, "w", encoding="utf-8") as f: f.write(html)

p_path = os.path.join(d, "rnaas_exoplanets.pdf")
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
subprocess.run([edge, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={p_path}", f"file:///{h_path.replace(os.sep, '/')}"], capture_output=True)

if os.path.exists(p_path):
    print("SUCCESS: PDF generated, size:", os.path.getsize(p_path))
else:
    print("Failed")
