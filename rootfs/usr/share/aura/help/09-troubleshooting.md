# Troubleshooting

## Start here

Run `aura doctor` in Celestia Shell — it checks disk, memory, network
and UTM guest tools, and prints the exact fix for anything it finds.

## No internet

- In UTM, set the VM's network to **Shared (NAT)**.
- Inside AURA: `aura doctor`, then check the network icon in the menu bar.
- Restart networking: `sudo systemctl restart NetworkManager`

## Clipboard / shared folder not working

- Confirm both are enabled in UTM → Edit → Sharing.
- Ensure tools are installed: `aura install spice-vdagent qemu-guest-agent`
- Log out and back in after installing.

## Display doesn't resize with the window

- Install/restart `spice-vdagent` (above), or set the resolution manually
  in Settings → Display.

## AURA feels slow

- Allocate more RAM/CPUs in UTM (VM powered off).
- Settings → Effects: turn off transparency and window shadows.
- `aura clean` to free space; `aura monitor`-style check via AURA Monitor.
  (Command-line equivalent: `aura system`.)

## Forgot your password

Boot the VM holding **Esc** to reach the GRUB menu → Advanced options →
recovery mode → root shell → `passwd your-username` → `reboot`.

## Restore everything visual

`aura theme reset` restores AURA's default appearance instantly.
For deeper recovery, roll back a UTM snapshot or a Timeshift snapshot
in **AURA Backup**.
