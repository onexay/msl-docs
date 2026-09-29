---
title: Manual install steps
weight: 2
description: Install MSL from a downloaded release, without questions, or with the VS Code extension set up by hand.
---

The one-line installer in [Install MSL]({{< relref "/docs/install/install" >}}) suits most people. This page covers installing a release you downloaded yourself, installing without questions, and what the installer changes on your Mac.

## Step 1: Download a release

1. Open the [latest release](https://github.com/onexay/msl/releases/latest) and download `msl-<version>-macos-arm64.tar.gz` and its `.sha256` file.
2. Check the download:

    ```console
    $ shasum -a 256 -c msl-<version>-macos-arm64.tar.gz.sha256
    ```

## Step 2: Install it

Download the installer and point it at the file:

```console
$ curl -fsSL -o install.sh https://raw.githubusercontent.com/onexay/msl/main/install.sh
$ sh install.sh --from msl-<version>-macos-arm64.tar.gz
```

## Install without questions

Pass `--yes` and any options you need:

```console
$ curl -fsSL https://raw.githubusercontent.com/onexay/msl/main/install.sh | sh -s -- --yes [options]
```

| Option | Effect |
|---|---|
| `--prefix <dir>` | Where to install. The default is `~/.local`, which needs no sudo. `/usr/local` asks for sudo. |
| `--version <x.y.z>` | Install a specific release instead of the latest. |
| `--from <tarball>` | Install a downloaded `msl-<version>-macos-arm64.tar.gz`. |
| `--no-path` | Don't add MSL to `PATH`. |
| `--no-ide` | Don't set up the VS Code extension. |
| `--yes`, `-y` | Accept the defaults without asking. |

MSL has no Homebrew formula. It updates itself with `msl --update`.

## What the installer changes

| What | Where | Removed by |
|---|---|---|
| MSL itself: the command, the service, the kernel and VM image, the VS Code extension | `<prefix>/bin/msl`, `<prefix>/libexec/msl/msld`, `<prefix>/share/msl/`, `<prefix>/share/doc/msl/` | `msl --uninstall` |
| `PATH` | One line in `~/.zshrc`, `~/.bash_profile`, `~/.config/fish/config.fish` or `~/.profile` | Removing the line by hand |
| VS Code extension | Each IDE's extensions folder | `msl --manage-ide --ide all --uninstall`, or `msl --uninstall` |
| `enable-proposed-api` | Each IDE's `argv.json`, for example `~/.vscode/argv.json`. The first change saves a backup, `argv.json.msl-backup`. | The same; the entry is removed |
| Which `msl` the extension runs | `~/Library/Application Support/msl/cli-path` | The same |

MSL creates these the first time you use it:

| What | Where |
|---|---|
| Distributions and state | `~/Library/Application Support/msl/`: each distribution's sparse disk, `distros/<id>/ext4.img` (unless you chose another location), plus `registry.json`, `msld.log` and the service's sockets |
| Distribution files in Finder | `~/.msl/distros/<distro>`, while the VM runs |
| Downloads | `~/Library/Caches/msl/`: distribution images, and the VS Code Server for your IDE's version |
| VM settings | `~/.mslconfig`, only if you create it |

MSL doesn't install a LaunchAgent, a kernel extension or a login item. `msld` starts when you first run `msl`, and stops the VM 60 seconds after nothing is running.

## Install the VS Code extension by hand

The installer sets up the extension if it finds VS Code, VS Code Insiders, VSCodium or Cursor. Later, run `msl --manage-ide`. To install it without `msl`:

1. Download `msl-<version>.vsix` from the latest [extension release](https://github.com/onexay/msl-vscode-extension/releases).
2. Install it:

    ```console
    $ code --install-extension msl-<version>.vsix
    ```

3. In VS Code, run **Preferences: Configure Runtime Arguments**, add `"enable-proposed-api": ["onexay.msl"]` to `argv.json`, and save.
4. Quit VS Code with ⌘Q and open it again. Closing the window isn't enough.

The extension isn't on the Visual Studio Marketplace, because it uses VS Code's proposed remote-resolver API. See [Get started with VS Code]({{< relref "/docs/tutorials/msl-vscode" >}}).
