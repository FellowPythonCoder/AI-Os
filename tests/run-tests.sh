#!/bin/bash
# Run the AURA OS test suite (CLI, assets, scripts, syntax).
set -u
set -o pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1
FAIL=0

echo "🏔  AURA OS tests"
echo

echo "▶ Python syntax (all AURA programs + tools)"
for f in rootfs/usr/bin/aura rootfs/usr/bin/aura-* tools/*.py tests/*.py; do
    python3 -m py_compile "$f" || { echo "  ✗ $f"; FAIL=1; }
done
echo "  ✓ done"

echo "▶ Shell syntax"
for f in installer/*.sh build/*.sh rootfs/usr/bin/celestia-tutorial \
         rootfs/usr/share/aura/*.sh tests/*.sh; do
    bash -n "$f" || { echo "  ✗ $f"; FAIL=1; }
done
echo "  ✓ done"

if command -v shellcheck >/dev/null 2>&1; then
    echo "▶ shellcheck"
    shellcheck -S warning installer/*.sh build/*.sh tools/*.sh \
        rootfs/usr/bin/celestia-tutorial || FAIL=1
fi

echo "▶ Unit tests"
python3 -m unittest discover -s tests 2>&1 | tail -5 || FAIL=1

echo "▶ Installer dry-run (if sudo available)"
if sudo -n true 2>/dev/null; then
    sudo ./installer/install-aura.sh --dry-run --user "$(id -un)" >/dev/null 2>&1 \
        && echo "  ✓ dry-run clean" || { echo "  ✗ dry-run failed"; FAIL=1; }
else
    echo "  (skipped — no passwordless sudo)"
fi

echo
if [ "$FAIL" -eq 0 ]; then
    echo "✓ All tests passed."
else
    echo "✗ Some tests FAILED."
fi
exit "$FAIL"
