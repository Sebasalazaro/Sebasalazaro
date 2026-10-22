"""Generate the light and dark variants of every SVG used in the profile README.

Each asset is written twice (`*-dark.svg` / `*-light.svg`) from one template, and the
README picks the right one with <picture> + prefers-color-scheme, which GitHub ties to
the viewer's GitHub theme. Everything is static on purpose, except the blinking cursor in the banner.

    python scripts/build_svgs.py
"""

import re
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# navy + light blues, grays and purples
PALETTES = {
    "dark": {
        "panel": "#0b1220",
        "panel2": "#111b2e",
        "border": "#22304a",
        "text": "#e3e9f5",
        "muted": "#8391a8",
        "dim": "#3a4862",
        "blue": "#7cc0ff",
        "purple": "#b49cff",
        "lavender": "#d4c8ff",
        "chip": "#16233b",
    },
    "light": {
        "panel": "#f6f8fd",
        "panel2": "#eef2fa",
        "border": "#d3dcec",
        "text": "#14213d",
        "muted": "#5c6880",
        "dim": "#b9c4d8",
        "blue": "#1f62c4",
        "purple": "#6b47d6",
        "lavender": "#4b3a9a",
        "chip": "#e4eaf6",
    },
}

MONO = "'JetBrains Mono','SF Mono','Cascadia Code',Consolas,Menlo,'DejaVu Sans Mono',monospace"


def edge_gradient(p):
    return (f'<linearGradient id="edge" x1="0" x2="1">'
            f'<stop offset="0" stop-color="{p["blue"]}"/><stop offset="1" stop-color="{p["purple"]}"/>'
            f'</linearGradient>')


def banner(p):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 250" width="880" height="250" role="img" aria-label="shiki@OS terminal: ./getProfile --user shiki. Welcome, I'm Sebastian. Security engineer with a developer's brain.">
  <defs>
    <clipPath id="win"><rect x="1" y="1" width="878" height="248" rx="14"/></clipPath>
    <style>
      text {{ font-family: {MONO}; }}
      .title {{ font-size: 12px; fill: {p['muted']}; }}
      .cmd {{ font-size: 15px; }}
      .big {{ font-size: 28px; font-weight: 700; fill: {p['text']}; }}
      .sub {{ font-size: 17px; fill: {p['blue']}; }}
      .tags {{ font-size: 12px; fill: {p['muted']}; letter-spacing: 1.5px; }}
      .ready {{ font-size: 15px; fill: {p['lavender']}; }}
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
    </style>
  </defs>

  <g clip-path="url(#win)">
    <rect width="880" height="250" fill="{p['panel']}"/>
    <rect width="880" height="34" fill="{p['panel2']}"/>
  </g>
  <rect x="1" y="1" width="878" height="248" rx="14" fill="none" stroke="{p['border']}"/>

  <circle cx="24" cy="18" r="6" fill="#ff5f57"/>
  <circle cx="44" cy="18" r="6" fill="#febc2e"/>
  <circle cx="64" cy="18" r="6" fill="#28c840"/>
  <text class="title" x="440" y="22" text-anchor="middle">shiki@OS: ~ GitHub Terminal</text>

  <text class="cmd" x="36" y="80"><tspan fill="{p['purple']}">shiki@OS</tspan><tspan fill="{p['muted']}">:</tspan><tspan fill="{p['blue']}">~</tspan><tspan fill="{p['muted']}">$ </tspan><tspan fill="{p['text']}" font-weight="700">./getProfile</tspan><tspan fill="{p['muted']}"> --user </tspan><tspan fill="{p['blue']}">shiki</tspan></text>
  <text class="big" x="36" y="126">Welcome, I'm Sebastian.</text>
  <text class="sub" x="36" y="160">security engineer with a developer's brain</text>
  <text class="tags" x="36" y="192">PENTESTING · FULL-STACK · AI SYSTEMS · COLOMBIA</text>
  <text class="ready" x="36" y="224">ready? (y/n)</text>
  <rect class="cursor" x="148" y="211" width="9" height="16" fill="{p['lavender']}"/>
</svg>
"""


WHOAMI = '''shiki = {
    "name":    "Sebastian Salazar",
    "role":    "Cybersecurity Engineer @Exfil",
    "focus":   ["Web & API Pentesting",
                "AI Systems", "Full-Stack"],
    "mindset": "Make people feel good with the stuff I build!",
    "afk":     ["Anime", "Gacha", "Movies", "Fantasy Worlds"],
}'''

# The whoami card and the GIF sit side by side with the same height. The GIF is 640x360,
# so the README widths are derived from these numbers (see WHOAMI_* below).
WHOAMI_W, WHOAMI_H, WHOAMI_GAP = 682, 256, 16


def highlight(line, p):
    out = []
    parts = re.split(r'("[^"]*")', line)
    for i, part in enumerate(parts):
        if not part:
            continue
        if part.startswith('"'):
            is_key = i + 1 < len(parts) and parts[i + 1].startswith(":")
            out.append(f'<tspan fill="{p["purple"] if is_key else p["blue"]}">{escape(part)}</tspan>')
        else:
            colored = re.sub(r"\bshiki\b", f'</tspan><tspan fill="{p["text"]}">shiki</tspan><tspan fill="{p["muted"]}">',
                             escape(part))
            out.append(f'<tspan fill="{p["muted"]}">{colored}</tspan>')
    return "".join(out)


def whoami(p):
    lines = WHOAMI.split("\n")
    lh = 27
    top = (WHOAMI_H - lh * (len(lines) - 1)) / 2 + 5
    body = "\n  ".join(
        f'<text x="28" y="{top + i * lh:.0f}" xml:space="preserve">{highlight(line, p)}</text>'
        for i, line in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WHOAMI_W + WHOAMI_GAP} {WHOAMI_H}" width="{WHOAMI_W + WHOAMI_GAP}" height="{WHOAMI_H}" role="img" aria-label="whoami: Sebastian Salazar, Cybersecurity Engineer at Exfil. Focus: web and API pentesting, AI systems, full-stack. Mindset: make people feel good with the stuff I build. AFK: anime, gacha, movies, fantasy worlds.">
  <defs>
    <style>text {{ font-family: {MONO}; font-size: 17px; white-space: pre; }}</style>
  </defs>
  <rect x=".5" y=".5" width="{WHOAMI_W - 1}" height="{WHOAMI_H - 1}" rx="12" fill="{p['panel']}" stroke="{p['border']}"/>
  {body}
</svg>
"""


