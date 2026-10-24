#!/usr/bin/env python3
"""
Generate the AuraIcons icon theme (SVG).

Every application icon is a rounded-square ("squircle") tile with a blue-family
gradient and a bold white glyph — one consistent language across the whole OS.
Run:  python3 tools/generate_icons.py
Output is written into rootfs/usr/share/icons/AuraIcons/.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "rootfs", "usr", "share", "icons", "AuraIcons")

TILE = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c1}"/>
      <stop offset="1" stop-color="{c2}"/>
    </linearGradient>
    <clipPath id="sq"><rect x="6" y="6" width="244" height="244" rx="54"/></clipPath>
  </defs>
  <g clip-path="url(#sq)">
    <rect x="6" y="6" width="244" height="244" fill="url(#g)"/>
    <ellipse cx="128" cy="-30" rx="180" ry="110" fill="#ffffff" opacity="0.14"/>
  </g>
  <rect x="6" y="6" width="244" height="244" rx="54" fill="none" stroke="#ffffff" stroke-opacity="0.28" stroke-width="2"/>
  <g fill="#ffffff" stroke="#ffffff">
{glyph}
  </g>
</svg>
"""

W = 'fill="#ffffff" stroke="none"'
S = 'fill="none"'

# name -> (gradient_top, gradient_bottom, glyph_svg)
APPS = {
    "aura-finder": ("#1d6fe0", "#38b6f6", f"""
    <path {W} d="M44 92a10 10 0 0 1 10-10h52l14 16h82a10 10 0 0 1 10 10v84a10 10 0 0 1-10 10H54a10 10 0 0 1-10-10z" opacity="0.95"/>
    <path d="M70 176 L116 124 L144 152 L170 128 L198 176 Z" fill="#1d6fe0" stroke="none"/>"""),
    "celestia-shell": ("#0a1e46", "#14418f", f"""
    <rect x="40" y="56" width="176" height="144" rx="14" {S}/>
    <path {S} d="M74 102 L112 128 L74 154" stroke="#57d7ff"/>
    <path {S} d="M126 160 H182" stroke="#57d7ff"/>"""),
    "aura-browser": ("#0f5fd7", "#37c6f4", f"""
    <circle cx="128" cy="128" r="74" {S}/>
    <path {S} d="M54 128 H202 M128 54 C160 88 160 168 128 202 C96 168 96 88 128 54"/>"""),
    "aura-settings": ("#33507e", "#5b84c4", f"""
    <path {S} d="M64 92 H192 M64 128 H192 M64 164 H192"/>
    <circle cx="104" cy="92" r="14" {W}/><circle cx="156" cy="128" r="14" {W}/><circle cx="92" cy="164" r="14" {W}/>"""),
    "aura-appcenter": ("#7a4fe0", "#3f8fe0", f"""
    <rect x="58" y="58" width="60" height="60" rx="14" {W}/>
    <rect x="138" y="58" width="60" height="60" rx="30" {W} opacity="0.75"/>
    <rect x="58" y="138" width="60" height="60" rx="30" {W} opacity="0.75"/>
    <rect x="138" y="138" width="60" height="60" rx="14" {W}/>"""),
    "aura-text": ("#2f7fe0", "#63c7f2", f"""
    <rect x="68" y="44" width="120" height="168" rx="12" {W}/>
    <path d="M92 92 H164 M92 122 H164 M92 152 H136" stroke="#2f7fe0" stroke-width="12" stroke-linecap="round" fill="none"/>"""),
    "aura-studio": ("#12275e", "#2a6fd0", f"""
    <path {S} d="M98 84 L56 128 L98 172 M158 84 L200 128 L158 172" stroke="#6fe3ff"/>
    <path {S} d="M140 70 L116 186" stroke="#ffffff"/>"""),
    "aura-notes": ("#e0a83c", "#f2cd63", f"""
    <rect x="60" y="48" width="136" height="160" rx="12" {W}/>
    <rect x="60" y="48" width="136" height="34" rx="12" fill="#c78f22" stroke="none"/>
    <path d="M84 116 H172 M84 146 H172 M84 176 H140" stroke="#8a6a1f" stroke-width="11" stroke-linecap="round" fill="none"/>"""),
    "aura-calendar": ("#d6455b", "#f2768a", f"""
    <rect x="52" y="66" width="152" height="140" rx="14" {W}/>
    <rect x="52" y="66" width="152" height="40" rx="14" fill="#b03047" stroke="none"/>
    <path {S} d="M88 50 V84 M168 50 V84" stroke-width="14"/>
    <circle cx="92" cy="140" r="10" fill="#d6455b" stroke="none"/><circle cx="128" cy="140" r="10" fill="#d6455b" stroke="none" opacity="0.55"/>
    <circle cx="164" cy="140" r="10" fill="#d6455b" stroke="none" opacity="0.3"/><circle cx="92" cy="174" r="10" fill="#d6455b" stroke="none" opacity="0.3"/>
    <circle cx="128" cy="174" r="10" fill="#d6455b" stroke="none"/><circle cx="164" cy="174" r="10" fill="#d6455b" stroke="none" opacity="0.55"/>"""),
    "aura-calculator": ("#3a4a63", "#7086a8", f"""
    <rect x="66" y="44" width="124" height="168" rx="14" {W}/>
    <rect x="84" y="62" width="88" height="30" rx="7" fill="#3a4a63" stroke="none"/>
    <g fill="#3a4a63" stroke="none">
      <circle cx="94" cy="118" r="9"/><circle cx="128" cy="118" r="9"/><circle cx="162" cy="118" r="9"/>
      <circle cx="94" cy="148" r="9"/><circle cx="128" cy="148" r="9"/><circle cx="162" cy="148" r="9"/>
      <circle cx="94" cy="178" r="9"/><circle cx="128" cy="178" r="9"/><circle cx="162" cy="178" r="9" fill="#2f9fe0"/>
    </g>"""),
    "aura-monitor": ("#0e2f5e", "#1f9ed8", f"""
    <path {S} d="M44 150 H92 L112 92 L140 186 L160 128 H212" stroke="#5ff2c8" stroke-width="15"/>"""),
    "aura-photos": ("#2a9d8f", "#57c8f2", f"""
    <rect x="46" y="62" width="164" height="132" rx="14" {W}/>
    <circle cx="92" cy="102" r="13" fill="#2a9d8f" stroke="none"/>
    <path d="M58 182 L110 124 L142 156 L168 132 L198 182 Z" fill="#2a9d8f" stroke="none"/>"""),
    "aura-media": ("#8e44c9", "#3f8fe0", f"""
    <circle cx="128" cy="128" r="72" {W} opacity="0.22"/>
    <circle cx="128" cy="128" r="72" {S}/>
    <path {W} d="M108 88 L176 128 L108 168 Z"/>"""),
    "aura-archive": ("#8a6a3c", "#c9a35c", f"""
    <rect x="54" y="78" width="148" height="112" rx="12" {W}/>
    <rect x="54" y="78" width="148" height="30" fill="#6e5327" stroke="none"/>
    <path {S} d="M128 108 V168" stroke="#8a6a3c"/>
    <rect x="114" y="150" width="28" height="22" rx="5" fill="#8a6a3c" stroke="none"/>"""),
    "aura-screenshot": ("#45597a", "#7d9cc4", f"""
    <path {S} d="M58 96 V66 a8 8 0 0 1 8-8 h30 M160 58 h30 a8 8 0 0 1 8 8 v30 M198 160 v30 a8 8 0 0 1-8 8 h-30 M96 198 H66 a8 8 0 0 1-8-8 v-30"/>
    <circle cx="128" cy="128" r="26" {S}/>"""),
    "aura-pdf": ("#c23b3b", "#e06868", f"""
    <rect x="68" y="44" width="120" height="168" rx="12" {W}/>
    <text x="128" y="146" font-family="sans-serif" font-weight="bold" font-size="44" text-anchor="middle" fill="#c23b3b" stroke="none">PDF</text>"""),
    "aura-transfer": ("#1f9ed8", "#2fd0a8", f"""
    <path {S} d="M128 52 V164" stroke-width="16"/>
    <path {S} d="M84 124 L128 168 L172 124" stroke-width="16"/>
    <path {S} d="M60 196 H196" stroke-width="16"/>"""),
    "aura-taskmanager": ("#274b8f", "#4fa0e8", f"""
    <path {S} d="M64 82 H192 M64 128 H192 M64 174 H192"/>
    <rect x="56" y="70" width="16" height="24" rx="4" {W}/><rect x="120" y="116" width="16" height="24" rx="4" {W}/><rect x="84" y="162" width="16" height="24" rx="4" {W}/>"""),
    "aura-backup": ("#1c7a5e", "#3fc48f", f"""
    <path {W} d="M128 46 L196 70 V126 C196 172 166 202 128 216 C90 202 60 172 60 126 V70 Z" opacity="0.95"/>
    <path d="M128 92 V132 L158 148" fill="none" stroke="#1c7a5e" stroke-width="13" stroke-linecap="round"/>
    <path d="M94 100 a38 38 0 0 1 30-12" fill="none" stroke="#1c7a5e" stroke-width="11" stroke-linecap="round"/>"""),
    "aura-help": ("#2f7fe0", "#57c8f2", f"""
    <text x="128" y="178" font-family="sans-serif" font-weight="bold" font-size="150" text-anchor="middle" fill="#ffffff" stroke="none">?</text>"""),
    "aura-firewall": ("#8f2d3f", "#e0653c", f"""
    <g stroke="none">
      <rect x="52" y="96" width="72" height="30" rx="5" {W}/><rect x="132" y="96" width="72" height="30" rx="5" {W}/>
      <rect x="76" y="134" width="72" height="30" rx="5" {W}/><rect x="156" y="134" width="48" height="30" rx="5" {W}/><rect x="52" y="134" width="16" height="30" rx="5" {W}/>
      <rect x="52" y="172" width="72" height="30" rx="5" {W}/><rect x="132" y="172" width="72" height="30" rx="5" {W}/>
    </g>
    <path {W} d="M128 30 C140 52 156 60 156 82 a28 28 0 1 1 -56 0 C100 60 116 52 128 30 Z" opacity="0.95"/>"""),
    "aura-welcome": ("#0b2a6b", "#2ea8e8", f"""
    <circle cx="182" cy="78" r="19" {W}/>
    <path {W} d="M30 196 L98 104 L144 152 L184 112 L226 196 Z" opacity="0.65"/>
    <path {W} d="M30 212 L112 118 L158 166 L196 134 L226 212 Z"/>"""),
    "utilities-terminal": ("#0a1e46", "#14418f", f"""
    <rect x="40" y="56" width="176" height="144" rx="14" {S}/>
    <path {S} d="M74 102 L112 128 L74 154"/>
    <path {S} d="M126 160 H182"/>"""),
    "system-software-install": ("#7a4fe0", "#3f8fe0", f"""
    <path {W} d="M128 52 L198 88 V168 L128 204 L58 168 V88 Z" opacity="0.95"/>
    <path {S} d="M58 88 L128 124 L198 88 M128 124 V204" stroke="#4a35a8"/>"""),
}

