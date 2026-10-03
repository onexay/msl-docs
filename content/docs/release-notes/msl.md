---
title: MSL release notes
linkTitle: MSL
weight: 1
description: What changed in each release of MSL, newest first.
---

What changed in each MSL release, newest first. Update to the latest release with `msl --update`. Changes that can break a script or a habit are marked **Breaking**. Each version links to its GitHub release, which has the downloads and checksums.

## 0.3.0

1 October 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.3.0) · kernel `kernel-6.18.15-msl-a1a22bd`

**Changed**

- **Breaking:** MSL, its service and the VS Code extension are updated together, and the extension from MSL 0.2.0 or earlier can't connect to MSL 0.3.0. After updating from 0.2.0, run `msl --manage-ide --install` once. From then on, `msl --update` also updates the extension in every IDE that has it. See [Upgrade MSL]({{< relref "/docs/install/upgrade" >}}).
- A command's input and output go straight between `msl` and the VM instead of through `msld` ([#57](https://github.com/onexay/msl/issues/57)). Output through a pipe is about twice as fast (4 GiB in 4.8 s, was 8.2 s), and a slow or stuck command no longer slows down the others. `msl --import`, `--export` and `--install` move their tar streams the same way.
- Each distribution's disk is attached to the VM when it starts and served by Virtualization.framework, so `fsync` inside a distribution reaches the SSD again: the durability caveat of 0.2.0 no longer applies. A disk that appears while the VM runs (an install, an import, a move to another volume, a resize) restarts the VM if no distribution is running, in about 1.5 s; otherwise it's served more slowly until the VM next restarts. Up to 19 disks are attached at start, and a disk is no longer limited to 4 TB. See [Manage disk space]({{< relref "/docs/how-to/disk-space" >}}).
- An idle MSL wakes the Mac far less: the idle VM uses about 0.5% CPU, down from 2.5–3.5%.
- Forwarded ports and `~/.msl/distros` are carried by two processes of their own, `msl-portd` and `msl-fileviewd`, like WSL's `wslrelay.exe`, so `msld` no longer copies their data.
- MSL bundles [VS Code extension 0.2.0]({{< relref "/docs/release-notes/vscode#020" >}}).

**Fixed**

- `msl --export <distro> -` into a reader that stops early (`| head`) no longer crashes `msl`.

**Removed**

- `MSL_DISK_SLOTS`, with the disk slots it sized.

## 0.2.0

29 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.2.0) · kernel `kernel-6.18.15-msl-a1a22bd`

**Added**

