"""Fetch the GitHub stats card and drop the 'Total Issues' row."""
import re, sys, urllib.request

USER = "DavidBatoDev"
URL = f"https://github-profile-summary-cards.vercel.app/api/cards/stats?username={USER}&theme=tokyonight"
STEP = 25.2  # row height in the card

svg = urllib.request.urlopen(URL, timeout=30).read().decode()
if "Total Stars" not in svg:
    sys.exit("unexpected response, keeping existing card")

# icon group for row index 3 (nested <g> inside a gpsc-item <g>)
svg, n1 = re.subn(r'<g class="gpsc-item" style="--gpsc-i: 3;">\s*<g .*?</g>\s*</g>', "", svg, flags=re.S)
# label + value text for row index 3
svg, n2 = re.subn(r'<text [^>]*--gpsc-i: 3;[^>]*>.*?</text>', "", svg, flags=re.S)
if (n1, n2) != (1, 2):
    sys.exit(f"layout changed ({n1},{n2}), keeping existing card")

# pull the last row (index 4) up, and renumber it
svg = re.sub(r'(--gpsc-i: 4;">\s*<g transform="translate\(0,)([\d.]+)(\))',
             lambda m: f'{m.group(1)}{float(m.group(2)) - STEP:g}{m.group(3)}', svg)
svg = re.sub(r'(<text x="\d+" y=")([\d.]+)("[^>]*--gpsc-i: 4;)',
             lambda m: f'{m.group(1)}{float(m.group(2)) - STEP:g}{m.group(3)}', svg)

open("assets/stats.svg", "w", encoding="utf-8").write(svg)
print("ok")
