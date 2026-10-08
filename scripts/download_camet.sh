#!/usr/bin/env bash
# Download CAMET (China Urban Rail Transit Association) reports into data/raw/camet/.
#
# camet-*.pdf are the year-end and mid-year bulletins (快报),
# whose appendix table lists every new line and marks the FAO ones.
# annual-*.pdf are the annual statistics and analysis reports,
# whose FAO sections list the new fully automated lines for 2021 and 2022
# and give per-year counts of new lines.
set -euo pipefail

main() {
    local root
    root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    local out="${root}/data/raw/camet"
    local oss="https://infosharingp2-oss.camet.org.cn"
    local bjtu="https://kyy.bjtu.edu.cn/media/attachments/2022/04"
    mkdir -p "${out}"
    local -A urls=(
        [annual-2015.pdf]="${bjtu}/20220428170745_735.pdf"
        [annual-2016.pdf]="${bjtu}/20220428170723_799.pdf"
        [annual-2018.pdf]="${oss}/u/cms/www/202206/15155806ka9f.pdf"
        [annual-2019.pdf]="${oss}/u/cms/www/202206/15155455y8f6.pdf"
        [annual-2021.pdf]="https://srmis.bjtu.edu.cn/media/attachments/2022/04/20220428170201_418.pdf"
        [annual-2022.pdf]="${oss}/u/cms/www/202304/07144043slcg.pdf"
        [annual-2024.pdf]="${oss}/resources/manual/2025/04/01/660853988892741.pdf"
        [camet-2023.pdf]="${oss}/u/cms/www/202401/011949480gg0.pdf"
        [camet-2024.pdf]="${oss}/resources/manual/2025/01/02/629337680478277.pdf"
        [camet-2025.pdf]="${oss}/resources/manual/2026/01/04/759313381470277.pdf"
        [camet-2026h1.pdf]="${oss}/resources/manual/2026/07/01/822296704208965.pdf"
    )
    local name
    for name in "${!urls[@]}"; do
        # The CAMET servers are slow, so skip files that are already here.
        if [[ -s "${out}/${name}" ]]; then
            continue
        fi
        curl -fsSL --max-time 600 -o "${out}/${name}" "${urls[${name}]}"
    done
}

main "$@"
