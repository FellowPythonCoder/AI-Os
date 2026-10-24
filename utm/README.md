# UTM reference configuration for AURA OS

Create the VM with UTM's wizard (**Virtualize → Linux**) using these values.
(We deliberately don't ship a `.utm` bundle: UTM generates per-machine UUIDs
for drives, and the wizard applies your Mac's correct defaults.)

| UTM field | AURA value |
|---|---|
| Architecture | ARM64 (aarch64) |
| System | QEMU ARM Virtual Machine (virt) — wizard default |
| Memory | 4096–6144 MB (16 GB Mac: 6144 max recommended) |
| CPU | 4 cores (or "Default") |
| Boot | UEFI (default) |
| Storage | 32768 MB+, NVMe or VirtIO interface |
| Display | virtio-gpu-pci / ramfb (wizard default), **Retina mode: on** |
| Network | Shared Network (NAT), virtio-net-pci |
| Sound | Intel HDA / virtio (wizard default) |
| Sharing | Clipboard **on**, Directory Share → pick a folder |
| Input | USB keyboard/mouse (defaults) |

Then follow ../docs/INSTALL-UTM.md (Routes A/B/C).
