#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  AURA OS finalize — turn a rootfs with the AURA overlay into a finished
#  system. Shared by install-aura.sh (running systems), live-build hooks and
#  the debos image build. Idempotent: safe to run more than once.
#
#  Usage: finalize.sh [--user NAME] [--skip-boot] [--live]
#    --user NAME   also prepare that user's home (skel merge + zsh)
#    --skip-boot   don't touch GRUB/initramfs (used inside live builds)
#    --live        live-ISO tweaks (installer shortcut, live user services)
# ─────────────────────────────────────────────────────────────────────────────
set -u
export DEBIAN_FRONTEND=noninteractive
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TARGET_USER=""
SKIP_BOOT=0
LIVE=0
while [ $# -gt 0 ]; do
    case "$1" in
        --user) TARGET_USER="${2:-}"; shift 2 ;;
        --skip-boot) SKIP_BOOT=1; shift ;;
        --live) LIVE=1; shift ;;
        *) echo "finalize: unknown argument $1" >&2; shift ;;
    esac
done

log()  { echo "  ▸ $*"; }
warn() { echo "  ! $*" >&2; }

[ "$(id -u)" -eq 0 ] || { echo "finalize must run as root" >&2; exit 1; }

echo "🏔  Finalizing AURA OS…"

# ── Executable bits for AURA programs ────────────────────────────────────────
chmod 0755 /usr/bin/aura /usr/bin/aura-* /usr/bin/celestia-tutorial 2>/dev/null || true

# ── GLib schemas (Plank defaults, GNOME-app defaults) ────────────────────────
if command -v glib-compile-schemas >/dev/null 2>&1; then
    log "Compiling GLib schemas"
    glib-compile-schemas /usr/share/glib-2.0/schemas 2>/dev/null \
        || warn "glib-compile-schemas reported problems (continuing)"
fi

# ── Icon caches ──────────────────────────────────────────────────────────────
for theme in /usr/share/icons/AuraIcons /usr/share/icons/hicolor; do
    [ -d "$theme" ] && gtk-update-icon-cache -f -t "$theme" >/dev/null 2>&1 || true
