---
title: Adjust case sensitivity
weight: 5
description: How file name case works in MSL distributions and in macOS files under /mnt/macos, and how to get case-sensitive storage for a project.
---

Case sensitivity decides whether `README.md` and `readme.md` are two files or one. Linux file systems are case-sensitive. macOS volumes are usually case-insensitive: APFS, the default, keeps the case you type but treats names that differ only in case as the same file.

## Where each rule applies

| Location | Case-sensitive? |
|---|---|
| A distribution's own files (`/home`, `/usr`, …) | Yes, as on any Linux system. |
| macOS files under `/mnt/macos` | Whatever the macOS volume is. On a default Mac, no. |
| Disks attached with `msl --mount` | Whatever the disk's file system is. ext4 and XFS are case-sensitive. |

So, on a default Mac, this happens under `/mnt/macos` but not in your Linux home directory:

```console
$ cd /mnt/macos/Users/me/tmp          # inside a distribution
$ touch Makefile makefile
$ ls
Makefile
```

Problems this can cause under `/mnt/macos`: a Git repository with two files whose names differ only in case checks out as one file, and a build that writes `foo.o` and `Foo.o` overwrites one with the other.

## Changing it

WSL can turn case sensitivity on for a single Windows directory. MSL has no equivalent: the macOS volume's setting applies to everything on it, and MSL can't change it per directory.

What you can do:

- **Keep the project in the distribution.** Clone and build in your Linux home directory. It's case-sensitive, and faster than `/mnt/macos`. You can still open the files from macOS in Finder or VS Code. See [Working across file systems]({{< relref "/docs/concepts/filesystems" >}}).
- **Use a Linux disk image.** An ext4 image attached with `msl --mount` is case-sensitive and shared by every distribution, which suits large projects or data you want outside a single distribution. macOS can't open ext4 itself. See [Mount a disk in MSL]({{< relref "/docs/how-to/mount-disk" >}}).