- MSL shuts down cleanly when you log out, restart or shut down the Mac ([#52](https://github.com/onexay/msl/issues/52)). Before, the VM died with `msld`: distributions got no warning, and writes not yet synced were lost. `msld` now stops the distributions, unmounts and flushes their disks, and powers the VM off. It runs as a LaunchAgent (`~/Library/LaunchAgents/dev.msl.msld.plist`) that launchd starts on demand and gives up to 30 seconds to do this. `msl --uninstall` removes it.
- Each new distribution gets its own disk, a sparse `ext4.img` in its install location, like WSL's `ext4.vhdx` ([#50](https://github.com/onexay/msl/issues/50)). It's 256 GB by default, or the size of the macOS disk if that's smaller; `msl --install --vhd-size` and `defaultVhdSize` choose another size. The VM attaches disks through 16 disk slots, so a stopped distribution you haven't used for a while can give its slot up. See [Manage disk space]({{< relref "/docs/how-to/disk-space" >}}).
- `msl --manage --move`, `msl --manage --resize` for one distribution, `msl --export --vhd`, `msl --import --vhd` and `msl --import-in-place` work as in WSL, with raw ext4 images instead of VHDX. `msl --unregister` deletes the distribution's `ext4.img`, including one imported in place.
- `nestedVirtualization` in `[msl2]`, as in `.wslconfig` (default `true`): `/dev/kvm` in the distributions on a Mac with an M3 chip or later; MSL's kernel (`6.18.15-msl-a1a22bd`) has KVM built in, and `uname -r` now shows that release. `msl --status` shows whether it's on.
- The VM keeps one machine identifier across boots, and its `/etc/machine-id` is that identifier's UUID. Distributions keep their own.

**Changed**

- **Breaking:** `msl --manage <distro> --resize` grows that distribution's disk (it must be stopped) rather than `data.img` for all of them. Distributions from earlier versions stay on `data.img`, and `--resize` still grows `data.img` for them, until you move them onto their own disk with `msl --manage <distro> --move <folder>`.
- **Breaking:** `fsync` inside a distribution on its own disk isn't a durability point. Virtualization.framework passes no flushes to these disks, so writes are flushed to the SSD when a disk is detached and at `msl --shutdown`. A crash of MSL or the VM keeps what was written; a macOS crash or power loss can lose recent writes. See [Durability]({{< relref "/docs/how-to/disk-space#durability" >}}).
- `msl --status` shows the distributions' disks (`Distribution disks`), and the shared disk only while a distribution is still on it.
- The kernel and the VS Code extension moved to their own repositories, [msl-kernel](https://github.com/onexay/msl-kernel) and [msl-vscode-extension](https://github.com/onexay/msl-vscode-extension). MSL still bundles both.

## 0.1.11

28 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.11) · kernel `kernel-6.18.15-msl-21f0ec7`

**Fixed**

- The VM no longer crashes when macOS runs short of memory ([#48](https://github.com/onexay/msl/issues/48)). With the 4 KiB-page kernel, every distribution could crash within seconds once macOS started compressing or swapping the VM's memory, and a crash in the middle of a write could damage the data disk. The cause is Virtualization.framework's handling of 4 KiB pages in the VM on the Mac's 16 KiB pages. MSL's kernel now uses 16 KiB pages, like the Mac (`getconf PAGESIZE` is 16384). Ubuntu 22.04 and 26.04, Debian 13, Fedora 44, AlmaLinux 9 and Kali were tested: every binary and library loads, and systemd and package managers work. Programs built to assume 4 KiB pages don't run; see [Troubleshooting]({{< relref "/docs/troubleshooting" >}}).
- `msl --install` no longer hangs at the first setup prompt when its input is `/dev/tty`, as when `install.sh` runs it. On macOS, `/dev/tty` means the calling process's controlling terminal, and `msld` has none. `msl` now passes `msld` the real terminal device.

## 0.1.10

26 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.10)

**Fixed**

- MSL starts on macOS 26 again. 0.1.9 was built with Xcode 27, whose Swift runtime links libraries macOS 26 doesn't have, so `msld` failed to start there. Releases are now built by CI with Xcode 26, the version that matches MSL's minimum macOS. If you installed 0.1.9 on macOS 26, reinstall with the one-line installer; your distributions are kept.

## 0.1.9

25 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.9)

**Fixed**

- Sessions get the distribution's locale (`LANG`, `LANGUAGE`, `LC_*` from `/etc/default/locale` or `/etc/locale.conf`), as in WSL and login shells. Without it, VS Code's terminal set `LANG` from VS Code's own display language, and bash printed `setlocale: cannot change locale (en_US.UTF-8)` on distributions without that locale, such as Ubuntu with only `C.UTF-8`.

## 0.1.8

25 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.8)

**Fixed**

- `msl` failed with "could not start <current directory>/msld" when `msld` wasn't already running, for example right after `msl --update`. It looked for `msld` next to `argv[0]`, which is just `msl` when it runs from `PATH`. The same lookup set the install prefix for `--update`, `--uninstall` and `--version --json`, and the path recorded for the VS Code extension. `msl` now uses its real executable path.

**Security**

- Other local user accounts can no longer read or change your distributions through `~/.msl/distros` ([#1](https://github.com/onexay/msl/issues/1)). The view is served through a Unix socket that only your user can open, instead of a `127.0.0.1` port, and `msld` checks every NFS call: only your user ID and the kernel's get through, and only `msld` can mount the view. `fileViewTransport = tcp` in `[msl2]` brings back the port, with the same checks but weaker protection. See [Security model]({{< relref "/docs/security" >}}).

## 0.1.7

25 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.7) · kernel `kernel-6.18.15-msl-76f230e`

**Added**

- `msl --manage <distro> --resize <size>` grows the disk all distributions share ([#3](https://github.com/onexay/msl/issues/3)). Stop every distribution first with `msl --shutdown`. MSL restarts the VM, which checks and grows the filesystem before mounting it, in about 3 seconds for 256 GB. The disk can't shrink, and can't be larger than the macOS disk.
- `defaultVhdSize` in `[msl2]`, as in `.wslconfig`, sets the disk's size when it's created. Without it, a new disk is 256 GB, but never more than the macOS disk.
- `msl --status` shows the disk: its maximum size, what it uses on macOS, and what's free in the distributions and on macOS. It warns when macOS is nearly out of disk space, which the distributions can't see.

**Changed**

- **Breaking:** macOS files are mounted at `/mnt/macos` in every distribution, not `/mnt/mac` (`/macos` with a custom `[automount] root`). The environment variables `MSL_MAC_USER`, `MSL_MAC_HOME` and `MSL_MAC_VIEW` are now `MSL_MACOS_USER`, `MSL_MACOS_HOME` and `MSL_MACOS_VIEW`, and `msl --version --json` reports `macos` instead of `macOS`. Update scripts, shell profiles and editor settings that use the old names; there's no compatibility link.
- Messages say "macOS" throughout, instead of mixing "Mac" and "macOS".
- `msl --version` and `msld`'s log show the commit a build came from, as `0.1.7+3af5916` (with `.dirty` for uncommitted changes). Update checks still compare the plain version.
- Kernel releases are tagged with a hash of their configuration instead of a counter, for example `kernel-6.18.15-msl-76f230e`. `msl --version` shows it.
- The kernel enables device-mapper and the NBD client. See [Kernel release notes]({{< relref "/docs/release-notes/kernel" >}}).
- The VM's initial RAM disk carries static `e2fsck` and `resize2fs` from Debian's e2fsprogs 1.47.2 (GPL-2.0), to check and grow the shared disk. Their source is attached to each release.

**Fixed**

- `msl --shutdown` leaves the shared disk clean. It used to power off with the filesystem still marked for journal recovery, which then ran at every boot ([#45](https://github.com/onexay/msl/issues/45)).

## 0.1.6

25 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.6)

**Changed**

- **Breaking:** `msl --manage <distro> --move` fails with "not supported" instead of reporting success. It only recorded the location: every distribution lives on the shared disk, so nothing was moved.
- The VM section of `~/.mslconfig` is now `[msl2]`. `[wsl2]` still works, so existing files and a copied `.wslconfig` need no change.

**Fixed**

- Names that are CNAME aliases, such as deb.debian.org, cdn.kernel.org and www.apple.com, resolve in distributions again ([#42](https://github.com/onexay/msl/issues/42)). 0.1.5's DNS fix made macOS report the CNAME record as well, and `msld` then answered with the alias alone or with records glibc rejects, so `apt` and `curl` couldn't reach those hosts.

## 0.1.5

25 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.5)

**Fixed**

- DNS lookups no longer stall for 5 to 10 seconds when a name has an IPv4 address but no IPv6 one, as github.com does ([#41](https://github.com/onexay/msl/issues/41)). `msld` now passes on macOS's "no such record" answer instead of waiting for a timeout. Tools that look up both address families, such as curl, git and VS Code's extension host, used to hit connect timeouts; VS Code timed out connecting to `api.github.com` while cloning.

## 0.1.4

25 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.4)

**Added**

- `msl --manage-ide [--ide <vscode|vscode-insiders|vscode-oss|cursor|all>] [--install|--uninstall]` sets up the VS Code extension ([#35](https://github.com/onexay/msl/issues/35)). It installs the bundled extension and enables its proposed API in the IDE's `argv.json`, keeping comments and other keys. Without options, it lists the IDEs it finds and asks what to do. The installer runs it for the IDEs it finds (`--no-ide` skips this), and `msl --uninstall` undoes it.
- A preview VS Code extension that opens folders inside a distribution, with no SSH and no network port on macOS. See [Get started with VS Code]({{< relref "/docs/tutorials/msl-vscode" >}}) and the [VS Code extension release notes]({{< relref "/docs/release-notes/vscode" >}}).
- `msld`'s connect socket, `connect.sock`, which the extension uses to open byte streams into a distribution ([#32](https://github.com/onexay/msl/issues/32)).

**Changed**

- **Breaking:** distribution files on macOS moved from `~/MSL/<distro>` to `~/.msl/distros/<distro>`, so they no longer add a visible folder to your home directory. Each distribution still appears in Finder under Locations with its logo. On start, `msld` unmounts old `~/MSL` mounts and removes `~/MSL` if it's empty. `MSL_VIEW_DIR` still overrides the location.
- x86_64-only distributions (Arch Linux, SUSE Linux Enterprise, eLxr) are no longer offered by `msl --list --online`, and `msl --install` refuses them ([#40](https://github.com/onexay/msl/issues/40)). `--install --from-file` accepts x86_64 images, but MSL doesn't support starting x86_64-only distributions.
- Releases no longer include a `.pkg`. `install.sh` is the way to install MSL, and the only one that sets up IDEs.
- The VS Code extension has its own releases, `vscode-<version>`, like the kernel. Each MSL release bundles the published one.

**Fixed**

- `msl --help` lists every command `msl` accepts, adding `--debug-shell`, `--mount` and `--unmount`, `--update`, `--uninstall`, `--manage`, `--set-version`, `--set-default-version` and `--list --online`.
- `msld` removes its VM bridge sockets when the VM stops, so stale sockets no longer pile up.

## 0.1.3

25 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.3)

**Added**

- `--json` for the query commands: `--list` and its variants, `--list --online`, `--status` and `--version`. Errors go to stderr as JSON, with `wsl.exe`'s exit codes.

## 0.1.2

24 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.2)

**Fixed**

- Stopping a distribution (`--terminate`, the idle timeout, `--shutdown`) shuts it down cleanly instead of killing it ([#19](https://github.com/onexay/msl/issues/19)). systemd distributions power off, and other distributions' processes get `SIGTERM`. Anything still running after 10 seconds is killed. Previously journald reported "corrupted or uncleanly shut down" journals, and services could lose unflushed data.
- The network interface stays `eth0`, as in WSL ([#20](https://github.com/onexay/msl/issues/20)). systemd 259, in Ubuntu 26.04, treats the distribution as a container, so it ignored `net.ifnames=0` and renamed the interface to `enp0s1`.

## 0.1.1

24 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.1) · kernel `kernel-6.18.15-msl.1`

The first release. (0.1.0 was withdrawn before it was announced; 0.1.1 replaces it.)

- The `wsl.exe` command line on macOS, with the same arguments, behaviour and messages: install, import, export and unregister; list, set the default, terminate and shut down; `--status`, `--manage`, `--mount` and `--unmount`; `--debug-shell`, `--update`, `--uninstall` and `--version`.
- Unmodified arm64 WSL distribution images, from Microsoft's distribution list or a `.wsl` file, in one lightweight Virtualization.framework VM. Each distribution gets its own init and can run systemd.
- Integration with macOS: the macOS filesystem in every distribution, with `msl` starting in your current macOS directory; `MSLENV` and `mslpath`; localhost forwarding and DNS through macOS; each distribution's files in Finder, with the distribution's logo.
- `~/.mslconfig` (the `.wslconfig` equivalent), `/etc/wsl.conf` and `/etc/msl.conf`, idle timeouts, and MSL's own first-run setup for Debian.
- An interactive installer, `install.sh`, and self-update with `msl --update`.
- PGP-signed release checksums: `install.sh` verifies the signature when `gpg` is installed and a signature is published.
- Releases include the full licence texts of all dependencies, and the GPL source of BusyBox and the kernel.
- Licensed under Apache-2.0.
