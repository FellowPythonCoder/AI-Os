# Compatibility — an honest guide

AURA OS is a Linux system for ARM64. Most of the Linux world runs
beautifully here — but not everything from other platforms does.

## What runs natively

- **Thousands of Debian ARM64 packages** via App Center / APT
- **Flatpaks** from Flathub (ARM64 builds)
- **Web apps** in AURA Browser (Firefox ESR or Chromium)
- **Development**: Python, Node.js, Go, Rust, GCC/Clang, Docker (ARM64)

## macOS software

macOS applications **cannot run inside AURA** — they need macOS itself.
Your Mac is right there: keep macOS apps in macOS, share files through
a UTM shared folder, and use AURA for everything Linux does well.

## Windows software

Windows `.exe` files do not run natively. Options, in order:

1. **Linux version or web version** of the same app (very common now)
2. **A free alternative** — LibreOffice for Office files, GIMP/Krita for
   images, Kdenlive for video
3. **Wine** for some Windows programs (results vary; check winehq.org).
   Note: on ARM64, Wine needs x86 emulation (Box86/FEX) for 32/64-bit
   Windows binaries — advanced territory.
4. **A separate Windows-on-ARM VM** in UTM for software that truly needs it

## Architecture matters

Downloads must say **arm64 / aarch64**. An `amd64` or `x86_64` .deb or
AppImage will refuse to run — `aura system` shows your architecture.
