# Automated Metro Data

What share of the new metro lines opened worldwide in the last decade
are automated at GoA3 or GoA4?

This repo collects every new urban rail line opened since 2016-01-01
that is fully grade-separated and not part of the mainline railway,
tags each one with its grade of automation (GoA),
and computes the automated share.

## Scope

A line is counted if it is:

- **New-build**: an entirely new line, not an extension of an existing one.
  A line that opens in stages is counted once, at its first opening.
- **Fully grade-separated**: metro, grade-separated light rail, monorail,
  and automated people movers count; trams and street-running light rail do not.
- **Non-mainline**: metro-standard suburban lines (such as China's 市域快轨) count;
  services on mainline railways (such as S-Bahn, RER or commuter rail) do not.
- **Opened between 2016-01-01 and today**.

Lines are counted **by line**, not by km,
though the length at first opening is kept where known.

### What counts as automated

A line counts as automated if it was designed and opened for
GoA3 (driverless, with an attendant on board) or GoA4 (unattended) operation.
That includes Chinese lines designated as fully automated operation (FAO) by CAMET,
which are built for unattended operation,
but often start out with a driver or attendant on board.

Lines that are only "UTO-ready" are **not** counted.
These usually have CBTC signalling
but lack the obstacle and track-intrusion detection, FAO depots, and safety certification
that unattended operation needs,
and conversions to full automation are rare.

## Sources

- [UrbanRail.net](https://www.urbanrail.net/news.htm):
  a year-by-year log of every opening worldwide,
  which flags entirely new lines.
  `scripts/download_urbanrail.sh` downloads it,
  and `scripts/parse_urbanrail.py` turns it into a CSV of opening events.
- [CAMET](https://www.camet.org.cn/) (China Urban Rail Transit Association) annual reports,
  whose Appendix Table 2 (附表2) lists every new line in mainland China
  and marks the FAO ones.
- Wikipedia and operator sources for the GoA of lines outside China.
- [UITP Statistics Brief on metro automation](https://cms.uitp.org/wp/wp-content/uploads/2020/06/Statistics-Brief-Metro-automation_final_web03.pdf) (2019).

## Layout

- `scripts/`: download and parse scripts.
- `data/raw/`: downloaded source pages and reports.
- `data/`: generated and curated CSVs.
- `new_metro_lines_goa4.xlsx`: the earlier spreadsheet this work started from,
  with GoA4-only, km-based estimates.

## Status

Work in progress.
The earlier spreadsheet found that about 20% of new km in China
and about 48% of new lines elsewhere were GoA4 over the decade,
with the current annual rate near 50%.
Those figures are being redone by line count, with GoA3 included,
from the per-line sources above.
