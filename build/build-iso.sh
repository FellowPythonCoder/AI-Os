#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  Build the AURA OS bootable live/installer ISO (ARM64) with Debian
#  live-build. Must run on an ARM64 Debian/Ubuntu host (e.g. a Linux VM on
#  your Mac, or the GitHub Actions ARM runner — see .github/workflows).
#
#  Usage:  sudo ./build/build-iso.sh
#  Output: build/out/AURA-OS-1.0-arm64.iso
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LIVE_DIR="$REPO_DIR/build/live"
OUT_DIR="$REPO_DIR/build/out"

[ "$(id -u)" -eq 0 ] || { echo "Please run with sudo." >&2; exit 1; }
command -v lb >/dev/null || { echo "live-build not found: sudo apt install live-build" >&2; exit 1; }
[ "$(dpkg --print-architecture)" = "arm64" ] || {
    echo "This build must run on an ARM64 host (current: $(dpkg --print-architecture))." >&2
    echo "Use an ARM64 Linux VM on the Mac, or CI (ubuntu-24.04-arm)." >&2
    exit 1
}

mkdir -p "$LIVE_DIR/config/package-lists" \
         "$LIVE_DIR/config/hooks/live" \
         "$LIVE_DIR/config/includes.chroot" \
         "$OUT_DIR"

echo "▸ Assembling live-build configuration…"

# Package lists from the single source of truth
cat "$REPO_DIR/build/packages/core.txt" \
    "$REPO_DIR/build/packages/optional.txt" \
    "$REPO_DIR/build/packages/live.txt" \
    > "$LIVE_DIR/config/package-lists/aura.list.chroot"

# Root filesystem overlay (the whole AURA personality)
rsync -a --delete "$REPO_DIR/rootfs/" "$LIVE_DIR/config/includes.chroot/"

# Calamares branding (graphical installer)
install -d "$LIVE_DIR/config/includes.chroot/etc/calamares/branding/aura"
cp "$REPO_DIR/build/live/calamares/branding.desc" \
   "$REPO_DIR/build/live/calamares/show.qml" \
   "$LIVE_DIR/config/includes.chroot/etc/calamares/branding/aura/"

# Chroot hook: finalize AURA inside the image
cat > "$LIVE_DIR/config/hooks/live/0500-aura.hook.chroot" <<'HOOK'
#!/bin/sh
set -e
echo "AURA hook: finalizing system…"
/usr/share/aura/finalize.sh --skip-boot --live || true
# Point Calamares at the AURA branding
if [ -f /etc/calamares/settings.conf ] && [ -f /etc/calamares/branding/aura/branding.desc ]; then
    sed -i 's/^branding:.*/branding: aura/' /etc/calamares/settings.conf || true
    grep -q '^branding:' /etc/calamares/settings.conf || echo 'branding: aura' >> /etc/calamares/settings.conf
fi
echo "AURA hook: done."
HOOK
chmod +x "$LIVE_DIR/config/hooks/live/0500-aura.hook.chroot"

cd "$LIVE_DIR"

# Clean any previous partial config but keep our config/ content
lb clean --purge >/dev/null 2>&1 || true

echo "▸ Configuring (Debian bookworm, arm64, grub-efi)…"
lb config noauto \
    --mode debian \
    --distribution bookworm \
    --architectures arm64 \
    --archive-areas "main contrib non-free-firmware" \
    --parent-archive-areas "main contrib non-free-firmware" \
    --binary-images iso-hybrid \
    --bootloaders grub-efi \
    --bootappend-live "boot=live components quiet splash loglevel=3 username=aura user-fullname=AURA hostname=aura-os locales=en_US.UTF-8 keyboard-layouts=us" \
    --debian-installer false \
    --firmware-binary false \
    --firmware-chroot false \
    --linux-flavours arm64 \
    --linux-packages linux-image \
    --memtest none \
    --iso-application "AURA OS" \
    --iso-publisher "AURA OS Project" \
    --iso-volume "AURA_OS_1.0" \
    --security true \
    --updates true \
    --cache-packages true

echo "▸ Building ISO (this downloads the Debian archive — be patient)…"
lb build 2>&1 | tee "$OUT_DIR/build-iso.log"

ISO="$(ls -1 "$LIVE_DIR"/*.iso 2>/dev/null | head -n1)"
[ -n "$ISO" ] || { echo "Build finished but no ISO was produced — see $OUT_DIR/build-iso.log" >&2; exit 1; }

cp "$ISO" "$OUT_DIR/AURA-OS-1.0-arm64.iso"
(cd "$OUT_DIR" && sha256sum AURA-OS-1.0-arm64.iso > AURA-OS-1.0-arm64.iso.sha256)

echo
echo "✓ Done: $OUT_DIR/AURA-OS-1.0-arm64.iso"
echo "  In UTM: create an ARM64 VM (Virtualize → Linux), point the CD/DVD"
echo "  drive at this ISO, boot, then click “Install AURA OS”."
