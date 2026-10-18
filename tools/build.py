# -*- coding: utf-8 -*-
"""Build the profile README visuals.

One spec, two themes. Every visual is written to assets/<name>.svg (light) and
assets/dark/<name>.svg, so the README can serve them through <picture> and
prefers-color-scheme without depending on any third-party widget service.

Run:  python tools/build.py
"""

from __future__ import annotations

import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 846  # GitHub's README column on desktop

# Backgrounds stay transparent so the visuals sit on whatever GitHub theme the
# reader uses, including the dimmed one. Only ink colours differ per theme.
THEMES = {
    "light": dict(ink="#1f2328", muted="#59636e", line="#d1d9e0",
                  accent="#8a5a00", wash="#f6f8fa", band="#eaeef2"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", line="#3d444d",
                 accent="#d9a441", wash="#161b22", band="#21262d"),
}

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


# ---------------------------------------------------------------- primitives

def svg(height: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
        f'viewBox="0 0 {W} {height}" role="img">\n{body}</svg>\n'
    )


def text(x, y, s, *, size=28, fill="ink", font=SANS, weight=400,
         anchor="start", spacing=0, opacity=None, t=None) -> str:
    attrs = [
        f'x="{x}"', f'y="{y}"', f'font-family="{font}"', f'font-size="{size}"',
        f'font-weight="{weight}"', f'fill="{t[fill] if fill in t else fill}"',
    ]
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    return f'  <text {" ".join(attrs)}>{escape(s)}</text>\n'


def rule(x1, y, x2, t, *, stroke="line", width=1, dash=None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
            f'stroke="{t[stroke]}" stroke-width="{width}"{d}/>\n')


def vrule(x, y1, y2, t, *, stroke="line", width=1, dash=None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" '
            f'stroke="{t[stroke]}" stroke-width="{width}"{d}/>\n')


def rect(x, y, w, h, t, *, fill=None, stroke="line", rx=6, width=1) -> str:
    f = t[fill] if fill else "none"
    s = t[stroke] if stroke else "none"
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{f}" stroke="{s}" stroke-width="{width}"/>\n')


def arrow(x1, y, x2, t, *, stroke="muted") -> str:
    """Horizontal arrow drawn as a line plus an explicit head.

    Deliberately avoids <marker>: markers are dropped by some SVG rasterisers,
    and a README visual has to survive whatever renders it.
    """
    head = f'M{x2} {y} L{x2 - 9} {y - 5} L{x2 - 9} {y + 5} Z'
    return (f'  <line x1="{x1}" y1="{y}" x2="{x2 - 7}" y2="{y}" stroke="{t[stroke]}" '
            f'stroke-width="1.5"/>\n  <path d="{head}" fill="{t[stroke]}"/>\n')


# ------------------------------------------------------------------ visuals

def header(t) -> str:
    # Widths are eyeballed for the generic sans stack, then given slack: the
    # reader's font is not ours, so nothing sits closer than ~24px to its
    # neighbour.
    b = ""
    b += text(0, 78, "ILHAM", size=80, weight=700, spacing=-1, t=t)
    b += text(276, 78, "BINTANG", size=80, weight=200, spacing=-1, fill="muted", t=t)
    b += text(0, 150, "SATRIA", size=80, weight=700, spacing=-1, t=t)
    b += rule(0, 182, W, t)
    b += text(0, 218, "Sains Data Terapan · PENS Surabaya", size=25, fill="muted", t=t)
    b += text(W, 218, "@YonoBengkel", size=25, fill="accent", font=MONO, anchor="end", t=t)
    return svg(238, b)


def band(num, label, t) -> str:
    b = rect(0, 0, W, 56, t, fill="band", stroke=None, rx=4)
    b += text(22, 37, num, size=24, weight=700, fill="accent", font=MONO, t=t)
    b += text(76, 37, "—", size=24, fill="muted", font=MONO, t=t)
    b += text(112, 37, label, size=24, weight=500, font=MONO, spacing=1, t=t)
    return svg(56, b)


WHOAMI = [
    ("Mahasiswa Sains Data Terapan, Politeknik Elektronika Negeri Surabaya.", "ink"),
    ("Magang sebagai AI Engineer di Ideola sejak Juli 2026.", "ink"),
    ("", None),
    ("Saya lebih tertarik pada kenapa sebuah metode bekerja daripada", "ink"),
    ("pada tool yang memakainya. Yang saya kejar: tahu asumsi apa yang", "ink"),
    ("sedang dipinjam, dan kapan asumsi itu patah.", "ink"),
    ("", None),
    ("Dua bagian berikutnya bukan daftar kemampuan. Keduanya satu", "muted"),
    ("keputusan nyata dari dua proyek, lengkap dengan alasannya.", "muted"),
]


