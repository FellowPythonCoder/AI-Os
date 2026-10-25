#!/usr/bin/env python3
"""
Generate the AuraIcons icon theme — AURA Liquid Glass Blue Edition (SVG).

Every application icon is crafted in the AURA Liquid Glass design language:
- Rounded-square squircle silhouette with ambient shadow and double glass rim
- Refined Blue Liquid Glass palette (#071426, #0B2345, #1677FF, #55D6FF, #BDEBFF, #F4F9FF)
- Zero warm gold, orange, bronze, or red tile backgrounds — cohesive blue, cyan,
  frosted crystal, and polished silver across the entire desktop
- Multi-layered 3D-inspired forms, internal lighting, specular glass reflections,
  and crisp readability at small and large sizes

Run:  python3 tools/generate_icons.py
Output is written into rootfs/usr/share/icons/AuraIcons/.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.join(REPO, "rootfs", "usr", "share", "icons", "AuraIcons")

# 3D Liquid Glass Tile Template
TILE = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{c1}"/>
      <stop offset="0.55" stop-color="{c2}"/>
      <stop offset="1" stop-color="{c3}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.28" r="0.62">
      <stop offset="0" stop-color="{glow}" stop-opacity="0.42"/>
      <stop offset="0.65" stop-color="#1677FF" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#071426" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="glassFrost" x1="0" y1="0" x2="0.2" y2="1">
      <stop offset="0" stop-color="#F4F9FF" stop-opacity="0.96"/>
      <stop offset="0.6" stop-color="#BDEBFF" stop-opacity="0.88"/>
      <stop offset="1" stop-color="#89D4FF" stop-opacity="0.82"/>
    </linearGradient>
    <linearGradient id="glassBlue" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0" stop-color="#55D6FF" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#1677FF" stop-opacity="0.90"/>
    </linearGradient>
    <linearGradient id="glassDeep" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0B2345" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#071426" stop-opacity="0.96"/>
    </linearGradient>
    <linearGradient id="silver" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F4F9FF"/>
      <stop offset="0.5" stop-color="#D2E6F8"/>
      <stop offset="1" stop-color="#8FB5D8"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F4F9FF" stop-opacity="0.30"/>
      <stop offset="0.5" stop-color="#BDEBFF" stop-opacity="0.07"/>
      <stop offset="1" stop-color="#55D6FF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F4F9FF" stop-opacity="0.68"/>
      <stop offset="0.5" stop-color="#55D6FF" stop-opacity="0.48"/>
      <stop offset="1" stop-color="#1677FF" stop-opacity="0.28"/>
    </linearGradient>
    <clipPath id="sq">
      <rect x="6" y="6" width="244" height="244" rx="56"/>
    </clipPath>
  </defs>
  <!-- 3D base drop shadow -->
  <rect x="10" y="14" width="236" height="234" rx="54" fill="#030914" opacity="0.46"/>
  <g clip-path="url(#sq)">
    <rect x="6" y="6" width="244" height="244" fill="url(#bg)"/>
    <circle cx="128" cy="76" r="136" fill="url(#glow)"/>
    <path d="M6 6 H250 V96 C188 118 68 116 6 86 Z" fill="url(#sheen)"/>
{glyph}
    <!-- Subtle inner bottom reflection -->
    <path d="M36 244 H220" stroke="#55D6FF" stroke-width="1.5" stroke-opacity="0.35"/>
  </g>
  <rect x="6" y="6" width="244" height="244" rx="56" fill="none" stroke="url(#rim)" stroke-width="2.4"/>
  <rect x="8.5" y="8.5" width="239" height="239" rx="53.5" fill="none" stroke="#F4F9FF" stroke-opacity="0.15" stroke-width="1"/>
</svg>
"""

