# Celestia Shell — complete guide

Celestia Shell is AURA OS's terminal: a deep-blue xfce4-terminal running
**Zsh** with syntax highlighting, autosuggestions, substring history search
and the **`aura`** command — AURA's friendly control panel for the keyboard.

Open it with `Super + Enter`, `Ctrl + Alt + T`, or from the dock.
New here? Type **`aura tutorial`** — 6 hands-on lessons, 5 minutes, safe
(all practice runs with `--dry-run` or read-only commands).

## The aura command

| Command | What it does |
|---|---|
| `aura help` | The built-in command guide |
| `aura version` / `aura fetch` | Version / logo + system summary |
| `aura system [--json]` | OS, kernel, CPU, **guest RAM**, disk, virtualization, uptime |
| `aura apps [--search text]` | List/filter installed applications |
| `aura open <app\|file\|url>` | Launch an app by name/ID, open a file or URL |
| `aura settings [page]` | Open AURA Settings |
| `aura tutorial` | Interactive tour |
| `aura doctor` | Health checks (disk, RAM, network, UTM tools) with fixes |
| `aura backup` | Open AURA Backup (Timeshift) |

### Appearance

```bash
aura theme light | dark | auto      # mode
aura theme list                     # modes & accents
aura theme accent glacier           # accents: ocean electric glacier midnight cyan teal violet
aura theme accent "#ff8800"         # any color
aura theme blue                     # shortcut for the classic AURA blue
aura theme reset                    # back to AURA defaults

aura wallpaper list
aura wallpaper set aura-aurora-ridge
aura wallpaper set ~/Pictures/lake.jpg

aura dock                           # show current dock settings
aura dock size 64                   # 24–128 px
aura dock position left             # bottom|left|right|top
aura dock zoom on|off
aura dock autohide on|off
```

Changes write `~/.config/aura/config.json` and apply via xfconf/gsettings,
so AURA Settings (GUI) always shows the same state. Accent switching rebuilds
a per-user `AuraCustom` GTK theme with a fresh `accent.css` — the whole OS,
including window borders, follows instantly.

### Software (real APT & Flatpak)

```bash
aura search photo editor        # apt-cache search, friendliest first 40
aura install gimp inkscape      # sudo apt-get install (explains first)
aura install --flatpak org.signal.Signal
aura remove gimp
aura update                     # refresh lists, list what's upgradable
aura upgrade                    # install all updates
aura clean                      # preview cleanup sizes
aura clean --yes                # empty Trash + apt autoclean/autoremove + journal vacuum
```

Add `--dry-run` to install/remove/upgrade/update to print the exact command
without running it. Everything system-changing asks for your password — AURA
never runs downloads as root silently.

### Session

```bash
aura session lock | logout | suspend | reboot | shutdown
```

## Everyday Linux

Celestia is a real shell: `ls cd mkdir cp mv rm cat grep find`, pipes and
redirects, `git`, `python3`, `node`, `ssh`, `scp`, `curl`, `wget`, `tar`,
`make`, `gcc`… all present or one `aura install` away. Scripts work too:
`chmod +x script.sh && ./script.sh`.

Handy AURA extras defined in `/etc/celestia/zshrc`:

- `ll`, `la`, `..`, `...`, `gs` (git status), `open` (= `aura open`)
- `afetch`, `ainstall`, `asearch`, `aupdate`, `help-me` (= `aura help`)
- `mkcd dir` — make a folder and step into it
- `extract file.zip` — unpack zip/tar/7z/deb/gz…
- `celestia` — show the welcome banner again

## Keyboard

| Keys | Action |
|---|---|
| Tab / Tab Tab | Complete / open completion menu |
| ↑ ↓ (after typing) | History matching the typed prefix |
| Ctrl + R | Search all history |
| Ctrl + Shift + T / W | New / close tab |
| Ctrl + Shift + C / V | Copy / paste |
| Right-click | Split panes, profiles, preferences |

## Customizing Celestia

Colors/fonts/opacity: **AURA Settings → Celestia Shell** (writes
`~/.config/xfce4/terminal/terminalrc`). Color schemes live in
`/usr/share/xfce4/terminal/colorschemes/` — "Celestia" is the signature one.
Shell behavior: edit `~/.zshrc` (your file; system defaults are in
`/etc/celestia/zshrc` and load first, so updates never clobber you).
Prefer bash? Settings → Celestia Shell → "Use bash", or `chsh -s /bin/bash`.

Completions for `aura` ship for both shells
(`/usr/share/zsh/vendor-completions/_aura`, bash-completion dir) and can be
regenerated anytime: `aura completion zsh|bash`.
