#!/usr/bin/env python3
"""
Generate AURA .desktop launchers, Plank dock items and "hide the original"
stubs so menus show one Luna, AURA-branded set of applications.

Each AURA app maps to a REAL program (or to one of AURA's own apps in
rootfs/usr/bin). Run: python3 tools/generate_desktop_files.py
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rootfs")
APPS_DIR = os.path.join(ROOT, "usr", "share", "applications")
DOCK_DIR = os.path.join(ROOT, "etc", "skel", ".config", "plank", "dock1", "launchers")
HIDE_DIR = os.path.join(ROOT, "etc", "skel", ".local", "share", "applications")

# id, Name, Exec, Icon, Comment, Categories, extra-keys
APPS = [
    ("aura-finder", "AURA Finder", "thunar %U", "aura-finder",
     "Browse files, folders and drives", "System;FileTools;FileManager;Utility;Core;",
     {"MimeType": "inode/directory;"}),
    ("celestia-shell", "Celestia Shell",
     'xfce4-terminal --title="Celestia Shell"', "celestia-shell",
     "AURA's command-line environment — try `aura help`",
     "System;TerminalEmulator;Utility;", {}),
    ("celestia-tutorial", "Celestia Tutorial",
     'xfce4-terminal --title="Celestia Tutorial" -e celestia-tutorial',
     "celestia-shell", "A five-minute guided tour of Celestia Shell",
     "System;Utility;Documentation;", {}),
    ("aura-launcher", "AURA Launcher", "aura-launcher", "aura-launcher",
     "Searchable application launcher with Kali and system categories",
     "System;Utility;", {}),
    ("aura-security", "AURA Security Center", "aura-security", "aura-security",
     "Kali Linux and Debian security toolkit manager and launcher",
     "System;Security;Network;", {}),
    ("aura-appbar", "AURA App Bar", "aura-appbar", "aura-appbar",
     "Floating dark-blue glass quick-launch bar and desktop search",
     "System;Utility;", {}),
    ("aura-browser", "AURA Browser", "firefox-esr %u", "aura-browser",
     "Surf the web with Firefox ESR", "Network;WebBrowser;",
     {"MimeType": "text/html;text/xml;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;"}),
    ("aura-settings", "AURA Settings", "aura-settings", "aura-settings",
     "Appearance, wallpaper, dock, terminal and more", "Settings;DesktopSettings;", {}),
    ("aura-appcenter", "AURA App Center", "aura-appcenter", "aura-appcenter",
     "Install, update and remove applications", "System;PackageManager;Settings;", {}),
    ("aura-text", "AURA Text", "mousepad %F", "aura-text",
     "Write notes and edit text files", "Utility;TextEditor;",
     {"MimeType": "text/plain;text/x-chdr;text/x-csrc;text/x-python;"}),
    ("aura-studio", "AURA Studio", "geany %F", "aura-studio",
     "Code editor with projects, Git and a built-in terminal", "Development;IDE;", {}),
    ("aura-notes", "AURA Notes", "aura-notes", "aura-notes",
     "Searchable notes with Markdown support", "Office;Utility;", {}),
    ("aura-calendar", "AURA Calendar", "aura-calendar", "aura-calendar",
     "Calendar, events and reminders", "Office;Calendar;", {}),
    ("aura-calculator", "AURA Calculator", "galculator", "aura-calculator",
     "Standard and scientific calculator", "Utility;Calculator;Math;", {}),
    ("aura-monitor", "AURA Monitor", "aura-monitor", "aura-monitor",
     "Live CPU, memory, disk and network graphs", "System;Monitor;", {}),
    ("aura-photos", "AURA Photos", "ristretto %F", "aura-photos",
     "View and organize your pictures", "Graphics;Photography;Viewer;",
     {"MimeType": "image/png;image/jpeg;image/gif;image/bmp;image/svg+xml;image/webp;image/tiff;"}),
    ("aura-media", "AURA Media", "parole %F", "aura-media",
     "Play music and videos", "AudioVideo;Player;Audio;Video;",
     {"MimeType": "audio/mpeg;audio/ogg;audio/flac;audio/x-wav;video/mp4;video/x-matroska;video/webm;"}),
    ("aura-archive", "AURA Archive", "xarchiver %F", "aura-archive",
     "Create and extract ZIP, TAR, 7z and other archives", "Utility;Archiving;Compression;",
     {"MimeType": "application/zip;application/x-tar;application/x-7z-compressed;application/gzip;application/x-bzip2;application/x-xz;application/x-rar;"}),
    ("aura-screenshot", "AURA Screenshot", "xfce4-screenshooter", "aura-screenshot",
     "Capture the screen, a window or a region", "Utility;Graphics;", {}),
    ("aura-pdf", "AURA PDF", "evince %F", "aura-pdf",
     "Read PDF and other documents", "Office;Viewer;",
     {"MimeType": "application/pdf;application/postscript;image/vnd.djvu;"}),
    ("aura-transfer", "AURA Transfer", "aura-transfer", "aura-transfer",
     "Resumable downloads, checksum verifier and file transfer", "Network;FileTransfer;", {}),
    ("aura-taskmanager", "AURA Task Manager", "xfce4-taskmanager", "aura-taskmanager",
     "See and control running processes", "System;Monitor;", {}),
    ("aura-backup", "AURA Backup", "timeshift-gtk", "aura-backup",
     "System snapshots and restore points (Timeshift)", "System;Archiving;Settings;", {}),
    ("aura-help", "AURA Help", "aura-help", "aura-help",
     "Guides, shortcuts and troubleshooting", "System;Utility;Documentation;", {}),
    ("aura-welcome", "Welcome to AURA", "aura-welcome", "aura-welcome",
     "Set up and personalize AURA OS", "System;Settings;", {}),
    ("aura-firewall", "AURA Firewall", "gufw", "aura-firewall",
     "Firewall rules — what may reach this machine from the network",
     "Settings;Security;Network;", {}),
    ("aura-lock", "AURA Lock Screen", "aura-lock", "aura-lock",
     "Lock the desktop session with AURA Liquid Glass", "System;Security;", {}),
    ("aura-quicksettings", "AURA Quick Settings", "aura-quicksettings", "aura-quicksettings",
     "Liquid Glass control center for network, audio, brightness, theme and power",
     "Settings;DesktopSettings;", {}),
    ("aura-about", "About This AURA", "aura-about", "aura-about",
     "Version, hardware and system information", "System;Settings;", {}),
]

# Original desktop IDs to hide (replaced by the AURA-branded entries above).
HIDE = [
    "thunar.desktop", "xfce4-terminal.desktop", "firefox-esr.desktop",
    "org.xfce.mousepad.desktop", "geany.desktop", "xfcalendar.desktop",
    "galculator.desktop", "org.xfce.ristretto.desktop",
    "org.xfce.Parole.desktop", "xarchiver.desktop",
    "xfce4-screenshooter.desktop", "org.gnome.Evince.desktop",
    "uget-gtk.desktop", "xfce4-taskmanager.desktop", "timeshift-gtk.desktop",
    "thunar-volman-settings.desktop", "org.xfce.thunar.desktop",
]

DOCK_APPS = ["aura-launcher", "celestia-shell", "aura-finder", "aura-browser",
             "aura-security", "aura-studio", "aura-monitor", "aura-appcenter",
             "aura-settings"]


def main():
    os.makedirs(APPS_DIR, exist_ok=True)
    os.makedirs(DOCK_DIR, exist_ok=True)
    os.makedirs(HIDE_DIR, exist_ok=True)
    for app_id, name, exe, icon, comment, cats, extra in APPS:
        lines = ["[Desktop Entry]", "Version=1.0", "Type=Application",
                 f"Name={name}", f"Comment={comment}", f"Exec={exe}",
                 f"Icon={icon}", "Terminal=false", f"Categories={cats}",
                 "StartupNotify=true"]
        for k, v in extra.items():
            lines.append(f"{k}={v}")
        with open(os.path.join(APPS_DIR, app_id + ".desktop"), "w",
                  encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    print(f"{len(APPS)} AURA applications")

    for app_id in DOCK_APPS:
        with open(os.path.join(DOCK_DIR, app_id + ".dockitem"), "w",
                  encoding="utf-8") as fh:
            fh.write("[PlankDockItemPreferences]\n"
                     f"Launcher=file:///usr/share/applications/{app_id}.desktop\n")
    # Trash docklet at the end of the dock
    with open(os.path.join(DOCK_DIR, "trash.dockitem"), "w", encoding="utf-8") as fh:
        fh.write("[PlankDockItemPreferences]\nDockItem=TrashDockItem\n")
    print(f"{len(DOCK_APPS) + 1} dock items")

    for desktop in HIDE:
        with open(os.path.join(HIDE_DIR, desktop), "w", encoding="utf-8") as fh:
            fh.write("[Desktop Entry]\nType=Application\nName=Hidden by AURA\n"
                     "NoDisplay=true\n")
    print(f"{len(HIDE)} originals hidden")


if __name__ == "__main__":
    main()
