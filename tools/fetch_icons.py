# -*- coding: utf-8 -*-
"""Vendor the devicon SVGs used by the stack marquee.

The marquee has to inline them: an SVG loaded through <img>, which is how
GitHub serves README images, is not allowed to fetch external resources, so a
remote <image href> would render as nothing.

Run once, or whenever ICONS changes:  python tools/fetch_icons.py
"""

from __future__ import annotations

import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "icons")
BASE = "https://raw.githubusercontent.com/devicons/devicon/master/icons"

# (devicon folder, file suffix). Ordered roughly the way the work flows:
# language, notebook, data, modelling, storage, streaming, ops, web.
ICONS = [
    ("python", "original"),
    ("jupyter", "original"),
    ("pandas", "original"),
    ("numpy", "original"),
    ("scikitlearn", "original"),
    ("pytorch", "original"),
    ("tensorflow", "original"),
    ("opencv", "original"),
    ("plotly", "original"),
    ("postgresql", "original"),
    ("mysql", "original"),
    ("sqlalchemy", "original"),
    ("apachekafka", "original"),
    ("apachespark", "original"),
    ("apacheairflow", "original"),
    ("docker", "original"),
    ("git", "original"),
    ("linux", "original"),
    ("bash", "original"),
    ("anaconda", "original"),
    ("streamlit", "original"),
    ("fastapi", "original"),
    ("typescript", "original"),
    ("javascript", "original"),
    ("react", "original"),
    ("tailwindcss", "original"),
    ("vscode", "original"),
]


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    ok, bad = 0, []
    for name, suffix in ICONS:
        url = f"{BASE}/{name}/{name}-{suffix}.svg"
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                if r.status != 200:
                    bad.append((name, r.status))
                    continue
                data = r.read()
        except Exception as exc:                      # noqa: BLE001 - report and move on
            bad.append((name, type(exc).__name__))
            continue
        with open(os.path.join(OUT, f"{name}.svg"), "wb") as fh:
            fh.write(data)
        ok += 1
    print(f"fetched {ok}/{len(ICONS)} into tools/icons/")
    for name, why in bad:
        print(f"  MISSING {name}: {why}")


if __name__ == "__main__":
    main()
