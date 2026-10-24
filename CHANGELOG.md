# Changelog

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