# Cards carry their own transparent margin, so two side by side at 50% get breathing room
CARD_W, CARD_H, CARD_M = 430, 216, 12


def card(c, p):
    w, h, m = CARD_W, CARD_H, CARD_M
    # Wrap across the full card width and center the block between tagline and divider
    lines = textwrap.wrap(c["desc"], 50)
    first = (85 + h - 40) / 2 + 4 - (len(lines) - 1) * 10
    desc = "\n  ".join(
        f'<text class="desc" x="26" y="{first + i * 20:.0f}">{escape(line)}</text>' for i, line in enumerate(lines)
    )
    chip_w = len(c["badge"]) * 7.3 + 20
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 2 * m} {h + 2 * m}" width="{w + 2 * m}" height="{h + 2 * m}" role="img" aria-label="{escape(c['name'])}: {escape(c['tagline'])}">
  <defs>
    {edge_gradient(p)}
    <style>
      text {{ font-family: {MONO}; }}
      .kicker {{ font-size: 11px; fill: {p['muted']}; letter-spacing: 1.5px; }}
      .name {{ font-size: 20px; font-weight: 700; fill: {p['text']}; }}
      .tagline {{ font-size: 13px; fill: {p['blue']}; }}
      .desc {{ font-size: 12px; fill: {p['muted']}; }}
      .stack {{ font-size: 11px; fill: {p['purple']}; }}
      .badge {{ font-size: 11px; font-weight: 700; fill: {p['lavender']}; letter-spacing: .5px; }}
    </style>
  </defs>
  <g transform="translate({m} {m})">
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{p['panel']}" stroke="{p['border']}"/>
  <rect x="26" y="0" width="56" height="3" rx="1.5" fill="url(#edge)"/>

  <text class="kicker" x="26" y="34">{escape(c['kicker'])}</text>
  <text class="name" x="26" y="63">{escape(c['name'])}</text>
  <text class="tagline" x="26" y="85">{escape(c['tagline'])}</text>
  {desc}
  <line x1="26" y1="{h - 40}" x2="{w - 26}" y2="{h - 40}" stroke="{p['border']}"/>
  <text class="stack" x="26" y="{h - 18}">{escape(c['stack'])}</text>

  <rect x="{w - 26 - chip_w:.1f}" y="20" width="{chip_w:.1f}" height="22" rx="11" fill="{p['chip']}" stroke="{p['border']}"/>
  <text class="badge" x="{w - 26 - chip_w / 2:.1f}" y="35" text-anchor="middle">{escape(c['badge'])}</text>

  </g>
</svg>
"""


CARDS = [
    {
        "slug": "shirou-day", "kicker": "FANDOM · REALTIME", "badge": "LIVE",
        "name": "Shirou Day", "tagline": "shirouday.com ↗",
        "desc": "The community's archive for Shirou Day: every avi kept and credited, plus a live Sword Clicker synced for everyone online under heavy traffic.",
        "stack": "Next.js · Cloudflare Workers · D1 · R2",
    },
    {
        "slug": "redactor", "kicker": "SECURITY · TOOLING", "badge": "OPEN SOURCE",
        "name": "redactor", "tagline": "pentest traffic, safe for LLMs",
        "desc": "Sanitizes Burp, HAR and raw HTTP fully offline, keeping enough structure for the model to still reason about it.",
        "stack": "Rust · Tauri · Svelte · ONNX",
    },
    {
        "slug": "dnd-ai", "kicker": "GAME · TABLETOP", "badge": "EAFIT INVENTIVA WINNER",
        "name": "DnD-AI", "tagline": "an AI dungeon master",
        "desc": "Takes the heavy lifting off the Dungeon Master: AI-built story, maps and enemies, so friends anywhere can play a richer, more visual session.",
        "stack": "Django · Gemini · OpenAI · LangChain",
    },
    {
        "slug": "recocha", "kicker": "SOCIAL · SPORTS", "badge": "LIVE",
        "name": "Recocha", "tagline": "recocha.app ↗",
        "desc": "La polla del mundial entre amigos: World Cup 2026 pools with picks, brackets and live standings, shared over WhatsApp.",
        "stack": "Next.js · Supabase · Prisma · Mercado Pago",
    },
]


def main():
    (OUT / "cards").mkdir(parents=True, exist_ok=True)
    for mode, p in PALETTES.items():
        (OUT / f"banner-{mode}.svg").write_text(banner(p), encoding="utf-8")
        (OUT / f"whoami-{mode}.svg").write_text(whoami(p), encoding="utf-8")
        for c in CARDS:
            (OUT / "cards" / f"{c['slug']}-{mode}.svg").write_text(card(c, p), encoding="utf-8")

    # README widths that give the whoami card and the 640x360 GIF the same height
    a = (WHOAMI_W + WHOAMI_GAP) / WHOAMI_H
    g = 640 / 360
    print(f"ok  whoami width {100 * a / (a + g):.2f}%  gif width {100 * g / (a + g):.2f}%")


if __name__ == "__main__":
    main()
