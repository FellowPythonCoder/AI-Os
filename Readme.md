# 🏔️ AURA OS

### A new desktop experience. Inspired by the beauty of blue mountains.

AURA OS is an experimental, blue-themed operating system project designed to bring a modern, macOS-inspired desktop experience to Apple Silicon Macs through UTM virtualization.

Featuring a custom blue mountain identity, a graphical desktop, extensive customization, a built-in terminal called **Celestia Shell**, and a vision for a growing ecosystem of applications, AURA aims to make Linux feel beautiful, approachable, and powerful.

> **Project status:** Experimental — features, compatibility, and stability are still being developed and tested.

---

## ✨ Features

- 🔵 **Beautiful blue design** — A consistent visual identity inspired by blue mountain landscapes.
- 🖥️ **Modern graphical desktop** — A clean, macOS-inspired interface with a menu bar, dock, windows, and desktop customization.
- ⌨️ **Celestia Shell** — A built-in terminal experience designed for commands, scripts, development, and system management.
- 📦 **Software installation** — Access compatible Linux applications and development tools through supported package managers.
- 🎨 **Deep customization** — Personalize wallpapers, themes, colors, icons, fonts, panels, and other desktop settings.
- 🗂️ **Desktop applications** — A growing collection of utilities, productivity tools, and developer applications.
- 🛠️ **Developer-friendly** — Designed to support tools such as Git, Python, Node.js, compilers, and other compatible packages.
- 🍎 **Apple Silicon virtualization** — Intended to run as an ARM64 virtual machine using UTM on compatible Macs.

*Note: Features listed here describe the project's goals. Refer to the current source code and testing results to determine what is actually implemented.*

## 🏔️ Design Philosophy

AURA OS is built around three ideas:

1. **Simplicity:** Make the desktop intuitive and easy to use.
2. **Customization:** Let users shape their environment to match their preferences.
3. **Capability:** Provide access to a real operating system, useful applications, and a powerful command line.

AURA takes inspiration from the visual polish and usability of macOS while aiming to establish its own branding and desktop experience. It is an independent project and is not affiliated with Apple.

## 💻 Target Platform

The initial target is:

| Component | Target |
|---|---|
| Host computer | Apple Silicon Mac |
| Development target | Mac M4 with 16 GB RAM |
| Virtualization | UTM |
| Guest architecture | ARM64 / AArch64 |
| OS foundation | Linux-based |
| Desktop | Customizable graphical environment |
| Terminal | Celestia Shell |
| Project stage | Experimental |

Actual hardware requirements depend on the guest OS, enabled features, and applications being used.

## 🚀 Getting Started

### Requirements

- An Apple Silicon Mac or another supported ARM64 system.
- [UTM](https://mac.getutm.app/) for virtualization.
- The AURA OS installation image, once a bootable release is available.
- Sufficient free disk space and memory for the virtual machine.

### Installation

1. Download a published AURA OS image from the repository's **Releases** page, if available.
2. Open UTM and create a new virtual machine.
3. Select the appropriate Linux or ARM64 virtualization option for the supplied image.
4. Allocate suitable memory, CPU cores, and storage.
5. Attach the image and start the virtual machine.
6. Follow the installer or first-boot instructions provided with that release.

**Important:** Do not assume a bootable image is available just because the source repository exists. If no release image has been published, follow the project's build instructions instead.

## ⌨️ Celestia Shell

Celestia Shell is the planned command-line environment for AURA OS.

The goal is to provide a useful terminal with command history, autocomplete, tabs, shell compatibility, developer tools, and AURA-specific system commands.

Example commands planned for AURA include:

```bash
aura help
aura apps
aura settings
aura theme blue
aura system
aura update
aura search firefox
```

These commands are examples of the intended interface. They should be treated as available only when implemented in the installed version.

AURA is intended to support standard Linux commands and package-management tools so users can install compatible software, download files, work with Git repositories, and develop applications.

## 🧪 Testing

AURA OS is an experimental project. Testing is an important part of development, and features should be marked as verified only after they have been tested on the relevant configuration.

### Testing checklist

- [ ] OS image boots successfully in UTM.
- [ ] ARM64 architecture is correctly configured.
- [ ] Graphical desktop loads without critical errors.
- [ ] Login and user accounts work.
- [ ] Menu bar, dock, and window management function correctly.
- [ ] Celestia Shell launches and accepts commands.
- [ ] Standard Linux commands work.
- [ ] Package manager can install a compatible application.
- [ ] Networking and DNS work inside the VM.
- [ ] Files can be created, opened, moved, and deleted.
- [ ] Themes and wallpapers persist after reboot.
- [ ] Guest memory usage is reported accurately.
- [ ] System updates complete successfully.
- [ ] Restart and shutdown work correctly.

### Reporting a test result

When reporting a successful test, include the host device, macOS version, UTM version, guest architecture, memory allocation, and the exact steps performed.

Known issues and untested features should be documented openly. A successful build does not automatically mean every application or feature works correctly.

## 🤖 AI-Assisted Development

**AURA OS is developed with assistance from artificial intelligence.**

AI tools have been used to help with project planning, generating and refining code, designing the user experience, writing documentation, troubleshooting, and exploring implementation approaches.

The project is also subject to human review, testing, debugging, and ongoing development. AI-generated code can contain mistakes, security issues, incomplete implementations, or incorrect assumptions, so contributions must be reviewed and tested.

AI assistance is disclosed here for transparency. It does not mean every part of the project was generated by AI, nor does it guarantee that the software works as intended.

## 🔐 Security and Reliability

Because AURA is experimental:

- Back up important files before testing.
- Test unfamiliar builds in a virtual machine rather than on a primary operating system.
- Review installation scripts before running them.
- Avoid running untrusted scripts with administrator privileges.
- Do not store sensitive information in an untrusted development build.
- Report security vulnerabilities responsibly.

## 🗺️ Roadmap

- [ ] Establish a reliable ARM64 Linux base.
- [ ] Create the AURA mountain logo and visual identity.
- [ ] Build the customized graphical desktop.
- [ ] Implement Celestia Shell.
- [ ] Add comprehensive theme and appearance settings.
- [ ] Integrate an application center.
- [ ] Add file management and system monitoring tools.
- [ ] Improve UTM integration and first-run setup.
- [ ] Test installation, updates, and recovery.
- [ ] Publish reproducible build instructions and stable releases.

Roadmap items may change as development progresses.

## 🤝 Contributing

Contributions, bug reports, feature suggestions, documentation improvements, and testing feedback are welcome.

When opening an issue, please include:

- A clear description of the problem.
- Steps to reproduce it.
- Expected and actual behavior.
- Relevant error messages or logs.
- Your host system and UTM configuration.
- Whether the issue is reproducible.

Please distinguish confirmed bugs from feature requests and unverified observations.

## 📜 License

AURA OS's license should be specified in the repository's `LICENSE` file. Until a license is selected and published, do not assume the project is open for unrestricted reuse or redistribution.

Third-party components remain subject to their respective licenses.

## 💙 A Final Note

AURA OS is an ongoing experiment in creating a beautiful, customizable, and capable desktop operating system.

Built with curiosity, AI-assisted development, and a focus on the user experience, AURA aims to combine a distinctive blue aesthetic with the flexibility of Linux.

**Welcome to AURA OS. Explore beyond the ordinary.** 🏔️
