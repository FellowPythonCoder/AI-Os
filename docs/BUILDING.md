# Building AURA OS

All builds need an **ARM64 Debian/Ubuntu host** (a Linux VM on your Mac
works perfectly, as does GitHub's `ubuntu-24.04-arm` runner). Builds
download the Debian archive, so they're large (completed ISO ≈ 2.5–3 GB).

## 0. Test first (any machine, seconds)

```bash
./tests/run-tests.sh
```

Runs Python/shell syntax checks, 17 unit tests (the `aura` CLI end-to-end
against throwaway configs, asset/XML/JSON validation, generator
reproducibility) and a full installer `--dry-run`.

## 1. Installer ISO (live-build)

```bash
sudo apt install live-build rsync
sudo ./build/build-iso.sh
# → build/out/AURA-OS-1.0-arm64.iso  (+ .sha256, build-iso.log)
```

What it does: assembles `build/live/config` (package lists from
`build/packages/`, AURA overlay into `includes.chroot`, Calamares branding,
a chroot hook running `/usr/share/aura/finalize.sh --skip-boot --live`), then
`lb config` (Debian bookworm, arm64, grub-efi, live user `aura`) and `lb build`.

## 2. Preinstalled disk image (debos)

```bash
sudo apt install debos qemu-utils
./build/build-image.sh
# → build/out/AURA-OS-1.0-arm64.img, .qcow2, .sha256
```

What it does: renders `build/debos/aura.yaml` from the shared package lists
(`tools/render_debos_recipe.py`), then debos partitions a 12 GB GPT image
(ESP + ext4 root, grows on first boot via `x-systemd.growfs`), debootstraps
Debian, installs packages, applies the overlay, installs GRUB (UEFI,
removable-media path), creates user `aura`/`aura` (**forced password change
on first login**) and runs `finalize.sh`. Override the debos backend with
`DEBOS_BACKEND=qemu` on hosts without `/dev/kvm`.

## 3. Transform an existing Debian (no image build)

```bash
sudo ./installer/install-aura.sh --user "$USER"     # add --dry-run to preview
```

See [INSTALL-UTM.md](INSTALL-UTM.md) Route C. This is also how AURA is
developed day-to-day: edit `rootfs/`, re-run the installer, done.

## CI

| Workflow | Trigger | What |
|---|---|---|
| `ci.yml` | every push/PR | tests, shellcheck, desktop-file & XML validation, **generated-asset drift check** (re-runs all `tools/` generators and fails if the tree changes) |
| `build-image.yml` | manual / tags `v*` | debos image on `ubuntu-24.04-arm`; uploads artifact, attaches to releases |
| `build-iso.yml` | manual / tags `v*` | live-build ISO on `ubuntu-24.04-arm`; uploads artifact, attaches to releases |

## Regenerating assets

Icons, cursors, themes, xfwm4 decorations, sounds, desktop files and the
debos recipe are **generated** and committed. After editing a generator:

```bash
python3 tools/generate_icons.py          # + cursors/themes/xfwm4/sounds/…
python3 tools/render_debos_recipe.py
git add -A && git commit
```

CI enforces that committed assets match generator output exactly.

## Verifying artifacts

```bash
cd build/out && sha256sum -c AURA-OS-1.0-arm64.sha256
qemu-img check AURA-OS-1.0-arm64.qcow2
```
