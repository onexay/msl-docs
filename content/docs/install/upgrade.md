---
title: Update and uninstall MSL
weight: 3
description: Update MSL to a new release, check for breaking changes, and remove MSL.
---

## Update MSL

```console
$ msl --update
```

This installs the latest release in place and keeps your distributions and settings. `msl --update --pre-release` installs a pre-release if one is available. [Release notes]({{< relref "/docs/release-notes" >}}) lists what changed.

## Breaking changes

These changes can break a script or a habit. Newest first.

### 0.1.10: reinstall on macOS 26 if you have 0.1.9

MSL 0.1.9 was built with an Xcode newer than MSL's minimum macOS, and its service doesn't start on macOS 26. If you installed 0.1.9 on macOS 26, reinstall with the one-line installer from [Install MSL]({{< relref "/docs/install/install" >}}). Your distributions are kept. On macOS 27, `msl --update` is enough.

### 0.1.7: `/mnt/mac` is now `/mnt/macos`

| Before 0.1.7 | From 0.1.7 |
|---|---|
| macOS files at `/mnt/mac` | `/mnt/macos` |
| With `[automount] root=/`: `/mac` | `/macos` |
| `MSL_MAC_USER`, `MSL_MAC_HOME`, `MSL_MAC_VIEW` | `MSL_MACOS_USER`, `MSL_MACOS_HOME`, `MSL_MACOS_VIEW` |
| `msl --version --json`: key `macOS` | key `macos` |

Update scripts, shell profiles and editor settings that use the old names. There's no link from `/mnt/mac`.

### 0.1.6: `--manage --move` is refused

`msl --manage <distro> --move <location>` used to report success without moving anything, because every distribution lives on one shared disk. It now fails with "not supported".

The VM section of `~/.mslconfig` is now `[msl2]`. `[wsl2]` still works, so a copied `.wslconfig` needs no change.

### 0.1.4: distribution files moved to `~/.msl/distros`

Distribution files on macOS moved from `~/MSL/<distro>` to `~/.msl/distros/<distro>`. Finder still lists each distribution under Locations.

## Uninstall MSL

```console
$ msl --uninstall
```

This removes MSL and undoes the VS Code setup. Your distributions and settings stay in `~/Library/Application Support/msl`, so installing MSL again brings them back. The line the installer added to your shell's startup file stays; remove it by hand.

## Remove everything, including distributions

{{< callout type="warning" >}}
This deletes every distribution and all the files in them, permanently. Export any distribution you want to keep first: `msl --export <distro> <file>`.
{{< /callout >}}

1. Stop every distribution and the VM:

    ```console
    $ msl --shutdown
    ```

2. Uninstall MSL:

    ```console
    $ msl --uninstall
    ```

3. Delete MSL's data, downloads and settings:

    ```console
    $ rm -rf ~/Library/Application\ Support/msl ~/Library/Caches/msl ~/.mslconfig
    ```

`~/Library/Application Support/msl` holds `data.img`, the disk with every distribution on it. `~/Library/Caches/msl` holds downloaded images, and `~/.mslconfig` exists only if you created it.
