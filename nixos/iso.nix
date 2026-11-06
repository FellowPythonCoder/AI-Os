{ lib, ... }:
{
  # Keep the upstream installer kernel and hardware detection for this first
  # boot milestone. In particular, don't strip virtio or EFI drivers yet.
  networking.hostName = "auraos-live";
  image.baseName = lib.mkForce "auraOS-1.0-aarch64";
  isoImage.volumeID = "AURAOS_1_0_AARCH64";
  isoImage.makeEfiBootable = true;
  isoImage.makeUsbBootable = true;
  system.stateVersion = "25.11";
}