# App definitions: name -> (c1, c2, c3, glow_color, glyph_svg)
APPS = {
    # 1. Finder-style file manager
    "aura-finder": ("#0B2345", "#124696", "#1677FF", "#55D6FF", """
    <rect x="42" y="76" width="172" height="126" rx="20" fill="#040D1A" opacity="0.35"/>
    <path d="M40 84 a16 16 0 0 1 16-16 h50 l16 16 h78 a16 16 0 0 1 16 16 v82 a18 18 0 0 1-18 18 H58 a18 18 0 0 1-18-18 Z" fill="url(#glassBlue)"/>
    <rect x="52" y="90" width="152" height="26" rx="8" fill="#F4F9FF" opacity="0.88"/>
    <rect x="40" y="104" width="176" height="94" rx="18" fill="url(#glassFrost)"/>
    <path d="M44 106 H212" stroke="#F4F9FF" stroke-width="2" stroke-opacity="0.85"/>
    <path d="M84 180 L118 134 L142 160 L162 140 L186 180 Z" fill="#0B2345" opacity="0.86"/>
    <path d="M84 180 L118 134 L132 150 L114 180 Z" fill="#1677FF" opacity="0.9"/>
    <circle cx="166" cy="126" r="8" fill="#1677FF"/>"""),

    # 2. Celestia Shell
    "celestia-shell": ("#071426", "#0B2345", "#103468", "#55D6FF", """
    <rect x="38" y="54" width="184" height="156" rx="22" fill="#020812" opacity="0.5"/>
    <rect x="36" y="48" width="184" height="154" rx="22" fill="url(#glassDeep)" stroke="#55D6FF" stroke-opacity="0.55" stroke-width="2"/>
    <path d="M36 70 a22 22 0 0 1 22-22 h140 a22 22 0 0 1 22 22 v12 H36 Z" fill="#133463" opacity="0.95"/>
    <circle cx="58" cy="65" r="5.5" fill="#55D6FF"/>
    <circle cx="76" cy="65" r="5.5" fill="#1677FF"/>
    <circle cx="94" cy="65" r="5.5" fill="#BDEBFF" opacity="0.7"/>
    <path d="M68 108 L106 132 L68 156" fill="none" stroke="#55D6FF" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="118" y="148" width="54" height="12" rx="6" fill="#F4F9FF"/>
    <circle cx="188" cy="112" r="18" fill="#55D6FF" opacity="0.14"/>"""),

    # 3. Web Browser
    "aura-browser": ("#071426", "#0D357A", "#1677FF", "#55D6FF", """
    <circle cx="128" cy="132" r="82" fill="#030B18" opacity="0.42"/>
    <circle cx="128" cy="128" r="80" fill="url(#glassBlue)" stroke="#F4F9FF" stroke-width="2.5" stroke-opacity="0.75"/>
    <ellipse cx="128" cy="128" rx="42" ry="78" fill="none" stroke="#BDEBFF" stroke-width="3.5" stroke-opacity="0.65"/>
    <path d="M50 110 Q128 88 206 110 M50 146 Q128 168 206 146 M128 48 V208" fill="none" stroke="#BDEBFF" stroke-width="3" stroke-opacity="0.55"/>
    <!-- 3D Liquid Glass Compass Needle -->
    <polygon points="168,88 138,138 118,118" fill="#F4F9FF"/>
    <polygon points="88,168 138,138 118,118" fill="#0B2345" opacity="0.88"/>
    <circle cx="128" cy="128" r="8" fill="#55D6FF" stroke="#F4F9FF" stroke-width="2"/>"""),

    # 4. App Center
    "aura-appcenter": ("#071426", "#0E336B", "#1677FF", "#55D6FF", """
    <rect x="48" y="72" width="160" height="136" rx="24" fill="#040D1B" opacity="0.4"/>
    <path d="M96 74 V58 a32 32 0 0 1 64 0 V74" fill="none" stroke="#BDEBFF" stroke-width="10" stroke-linecap="round"/>
    <rect x="46" y="68" width="164" height="136" rx="24" fill="url(#glassFrost)" stroke="#F4F9FF" stroke-width="2"/>
    <!-- 4 Blue Glass App Tiles inside bag -->
    <rect x="68" y="90" width="50" height="50" rx="13" fill="#1677FF"/>
    <rect x="138" y="90" width="50" height="50" rx="13" fill="#0B2345"/>
    <rect x="68" y="146" width="50" height="42" rx="12" fill="#0E4FB5"/>
    <rect x="138" y="146" width="50" height="42" rx="12" fill="#55D6FF"/>
    <path d="M163 102 V126 M152 116 L163 127 L174 116" fill="none" stroke="#55D6FF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M78 128 L92 104 L108 128 Z" fill="#F4F9FF"/>"""),

    # 5. System Settings
    "aura-settings": ("#071426", "#0B2345", "#1A4B8C", "#55D6FF", """
    <rect x="42" y="48" width="172" height="164" rx="26" fill="#030A16" opacity="0.42"/>
    <rect x="40" y="44" width="176" height="168" rx="26" fill="url(#silver)" opacity="0.18" stroke="#BDEBFF" stroke-opacity="0.45" stroke-width="2"/>
    <!-- 3 Tactile Liquid Glass Sliders -->
    <rect x="62" y="76" width="132" height="12" rx="6" fill="#071426" opacity="0.7"/>
    <rect x="62" y="76" width="68" height="12" rx="6" fill="#55D6FF"/>
    <circle cx="130" cy="82" r="16" fill="url(#glassFrost)" stroke="#1677FF" stroke-width="3"/>
    <rect x="62" y="122" width="132" height="12" rx="6" fill="#071426" opacity="0.7"/>
    <rect x="62" y="122" width="100" height="12" rx="6" fill="#1677FF"/>
    <circle cx="162" cy="128" r="16" fill="url(#glassFrost)" stroke="#55D6FF" stroke-width="3"/>
    <rect x="62" y="168" width="132" height="12" rx="6" fill="#071426" opacity="0.7"/>
    <rect x="62" y="168" width="42" height="12" rx="6" fill="#55D6FF"/>
    <circle cx="104" cy="174" r="16" fill="url(#glassFrost)" stroke="#1677FF" stroke-width="3"/>"""),

    # 6. Text and code editor
    "aura-text": ("#0B2345", "#144A9E", "#1677FF", "#BDEBFF", """
    <rect x="58" y="44" width="140" height="174" rx="18" fill="#040C1A" opacity="0.38"/>
    <rect x="56" y="40" width="140" height="174" rx="18" fill="url(#glassFrost)" stroke="#F4F9FF" stroke-width="2"/>
    <rect x="78" y="72" width="66" height="10" rx="5" fill="#1677FF"/>
    <rect x="78" y="96" width="96" height="9" rx="4.5" fill="#0B2345" opacity="0.65"/>
    <rect x="78" y="118" width="96" height="9" rx="4.5" fill="#0B2345" opacity="0.65"/>
    <rect x="78" y="140" width="82" height="9" rx="4.5" fill="#0B2345" opacity="0.65"/>
    <rect x="78" y="162" width="56" height="9" rx="4.5" fill="#1677FF" opacity="0.85"/>
    <!-- 3D Blue Crystal Stylus -->
    <g transform="translate(158,142) rotate(-38)">
      <rect x="-10" y="-48" width="20" height="76" rx="6" fill="url(#glassDeep)" stroke="#55D6FF" stroke-width="2"/>
      <polygon points="-10,28 10,28 0,48" fill="#55D6FF"/>
    </g>"""),

    # 7. Development Studio
    "aura-studio": ("#071426", "#0B2345", "#1677FF", "#55D6FF", """
    <rect x="36" y="48" width="184" height="160" rx="22" fill="url(#glassDeep)" stroke="#55D6FF" stroke-opacity="0.5" stroke-width="2"/>
    <rect x="36" y="48" width="42" height="160" rx="22" fill="#0E2C59" opacity="0.85"/>
    <circle cx="57" cy="76" r="6" fill="#55D6FF"/>
    <circle cx="57" cy="98" r="6" fill="#1677FF"/>
    <circle cx="57" cy="120" r="6" fill="#BDEBFF" opacity="0.6"/>
    <path d="M114 94 L86 128 L114 162" fill="none" stroke="#55D6FF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M168 94 L196 128 L168 162" fill="none" stroke="#F4F9FF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M148 86 L132 170" fill="none" stroke="#1677FF" stroke-width="9" stroke-linecap="round"/>"""),

    # 8. Notes (Cool Frosted Crystal & Electric Cyan — NO warm gold/yellow!)
    "aura-notes": ("#0B2345", "#134B9E", "#1677FF", "#55D6FF", """
    <rect x="54" y="46" width="148" height="172" rx="20" fill="#040D1C" opacity="0.38"/>
    <rect x="52" y="42" width="148" height="172" rx="20" fill="url(#glassFrost)" stroke="#F4F9FF" stroke-width="2"/>
    <path d="M52 62 a20 20 0 0 1 20-20 h108 a20 20 0 0 1 20 20 v24 H52 Z" fill="url(#glassBlue)"/>
    <!-- Silver spiral binding rings -->
    <rect x="78" y="34" width="10" height="22" rx="5" fill="url(#silver)"/>
    <rect x="122" y="34" width="10" height="22" rx="5" fill="url(#silver)"/>
    <rect x="166" y="34" width="10" height="22" rx="5" fill="url(#silver)"/>
    <!-- Note lines & cyan checkmarks -->
    <circle cx="80" cy="112" r="7" fill="#1677FF"/>
    <rect x="96" y="107" width="80" height="10" rx="5" fill="#0B2345" opacity="0.78"/>
    <circle cx="80" cy="142" r="7" fill="#55D6FF"/>
    <rect x="96" y="137" width="80" height="10" rx="5" fill="#0B2345" opacity="0.65"/>
    <circle cx="80" cy="172" r="7" fill="#1677FF" opacity="0.6"/>
    <rect x="96" y="167" width="56" height="10" rx="5" fill="#0B2345" opacity="0.55"/>"""),

    # 9. Calendar (Blue Liquid Glass & Ice Cyan — NO red/orange!)
    "aura-calendar": ("#071426", "#0B2345", "#1677FF", "#55D6FF", """
    <rect x="46" y="54" width="164" height="158" rx="22" fill="#030A18" opacity="0.42"/>
    <rect x="44" y="50" width="164" height="158" rx="22" fill="url(#glassFrost)" stroke="#F4F9FF" stroke-width="2"/>
    <path d="M44 72 a22 22 0 0 1 22-22 h120 a22 22 0 0 1 22 22 v26 H44 Z" fill="url(#glassBlue)"/>
    <rect x="82" y="38" width="12" height="28" rx="6" fill="url(#silver)"/>
    <rect x="158" y="38" width="12" height="28" rx="6" fill="url(#silver)"/>
    <text x="126" y="81" font-family="sans-serif" font-weight="bold" font-size="20" letter-spacing="3" text-anchor="middle" fill="#F4F9FF">AURA</text>
    <!-- Date grid with glowing cyan active day -->
    <rect x="68" y="114" width="28" height="24" rx="7" fill="#0B2345" opacity="0.25"/>
    <rect x="112" y="114" width="28" height="24" rx="7" fill="#1677FF"/>
    <rect x="156" y="114" width="28" height="24" rx="7" fill="#0B2345" opacity="0.25"/>
    <rect x="68" y="152" width="28" height="24" rx="7" fill="#0B2345" opacity="0.25"/>
    <rect x="112" y="152" width="28" height="24" rx="7" fill="#55D6FF"/>
    <rect x="156" y="152" width="28" height="24" rx="7" fill="#0B2345" opacity="0.25"/>"""),

    # 10. Calculator
    "aura-calculator": ("#071426", "#0B2345", "#153D7A", "#55D6FF", """
    <rect x="58" y="38" width="140" height="180" rx="22" fill="url(#glassDeep)" stroke="#55D6FF" stroke-opacity="0.55" stroke-width="2"/>
    <rect x="74" y="54" width="108" height="40" rx="10" fill="#0E2E5C" stroke="#55D6FF" stroke-opacity="0.45" stroke-width="1.5"/>
    <text x="172" y="82" font-family="monospace" font-weight="bold" font-size="24" text-anchor="end" fill="#55D6FF">2048</text>
    <g fill="#BDEBFF" opacity="0.88">
      <rect x="74" y="110" width="28" height="24" rx="7"/><rect x="114" y="110" width="28" height="24" rx="7"/>
      <rect x="74" y="144" width="28" height="24" rx="7"/><rect x="114" y="144" width="28" height="24" rx="7"/>
      <rect x="74" y="178" width="68" height="24" rx="7"/>
    </g>
    <g fill="#1677FF">
      <rect x="154" y="110" width="28" height="24" rx="7"/>
      <rect x="154" y="144" width="28" height="24" rx="7"/>
    </g>
    <rect x="154" y="178" width="28" height="24" rx="7" fill="#55D6FF"/>"""),

    # 11. System Monitor
    "aura-monitor": ("#071426", "#0B2345", "#113A78", "#55D6FF", """
    <rect x="36" y="48" width="184" height="160" rx="24" fill="url(#glassDeep)" stroke="#55D6FF" stroke-opacity="0.5" stroke-width="2"/>
    <path d="M52 92 H204 M52 128 H204 M52 164 H204" stroke="#1677FF" stroke-width="1.5" stroke-opacity="0.28"/>
    <path d="M48 164 L86 164 L108 102 L134 176 L158 82 L180 140 L208 140 L208 192 L48 192 Z" fill="#1677FF" opacity="0.32"/>
    <path d="M48 164 L86 164 L108 102 L134 176 L158 82 L180 140 L208 140" fill="none" stroke="#55D6FF" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="158" cy="82" r="7" fill="#F4F9FF" stroke="#55D6FF" stroke-width="3"/>"""),

    # 12. Photos
    "aura-photos": ("#071426", "#0D3472", "#1677FF", "#55D6FF", """
    <rect x="42" y="56" width="172" height="148" rx="22" fill="#030B18" opacity="0.4"/>
    <rect x="40" y="52" width="172" height="148" rx="22" fill="url(#glassFrost)" stroke="#F4F9FF" stroke-width="2"/>
    <rect x="52" y="64" width="148" height="124" rx="14" fill="url(#glassDeep)"/>
    <circle cx="164" cy="94" r="14" fill="#55D6FF"/>
    <circle cx="164" cy="94" r="8" fill="#F4F9FF"/>
    <path d="M52 184 L102 116 L142 158 L168 128 L200 184 Z" fill="url(#glassBlue)"/>
    <path d="M52 188 L88 136 L124 172 L156 142 L200 188 Z" fill="#BDEBFF" opacity="0.9"/>"""),

    # 13. Media Player
    "aura-media": ("#071426", "#0B2345", "#1677FF", "#55D6FF", """
    <circle cx="128" cy="132" r="80" fill="#030A18" opacity="0.45"/>
    <circle cx="128" cy="128" r="78" fill="url(#glassDeep)" stroke="#55D6FF" stroke-width="3"/>
    <circle cx="128" cy="128" r="58" fill="none" stroke="#1677FF" stroke-width="6" stroke-opacity="0.6"/>
    <circle cx="128" cy="128" r="42" fill="url(#glassBlue)"/>
    <path d="M114 102 L158 128 L114 154 Z" fill="#F4F9FF"/>"""),

    # 14. File Transfer
    "aura-transfer": ("#071426", "#0C2F66", "#1677FF", "#55D6FF", """
    <circle cx="128" cy="128" r="78" fill="url(#glassDeep)" stroke="#55D6FF" stroke-opacity="0.5" stroke-width="2.5"/>
    <!-- Upward cyan crystal arrow -->
    <path d="M98 172 V86 M74 110 L98 84 L122 110" fill="none" stroke="#55D6FF" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Downward frosted white crystal arrow -->
    <path d="M158 84 V170 M134 146 L158 172 L182 146" fill="none" stroke="#F4F9FF" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>"""),

    # 15. Archive Manager (Blue Crystal & Silver Vault — NO brown/bronze!)
    "aura-archive": ("#071426", "#0B2345", "#144999", "#55D6FF", """
    <rect x="46" y="64" width="164" height="136" rx="22" fill="url(#glassFrost)" stroke="#F4F9FF" stroke-width="2"/>
    <path d="M46 86 a22 22 0 0 1 22-22 h120 a22 22 0 0 1 22 22 v20 H46 Z" fill="url(#glassBlue)"/>
    <!-- Vertical silver zipper track -->
    <rect x="116" y="64" width="24" height="136" fill="#0B2345" opacity="0.82"/>
    <g fill="#55D6FF">
      <rect x="120" y="72" width="16" height="8" rx="3"/>
      <rect x="120" y="88" width="16" height="8" rx="3"/>
      <rect x="120" y="104" width="16" height="8" rx="3"/>
      <rect x="120" y="120" width="16" height="8" rx="3"/>
    </g>
    <rect x="110" y="136" width="36" height="44" rx="10" fill="url(#silver)" stroke="#1677FF" stroke-width="3"/>
    <circle cx="128" cy="160" r="6" fill="#0B2345"/>"""),

    # 16. Screenshot utility
    "aura-screenshot": ("#071426", "#0B2345", "#1677FF", "#55D6FF", """
    <rect x="44" y="62" width="168" height="136" rx="24" fill="url(#glassDeep)" stroke="#BDEBFF" stroke-opacity="0.55" stroke-width="2"/>
    <path d="M62 98 V78 h20 M194 98 V78 h-20 M62 162 V182 h20 M194 162 V182 h-20" fill="none" stroke="#55D6FF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="128" cy="130" r="38" fill="url(#glassBlue)" stroke="#F4F9FF" stroke-width="4"/>
    <circle cx="128" cy="130" r="18" fill="#071426"/>
    <circle cx="140" cy="118" r="6" fill="#F4F9FF"/>
    <circle cx="180" cy="84" r="6" fill="#55D6FF"/>"""),

    # 17. PDF Viewer (Frosted White & Cobalt/Cyan — NO red!)
    "aura-pdf": ("#071426", "#0B2345", "#1677FF", "#55D6FF", """
    <path d="M62 42 h96 l40 40 v132 a18 18 0 0 1-18 18 H62 a18 18 0 0 1-18-18 V60 a18 18 0 0 1 18-18 Z" fill="url(#glassFrost)" stroke="#F4F9FF" stroke-width="2"/>
    <path d="M158 42 v26 a14 14 0 0 0 14 14 h26 Z" fill="#55D6FF"/>
    <rect x="56" y="102" width="128" height="44" rx="10" fill="url(#glassBlue)"/>
    <text x="120" y="133" font-family="sans-serif" font-weight="bold" font-size="30" letter-spacing="2" text-anchor="middle" fill="#F4F9FF">PDF</text>
    <rect x="72" y="164" width="96" height="9" rx="4.5" fill="#0B2345" opacity="0.65"/>
    <rect x="72" y="184" width="68" height="9" rx="4.5" fill="#1677FF" opacity="0.75"/>"""),

    # 18. Backup utility
    "aura-backup": ("#071426", "#0B2345", "#134996", "#55D6FF", """
    <path d="M128 40 L200 68 V126 C200 174 168 206 128 220 C88 206 56 174 56 126 V68 Z" fill="url(#glassFrost)" stroke="#F4F9FF" stroke-width="2.5"/>
    <path d="M128 54 L184 76 V124 C184 162 158 188 128 200 C98 188 72 162 72 124 V76 Z" fill="url(#glassDeep)"/>
    <path d="M92 126 a36 36 0 1 1 12 26" fill="none" stroke="#55D6FF" stroke-width="10" stroke-linecap="round"/>
    <polygon points="84,114 110,126 88,142" fill="#55D6FF"/>
    <path d="M128 104 V128 L146 140" fill="none" stroke="#F4F9FF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>"""),

    # 19. Task Manager
    "aura-taskmanager": ("#071426", "#0B2345", "#143E82", "#55D6FF", """
    <rect x="42" y="48" width="172" height="160" rx="22" fill="url(#glassDeep)" stroke="#55D6FF" stroke-opacity="0.5" stroke-width="2"/>
    <rect x="64" y="74" width="128" height="22" rx="8" fill="#0E2E5C"/>
    <rect x="64" y="74" width="96" height="22" rx="8" fill="url(#glassBlue)"/>
    <rect x="64" y="116" width="128" height="22" rx="8" fill="#0E2E5C"/>
    <rect x="64" y="116" width="68" height="22" rx="8" fill="#55D6FF"/>
    <rect x="64" y="158" width="128" height="22" rx="8" fill="#0E2E5C"/>
    <rect x="64" y="158" width="112" height="22" rx="8" fill="url(#glassFrost)"/>"""),

    # 20. Help Center
    "aura-help": ("#071426", "#0D3778", "#1677FF", "#55D6FF", """
    <circle cx="128" cy="128" r="80" fill="url(#glassBlue)" stroke="#F4F9FF" stroke-width="3" stroke-opacity="0.8"/>
    <circle cx="128" cy="128" r="62" fill="url(#glassDeep)"/>
    <path d="M106 102 C106 84 150 84 150 106 C150 122 128 124 128 142" fill="none" stroke="#55D6FF" stroke-width="14" stroke-linecap="round"/>
    <circle cx="128" cy="168" r="8" fill="#F4F9FF"/>"""),

    # 21. Firewall (Blue Shield & Electric Cyan Guard — NO orange/red!)
    "aura-firewall": ("#071426", "#0B2345", "#1677FF", "#55D6FF", """
    <path d="M128 38 L202 66 V126 C202 174 168 206 128 220 C88 206 54 174 54 126 V66 Z" fill="url(#glassBlue)" stroke="#F4F9FF" stroke-width="2.5"/>
    <path d="M128 54 V202 C96 190 70 162 70 124 V76 Z" fill="#0B2345" opacity="0.65"/>
    <rect x="104" y="116" width="48" height="40" rx="9" fill="#F4F9FF"/>
    <path d="M114 116 V102 a14 14 0 0 1 28 0 V116" fill="none" stroke="#55D6FF" stroke-width="8" stroke-linecap="round"/>
    <circle cx="128" cy="136" r="6" fill="#0B2345"/>"""),

    # 22. Lock Screen & Quick Settings
    "aura-lock": ("#071426", "#0B2345", "#123C7B", "#55D6FF", """
    <circle cx="128" cy="128" r="78" fill="url(#glassDeep)" stroke="#55D6FF" stroke-opacity="0.55" stroke-width="2.5"/>
    <rect x="88" y="118" width="80" height="64" rx="14" fill="url(#glassFrost)"/>
    <path d="M104 118 V96 a24 24 0 0 1 48 0 V118" fill="none" stroke="#55D6FF" stroke-width="12" stroke-linecap="round"/>
    <circle cx="128" cy="146" r="8" fill="#0B2345"/>
    <rect x="124" y="148" width="8" height="16" rx="4" fill="#1677FF"/>"""),

    "aura-quicksettings": ("#071426", "#0B2345", "#1677FF", "#55D6FF", """
    <rect x="46" y="62" width="164" height="56" rx="28" fill="url(#glassBlue)" stroke="#F4F9FF" stroke-width="2"/>
    <circle cx="178" cy="90" r="20" fill="#F4F9FF"/>
    <rect x="46" y="138" width="164" height="56" rx="28" fill="url(#glassDeep)" stroke="#55D6FF" stroke-width="2"/>
    <circle cx="78" cy="166" r="20" fill="#55D6FF"/>"""),
}

