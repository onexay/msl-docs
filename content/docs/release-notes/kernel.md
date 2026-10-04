---
title: Kernel release notes
linkTitle: Kernel
weight: 2
description: The current Linux kernel release bundled with MSL.
---

MSL runs its own arm64 build of the Linux kernel: unmodified Linux from kernel.org, configured with Apple's configuration for its `container` tool plus MSL's additions. The configuration and build scripts are in [onexay/msl-kernel](https://github.com/onexay/msl-kernel). `msl --version` shows the bundled kernel version.

## v6.18.15+b665f87

Linux 6.18.15 for arm64 · 3 October 2026 · bundled with MSL 0.1.0 · [GitHub release](https://github.com/onexay/msl-kernel/releases/tag/v6.18.15%2Bb665f87)

- Built from kernel commit [`b665f87`](https://github.com/onexay/msl-kernel/commit/b665f87dd1e4d2236d9b9e6c1a94ac2840aef225). `uname -r` reports `6.18.15-msl-b665f87`.
- The release includes the arm64 kernel image (`Image`), configuration, `kernel.version`, build provenance, `release.sha256` checksums and the matching Linux 6.18.15 source archive (GPL-2.0).
- Pin this release in MSL with `scripts/pin.sh kernel v6.18.15+b665f87`.
