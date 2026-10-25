# 🏔️ AURA OS — Liquid Glass Blue Edition

### A blue-mountain desktop operating system for Apple Silicon

**AURA OS** is a complete, bootable ARM64 operating system that runs in
[UTM](https://mac.getutm.app/) on Apple Silicon Macs (developed for an M4
with 16 GB). Featuring the **AURA Liquid Glass** design identity —
translucent blue glass surfaces (`#071426`, `#0B2345`, `#1677FF`, `#55D6FF`,
`#BDEBFF`, `#F4F9FF`), 3D-inspired squircle icons, a floating glass dock,
a PAM-authenticated mountain lock screen, and an interactive Liquid Glass
Theme Editor — it pairs macOS-inspired elegance with the real power of
Debian GNU/Linux underneath and **Celestia Shell**, AURA's signature terminal.

> AURA is an independent project. It is not affiliated with Apple, and it
> is not a website or a mockup — it's a real OS you boot.

![AURA default wallpaper: midnight blue peaks over a still lake](rootfs/usr/share/backgrounds/aura/aura-midnight-peaks.jpg)

---

## ✨ What's inside

| | |
|---|---|
| 🏔 **Liquid Glass Identity** | Original 3D blue-mountain logo, 8 coordinated wallpapers (incl. Liquid Waves, Cyan Horizon, Minimal Gradient & Lock Peaks), custom GTK3/4 + xfwm4 Liquid Glass themes (Light & Dark), 84 SVG 3D-inspired `AuraIcons`, animated `AuraCursor`, synthesized sound theme, Plymouth boot splash, GRUB theme, LightDM login |
| 🔒 **PAM Lock Screen** | `aura-lock` (`Super+L`) — real Linux PAM (`libpam.so.0` + `PAM_DISALLOW_NULL_AUTHTOK`) session lock with mountain wallpaper, animated snow/light particles, large centered digital clock + date, glowing circular user avatar, translucent blue-glass password box, notification privacy (auto-DND while locked), and idle auto-lock |
| 🖥️ **Desktop & Quick Settings** | Xfce-based: translucent 32px top menu bar with global app menu, floating `aura-quicksettings` control center (`Super+S`), Plank floating blue-glass dock with magnification & running indicators, 4 workspaces, window snapping/tiling, Spotlight-style search (`Super+Space`) |
| ⌨️ **Celestia Shell** | Deep navy (`#071426`) Zsh terminal with electric-cyan (`#55D6FF`) syntax highlighting, tabs, `tmux` split panes (`panes`), autosuggestions, fuzzy history + the **`aura`** CLI (`aura glass`, `aura lock`, `aura theme`, `aura install`, `aura doctor`, …) |
| 🧩 **26 AURA apps** | Finder, Browser, Settings, Quick Settings, Lock Screen, App Center, Text, Studio, Notes, Calendar, Calculator, Monitor, Photos, Media, Archive, Screenshot, PDF, Transfer, Task Manager, Backup, Firewall, Help, Welcome, About… every one launches a real program |
| 🎨 **12-Section System Settings** | Interactive **Liquid Glass Theme Editor** with live Cairo preview, glass opacity & blur sliders, performance mode, wallpapers & lock screen config, dock & menu bar, icons & cursor, UTM display & brightness, keyboard/mouse, notifications, security, network/audio, startup items, Celestia Shell, and VM info |
| 🛠️ **Developer-ready** | Git, Python 3, Node.js + npm, GCC/G++/CMake/GDB, tmux, ripgrep, SSH, curl preinstalled |
| 🍎 **UTM-native** | ARM64 guest tools preinstalled (clipboard, display resize, shared folders), honest guest-vs-host RAM reporting, tuned for a 16 GB Mac |

## 🚀 Quick start (fastest: ~15 minutes)

1. Install **Debian 12 ARM64** in UTM (Virtualize → Linux; use the
   official `debian-12.x-arm64-netinst.iso`), 4–6 GB RAM, 4 cores, 32 GB disk.
2. In the VM: `sudo apt install git && git clone https://github.com/FellowPythonCoder/AI-Os`
3. `cd AI-Os && sudo ./installer/install-aura.sh --user "$USER"`
4. Reboot → AURA login → Welcome wizard. Done. 🏔️

Prefer a prebuilt image or installer ISO? See **[docs/INSTALL-UTM.md](docs/INSTALL-UTM.md)**
for all three routes (download, ISO install, Debian transform) with exact
UTM settings and troubleshooting.

## ⌨️ Celestia Shell in 30 seconds

```console
▲ you@aura-os ~ 
➜ aura help            # the friendly command guide
➜ aura install gimp    # real APT installs (password-prompted)
➜ aura theme glacier   # whole OS re-accents instantly
➜ aura wallpaper set aura-aurora-ridge
➜ aura doctor          # plain-English health check
```

Plus everything Linux: `git`, `python3`, `node`, `ssh`, `docker`, `curl`…
Full guide: **[docs/CELESTIA.md](docs/CELESTIA.md)**.

## 📚 Documentation

- [Install on UTM](docs/INSTALL-UTM.md) — the three install routes, VM settings
- [Building AURA](docs/BUILDING.md) — ISO & disk-image builds, CI
- [Architecture](docs/ARCHITECTURE.md) — how the pieces fit together
- [Celestia Shell](docs/CELESTIA.md) — every `aura` command
- [Customization](docs/CUSTOMIZATION.md) — themes, dock, effects, terminal
- [Features & limitations](docs/FEATURES.md) — honest status of everything
- [Troubleshooting](docs/TROUBLESHOOTING.md) — fixes for common issues

## 🧱 Building from source

```bash
./tests/run-tests.sh          # 17 tests: CLI, assets, scripts (fast)
sudo ./build/build-iso.sh     # bootable live/installer ISO  (ARM64 host)
./build/build-image.sh        # preinstalled UTM disk image   (ARM64 host)
```

GitHub Actions does both on native ARM64 runners
([build-iso.yml](.github/workflows/build-iso.yml),
[build-image.yml](.github/workflows/build-image.yml)) and attaches
artifacts to tagged releases.

## 🙏 Credits

AURA OS is a derivative work standing on
[Debian](https://www.debian.org/), the [Linux kernel](https://kernel.org/),
[Xfce](https://xfce.org/), [Plank](https://launchpad.net/plank),
[LightDM](https://github.com/canonical/lightdm),
[Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/),
[Calamares](https://calamares.io/), [debos](https://github.com/go-debos/debos),
and thousands of free-software authors. AURA's own artwork, themes, code and
documentation are MIT-licensed (see [LICENSE](LICENSE)); the wallpapers ship
with the project. "macOS" is a trademark of Apple Inc.; AURA's interface is
*inspired by* good desktop design, uses its own branding throughout, and
contains no Apple assets.
