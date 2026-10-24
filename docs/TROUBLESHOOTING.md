# Troubleshooting AURA OS

**Always first:** open Celestia Shell and run **`aura doctor`**. It checks
disk space, guest RAM pressure, internet reachability, UTM guest tools and
service health, and prints the exact fix for each problem it finds.

## Installation & boot

**Black screen / no graphical boot in UTM**
The VM must be **ARM64 "Virtualize"**, not x86 "Emulate". AURA images are
ARM64-only. Recreate the VM (Virtualize → Linux). Also give it ≥ 4 GB RAM.

**"No bootable device" / drops to UEFI shell**
- ISO route: the ISO must be attached (Edit → Drives → CD/DVD shows the file).
- Image route: the imported qcow2 must be first in the drive list and use
  NVMe/VirtIO interface. If UEFI still can't find it, in the UEFI menu choose
  *Boot Maintenance Manager → Boot From File → EFI → BOOT → BOOTAA64.EFI*
  (AURA installs GRUB at the removable-media path precisely for this).

**GRUB menu doesn't appear / need recovery mode**
Hold **Esc** right after starting the VM.

**Forgot the password**
Esc → *Advanced options → recovery mode* → root shell →
`passwd YOURUSERNAME` → `reboot`.

**Stuck at Plymouth (boot splash) for minutes**
Press Esc to see boot messages. Usual culprits: full disk
(recovery console → `aura clean --yes` won't run without the CLI loaded —
use `apt-get clean` and empty `~/.cache`), or a bad `/etc/fstab` entry after
drive changes (`journalctl -xb` shows it; comment the line out).

## Desktop & display

**Display doesn't resize with the UTM window / blurry text**
`aura install spice-vdagent`, log out/in. In UTM preferences for the VM,
enable the Retina/high-resolution display option; then
AURA Settings → System → Display to confirm the mode.

**Dock or menu bar missing**
`aura open celestia-shell` (or Ctrl+Alt+T), then: `plank &` restarts the
dock; `xfce4-panel -r` restarts the menu bar. If it recurs, check
`~/.xsession-errors`.

**A theme experiment went too far**
`aura theme reset` restores AURA defaults instantly. Nuclear option:
re-run `sudo ./installer/install-aura.sh --user "$USER"` — it's idempotent
and never touches your documents.

**Window buttons disappeared after changing theme**
The xfwm4 theme must match: `aura theme dark` (or light) re-applies both
the GTK and window-manager themes together.

## UTM integration

**Clipboard doesn't cross between Mac and AURA**
UTM (VM off or running): Edit → Sharing → *Enable Clipboard Sharing*.
In AURA: `aura doctor` — it verifies `spice-vdagent`; install + re-login
if prompted.

**Shared folder not visible**
UTM → Edit → Sharing → Directory Share must list a folder. In AURA it
appears via SPICE WebDAV/virtio-9p: check AURA Finder → Network, or
`ls /media` and `mount | grep -i 9p`. `spice-webdavd` (optional package)
improves WebDAV sharing: `aura install spice-webdavd`.

**No sound**
UTM sound device on; in AURA click the volume icon → ensure the output
isn't muted; `pavucontrol` for per-app routing (PipeWire).

## Performance on a 16 GB Mac

- 4–6 GB RAM / 4 cores is the sweet spot; more starves macOS.
- Settings → Effects: compositor **off** is the biggest FPS win.
- Close heavy tabs/apps; check AURA Monitor — remember its RAM graph is
  the *guest's* allocation.
- UTM snapshots are cheap: snapshot before experiments, delete after wins.

## Packages & updates

**`aura install x` says "Unable to locate package"**
Run `aura update` first; check spelling with `aura search`. Package names
are lowercase and must exist for **arm64**. The App Center's repository
search shows the same data.

**An update wants to replace `/etc/os-release` etc.**
Normal Debian behavior for `base-files`. Keeping the *installed* (AURA)
version is safe; re-running the AURA installer also restores branding.

**Flatpak "No remote refs found"**
`flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo`
then retry (the installer normally does this; it can fail without network).

## Still stuck?

- `aura system` output + a description → open an issue:
  https://github.com/FellowPythonCoder/AI-Os/issues
- The in-OS guide has more: **AURA Help → Troubleshooting**.
