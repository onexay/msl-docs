---
title: MSL release notes
linkTitle: MSL
weight: 1
description: The current MSL release and its changes.
---

Update MSL to the current release with `msl --update`. These notes follow the release notes published with each GitHub release.

## v0.1.1

MSL release · 8 October 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.1)

### Added
- Mirror macOS proxy settings into new distro sessions with `autoProxy`, and optionally use the Mac's DNS servers with `dnsProxy` when DNS tunneling is off.

### Fixed
- Check ext4 disks with recorded filesystem errors before mounting them.

## v0.1.0

4 October 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/v0.1.0) · kernel [`v6.18.15+0752837`](https://github.com/onexay/msl-kernel/releases/tag/v6.18.15%2B0752837) · VS Code extension [`v0.1.0`](https://github.com/onexay/msl-vscode-extension/releases/tag/v0.1.0)

**Changed**

- **Breaking:** MSL requires macOS 27 or later. Its GPU device is available on macOS 27; on older versions, the installer, `msl`, `msld` and `msl --update` stop with a clear message.
- Kernel and VS Code extension pins accept SemVer release tags while continuing to support existing pins.
- `msl --version` and development VSIX versions show plain SemVer. JSON version output retains the MSL commit, and the kernel's `uname -r` includes its short source hash.
- Build, install, fetch and end-to-end scripts now live in `scripts/`. The root `install.sh` remains the public installer entry point.
- Shared code and protocol definitions live in `core/`, macOS executables and services in `host/`, and Swift, Rust and end-to-end tests in `tests/`.

Install with `sh install.sh` or `sh install.sh --version 0.1.0`. Update an existing installation with `msl --update`.

The release archive is ad-hoc signed, not notarised, and its SHA-256 checksum is not PGP-signed. The archive is `msl-0.1.0-macos-arm64.tar.gz`.