# Trash icon (sculpted frosted silver-blue crystal bin)
TRASH_GLYPH = """
    <ellipse cx="128" cy="72" rx="58" ry="14" fill="url(#silver)" stroke="#F4F9FF" stroke-width="2"/>
    <path d="M72 74 L86 200 a18 18 0 0 0 18 16 h48 a18 18 0 0 0 18-16 L184 74 Z" fill="url(#glassFrost)" opacity="0.92" stroke="#F4F9FF" stroke-width="2"/>
    <path d="M104 102 L108 186 M128 102 V186 M152 102 L148 186" stroke="#0B2345" stroke-width="8" stroke-linecap="round" opacity="0.55"/>
    <rect x="108" y="54" width="40" height="12" rx="6" fill="#55D6FF"/>
"""

# 3D Liquid Glass Folder Template
FOLDER = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <defs>
    <linearGradient id="fBack" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1677FF"/>
      <stop offset="1" stop-color="#0B2345"/>
    </linearGradient>
    <linearGradient id="fFront" x1="0" y1="0" x2="0.2" y2="1">
      <stop offset="0" stop-color="#BDEBFF" stop-opacity="0.96"/>
      <stop offset="0.45" stop-color="#55D6FF" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#1677FF" stop-opacity="0.95"/>
    </linearGradient>
  </defs>
  <rect x="24" y="68" width="208" height="142" rx="22" fill="#040C1A" opacity="0.36"/>
  <path d="M22 76 a18 18 0 0 1 18-18 h58 l18 18 h102 a18 18 0 0 1 18 18 v28 H22 Z" fill="url(#fBack)"/>
  <rect x="36" y="84" width="184" height="24" rx="10" fill="#F4F9FF" opacity="0.9"/>
  <rect x="22" y="96" width="212" height="110" rx="20" fill="url(#fFront)" stroke="#F4F9FF" stroke-opacity="0.7" stroke-width="2"/>
  <path d="M28 98 H228" stroke="#F4F9FF" stroke-width="2" stroke-opacity="0.85"/>
  {emblem}
