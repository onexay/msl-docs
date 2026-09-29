---
title: Import any Linux distribution
weight: 1
description: Import an arm64 Linux root filesystem or disk image as an MSL distribution with msl --import, and back up or move distributions with --export.
---

`msl --install` covers the distributions in Microsoft's WSL list. To use anything else, import its root filesystem from a tar file with `msl --import`, the same command WSL uses.

## Get a root filesystem tar file

MSL runs arm64 Linux only, so the root filesystem must be built for arm64 (aarch64). x86_64 distributions aren't supported yet.

Two common sources:

- **A distribution's own rootfs tarball.** Many distributions publish an arm64 root filesystem as a `.tar`, `.tar.gz`, `.tar.xz` or `.tar.zst` file. Download it on macOS.
- **A container image.** On a machine with Docker or Podman, create a container from an arm64 image and export its filesystem:

    ```console
    $ docker create --platform linux/arm64 --name rootfs debian:trixie
    $ docker export rootfs > debian.tar
    $ docker rm rootfs
    ```

    Container images are minimal. They usually have no `init` system, no `sudo` and no user account besides root.

## Import it

```console
$ msl --import MyDistro ~/msl/MyDistro debian.tar
$ msl -d MyDistro
```

| Argument | Meaning |
|---|---|
| `<Distro>` | The name of the new distribution. It must be unique. |
| `<InstallLocation>` | The folder for the distribution's disk, `ext4.img`. See [Manage disk space]({{< relref "/docs/how-to/disk-space" >}}). |
| `<FileName>` | The tar file, plain or compressed with gzip, xz or zstd; MSL detects which. Use `-` to read it from standard input. |

`--version 2` is accepted. With `--vhd`, `<FileName>` is a raw ext4 disk image instead of a tar file; see [Export and import disk images]({{< relref "/docs/how-to/disk-space#export-and-import-disk-images" >}}).

You can pipe an export straight into an import, for example to clone a distribution:

```console
$ msl --export Ubuntu - | msl --import Ubuntu-copy ~/msl/Ubuntu-copy -
```

If the tar file contains `/etc/wsl-distribution.conf` with a first-run command, MSL runs it the first time you open an interactive shell, as it does for installed distributions. See [Build a custom distribution]({{< relref "/docs/how-to/build-custom-distro" >}}).

## Set up a user

An imported distribution starts as root, unless its first-run setup creates a user. To work as a regular user, create one inside the distribution and make it the default:

```console
$ msl -d MyDistro -u root
# useradd -m -s /bin/bash -G sudo me     # the admin group is "wheel" on Fedora-like distributions
# passwd me
# exit
$ msl --manage MyDistro --set-default-user me
```

The user must already exist; otherwise `--set-default-user` fails with "User not found."

Instead of `--set-default-user`, you can set the user in the distribution's `/etc/wsl.conf` (or `/etc/msl.conf`):

```ini
[user]
default=me
```

MSL picks the user in this order: `-u` on the command line, then `[user] default` in `/etc/wsl.conf`, then the user set with `--set-default-user`, then root. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

## Install a `.wsl` file

A `.wsl` file is a distribution image in WSL's format, the same kind `msl --install` downloads. Install one from disk with `--from-file`:

```console
$ msl --install --from-file ~/Downloads/mydistro.wsl --name MyDistro
```

This runs the image's first-run setup, like an online install. `--name` is optional when the image declares a default name.

## Back up and move distributions

`msl --export` writes a distribution to a tar file, which `msl --import` (or `wsl --import` on Windows) can read back:

```console
$ msl --terminate Ubuntu                          # stop it first, so files aren't changing
$ msl --export Ubuntu ~/Backups/ubuntu.tar.xz --format tar.xz
```

`--format` is `tar` (the default), `tar.gz` or `tar.xz`. Use `-` as the file name to write to standard output.

`--export --vhd` copies the distribution's whole disk instead, as a raw ext4 image that `--import --vhd` or `--import-in-place` registers again. See [Export and import disk images]({{< relref "/docs/how-to/disk-space#export-and-import-disk-images" >}}).

To move a distribution to another Mac, export it, copy the file, and import it there under the same name. To move it to another folder or drive on the same Mac, use `msl --manage <Distro> --move <folder>`; see [Move a distribution]({{< relref "/docs/how-to/disk-space#move-a-distribution" >}}).
