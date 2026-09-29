---
title: VS Code extension release notes
linkTitle: VS Code extension
weight: 3
description: Releases of the MSL extension for VS Code, VS Code Insiders, VSCodium and Cursor, newest first.
---

The MSL extension opens folders inside a distribution from VS Code, VS Code Insiders, VSCodium or Cursor. Its source is in [onexay/msl-vscode-extension](https://github.com/onexay/msl-vscode-extension). Each MSL release bundles one extension release, and `msl --manage-ide` installs it. The extension uses VS Code's proposed remote-resolver API, so it isn't on the Visual Studio Marketplace. See [Get started with VS Code]({{< relref "/docs/tutorials/msl-vscode" >}}).

## 0.1.1

25 September 2026 · bundled with MSL 0.1.4 and later · [GitHub release](https://github.com/onexay/msl-vscode-extension/releases/tag/vscode-0.1.1)

- The extension runs the MSL that set it up ([#35](https://github.com/onexay/msl/issues/35)). `msl --manage-ide --install` records its own path, and the extension reads it, so MSL can be installed anywhere without setting `msl.path`. The lookup order is the `msl.path` setting, then the recorded path, then `~/.local/bin/msl`, `/usr/local/bin/msl` and `PATH`.

This release was first published in the msl repository; the copy in msl-vscode-extension has the identical file (SHA-256 `8123ad8ddb6afd42b04db6a176144b64c710d4a5c01e91c0750539530e2e812a`).

## 0.1.0

25 September 2026 · [GitHub release](https://github.com/onexay/msl/releases/tag/vscode-0.1.0)

The first release as a separate download. No MSL release bundled it: MSL 0.1.4, the first with the extension, shipped 0.1.1.

- Opens folders inside a distribution: **MSL: Connect to Distro**, or `vscode-remote://msl+<distro>/<path>`. The window stays on macOS, while the terminal, language servers, debuggers and extensions run in the distribution.
- Connects through `msld`'s connect socket and the VM's internal channel. It uses no SSH and opens no network port on macOS. With an older `msld`, it falls back to one `msl` process per connection.
- Installs the VS Code Server that matches your IDE's version into the distribution. It downloads the server on macOS and caches it for every distribution, so the distribution needs no `curl` or `wget`, as in stock Debian.
- Reuses a running server only if it's really the server and accepts connections, so it recovers after a VM restart, and starts one server when several connections open at once.
- Forwarded ports keep a download going when the local client reads slowly, instead of cutting it off.
