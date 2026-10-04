---
title: Kernel release notes
linkTitle: Kernel
weight: 2
description: The current Linux kernel release bundled with MSL.
---

MSL runs its own arm64 build of the Linux kernel: unmodified Linux from kernel.org, configured with Apple's configuration for its `container` tool plus MSL's additions. The configuration and build scripts are in [onexay/msl-kernel](https://github.com/onexay/msl-kernel). `msl --version` shows the bundled kernel version.

## v6.18.15+0752837

Linux 6.18.15 for arm64 · 4 October 2026 · bundled with MSL 0.1.0 · [GitHub release](https://github.com/onexay/msl-kernel/releases/tag/v6.18.15%2B0752837)

- Built from kernel commit [`0752837`](https://github.com/onexay/msl-kernel/commit/0752837095020c64360856581bb7c285badeebe8). `uname -r` reports `6.18.15-msl-0752837`.
- The release includes the arm64 kernel image (`Image`), configuration, `kernel.version`, build provenance, `release.sha256` checksums and the matching Linux 6.18.15 source archive (GPL-2.0).
- Pin this release in MSL with `scripts/pin.sh kernel v6.18.15+0752837`.
