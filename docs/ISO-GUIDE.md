# Build the AURA OS ISO and run it in UTM — every command, step by step

The ISO must be built on **ARM64 Linux** — `apt`/`live-build` don't exist
on macOS, so don't paste the Linux commands into Mac Terminal. Two ways:

* **Easiest (all from Mac Terminal):** one command — `./build/build-on-mac.sh`
  creates an ARM64 Debian VM with Lima, builds inside it, and puts the ISO
  in `~/Downloads`. Skip to **Phase 4** when it's done. (First run installs
  Homebrew's `lima` package if needed; if you have no Homebrew, the script
  prints the one-line installer.)
* **Manual builder VM in UTM:** Phases 0–3 below.

Total time: ~1–2 hours (mostly downloads). A no-build alternative using
GitHub Actions is at the end.

---

## Phase 0 — On your Mac (2 minutes)

1. Install **UTM**: https://mac.getutm.app/ (or `brew install --cask utm`).
2. Download the **Debian 12 ARM64 netinst ISO** (for the builder VM):
   https://cdimage.debian.org/debian-cd/current/arm64/iso-cd/
   → pick the file like `debian-12.x.x-arm64-netinst.iso` (~660 MB).
3. Make a shared folder for later (optional): `~/AURA-Shared`.

## Phase 1 — Create the builder VM (UTM clicks)

1. UTM → **＋ Create a New Virtual Machine** → **Virtualize** → **Linux**.
2. **Uncheck** “Use Apple Virtualization” (QEMU backend = SPICE clipboard,
   resize and sharing work in AURA).
3. **Boot ISO Image** → Browse → the Debian netinst ISO → Continue.
4. Hardware: **Memory 6144 MB**, **CPU Cores 4** → Continue.
5. Storage: **49152 MB** (48 GB — the build needs room) → Continue.
6. Shared Directory: choose `~/AURA-Shared` (optional) → Continue.
7. Name it `AURA Builder` → Save → press **▶**.

Debian installer: **Graphical install** → language/country/keyboard →
hostname `aura-builder` → create your user + password → Partitioning:
**Guided – use entire disk** → *All files in one partition* → Finish →
**Yes** → Software selection: **uncheck** “Debian desktop environment” and
GNOME, **check** “SSH server” and “standard system utilities” → Install
GRUB: **Yes**, device: the offered disk → Finish → the VM reboots.
(If the installer loops, stop the VM → Edit → Drives → CD/DVD → Clear.)

## Phase 2 — Build the ISO (commands, in the builder VM)

Log into Debian, open a terminal (or SSH in), then exactly:

```bash
sudo apt update
sudo apt install -y git live-build rsync debootstrap squashfs-tools \
    xorriso grub-efi-arm64-bin mtools dosfstools

git clone -b arena/3424d119-ai-os https://github.com/FellowPythonCoder/AI-Os.git
cd AI-Os

sudo ./build/build-iso.sh
```

Wait **30–90 minutes** (downloads ~130 Debian packages + builds the live
system). If anything fails (network hiccup etc.), just run
`sudo ./build/build-iso.sh` again — downloaded packages are cached, so the
retry is much faster. Details are logged to `build/out/build-iso.log`.

When it finishes, verify:

```bash
ls -lh build/out/
cd build/out && sha256sum -c AURA-OS-1.0-arm64.iso.sha256   # expect: OK
```

## Phase 3 — Copy the ISO to your Mac

**Option A — web download (simplest).** In the builder VM:

```bash
cd ~/AI-Os/build/out
hostname -I                 # note the IP, e.g. 192.168.64.5
python3 -m http.server 8000
```

On the Mac, open `http://192.168.64.5:8000/` (use *your* VM's IP) and click
`AURA-OS-1.0-arm64.iso`. Press Ctrl+C in the VM when done.

**Option B — scp from Mac Terminal** (works because you installed SSH server):

```bash
scp YOURUSER@192.168.64.5:~/AI-Os/build/out/AURA-OS-1.0-arm64.iso ~/Downloads/
```

Then shut the builder down: `sudo poweroff` (keep the VM — future rebuilds
start from Phase 2 with a `git pull`).

## Phase 4 — Create the AURA VM (UTM clicks)

1. **＋** → **Virtualize** → **Linux** → uncheck “Use Apple Virtualization”.
2. **Boot ISO Image** → Browse → `AURA-OS-1.0-arm64.iso` → Continue.
3. **Memory 4096–6144 MB**, **CPU 4** → Continue.
4. Storage **32768 MB or more** → Continue.
5. Shared Directory: pick a Mac folder you want visible in AURA.
6. Name: `AURA OS` → Save.
7. (Optional) select the VM → Edit → Display → enable Retina/HiDPI if shown;
   Sharing → **Enable Clipboard Sharing**.
8. Press **▶**.

## Phase 5 — Install AURA (in the live desktop)

AURA boots **live** first — look around freely. Then double-click
**Install AURA OS** on the desktop and walk the Calamares wizard:

1. **Welcome** – language → Next
2. **Location** – your timezone → Next
3. **Keyboard** – your layout → Next
4. **Partitions** – **Erase disk** (this erases only the *virtual* disk)
5. **Users** – your name, username, password; computer name `aura-os`
6. **Summary** → **Install** (~10–20 min) → **Restart Now** → Done

If it boots back into the live desktop, the ISO is still attached:
power off → Edit (sliders icon) → Drives → the CD/DVD drive → **Clear** →
Save → ▶.

## Phase 6 — First boot & health check

GRUB (AURA theme) → blue-mountain boot splash → **log in** → the Welcome
wizard (mode, accent color, wallpaper, display, Celestia intro) →
**Start using AURA** 🏔️

Open **Celestia Shell** (dock icon or `Ctrl+Alt+T`) and run:

```bash
aura fetch        # logo + system summary
aura doctor       # must be all ✓ (network, UTM tools, disk…)
aura update       # refresh + list updates
aura upgrade      # install them (asks your password)
aura tutorial     # 5-minute interactive tour
```

Finally, in UTM take a **snapshot** of the golden state.

---

## Alternative: build with GitHub Actions (no builder VM)

The repo ships `.github/workflows/build-iso.yml` (native ARM64 runners):

1. Merge branch `arena/3424d119-ai-os` into `main` (GitHub only shows
   *Run workflow* for workflows present on the default branch).
2. Repo → **Actions** → **Build AURA OS ISO (live-build, ARM64)** →
   **Run workflow** → branch `main` → Run. (~1–3 h)
3. Open the finished run → **Artifacts** → download
   `AURA-OS-1.0-arm64-iso` (a zip with the ISO + sha256), unzip, then
   continue at **Phase 4** above.

## Troubleshooting the classics

| Symptom | Fix |
|---|---|
| ISO boots to black screen | VM is x86/Emulate or Apple-virt without display — recreate as **ARM64 Virtualize**, QEMU backend, ≥4 GB |
| UEFI shell / no boot device | ISO not attached, or wrong boot order; UEFI menu → Boot From File → CD → `EFI/BOOT/BOOTAA64.EFI` |
| `build-iso.sh` says “must run on an ARM64 host” | You're not in the ARM64 builder VM (e.g. ran it on the Mac) |
| Build fails mid-download | Just re-run `sudo ./build/build-iso.sh` — cache makes it resume fast |
| Calamares “no EFI partition” type warnings | Pick **Erase disk** and let it partition automatically |
| Boots to live desktop after install | ISO still attached — Edit → Drives → CD/DVD → Clear |
| `aura doctor` flags spice-vdagent | `aura install spice-vdagent qemu-guest-agent`, then log out/in |
