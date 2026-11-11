"""
STRATA — a GitHub profile README drawn as a geological survey of you.

Edit CONFIG below, then run:   python build.py
It writes README.md + assets/strata.svg + assets/seismograph.svg.
Copy all three into your <username>/<username> repo and push.
"""
import datetime
import json
import math
import os
import subprocess
import urllib.request
import random
from html import escape
from pathlib import Path

# ─────────────────────────────── EDIT ME ────────────────────────────────
CONFIG = {
    "username": "nocashflow",             # GitHub handle, no @
    "name": "nocashflow",
    "tagline": "ships first, reads the docs later",
    "location": "location: classified",   # shown along the bottom edge
    "coords": "LAT ??.??° · LON ??.??°",

    # Top layer first. Each layer is one thing you're made of, with one fossil.
    # fossil kinds: ammonite, trilobite, fern, bone, crystal
    "layers": [
        {"years": "right now", "title": "Topsoil — whatever I shipped today",
         "stack": "commits named 'fix', 'fix 2', 'ok actually fix'",
         "fossil": "ammonite", "project": "main branch"},
        {"years": "last week", "title": "Clay — learning by breaking things",
         "stack": "console.log · try/catch · prayer",
         "fossil": "trilobite", "project": "deprecated-api"},
        {"years": "last month", "title": "Sandstone — 47 browser tabs of docs",
         "stack": "MDN · Stack Overflow · asking Claude",
         "fossil": "fern", "project": "open-tabs"},
        {"years": "the tutorial era", "title": "Shale — node_modules, fully fossilized",
         "stack": "1.2 GB of dependencies · 0 regrets",
         "fossil": "bone", "project": "left-pad"},
        {"years": "the beginning", "title": "Bedrock — the first `hello, world`",
         "stack": "curiosity · stubbornness · caffeine",
         "fossil": "crystal", "project": "hello-world"},
    ],
    "core": "“I'll take you to the moon.”",
    "core_sub": "— David Martinez. The moon is prod. The rocket is a Friday deploy.",

    # Spikes on the seismograph. magnitude 1–9 sets spike height.
    # Keep values under ~22 characters (the last one can go to ~28).
    "readings": [
        {"label": "currently learning", "value": "whatever breaks next", "magnitude": 5.1},
        {"label": "open to", "value": "positive cash flow", "magnitude": 7.4},
        {"label": "ask me about", "value": "my 47 unfinished repos", "magnitude": 4.3},
        {"label": "fun fact", "value": "my code works. no idea why", "magnitude": 6.2},
    ],

    # Specimen catalogue rows (project links table).
    "specimens": [
        {"name": "context-meter", "repo": "nocashflow/context-meter",
         "what": "See your Claude Code context, plan limits and cost as a band above the prompt or a side panel."},
        {"name": "next-big-thing", "repo": "nocashflow",
         "what": "Not started yet. The README is incredible though."},
    ],

    "contact": [  # label, url, shields.io logo name
        ("Follow on GitHub", "https://github.com/nocashflow", "github"),
        ("context-meter", "https://github.com/nocashflow/context-meter", "anthropic"),
    ],
    "show_stats": True,  # adds GitHub stats cards themed to match
}
# ────────────────────────────────────────────────────────────────────────

W = 840
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SERIF = "Georgia, 'Times New Roman', serif"

STRATA_STYLE = [  # base, texture ink, text ink, pattern
    ("#3a2a1f", "#5a4331", "#f3e6d3", "dots"),
    ("#8b4a2b", "#a65f3b", "#fbeee0", "dash"),
    ("#c38d50", "#a8743d", "#2b1d10", "pebble"),
    ("#59616d", "#6d7683", "#eef1f5", "shale"),
    ("#bdb59d", "#a59d84", "#2a261c", "brick"),
]


