#!/usr/bin/env bash
# macOS host launcher; the actual Nix build happens in a Linux container.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ $(uname -s) != Darwin || $(uname -m) != arm64 ]]; then
  echo 'This launcher requires an Apple Silicon Mac. On aarch64 Linux run ./build-iso.sh instead.' >&2
  exit 1
fi
if ! command -v docker >/dev/null 2>&1; then
  echo 'Docker CLI not found. Install and start Docker Desktop, then retry.' >&2
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo 'Docker Desktop is not ready. Run: open -a Docker' >&2
  echo 'Wait until Docker Desktop says it is running, then retry.' >&2
  exit 1
fi
mkdir -p output
printf '%s\n' 'Starting an ARM64 Linux Nix container. The first build can take a long time.'
printf '%s\n' 'Nix sandboxing is disabled inside the container; only build trusted code.'
# Keep the container ephemeral; no privileged mode and no access to Docker's
# socket inside the container. The ISO is copied to the host bind mount.
exec docker run --rm --platform linux/arm64 \
  --mount "type=bind,source=$PWD,target=/workspace" \
  --workdir /workspace \
  -e 'NIX_CONFIG=sandbox = false' \
  nixos/nix:latest /bin/sh -c './build-iso.sh'
