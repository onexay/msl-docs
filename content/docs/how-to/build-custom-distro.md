---
title: Build a custom distribution
weight: 2
description: Package a Linux distribution as a .wsl image that MSL installs like the ones in Microsoft's list, with its own first-run setup and Finder icon.
---

MSL installs the same `.wsl` images as WSL. If you build one for arm64, it installs on MSL with `msl --install --from-file`, and you can publish it in your own distribution list.

## What a `.wsl` file is

A `.wsl` file is a tar file, usually gzip-compressed, containing a distribution's root filesystem. It can include `/etc/wsl-distribution.conf`, which describes how the distribution is set up when it's installed. MSL reads the image as it is; the only file it adds is the `/usr/bin/mslpath` symlink.

To build one, prepare an arm64 root filesystem, add the files below, and tar it from the root:

```console
$ sudo tar --numeric-owner -czf ../mydistro.wsl -C rootfs .
```

## `/etc/wsl-distribution.conf`

MSL honours these keys. Others are ignored.

| Key | Meaning in MSL |
|---|---|
| `[oobe] command` | A command run as root the first time a user opens an interactive shell in the distribution, typically a script that creates the user account. It runs from `/`, with `WSL_DISTRO_NAME` set to the distribution's name and `MSL_MACOS_USER` set to your macOS user name. If it fails, it runs again on the next interactive start. |
| `[oobe] defaultUid` | The user that shells run as once the first-run command succeeds, usually `1000`, the account the command created. |
| `[oobe] defaultName` | The distribution's name when you install without `--name`. |
| `[shortcut] icon` | A Windows `.ico` file in the image, for example `/usr/share/wsl/mydistro.ico`. MSL converts it and uses it as the distribution's icon in Finder. |

An example:

```ini
[oobe]
command = /usr/lib/wsl/first-setup.sh
defaultUid = 1000
defaultName = MyDistro

[shortcut]
icon = /usr/share/wsl/mydistro.ico
```

The first-run command only runs for an interactive shell (`msl -d MyDistro` in a terminal), not for `msl -e` or piped commands, so scripts don't hang on its prompts. Write it so it works on both WSL and MSL: it can't run Windows programs on MSL, and it shouldn't rely on anything under `/mnt/c`.

Settings for the running distribution, such as systemd, the default user and mounts, belong in `/etc/wsl.conf`. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

## Test it

```console
$ msl --install --from-file mydistro.wsl
$ msl -d MyDistro
```

Without `--name`, the distribution takes `defaultName` from `/etc/wsl-distribution.conf`. If the image has none, the install fails and asks for `--name`. To test the first run again, remove the distribution and reinstall it:

```console
$ msl --unregister MyDistro
```

## Publish a distribution list

`msl --list --online` and `msl --install <Distro>` read Microsoft's distribution list, [`DistributionInfo.json`](https://github.com/microsoft/WSL/blob/master/distributions/DistributionInfo.json). Set `MSL_DISTRIBUTION_LIST_URL` to use a list of your own instead, for example your company's images:

```console
$ export MSL_DISTRIBUTION_LIST_URL=https://example.com/msl/distributions.json
$ msl --list --online
$ msl --install MyDistro
```

The URL can be `https://` or a `file://` path. The list uses the format of Microsoft's file. MSL reads these fields:

```json
{
  "Default": "MyDistro",
  "ModernDistributions": {
    "MyDistro": [
      {
        "Name": "MyDistro",
        "FriendlyName": "My Distro 1.0",
        "Default": true,
        "Arm64Url": {
          "Url": "https://example.com/msl/mydistro-1.0-arm64.wsl",
          "Sha256": "<SHA-256 of the file>"
        }
      }
    ]
  }
}
```

- Entries are grouped by flavor. `msl --install <flavor>` installs the flavor's entry marked `"Default": true`; any entry can also be installed by its `Name`.
- The top-level `Default` is what `msl --install` installs when you don't name a distribution.
- MSL uses `Arm64Url`. It checks the download against `Sha256` and refuses it on a mismatch. Entries with only an `Amd64Url` (x86_64) aren't listed.
- Downloads are cached in `~/Library/Caches/msl/downloads`, keyed by their SHA-256.

A list written for WSL works unchanged, as long as its entries have an `Arm64Url`.
