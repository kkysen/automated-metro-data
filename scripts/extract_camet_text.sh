#!/usr/bin/env bash
# Extract the text of the CAMET report pages this project relies on
# into data/camet_text/, so they can be read and searched without the PDFs.
#
# The pages are the bulletins' summaries and new-line tables (附表2),
# and the annual reports' tables of new lines and sections on
# fully automated operation (FAO, 全自动运行), including FAO km totals.
# Run scripts/download_camet.sh first.
set -euo pipefail

main() {
    local root
    root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    local in="${root}/data/raw/camet"
    local out="${root}/data/camet_text"
    mkdir -p "${out}"
    local -A pages=(
        [annual-2015]="27"
        [annual-2016]="8 9 10 11 41"
        [annual-2018]="45"
        [annual-2019]="56"
        [annual-2021]="3 12 61"
        [annual-2022]="5 15 74"
        [annual-2024]="5 14 15"
        [camet-2023]="1 3 5 10 11 12"
        [camet-2024]="1 2 3 4 11 12 13 14"
        [camet-2025]="1 2 3 4 10 11 12 13 14"
        [camet-2026h1]="1 2 3 9"
    )
    local name
    local page
    for name in "${!pages[@]}"; do
        {
            echo "# ${name}.pdf: selected pages, extracted by scripts/extract_camet_text.sh"
            echo "# In the new-line tables, a * on the line above a row marks an FAO line."
            for page in ${pages[${name}]}; do
                echo
                echo "## Page ${page}"
                echo
                # Drop lines made up only of the diagonal watermark's characters,
                # and trailing spaces left by the layout.
                pdftotext -q -layout -f "${page}" -l "${page}" "${in}/${name}.pdf" - \
                    | rg -v '^[\s中国城市轨道交通协会]*[中国城市轨道交通协会][\s中国城市轨道交通协会]*$' \
                    | sed -E 's/[[:space:]]+$//' \
                    | cat -s
            done
        } > "${out}/${name}.txt"
    done
}

main "$@"
