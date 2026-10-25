#!/usr/bin/env python3
"""
Unit/smoke tests for the `aura` CLI. Run from the repo root:

    python3 -m unittest discover -s tests -v
    # or:  ./tests/run-tests.sh
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     ".."))
AURA = os.path.join(REPO, "rootfs", "usr", "bin", "aura")


def run_aura(args, tmp):
    env = dict(os.environ)
    env.update({
        "AURA_CONFIG_DIR": os.path.join(tmp, "config", "aura"),
        "AURA_HOME_THEMES": os.path.join(tmp, ".themes"),
        "AURA_SHARE_DIR": os.path.join(REPO, "rootfs", "usr", "share"),
        "NO_COLOR": "1",
    })
    return subprocess.run([sys.executable, AURA] + args, capture_output=True,
                          text=True, env=env, timeout=30)


class AuraCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="aura-test-")

    def cli(self, *args):
        return run_aura(list(args), self.tmp)

    def test_help_and_version(self):
        r = self.cli("help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Celestia Shell", r.stdout)
        self.assertIn("aura install firefox", r.stdout)
        r = self.cli("version")
        self.assertIn("AURA OS", r.stdout)

    def test_system_json(self):
        r = self.cli("system", "--json")
        self.assertEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        for key in ("os", "kernel", "arch", "ram_total_gib", "cpu_cores"):
            self.assertIn(key, d)
        self.assertGreater(d["cpu_cores"], 0)

    def test_apps_discovers_aura_suite(self):
        r = self.cli("apps")
        self.assertEqual(r.returncode, 0)
        for app in ("AURA Finder", "Celestia Shell", "AURA App Center",
                    "AURA Settings", "AURA Monitor", "AURA Notes"):
            self.assertIn(app, r.stdout)

    def test_open_dry_run(self):
        r = self.cli("open", "--dry-run", "celestia-shell")
        self.assertEqual(r.returncode, 0)
        self.assertIn("dry-run", r.stdout)
        r = self.cli("open", "--dry-run", "definitely-not-an-app-xyz")
        self.assertEqual(r.returncode, 1)

    def test_theme_accent_applies_and_persists(self):
        r = self.cli("theme", "accent", "glacier")
        self.assertEqual(r.returncode, 0, r.stderr)
        cfg = json.load(open(os.path.join(
            self.tmp, "config", "aura", "config.json"), encoding="utf-8"))
        self.assertEqual(cfg["accent"], "glacier")
        # per-user theme copy with a rewritten accent.css must exist
        accent_css = os.path.join(self.tmp, ".themes", "AuraCustom",
                                  "gtk-3.0", "accent.css")
        self.assertTrue(os.path.isfile(accent_css))
        self.assertIn("#38b6e8", open(accent_css, encoding="utf-8").read())

    def test_theme_blue_shortcut_and_reset(self):
        self.assertEqual(self.cli("theme", "blue").returncode, 0)
        self.assertEqual(self.cli("theme", "light").returncode, 0)
        self.assertEqual(self.cli("theme", "reset").returncode, 0)
        cfg = json.load(open(os.path.join(
            self.tmp, "config", "aura", "config.json"), encoding="utf-8"))
        self.assertEqual(cfg["theme_mode"], "dark")
        self.assertEqual(cfg["accent"], "ocean")

    def test_wallpaper_list_and_set(self):
        r = self.cli("wallpaper", "list")
        self.assertEqual(r.returncode, 0)
        self.assertIn("aura-midnight-peaks", r.stdout)
        r = self.cli("wallpaper", "set", "aura-aurora-ridge")
        self.assertEqual(r.returncode, 0)
        r = self.cli("wallpaper", "set", "no-such-wallpaper")
        self.assertEqual(r.returncode, 1)

    def test_dock_validation(self):
        self.assertEqual(self.cli("dock", "size", "72").returncode, 0)
        cfg = json.load(open(os.path.join(
            self.tmp, "config", "aura", "config.json"), encoding="utf-8"))
        self.assertEqual(cfg["dock"]["size"], 72)
        self.assertEqual(self.cli("dock", "size", "banana").returncode, 2)
        self.assertEqual(self.cli("dock", "position", "diagonal").returncode, 2)

    def test_install_dry_run(self):
        r = self.cli("install", "--dry-run", "-y", "htop")
        self.assertEqual(r.returncode, 0)
        self.assertIn("apt-get install -y htop", r.stdout)

    def test_clean_preview_changes_nothing(self):
        r = self.cli("clean")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Nothing has been deleted", r.stdout)

    def test_completions(self):
        self.assertIn("aura", self.cli("completion", "zsh").stdout)
        self.assertIn("complete -F", self.cli("completion", "bash").stdout)

    def test_bad_accent_rejected(self):
        self.assertEqual(self.cli("theme", "accent", "chartreuse").returncode, 1)
        r = self.cli("theme", "accent", "#12ab34")
        self.assertEqual(r.returncode, 0)

    def test_liquid_glass_presets_and_opacity(self):
        self.assertEqual(self.cli("glass", "frosted").returncode, 0)
        cfg = json.load(open(os.path.join(
            self.tmp, "config", "aura", "config.json"), encoding="utf-8"))
        self.assertEqual(cfg["glass_preset"], "frosted")
        glass_css = os.path.join(self.tmp, ".themes", "AuraCustom",
                                 "gtk-3.0", "glass.css")
        self.assertTrue(os.path.isfile(glass_css))
        self.assertEqual(self.cli("glass", "opacity", "0.74").returncode, 0)
        self.assertIn("0.74", open(glass_css, encoding="utf-8").read())
        self.assertEqual(self.cli("glass", "performance").returncode, 0)
        cfg = json.load(open(os.path.join(
            self.tmp, "config", "aura", "config.json"), encoding="utf-8"))
        self.assertTrue(cfg["performance_mode"])

    def test_lock_screen_pam_and_cli(self):
        lock_bin = os.path.join(REPO, "rootfs", "usr", "bin", "aura-lock")
        self.assertTrue(os.path.isfile(lock_bin))
        r = subprocess.run([sys.executable, lock_bin, "--status"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(r.returncode, 0)
        self.assertIn("PAM", r.stdout)
        # Empty password must always be rejected
        r_empty = subprocess.run([sys.executable, lock_bin, "--check-auth", "user", ""],
                                 capture_output=True, text=True, timeout=15)
        self.assertNotEqual(r_empty.returncode, 0)
        # Wrong password must always be rejected by PAM
        r_bad = subprocess.run([sys.executable, lock_bin, "--check-auth", "root", "wrong-pass-xyz"],
                               capture_output=True, text=True, timeout=15)
        self.assertNotEqual(r_bad.returncode, 0)

    def test_font_presets_and_css(self):
        r_list = self.cli("font", "list")
        self.assertEqual(r_list.returncode, 0)
        self.assertIn("orbitron", r_list.stdout)
        self.assertIn("rajdhani", r_list.stdout)
        r_set = self.cli("font", "orbitron")
        self.assertEqual(r_set.returncode, 0)
        font_css = os.path.join(self.tmp, ".themes", "AuraCustom",
                                "gtk-3.0", "font.css")
        self.assertTrue(os.path.isfile(font_css))
        self.assertIn("Orbitron", open(font_css, encoding="utf-8").read())

    def test_kali_security_center_and_cli(self):
        r = self.cli("kali", "status")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Information Gathering", r.stdout)
        self.assertIn("Web Application Security", r.stdout)
        self.assertIn("Wireless Security", r.stdout)
        self.assertIn("nmap", r.stdout)
        self.assertIn("wireshark", r.stdout)
        self.assertIn("metasploit", r.stdout)
        r_hw = self.cli("kali", "wireless")
        self.assertEqual(r_hw.returncode, 0)
        hw_data = json.loads(r_hw.stdout)
        self.assertIn("has_wireless", hw_data)
        self.assertIn("summary", hw_data)

    def test_launcher_and_appbar_cli(self):
        r_ln = self.cli("launcher", "list")
        self.assertEqual(r_ln.returncode, 0)
        self.assertIn("AURA Security Center", r_ln.stdout)
        self.assertIn("Total discovered applications:", r_ln.stdout)
        r_bar = self.cli("appbar", "status")
        self.assertEqual(r_bar.returncode, 0)
        self.assertIn("AURA Cool App Bar", r_bar.stdout)

    def test_quicksettings_and_monitor_status(self):
        qs_bin = os.path.join(REPO, "rootfs", "usr", "bin", "aura-quicksettings")
        r_qs = subprocess.run([sys.executable, qs_bin, "--status"],
                              capture_output=True, text=True, timeout=15)
        self.assertEqual(r_qs.returncode, 0)
        self.assertIn("Network:", r_qs.stdout)
        self.assertIn("Firewall:", r_qs.stdout)
        mon_bin = os.path.join(REPO, "rootfs", "usr", "bin", "aura-monitor")
        r_mon = subprocess.run([sys.executable, mon_bin, "--status"],
                               capture_output=True, text=True, timeout=15)
        self.assertEqual(r_mon.returncode, 0)
        self.assertIn("Guest RAM:", r_mon.stdout)
        self.assertIn("Temperatures:", r_mon.stdout)


class Assets(unittest.TestCase):
    def test_all_generators_idempotent(self):
        """Re-running the asset generators must succeed and not change APIs."""
        for tool in ("generate_icons.py", "generate_cursors.py",
                     "generate_themes.py", "generate_xfwm4.py",
                     "generate_sounds.py", "generate_desktop_files.py",
                     "render_debos_recipe.py"):
            r = subprocess.run([sys.executable,
                                os.path.join(REPO, "tools", tool)],
                               capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, f"{tool}: {r.stderr}")

    def test_key_files_exist(self):
        must = [
            "rootfs/usr/bin/aura", "rootfs/usr/bin/celestia-tutorial",
            "rootfs/usr/bin/aura-settings", "rootfs/usr/bin/aura-appcenter",
            "rootfs/usr/bin/aura-welcome", "rootfs/etc/os-release",
            "rootfs/usr/share/themes/AuraDark/gtk-3.0/gtk.css",
            "rootfs/usr/share/themes/AuraLight/gtk-3.0/gtk.css",
            "rootfs/usr/share/icons/AuraIcons/index.theme",
            "rootfs/usr/share/backgrounds/aura/aura-midnight-peaks.jpg",
            "rootfs/etc/skel/.zshrc", "build/debos/aura.yaml",
            "build/packages/core.txt", "installer/install-aura.sh",
            "rootfs/usr/share/aura/finalize.sh", "build/build-iso.sh",
            "build/build-image.sh", "rootfs/usr/share/aura/catalog.json",
        ]
        for rel in must:
            self.assertTrue(os.path.isfile(os.path.join(REPO, rel)), rel)

    def test_svgs_and_xml_parse(self):
        import glob
        import xml.dom.minidom
        svgs = glob.glob(os.path.join(REPO, "rootfs", "**", "*.svg"),
                         recursive=True) + \
               glob.glob(os.path.join(REPO, "assets", "**", "*.svg"),
                         recursive=True)
        self.assertGreater(len(svgs), 30)
        for f in svgs:
            xml.dom.minidom.parse(f)
        xmls = glob.glob(os.path.join(
            REPO, "rootfs/etc/skel/.config/xfce4/xfconf/**/*.xml"),
            recursive=True)
        self.assertGreaterEqual(len(xmls), 6)
        for f in xmls:
            xml.dom.minidom.parse(f)

    def test_catalog_shape(self):
        data = json.load(open(os.path.join(
            REPO, "rootfs/usr/share/aura/catalog.json"), encoding="utf-8"))
        count = 0
        for cat in data["categories"]:
            self.assertIn("name", cat)
            for app in cat["apps"]:
                count += 1
                self.assertIn("name", app)
                self.assertIn("desc", app)
                self.assertTrue(app.get("apt") or app.get("flatpak")
                                or app.get("note"),
                                f"{app['id']} has no install path")
        self.assertGreaterEqual(count, 40)

    def test_every_aura_app_has_icon(self):
        import configparser
        icons_root = os.path.join(REPO, "rootfs/usr/share/icons/AuraIcons/"
                                       "scalable/apps")
        available = {os.path.splitext(f)[0] for f in os.listdir(icons_root)}
        apps_dir = os.path.join(REPO, "rootfs/usr/share/applications")
        for fn in os.listdir(apps_dir):
            if not fn.endswith(".desktop"):
                continue
            cp = configparser.ConfigParser(interpolation=None)
            cp.read(os.path.join(apps_dir, fn), encoding="utf-8")
            icon = cp["Desktop Entry"].get("Icon", "")
            self.assertIn(icon, available, f"{fn} → missing icon {icon}")

    def test_liquid_glass_wallpapers_and_icons_inventory(self):
        wp_dir = os.path.join(REPO, "rootfs/usr/share/backgrounds/aura")
        for wp in (
            "aura-dark-peaks.jpg", "aura-midnight-peaks.jpg",
            "aura-glacier-dawn.jpg", "aura-aurora-ridge.jpg",
            "aura-crystal-valley.jpg", "aura-liquid-waves.jpg",
            "aura-cyan-horizon.jpg", "aura-minimal-gradient.jpg",
            "aura-lock-peaks.jpg",
        ):
            self.assertTrue(os.path.isfile(os.path.join(wp_dir, wp)), wp)
        icons_dir = os.path.join(REPO, "rootfs/usr/share/icons/AuraIcons/scalable/apps")
        for req in (
            "aura-logo", "aura-finder", "celestia-shell", "aura-browser",
            "aura-appcenter", "aura-settings", "aura-text", "aura-studio",
            "aura-notes", "aura-calendar", "aura-calculator", "aura-monitor",
            "aura-photos", "aura-media", "aura-transfer", "aura-archive",
            "aura-screenshot", "aura-pdf", "aura-backup", "aura-taskmanager",
            "aura-help", "aura-firewall", "aura-lock", "aura-quicksettings",
            "aura-launcher", "aura-appbar", "aura-security", "aura-nmap",
            "aura-wireshark", "aura-metasploit", "aura-burpsuite",
            "aura-aircrack", "aura-john", "aura-hydra", "aura-sqlmap",
            "aura-hashcat", "aura-zaproxy", "aura-gobuster", "aura-nikto",
            "user-trash",
        ):
            p = os.path.join(icons_dir, req + ".svg")
            self.assertTrue(os.path.isfile(p), f"Missing icon: {req}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