</svg>
"""

EMBLEMS = {
    "folder": '<path d="M96 168 L124 132 L144 154 L158 138 L178 168 Z" fill="#071426" opacity="0.32"/>',
    "folder-documents": '<rect x="104" y="122" width="48" height="58" rx="8" fill="#F4F9FF"/><path d="M114 138 h28 M114 152 h28 M114 166 h18" stroke="#0B2345" stroke-width="6" stroke-linecap="round"/>',
    "folder-download": '<path d="M128 118 v42 M106 142 l22 22 22-22 M100 176 h56" stroke="#F4F9FF" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "folder-music": '<path d="M114 168 V120 l42-8 v48" stroke="#F4F9FF" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="102" cy="168" r="12" fill="#F4F9FF"/><circle cx="144" cy="158" r="12" fill="#F4F9FF"/>',
    "folder-pictures": '<circle cx="106" cy="134" r="8" fill="#F4F9FF"/><path d="M86 176 L118 138 L140 160 L156 144 L174 176 Z" fill="#F4F9FF"/>',
    "folder-videos": '<polygon points="110,124 158,150 110,176" fill="#F4F9FF"/>',
    "user-home": '<path d="M90 152 L128 118 L166 152 M100 146 v32 h56 v-32" stroke="#F4F9FF" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "folder-open": '<path d="M96 168 L124 132 L144 154 L158 138 L178 168 Z" fill="#F4F9FF" opacity="0.65"/>',
}

# Standard freedesktop icon aliases mapped to our redesigned AURA Liquid Glass icons
ALIASES = {
    "apps": {
        "utilities-terminal": "celestia-shell",
        "org.xfce.terminal": "celestia-shell",
        "system-file-manager": "aura-finder",
        "org.xfce.thunar": "aura-finder",
        "thunar": "aura-finder",
        "web-browser": "aura-browser",
        "firefox-esr": "aura-browser",
        "system-software-install": "aura-appcenter",
        "preferences-system": "aura-settings",
        "org.xfce.settings.manager": "aura-settings",
        "accessories-text-editor": "aura-text",
        "org.xfce.mousepad": "aura-text",
        "geany": "aura-studio",
        "accessories-notes": "aura-notes",
        "office-calendar": "aura-calendar",
        "orage": "aura-calendar",
        "accessories-calculator": "aura-calculator",
        "galculator": "aura-calculator",
        "utilities-system-monitor": "aura-monitor",
        "org.xfce.taskmanager": "aura-taskmanager",
        "multimedia-photo-viewer": "aura-photos",
        "org.xfce.ristretto": "aura-photos",
        "multimedia-video-player": "aura-media",
        "org.xfce.Parole": "aura-media",
        "parole": "aura-media",
        "package-x-generic": "aura-archive",
        "xarchiver": "aura-archive",
        "applets-screenshooter": "aura-screenshot",
        "org.xfce.screenshooter": "aura-screenshot",
        "application-pdf": "aura-pdf",
        "org.gnome.Evince": "aura-pdf",
        "system-backup": "aura-backup",
        "timeshift": "aura-backup",
        "help-browser": "aura-help",
        "system-help": "aura-help",
        "gufw": "aura-firewall",
        "security-high": "aura-firewall",
        "system-lock-screen": "aura-lock",
        "xfce4-screensaver": "aura-lock",
    },
}

INDEX_THEME = """[Icon Theme]
Name=AuraIcons
Comment=AURA OS Liquid Glass Blue Edition icon theme
Inherits=Papirus-Dark,Papirus,Adwaita,hicolor
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
    # Copy branding SVGs into rootfs/usr/share/pixmaps as well
    pixmaps = os.path.join(REPO, "rootfs", "usr", "share", "pixmaps")
    os.makedirs(pixmaps, exist_ok=True)
    for fn in ("aura-logo.svg", "aura-logo-symbol.svg", "aura-logo-mono.svg"):
        src = os.path.join(REPO, "assets", "branding", fn)
        if os.path.isfile(src):
            shutil.copyfile(src, os.path.join(pixmaps, fn))

    for name, (c1, c2, c3, glow, glyph) in APPS.items():
        write(os.path.join(ROOT, "scalable", "apps", name + ".svg"),
              TILE.format(c1=c1, c2=c2, c3=c3, glow=glow, glyph=glyph))

    # AURA mountain logo for OS / Welcome / About / Start menu
    logo_src = os.path.join(REPO, "assets", "branding", "aura-logo.svg")
    with open(logo_src, encoding="utf-8") as fh:
        logo = fh.read()
    for alias in ("aura-logo", "start-here", "distributor-logo",
                  "aura-about", "aura-welcome", "xfce4-whiskermenu"):
        write(os.path.join(ROOT, "scalable", "apps", alias + ".svg"), logo)

    # Standard desktop aliases
    for cat, mapping in ALIASES.items():
        for alias, target in mapping.items():
            target_path = os.path.join(ROOT, "scalable", cat, target + ".svg")
            with open(target_path, encoding="utf-8") as fh:
                svg = fh.read()
            write(os.path.join(ROOT, "scalable", cat, alias + ".svg"), svg)

    # Places / Folders
    for name, emblem in EMBLEMS.items():
        write(os.path.join(ROOT, "scalable", "places", name + ".svg"),
              FOLDER.format(emblem=emblem))

    # Trash (empty & full)
    trash_svg = TILE.format(c1="#071426", c2="#0B2345", c3="#164B96",
                            glow="#55D6FF", glyph=TRASH_GLYPH)
    write(os.path.join(ROOT, "scalable", "places", "user-trash.svg"), trash_svg)
    write(os.path.join(ROOT, "scalable", "places", "user-trash-full.svg"), trash_svg)
    write(os.path.join(ROOT, "scalable", "apps", "user-trash.svg"), trash_svg)

    # Drive icon
    write(os.path.join(ROOT, "scalable", "devices", "drive-harddisk.svg"),
          TILE.format(c1="#071426", c2="#0B2345", c3="#164B96", glow="#55D6FF", glyph="""
    <rect x="48" y="76" width="160" height="104" rx="20" fill="url(#silver)" stroke="#F4F9FF" stroke-width="2"/>
    <circle cx="102" cy="128" r="26" fill="#0B2345"/>
    <circle cx="102" cy="128" r="9" fill="#55D6FF"/>
    <rect x="146" y="118" width="40" height="8" rx="4" fill="#0B2345" opacity="0.6"/>
    <circle cx="180" cy="154" r="7" fill="#55D6FF"/>"""))

    # Status lock icon
    with open(os.path.join(ROOT, "scalable", "apps", "aura-lock.svg"), encoding="utf-8") as fh:
        lock_svg = fh.read()
    write(os.path.join(ROOT, "scalable", "status", "system-lock-screen.svg"), lock_svg)

    write(os.path.join(ROOT, "index.theme"), INDEX_THEME)
    print("AuraIcons Liquid Glass theme generated.")


if __name__ == "__main__":
    main()
