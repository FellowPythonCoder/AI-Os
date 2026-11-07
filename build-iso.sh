#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ $(uname -s) != Linux || $(uname -m) != aarch64 ]]; then
  echo 'Build on aarch64 Linux, or run ./build-iso-docker.sh on an Apple Silicon Mac.' >&2
  exit 1
fi
if ! command -v nix >/dev/null 2>&1; then
  echo 'Nix is required; see MILESTONE-1.md for installation instructions.' >&2
  exit 1
fi
# Make a clean source snapshot without previous images, Git metadata or result
# symlinks. path: supports uncommitted changes but would otherwise copy output/
# into the Nix store (including a potentially multi-gigabyte old ISO).
source_dir=$(mktemp -d "${TMPDIR:-/tmp}/auraos-source.XXXXXXXX")
trap 'rm -rf -- "$source_dir"' EXIT
tar --exclude='./.git' --exclude='./output' --exclude='./result' \
  --exclude='./result-*' -cf - . | tar -xf - -C "$source_dir"
result=$(nix --extra-experimental-features 'nix-command flakes' build \
  --show-trace --no-write-lock-file --no-link --print-out-paths \
  "path:$source_dir#nixosConfigurations.auraos-iso.config.system.build.isoImage")
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
