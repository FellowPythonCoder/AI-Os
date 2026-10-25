# Changelog

## AURA OS 1.0 "Aurora Peaks" — Liquid Glass Blue Edition — 2026-10-25

Complete UI redesign into **AURA Liquid Glass** while preserving all ARM64 UTM functionality:

- **AURA Liquid Glass Palette & Themes**: Cohesive translucent blue glass system (`#071426` Midnight Navy, `#0B2345` Deep Ocean, `#1677FF` AURA Blue, `#55D6FF` Electric Cyan, `#BDEBFF` Ice Blue, `#F4F9FF` Frosted White) with dynamic `glass.css` & `accent.css` live re-skinning and zero warm gold/orange/bronze/red tile accents.
- **3D-Inspired `AuraIcons` Redesign**: 84 scalable SVGs across all 22+ core applications, places, devices, and desktop aliases with multi-stop gradients, specular reflections, internal cyan lighting, and drop shadows.
- **PAM-Authenticated Lock Screen (`aura-lock`)**: Fullscreen mountain lock screen with real Linux PAM authentication (`libpam.so.0` + `PAM_DISALLOW_NULL_AUTHTOK`), notification privacy (`xfce4-notifyd` auto-DND while locked), X11 seat grab, animated snow/light particles, large centered digital clock + date, glowing user avatar, system-status widgets, Switch User, and idle auto-lock.
- **Quick Settings Control Center (`aura-quicksettings`)**: Floating translucent blue-glass panel (`Super+S` / top menu bar button) for network, dark/light mode, Liquid Glass presets, Do Not Disturb, audio volume, and `xrandr` display brightness.
- **12-Section System Settings (`aura-settings`)**: Redesigned with an interactive Liquid Glass Theme Editor (live Cairo preview, glass opacity, blur intensity, shadow depth, performance mode) and 12 organized sections.
- **Built-in Calendar & Transfer Apps**: Added native GTK3 `aura-calendar` and `aura-transfer` apps so every launcher works out of the box on Debian 12 ARM64.
- **Wallpapers & Celestia Shell**: Added 4 new Liquid Glass wallpapers (`aura-liquid-waves.jpg`, `aura-cyan-horizon.jpg`, `aura-minimal-gradient.jpg`, `aura-lock-peaks.jpg`), `tmux` split-pane configuration (`~/.tmux.conf`), and cyan/ice syntax highlighting.
- **ISO Build & Mac Automation**: Fixed lowercase package names in `build/packages/core.txt`, added tolerant optional package hook in `build/build-iso.sh`, updated `build/build-on-mac.sh` with GitHub Release fast-download + non-interactive Lima (`--tty=false`), and enabled automated ARM64 ISO builds on GitHub Actions.

## AURA OS 1.0 "Aurora Peaks" — 2026-10-24

First complete release of the AURA OS source tree.

- **Base**: Debian 12 (bookworm) ARM64 derivative targeting UTM on Apple Silicon.
- **Desktop**: AURA-skinned Xfce — top menu bar with global app menu, Plank
  dock with magnification, 4 workspaces, clipboard history, notifications,
  Spotlight-style search, full shortcut map.
- **Celestia Shell**: Zsh environment + `aura` CLI (21 subcommands) +
  interactive 6-lesson tutorial + completions.
- **Apps**: 24 AURA launchers over real programs; 7 AURA-native GTK apps
  (Settings, App Center, Welcome, Notes, Monitor, Help, About);
  App Center catalog of 56 apps on APT + Flathub.
- **Theming**: generated AuraDark/AuraLight (GTK3/GTK4/xfwm4), AuraIcons,
  AuraCursor (binary XCursor + animated spinner), synthesized sound theme,
  Plymouth & GRUB themes, LightDM slick-greeter skin, 4 wallpapers.
- **Builds**: install-aura.sh transformer (dry-run + backups), live-build
  installer ISO (Calamares, AURA branding), debos preinstalled UTM image,
  GitHub Actions CI + ARM64 artifact builds, 17-test suite (all passing).
