# Experimental desktop image — not release-ready

The default flake target now attempts to start Hyprland and Caelestia on the
live image, with upstream Caelestia Hyprland dotfiles, a greetd autologin,
PipeWire, NetworkManager and a small app set. This is **unbuilt, untested
integration code**, not a finished OS or a verified UTM image. In particular,
the configuration may fail evaluation, fail to build, or fail to start a
session. Upstream Lua Hyprland configuration requires compatible Hyprland and
Caelestia versions. This repository does not yet include a checked-in flake
lock; the top-level sources are pinned to revisions, while transitive inputs
come from the shell's upstream lock. Verify and commit a lock file after the
first successful evaluation.

**Not implemented or verified:** Calamares and an installable disk system,
first-boot user setup, safe-graphics entry, shared folders, graphical clipboard
and dynamic resolution, boot splash, default wallpaper and dynamic colors,
complete dark theme, aurapkg, comprehensive dependencies, performance targets,
or any of the requested UTM smoke tests. The upstream dots contain Arch-specific
commands and paths; some features will not work on NixOS without adaptation.
The live user is passwordless and must not be treated as a secure install.
Do not use this ISO for production or to install onto a disk.

Mac Docker build instructions are in [DOCKER-BUILD.md](DOCKER-BUILD.md).
Native Linux build and UTM instructions are in [MILESTONE-1.md](MILESTONE-1.md), but the
expected result is now an **attempted graphical session**, rather than the
console-only milestone described there. The build needs access to GitHub,
Nix's binary cache and the shell's Quickshell source at git.outfoxxed.me.
The upstream shell's README documents its package and dependencies. Its
[project](https://github.com/caelestia-dots/shell),
[dotfiles](https://github.com/caelestia-dots/caelestia), Quickshell and
Hyprland are third-party projects, with their own licenses and credits. Their
respective licenses apply; this is not a claim of affiliation.
