"""Build data/urban_rail_openings.csv from the curation files.

Usage: python build_openings.py

Inputs, all in data/curation/:
- events.csv: one row per UrbanRail.net opening (plus a few added rows),
  with the hand-reviewed line name, new-build flag, and include flag.
- cities.csv: UrbanRail.net city names to clean city and country names.
- lines.csv: per-line overrides of mode, mainline, grade separation, and GoA.
  Lines not listed there get the defaults for their UrbanRail.net mode below.
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURATION = ROOT / "data" / "curation"
OUT = ROOT / "data" / "urban_rail_openings.csv"

# (mode, mainline, grade_separated, goa) for each UrbanRail.net mode icon.
# Trams run on sight (GoA0); other lines default to the most common level.
DEFAULTS = {
    "metro": ("metro", "no", "yes", "2"),
    "light-rail": ("light rail", "no", "no", "1"),
    "tram": ("tram", "no", "no", "0"),
    "monorail": ("monorail", "no", "yes", "2"),
    "people-mover": ("people mover", "no", "yes", "4"),
    "s-bahn": ("commuter rail", "yes", "no", "1"),
}
# China's suburban lines (市域快轨) are metro-standard, not mainline.
CHINA_SUBURBAN = ("suburban metro", "no", "yes", "2")
DEFAULT_BASIS = "mode default; unverified"
# CAMET lists every FAO line opened since 2021, and its FAO totals
# leave no room for unlisted ones before that.
CHINA_NOT_FAO = "CAMET: not FAO (inferred from its FAO tables and totals)"

FIELDS = [
    "opening_date",
    "country",
    "city",
    "line",
    "mode",
    "km",
    "mainline",
    "grade_separated",
    "new_build",
    "goa",
    "automated",
    "goa_basis",
    "description",
    "note",
    "urbanrail_id",
]


def read(name):
    with open(CURATION / name, newline="") as f:
        return list(csv.DictReader(f))


def main():
    cities = {}
    for r in read("cities.csv"):
        cities[r["city"]] = r["country"]
    lines = {(r["city"], r["line"]): r for r in read("lines.csv")}
    used = set()
    out = []
    for e in read("events.csv"):
        if e["include"] != "yes":
            continue
        country = cities[e["city"]]
        mode, mainline, graded, goa = DEFAULTS[e["urbanrail_mode"]]
        if e["urbanrail_mode"] == "s-bahn" and country == "China":
            mode, mainline, graded, goa = CHINA_SUBURBAN
        basis = DEFAULT_BASIS
        if country == "China" and e["urbanrail_mode"] != "tram":
            basis = CHINA_NOT_FAO
        override = lines.get((e["city"], e["line"]))
        if override:
            used.add((e["city"], e["line"]))
            mode = override["mode"] or mode
            mainline = override["mainline"] or mainline
            graded = override["grade_separated"] or graded
            if override["goa"] or override["goa_basis"]:
                goa = override["goa"]
                basis = override["goa_basis"]
        automated = "" if goa == "" else ("yes" if int(goa) >= 3 else "no")
        out.append({
            "opening_date": e["date"],
            "country": country,
            "city": e["city"],
            "line": e["line"],
            "mode": mode,
            "km": e["km"],
            "mainline": mainline,
            "grade_separated": graded,
            "new_build": e["new_build"],
            "goa": goa,
            "automated": automated,
            "goa_basis": basis,
            "description": e["description"],
            "note": e["note"],
            "urbanrail_id": "" if e["id"].startswith("x") else e["id"],
        })
    unused = sorted(set(lines) - used)
    if unused:
        sys.exit(f"lines.csv rows matching no event: {unused}")
    out.sort(key=lambda r: (r["opening_date"], r["country"], r["city"], r["line"]))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)
    print(f"wrote {len(out)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
