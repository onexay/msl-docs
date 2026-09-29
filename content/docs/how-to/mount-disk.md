---
title: Mount a disk in MSL
weight: 3
description: Attach a Linux disk image to MSL's VM with msl --mount, and reach it from every distribution under /mnt/msl.
---

`msl --mount` attaches a disk image to MSL's VM and mounts it in every distribution, like `wsl --mount`. Use it for a filesystem macOS can't read, such as an ext4 or XFS image.

## Mount a disk image

```console
$ msl --mount ~/disks/data.img
The disk was successfully mounted as '/mnt/msl/data'.
To unmount and detach the disk, run 'msl --unmount ~/disks/data.img'.
```

The disk is mounted at `/mnt/msl/<name>` in every distribution. The name defaults to the file name without its extension.

The file must be a raw disk image, such as one made with `truncate` and `mkfs`. MSL doesn't read VHD or VHDX files; `--vhd` is accepted for compatibility and changes nothing. To make a new ext4 image from a distribution:

```console
$ truncate -s 8G /mnt/macos/Users/me/disks/data.img     # inside a distribution
$ mkfs.ext4 /mnt/macos/Users/me/disks/data.img
```

## Options

| Option | Effect |
|---|---|
| `--name <Name>` | Mount at `/mnt/msl/<Name>` instead. |
| `--type <Filesystem>`, `-t` | The filesystem type. Default `ext4`. |
| `--options <Options>`, `-o` | Mount options passed to the filesystem, for example `-o "data=ordered"`. |
| `--partition <Index>` | Mount one partition instead of the whole disk. Without `--name`, the mount point gets a `p<Index>` suffix, such as `/mnt/msl/datap1`. |
| `--bare` | Attach the disk without mounting it. MSL prints the Linux device name (for example `/dev/sda`), so you can partition, format or mount it yourself from a distribution as root. |

MSL's kernel can mount ext4 and XFS. FAT, exFAT, Btrfs, NTFS, HFS+ and ISO 9660 aren't built in, and the kernel doesn't load modules. Use disks in those formats from macOS, and copy files across through `/mnt/macos`.

If the disk attaches but won't mount (a wrong `--type`, for example), it stays attached, as in WSL. Check the kernel's messages with `dmesg` in `msl --debug-shell`, then detach it with `msl --unmount`.

## Unmount

```console
$ msl --unmount ~/disks/data.img     # one disk
$ msl --unmount                      # every attached disk
```

Unmount before you copy, move or open the image file on macOS. Disks are also detached when the VM stops, for example after `msl --shutdown` or when it idles out, so mount them again after a restart.

{{< callout type="warning" >}}
The image is attached to the VM as a USB disk, and Linux doesn't flush writes to it the way it flushes a normal disk. A write that Linux reports as saved can be lost if macOS crashes or loses power ([#43](https://github.com/onexay/msl/issues/43)). Keep a copy of anything on it that you can't recreate.
{{< /callout >}}

## Physical disks

MSL also accepts a macOS disk device such as `/dev/disk4`. `msld` runs as your user, though, and macOS lets only administrators open raw disks, so this normally fails with "Administrator access is needed to mount a disk." Mounting physical disks and USB drives isn't supported yet; copy the data into an image file, or use the drive from macOS and copy files across through `/mnt/macos`. See [Connect USB devices]({{< relref "/docs/how-to/connect-usb" >}}).
