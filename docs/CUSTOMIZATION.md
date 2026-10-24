# Customizing AURA OS

Everything is changeable from **AURA Settings** (visual, live preview) or
from **Celestia Shell** via `aura` — both write the same config
(`~/.config/aura/config.json`), so they never disagree. Changes apply
instantly and survive reboots.

## Appearance

| Want | GUI | CLI |
|---|---|---|
| Light/Dark | Settings → Appearance → Mode | `aura theme light` |
| Accent color | swatches or custom picker | `aura theme accent glacier`, `aura theme blue`, any `#hex` |
| Wallpaper | Settings → Wallpaper grid | `aura wallpaper set <name\|path>` |
| Icon theme | Settings → Appearance | saved to xsettings (`/Net/IconThemeName`) |
| Cursor theme | Settings → Appearance | (`/Gtk/CursorThemeName`, next login) |
| Font / size | font picker | (`/Gtk/FontName`) |
| Text scaling | slider (0.8–2.0×) | (`/Xft/DPI`) |
| Restore defaults | button | `aura theme reset` |

Under the hood, accent changes copy the active theme to `~/.themes/AuraCustom`
and rewrite its `accent.css`; GTK3, GTK4 and xfwm4 all read from it, so one
action re-skins windows, menus, the panel and the window buttons together.

## Dock & menu bar

- **Dock**: Settings → Dock, or `aura dock size|position|zoom|autohide`.
  Right-click the dock for Plank's own preferences; drag icons to rearrange;
  drag apps from the AURA menu to pin them (stored in
  `~/.config/plank/dock1/launchers/`).
- **Menu bar**: height slider in Settings; right-click the bar → Panel
  Preferences for applets. The AURA logo button opens Whisker Menu —
  favorites and search actions (`?` web, `#` files, `!` run, `aura` commands)
  are editable in `~/.config/xfce4/panel/whiskermenu-1.rc`.

## Effects & performance

Settings → Effects toggles the compositor, window/popup shadows, snapping,
tiling, Super+scroll zoom and GTK animations (writes
`~/.config/gtk-3.0/settings.ini`). Turning shadows/transparency off is the
biggest speed-up inside a VM.

## Celestia Shell

Settings → Celestia Shell: font, background opacity (transparency over your
wallpaper), color scheme, and login shell (zsh/bash). For prompt/alias-level
tweaks edit `~/.zshrc` — it loads *after* `/etc/celestia/zshrc`, so your
lines always win and OS updates never overwrite them.

## Desktop & widgets

- Files/folders/shortcuts on the desktop: just create them in `~/Desktop`.
- Widgets: **AURA Widgets** (Conky) shows a glassy clock + CPU/RAM/disk
  glance; enable at login in Settings → Session and Startup, edit
  `~/.config/conky/aura.conkyrc` to make it yours.
- Workspaces: four by default (Summit · Ridge · Valley · Glacier) — rename
  or rescale in Settings Manager → Workspaces.

## File manager

AURA Finder (Thunar): tabs (Ctrl+T), split view (F3), view modes, sidebar
bookmarks (drag folders in), custom actions (Edit → Configure custom
actions), default apps via right-click → Open With → Set as default.

## Advanced theming

Themes are **generated** from design tokens (`tools/generate_themes.py`):
edit two palettes, regenerate, and both GTK3/GTK4 sheets update. Window
decorations (`tools/generate_xfwm4.py`) and icons
(`tools/generate_icons.py`) work the same way — fork the generators to make
a wholly new look, then re-run `installer/install-aura.sh` to apply it.
