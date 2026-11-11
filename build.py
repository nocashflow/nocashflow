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
    "role": "NETRUNNER · NOCORPO · UNLICENSED",

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
    """Braindance recording: one thin vitals trace that blips at each clue
    and climbs into the moon, where two tiny figures sit."""
    H = 236
    readings = c["readings"][:4]
    rnd = random.Random(2077)
    y0 = 126                                  # trace baseline
    mx, my, mr = 742, 128, 58                 # the moon
    cx = [86 + i * 122 for i in range(len(readings))]

    # build the trace as one polyline: flat, PQRST blip per clue, then a curve up into the moon
    trace = [(24, y0)]
    peaks = []
    for p, r in zip(cx, readings):
        amp = 14 + r["magnitude"] * 3.2
        for dx, dy in [(-16, 0), (-10, -4), (-6, 0), (-2, 6), (2, -amp), (6, 12), (10, 0), (18, -5), (24, 0)]:
            trace.append((p + dx, y0 + dy))
        peaks.append((p + 2, y0 - amp))
    trace.append((600, y0))
    ex, ey = mx - mr * math.cos(math.radians(22)), my + mr * math.sin(math.radians(22))
    p0, p1, p2, p3 = (600, y0), (636, y0), (648, ey), (ex, ey)
    for k in range(1, 21):
        t = k / 20
        trace.append(tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * cc + t ** 3 * d
                           for a, b, cc, d in zip(p0, p1, p2, p3)))
    L = sum(math.dist(a, b) for a, b in zip(trace, trace[1:]))
    tp = pts(trace)

    # clue labels, alternating above / below the trace
    clues = ""
    for i, ((px, py), r) in enumerate(zip(peaks, readings)):
        top = i % 2 == 0
        ly = 44 if top else 192
        lead_from, lead_to = (py - 4, 70) if top else (y0 + 16, 176)
        clues += (
            f'<line x1="{px}" y1="{lead_from:.0f}" x2="{px}" y2="{lead_to}" stroke="#fff6ea" stroke-opacity=".3" stroke-dasharray="2 3"/>'
            f'<circle cx="{px}" cy="{py:.0f}" r="2.4" fill="{YEL}" class="pulse" style="animation-delay:{i * .45:.2f}s"/>'
            f'<text x="{px - 4}" y="{ly}" font-family="{MONO}" font-size="8.5" fill="{CYAN}" letter-spacing="1.3" opacity=".85">'
            f'CLUE {i + 1:02d} · {escape(r["label"]).upper()}</text>'
            f'<text x="{px - 4}" y="{ly + 17}" font-family="{MONO}" font-size="12.5" font-weight="700" fill="#fff6ea">'
            f'{escape(r["value"])}</text>')

    # faint timecode ticks under the trace
    ticks = "".join(
        f'<line x1="{x}" y1="{y0 + 30}" x2="{x}" y2="{y0 + (36 if k % 5 == 0 else 33)}" stroke="#fff6ea" stroke-opacity="{.3 if k % 5 == 0 else .12}"/>'
        for k, x in enumerate(range(24, 600, 12)))

    # moon
    craters = "".join(f'<circle cx="{mx + dx}" cy="{my + dy}" r="{r}" fill="#c9c0ae" opacity=".45"/>'
                      for dx, dy, r in [(-20, -6, 10), (18, 14, 13), (-8, 30, 5), (26, -24, 5), (-34, 18, 4), (4, -2, 3)])
    # two tiny figures seen from behind, sitting on the rim
    seat = my - mr + 1
    legs = ''
    him = (f'<g transform="translate({mx - 6} {seat + .8}) rotate(-7) scale(1.7)">{legs}'
           f'<path d="M-2.7,-9.6 h5.4 l1.1,9.8 q-3.8,1 -7.6,0 z" fill="{YEL}"/>'
           f'<path d="M-2.7,-9.6 h5.4 l.15,1.4 h-5.7 z" fill="#c9b800"/>'
           f'<g fill="{PINK}" stroke="{PINK}" stroke-width="1" stroke-linejoin="round" opacity=".75"><circle cx="0" cy="-12.2" r="2.6"/><path d="M-2.9,-12.6 l.9,-3.1 l1.1,1.5 l.9,-2.3 l1,2 l1.2,-1.6 l.7,3.5 z"/></g>'
           f'<g fill="#241c30"><circle cx="0" cy="-12.2" r="2.6"/><path d="M-2.9,-12.6 l.9,-3.1 l1.1,1.5 l.9,-2.3 l1,2 l1.2,-1.6 l.7,3.5 z"/></g></g>')
    her = (f'<g transform="translate({mx + 6} {seat + .6}) rotate(8) scale(1.6)">{legs}'
           f'<path d="M-2.4,-9.4 h4.8 l1,9.6 q-3.4,.9 -6.8,0 z" fill="#1b1630"/>'
           f'<path d="M-.4,-9.4 h.8 v9.6 h-.8 z" fill="{CYAN}" opacity=".9"/>'
           f'<path d="M-3.3,-9.8 Q-3.8,-16 0,-15.6 Q3.8,-16 3.3,-9.8 Q0,-10.8 -3.3,-9.8 z" fill="#ece6ff"/></g>')
    moon = (f'<circle cx="{mx}" cy="{my}" r="{mr + 46}" fill="url(#halo)" class="breathe"/>'
            f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="url(#moonfill)"/>{craters}'
            f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="{PINK}" stroke-opacity=".35" stroke-width="1.5"/>'
            f'{him}{her}'
            f'<text x="{mx}" y="{my + mr + 24}" text-anchor="middle" font-family="{MONO}" font-size="8.5" fill="#fff6ea" '
            f'opacity=".6" letter-spacing="2">EOF · TO THE MOON</text>')

    stars = "".join(f'<circle cx="{rnd.uniform(20, W - 20):.0f}" cy="{rnd.uniform(36, H - 30):.0f}" r="{rnd.choice([.5, .7, .9])}" '
                    f'fill="#fff6ea" class="tw" style="animation-delay:{rnd.uniform(0, 3):.1f}s"/>' for _ in range(40))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Braindance recording: a vitals trace with four clues, ending at the moon">