done
command -v update-icon-caches >/dev/null 2>&1 && update-icon-caches /usr/share/icons/* >/dev/null 2>&1 || true
command -v fc-cache >/dev/null 2>&1 && fc-cache -f >/dev/null 2>&1 || true
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database /usr/share/applications >/dev/null 2>&1 || true

# ── Boot artwork (Plymouth + GRUB PNGs) ──────────────────────────────────────
if [ -x /usr/share/aura/render-boot-assets.sh ]; then
    log "Rendering boot artwork"
    /usr/share/aura/render-boot-assets.sh "" || warn "boot artwork partially failed"
fi

# ── Plymouth default theme ───────────────────────────────────────────────────
if command -v update-alternatives >/dev/null 2>&1 && [ -f /usr/share/plymouth/themes/aura/aura.plymouth ]; then
    log "Setting Plymouth theme: aura"
    update-alternatives --install /usr/share/plymouth/themes/default.plymouth \
        default.plymouth /usr/share/plymouth/themes/aura/aura.plymouth 120 >/dev/null 2>&1 || true
    update-alternatives --set default.plymouth \
        /usr/share/plymouth/themes/aura/aura.plymouth >/dev/null 2>&1 || true
fi

# ── GRUB: AURA branding + quiet splash (kept in our own drop-in) ────────────
if [ "$SKIP_BOOT" -eq 0 ]; then
    mkdir -p /etc/default/grub.d
    cat > /etc/default/grub.d/aura.cfg <<'GRUBEOF'
# AURA OS bootloader defaults
GRUB_DISTRIBUTOR="AURA OS"
GRUB_THEME="/usr/share/grub/themes/aura/theme.txt"
GRUB_GFXMODE="auto"
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash loglevel=3"
GRUB_TIMEOUT=5
GRUB_TIMEOUT_STYLE="menu"
GRUBEOF
    if command -v update-grub >/dev/null 2>&1 && [ -d /boot/grub ]; then
        log "Updating GRUB configuration"
        update-grub >/dev/null 2>&1 || warn "update-grub failed (continuing)"
    fi
    if command -v update-initramfs >/dev/null 2>&1; then
        log "Rebuilding initramfs (boot splash)"
        update-initramfs -u >/dev/null 2>&1 || warn "update-initramfs failed (continuing)"
    fi
fi

# ── Display manager → LightDM ────────────────────────────────────────────────
if [ -e /usr/sbin/lightdm ]; then
    log "Selecting LightDM as display manager"
    echo "/usr/sbin/lightdm" > /etc/X11/default-display-manager 2>/dev/null || true
    if command -v debconf-set-selections >/dev/null 2>&1; then
        echo "lightdm shared/default-x-display-manager select lightdm" | debconf-set-selections 2>/dev/null || true
    fi
    systemctl enable lightdm.service >/dev/null 2>&1 || true
    systemctl set-default graphical.target >/dev/null 2>&1 || true
fi

# ── Services ─────────────────────────────────────────────────────────────────
for svc in NetworkManager qemu-guest-agent spice-vdagentd; do
    systemctl enable "$svc" >/dev/null 2>&1 || true
done

# Firewall: ship ufw rules only if ufw is installed — never force-install one.
if command -v ufw >/dev/null 2>&1; then
    # Set safe defaults without deleting any rules the user already made.
    ufw default deny incoming >/dev/null 2>&1 || true
    ufw default allow outgoing >/dev/null 2>&1 || true
    log "Firewall (ufw) defaulted to deny-incoming — enable with: sudo ufw enable"
fi

# ── Flatpak: Flathub remote (App Center's second source) ────────────────────
if command -v flatpak >/dev/null 2>&1; then
    log "Adding Flathub remote"
    flatpak remote-add --if-not-exists flathub \
        https://dl.flathub.org/repo/flathub.flatpakrepo >/dev/null 2>&1 \
        || warn "Flathub remote not added (no network?) — App Center can retry later"
fi

# ── Default browser alternatives ─────────────────────────────────────────────
if [ -e /usr/bin/firefox-esr ]; then
    update-alternatives --set x-www-browser /usr/bin/firefox-esr >/dev/null 2>&1 || true
    update-alternatives --set gnome-www-browser /usr/bin/firefox-esr >/dev/null 2>&1 || true
fi

# ── Locale sanity (images only; installers/user systems keep their own) ─────
if [ ! -f /etc/locale.gen ]; then
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
    locale-gen >/dev/null 2>&1 || true
fi

# ── Prepare a user home ──────────────────────────────────────────────────────
prepare_user() {
    local u="$1" home
    home="$(getent passwd "$u" | cut -d: -f6)"
    [ -n "$home" ] && [ -d "$home" ] || { warn "no home for $u — skipping"; return; }
    log "Preparing home for $u ($home)"
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --ignore-existing /etc/skel/ "$home"/ 2>/dev/null || true
    else
        cp -rn /etc/skel/. "$home"/ 2>/dev/null || true
    fi
    # Always refresh AURA-owned pieces that should track the OS version
    mkdir -p "$home/.config/plank/dock1/launchers" "$home/.config/autostart" \
             "$home/.config/aura" "$home/.local/share/applications"
    cp -f /etc/skel/.config/plank/dock1/launchers/*.dockitem \
          "$home/.config/plank/dock1/launchers/" 2>/dev/null || true
    cp -f /etc/skel/.local/share/applications/*.desktop \
          "$home/.local/share/applications/" 2>/dev/null || true
    cp -f /etc/skel/.config/autostart/*.desktop "$home/.config/autostart/" 2>/dev/null || true
    # Default shell → zsh (Celestia). Users can switch back any time.
    if [ -x /bin/zsh ] || [ -x /usr/bin/zsh ]; then
        chsh -s /bin/zsh "$u" >/dev/null 2>&1 || chsh -s /usr/bin/zsh "$u" >/dev/null 2>&1 || true
    fi
    mkdir -p "$home"/{Desktop,Documents,Downloads,Music,Pictures,Videos,Notes,Projects}
    chown -R "$u":"$u" "$home/.config" "$home/.local" "$home/Desktop" \
        "$home/Documents" "$home/Downloads" "$home/Music" "$home/Pictures" \
        "$home/Videos" "$home/Notes" "$home/Projects" 2>/dev/null || true
    [ -f "$home/.zshrc" ] && chown "$u":"$u" "$home/.zshrc" || true
}

if [ -n "$TARGET_USER" ]; then
    prepare_user "$TARGET_USER"
fi

# ── Live-ISO extras ──────────────────────────────────────────────────────────
if [ "$LIVE" -eq 1 ]; then
    log "Applying live-session extras"
    # "Install AURA OS" shortcut appears only in the live session
    install -Dm644 /usr/share/aura/install-aura-os.desktop \
        /etc/skel/Desktop/Install-AURA-OS.desktop 2>/dev/null || true
    chmod +x /etc/skel/Desktop/Install-AURA-OS.desktop 2>/dev/null || true
fi

echo "✓ AURA OS finalize complete."