def whoami(t) -> str:
    b = ""
    y = 40
    for line, fill in WHOAMI:
        if line:
            b += text(0, y, line, size=27, fill=fill, t=t)
        y += 40
    return svg(y - 10, b)


def method(t) -> str:
    """Medallion: why the silver layer needs a point-in-time join."""
    b = text(0, 32, "Medallion — kenapa join biasa memberi angka yang salah", size=27, weight=600, t=t)

    cols = [("BRONZE", "salinan mentah", 0), ("SILVER", "dibersihkan, disatukan", 290), ("GOLD", "siap dibaca", 580)]
    for name, sub, x in cols:
        w = 236
        b += rect(x, 60, w, 92, t, fill="wash")
        b += text(x + 18, 98, name, size=22, weight=700, fill="accent", font=MONO, spacing=1, t=t)
        b += text(x + 18, 130, sub, size=21, fill="muted", t=t)
    b += arrow(246, 106, 282, t)
    b += arrow(536, 106, 572, t)

    b += rule(0, 190, W, t, dash="4 4")
    b += text(0, 228, "Harga pokok sebuah produk berubah dari waktu ke waktu.", size=25, t=t)
    b += text(0, 262, "Join pada product_id saja memakai harga pokok terbaru untuk", size=25, t=t)
    b += text(0, 296, "transaksi tahun lalu — margin historis jadi keliru.", size=25, t=t)

    b += rect(0, 324, W, 118, t, fill="wash")
    b += text(22, 362, "Perbaikan: as-of join", size=23, weight=700, fill="accent", font=MONO, t=t)
    b += text(22, 398, "ambil baris harga yang berlaku pada tanggal transaksi, bukan", size=23, fill="muted", t=t)
    b += text(22, 428, "baris harga yang berlaku hari ini.", size=23, fill="muted", t=t)
    return svg(466, b)


def topsis(t) -> str:
    """TOPSIS: the ideal and anti-ideal points are composites, not suppliers."""
    b = text(0, 32, "Supplier DSS — titik ideal itu tidak pernah ada", size=27, weight=600, t=t)

    ox, oy, ax = 70, 318, 232          # origin, and axis length
    b += vrule(ox, oy - ax, oy, t, stroke="muted")
    b += rule(ox, oy, ox + ax, t, stroke="muted")
    b += text(ox - 8, 76, "kualitas", size=20, fill="muted", font=MONO, t=t)
    b += text(ox, oy + 36, "harga, dibalik  →", size=20, fill="muted", font=MONO, t=t)

    for x, y, lab in ((118, 252, "A"), (180, 190, "B"), (236, 268, "C")):
        b += f'  <circle cx="{x}" cy="{y}" r="6" fill="{t["ink"]}"/>\n'
        b += text(x + 13, y - 11, lab, size=21, weight=600, font=MONO, t=t)

    # A+ takes the best value of every criterion, A- the worst of every one.
    b += (f'  <circle cx="276" cy="124" r="9" fill="none" stroke="{t["accent"]}" '
          f'stroke-width="2.5"/>\n')
    b += text(292, 118, "A+", size=21, weight=700, fill="accent", font=MONO, t=t)
    b += (f'  <circle cx="104" cy="296" r="9" fill="none" stroke="{t["accent"]}" '
          f'stroke-width="2.5" stroke-dasharray="3 3"/>\n')
    b += text(120, 316, "A−", size=21, weight=700, fill="accent", font=MONO, t=t)

    b += (f'  <path d="M180 190 L270 130" stroke="{t["accent"]}" stroke-width="1.5" '
          f'fill="none"/>\n')
    b += (f'  <path d="M180 190 L110 289" stroke="{t["accent"]}" stroke-width="1.5" '
          f'fill="none" stroke-dasharray="4 4"/>\n')
    b += text(232, 152, "S+", size=20, fill="accent", font=MONO, t=t)
    b += text(148, 266, "S−", size=20, fill="accent", font=MONO, t=t)

    x0 = 400
    for i, line in enumerate([
        "A+ menggabungkan nilai terbaik",
        "dari setiap kriteria, A− nilai",
        "terburuknya. Keduanya komposit",
        "khayalan: tidak ada pemasok",
        "yang berada di titik itu.",
    ]):
        b += text(x0, 96 + i * 34, line, size=23, t=t)
    b += rect(x0, 282, 390, 90, t, fill="wash")
    b += text(x0 + 18, 320, "C = S− / (S+ + S−)", size=25, weight=700, fill="accent", font=MONO, t=t)
    b += text(x0 + 18, 352, "dekat ideal, jauh dari terburuk", size=20, fill="muted", t=t)

    b += rule(0, 406, W, t, dash="3 5")
    b += text(0, 444, "Buang satu kriteria dan peringkatnya ikut berubah, karena A+ dan A−", size=23, fill="muted", t=t)
    b += text(0, 476, "dihitung ulang dari kolom yang tersisa.", size=23, fill="muted", t=t)
    return svg(500, b)


