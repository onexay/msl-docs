---
title: Manage disk space
weight: 6
description: How MSL stores distributions on one shared, sparse disk, and how to check, grow and compact it.
---

WSL gives each distribution its own virtual disk. MSL keeps every distribution on one shared disk, `~/Library/Application Support/msl/data.img`, where each distribution is a directory. They all draw on the same free space.

`data.img` is a sparse file: macOS stores only the blocks that hold data. A disk with a 256 GB maximum takes a few gigabytes on the Mac until the distributions fill it.

## Check how much space is used

```console
$ msl --status
  Disk:                      257 GB max, 5.2 GB used on macOS (data.img)
  macOS free space:          243.5 GB
```

While the VM is running, a `Disk free` line also shows the space left inside the disk.

{{< callout type="warning" >}}
Because the disk is sparse, distributions can't see that macOS is running out of space. When the Mac's disk is full, writes fail inside the distributions even though they still report free space. `msl --status` warns when macOS has less than 16 GB free and less than the distributions think they have. Free up space on macOS first.
{{< /callout >}}

## Choose the size

MSL creates the disk the first time the VM starts. Its maximum size is 256 GB, or the size of the Mac's disk if that's smaller, so distributions are never promised more space than the Mac has.

To pick another size, set `defaultVhdSize` in `~/.mslconfig` before the first start. The minimum is 4 GB.

```ini
[msl2]
defaultVhdSize = 512GB
```

Once `data.img` exists, the setting has no effect. Grow the disk instead.

## Grow the disk

Stop everything, then resize:

```console
$ msl --shutdown
$ msl --manage Ubuntu --resize 512GB
```

This grows `data.img`, and with it the space for every distribution. The distribution name is required only because WSL's command takes one. Every distribution must be stopped. MSL enlarges the file, restarts the VM, and checks and grows the file system before mounting it, which takes a few seconds for a 256 GB disk.

The disk can't shrink, and it can't grow beyond the size of the Mac's disk.

## Return space to macOS

Deleting files in a distribution frees space inside the disk, not on the Mac. MSL hands freed blocks back to macOS every time the VM shuts down. To do it now:

```console
$ msl --manage Ubuntu --compact
```

`--set-sparse` is accepted for compatibility; the disk is always sparse.

## Move or remove distributions

`msl --manage <Distro> --move` isn't supported: there's no per-distribution disk file to move. To copy a distribution somewhere else, export it and import it again. See [Import any Linux distribution]({{< relref "/docs/how-to/use-custom-distro" >}}).

`msl --unregister <Distro>` deletes a distribution and its files. The space it used becomes free inside the disk, and goes back to macOS at the next shutdown or `--compact`.
