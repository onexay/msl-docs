---
title: Manage disk space
weight: 6
description: How MSL stores each distribution on its own sparse disk, and how to check, grow, compact, move, export and import disks.
---

As in WSL, each distribution has its own virtual disk: a sparse ext4 image named `ext4.img` in the distribution's install location. By default that's `~/Library/Application Support/msl/distros/<id>/ext4.img`. `msl --install --location <folder>` and `msl --import <Distro> <folder> <file>` put it in `<folder>`.

`ext4.img` is a sparse file: macOS stores only the blocks that hold data. A disk with a 256 GB maximum takes a few hundred megabytes on the Mac until the distribution fills it.

Distributions installed by MSL 0.1.11 or earlier stay on the old shared disk, `~/Library/Application Support/msl/data.img`, where each distribution is a directory. Give one its own disk with `--move`; see [Move a distribution](#move-a-distribution).

## How disks are attached

Virtualization.framework can't add a disk to a running VM, so MSL starts the VM with 16 empty disk slots and fills them as needed: every distribution's disk when the VM starts, and a distribution's disk when you use it. With all 16 slots taken, the stopped distribution used longest ago gives its slot up. Only distributions whose disk is attached appear in `~/.msl/distros`.

## Check how much space is used

```console
$ msl --status
  Distribution disks:        3 disks, 2.4 GB used on macOS (768 GB max)
  macOS free space:          243.5 GB
```

While any distribution is still on `data.img`, `Shared disk` lines show that disk too.

{{< callout type="warning" >}}
Because the disks are sparse, distributions can't see that macOS is running out of space. When the Mac's disk is full, writes fail inside the distributions even though they still report free space. `msl --status` warns when macOS has less than 16 GB free and less than the disks can still grow by. Free up space on macOS first.
{{< /callout >}}

## Choose the size

A new disk is 256 GB, or the size of the Mac's disk if that's smaller, so a distribution is never promised more space than the Mac has. To choose the size for one distribution:

```console
$ msl --install Ubuntu --vhd-size 64GB
```

To change the default for new distributions, set `defaultVhdSize` in `~/.mslconfig`:

```ini
[msl2]
defaultVhdSize = 512GB
```

The minimum is 4 GB and the maximum 4 TB.

## Grow a disk

Stop the distribution, then resize its disk:

```console
$ msl --terminate Ubuntu
$ msl --manage Ubuntu --resize 512GB
```

MSL enlarges the file, and the VM checks and grows the file system before mounting it again, which takes a few seconds. Other distributions keep running.

The disk can't shrink, and it can't grow beyond the size of the Mac's disk or 4 TB.

For a distribution still on `data.img`, `--resize` grows `data.img`, and with it the space for every distribution on it. Every distribution must be stopped first (`msl --shutdown`).

## Return space to macOS

Deleting files in a distribution frees space inside its disk, not on the Mac. MSL hands freed blocks back to macOS every time the VM shuts down. To do it now:

```console
$ msl --manage Ubuntu --compact
```

`--set-sparse` is accepted for compatibility; disks are always sparse.

## Move a distribution

```console
$ msl --manage Ubuntu --move /Volumes/External/Ubuntu
```

This stops the distribution and moves its `ext4.img` into the new folder: a rename on the same volume, a copy to another one. A distribution still on `data.img` gets a disk of its own in that folder: MSL copies its files over and then deletes them from `data.img`.

## Export and import disk images

A distribution's disk can be copied out and registered again as a new distribution, as with WSL's `--vhd` options:

```console
$ msl --export Ubuntu ubuntu.img --vhd
$ msl --import Ubuntu-2 ~/distros/ubuntu-2 ubuntu.img --vhd
$ msl --import-in-place Ubuntu-3 ~/images/ubuntu-3.img
```

- `--export --vhd` stops the distribution and copies its disk, an instant clone on APFS. A distribution still on `data.img` has no disk of its own to export; `--move` it first.
- `--import --vhd` copies a disk image to `ext4.img` in the install location.
- `--import-in-place` uses the image where it is.

MSL's images are raw ext4, not VHDX, and the file system's root is the distribution's root, as in WSL's `ext4.vhdx`. Convert between the two with `qemu-img`:

```console
$ qemu-img convert -O raw ext4.vhdx ext4.img      # a WSL disk, for MSL
$ qemu-img convert -O vhdx ext4.img ext4.vhdx     # an MSL disk, for WSL
```

## Remove a distribution

`msl --unregister <Distro>` deletes the distribution and its `ext4.img`, as WSL deletes `ext4.vhdx`. That includes an image imported with `--import-in-place`. For a distribution still on `data.img`, the space it used becomes free inside `data.img`, and goes back to macOS at the next shutdown or `--compact`.

## Durability

MSL serves the disks to the VM itself, and Virtualization.framework never tells it when a distribution calls `fsync`. So MSL writes the way `qemu-nbd` does by default: a write is done once it's in macOS's file cache, and each disk is flushed to the SSD when it's detached, including at shutdown.

- If MSL or the VM crashes, what the distribution had written to its disk is kept: macOS still writes out its cache. As after any Linux crash, writes still in the distribution's own memory are lost; `sync` or `fsync` guards against that.
- If macOS crashes or the Mac loses power, the last writes can be lost and a distribution's file system can be damaged. MSL checks and repairs it (`e2fsck`) the next time it attaches the disk.

{{< callout type="warning" >}}
`fsync` inside a distribution doesn't guarantee the data is on the SSD, so a database's commit isn't safe from a power loss until the disk is flushed. `msl --shutdown` flushes every disk; run it before relying on data surviving a power loss.
{{< /callout >}}
