---
title: VS Code extension release notes
linkTitle: VS Code extension
sidebar_position: 3
description: The current MSL extension release for VS Code, VS Code Insiders, VSCodium and Cursor.
---

The MSL extension opens folders inside a distribution from VS Code, VS Code Insiders, VSCodium or Cursor. Its source is in [onexay/msl-vscode-extension](https://github.com/onexay/msl-vscode-extension). MSL installs the bundled extension with `msl --manage-ide`. The extension uses VS Code's proposed remote-resolver API, so it isn't on the Visual Studio Marketplace. See [Get started with VS Code](../tutorials/msl-vscode.md).

## v0.2.0

MSL VS Code extension release · 19 October 2026 · [GitHub release](https://github.com/onexay/msl-vscode-extension/releases/tag/v0.2.0)

## What's Changed
* Bump actions/download-artifact from 7 to 8 in the actions group by @dependabot[bot] in https://github.com/onexay/msl-vscode-extension/pull/1
* Document the initial extension release by @onexay in https://github.com/onexay/msl-vscode-extension/pull/2
* Generate extension release notes on GitHub by @onexay in https://github.com/onexay/msl-vscode-extension/pull/3
* Add MSL extension icon by @onexay in https://github.com/onexay/msl-vscode-extension/pull/5

## New Contributors
* @dependabot[bot] made their first contribution in https://github.com/onexay/msl-vscode-extension/pull/1
* @onexay made their first contribution in https://github.com/onexay/msl-vscode-extension/pull/2

**Full Changelog**: https://github.com/onexay/msl-vscode-extension/compare/v0.1.0...v0.2.0

## v0.1.0

4 October 2026 · bundled with MSL 0.1.0 · [GitHub release](https://github.com/onexay/msl-vscode-extension/releases/tag/v0.1.0)

- The standalone VSIX is `msl-0.1.0.vsix`; its release includes `release.sha256`.
- Built by the release workflow from commit [`64fd4bb`](https://github.com/onexay/msl-vscode-extension/commit/64fd4bbcec22a077c7ccd5e7d399fbebd1c66093).
- Install it through MSL with `msl --manage-ide`.
