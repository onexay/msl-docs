---
title: Get started using VS Code with MSL
weight: 2
description: Use the MSL extension to open folders inside a Linux distribution from VS Code, VS Code Insiders, VSCodium or Cursor on macOS.
---

The MSL extension lets VS Code work inside a Linux distribution, the way VS Code's WSL extension does on Windows. The window runs on macOS, while the terminal, language servers, debuggers and extensions run in the distribution. It works with VS Code, VS Code Insiders, VSCodium and Cursor.

## Prerequisites

- MSL 0.1.3 or later, with a distribution installed. See [Install MSL]({{< relref "/docs/install/install" >}}).
- VS Code, VS Code Insiders, VSCodium or Cursor installed on macOS.

## Set up the extension

The MSL installer sets the extension up if it finds one of those IDEs. To set it up later, or for another IDE:

```console
$ msl --manage-ide                             # lists the IDEs found and asks
$ msl --manage-ide --ide vscode --install      # or vscode-insiders, vscode-oss, cursor, all
```

Then quit the IDE with ⌘Q and reopen it. Closing the window isn't enough.

`--manage-ide --install` installs the extension with the IDE's own command-line tool. It also adds `"enable-proposed-api": ["onexay.msl"]` to the IDE's `argv.json`, keeping its comments and other settings. The first change saves a backup, `argv.json.msl-backup`.

To remove the extension and the `argv.json` entry:

```console
$ msl --manage-ide --ide all --uninstall
```

`msl --uninstall` does the same.

### Install the extension by hand

The extension isn't on the Visual Studio Marketplace. To install it without `--manage-ide`:

1. Download `msl-<version>.vsix` from the newest [extension release](https://github.com/onexay/msl-vscode-extension/releases).
2. Install it:

    ```console
    $ code --install-extension msl-<version>.vsix
    ```

3. In VS Code, run **Preferences: Configure Runtime Arguments**, add `"enable-proposed-api": ["onexay.msl"]` to `argv.json`, save, and quit and reopen VS Code (⌘Q).

## Connect to a distribution

Open the command palette and run **MSL: Connect to Distro**, then pick a distribution. **MSL: Connect to Distro in New Window** keeps your current window.

The first connection installs the VS Code Server that matches your IDE's version into `~/.vscode-server` in the distribution. MSL downloads it on macOS and caches it in `~/Library/Caches/msl/vscode-server/`, so every distribution reuses it and none needs `curl` or `wget`.

## Open a folder

Once connected, use **File › Open Folder** to open a folder in the distribution, for example `~/src/project`. You can also open one directly from a macOS terminal:

```console
$ code --folder-uri vscode-remote://msl+Ubuntu/home/me/project
```

You can have windows open on several distributions at once. The window title and the remote indicator show `MSL: <distro>`.

Servers you start in the distribution are forwarded automatically. They appear in VS Code's Ports view and listen on macOS's `127.0.0.1`.

## How it connects

VS Code's WSL extension works only on Windows, because it calls `wsl.exe`. Remote - SSH would work with MSL, but it needs an SSH server in every distribution and a network port on macOS. The MSL extension connects VS Code to its server through MSL's own service and the VM's internal channel instead. It uses no SSH and opens no network port on macOS.

To connect to a remote machine, an extension needs VS Code's remote-resolver API. VS Code keeps that API "proposed": only Microsoft's own remote extensions may use it unless you enable it for an extension in `argv.json`. That's the change `--manage-ide` makes, and it's why the extension isn't on the Marketplace.

## Which msl the extension runs

The extension looks for `msl` in this order:

1. The `msl.path` setting, if it's set.
2. The `msl` that last ran `msl --manage-ide --install`. It records its path in `~/Library/Application Support/msl/cli-path`, so any install location works.
3. `~/.local/bin/msl`, then `/usr/local/bin/msl`, then `PATH`.

## Troubleshooting

The extension writes its log to **Output › MSL**.

**"No remote extension installed to resolve msl"**
: The extension didn't start. **Output › Log (Extension Host)** shows `CANNOT use API proposal: resolvers`. Run `msl --manage-ide`, or add `enable-proposed-api` to `argv.json` yourself with **Preferences: Configure Runtime Arguments**. Then quit the IDE with ⌘Q.

**"msl --list --verbose --json exited with 255"**
: The extension found an `msl` older than 0.1.3. Run `msl --manage-ide --install` with the `msl` you want, or set `msl.path`.

**`bash: warning: setlocale: … cannot change locale` in the terminal**
: The VS Code Server started without the distribution's locale. MSL 0.1.9 and later start it with the locale from `/etc/default/locale`. After updating, reload the window or run `msl --shutdown`.

For other problems, see [Troubleshooting]({{< relref "/docs/troubleshooting" >}}).