# The right-hand label carries the stack rather than repeating the repo name,
# which also keeps it short enough never to collide with the title.
WORK = [
    ("Medallion", "Gudang data batch yang menyatukan penjualan CRM dan ERP. Lapisan "
                  "bronze–silver–gold, as-of join untuk harga pokok historis.",
     "Python · SQL"),
    ("Data-Quality", "Enam dimensi kualitas data dan pemantauan drift 3σ atas 120 baris "
                     "sintetis. Termasuk simulasi bagaimana satu baris cacat "
                     "membelokkan garis regresi.",
     "pandas · sklearn"),
    ("ara-26", "Segmentasi kerusakan jalan, ARA ITS 2026. U-Net+++EfficientNet-B4 "
               "0.70773 di Kaggle, ensemble rata-rata probabilitas tiga model. Kerja tim.",
     "PyTorch"),
    ("agent", "Tujuh skrip Python tanpa dependensi berat untuk satu knowledge "
              "workspace. Recall holdout 0.889, MRR 1.0 pada uji pencarian.",
     "Python"),
    ("EventDriven-Streaming", "Pipeline ingesti berbasis Apache Kafka: produser, konsumer, "
                             "dan penanganan pesan yang datang tidak berurutan.",
     "Kafka"),
    ("Warungku", "Portal pemilik usaha: stok gudang dan perkiraan kebutuhan. "
                 "Tim berempat; bagian saya terutama logikanya.",
     "TypeScript"),
]


def work(t) -> str:
    b = ""
    y = 34
    for i, (name, desc, repo) in enumerate(WORK):
        if i:
            b += rule(0, y - 42, W, t, dash="3 5")
        b += text(0, y, name, size=27, weight=700, fill="accent", font=MONO, t=t)
        b += text(W, y, repo, size=20, fill="muted", font=MONO, anchor="end", t=t)
        y += 38
        # wrap at roughly 78 characters for 23px sans on an 846px canvas
        words, line = desc.split(), ""
        for wd in words:
            if len(line) + len(wd) + 1 > 78:
                b += text(0, y, line, size=23, fill="muted", t=t)
                y += 32
                line = wd
            else:
                line = f"{line} {wd}".strip()
        if line:
            b += text(0, y, line, size=23, fill="muted", t=t)
        y += 74
    return svg(y - 60, b)


STACK = [
    ("bahasa", "Python · SQL · TypeScript"),
    ("data", "pandas · scikit-learn · PyTorch · Kafka"),
    ("sehari-hari", "Git · Docker · Streamlit · Next.js · Postgres"),
    ("didalami", "arsitektur retrieval, evaluasi yang jujur"),
]


def stack(t) -> str:
    b = ""
    y = 36
    for label, items in STACK:
        b += text(0, y, label, size=21, weight=700, fill="accent", font=MONO, spacing=1, t=t)
        b += text(214, y, items, size=24, fill="ink", t=t)
        y += 30
        b += rule(0, y, W, t)
        y += 44
    return svg(y - 20, b)


def footer(t) -> str:
    b = rule(0, 1, W, t)
    b += text(0, 46, "Kerja Praktik · Januari–Juni 2027", size=23, fill="muted", t=t)
    b += text(W, 46, "ilhambintangporto.vercel.app", size=23, fill="accent", font=MONO, anchor="end", t=t)
    return svg(70, b)


VISUALS = {
    "header": header,
    "s01": lambda t: band("01", "whoami", t),
    "whoami": whoami,
    "s02": lambda t: band("02", "how i build", t),
    "method": method,
    "s03": lambda t: band("03", "one decision", t),
    "topsis": topsis,
    "s04": lambda t: band("04", "selected work", t),
    "work": work,
    "s05": lambda t: band("05", "stack", t),
    "stack": stack,
    "footer": footer,
}


def main() -> None:
    for theme, tokens in THEMES.items():
        out = os.path.join(ROOT, "assets") if theme == "light" else os.path.join(ROOT, "assets", "dark")
        os.makedirs(out, exist_ok=True)
        for name, fn in VISUALS.items():
            path = os.path.join(out, f"{name}.svg")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(fn(tokens))
    print(f"wrote {len(VISUALS) * 2} files into assets/ and assets/dark/")


if __name__ == "__main__":
    main()
