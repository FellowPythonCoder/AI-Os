# Installing AURA OS in UTM (Apple Silicon)

Three routes, easiest first. All need: **UTM** ([mac.getutm.app](https://mac.getutm.app/)),
an **Apple Silicon Mac**, and ~20 GB free space.

### Recommended VM settings (16 GB Mac)

| Setting | Value |
|---|---|
| Type | **Virtualize** → Linux (ARM64, Apple hypervisor) |
| Memory | **4096–6144 MB** (don't starve macOS) |
| CPU cores | **4** (Default also works) |
| Disk | **32 GB** (expanding) |
| Display | Retina mode **on** for sharpest text; resize with the window |
| Network | **Shared Network** (NAT) |
| Sharing | Clipboard **on**; pick a shared folder (e.g. `~/AURA-Shared`) |
| Sound | On |

> The RAM AURA reports is the memory *you allocate here* — `aura system`
> always labels it "guest memory" so there's no confusion with your Mac's 16 GB.

---

## Route A — Preinstalled image (fastest)

1. Download `AURA-OS-1.0-arm64.qcow2` from the project's
   [Releases](https://github.com/FellowPythonCoder/AI-Os/releases), or build
   it yourself (see BUILDING.md).
2. UTM → **＋** → *Start from Scratch*… actually easier: *Create a New VM* →
   **Virtualize** → **Linux** → *Boot from kernel image* **off** → set the
   settings above → when asked for a boot ISO choose **None**.
3. Finish the wizard, then select the VM → **Edit** (slider icon) → **Drives**:
   delete the empty default drive, **Import…** the downloaded `.qcow2`.
   Ensure the drive interface is **NVMe** or **VirtIO** and it's the first drive.
4. Start the VM. Log in: user **`aura`**, password **`aura`** — you'll be
   required to choose a new password immediately. The Welcome wizard opens
   on first login.

## Route B — Installer ISO

1. Get `AURA-OS-1.0-arm64.iso` (Releases or BUILDING.md).
2. UTM → **＋** → **Virtualize** → **Linux** → browse to the ISO → settings
   from the table → Save → ▶.
3. AURA boots **live** (try it freely — nothing is written yet).
4. Click **Install AURA OS** on the desktop. The Calamares wizard asks:
   language → keyboard → disk (choose *Erase disk* — it only erases the
   *virtual* disk) → your name/username/password → Install.
5. When it finishes, shut down, detach the ISO (Edit → Drives → CD/DVD →
   Clear), and boot your installed AURA.

## Route C — Transform a Debian install (most flexible)

1. Install stock **Debian 12 ARM64** (official netinst ISO) in UTM with the
   settings above. During Debian's installer you can pick *any* or *no*
   desktop — AURA will add its own. Create your normal user.
2. Inside Debian:
   ```bash
   sudo apt update && sudo apt install -y git
   git clone https://github.com/FellowPythonCoder/AI-Os
   cd AI-Os
   sudo ./installer/install-aura.sh --dry-run --user "$USER"   # preview
   sudo ./installer/install-aura.sh --user "$USER"             # for real
   sudo reboot
   ```
3. Log in → Welcome wizard. To preview exactly what changes, the
   `--dry-run` output lists every package and file; replaced system files
   are backed up under `/var/backups/aura-<date>/`.

## After install — 2-minute checklist

- [ ] `aura doctor` in Celestia Shell reports all green (network, UTM tools).
- [ ] Clipboard: copy text in macOS → paste in AURA (needs UTM Sharing on).
- [ ] Shared folder visible in AURA Finder (UTM → Edit → Sharing).
- [ ] `aura update && aura upgrade` once, to catch the latest Debian fixes.
- [ ] Take a UTM snapshot: your "golden" rollback point.

## Troubleshooting quickies

| Symptom | Fix |
|---|---|
| Black screen at boot | VM must be **Virtualize/ARM64**, not Emulate/x86. Delete and recreate as ARM64. |
| "No bootable device" | ISO not attached, or qcow2 not the first drive. Check Edit → Drives order. |
| Tiny/blurry display | Enable Retina in UTM display prefs; in AURA: Settings → Display. |
| No clipboard/resize | UTM → Sharing on; in AURA `aura install spice-vdagent`, re-login. |
| No network | UTM network = Shared. In AURA: `sudo systemctl restart NetworkManager`. |
| Slow UI | Give the VM ≥4 GB / 4 cores; AURA Settings → Effects → disable transparency/shadows. |

Full guide: **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**.
