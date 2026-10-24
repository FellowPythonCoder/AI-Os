#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  AURA OS installer — transform a fresh Debian 12 (bookworm) ARM64 system
#  into AURA OS. This is the quickest way to run AURA inside UTM:
#
#    1. Install stock Debian 12 ARM64 in UTM ("Virtualize", UEFI).
#    2. Clone this repo (or copy it via a UTM shared folder).
#    3. Run:  sudo ./installer/install-aura.sh --user "$USER"
#    4. Reboot → AURA login screen → welcome wizard.
#
#  Safe by design:
#    • --dry-run prints every action without changing anything.
#    • Files it overwrites are backed up to /var/backups/aura-<timestamp>/.
#    • Your home files are merged, never replaced (see finalize.sh).
#    • It installs only signed Debian repository packages (plus the AURA
#      overlay from this repo). Nothing is piped from the internet into root.
# ─────────────────────────────────────────────────────────────────────────────
set -u
export DEBIAN_FRONTEND=noninteractive

DRY_RUN=0
ASSUME_YES=0
TARGET_USER="${SUDO_USER:-}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
    cat <<EOF
AURA OS installer

Usage: sudo ./installer/install-aura.sh [options]
  --user NAME    user to prepare (default: the sudo caller)
  --yes          don't ask for confirmation
  --dry-run      print what would happen, change nothing
  --help         this help
EOF
}

while [ $# -gt 0 ]; do
    case "$1" in
        --user) TARGET_USER="${2:-}"; shift 2 ;;
        --yes|-y) ASSUME_YES=1; shift ;;
        --dry-run) DRY_RUN=1; shift ;;
        --help|-h) usage; exit 0 ;;
        *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
    esac
done

log()  { echo "▸ $*"; }
warn() { echo "! $*" >&2; }
die()  { echo "✗ $*" >&2; exit 1; }

run() {
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "  [dry-run] $*"
    else
        "$@"
    fi
}

# ── Preflight ────────────────────────────────────────────────────────────────
[ "$(id -u)" -eq 0 ] || die "Please run with sudo:  sudo $0 --user \$USER"
[ -d "$REPO_DIR/rootfs" ] || die "rootfs/ overlay not found next to this script."
[ -n "$TARGET_USER" ] || die "Tell me which user to prepare: --user YOURNAME"
id "$TARGET_USER" >/dev/null 2>&1 || die "User '$TARGET_USER' does not exist."

. /etc/os-release 2>/dev/null || die "Cannot read /etc/os-release"
case "${ID:-}:${ID_LIKE:-}" in
    debian*|aura*|*debian*) : ;;
    *) die "AURA OS targets Debian 12 (found '${PRETTY_NAME:-unknown}'). Aborting." ;;
esac
if [ "${VERSION_CODENAME:-}" != "bookworm" ] && [ "${DEBIAN_CODENAME:-}" != "bookworm" ]; then
    warn "This system reports codename '${VERSION_CODENAME:-?}'. AURA 1.0 is built"
    warn "for Debian 12 'bookworm' — continuing anyway, package names may differ."
fi

ARCH="$(dpkg --print-architecture)"
if [ "$ARCH" != "arm64" ]; then
    warn "Architecture is '$ARCH', not arm64. AURA is designed for Apple-Silicon"
    warn "UTM (arm64); the desktop will still install, but this is untested."
fi

FREE_GB="$(df --output=avail -BG / | tail -1 | tr -dc '0-9')"
if [ "${FREE_GB:-0}" -lt 12 ]; then
    warn "Only ${FREE_GB} GB free on /. AURA's desktop needs ~6 GB; 12+ GB recommended."
fi

echo
echo "🏔  AURA OS installer"
echo "   Base system : ${PRETTY_NAME:-Debian} ($ARCH)"
echo "   User        : $TARGET_USER"
echo "   Source      : $REPO_DIR"
echo "   Mode        : $([ "$DRY_RUN" -eq 1 ] && echo 'DRY RUN (no changes)' || echo 'install')"
echo
if [ "$ASSUME_YES" -ne 1 ] && [ "$DRY_RUN" -ne 1 ]; then
    printf "Continue? [y/N] "
    read -r reply
    case "$reply" in y|Y|yes|YES) ;; *) echo "Aborted."; exit 0 ;; esac
fi

# ── Packages ─────────────────────────────────────────────────────────────────
read_list() { grep -vE '^\s*(#|$)' "$1"; }

log "Updating package lists…"
run apt-get update

log "Installing AURA core packages (this can take a while)…"
# shellcheck disable=SC2046
run apt-get install -y --no-install-recommends \
    $(read_list "$REPO_DIR/build/packages/core.txt") \
    || die "Core package installation failed — see output above."

log "Installing optional extras (failures are OK)…"
while IFS= read -r pkg; do
    [ -n "$pkg" ] || continue
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "  [dry-run] apt-get install -y $pkg"
    else
        apt-get install -y --no-install-recommends "$pkg" >/dev/null 2>&1 \
            && log "  + $pkg" || warn "  - skipped $pkg (not available)"
    fi
done <<EOF
$(read_list "$REPO_DIR/build/packages/optional.txt")
EOF

# ── Overlay ──────────────────────────────────────────────────────────────────
BACKUP_DIR="/var/backups/aura-$(date +%Y%m%d-%H%M%S)"
log "Applying the AURA overlay (backups → $BACKUP_DIR)…"
if [ "$DRY_RUN" -eq 1 ]; then
    (cd "$REPO_DIR/rootfs" && find . -type f | sort | sed 's/^/  [dry-run] overlay → /')
else
    mkdir -p "$BACKUP_DIR"
    (cd "$REPO_DIR/rootfs" && find . -type f -print0 | while IFS= read -r -d '' f; do
        dest="/${f#./}"
        if [ -e "$dest" ] || [ -L "$dest" ]; then
            mkdir -p "$BACKUP_DIR$(dirname "$dest")"
            cp -a "$dest" "$BACKUP_DIR$dest" 2>/dev/null || true
        fi
    done)
    # --remove-destination so files replace symlinks cleanly (e.g. os-release)
    cp -a --remove-destination "$REPO_DIR/rootfs/." /
    chmod +x /usr/share/aura/finalize.sh
fi

# ── Finalize ─────────────────────────────────────────────────────────────────
log "Finalizing (themes, boot splash, login, user setup)…"
if [ "$DRY_RUN" -eq 1 ]; then
    echo "  [dry-run] /usr/share/aura/finalize.sh --user $TARGET_USER"
else
    /usr/share/aura/finalize.sh --user "$TARGET_USER"
fi

echo
echo "✓ AURA OS is installed."
echo
echo "  Next steps:"
echo "   1. Reboot:            sudo reboot"
echo "   2. Log in as $TARGET_USER — the Welcome wizard will greet you."
echo "   3. Open Celestia Shell and try:  aura help   ·   aura doctor"
echo
echo "  Undo: the pre-AURA versions of replaced system files are in"
echo "        $BACKUP_DIR"
