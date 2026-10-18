# -*- coding: utf-8 -*-
"""Build the profile README visuals.

One spec, two themes. Every visual is written to assets/<name>.svg (light) and
assets/dark/<name>.svg, so the README can serve them through <picture> and
prefers-color-scheme without depending on any third-party widget service.

The layout is deliberately card-first: paragraphs do not survive on a profile
page, because nobody reads a profile, they scan it. Each unit is a title, a
short line, and a tag.

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


def text(x, y, s, *, size=24, fill="ink", font=SANS, weight=400,
         anchor="start", spacing=0, t=None) -> str:
    attrs = [
        f'x="{x}"', f'y="{y}"', f'font-family="{font}"', f'font-size="{size}"',
        f'font-weight="{weight}"', f'fill="{t[fill] if fill in t else fill}"',
    ]
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    return f'  <text {" ".join(attrs)}>{escape(s)}</text>\n'


def rule(x1, y, x2, t, *, stroke="line", width=1, dash=None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
            f'stroke="{t[stroke]}" stroke-width="{width}"{d}/>\n')


def vrule(x, y1, y2, t, *, stroke="line", width=1) -> str:
    return (f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" '
            f'stroke="{t[stroke]}" stroke-width="{width}"/>\n')


def rect(x, y, w, h, t, *, fill=None, stroke="line", rx=6, width=1) -> str:
    f = t[fill] if fill else "none"
    s = t[stroke] if stroke else "none"
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{f}" stroke="{s}" stroke-width="{width}"/>\n')


# ------------------------------------------------------------------ visuals

def header(t) -> str:
    # Widths are eyeballed for the generic sans stack, then given slack: the
    # reader's font is not ours, so nothing sits closer than ~24px to its
    # neighbour.
    b = text(0, 78, "ILHAM", size=80, weight=700, spacing=-1, t=t)
    b += text(276, 78, "BINTANG", size=80, weight=200, spacing=-1, fill="muted", t=t)
    b += text(0, 150, "SATRIA", size=80, weight=700, spacing=-1, t=t)
    b += rule(0, 182, W, t)
    b += text(0, 218, "Data · Machine Learning · Surabaya", size=25, fill="muted", t=t)
    b += text(W, 218, "@YonoBengkel", size=25, fill="accent", font=MONO, anchor="end", t=t)
    return svg(238, b)


def band(num, label, t) -> str:
    b = rect(0, 0, W, 56, t, fill="band", stroke=None, rx=4)
    b += text(22, 37, num, size=24, weight=700, fill="accent", font=MONO, t=t)
    b += text(76, 37, "—", size=24, fill="muted", font=MONO, t=t)
    b += text(112, 37, label, size=24, weight=500, font=MONO, spacing=1, t=t)
    return svg(56, b)


def whoami(t) -> str:
    b = text(0, 38, "AI Engineer intern di Ideola sejak Juli 2026.", size=26, t=t)
    b += text(0, 84, "Mengejar kenapa metode bekerja, bukan daftar tool yang memakainya.",
              size=24, fill="muted", t=t)
    return svg(108, b)


# title, one line, stack tag. The line is capped near 36 characters so it fits
# a half-width card without wrapping in a font we do not control.
WORK = [
    ("Medallion", "Gudang data CRM + ERP, as-of join", "Python · SQL"),
    ("Data-Quality", "Enam dimensi mutu, drift 3σ", "pandas"),
    ("ara-26", "Segmentasi jalan, Kaggle 0.70773", "PyTorch"),
    ("agent", "Recall 0.889, MRR 1.0", "Python"),
    ("EventDriven-Streaming", "Ingesti Kafka, pesan tak urut", "Kafka"),
    ("Warungku", "Stok gudang, tim berempat", "TypeScript"),
]


def work(t) -> str:
    gut, rows = 24, (len(WORK) + 1) // 2
    cw = (W - gut) // 2
    ch, gap = 112, 20
    b = ""
    for i, (name, line, tag) in enumerate(WORK):
        x = (i % 2) * (cw + gut)
        y = (i // 2) * (ch + gap)
        b += rect(x, y, cw, ch, t, fill="wash")
        b += text(x + 20, y + 42, name, size=23, weight=700, fill="accent", font=MONO, t=t)
        b += text(x + 20, y + 78, line, size=20, fill="ink", t=t)
        b += text(x + cw - 20, y + 100, tag, size=17, fill="muted", font=MONO, anchor="end", t=t)
    return svg(rows * ch + (rows - 1) * gap, b)


def topsis(t) -> str:
    """TOPSIS: the ideal and anti-ideal points are composites, not suppliers.

    The drawing carries the argument; only the formula and one caption are set
    in type.
    """
    b = ""
    ox, oy, ax = 70, 274, 216          # origin, and axis length
    b += vrule(ox, oy - ax, oy, t, stroke="muted")
    b += rule(ox, oy, ox + ax, t, stroke="muted")
    b += text(ox - 8, 32, "kualitas", size=19, fill="muted", font=MONO, t=t)
    b += text(ox, oy + 34, "harga, dibalik  →", size=19, fill="muted", font=MONO, t=t)

    for x, y, lab in ((116, 212, "A"), (176, 152, "B"), (230, 228, "C")):
        b += f'  <circle cx="{x}" cy="{y}" r="6" fill="{t["ink"]}"/>\n'
        b += text(x + 13, y - 11, lab, size=20, weight=600, font=MONO, t=t)

    # A+ takes the best value of every criterion, A- the worst of every one.
    b += (f'  <circle cx="268" cy="86" r="9" fill="none" stroke="{t["accent"]}" '
          f'stroke-width="2.5"/>\n')
    b += text(284, 80, "A+", size=20, weight=700, fill="accent", font=MONO, t=t)
    b += (f'  <circle cx="102" cy="254" r="9" fill="none" stroke="{t["accent"]}" '
          f'stroke-width="2.5" stroke-dasharray="3 3"/>\n')
    b += text(118, 274, "A−", size=20, weight=700, fill="accent", font=MONO, t=t)

    b += (f'  <path d="M176 152 L262 92" stroke="{t["accent"]}" stroke-width="1.5" '
          f'fill="none"/>\n')
    b += (f'  <path d="M176 152 L108 247" stroke="{t["accent"]}" stroke-width="1.5" '
          f'fill="none" stroke-dasharray="4 4"/>\n')
    b += text(226, 116, "S+", size=19, fill="accent", font=MONO, t=t)
    b += text(146, 226, "S−", size=19, fill="accent", font=MONO, t=t)

    x0 = 392
    b += rect(x0, 92, W - x0, 112, t, fill="wash")
    b += text(x0 + 24, 140, "C = S− / (S+ + S−)", size=27, weight=700,
              fill="accent", font=MONO, t=t)
    b += text(x0 + 24, 176, "A+ dan A− komposit khayalan", size=20, fill="muted", t=t)

    b += text(0, 348, "Buang satu kriteria, peringkatnya ikut berubah.", size=21, fill="muted", t=t)
    return svg(372, b)


def stack(t) -> str:
    # Monospace runs about 0.6em per character, so 58 characters at 21px is
    # roughly 730px and keeps clear of the 846px edge.
    b = text(0, 30, "Python · SQL · pandas · PyTorch · Kafka · Docker · Postgres",
             size=21, font=MONO, t=t)
    return svg(48, b)


def footer(t) -> str:
    b = rule(0, 1, W, t)
    b += text(0, 46, "Kerja Praktik · Januari–Juni 2027", size=23, fill="muted", t=t)
    b += text(W, 46, "ilhambintangporto.vercel.app", size=23, fill="accent", font=MONO, anchor="end", t=t)
    return svg(70, b)


VISUALS = {
    "header": header,
    "s01": lambda t: band("01", "whoami", t),
    "whoami": whoami,
    "s02": lambda t: band("02", "selected work", t),
    "work": work,
    "s03": lambda t: band("03", "one idea", t),
    "topsis": topsis,
    "s04": lambda t: band("04", "stack", t),
    "stack": stack,
    "footer": footer,
}

# Left over from the paragraph-heavy first version; removed so the repo does
# not ship visuals the README no longer references.
RETIRED = ("method", "s05")


def main() -> None:
    for theme in THEMES:
        out = os.path.join(ROOT, "assets") if theme == "light" else os.path.join(ROOT, "assets", "dark")
        os.makedirs(out, exist_ok=True)
        for name, fn in VISUALS.items():
            with open(os.path.join(out, f"{name}.svg"), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(fn(THEMES[theme]))
        for name in RETIRED:
            stale = os.path.join(out, f"{name}.svg")
            if os.path.exists(stale):
                os.remove(stale)
    print(f"wrote {len(VISUALS) * 2} files into assets/ and assets/dark/")


if __name__ == "__main__":
    main()
