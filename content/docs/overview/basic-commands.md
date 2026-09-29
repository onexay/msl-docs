---
title: Basic commands for MSL
weight: 3
description: Reference for the msl command, which takes the same arguments as wsl.exe.
---

`msl` takes `wsl.exe`'s arguments and prints the same messages, so commands from WSL instructions work with `msl` in place of `wsl`. Run these in a macOS terminal. For the full list of options, run `msl --help`.

## Install

```console
$ msl --install <Distribution Name>
```

Installs a Linux distribution and runs its first-run setup, which asks you to create a Linux user. Without a name, it installs the distribution marked as the default in `msl --list --online`. See [Install MSL]({{< relref "/docs/install/install" >}}).

Options:

- `--name`: the name to give the distribution.
- `--location`: the folder for its disk, `ext4.img`.
- `--no-launch`, `-n`: install it without running its first-run setup.
- `--from-file <Path>`: install from a local `.wsl` image.
- `--vhd-size <Size>`: the maximum size of its disk, for example `64GB`.

`--web-download` and `--fixed-vhd` are accepted and ignored; disks are always sparse.

## List available Linux distributions

```console
$ msl --list --online
```

Lists the distributions you can install: the arm64 images in Microsoft's WSL distribution list. Also `msl -l -o`.

## List installed Linux distributions

```console
$ msl --list --verbose
```

Lists your distributions, whether each is running or stopped, and its version, which is always 2. Also `msl -l -v`. `--all` includes distributions being installed or removed, `--running` lists only running ones, and `--quiet` (`-q`) prints only the names.

## Set the version to 1 or 2

```console
$ msl --set-version <Distribution Name> 2
```

Accepted for compatibility. Every MSL distribution is version 2; version 1 isn't available on macOS.

## Set the default version

```console
$ msl --set-default-version 2
```

Accepted for compatibility. Only version 2 is available.

## Set the default Linux distribution

```console
$ msl --set-default <Distribution Name>
```

Sets the distribution that `msl` runs when you don't name one. Also `msl -s <Distribution Name>`.

## Start in your home directory

```console
$ msl ~
```

Starts a shell in your Linux home directory. Without `~`, `msl` starts in the macOS directory you ran it from, under `/mnt/macos`. `--cd <Directory>` starts in any Linux directory.

## Run a specific Linux distribution

```console
$ msl --distribution <Distribution Name> --user <User Name>
```

Runs a distribution as a given user. Also `msl -d <Distribution Name> -u <User Name>`. The user must exist in the distribution.

## Run a command

```console
$ msl ls -la                  # through the distribution's shell: globs, variables and pipes work
$ msl -e uname -m             # without a shell; the exit code is passed through
$ msl --cd ~ -- make test     # everything after -- is passed as it is
$ git log | msl -e wc -l      # stdin and stdout are pipes in both directions
```

An interactive command gets a terminal, as in WSL, and window resizes and Ctrl-C reach the Linux process. `--shell-type <standard|login|none>` chooses how the shell runs the command.

## Update MSL

```console
$ msl --update
```

Installs the latest MSL release in place and keeps your distributions and settings. `--pre-release` installs a pre-release if there is one. See [Update and uninstall MSL]({{< relref "/docs/install/upgrade" >}}).

## Check the status

```console
$ msl --status
```

Shows the default distribution and the VM's settings: memory, processors, kernel, networking, nested virtualization, idle timeouts, the distributions' disks and their use on macOS, and whether the VM is running. It also lists `~/.mslconfig` changes that apply after the next `msl --shutdown`.

## Check the version

```console
$ msl --version
```

Shows the MSL, kernel and macOS versions. Also `msl -v`.

## Help

```console
$ msl --help
```

Lists every command and option.

## Run as a specific user

```console
$ msl --user <User Name>
```

Runs the default distribution as another user, for example `msl -u root`. The user must exist in the distribution.

## Change the default user for a distribution

```console
$ msl --manage <Distribution Name> --set-default-user <User Name>
```

Sets the user that shells run as. The user must exist in the distribution. `[user] default` in the distribution's `/etc/wsl.conf` does the same; see [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

## Shut down

```console
$ msl --shutdown
```

