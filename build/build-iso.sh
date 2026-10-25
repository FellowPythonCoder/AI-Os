#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  Build the AURA OS bootable live/installer ISO (ARM64) with Debian
#  live-build. Must run on an ARM64 Debian/Ubuntu host (e.g. a Linux VM on
#  your Mac via build/build-on-mac.sh, or the GitHub Actions ARM64 runner).
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
         "$LIVE_DIR/config/includes.chroot/usr/share/aura" \
         "$OUT_DIR"

echo "▸ Assembling live-build configuration…"

# Core + live package list (comments and blank lines stripped for live-build)
grep -Ev '^[[:space:]]*(#|$)' \
    "$REPO_DIR/build/packages/core.txt" \
    "$REPO_DIR/build/packages/live.txt" \
    > "$LIVE_DIR/config/package-lists/aura.list.chroot"

# Root filesystem overlay (the whole AURA Liquid Glass personality)
rsync -a --delete "$REPO_DIR/rootfs/" "$LIVE_DIR/config/includes.chroot/"

# Copy optional package list into chroot so the hook can install available ones tolerantly
install -Dm644 "$REPO_DIR/build/packages/optional.txt" \
    "$LIVE_DIR/config/includes.chroot/usr/share/aura/optional-packages.txt"

# Calamares branding (graphical installer)
install -d "$LIVE_DIR/config/includes.chroot/etc/calamares/branding/aura"
cp "$REPO_DIR/build/live/calamares/branding.desc" \
   "$REPO_DIR/build/live/calamares/show.qml" \
   "$LIVE_DIR/config/includes.chroot/etc/calamares/branding/aura/"

# Chroot hook: install available optional packages + finalize AURA inside the image
cat > "$LIVE_DIR/config/hooks/live/0500-aura.hook.chroot" <<'HOOK'
#!/bin/sh
set -e
export DEBIAN_FRONTEND=noninteractive
echo "AURA hook: installing available optional packages…"
if [ -f /usr/share/aura/optional-packages.txt ]; then
    for pkg in $(grep -Ev '^[[:space:]]*(#|$)' /usr/share/aura/optional-packages.txt); do
        if apt-cache show "$pkg" >/dev/null 2>&1; then
            apt-get install -y --no-install-recommends "$pkg" || true
        fi
    done
fi
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

# Clean previous build stages but KEEP the downloaded-package cache,
# so re-running after a failure resumes in minutes, not from zero.
lb clean >/dev/null 2>&1 || true

KEYRING_OPT=()
if [ -f /usr/share/keyrings/debian-archive-keyring.gpg ]; then
    KEYRING_OPT=(--debootstrap-options "--keyring=/usr/share/keyrings/debian-archive-keyring.gpg")
fi

echo "▸ Configuring (Debian bookworm, arm64, grub-efi)…"
lb config noauto \
    --mode debian \
    --distribution bookworm \
    --architectures arm64 \
    --archive-areas "main contrib non-free-firmware" \
    --parent-archive-areas "main contrib non-free-firmware" \
    --mirror-bootstrap "http://deb.debian.org/debian" \
    --mirror-chroot "http://deb.debian.org/debian" \
    --mirror-chroot-security "http://security.debian.org/debian-security" \
    --mirror-binary "http://deb.debian.org/debian" \
    --parent-mirror-bootstrap "http://deb.debian.org/debian" \
    --parent-mirror-chroot "http://deb.debian.org/debian" \
    --parent-mirror-chroot-security "http://security.debian.org/debian-security" \
    --parent-mirror-binary "http://deb.debian.org/debian" \
    "${KEYRING_OPT[@]}" \
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
