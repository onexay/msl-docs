---
title: File access and permissions
weight: 3
description: How Linux permissions and ownership work on macOS files under /mnt/macos, and on distribution files seen from macOS in ~/.msl/distros.
---

A file can be reached from both sides with MSL: macOS files from Linux under `/mnt/macos`, and Linux files from macOS under `~/.msl/distros`. This page explains who owns those files and who is allowed to read and change them in each direction.

## Linux files in a distribution

Files in a distribution's own file system, such as `/home` or `/etc`, behave as on any Linux system. Their owners, groups and modes are stored in the distribution, and `chmod`, `chown`, `sudo` and file capabilities work as usual.

## macOS files in Linux: /mnt/macos

`/mnt/macos` is your Mac's file system, shared into the VM with virtiofs. Two rules decide what Linux can do there:

- **Every file appears to belong to whoever looks at it.** When your Linux user lists a macOS folder, the files show that user as their owner; when root lists it, they show root. Because of this, any Linux user can work in your macOS folders, and tools that check ownership, such as git's `safe.directory` check, are satisfied.
- **macOS checks every access as your macOS user.** MSL runs as your macOS account, so a Linux program can read and change exactly the files you can, and no more. `sudo` in Linux doesn't give access to files your macOS account can't open.

WSL's DrvFs options for Windows drives (`metadata`, `uid`, `gid`, `umask`, `fmask`, `dmask`) don't exist in MSL. There's no setting to store Linux permissions on macOS files.

## Linux files in macOS: ~/.msl/distros

While the VM runs, each distribution's files are at `~/.msl/distros/<distro>` and in Finder under **Locations**. They're network (NFS) mounts that MSL creates at VM start and removes when the VM stops.

- **Only your macOS user can use them.** MSL serves the files on a Unix socket that only your account can open, and checks every request, so other accounts on the same Mac can't read your distributions. If you set `fileViewTransport = tcp` in `~/.mslconfig`, the files are served on a `127.0.0.1` port instead, which other users on the Mac can reach. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config#main-settings" >}}).
- **New files take the owner of their folder.** A file you create from macOS in `/home/me/project` belongs to the owner of `project`, typically your Linux user; one created in `/etc` belongs to root.
- **Finder's own files stay out of Linux.** `.DS_Store` files, and the `._` files macOS uses to store extended attributes (tags, quarantine flags, resource forks) on network volumes, are kept in the VM's memory. Linux never sees them, and they're gone when the VM stops. Copying a file with extended attributes from Finder works, but the attributes aren't kept.

## Files on mounted disks

A disk image attached with `msl --mount` is mounted at `/mnt/msl/<name>` in every distribution. Its files have the owners and permissions stored on that disk, as on any Linux system. See [Mount a disk]({{< relref "/docs/how-to/mount-disk" >}}).
