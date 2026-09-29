---
title: Kernel release notes
linkTitle: Kernel
weight: 2
description: Releases of the Linux kernel MSL runs, newest first, and which MSL releases bundle each one.
---

MSL runs its own build of the Linux kernel: unmodified Linux from kernel.org, configured with Apple's configuration for its `container` tool plus MSL's additions. The configuration and build scripts are in [onexay/msl-kernel](https://github.com/onexay/msl-kernel). Each MSL release bundles one kernel release; `msl --version` shows which.

Kernel releases are tagged `kernel-<Linux version>-msl-<hash>`, where the hash covers the Linux version and the configuration. The same configuration always gives the same tag. Each release has the kernel image, its configuration, checksums, and the corresponding kernel.org source (GPL-2.0).

## kernel-6.18.15-msl-21f0ec7

Linux 6.18.15 · 28 September 2026 · bundled with MSL 0.1.11 and later · [GitHub release](https://github.com/onexay/msl-kernel/releases/tag/kernel-6.18.15-msl-21f0ec7)

- **16 KiB memory pages**, matching the Mac ([#48](https://github.com/onexay/msl/issues/48)). With 4 KiB pages in the VM, Virtualization.framework's handling of 4 KiB pages corrupts the guest kernel's memory when macOS compresses or swaps the VM's memory: every distribution could crash within seconds under memory pressure. Kernels with 16 KiB pages run clean. `getconf PAGESIZE` now shows `16384`.
- Ubuntu 22.04 and 26.04, Debian 13, Fedora 44, AlmaLinux 9 and Kali were checked: no binary or library needs pages smaller than 16 KiB, and systemd, package managers, Python and jemalloc work. Programs built to assume 4 KiB pages don't run; see [Troubleshooting]({{< relref "/docs/troubleshooting" >}}).

This release was first published in the msl repository; the copy in msl-kernel has identical files.

## kernel-6.18.15-msl-76f230e

Linux 6.18.15 · 25 September 2026 · bundled with MSL 0.1.7 to 0.1.10 · [GitHub release](https://github.com/onexay/msl/releases/tag/kernel-6.18.15-msl-76f230e)

- Enables device-mapper (`CONFIG_MD`, `CONFIG_BLK_DEV_DM`) and the NBD client (`CONFIG_BLK_DEV_NBD`).
- The first kernel tagged with a configuration hash instead of a counter.

## kernel-6.18.15-msl.1

Linux 6.18.15 · 24 September 2026 · bundled with MSL 0.1.1 to 0.1.6 · [GitHub release](https://github.com/onexay/msl/releases/tag/kernel-6.18.15-msl.1)

The first MSL kernel. On top of Apple's 6.18 configuration, which already has namespaces, overlayfs, BPF, virtiofs and vsock, it adds:

- USB mass storage, for attaching disk images with `msl --mount`;
- ext4 quota support;
- the NFS server, which serves each distribution's files to Finder.
