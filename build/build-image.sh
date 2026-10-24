#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  Build the AURA OS preinstalled ARM64 disk image for UTM, with debos.
#  Runs on an ARM64 Debian/Ubuntu host. Also produces a .qcow2 for UTM.
#
#  Usage:  ./build/build-image.sh
#  Output: build/out/AURA-OS-1.0-arm64.img (+ .qcow2, + sha256)
#
#  Default login (change forced at first boot):  user "aura", password "aura"
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$REPO_DIR/build/out"
mkdir -p "$OUT_DIR"

command -v debos >/dev/null || {
    echo "debos not found:  sudo apt install debos" >&2; exit 1; }
[ "$(dpkg --print-architecture)" = "arm64" ] || {
    echo "Run this on an ARM64 host (current: $(dpkg --print-architecture))." >&2
    exit 1; }

echo "▸ Rendering debos recipe from package lists…"
python3 "$REPO_DIR/tools/render_debos_recipe.py"

echo "▸ Building disk image with debos (downloads Debian — be patient)…"
cd "$REPO_DIR/build/debos"
# Prefer hardware acceleration; fall back to emulation when /dev/kvm is absent.
BACKEND="${DEBOS_BACKEND:-kvm}"
[ -w /dev/kvm ] || BACKEND="${DEBOS_BACKEND:-qemu}"
echo "  debos backend: $BACKEND"
debos --fakemachine-backend="$BACKEND" \
      --memory=4GB --cpus=4 \
      --artifactdir="$OUT_DIR" \
      aura.yaml

IMG="$OUT_DIR/AURA-OS-1.0-arm64.img"
[ -f "$IMG" ] || { echo "debos finished but no image found in $OUT_DIR" >&2; exit 1; }

if command -v qemu-img >/dev/null; then
    echo "▸ Converting to qcow2 for UTM…"
    qemu-img convert -c -O qcow2 "$IMG" "$OUT_DIR/AURA-OS-1.0-arm64.qcow2"
fi

(cd "$OUT_DIR" && sha256sum AURA-OS-1.0-arm64.img* AURA-OS-1.0-arm64.qcow2 2>/dev/null \
    > AURA-OS-1.0-arm64.sha256 || sha256sum AURA-OS-1.0-arm64.img \
    > AURA-OS-1.0-arm64.sha256)

echo
echo "✓ Done."
ls -lh "$OUT_DIR"/AURA-OS-1.0-arm64.* 2>/dev/null
echo
echo "In UTM: create a new ARM64 VM (Virtualize), skip the ISO, then replace"
echo "its empty drive with AURA-OS-1.0-arm64.qcow2 — see docs/INSTALL-UTM.md."
echo "First login: user 'aura', password 'aura' (you'll be asked to change it)."
