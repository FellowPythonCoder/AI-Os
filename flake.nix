{
  description = "auraOS aarch64 NixOS live images";
  inputs = {
    # Matches the nixpkgs revision locked by the selected Caelestia shell.
    nixpkgs.url = "github:NixOS/nixpkgs/1c89083e451e891152365b799595cf7790a43325";
    caelestia-shell = {
      url = "github:caelestia-dots/shell/bcbb5d5139d5159839c7362d8f4954ccc7dbd67d";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    caelestia-dots = {
      url = "github:caelestia-dots/caelestia/01d2df329240be60148d25804690779a078c6378";
      flake = false;
    };
  };

  outputs = inputs@{ nixpkgs, ... }: {
    nixosConfigurations.auraos-iso = nixpkgs.lib.nixosSystem {
      system = "aarch64-linux";
      specialArgs = { inherit inputs; };
      modules = [
        "${nixpkgs}/nixos/modules/installer/cd-dvd/installation-cd-minimal.nix"
        ./nixos/iso.nix
        ./nixos/desktop.nix
      ];
    };
  };
}
