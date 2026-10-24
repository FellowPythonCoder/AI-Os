# UTM Tips (running AURA on your Mac)

AURA OS runs *inside* UTM. A few things live on the UTM side:

## Memory (RAM) and CPUs

The RAM and CPU cores AURA reports are the ones **allocated in UTM** —
not your Mac's total. To change them: shut AURA down, right-click the
VM in UTM → Edit → System. For a 16 GB Mac we recommend **4–6 GB RAM**
and **4 CPU cores**, leaving plenty for macOS.

## Clipboard, display and shared folders

These need UTM's SPICE tools, which AURA pre-installs
(`spice-vdagent`, `qemu-guest-agent`):

- **Clipboard** between Mac and AURA: enable in UTM → Edit → Sharing.
- **Shared folder**: UTM → Edit → Sharing → Directory Share. In AURA it
  is mounted automatically (virtio-9p/WebDAV depending on UTM version);
  look in AURA Finder or run `aura doctor`.
- **Display resize**: resizing the UTM window resizes AURA's display.
  For the sharpest text enable Retina mode in UTM's display settings.

## Snapshots

Before big experiments, use UTM's snapshot feature (or AURA Backup /
Timeshift inside the guest). You can always roll back.

## Performance notes

- AURA's effects are GPU-friendly but modest; if animation feels heavy,
  turn off transparency in Settings → Effects.
- Give the VM at least 32 GB of disk for comfort.
- UTM's "Virtualize" (Apple hypervisor) mode is fastest for ARM64.
