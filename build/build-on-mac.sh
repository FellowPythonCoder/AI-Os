#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  Get or Build the AURA OS ISO *from macOS Terminal* (Apple Silicon).
#
#  1. Fast path: if a prebuilt AURA-OS-1.0-arm64.iso release is already
#     published on GitHub Releases, downloads it straight to ~/Downloads
#     (unless --build-from-source is passed).
#  2. Local build path: creates/starts an ARM64 Debian VM with Lima
#     (--tty=false so it never stops at a menu), runs build/build-iso.sh
#     inside it, and copies AURA-OS-1.0-arm64.iso to ~/Downloads.
#
#  Usage (on the Mac, from ~/AI-Os):
#      caffeinate -i ./build/build-on-mac.sh
#  Options:
#      --build-from-source   always build locally via Lima
#      --stop                stop the builder VM afterwards
# ─────────────────────────────────────────────────────────────────────────────
set -eu
set -o pipefail 2>/dev/null || true

STOP_AFTER=0
FORCE_SOURCE=0
for arg in "$@"; do
    case "$arg" in
        --stop) STOP_AFTER=1 ;;
        --build-from-source) FORCE_SOURCE=1 ;;
    esac
done

VM="${BUILDER_NAME:-aura-builder}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RELEASE_URL="https://github.com/FellowPythonCoder/AI-Os/releases/download/v1.0-liquid-glass/AURA-OS-1.0-arm64.iso"
SHA_URL="https://github.com/FellowPythonCoder/AI-Os/releases/download/v1.0-liquid-glass/AURA-OS-1.0-arm64.iso.sha256"

log()  { printf '▸ %s\n' "$*"; }
die()  { printf '✗ %s\n' "$*" >&2; exit 1; }

# ── Fast path: check if GitHub Releases already has the prebuilt ISO ─────────
if [ "$FORCE_SOURCE" -eq 0 ] && command -v curl >/dev/null 2>&1; then
    if curl -fsSLI "$RELEASE_URL" >/dev/null 2>&1; then
        log "Prebuilt AURA OS Liquid Glass ISO found on GitHub Releases — downloading to ~/Downloads…"
        mkdir -p "$HOME/Downloads"
        curl -fL --progress-bar -o "$HOME/Downloads/AURA-OS-1.0-arm64.iso" "$RELEASE_URL"
        curl -fsSL -o "$HOME/Downloads/AURA-OS-1.0-arm64.iso.sha256" "$SHA_URL" 2>/dev/null || true
        if [ -f "$HOME/Downloads/AURA-OS-1.0-arm64.iso.sha256" ]; then
            (cd "$HOME/Downloads" && shasum -a 256 -c AURA-OS-1.0-arm64.iso.sha256) || true
        fi
        echo
        echo "✓ Done: $HOME/Downloads/AURA-OS-1.0-arm64.iso"
        ls -lh "$HOME/Downloads/AURA-OS-1.0-arm64.iso"
        exit 0
    fi
fi

# ── Platform checks ──────────────────────────────────────────────────────────
[ "$(uname -s)" = "Darwin" ] || die "This script is for macOS. On Linux, run build/build-iso.sh directly."
if [ "$(uname -m)" != "arm64" ]; then
    die "Intel Mac detected — an ARM64 ISO can't be built locally at usable speed.
Use GitHub Actions instead (see docs/ISO-GUIDE.md)."
fi

# ── Homebrew + Lima ──────────────────────────────────────────────────────────
if ! command -v brew >/dev/null 2>&1; then
    die "Homebrew is not installed. Install it first (one command, from brew.sh):
  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"
Then re-run ./build/build-on-mac.sh"
fi
if ! command -v limactl >/dev/null 2>&1; then
    log "Installing Lima (Linux VMs for Mac)…"
    brew install lima
fi

# ── Branch to build (default: whatever this Mac checkout is on) ─────────────
BRANCH="${AURA_BRANCH:-}"
if [ -z "$BRANCH" ]; then
    BRANCH="$(git -C "$REPO_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
fi
log "Builder VM: $VM · branch: $BRANCH"

# ── Create / start the builder VM (non-interactive: --tty=false) ─────────────
if ! limactl list --format '{{.Name}}' 2>/dev/null | grep -qx "$VM"; then
    log "Creating ARM64 Debian builder VM (one-time, downloads ~400 MB)…"
    limactl create --tty=false --name="$VM" --cpus=4 --memory=6 --disk=60 template:debian \
      || limactl create --tty=false --name="$VM" --cpus=4 --memory=6 --disk=60 template://debian \
      || limactl start --tty=false --name="$VM" --cpus=4 --memory=6 --disk=60 template://debian
fi
log "Starting builder VM…"
limactl start --tty=false "$VM" 2>/dev/null || limactl start "$VM"

guest() { limactl shell "$VM" -- bash -lc "$1"; }

# ── Install tools, fetch sources, build ──────────────────────────────────────
log "Installing build tools inside the VM…"
guest 'set -e
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y git live-build rsync debootstrap debian-archive-keyring \
    squashfs-tools xorriso grub-efi-arm64-bin mtools dosfstools'

log "Fetching AURA OS sources (branch: $BRANCH)…"
guest "set -e
cd \"\$HOME\"
if [ -d AI-Os/.git ]; then
  cd AI-Os && git fetch origin && git checkout \"$BRANCH\" && git reset --hard \"origin/$BRANCH\"
else
  git clone -b \"$BRANCH\" https://github.com/FellowPythonCoder/AI-Os.git
fi"

log "Building the ISO — this is the long part (30–90 min). Keep the Mac awake…"
guest 'set -e
cd "$HOME/AI-Os"
sudo ./build/build-iso.sh'

# ── Copy the ISO (+ checksum) to the Mac ─────────────────────────────────────
GUEST_USER="$(guest 'whoami' | tr -d '\r\n')"
ISO_GUEST="/home/$GUEST_USER/AI-Os/build/out/AURA-OS-1.0-arm64.iso"
SHA_GUEST="/home/$GUEST_USER/AI-Os/build/out/AURA-OS-1.0-arm64.iso.sha256"
log "Copying ISO to ~/Downloads…"
limactl copy "$VM:$ISO_GUEST" "$HOME/Downloads/"
limactl copy "$VM:$SHA_GUEST" "$HOME/Downloads/" || true

if [ -f "$HOME/Downloads/AURA-OS-1.0-arm64.iso.sha256" ]; then
    log "Verifying checksum…"
    (cd "$HOME/Downloads" && shasum -a 256 -c AURA-OS-1.0-arm64.iso.sha256)
fi

[ "$STOP_AFTER" -eq 1 ] && limactl stop "$VM"

echo
echo "✓ Done: $HOME/Downloads/AURA-OS-1.0-arm64.iso"
echo
echo "Next: run it in UTM — Create VM → Virtualize → Linux → uncheck"
echo "\"Use Apple Virtualization\" → Boot ISO → this file → 6 GB RAM,"
echo "4 CPUs, 32 GB storage → boot → double-click \"Install AURA OS\"."
echo "Full click-by-click: docs/ISO-GUIDE.md (Phase 4 onwards)."
