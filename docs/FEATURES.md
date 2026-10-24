# AURA OS 1.0 — Features & honest limitations

## ✅ Implemented and tested (in this repo)

- **`aura` CLI** — 21 subcommands, fully working & unit-tested (theme,
  accent, wallpaper, dock, apps, open, search/install/remove/update/upgrade,
  clean, doctor, system/fetch, session, backup, completions).
- **Celestia Shell** — Zsh config (prompt with Git branch, completions,
  autosuggestions, syntax highlighting, history search), Celestia terminal
  color scheme, 6-lesson interactive tutorial (runs against real commands).
- **Branding set** — logo (3 SVG variants), 4 mountain wallpapers,
  AuraIcons (38 SVGs), AuraCursor (real binary XCursors incl. animated
  spinner), AuraDark/AuraLight GTK3+GTK4 CSS themes, generated xfwm4 XPM
  decorations, 13 synthesized system sounds, Plymouth splash, GRUB theme,
  LightDM slick-greeter skin, os-release/issue/motd identity.
- **Desktop defaults** — top menu bar (Whisker + global appmenu + tray +
  PulseAudio + power + clipman + clock + session), Plank dock w/ AURA theme
  & pinned apps incl. Trash, xfdesktop wallpaper, 4 named workspaces,
  snapping/tiling/compositor defaults, full shortcut map, clipboard history.
- **24 AURA app launchers → real programs** + 6 AURA-native GTK apps
  (Settings, App Center, Welcome, Notes, Monitor, Help, About) + widgets.
- **App Center** — 56-app curated catalog (APT + Flathub, 10 categories),
  installed-state detection, pkexec installs/removals with live log,
  repository-wide search, update checker + Upgrade All.
- **First-run wizard** — account, mode, accent, wallpaper, display &
  accessibility, Celestia intro, App Center; autostarts once.
- **Installers/builds** — `install-aura.sh` (with `--dry-run`, tested),
  shared `finalize.sh`, live-build ISO script + Calamares branding, debos
  UTM image recipe (generated from one package-list source), GitHub Actions
  for CI + ARM64 artifact builds.
- **Test suite** — 17 tests, all passing (`./tests/run-tests.sh`).

## ✅ Implemented by composition (upstream components, AURA-configured)

Window management/snapping/fullscreen (xfwm4), file manager w/ tabs, split
view, thumbnails (Thunar+tumbler), browser (Firefox ESR), editor &
light IDE (Mousepad, Geany), image viewer (Ristretto), media (Parole),
PDF (Evince), archives (Xarchiver), screenshots (xfce4-screenshooter),
downloads (uGet), snapshots (Timeshift), notifications (xfce4-notifyd),
lock screen (xfce4-screensaver), display/power/keyboard panels (Xfce),
package updates = Debian's own.

## ⚠️ Known limitations (planned or inherent)

- **X11, not Wayland.** Xfce on Xorg was chosen for VM reliability; blur is
  faked with translucency (xfwm4 compositor), not true Gaussian blur.
  Picom ships as an optional extra for those who want more.
- **Global app menu** (xfce4-appmenu-plugin, optional package) works only
  with apps that export menus — many Xfce apps keep in-window menus.
- **"Auto" theme** currently maps to Dark; time-of-day switching is on the
  roadmap.
- **Screen recording** isn't preinstalled; OBS Studio is one click away in
  the App Center (works under UTM's virtual display).
- **Live ISO bootloader menu** is live-build's stock GRUB screen (the AURA
  GRUB theme applies post-install). Cosmetic only.
- **Package-name validation against the live Debian archive** happens in CI
  image builds; the three least-certain packages install opportunistically
  (see `build/packages/optional.txt`) so a rename can never break installs.
- **Not every Windows/macOS app runs here** — by design and physics.
  See the in-OS *Compatibility* help topic for the honest guide
  (Linux versions, web apps, Wine notes, separate VMs).
- Guest tools depend on UTM/QEMU features being enabled (clipboard,
  directory sharing); `aura doctor` tells you exactly what's missing.

## Not yet built (roadmap candidates)

Time-based auto theme · `.deb` packaging of the overlay for cleaner upgrades ·
notification-history panel applet · AURA Mail/Calendar native clients ·
ARM64→x86 user-mode helpers (FEX/Box64) evaluation · additional workspace
gestures · more wallpapers & a community theme gallery.
