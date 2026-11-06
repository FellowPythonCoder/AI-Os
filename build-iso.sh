#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ $(uname -s) != Linux || $(uname -m) != aarch64 ]]; then
  echo 'Build on an aarch64 Linux machine or aarch64 NixOS VM.' >&2
  exit 1
fi
if ! command -v nix >/dev/null 2>&1; then
  echo 'Nix is required; see MILESTONE-1.md for installation instructions.' >&2
  exit 1
fi
# path: includes untracked working-tree files, unlike a local Git flake.
# The sole input is pinned to a commit; do not modify the checkout on build.
result=$(nix --extra-experimental-features 'nix-command flakes' build \
  --no-write-lock-file --no-link --print-out-paths \
  "path:$PWD#nixosConfigurations.auraos-iso.config.system.build.isoImage")
source_iso="$result/iso/auraOS-1.0-aarch64.iso"
if [[ ! -f "$source_iso" ]]; then
  echo "Expected ISO not found: $source_iso" >&2
  exit 1
fi
mkdir -p output
cp -- "$source_iso" output/auraOS-1.0-aarch64.iso
chmod u+w output/auraOS-1.0-aarch64.iso
printf '\nISO: %s\n' "$PWD/output/auraOS-1.0-aarch64.iso"
wc -c < output/auraOS-1.0-aarch64.iso | awk '{print "Size: " $1 " bytes"}'
(cd output && sha256sum auraOS-1.0-aarch64.iso | tee auraOS-1.0-aarch64.iso.sha256)