FOLDER = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <defs>
    <linearGradient id="fb" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5eb2f2"/><stop offset="1" stop-color="#2f7fe0"/>
    </linearGradient>
    <linearGradient id="ff" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#8fd0fb"/><stop offset="1" stop-color="#57acf2"/>
    </linearGradient>
  </defs>
  <path d="M28 84 a12 12 0 0 1 12-12 h64 l18 20 h106 a12 12 0 0 1 12 12 v18 H28z" fill="url(#fb)"/>
  <rect x="28" y="106" width="200" height="92" rx="12" fill="url(#ff)"/>
  {emblem}
</svg>
"""

EMBLEMS = {
    "folder": "",
    "folder-documents": '<path d="M104 128 h48 v52 h-48z M114 142 h28 M114 156 h28" stroke="#ffffff" stroke-width="7" fill="none" stroke-linecap="round"/>',
    "folder-download": '<path d="M128 122 v36 M106 140 l22 22 22-22 M100 176 h56" stroke="#ffffff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "folder-music": '<path d="M112 168 V118 l44-8 v48" stroke="#ffffff" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="98" cy="168" r="13" fill="#ffffff"/><circle cx="142" cy="158" r="13" fill="#ffffff"/>',
    "folder-pictures": '<circle cx="106" cy="136" r="7" fill="#ffffff"/><path d="M86 176 L118 140 L140 162 L154 148 L172 176Z" fill="#ffffff"/>',
    "folder-videos": '<path d="M112 128 l44 24-44 24z" fill="#ffffff"/>',
    "user-home": '<path d="M88 152 L128 116 L168 152 M98 144 v34 h60 v-34" stroke="#ffffff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "folder-open": "",
}

INDEX_THEME = """[Icon Theme]
Name=AuraIcons
Comment=AURA OS blue mountain icon theme
Inherits=Papirus,Adwaita,hicolor
Example=folder
Directories=scalable/apps,scalable/places,scalable/status,scalable/devices

