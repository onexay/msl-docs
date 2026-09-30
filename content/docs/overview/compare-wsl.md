---
title: Comparing MSL and WSL
weight: 2
description: What works the same in MSL as in WSL 2, and what's different on macOS.
---

MSL aims to behave like WSL 2, so that one set of instructions works on Windows and macOS. This page lists where it matches and where macOS makes it differ.

## Comparing features

| Feature | WSL 2 | MSL |
|---|---|---|
| Host | Windows | macOS 26 or later, Apple silicon |
| Command line | `wsl.exe` | `msl`: the same arguments, messages and exit codes |
| Distribution images | Microsoft's WSL distribution list, `.wsl` images | The same list and images, arm64 variants, unmodified |
| Architecture | One shared utility VM, per-distribution namespaces | The same |
| Per-distribution settings | `/etc/wsl.conf` | `/etc/wsl.conf`, or `/etc/msl.conf` if present (supported keys below) |
| VM settings | `.wslconfig` | `~/.mslconfig`, same keys; a `.wslconfig` can be copied as is |
| systemd | Yes | Yes, with `[boot] systemd=true` |
| Host files in Linux | `/mnt/c`, `/mnt/d` | `/mnt/macos` |
| Linux files on the host | `\\wsl.localhost\<distro>` in File Explorer | `~/.msl/distros/<distro>` and Finder's Locations, while the VM runs |
| Path conversion, environment | `wslpath`, `WSLENV`, `WSL_DISTRO_NAME` | `mslpath`, `MSLENV`, `MSL_DISTRO_NAME` |
| Running host programs from Linux | Yes (`notepad.exe`) | No, by design |
| Networking | NAT, or mirrored | NAT only |
| localhost forwarding | Yes | Yes, IPv4 and IPv6 |
| DNS through the host | `dnsTunneling` | Yes, through macOS's resolver |
| Disks | One `ext4.vhdx` per distribution | One `ext4.img` per distribution: raw ext4, not VHDX |
| Nested virtualization | `nestedVirtualization` | The same, on a Mac with an M3 chip or later |
| Memory returned to the host while running | Yes (`autoMemoryReclaim`) | No, only when the VM stops |
| GUI apps (WSLg), GPU | Yes | No |
| USB devices | With usbipd-win | No; disk images only (`msl --mount`) |
| x86_64 distributions | Native | Not yet |
| WSL 1 | Yes | No; every distribution is version 2 |
| JSON output | No | `--json` on `--list`, `--status` and `--version` |

## Distributions and `wsl.conf`

MSL runs the images from Microsoft's WSL distribution list, which is what `msl --list --online` shows. It uses the arm64 variants, and runs each image's own first-run setup, including its `wsl-distribution.conf`. Ubuntu 26.04 and 24.04, and Debian 13, are tested. The only file MSL adds to an image is the `/usr/bin/mslpath` link.

Some first-run scripts print Windows wording, such as "Provisioning the new WSL instance". That's their stock text; MSL skips the steps that need Windows.

MSL reads `/etc/msl.conf`, falling back to `/etc/wsl.conf`. It supports these keys:

| Section | Keys |
|---|---|
| `[boot]` | `systemd`, `command` |
| `[user]` | `default` |
| `[automount]` | `enabled`, `root`, `mountFsTab` |
| `[network]` | `hostname`, `generateHosts`, `generateResolvConf` |

`[interop]` is read and ignored. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

## No interop with macOS programs

WSL can run Windows programs from Linux, and puts Windows directories on Linux's `PATH`. MSL never runs macOS programs from Linux and never adds macOS paths to `PATH`. Build tools such as `npm`, `node-gyp` and `configure` therefore find only Linux toolchains, and build output is always Linux, even under `/mnt/macos`. WSL detection stays off, so tools don't assume Windows interop.

## Disks

As in WSL, each distribution has its own sparse disk, and `--manage --move`, `--manage --resize`, `--export --vhd`, `--import --vhd` and `--import-in-place` work. The differences:

- The disk is a raw ext4 image, `ext4.img`, not VHDX. Convert with `qemu-img convert -O raw` or `-O vhdx`.
- Disks can't be added to a running VM. A disk added while a distribution runs is mounted through the Mac file share until the VM restarts: slower, and `fsync` there doesn't reach the SSD right away. See [How disks are attached]({{< relref "/docs/how-to/disk-space#how-disks-are-attached" >}}).
- Up to 19 distribution disks are attached when the VM starts.
- Distributions from MSL 0.1.11 or earlier stay on one shared disk, `data.img`, until you move them.

See [Manage disk space]({{< relref "/docs/how-to/disk-space" >}}).

## Memory

Virtualization.framework doesn't give memory back to macOS while the VM runs. Memory the distributions used goes back when the VM stops: 60 seconds after the last distribution stops, or at `msl --shutdown`. `autoMemoryReclaim` is accepted and has no effect.

## Not available yet

- x86_64-only distributions. `msl --list --online` leaves them out, and `msl --install` refuses them ([#40](https://github.com/onexay/msl/issues/40)).
- GUI apps, GPU access and USB devices.
- Mirrored networking.
- Shrinking a disk.

Planned work is in the [milestones](https://github.com/onexay/msl/milestones).
