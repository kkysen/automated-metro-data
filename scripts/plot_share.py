"""Chart the share of new lines that are automated (GoA3 or GoA4), by year.

Usage: python plot_share.py

Reads data/urban_rail_openings.csv and writes:
- data/automated_share_by_year.csv: the numbers behind the chart.
- charts/automated_share_by_year.svg: a bar chart of the share per year.

A line counts if it is new-build, fully grade-separated, and not mainline.
"""

import csv
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPENINGS = ROOT / "data" / "urban_rail_openings.csv"
TABLE = ROOT / "data" / "automated_share_by_year.csv"
SVG = ROOT / "charts" / "automated_share_by_year.svg"

# Layout, in px.
WIDTH = 760
HEIGHT = 420
LEFT = 56
RIGHT = 16
TOP = 72
BOTTOM = 64
BAR_GAP = 0.3


def counted(r):
    return r["new_build"] == "yes" and r["grade_separated"] == "yes" and r["mainline"] == "no"


def tally():
    total = Counter()
    automated = Counter()
    last_date = ""
    with open(OPENINGS, newline="") as f:
        for r in csv.DictReader(f):
            if not counted(r):
                continue
            year = r["opening_date"][:4]
            total[year] += 1
            automated[year] += r["automated"] == "yes"
            last_date = max(last_date, r["opening_date"])
    years = sorted(total)
    return [(y, total[y], automated[y]) for y in years], last_date


def write_table(rows):
    with open(TABLE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "new_lines", "automated_lines", "automated_share"])
        for year, n, a in rows:
            w.writerow([year, n, a, f"{a / n:.3f}"])


def bar_path(x, y, w, h, r):
    """A bar with rounded top corners, square at the baseline."""
    r = min(r, w / 2, h)
    return (
        f"M{x:.1f},{y + h:.1f} V{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} "
        f"H{x + w - r:.1f} Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f} V{y + h:.1f} Z"
    )


def write_svg(rows, last_date):
    plot_w = WIDTH - LEFT - RIGHT
    plot_h = HEIGHT - TOP - BOTTOM
    step = plot_w / len(rows)
    bar_w = step * (1 - BAR_GAP)
    n_all = sum(n for _, n, _ in rows)
    a_all = sum(a for _, _, a in rows)
    last_year = rows[-1][0]

    def y_of(share):
        return TOP + plot_h * (1 - share)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}" role="img" aria-labelledby="t d" '
        'font-family="system-ui, -apple-system, Segoe UI, sans-serif">',
        '<title id="t">Share of new metro lines that are automated (GoA3/GoA4), by year</title>',
        f'<desc id="d">{a_all} of {n_all} new grade-separated, non-mainline urban rail lines '
        f"opened from 2016 to {last_date} are automated.</desc>",
        "<style>",
        ".bg{fill:#fcfcfb}.bar{fill:#2a78d6}.bar.partial{fill-opacity:.55}",
        ".grid{stroke:#e4e3df;stroke-width:1}.axis{stroke:#a3a29c;stroke-width:1}",
        ".t1{fill:#0b0b0b}.t2{fill:#52514e}",
        "@media (prefers-color-scheme: dark){",
        ".bg{fill:#1a1a19}.bar{fill:#3987e5}.grid{stroke:#2e2e2c}.axis{stroke:#5d5c57}",
        ".t1{fill:#ffffff}.t2{fill:#c3c2b7}}",
        "</style>",
        f'<rect class="bg" width="{WIDTH}" height="{HEIGHT}" rx="8"/>',
        f'<text class="t1" x="{LEFT}" y="28" font-size="17" font-weight="600">'
        "Share of new metro lines that are automated (GoA3/GoA4)</text>",
        f'<text class="t2" x="{LEFT}" y="50" font-size="13">'
        f"New-build, grade-separated, non-mainline urban rail lines worldwide; "
        f"{a_all} of {n_all} ({a_all / n_all:.0%}) since 2016</text>",
    ]
    for share in (0, 0.25, 0.5, 0.75):
        y = y_of(share)
        cls = "axis" if share == 0 else "grid"
        out.append(f'<line class="{cls}" x1="{LEFT}" x2="{WIDTH - RIGHT}" y1="{y:.1f}" y2="{y:.1f}"/>')
        out.append(
            f'<text class="t2" x="{LEFT - 8}" y="{y + 4:.1f}" font-size="12" '
            f'text-anchor="end">{share:.0%}</text>'
        )
    for i, (year, n, a) in enumerate(rows):
        share = a / n
        x = LEFT + i * step + (step - bar_w) / 2
        y = y_of(share)
        cx = x + bar_w / 2
        partial = year == last_year
        label = f"{year}: {a} of {n} new lines automated ({share:.0%})"
        if partial:
            label += f", through {last_date}"
        out.append(f"<g><title>{escape(label)}</title>")
        # A hit target taller than the bar, for the native tooltip.
        out.append(
            f'<rect x="{LEFT + i * step:.1f}" y="{TOP}" width="{step:.1f}" '
            f'height="{plot_h}" fill="transparent"/>'
        )
        cls = "bar partial" if partial else "bar"
        out.append(f'<path class="{cls}" d="{bar_path(x, y, bar_w, y_of(0) - y, 4)}"/>')
        out.append(
            f'<text class="t1" x="{cx:.1f}" y="{y - 6:.1f}" font-size="12" '
            f'text-anchor="middle">{share:.0%}</text>'
        )
        out.append("</g>")
        year_label = f"{year}*" if partial else year
        out.append(
            f'<text class="t1" x="{cx:.1f}" y="{y_of(0) + 18:.1f}" font-size="12" '
            f'text-anchor="middle">{year_label}</text>'
        )
        out.append(
            f'<text class="t2" x="{cx:.1f}" y="{y_of(0) + 34:.1f}" font-size="11" '
            f'text-anchor="middle">{a}/{n}</text>'
        )
    out.append(
        f'<text class="t2" x="{LEFT}" y="{HEIGHT - 10}" font-size="11">'
        f"Below each year: automated/new lines. * {last_year} through {last_date}. "
        "Sources: UrbanRail.net, CAMET.</text>"
    )
    out.append("</svg>")
    SVG.parent.mkdir(exist_ok=True)
    SVG.write_text("\n".join(out) + "\n")


def main():
    rows, last_date = tally()
    write_table(rows)
    write_svg(rows, last_date)
    for year, n, a in rows:
        print(year, n, a, f"{a / n:.0%}")


if __name__ == "__main__":
    main()
