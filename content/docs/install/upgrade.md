---
title: Update and uninstall MSL
weight: 3
description: Update MSL to a new release or remove it.
---

## Update MSL

```console
$ msl --update
```

This installs the latest release in place and keeps your distributions and settings, and updates the VS Code extension in each IDE that has it. `msl --update --pre-release` installs a pre-release if one is available. [Release notes]({{< relref "/docs/release-notes" >}}) lists what changed.

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

`~/Library/Application Support/msl` holds each distribution's disk, `distros/<id>/ext4.img`, and `data.img`, the shared disk of distributions from earlier versions. A distribution installed or moved to another folder keeps its `ext4.img` there; delete it with `msl --unregister <distro>` before you uninstall. `~/Library/Caches/msl` holds downloaded images, and `~/.mslconfig` exists only if you created it.
