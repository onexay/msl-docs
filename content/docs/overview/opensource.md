---
title: MSL open source code
weight: 4
description: Where MSL's source code lives, how it's licensed, and how to contribute.
---

MSL is open source and developed on GitHub. Its code is split across four repositories.

## Repositories

| Repository | What it contains |
|---|---|
| [onexay/msl](https://github.com/onexay/msl) | The `msl` command and the `msld` service (Swift), the guest init and agent that run inside the VM (Rust), the installer, and MSL releases |
| [onexay/msl-kernel](https://github.com/onexay/msl-kernel) | The Linux kernel configuration and build scripts, and kernel releases |
| [onexay/msl-vscode-extension](https://github.com/onexay/msl-vscode-extension) | The VS Code extension, and its releases |
| [onexay/msl-docs](https://github.com/onexay/msl-docs) | This documentation site |

Each MSL release bundles a specific kernel release and extension release. The release notes name them.

## Licence

MSL is licensed under the Apache License 2.0. Release packages also contain the Linux kernel, BusyBox and e2fsprogs, which are licensed under GPL-2.0 and run inside the VM as separate programs. Their corresponding source is attached to the GitHub releases: BusyBox and e2fsprogs to each MSL release, and the kernel to each kernel release.

## Report a bug or request a feature

- Search the [issues](https://github.com/onexay/msl/issues) first, including closed ones.
- To report a bug, open a [bug report](https://github.com/onexay/msl/issues/new/choose) with the output of `msl --version` and `msl --status`, and the relevant lines from `~/Library/Application Support/msl/msld.log`. Remove anything private first. See [Troubleshooting]({{< relref "/docs/troubleshooting" >}}).
- Report security problems privately, as described in the [security policy](https://github.com/onexay/msl/blob/main/SECURITY.md), not in a public issue.
- For documentation problems, open an issue in [msl-docs](https://github.com/onexay/msl-docs/issues), or use the edit link at the bottom of a page.

## Contribute

Start with [CONTRIBUTING.md](https://github.com/onexay/msl/blob/main/CONTRIBUTING.md) in msl. It covers setting up a build, running the tests and the pull-request process. For anything bigger than a small fix, open an issue first to agree on the approach. Behaviour follows WSL's, so the WSL behaviour is the spec for anything in the command line.

Every commit must be signed off under the [Developer Certificate of Origin](https://developercertificate.org/): `git commit -s`.
