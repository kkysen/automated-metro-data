#!/usr/bin/env bash
# Download UrbanRail.net's yearly lists of new openings into data/raw/urbanrail/.
set -euo pipefail

main() {
    local root
    root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    local out="${root}/data/raw/urbanrail"
    local first_year=2016
    local last_year
    last_year="$(date +%Y)"
    mkdir -p "${out}"
    local year
    for ((year = first_year; year < last_year; year++)); do
        curl -fsSL -o "${out}/news${year}.htm" "https://www.urbanrail.net/news${year}.htm"
    done
    # The current year lives on the main news page.
    curl -fsSL -o "${out}/news${last_year}.htm" "https://www.urbanrail.net/news.htm"
}

main "$@"