Stops every running distribution and the VM, and flushes every distribution's disk to the SSD. Use it to apply changes to `~/.mslconfig`. `--force` stops the VM even if an operation is in progress, which can lose data.

## Terminate

```console
$ msl --terminate <Distribution Name>
```

Stops one distribution. Also `msl -t <Distribution Name>`.

## Identify IP addresses

All distributions share one network, so they have the same IP address. From inside a distribution:

- `hostname -I` prints the VM's IP address.
- `host.internal`, which MSL adds to each distribution's `/etc/hosts`, is the address of the Mac as seen from Linux.

You rarely need either: a server in a distribution is reachable at `localhost` on macOS. See [Networking]({{< relref "/docs/concepts/networking" >}}).

## Export a distribution

```console
$ msl --export <Distribution Name> <FileName>
```

Writes the distribution to a tar file, the format `wsl --import` takes. Use `-` as the file name for stdout. `--format tar.gz` or `--format tar.xz` compresses it. `--vhd` copies the distribution's disk instead, as a raw ext4 image; it stops the distribution first.

## Import a distribution

```console
$ msl --import <Distribution Name> <InstallLocation> <FileName>
```

Imports a tar file as a new distribution, with its disk in `<InstallLocation>`. Use `-` as the file name for stdin. `--vhd` imports a raw ext4 disk image instead, copied to `<InstallLocation>/ext4.img`. See [Import any Linux distribution]({{< relref "/docs/how-to/use-custom-distro" >}}).

## Import a distribution in place

```console
$ msl --import-in-place <Distribution Name> <FileName>
```

Registers a raw ext4 disk image as a new distribution, using the file where it is. `msl --unregister` deletes it.

## Unregister or uninstall a Linux distribution

```console
$ msl --unregister <Distribution Name>
```

Removes the distribution and deletes its files, including its disk, `ext4.img`, as WSL deletes `ext4.vhdx`.

{{< callout type="warning" >}}
Everything in the distribution is deleted permanently, including your files in its home directories. Export it first if you might need it again.
{{< /callout >}}

## Move, grow or compact a distribution's disk

```console
$ msl --manage <Distribution Name> --move <Location>
$ msl --manage <Distribution Name> --resize 512GB
$ msl --manage <Distribution Name> --compact
```

`--move` stops the distribution and moves its disk to another folder. `--resize` grows the disk of a stopped distribution; it can't shrink. `--compact` returns space freed inside the disk to macOS. See [Manage disk space]({{< relref "/docs/how-to/disk-space" >}}).

## Mount a disk

```console
$ msl --mount <Disk>
```

Attaches a disk image to the VM and mounts it at `/mnt/msl/<Name>` in every distribution. `--name`, `--type` (`-t`), `--options` (`-o`), `--partition` and `--bare` work as in WSL, and `--vhd` is accepted. See [Mount a disk]({{< relref "/docs/how-to/mount-disk" >}}).

## Unmount disks

```console
$ msl --unmount <Disk>
```

Unmounts and detaches a disk. Without a disk, it detaches all of them.

## Commands only in MSL

### JSON output

```console
$ msl --list --verbose --json
```

`--json` prints JSON instead of text for `--list`, `--list --online`, `--status` and `--version`. See [Use JSON output in scripts]({{< relref "/docs/how-to/json-output" >}}).

### Set up VS Code

```console
$ msl --manage-ide
```

Sets up the MSL extension in VS Code, VS Code Insiders, VSCodium or Cursor. `--ide <vscode|vscode-insiders|vscode-oss|cursor|all>` picks the IDE, and `--install` or `--uninstall` says what to do. See [Get started with VS Code]({{< relref "/docs/tutorials/msl-vscode" >}}).

### Debug shell

```console
$ msl --debug-shell
```

Opens a root shell in the utility VM itself, outside every distribution, for diagnosing problems.

### Uninstall MSL

```console
$ msl --uninstall
```

Removes MSL and its VS Code setup, and keeps your distributions and settings.

## Not available on macOS

These `wsl.exe` options have no macOS equivalent: `--system`, `--enable-wsl1`, `--inbox`, and WSL 1. `--set-sparse` is accepted, and disks are always sparse.
