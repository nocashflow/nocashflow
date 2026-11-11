"""
NOCASHFLOW // netrunner bounty poster — GitHub profile README generator.

Edit CONFIG, then run:   python build.py
Writes README.md + assets/header.svg + assets/seismograph.svg.
(The old geological-survey version lives in archive/geological-survey/.)
"""
import math
import random
from html import escape
from pathlib import Path

# ─────────────────────────────── EDIT ME ────────────────────────────────
CONFIG = {
    "username": "nocashflow",
    "name": "NOCASHFLOW",
    "id": "NC-0x2A",
    "tagline": "ships first, reads the docs later",
    "role": "NETRUNNER · FREELANCE · MOSTLY HARMLESS",

    "bounty": [  # right-hand wanted panel
        ("WANTED FOR", "crimes against prod"),
        ("LAST SEEN", "force-pushing to main"),
        ("KNOWN ALIASES", "'fix', 'fix 2', 'final fix'"),
    ],
    "reward": "€$ 0.00",
    "reward_note": "no cash flow. it's in the name.",

    "bars": [  # label, percent
        ("HUMANITY", 62),
        ("CAFFEINE", 94),
        ("SLEEP", 8),
    ],

    "ticker": [
        "I'LL TAKE YOU TO THE MOON",
        "DEPLOYS ON FRIDAYS",
        "SHIPS FIRST · READS DOCS LATER",
        "47 UNFINISHED REPOS AND COUNTING",
        "CHROME: OPTIONAL · COMMITS: MANDATORY",
    ],

    # Spikes on the seismograph. magnitude 1–9 sets spike height.
    # Keep values under ~22 characters (the last one can go to ~28).
    "readings": [
        {"label": "currently learning", "value": "whatever breaks next", "magnitude": 5.1},
        {"label": "open to", "value": "positive cash flow", "magnitude": 7.4},
        {"label": "ask me about", "value": "my 47 unfinished repos", "magnitude": 4.3},
        {"label": "fun fact", "value": "my code works. no idea why", "magnitude": 6.2},
    ],
}
# ────────────────────────────────────────────────────────────────────────

W = 840
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SERIF = "Georgia, 'Times New Roman', serif"
DISPLAY = "Impact, 'Haettenschweiler', 'Arial Narrow Bold', 'Franklin Gothic Heavy', sans-serif"
YEL, CYAN, PINK, INK, BG = "#fcee0a", "#3ef0ff", "#ff2e88", "#0d0b14", "#0a0812"