def wave(y, amp, seed):
    rnd = random.Random(seed)
    p1, p2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
    f1, f2 = rnd.uniform(0.006, 0.011), rnd.uniform(0.018, 0.03)
    return [(x, y + amp * math.sin(x * f1 + p1) + amp * 0.4 * math.sin(x * f2 + p2))
            for x in range(0, W + 1, 12)]


def pts(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def fossil(kind, cx, cy, ink):
    s = f'stroke="{ink}" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "ammonite":
        sp = []
        for i in range(0, 260):
            t = i / 260 * 4.2 * math.pi
            r = 1.2 + 2.0 * t
            sp.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        ribs = ""
        for i in range(40, 260, 9):
            t = i / 260 * 4.2 * math.pi
            r1, r2 = 1.2 + 2.0 * t, 1.2 + 2.0 * (t - 2 * math.pi)
            if r2 > 0:
                ribs += (f'<line x1="{cx + r1 * math.cos(t):.1f}" y1="{cy + r1 * math.sin(t):.1f}" '
                         f'x2="{cx + max(r2, 0) * math.cos(t):.1f}" y2="{cy + max(r2, 0) * math.sin(t):.1f}" opacity=".55"/>')
        return f'<g {s}><polyline points="{pts(sp)}"/>{ribs}</g>'
    if kind == "trilobite":
        g = f'<ellipse cx="{cx}" cy="{cy}" rx="13" ry="19"/>'
        g += f'<path d="M{cx-13},{cy-8} Q{cx},{cy-30} {cx+13},{cy-8}"/>'
        g += f'<line x1="{cx-5}" y1="{cy-14}" x2="{cx-5}" y2="{cy+17}" opacity=".6"/>'
        g += f'<line x1="{cx+5}" y1="{cy-14}" x2="{cx+5}" y2="{cy+17}" opacity=".6"/>'
        for k in range(-8, 16, 4):
            w = 13 * math.sqrt(max(0, 1 - (k / 19) ** 2))
            g += f'<line x1="{cx-w:.1f}" y1="{cy+k}" x2="{cx+w:.1f}" y2="{cy+k}" opacity=".7"/>'
        return f'<g {s}>{g}</g>'
    if kind == "fern":
        g = f'<path d="M{cx-4},{cy+22} Q{cx+2},{cy} {cx-2},{cy-22}"/>'
        for k in range(8):
            yy = cy + 18 - k * 5.2
            L = 14 - k * 1.3
            g += f'<path d="M{cx-1},{yy} q{-L*0.6},{-3} {-L},{-1}" opacity=".85"/>'
            g += f'<path d="M{cx},{yy-2} q{L*0.6},{-3} {L},{-1}" opacity=".85"/>'
        return f'<g {s}>{g}</g>'
    if kind == "bone":
        d = (f"M{cx-18},{cy-4} a5,5 0 1 1 6,-5 L{cx+12},{cy+1} a5,5 0 1 1 6,5 "
             f"a5,5 0 1 1 -6,5 L{cx-12},{cy+3} a5,5 0 1 1 -6,-7 z")
        return f'<g {s} transform="rotate(-24 {cx} {cy})"><path d="{d}"/></g>'
    # crystal / geode
    g = f'<ellipse cx="{cx}" cy="{cy}" rx="20" ry="15"/>'
    for a in range(0, 360, 30):
        r = math.radians(a)
        g += (f'<polyline points="{cx+19*math.cos(r):.1f},{cy+14*math.sin(r):.1f} '
              f'{cx+8*math.cos(r+0.25):.1f},{cy+6*math.sin(r+0.25):.1f} '
              f'{cx+9*math.cos(r-0.2):.1f},{cy+7*math.sin(r-0.2):.1f}" opacity=".8"/>')
    return f'<g {s}>{g}</g>'


def patterns():
    out = []
    for i, (base, tex, _, kind) in enumerate(STRATA_STYLE):
        pid = f"p{i}"
        if kind == "dots":
            body = (f'<circle cx="3" cy="4" r="1.1" fill="{tex}"/><circle cx="11" cy="10" r="0.9" fill="{tex}"/>'
                    f'<circle cx="15" cy="2" r="0.7" fill="{tex}"/>')
            size = 18
        elif kind == "dash":
            body = (f'<line x1="2" y1="5" x2="12" y2="5" stroke="{tex}" stroke-width="1.2"/>'
                    f'<line x1="14" y1="13" x2="22" y2="13" stroke="{tex}" stroke-width="1.2"/>')
            size = 24
        elif kind == "pebble":
            body = (f'<ellipse cx="6" cy="6" rx="3" ry="2" fill="none" stroke="{tex}" stroke-width="1"/>'
                    f'<ellipse cx="18" cy="16" rx="2.2" ry="1.5" fill="none" stroke="{tex}" stroke-width="1"/>'
                    f'<circle cx="20" cy="4" r=".8" fill="{tex}"/>')
            size = 24
        elif kind == "shale":
            body = (f'<line x1="0" y1="4" x2="30" y2="4" stroke="{tex}" stroke-width=".8"/>'
                    f'<line x1="6" y1="10" x2="26" y2="10" stroke="{tex}" stroke-width=".8"/>')
            size = 30
        else:  # brick
            body = (f'<path d="M0,0 H32 M0,12 H32 M10,0 V12 M26,12 V24" stroke="{tex}" stroke-width="1" fill="none"/>')
            size = 32 if kind == "brick" else 24
        h = 24 if kind == "brick" else size
        out.append(f'<pattern id="{pid}" width="{size}" height="{h}" patternUnits="userSpaceOnUse">'
                   f'<rect width="{size}" height="{h}" fill="{base}"/>{body}</pattern>')
    return "".join(out)


def build_strata(c):
    sky_h, layer_h, core_h = 168, 92, 142
    layers = c["layers"][:5]
    H = sky_h + layer_h * len(layers) + core_h
    surface = sky_h
    bore_x = 132
    drill_end = H - core_h + 46
    drill_dur, drill_delay = 5.2, 0.6

    def delay_at(y):
        return drill_delay + drill_dur * (y - surface) / (drill_end - surface)

    rnd = random.Random(7)
    stars = "".join(
        f'<circle class="tw" cx="{rnd.uniform(10, W-10):.0f}" cy="{rnd.uniform(8, sky_h-50):.0f}" '
        f'r="{rnd.choice([0.7, 0.9, 1.2])}" fill="#fff4dc" style="animation-delay:{rnd.uniform(0, 4):.2f}s"/>'
        for _ in range(46))

    # boundaries
    bounds = [wave(surface, 4, 1)]
    for i in range(1, len(layers) + 1):
        bounds.append(wave(surface + layer_h * i, 7, i * 13))

    body = []
    for i, L in enumerate(layers):
        top, bot = bounds[i], bounds[i + 1]
        base, tex, ink, _ = STRATA_STYLE[i]
        poly = top + list(reversed(bot))
        body.append(f'<polygon points="{pts(poly)}" fill="url(#p{i})"/>')
        body.append(f'<polyline points="{pts(bot)}" fill="none" stroke="#000" stroke-opacity=".28" stroke-width="1.2"/>')
        y0 = surface + layer_h * i
        mid = y0 + layer_h / 2
        d = delay_at(mid)
        n = f"{i+1:02d}"
        body.append(
            f'<g class="fade" style="animation-delay:{d:.2f}s">'
            f'{fossil(L["fossil"], 232, mid - 6, ink)}'
            f'<text x="232" y="{mid + 34:.0f}" text-anchor="middle" font-family="{MONO}" font-size="9.5" '
            f'fill="{ink}" opacity=".85" letter-spacing=".5">{escape(L["project"])}</text>'
            f'<text x="310" y="{mid - 18:.0f}" font-family="{MONO}" font-size="10" fill="{ink}" opacity=".7" '
            f'letter-spacing="2.2">STRATUM {n} · {escape(L["years"]).upper()}</text>'
            f'<text x="310" y="{mid + 4:.0f}" font-family="{SERIF}" font-size="19" fill="{ink}">{escape(L["title"])}</text>'
            f'<text x="310" y="{mid + 25:.0f}" font-family="{MONO}" font-size="11.5" fill="{ink}" opacity=".82">'
            f'{escape(L["stack"])}</text></g>')
        # depth ruler
        body.append(f'<line x1="0" y1="{y0}" x2="22" y2="{y0}" stroke="#fff" stroke-opacity=".5"/>'
                    f'<text x="28" y="{y0 + 4}" font-family="{MONO}" font-size="9" fill="{ink}" opacity=".65">'
                    f'{i * 120}m</text>')
        for t in range(1, 4):
            yy = y0 + t * layer_h / 4
            body.append(f'<line x1="0" y1="{yy:.0f}" x2="10" y2="{yy:.0f}" stroke="#fff" stroke-opacity=".3"/>')

    # grass along the surface
    grass = "".join(
        f'<line x1="{x}" y1="{y:.1f}" x2="{x + rnd.uniform(-2, 2):.1f}" y2="{y - rnd.uniform(3, 8):.1f}" '
        f'stroke="#6f8a3e" stroke-width="1.3" stroke-linecap="round"/>'
        for x, y in [(xx, bounds[0][min(len(bounds[0]) - 1, xx // 12)][1]) for xx in range(2, W, 5)])

    core_top = bounds[-1]
    core_poly = core_top + [(W, H), (0, H)]
    core_y = H - core_h

    stamp_x, stamp_y = 742, 78
    username = escape(c["username"])

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Geological survey of {escape(c['name'])}">
<style>
.tw{{animation:tw 3.4s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
.fade{{opacity:0;animation:fade .9s ease-out forwards}}
@keyframes fade{{from{{opacity:0;transform:translateX(-6px)}}to{{opacity:1;transform:none}}}}
.bore{{stroke-dasharray:{drill_end - surface};stroke-dashoffset:{drill_end - surface};animation:bore {drill_dur}s cubic-bezier(.45,.05,.55,.95) {drill_delay}s forwards}}
@keyframes bore{{to{{stroke-dashoffset:0}}}}
.bit{{animation:bit {drill_dur}s cubic-bezier(.45,.05,.55,.95) {drill_delay}s forwards}}
@keyframes bit{{to{{transform:translateY({drill_end - surface}px)}}}}
.shake{{animation:shake .09s linear infinite alternate}}
@keyframes shake{{from{{transform:translateX(-.8px)}}to{{transform:translateX(.8px)}}}}
.glow{{animation:glow 3.2s ease-in-out infinite}}
@keyframes glow{{0%,100%{{opacity:.35}}50%{{opacity:.85}}}}
.blob{{animation:blob 7s ease-in-out infinite alternate}}
@keyframes blob{{to{{transform:translate(18px,-6px) scale(1.15)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.fade{{opacity:1}}.bore{{stroke-dashoffset:0}}.bit{{transform:translateY({drill_end - surface}px)}}}}
</style>
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#0e1626"/><stop offset=".55" stop-color="#2a3150"/><stop offset="1" stop-color="#b8735a"/>
</linearGradient>
<radialGradient id="magma" cx=".5" cy="1" r=".9">
<stop offset="0" stop-color="#ffd27a"/><stop offset=".35" stop-color="#ff7a2e"/><stop offset=".75" stop-color="#b8240f"/><stop offset="1" stop-color="#5a1208"/>
</radialGradient>
<radialGradient id="hot" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff0b0"/><stop offset="1" stop-color="#ff8a3d" stop-opacity="0"/></radialGradient>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
{patterns()}
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{sky_h + 10}" fill="url(#sky)"/>
{stars}
<text x="310" y="54" font-family="{MONO}" font-size="10.5" fill="#e9d7bd" opacity=".75" letter-spacing="3.2">GEOLOGICAL SURVEY OF</text>
<text x="308" y="98" font-family="{SERIF}" font-size="44" font-style="italic" fill="#fff4e2">{escape(c['name'])}</text>
<text x="310" y="124" font-family="{MONO}" font-size="12.5" fill="#f1dcc2" opacity=".9">@{username} — {escape(c['tagline'])}</text>

<g transform="translate({stamp_x} {stamp_y}) rotate(-12)" opacity=".8">
<circle r="46" fill="none" stroke="#f1dcc2" stroke-width="1.4"/>
<circle r="40" fill="none" stroke="#f1dcc2" stroke-width=".6" stroke-dasharray="2 3"/>
<text y="-14" text-anchor="middle" font-family="{MONO}" font-size="8" fill="#f1dcc2" letter-spacing="2">SHEET Nº</text>
<text y="8" text-anchor="middle" font-family="{SERIF}" font-size="22" fill="#fff4e2">001</text>
<text y="22" text-anchor="middle" font-family="{MONO}" font-size="7" fill="#f1dcc2" letter-spacing="1.5">SURVEYED</text>
<text y="31" text-anchor="middle" font-family="{MONO}" font-size="7" fill="#f1dcc2" letter-spacing="1.5">2026</text>
</g>

<!-- derrick -->
<g stroke="#e6cfae" stroke-width="1.6" fill="none" stroke-linecap="round">
<path d="M{bore_x-22},{surface} L{bore_x},{surface-78} L{bore_x+22},{surface}"/>
<path d="M{bore_x-16},{surface-22} H{bore_x+16} M{bore_x-10},{surface-45} H{bore_x+10} M{bore_x-17},{surface-22} L{bore_x+10},{surface-45} M{bore_x+17},{surface-22} L{bore_x-10},{surface-45}"/>
<path d="M{bore_x-6},{surface-78} H{bore_x+6}"/>
</g>
<circle cx="{bore_x}" cy="{surface-81}" r="2.4" fill="#ffb35a" class="glow"/>

{"".join(body)}

<polygon points="{pts(core_poly)}" fill="url(#magma)"/>
<ellipse class="blob" cx="300" cy="{H - 30}" rx="120" ry="40" fill="url(#hot)" opacity=".5"/>
<ellipse class="blob" cx="640" cy="{H - 20}" rx="150" ry="44" fill="url(#hot)" opacity=".45" style="animation-delay:-3s"/>
<rect class="glow" x="0" y="{core_y - 10}" width="{W}" height="{core_h + 10}" fill="#ff9a4a" opacity=".4" style="mix-blend-mode:screen"/>
<g class="fade" style="animation-delay:{drill_delay + drill_dur:.2f}s">
<text x="310" y="{core_y + 44}" font-family="{MONO}" font-size="10" fill="#fff1d6" letter-spacing="3">THE CORE · WHAT KEEPS ME MOLTEN</text>
<text x="310" y="{core_y + 74}" font-family="{SERIF}" font-size="21" font-style="italic" fill="#fffaf0">{escape(c['core'])}</text>
<text x="310" y="{core_y + 98}" font-family="{MONO}" font-size="11.5" fill="#fff1d6" opacity=".88">{escape(c.get('core_sub', ''))}</text>
</g>

<line class="bore" x1="{bore_x}" y1="{surface}" x2="{bore_x}" y2="{drill_end}" stroke="#f6e7cf" stroke-width="2.2" stroke-dasharray="4 3"/>
<g class="bit"><g class="shake">
<line x1="{bore_x}" y1="{surface - 40}" x2="{bore_x}" y2="{surface - 6}" stroke="#d9c4a2" stroke-width="2"/>
<path d="M{bore_x-6},{surface-8} L{bore_x+6},{surface-8} L{bore_x},{surface+6} Z" fill="#f2d39a" stroke="#3a2a1f" stroke-width=".8"/>
</g></g>

<polyline points="{pts(bounds[0])}" fill="none" stroke="#1e150f" stroke-width="1.6"/>
{grass}
<text x="{W - 16}" y="{H - 14}" text-anchor="end" font-family="{MONO}" font-size="8.5" fill="#ffe2b8" opacity=".7" letter-spacing="1.5">{escape(c['coords'])} · {escape(c['location']).upper()}</text>
</g>
</svg>'''
    return svg


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
    u = c["username"]
    rows = "\n".join(
        f"| `Nº {i+1:02d}` | [**{escape(s['name'])}**](https://github.com/{s['repo']}) | {escape(s['what'])} |"
        for i, s in enumerate(c["specimens"]))
    badges = " ".join(
        f'<a href="{url}"><img src="https://img.shields.io/badge/{label.replace("-", "--").replace(" ", "_")}-2a1d12?style=for-the-badge&logo={logo}&logoColor=f1dcc2&labelColor=8b4a2b" alt="{label}"></a>'
        for label, url, logo in c["contact"])
    stats = ""
    if c["show_stats"] and (Path(__file__).parent / "assets" / "lab.svg").exists():
        stats = '''
<br>

<p align="center">
  <img src="./assets/lab.svg" width="100%" alt="Lab report: GitHub contributions, repos, stars, followers and language mix. Refreshed daily by a GitHub Action.">
</p>
'''
    return f'''<p align="center">
  <img src="./assets/strata.svg" width="100%" alt="A geological cross-section of {escape(c['name'])}: each rock layer is a year of work, each fossil a project, a drill bores down to the core.">
</p>

<p align="center"><sub><code>FIELD NOTE</code> &nbsp;·&nbsp; You're looking at a core sample. The newest work sits on top, the oldest is bedrock, and the fossils are projects that survived. Read it top to bottom, the way a geologist would.</sub></p>

<br>

### ⛏&nbsp; Specimen catalogue

| Nº | Specimen | Field description |
|:--:|:--|:--|
{rows}

<br>

<p align="center">
  <img src="./assets/seismograph.svg" width="100%" alt="Seismograph readings: {escape('; '.join(r['label'] + ': ' + r['value'] for r in c['readings']))}">
</p>

### ◉&nbsp; Signal the surface team

<p>
{badges}
</p>
{stats}
<p align="right"><sub>Survey ends here. Everything below this line is unexplored.</sub></p>
'''


def _token():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        return tok
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=15).stdout.strip() or None
    except Exception:
        return None


def fetch_stats(username):
    """Public numbers for the lab card, via GitHub GraphQL. Returns None if offline / no token."""
    tok = _token()
    if not tok:
        return None
    q = """query($u:String!){user(login:$u){
      followers{totalCount}
      contributionsCollection{contributionCalendar{totalContributions}}
      repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){
        totalCount nodes{stargazerCount languages(first:10){edges{size node{name color}}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": {"u": username}}).encode(),
        headers={"Authorization": f"bearer {tok}", "User-Agent": "strata-readme"})
    try:
        data = json.load(urllib.request.urlopen(req, timeout=30))["data"]["user"]
    except Exception as e:
        print("stats fetch failed:", e)
        return None
    langs = {}
    for r in data["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            langs.setdefault(n, [0, e["node"]["color"] or "#8b8b8b"])[0] += e["size"]
    return {
        "contrib": data["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "repos": data["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in data["repositories"]["nodes"]),
        "followers": data["followers"]["totalCount"],
        "langs": sorted(langs.items(), key=lambda kv: -kv[1][0]),
    }


def build_lab(c, s):
    H = 236
    year = datetime.date.today().year
    cells = [(f"{s['contrib']:,}", f"contributions · {year}"), (str(s["repos"]), "public repos"),
             (str(s["stars"]), "stars collected"), (str(s["followers"]), "followers")]
    nums = ""
    for i, (v, lab) in enumerate(cells):
        x = 40 + i * 200
        nums += (f'<g class="fade" style="animation-delay:{.2 + i * .15:.2f}s">'
                 f'<text x="{x}" y="102" font-family="{SERIF}" font-size="40" fill="#ffb35a">{escape(v)}</text>'
                 f'<text x="{x + 2}" y="124" font-family="{MONO}" font-size="10" fill="#f1dcc2" opacity=".7" letter-spacing="1.6">{escape(lab).upper()}</text></g>')
        if i:
            nums += f'<line x1="{x - 22}" y1="66" x2="{x - 22}" y2="126" stroke="#f1dcc2" stroke-opacity=".12"/>'

    top = s["langs"][:6]
    other = sum(v[0] for _, v in s["langs"][6:])
    if other:
        top.append(("Other", [other, "#6b5a4a"]))
    total = sum(v[0] for _, v in top) or 1
    bx, bw, by = 40, W - 80, 162
    bar, legend, x = "", "", bx
    lx = bx
    for i, (name, (size, color)) in enumerate(top):
        w = bw * size / total
        bar += f'<rect x="{x:.1f}" y="{by}" width="{max(w - 2, 1):.1f}" height="12" fill="{color}"/>'
        x += w
        pct = f"{100 * size / total:.1f}%"
        label = f"{name} {pct}"
        legend += (f'<circle cx="{lx + 4}" cy="{by + 37}" r="4" fill="{color}"/>'
                   f'<text x="{lx + 13}" y="{by + 41}" font-family="{MONO}" font-size="10.5" fill="#f1dcc2">{escape(name)} '
                   f'<tspan opacity=".55">{pct}</tspan></text>')
        lx += 28 + len(label) * 6.6
    if not top:
        bar = f'<text x="{bx}" y="{by + 10}" font-family="{MONO}" font-size="11" fill="#f1dcc2" opacity=".6">no samples yet. go push something.</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Lab report: GitHub stats for @{escape(c['username'])}">
<style>
.fade{{opacity:0;animation:fade .7s ease-out forwards}}
@keyframes fade{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:none}}}}
.grow{{transform-origin:{bx}px 0;transform:scaleX(0);animation:grow 1.4s cubic-bezier(.2,.7,.2,1) .6s forwards}}
@keyframes grow{{to{{transform:scaleX(1)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.fade{{opacity:1}}.grow{{transform:none}}}}
</style>
<defs><clipPath id="f"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="12" rx="6"/></clipPath></defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="#1f1610"/>
<rect width="{W}" height="30" fill="#2e2018"/>
<text x="20" y="19" font-family="{MONO}" font-size="10" fill="#f1dcc2" letter-spacing="2.4">LAB REPORT · CORE SAMPLE ANALYSIS · @{escape(c['username']).upper()}</text>
<text x="{W - 20}" y="19" text-anchor="end" font-family="{MONO}" font-size="10" fill="#f1dcc2" opacity=".55" letter-spacing="2">ANALYSED {datetime.date.today().isoformat()}</text>
{nums}
<text x="{bx}" y="{by - 12}" font-family="{MONO}" font-size="10" fill="#f1dcc2" opacity=".7" letter-spacing="2.4">MINERAL COMPOSITION</text>
<g clip-path="url(#bar)"><rect x="{bx}" y="{by}" width="{bw}" height="12" fill="#3a2a1f"/><g class="grow">{bar}</g></g>
<g class="fade" style="animation-delay:1.4s">{legend}</g>
</g>
</svg>'''


if __name__ == "__main__":
    out = Path(__file__).parent
    (out / "assets").mkdir(exist_ok=True)
    (out / "assets" / "strata.svg").write_text(build_strata(CONFIG), encoding="utf-8")
    (out / "assets" / "seismograph.svg").write_text(build_seismo(CONFIG), encoding="utf-8")
    if CONFIG["show_stats"]:
        stats = fetch_stats(CONFIG["username"])
        if stats:  # if the fetch fails, keep the last good lab.svg
            (out / "assets" / "lab.svg").write_text(build_lab(CONFIG, stats), encoding="utf-8")
    (out / "README.md").write_text(build_readme(CONFIG), encoding="utf-8")
    print("wrote README.md and assets/")
