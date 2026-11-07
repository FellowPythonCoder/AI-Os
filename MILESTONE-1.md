> **Superseded:** the default target now attempts an experimental desktop, not the minimal image documented below. See [DESKTOP-STATUS.md](DESKTOP-STATUS.md) for limitations. The build commands still apply.

# auraOS — milestone 1: minimal ARM64 UEFI live ISO

**Status: source prepared; not built or boot-tested.** The current target
attempts a live desktop but has no graphical installer, wallpaper, or disk setup
wizard yet. Do not use it to install a finished desktop. Hardware acceleration,
boot time and RAM targets have not been measured. Those belong to later
milestones, after this image has been built and tested in UTM.

The flake pins nixpkgs to commit `1c89083e451e891152365b799595cf7790a43325`
(the revision selected by the pinned Caelestia shell). The build script
resolves that exact revision without writing a lock file. Commit pinning avoids
moving branch inputs; a checked-in lock file and pinned desktop inputs are
still needed as the flake grows. The upstream minimal installation CD module
provides the ARM64 EFI boot image and virtio-compatible hardware detection.
We deliberately do not trim drivers before confirming that it boots.

## Build on aarch64 Linux

Use an ARM64 Linux machine or an **aarch64 NixOS VM in UTM**, with internet,
working DNS, sufficient free disk space (at least 30 GB recommended), and
4–8 GB RAM. macOS itself is not a supported build host for this script.
Binary cache access to `cache.nixos.org` is recommended; without it the build
may need to compile substantial dependencies.

On NixOS, Nix is already installed. On another Linux distribution, install
Nix using the official multi-user installer, after reviewing its instructions:

```sh
curl -L https://nixos.org/nix/install -o /tmp/install-nix
sh /tmp/install-nix --daemon
# Open a new login shell so Nix is on PATH, then verify:
nix --version
```

The installer requires sudo and supported system prerequisites. See
https://nix.dev/install-nix for distribution-specific details. Then, in this
repository:

```sh
./build-iso.sh
```

The checksum file contains the basename, so verify it from its directory:

```sh
(cd output && sha256sum -c auraOS-1.0-aarch64.iso.sha256)
```

The script prints the ISO path, byte size and SHA-256, and writes the image
and checksum into `output/`. The name is the requested eventual release name,
but this milestone image is **not** a 1.0 release. Build failures should not be
interpreted as a successful release. Nix downloads inputs on the first run.

## UTM boot test on Apple Silicon

1. Create a new VM in UTM using **Virtualize**, Linux, ARM64, and UEFI (not
   legacy BIOS). Attach `output/auraOS-1.0-aarch64.iso` as the boot ISO.
2. Allocate 4 CPU cores, 4–8 GB RAM, and a virtual disk (e.g. 32 GB). Use
   virtio networking and storage. For this console milestone, a standard
   virtual display is sufficient; GPU acceleration is not verified yet.
3. Start the VM and choose the default NixOS boot entry. If the ISO does not
   start, check that the VM is ARM64, uses UEFI, and actually boots from the
   attached CD/DVD. UTM's UI labels vary by version.
4. The image attempts an automatically logged-in graphical session. If it fails, try switching to a text console (Ctrl+Alt+F2) and log in as `nixos` with an empty password.
   Check:

   ```sh
   uname -m                 # aarch64
   test -d /sys/firmware/efi && echo UEFI
   cat /etc/os-release
   ip link                   # virtio network device present
   lsblk                     # installation ISO and virtual disk present
   systemctl is-system-running
   ```

   Run these commands in a terminal or text console. The last command may report `degraded`; inspect failed units with
   `systemctl --failed` and logs with `journalctl -b -p warning`. Network
   reachability depends on the VM's network configuration. Power off with
   `sudo poweroff`.

The upstream installer uses blank-password live accounts and passwordless
sudo; treat it as an ephemeral, untrusted live environment, not a secured
installed system. Do not expose it to untrusted networks. No disk is modified
by these checks; actual installation is outside this milestone.

## Troubleshooting

- **No bootable device / EFI shell:** verify ARM64 Virtualize mode, UEFI,
  boot order and ISO attachment; rebuild if the ISO copy is incomplete.
- **Black display:** wait for boot, check UTM display settings and try a
  standard non-accelerated display. This stage does not test graphical drivers.
- **No network:** check UTM's network attachment and `ip link`,
  `nmcli device status`, and `journalctl -b -u NetworkManager`.
- **Build fails:** check `uname -m`, free space, connectivity to GitHub and the
  Nix binary cache, and Nix daemon status. Retain the complete error log.

Report the build output, checksum, UTM version, VM configuration and boot
results before proceeding to milestone 2.