[scalable/apps]
Size=256
Context=Applications
Type=Scalable
MinSize=16
MaxSize=512

[scalable/places]
Size=256
Context=Places
Type=Scalable
MinSize=16
MaxSize=512

[scalable/status]
Size=256
Context=Status
Type=Scalable
MinSize=16
MaxSize=512

[scalable/devices]
Size=256
Context=Devices
Type=Scalable
MinSize=16
MaxSize=512
"""


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("icon:", os.path.relpath(path, ROOT))


def main():
    for name, (c1, c2, glyph) in APPS.items():
        write(os.path.join(ROOT, "scalable", "apps", name + ".svg"),
              TILE.format(c1=c1, c2=c2, glyph=glyph))
    # AURA logo as the start-here / distributor icon
    logo_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "assets", "branding", "aura-logo.svg")
    with open(logo_src, encoding="utf-8") as fh:
        logo = fh.read()
    for alias in ("aura-logo", "start-here", "distributor-logo", "aura-about"):
        write(os.path.join(ROOT, "scalable", "apps", alias + ".svg"), logo)
    for name, emblem in EMBLEMS.items():
        write(os.path.join(ROOT, "scalable", "places", name + ".svg"),
              FOLDER.format(emblem=emblem))
    # trash + drive basics
    write(os.path.join(ROOT, "scalable", "places", "user-trash.svg"),
          TILE.format(c1="#5b7296", c2="#869cbd", glyph=f"""
    <path {S} d="M76 84 H180 M104 84 V66 a10 10 0 0 1 10-10 h28 a10 10 0 0 1 10 10 v18 M88 84 L98 196 a12 12 0 0 0 12 11 h36 a12 12 0 0 0 12-11 L168 84 M114 116 V172 M142 116 V172"/>"""))
    write(os.path.join(ROOT, "scalable", "devices", "drive-harddisk.svg"),
          TILE.format(c1="#33507e", c2="#5b84c4", glyph=f"""
    <rect x="52" y="84" width="152" height="88" rx="14" {W}/>
    <circle cx="100" cy="128" r="20" fill="#33507e" stroke="none"/>
    <circle cx="100" cy="128" r="7" fill="#ffffff" stroke="none"/>
    <circle cx="182" cy="150" r="6" fill="#3fc48f" stroke="none"/>"""))
    write(os.path.join(ROOT, "index.theme"), INDEX_THEME)
    print("AuraIcons theme generated.")


if __name__ == "__main__":
    main()