<style>
.comet{{stroke-dasharray:70 {L:.0f};animation:comet 6s linear infinite}}
@keyframes comet{{from{{stroke-dashoffset:70}}to{{stroke-dashoffset:-{L:.0f}}}}}
.pulse{{animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
.rec{{animation:rec 1.2s steps(2) infinite}}
@keyframes rec{{50%{{opacity:.15}}}}
.tw{{animation:tw 3s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.8}}}}
.breathe{{animation:breathe 5s ease-in-out infinite;transform-origin:{mx}px {my}px}}
@keyframes breathe{{0%,100%{{opacity:.7;transform:scale(1)}}50%{{opacity:1;transform:scale(1.05)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.comet{{stroke-dasharray:none;opacity:0}}}}
</style>
<defs>
<clipPath id="f"><path d="M0,0 H{W - 22} L{W},22 V{H} H22 L0,{H - 22} Z"/></clipPath>
<radialGradient id="halo"><stop offset=".55" stop-color="{PINK}" stop-opacity=".22"/><stop offset=".8" stop-color="{PINK}" stop-opacity=".06"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
<radialGradient id="moonfill" cx=".38" cy=".35" r=".75"><stop offset="0" stop-color="#fffaf0"/><stop offset=".7" stop-color="#e8e0cf"/><stop offset="1" stop-color="#cfc4b0"/></radialGradient>
<linearGradient id="fadein" x1="24" y1="0" x2="600" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{CYAN}" stop-opacity=".15"/><stop offset=".12" stop-color="{CYAN}" stop-opacity=".8"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<filter id="glow" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="{BG}"/>
{stars}
<rect width="{W}" height="28" fill="#16111f"/>
<rect y="27" width="{W}" height="1" fill="{CYAN}" opacity=".35"/>
<circle class="rec" cx="20" cy="14" r="4" fill="{PINK}"/>
<text x="32" y="18" font-family="{MONO}" font-size="10" fill="{YEL}" letter-spacing="2">BD PLAYBACK · REC_{escape(c['username']).upper()}.bd</text>
<text x="{W - 16}" y="18" text-anchor="end" font-family="{MONO}" font-size="10" fill="#fff6ea" opacity=".55" letter-spacing="2">VITALS: STABLE-ISH · 4 CLUES</text>
{ticks}
{moon}
<polyline points="{tp}" fill="none" stroke="url(#fadein)" stroke-width="1.5" stroke-linejoin="round" opacity=".85"/>
<polyline class="comet" points="{tp}" fill="none" stroke="#e9fdff" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round" filter="url(#glow)"/>
{clues}
<text x="24" y="{H - 10}" font-family="{MONO}" font-size="9" fill="#fff6ea" opacity=".35" letter-spacing="1.6">◂◂  ▶  ▸▸   00:47:12   ·   SPEED 1.0x</text>
</g>
<path d="M0,0 H{W - 22} L{W},22 V{H} H22 L0,{H - 22} Z" fill="none" stroke="{CYAN}" stroke-opacity=".4" stroke-width="2"/>
</svg>'''


def build_readme(c):
    readings = escape('; '.join(r['label'] + ': ' + r['value'] for r in c['readings']))
    return f'''<p align="center">
  <img src="./assets/header.svg" width="100%" alt="{escape(c['name'])}: netrunner bounty poster. Wanted for crimes against prod. Reward: {escape(c['reward'])}.">
</p>

<p align="center">
  <img src="./assets/braindance.svg" width="100%" alt="Braindance recording ending at the moon. Clues: {readings}">
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
