---
title: VS Code extension release notes
linkTitle: VS Code extension
weight: 3
description: The current MSL extension release for VS Code, VS Code Insiders, VSCodium and Cursor.
---

The MSL extension opens folders inside a distribution from VS Code, VS Code Insiders, VSCodium or Cursor. Its source is in [onexay/msl-vscode-extension](https://github.com/onexay/msl-vscode-extension). MSL installs the bundled extension with `msl --manage-ide`. The extension uses VS Code's proposed remote-resolver API, so it isn't on the Visual Studio Marketplace. See [Get started with VS Code]({{< relref "/docs/tutorials/msl-vscode" >}}).

## v0.1.0

3 October 2026 · bundled with MSL 0.1.0 · [GitHub release](https://github.com/onexay/msl-vscode-extension/releases/tag/v0.1.0)

- The standalone VSIX is `msl-0.1.0.vsix`; its release includes `release.sha256`.
- Built by the release workflow from commit [`6cec07d`](https://github.com/onexay/msl-vscode-extension/commit/6cec07d80c363779ba85eb228ff89a919460c0e7).
- Install it through MSL with `msl --manage-ide`.
