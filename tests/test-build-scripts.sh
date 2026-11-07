#!/usr/bin/env bash
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/work/nixos" "$tmp/bin" "$tmp/store/iso" "$tmp/work/.git" "$tmp/work/output"
cp "$repo/build-iso.sh" "$repo/build-iso-docker.sh" "$repo/flake.nix" "$tmp/work/"
cp "$repo/nixos/"*.nix "$tmp/work/nixos/"
printf old > "$tmp/work/output/old.iso"
printf secret > "$tmp/work/.git/config"
printf 'fake iso' > "$tmp/store/iso/auraOS-1.0-aarch64.iso"
cat > "$tmp/bin/uname" <<'MOCK'
#!/usr/bin/env bash
if [[ ${MOCK_PLATFORM:-linux} == mac ]]; then
  [[ $1 == -s ]] && echo Darwin || echo arm64
else
  [[ $1 == -s ]] && echo Linux || echo aarch64
fi
MOCK
cat > "$tmp/bin/nix" <<'MOCK'
#!/usr/bin/env bash
for arg in "$@"; do case "$arg" in path:*) src=${arg#path:}; src=${src%%#*};; esac; done
[[ -f "$src/flake.nix" && -f "$src/nixos/desktop.nix" ]]
[[ ! -e "$src/.git" && ! -e "$src/output" ]]
printf '%s\n' "$FAKE_STORE"
MOCK
cat > "$tmp/bin/docker" <<'MOCK'
#!/usr/bin/env bash
if [[ $1 == info ]]; then exit "${MOCK_DOCKER_FAIL:-0}"; fi
printf '%s\n' "$@" > "$DOCKER_ARGS"
MOCK
chmod +x "$tmp/bin/"*
export PATH="$tmp/bin:$PATH" FAKE_STORE="$tmp/store" DOCKER_ARGS="$tmp/docker-args"
(cd "$tmp/work" && ./build-iso.sh)
(cd "$tmp/work/output" && sha256sum -c auraOS-1.0-aarch64.iso.sha256)
(cd "$tmp/work" && MOCK_PLATFORM=mac ./build-iso-docker.sh)
grep -Fxq 'linux/arm64' "$DOCKER_ARGS"
grep -Fxq 'nixos/nix:latest' "$DOCKER_ARGS"
if (cd "$tmp/work" && MOCK_PLATFORM=mac MOCK_DOCKER_FAIL=1 ./build-iso-docker.sh); then
  echo 'Expected Docker readiness check to fail' >&2; exit 1
fi
printf 'Mock launcher tests passed. A real Nix build and Docker/UTM run were not tested.\n'
