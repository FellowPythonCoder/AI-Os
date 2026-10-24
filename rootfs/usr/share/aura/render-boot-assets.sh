#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  Render AURA boot assets (Plymouth + GRUB PNGs) from source artwork.
#  Runs inside the target rootfs during install/build. Needs: rsvg-convert
#  (librsvg2-bin) and ImageMagick's convert. Safe to re-run.
#  Usage: render-boot-assets.sh [ROOT]        (ROOT defaults to /)
# ─────────────────────────────────────────────────────────────────────────────
set -u
ROOT="${1:-}"
PLY="$ROOT/usr/share/plymouth/themes/aura"
GRUB="$ROOT/usr/share/grub/themes/aura"
WP="$ROOT/usr/share/backgrounds/aura/aura-midnight-peaks.jpg"
LOGO="$ROOT/usr/share/pixmaps/aura-logo-symbol.svg"

warn() { echo "render-boot-assets: $*" >&2; }

mkdir -p "$PLY" "$GRUB"

if command -v rsvg-convert >/dev/null 2>&1 && [ -f "$LOGO" ]; then
    rsvg-convert -w 240 -h 240 "$LOGO" -o "$PLY/logo.png" \
        || warn "logo rasterization failed"
else
    warn "rsvg-convert not found — Plymouth will run without a logo image."
fi

if command -v convert >/dev/null 2>&1; then
    if [ -f "$WP" ]; then
        convert "$WP" -resize 1920x1080^ -gravity center -extent 1920x1080 \
            -modulate 82,100,100 "$PLY/background.png" || warn "bg convert failed"
        convert "$WP" -resize 1920x1080^ -gravity center -extent 1920x1080 \
            -modulate 78,100,100 "$GRUB/bg.png" || warn "grub bg convert failed"
    fi
    # Progress-bar slices for Plymouth (solid glass-blue)
    convert -size 300x8 'xc:#35507e' "$PLY/bar-bg.png" 2>/dev/null
    convert -size 300x8 gradient:'#57a8f2-#2f7fe0' -rotate 90 "$PLY/bar-fg.png" 2>/dev/null \
        || convert -size 300x8 'xc:#2f7fe0' "$PLY/bar-fg.png" 2>/dev/null
    # GRUB selection highlight (9-slice set, translucent blue)
    for part in c n e s w ne nw se sw; do
        convert -size 16x16 'xc:rgba(47,127,224,0.85)' "$GRUB/select_$part.png" 2>/dev/null
    done
else
    warn "ImageMagick convert not found — boot PNGs skipped (install: imagemagick)."
fi

echo "render-boot-assets: done."