def pts(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def build_header(c):
    H = 352
    rnd = random.Random(42)

    # yellow ID slab with cut corners
    sx0, sy0, sx1, sy1, cut = 24, 34, 556, 256, 34
    slab = [(sx0, sy0), (sx1 - cut, sy0), (sx1, sy0 + cut), (sx1, sy1), (sx0 + cut, sy1), (sx0, sy1 - cut)]

    # barcode on the slab
    bx, barcode = 64, ""
    while bx < 300:
        w = rnd.choice([1, 1, 2, 3])
        barcode += f'<rect x="{bx}" y="214" width="{w}" height="22" fill="{INK}"/>'
        bx += w + rnd.choice([1, 2, 2, 3])

    # glitch slices of the name: copies clipped to thin bands that jump sideways
    name = escape(c["name"])
    name_attrs = f'x="56" y="168" font-family="{DISPLAY}" font-size="84" font-weight="900" letter-spacing="1"'
    slices = ""
    for i, (y, h, dx, d) in enumerate([(108, 9, 14, 0.0), (132, 6, -18, 1.3), (150, 11, 10, 2.1)]):
        slices += (f'<clipPath id="s{i}"><rect x="0" y="{y}" width="{W}" height="{h}"/></clipPath>'
                   f'<g clip-path="url(#s{i})"><g class="slice" style="--dx:{dx}px;animation-delay:{d}s">'
                   f'<rect x="40" y="{y}" width="500" height="{h}" fill="{YEL}"/>'
                   f'<text {name_attrs} fill="{INK}">{name}</text></g></g>')

    # halftone dots, bottom-right
    halftone = "".join(
        f'<circle cx="{x}" cy="{y}" r="{max(0.3, (x - 560) / 260 * 2.2 * (y / H)):.2f}" fill="{PINK}" opacity=".5"/>'
        for x in range(570, W, 9) for y in range(270, H, 9))

    # wanted panel
    px0, py0, px1, py1 = 576, 34, 816, 256
    panel = [(px0, py0), (px1, py0), (px1, py1 - 22), (px1 - 22, py1), (px0, py1)]
    rows = ""
    y = 90
    for label, val in c["bounty"]:
        rows += (f'<text x="{px0 + 18}" y="{y}" font-family="{MONO}" font-size="9" fill="{CYAN}" letter-spacing="1.6">{escape(label)}</text>'
                 f'<text x="{px0 + 18}" y="{y + 16}" font-family="{MONO}" font-size="12" fill="#fff6ea">{escape(val)}</text>')
        y += 34

    # status bars
    bars = ""
    for i, (label, pct) in enumerate(c["bars"]):
        x = 24 + i * 200
        cells = ""
        for k in range(10):
            on = k < round(pct / 10)
            color = PINK if (label == "SLEEP" or (label == "HUMANITY" and k >= 5)) and on else YEL
            cells += (f'<rect x="{x + 74 + k * 8}" y="275" width="6" height="12" fill="{color if on else "#2a2433"}"'
                      f'{" class=\"blink\"" if on and k == round(pct / 10) - 1 else ""}/>')
        bars += (f'<text x="{x}" y="285" font-family="{MONO}" font-size="10" fill="#fff6ea" letter-spacing="1.4">{escape(label)}</text>'
                 f'{cells}<text x="{x + 158}" y="285" font-family="{MONO}" font-size="10" fill="{CYAN}">{pct:02d}%</text>')

    # ticker: two copies forced to the same exact width with textLength, so the loop is seamless
    tick = "  //  ".join(c["ticker"]) + "  //  "
    L = round(len(tick) * 7.4)
    tick_txt = escape(tick)
    ticker = "".join(
        f'<text x="{off}" y="333" font-family="{MONO}" font-size="12" font-weight="700" fill="{INK}" '
        f'textLength="{L}" lengthAdjust="spacing" xml:space="preserve">{tick_txt}</text>' for off in (0, L, 2 * L))

    stars = "".join(f'<rect x="{rnd.uniform(0, W):.0f}" y="{rnd.uniform(0, 30):.0f}" width="1" height="1" fill="{CYAN}" opacity=".5"/>'
                    for _ in range(30))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{name}: netrunner bounty poster. {escape(c['tagline'])}">
<style>
.rgb-c{{animation:rgbc 3.2s steps(1) infinite}}
.rgb-m{{animation:rgbm 3.2s steps(1) infinite}}
@keyframes rgbc{{0%{{transform:translate(-3px,0)}}8%{{transform:translate(-7px,1px)}}10%{{transform:translate(-3px,0)}}52%{{transform:translate(-5px,-1px)}}54%{{transform:translate(-3px,0)}}}}
@keyframes rgbm{{0%{{transform:translate(3px,0)}}8%{{transform:translate(8px,-1px)}}10%{{transform:translate(3px,0)}}52%{{transform:translate(5px,1px)}}54%{{transform:translate(3px,0)}}}}
.slice{{opacity:0;animation:slice 3.2s steps(1) infinite}}
@keyframes slice{{0%{{opacity:0;transform:none}}8%{{opacity:1;transform:translateX(var(--dx))}}11%{{opacity:0;transform:none}}}}
.scan{{animation:scan 4.5s linear infinite}}
@keyframes scan{{from{{transform:translateY(-40px)}}to{{transform:translateY({H}px)}}}}
.tick{{animation:tick {L / 38:.1f}s linear infinite}}
@keyframes tick{{to{{transform:translateX(-{L}px)}}}}
.blink{{animation:blink 1.1s steps(2) infinite}}
@keyframes blink{{50%{{opacity:.2}}}}
.flicker{{animation:flicker 5s linear infinite}}
@keyframes flicker{{0%,19%,21%,62%,64%,100%{{opacity:1}}20%,63%{{opacity:.35}}}}
.boot{{opacity:0;animation:boot .5s steps(3) forwards}}
@keyframes boot{{to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.boot{{opacity:1}}.slice{{opacity:0}}}}
</style>
<defs>
<clipPath id="frame"><path d="M0,0 H{W - 28} L{W},28 V{H} H28 L0,{H - 28} Z"/></clipPath>
<pattern id="scanl" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".28"/></pattern>
<pattern id="haz" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="16" fill="{YEL}"/></pattern>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".16"/></linearGradient>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{BG}"/>
{stars}
{halftone}
<rect x="0" y="0" width="{W}" height="20" fill="url(#haz)" opacity=".9"/>
<rect x="0" y="0" width="230" height="20" fill="{BG}"/>
<text x="14" y="14" font-family="{MONO}" font-size="10" fill="{YEL}" letter-spacing="2.2">// JACK-IN SEQUENCE OK</text>

<g class="boot" style="animation-delay:.1s">
<polygon points="{pts(slab)}" fill="{YEL}"/>
<polygon points="{pts([(sx1 - cut + 8, sy0), (sx1, sy0), (sx1, sy0 + cut - 8)])}" fill="{PINK}"/>
<text x="56" y="70" font-family="{MONO}" font-size="10" font-weight="700" fill="{INK}" letter-spacing="2.4">NETRUNNER ID // {escape(c['id'])}</text>
<text x="56" y="86" font-family="{MONO}" font-size="9" fill="{INK}" opacity=".7" letter-spacing="1.6">{escape(c['role'])}</text>
<g class="rgb-c"><text {name_attrs} fill="{CYAN}" opacity=".9">{name}</text></g>
<g class="rgb-m"><text {name_attrs} fill="{PINK}" opacity=".9">{name}</text></g>
<text {name_attrs} fill="{INK}">{name}</text>
{slices}
<text x="58" y="196" font-family="{MONO}" font-size="13" fill="{INK}">&gt; {escape(c['tagline'])}<tspan class="blink">_</tspan></text>
{barcode}
<text x="312" y="234" font-family="{MONO}" font-size="9" fill="{INK}" letter-spacing="1.4">@{escape(c['username']).upper()} · ISSUED 2077</text>
<text x="312" y="234" dy="12" font-family="{MONO}" font-size="9" fill="{INK}" opacity=".6" letter-spacing="1.4">VOID WHERE PROHIBITED</text>
</g>

<g class="boot" style="animation-delay:.45s">
<polygon points="{pts(panel)}" fill="#120e1c" stroke="{CYAN}" stroke-width="1.2"/>
<rect x="{px0}" y="{py0}" width="{px1 - px0}" height="34" fill="{PINK}"/>
<text x="{px0 + 18}" y="{py0 + 23}" font-family="{DISPLAY}" font-size="22" fill="{INK}" letter-spacing="3">WANTED</text>
<text x="{px1 - 14}" y="{py0 + 21}" text-anchor="end" font-family="{MONO}" font-size="9" font-weight="700" fill="{INK}" letter-spacing="1.4">DEAD OR DEPLOYED</text>
{rows}
<line x1="{px0 + 18}" y1="{y - 6}" x2="{px1 - 18}" y2="{y - 6}" stroke="{CYAN}" stroke-opacity=".35" stroke-dasharray="3 3"/>
<text x="{px0 + 18}" y="{y + 8}" font-family="{MONO}" font-size="9" fill="{CYAN}" letter-spacing="1.6">REWARD</text>
<text class="flicker" x="{px0 + 18}" y="{y + 36}" font-family="{DISPLAY}" font-size="32" fill="{YEL}" letter-spacing="1">{escape(c['reward'])}</text>
<text x="{px0 + 18}" y="{y + 52}" font-family="{MONO}" font-size="9" fill="#fff6ea" opacity=".6">{escape(c['reward_note'])}</text>
</g>

<g class="boot" style="animation-delay:.8s">{bars}</g>

<rect x="0" y="312" width="{W}" height="30" fill="{YEL}"/>
<rect x="0" y="312" width="{W}" height="2" fill="{PINK}"/>
<g class="tick">{ticker}</g>

<rect class="scan" x="0" y="0" width="{W}" height="40" fill="url(#beam)"/>
<rect width="{W}" height="{H}" fill="url(#scanl)"/>
</g>
<path d="M0,0 H{W - 28} L{W},28 V{H} H28 L0,{H - 28} Z" fill="none" stroke="{CYAN}" stroke-opacity=".5" stroke-width="2"/>
</svg>'''


def build_seismo(c):
    H, base = 236, 166
    readings = c["readings"][:5]
    xs = [104 + i * (W - 304) / max(1, len(readings) - 1) for i in range(len(readings))]
    rnd = random.Random(3)
    trace = []
    for x10 in range(30 * 2, (W - 24) * 2):
        x = x10 / 2
        y = base + rnd.uniform(-1.6, 1.6)
        for xi, r in zip(xs, readings):
            dx = x - xi
            if 0 <= dx < 70:
                amp = r["magnitude"] * 6.2 * math.exp(-dx / 14)
                y += amp * math.sin(dx * 1.15)
            elif -6 < dx < 0:
                y += rnd.uniform(-2, 2)
        trace.append((x, y))
    cum, total = [0.0], 0.0
    for a, b in zip(trace, trace[1:]):
        total += math.dist(a, b)
        cum.append(total)
    dur, start = 5.0, 0.3

    def t_at(x):
        idx = min(range(len(trace)), key=lambda k: abs(trace[k][0] - x))
        return start + dur * cum[idx] / total

    grid = "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="{H-14}" stroke="#fcee0a" stroke-opacity="{.13 if x % 50 == 30 else .04}"/>'
                   for x in range(30, W - 20, 10))
    grid += "".join(f'<line x1="30" y1="{y}" x2="{W-24}" y2="{y}" stroke="#fcee0a" stroke-opacity="{.13 if (y-40) % 40 == 0 else .04}"/>'
                    for y in range(40, H - 13, 10))

    labels = ""
    for k, (xi, r) in enumerate(zip(xs, readings)):
        peak = base - r["magnitude"] * 6.2 * 0.9 - 6
        ly = 82
        last = k == len(xs) - 1
        tx, anc = xi - 8, "start"
        labels += (f'<g class="fade" style="animation-delay:{t_at(xi + 8):.2f}s">'
                   f'<line x1="{xi+1}" y1="{max(peak, ly + 6):.0f}" x2="{xi+1}" y2="{ly + 6}" stroke="#ff2e88" stroke-width=".9" stroke-dasharray="2 2"/>'
                   f'<circle cx="{xi+1}" cy="{ly+6}" r="2.2" fill="#ff2e88"/>'
                   f'<text x="{tx}" y="{ly - 22}" text-anchor="{anc}" font-family="{MONO}" font-size="9" fill="#3ef0ff" letter-spacing=".9">'
                   f'M{r["magnitude"]:.1f} · {escape(r["label"]).upper()}</text>'
                   f'<text x="{tx}" y="{ly - 5}" text-anchor="{anc}" font-family="{SERIF}" font-size="15" font-style="italic" fill="#fff6ea">'
                   f'{escape(r["value"])}</text></g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Seismograph readings">
<style>
.tr{{stroke-dasharray:{total:.0f};stroke-dashoffset:{total:.0f};animation:tr {dur}s linear {start}s forwards}}
@keyframes tr{{to{{stroke-dashoffset:0}}}}
.fade{{opacity:0;animation:fade .7s ease-out forwards}}
@keyframes fade{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:none}}}}
.rec{{animation:rec 1.2s steps(2) infinite}}
@keyframes rec{{50%{{opacity:.15}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.tr{{stroke-dashoffset:0}}.fade{{opacity:1}}}}
</style>
<defs><clipPath id="f"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="paper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0b14"/><stop offset="1" stop-color="#16101f"/></linearGradient><filter id="neon" x="-5%" y="-30%" width="110%" height="160%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".35"/></pattern></defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="url(#paper)"/>
{grid}
<rect width="{W}" height="30" fill="#fcee0a"/><path d="M{W-150},30 l14,10 H{W} V30 Z" fill="#fcee0a"/>
<circle class="rec" cx="22" cy="15" r="4" fill="#ff2e88"/>
<text x="34" y="19" font-family="{MONO}" font-size="10" font-weight="700" fill="#0d0b14" letter-spacing="2.4">SEISMOGRAPH · STATION @{escape(c['username']).upper()} · LIVE READING</text>
<text x="{W-16}" y="19" text-anchor="end" font-family="{MONO}" font-size="10" fill="#0d0b14" opacity=".7" font-weight="700" letter-spacing="2">SCALE: VIBES</text>
<polyline class="tr" points="{pts(trace)}" fill="none" stroke="#fcee0a" stroke-width="1.4" stroke-linejoin="round" filter="url(#neon)"/>
<rect y="30" width="{W}" height="{H}" fill="url(#scan)"/>
{labels}
</g>
</svg>'''



def build_readme(c):
    readings = escape('; '.join(r['label'] + ': ' + r['value'] for r in c['readings']))
    return f'''<p align="center">
  <img src="./assets/header.svg" width="100%" alt="{escape(c['name'])}: netrunner bounty poster. Wanted for crimes against prod. Reward: {escape(c['reward'])}.">
</p>

<p align="center">
  <img src="./assets/seismograph.svg" width="100%" alt="Seismograph readings: {readings}">
</p>

<p align="center"><sub><code>// END OF TRANSMISSION</code> · jack into the repos below ↓</sub></p>
'''


if __name__ == "__main__":
    out = Path(__file__).parent
    (out / "assets").mkdir(exist_ok=True)
    (out / "assets" / "header.svg").write_text(build_header(CONFIG), encoding="utf-8")
    (out / "assets" / "seismograph.svg").write_text(build_seismo(CONFIG), encoding="utf-8")
    (out / "README.md").write_text(build_readme(CONFIG), encoding="utf-8")
    print("wrote README.md, assets/header.svg, assets/seismograph.svg")
