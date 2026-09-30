---
title: Manage disk space
weight: 6
description: How MSL stores each distribution on its own sparse disk, and how to check, grow, compact, move, export and import disks.
---

As in WSL, each distribution has its own virtual disk: a sparse ext4 image named `ext4.img` in the distribution's install location. By default that's `~/Library/Application Support/msl/distros/<id>/ext4.img`. `msl --install --location <folder>` and `msl --import <Distro> <folder> <file>` put it in `<folder>`.

`ext4.img` is a sparse file: macOS stores only the blocks that hold data. A disk with a 256 GB maximum takes a few hundred megabytes on the Mac until the distribution fills it.

Distributions installed by MSL 0.1.11 or earlier stay on the old shared disk, `~/Library/Application Support/msl/data.img`, where each distribution is a directory. Give one its own disk with `--move`; see [Move a distribution](#move-a-distribution).

## How disks are attached

When the VM starts, MSL attaches every distribution's disk to it, up to 19 disks, starting with the default distribution. Virtualization.framework serves these disks itself, as fast as the VM's own disk.

Virtualization.framework can't add a disk to a running VM. So when a disk appears while the VM is running (you install or import a distribution, move one to another volume, or resize one):

- If no distribution is running, MSL restarts the VM so the new disk is attached at start. This takes a second or two.
- If a distribution is running, MSL mounts the new disk through the Mac file share instead, until the VM next restarts. This works, but disk access is slower (random reads and writes especially), and `fsync` doesn't reach the SSD right away; see [Durability](#durability).

The VM stops a minute after the last distribution does (`vmIdleTimeout`), or with `msl --shutdown`; when it next starts, every disk is attached at start. To see how a distribution's disk is attached, run `df /` in it: `/dev/vd…` is a disk attached at start, and `/dev/loop…` is one mounted through the file share.

Only distributions whose disk is attached or mounted appear in `~/.msl/distros`. With more than 19 distributions, the others appear once you use them.

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

The minimum is 4 GB.

## Grow a disk

Stop the distribution, then resize its disk:

```console
$ msl --terminate Ubuntu
$ msl --manage Ubuntu --resize 512GB
```

MSL enlarges the file, and the VM checks and grows the file system before mounting it again, which takes a few seconds. Other distributions keep running. If any are running, the resized disk is mounted through the Mac file share until the VM next restarts; see [How disks are attached](#how-disks-are-attached).

The disk can't shrink, and it can't grow beyond the size of the Mac's disk.

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

This stops the distribution and moves its `ext4.img` into the new folder: a rename on the same volume, a copy to another one. A distribution still on `data.img` gets a disk of its own in that folder: MSL copies its files over and then deletes them from `data.img`. After a move to another volume, the disk is a new one to the VM; see [How disks are attached](#how-disks-are-attached).

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

A disk attached when the VM starts behaves like a disk on Linux: when a distribution calls `fsync`, Virtualization.framework flushes the data to the Mac's SSD (`F_FULLFSYNC`) before `fsync` returns. When you log out, restart or shut down the Mac, MSL stops the distributions and unmounts their disks first, as `msl --shutdown` does.

- If MSL or the VM crashes, what the distribution had written to its disk is kept. As after any Linux crash, writes still in the distribution's own memory are lost; `sync` or `fsync` guards against that.
- If macOS crashes or the Mac loses power, what was synced is kept. Writes that weren't synced can be lost, and MSL checks and repairs the file system (`e2fsck`) the next time it mounts the disk.

A disk mounted through the Mac file share (added while another distribution was running; `df /` shows `/dev/loop…`) is the exception. There, `fsync` reaches macOS's file cache but not the SSD. MSL flushes the disk to the SSD when it's unmounted and when the VM stops, and from the next VM start the disk is attached normally.

{{< callout type="warning" >}}
Until then, a macOS crash or power loss can lose recent writes on a disk mounted through the file share, even ones a database committed with `fsync`. `msl --shutdown` flushes it and ends that state; run it before relying on that data.
{{< /callout >}}
