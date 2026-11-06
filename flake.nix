{
  description = "auraOS milestone 1: aarch64 UEFI NixOS live image";

  # A revision, not a moving branch. Later desktop inputs will be pinned too.
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/b6018f87da91d19d0ab4cf979885689b469cdd41";

  outputs = { nixpkgs, ... }: {
    nixosConfigurations.auraos-iso = nixpkgs.lib.nixosSystem {
      system = "aarch64-linux";
      modules = [
        "${nixpkgs}/nixos/modules/installer/cd-dvd/installation-cd-minimal.nix"
        ./nixos/iso.nix
      ];
    };
  };
}
