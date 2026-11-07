# Experimental live desktop. See DESKTOP-STATUS.md before building.
{ inputs, lib, pkgs, ... }:
let
  # Caelestia's dotfiles expect a writable ~/.config/hypr (they generate
  # scheme/current.lua). Populate it once per live session, not a store symlink.
  startAura = pkgs.writeShellScript "start-aura" ''
    set -eu
    mkdir -p "$HOME/.config/hypr" "$HOME/.config/caelestia" "$HOME/Pictures/Wallpapers"
    cp -rn --no-preserve=mode,ownership ${inputs.caelestia-dots}/hypr/. "$HOME/.config/hypr/"
    chmod -R u+w "$HOME/.config/hypr"
    exec ${pkgs.dbus}/bin/dbus-run-session ${pkgs.hyprland}/bin/Hyprland
  '';
in {
  programs.hyprland.enable = true;
  services.greetd = {
    enable = true;
    useTextGreeter = true;
    settings = {
      initial_session = { command = "${startAura}"; user = "nixos"; };
      default_session = {
        command = "${pkgs.tuigreet}/bin/tuigreet --time --cmd ${startAura}";
        user = "greeter";
      };
    };
  };
  # greetd owns tty1, rather than the installer profile's autologin getty.
  services.getty.autologinUser = lib.mkForce null;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    pulse.enable = true;
  };
  security.rtkit.enable = true;
  hardware.graphics.enable = true;
  services.spice-vdagentd.enable = true;
  services.power-profiles-daemon.enable = true;
  programs.dconf.enable = true;
  environment.systemPackages = with pkgs; [
    inputs.caelestia-shell.packages.${pkgs.stdenv.hostPlatform.system}.with-cli
    foot xfce.thunar firefox mousepad imv mpv btop
    brightnessctl ddcutil lm_sensors swappy fish
    wl-clipboard cliphist grim slurp
    material-symbols rubik nerd-fonts.caskaydia-cove
    adw-gtk3 papirus-icon-theme
  ];
  environment.sessionVariables = {
    NIXOS_OZONE_WL = "1";
    WLR_NO_HARDWARE_CURSORS = "1";
  };
  # A dark preference for GTK applications; shell-specific theming remains
  # an explicit outstanding integration task.
  environment.etc."xdg/gtk-3.0/settings.ini".text = ''
    [Settings]
    gtk-application-prefer-dark-theme=1
    gtk-theme-name=adw-gtk3-dark
    gtk-icon-theme-name=Papirus-Dark
  '';
}
