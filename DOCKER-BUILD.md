# Build the experimental ISO on Apple Silicon with Docker Desktop

The image is **experimental and has not been built or boot-tested** in this
project. The desktop and installer are not finished; see [DESKTOP-STATUS.md](DESKTOP-STATUS.md).
The Docker launcher builds for ARM64 Linux inside Docker Desktop's Linux VM,
not for macOS. A successful build is not proof that it boots or that the GUI
works in UTM.

## Requirements

- Apple Silicon Mac with Docker Desktop installed and started; Docker must be
  able to access the repository folder (Docker Desktop Settings → Resources →
  File Sharing, if necessary).
- Internet access to Docker Hub, GitHub, `cache.nixos.org` and
  `git.outfoxxed.me` (Quickshell's upstream Git host). A build can still fail
  if a binary cache does not have a needed ARM64 package.
- Allow Docker Desktop ample resources: at least 4 CPUs, 8 GB RAM and 40 GB
  of free Docker disk-image space, plus enough host disk for the final ISO.
  More may be necessary. Settings vary between Docker Desktop versions.

## Commands

If you have already cloned this repository, update it first:

```sh
cd ~/Downloads/AI-Os
git pull --ff-only origin arena/f25a0ff6-ai-os
open -a Docker
```

Wait until Docker Desktop has finished starting (or `docker info` succeeds),
then run:

```sh
./build-iso-docker.sh
```

The launcher checks Docker, starts `nixos/nix:latest` as a **linux/arm64**
container and runs `build-iso.sh` inside it. Unlike a plain Ubuntu image, this
container already has Nix. The build disables Nix's build sandbox inside the
container for Docker compatibility: only build trusted sources. The image is
not pinned, so Nix client versions can change. The container is removed after
the build; its Nix store is not retained, so reruns may download again.

**Only if the build succeeds**, it prints the ISO's size and SHA-256 and writes:

```text
output/auraOS-1.0-aarch64.iso
output/auraOS-1.0-aarch64.iso.sha256
```

Verify using macOS's `shasum` (not `sha256sum`, which macOS does not include
by default):

```sh
(cd output && shasum -a 256 -c auraOS-1.0-aarch64.iso.sha256)
```

If the build fails, the output directory may be empty or contain an older ISO.
Do not use an old ISO as evidence that the latest build succeeded. Copy the
full error output (including `--show-trace`) when reporting a failure.

## UTM

Create an Apple Silicon **Virtualize** ARM64 Linux VM with UEFI, 4 cores,
4–8 GB memory and a virtual disk, and attach the ISO as the boot image. It is
an unverified live image, **not a disk installer**. See [MILESTONE-1.md](MILESTONE-1.md)
for diagnostic commands. Do not install it on a disk or use it as a production OS.

## Troubleshooting

- **Cannot connect to Docker:** start Docker Desktop with `open -a Docker`,
  wait for it to finish starting, then run `docker info` and retry.
- **Mount denied:** share the repository's parent folder in Docker Desktop.
- **No space left:** increase Docker Desktop's disk image limit and free up
  host disk space; removing a container does not reclaim other Docker images.
- **Network or fetching error:** check access to the hosts listed above and
  retry. The full build error may identify an additional upstream source.
- **`attribute 'tuigreet' missing`:** update this branch. The package is
  `pkgs.tuigreet`, not `pkgs.greetd.tuigreet` in the pinned nixpkgs.
- **Black screen after boot:** this is not a tested graphics configuration;
  check UTM's display settings and switch to a text console to inspect logs.
