# Installing Applications

## AURA App Center

The App Center offers curated categories — Productivity, Development,
Internet, Graphics, Video, Audio, Utilities, Games, Education and AI
tools — with one-click install and uninstall, powered by Debian APT
and Flatpak (Flathub).

## From Celestia Shell

- `aura search photo editor` — search the repositories
- `aura install gimp` — install with APT (asks for your password)
- `aura install --flatpak com.spotify.Client` — install from Flathub
- `aura remove gimp` — uninstall

## Other routes

- **AppImages**: download, then `chmod +x file.AppImage && ./file.AppImage`
  (ARM64 AppImages only — x86 ones won't run).
- **.deb files**: double-click in AURA Finder, or
  `sudo apt install ./file.deb` — must be built for **arm64**.
- **From source**: `git clone …`, then follow the project's README.
  Python, Node.js and C/C++ toolchains are preinstalled.

## Safety rules

- Install from the App Center / APT / Flathub whenever you can.
- Never paste mystery `curl … | sudo bash` one-liners. Download scripts,
  read them, then run them yourself.
- AURA will always ask for your password before system changes.
