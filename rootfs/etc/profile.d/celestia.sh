# Celestia Shell — login-shell integration for AURA OS (bash/sh sessions).
# Zsh users get the full experience from /etc/celestia/zshrc; this gives
# bash users the same AURA shortcuts.

if [ -n "$BASH_VERSION" ] && [ -z "$CELESTIA_BASH_DONE" ]; then
    CELESTIA_BASH_DONE=1
    alias ll='ls -alF --color=auto' 2>/dev/null
    alias open='aura open' 2>/dev/null
    alias help-me='aura help' 2>/dev/null
fi

# Prefer AURA's helpers for every login shell.
export AURA_OS=1
