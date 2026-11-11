"""
NOCASHFLOW // netrunner bounty poster — GitHub profile README generator.

Edit CONFIG, then run:   python build.py
Writes README.md + assets/header.svg + assets/braindance.svg.
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
        "WE'RE HAVING A MOMENT HERE",
        "PLATINUM PLAN WON'T SAVE THIS BUILD",
        "AIN'T WORTH IT, CHOOM · DEPLOYING ANYWAY",
        "MY CODE? JUST A RUDIMENTARY IMPLANT",
        "CAPRI'S IN THE TERMINAL · WHO GAVE HER SUDO ACCESS",
        "NO HAPPY ENDINGS IN NIGHT CITY",
    ],

    # Clues on the braindance timeline. magnitude 1–9 sets the audio burst.
    # Keep values under ~22 characters (the last one can go to ~28).
    "readings": [
        {"label": "currently learning", "value": "how not to flatline prod", "magnitude": 5.1},
        {"label": "open to", "value": "positive cash flow", "magnitude": 7.4},
        {"label": "ask me about", "value": "how i fumbled the moon", "magnitude": 4.3},
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


def build_braindance(c):
    """Braindance editor timeline: visual / audio / thermal tracks, readings pinned as clues,
    a playhead scrubbing toward a moon at the end of the recording."""
    H = 236
    readings = c["readings"][:4]
    rnd = random.Random(2077)
    tx0, tx1 = 104, 690                      # track area
    tracks = [("VISUAL", YEL, 92), ("AUDIO", CYAN, 118), ("THERMAL", PINK, 144)]
    th = 22
    cx = [tx0 + 40 + i * (tx1 - tx0 - 170) / max(1, len(readings) - 1) for i in range(len(readings))]

    # time ruler
    ruler = ""
    for k, x in enumerate(range(tx0, tx1 + 1, 10)):
        big = k % 10 == 0
        ruler += f'<line x1="{x}" y1="{86 - (6 if big else 3)}" x2="{x}" y2="86" stroke="#fff6ea" stroke-opacity="{.5 if big else .2}"/>'
        if big:
            ruler += (f'<text x="{x + 3}" y="79" font-family="{MONO}" font-size="7.5" fill="#fff6ea" opacity=".45">'
                      f'00:{k // 10 * 12:02d}:00</text>')

    # VISUAL: film-strip frames, brighter around clues
    vis, x = "", tx0
    while x < tx1:
        w = 14
        near = min(abs(x - p) for p in cx)
        op = .85 if near < 18 else rnd.uniform(.12, .38)
        vis += f'<rect x="{x}" y="{tracks[0][2] + 3}" width="{w - 2}" height="{th - 6}" fill="{YEL}" opacity="{op:.2f}"/>'
        x += w

    # AUDIO: waveform bars with bursts at clues (height from magnitude)
    aud, ay = "", tracks[1][2] + th / 2
    for x in range(tx0, tx1, 3):
        h = rnd.uniform(1, 5)
        for p, r in zip(cx, readings):
            d = abs(x - p)
            if d < 26:
                h += r["magnitude"] * 1.3 * (1 - d / 26) * rnd.uniform(.6, 1)
        h = min(h, th / 2 - 1)
        aud += f'<line x1="{x}" y1="{ay - h:.1f}" x2="{x}" y2="{ay + h:.1f}"/>'

    # THERMAL: heat gradient, hot spots at clues
    stops = []
    for i in range(41):
        f = i / 40
        x = tx0 + f * (tx1 - tx0)
        heat = .18 + rnd.uniform(0, .12) + sum(max(0, 1 - abs(x - p) / 40) for p in cx)
        heat = min(heat, 1)
        col = "#2a0f2e" if heat < .3 else ("#7a1450" if heat < .5 else (PINK if heat < .8 else "#ffb35a"))
        stops.append(f'<stop offset="{f:.3f}" stop-color="{col}"/>')

    # clues: marker through all tracks + label (alternating above / below)
    clues = ""
    for i, (p, r) in enumerate(zip(cx, readings)):
        top = i % 2 == 0
        ly = 40 if top else 196
        tx, anc = p + 6, "start"
        y_from = 86 if top else 166
        y_to = 58 if top else 182
        clues += (
            f'<line x1="{p:.0f}" y1="88" x2="{p:.0f}" y2="168" stroke="#fff6ea" stroke-width="1" stroke-opacity=".75"/>'
            f'<rect class="pulse" x="{p - 11:.0f}" y="{tracks[i % 3][2] - 1}" width="22" height="{th + 2}" fill="none" '
            f'stroke="{YEL}" stroke-width="1.2" style="animation-delay:{i * .5:.1f}s"/>'
            f'<line x1="{p:.0f}" y1="{y_from}" x2="{p:.0f}" y2="{y_to}" stroke="#fff6ea" stroke-opacity=".5" stroke-dasharray="2 2"/>'
            f'<path d="M{p:.0f},{y_to - 4} l4,4 l-4,4 l-4,-4 z" fill="{YEL}"/>'
            f'<text x="{tx:.0f}" y="{ly}" text-anchor="{anc}" font-family="{MONO}" font-size="8.5" fill="{CYAN}" letter-spacing="1.3">'
            f'CLUE {i + 1:02d} · {escape(r["label"]).upper()}</text>'
            f'<text x="{tx:.0f}" y="{ly + 17}" text-anchor="{anc}" font-family="{MONO}" font-size="13" font-weight="700" fill="#fff6ea">'
            f'{escape(r["value"])}</text>')

    # track labels
    tl = "".join(
        f'<rect x="16" y="{y}" width="{tx0 - 24}" height="{th}" fill="#16111f"/>'
        f'<rect x="16" y="{y}" width="3" height="{th}" fill="{col}"/>'
        f'<text x="26" y="{y + 14.5}" font-family="{MONO}" font-size="9" fill="{col}" letter-spacing="1.4">{name}</text>'
        for name, col, y in tracks)

    # the moon at the end of the recording, two tiny anonymous figures sitting on it
    mx, my, mr = 764, 128, 46
    craters = "".join(f'<circle cx="{mx + dx}" cy="{my + dy}" r="{r}" fill="#cfc8b8" opacity=".55"/>'
                      for dx, dy, r in [(-14, -10, 7), (12, 8, 9), (-6, 20, 4), (20, -18, 3.5), (-24, 10, 3)])
    fig = lambda x, y, s: (
        f'<g transform="translate({x} {y}) scale({s})" fill="{INK}">'
        f'<circle cx="0" cy="-11" r="2.6"/><path d="M-2.4,-8 h4.8 l.8,7 h-6.4 z"/>'
        f'<path d="M-3.2,-1.2 h7 l1.6,4.6 h-2.2 l-1.2,-2.6 h-5.2 z"/></g>')
    moon = (f'<circle cx="{mx}" cy="{my}" r="{mr + 14}" fill="url(#halo)"/>'
            f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="#efe9da"/>{craters}'
            f'{fig(mx - 6, my - mr + 2, 1)}{fig(mx + 6, my - mr + 2.5, .95)}'
            f'<text x="{mx}" y="{my - mr - 24}" text-anchor="middle" font-family="{MONO}" font-size="8" fill="#fff6ea" '
            f'opacity=".55" letter-spacing="1.6">END OF RECORDING</text>')

    stars = "".join(f'<circle cx="{rnd.uniform(706, 830):.0f}" cy="{rnd.uniform(36, 210):.0f}" r="{rnd.choice([.6, .8, 1])}" '
                    f'fill="#fff6ea" class="tw" style="animation-delay:{rnd.uniform(0, 3):.1f}s"/>' for _ in range(22))

    scrub = tx1 - tx0
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Braindance editor timeline">
<style>
.ph{{animation:ph 9s linear infinite}}
@keyframes ph{{from{{transform:translateX(0)}}to{{transform:translateX({scrub}px)}}}}
.pulse{{animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
.rec{{animation:rec 1.2s steps(2) infinite}}
@keyframes rec{{50%{{opacity:.15}}}}
.tw{{animation:tw 3s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.2}}50%{{opacity:.9}}}}
.wave{{animation:wave 1.6s ease-in-out infinite alternate;transform-origin:0 {ay}px}}
@keyframes wave{{to{{transform:scaleY(.7)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
<clipPath id="f"><path d="M0,0 H{W - 22} L{W},22 V{H} H22 L0,{H - 22} Z"/></clipPath>
<linearGradient id="heat" x1="{tx0}" y1="0" x2="{tx1}" y2="0" gradientUnits="userSpaceOnUse">{"".join(stops)}</linearGradient>
<radialGradient id="halo"><stop offset=".7" stop-color="#fff6ea" stop-opacity=".18"/><stop offset="1" stop-color="#fff6ea" stop-opacity="0"/></radialGradient>
<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".3"/></pattern>
</defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="698" y="28" width="{W - 698}" height="{H - 28}" fill="#0f0b1a"/>
{stars}
<rect width="{W}" height="28" fill="#16111f"/>
<rect y="27" width="{W}" height="1" fill="{CYAN}" opacity=".5"/>
<circle class="rec" cx="20" cy="14" r="4" fill="{PINK}"/>
<text x="32" y="18" font-family="{MONO}" font-size="10" fill="{YEL}" letter-spacing="2">BD EDITOR · REC_{escape(c['username']).upper()}.bd</text>
<text x="{W - 16}" y="18" text-anchor="end" font-family="{MONO}" font-size="10" fill="#fff6ea" opacity=".6" letter-spacing="2">EDIT MODE · LAYERS 3/3 · 4 CLUES FOUND</text>
{ruler}
{tl}
<rect x="{tx0}" y="{tracks[0][2]}" width="{tx1 - tx0}" height="{th}" fill="#16111f"/>{vis}
<rect x="{tx0}" y="{tracks[1][2]}" width="{tx1 - tx0}" height="{th}" fill="#16111f"/>
<g class="wave" stroke="{CYAN}" stroke-width="1.6" stroke-linecap="round">{aud}</g>
<rect x="{tx0}" y="{tracks[2][2]}" width="{tx1 - tx0}" height="{th}" fill="url(#heat)"/>
{clues}
<g class="ph">
<line x1="{tx0}" y1="84" x2="{tx0}" y2="168" stroke="{YEL}" stroke-width="1.6"/>
<path d="M{tx0 - 5},80 h10 v4 l-5,5 l-5,-5 z" fill="{YEL}"/>
</g>
{moon}
<text x="16" y="{H - 10}" font-family="{MONO}" font-size="9" fill="#fff6ea" opacity=".45" letter-spacing="1.6">◂◂  ▶  ▸▸   SPEED 1.0x   ·   SCAN MODE: ON</text>
<rect width="{W}" height="{H}" fill="url(#scan)"/>
</g>
<path d="M0,0 H{W - 22} L{W},22 V{H} H22 L0,{H - 22} Z" fill="none" stroke="{CYAN}" stroke-opacity=".45" stroke-width="2"/>
</svg>'''


def build_readme(c):
    readings = escape('; '.join(r['label'] + ': ' + r['value'] for r in c['readings']))
    return f'''<p align="center">
  <img src="./assets/header.svg" width="100%" alt="{escape(c['name'])}: netrunner bounty poster. Wanted for crimes against prod. Reward: {escape(c['reward'])}.">
</p>

<p align="center">
  <img src="./assets/braindance.svg" width="100%" alt="Braindance editor timeline. Clues: {readings}">
</p>

<p align="center"><sub><code>// END OF TRANSMISSION</code> · jack into the repos below ↓</sub></p>
'''


if __name__ == "__main__":
    out = Path(__file__).parent
    (out / "assets").mkdir(exist_ok=True)
    (out / "assets" / "header.svg").write_text(build_header(CONFIG), encoding="utf-8")
    (out / "assets" / "braindance.svg").write_text(build_braindance(CONFIG), encoding="utf-8")
    (out / "README.md").write_text(build_readme(CONFIG), encoding="utf-8")
    print("wrote README.md, assets/header.svg, assets/braindance.svg")
