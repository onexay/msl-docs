---
title: Set up an MSL development environment
weight: 1
description: Best practices for setting up a development environment in an MSL distribution, from your Linux user account to your editor, Git and databases.
---

This guide walks through setting up a Linux development environment with MSL: installing a distribution, creating your Linux user, keeping packages up to date, and connecting an editor, Git and the other tools you work with.

## Get started

Install MSL from a macOS terminal:

```console
$ curl -fsSL https://raw.githubusercontent.com/onexay/msl/main/install.sh | sh
```

The installer asks before each step. It can also install a first distribution, and it suggests Ubuntu. To install one yourself:

```console
$ msl --list --online      # distributions you can install
$ msl --install Ubuntu
```

MSL needs Apple silicon and macOS 27 or later. [Install MSL]({{< relref "/docs/install/install" >}}) covers the installer's options, and [Troubleshooting]({{< relref "/docs/troubleshooting" >}}) helps if something goes wrong.

## Set up your Linux username and password

The first time a distribution starts, its own setup asks you to create a Linux user name and password.

- The account belongs to that distribution only. It has nothing to do with your macOS account, and each distribution you install asks again.
- Nothing appears on screen while you type the password. That's normal.
- The account becomes the distribution's default user, so `msl` opens a shell as that user.
- It can run administrative commands with `sudo`.

Some distributions' setup scripts mention Windows ("Provisioning the new WSL instance"). That's their stock text, and MSL skips the steps that need Windows.

To change your password, run `passwd` in the distribution.

If you've forgotten it:

1. Open a root shell in the distribution from macOS:

    ```console
    $ msl -u root                  # the default distribution
    $ msl -d Debian -u root        # another one
    ```

2. Set a new password for your user:

    ```console
    # passwd <username>
    ```

3. Type `exit` to leave the root shell.

## Update and upgrade packages

MSL doesn't update your distributions' packages. Do it regularly with the distribution's package manager. On Ubuntu or Debian:

```console
$ sudo apt update && sudo apt upgrade
```

## Add additional distributions

Install more distributions from the same list, or import your own:

```console
$ msl --install Debian
$ msl -l -v                    # what's installed, and what's running
$ msl -s Debian                # make Debian the default
```

See [Import any Linux distribution]({{< relref "/docs/how-to/use-custom-distro" >}}) and [Build a custom distribution]({{< relref "/docs/how-to/build-custom-distro" >}}).

## Set up your terminal

MSL works in any macOS terminal, such as Terminal or iTerm2. Run `msl` to open a shell in the default distribution, starting in the macOS directory you ran it from. `msl ~` starts in your Linux home directory instead, and `msl -d <Distro>` opens another distribution.

Interactive programs work as they do in any Linux terminal: window resizes and Ctrl-C reach the Linux process.

## File storage

Keep your projects in the distribution's own file system, for example `~/src/project` in your Linux home directory. Linux tools are fastest there, and file names are case-sensitive, as Linux tools expect.

Your macOS files are available in Linux under `/mnt/macos`, so `/Users/me/src` is `/mnt/macos/Users/me/src`. That's the way to move files across, but it's slower and usually case-insensitive. See [Working across file systems]({{< relref "/docs/concepts/filesystems" >}}).

To open your Linux files on macOS, use `~/.msl/distros/<distro>` or the distribution's entry under Locations in Finder. `mslpath -w` gives the macOS path of a Linux file or directory:

```console
$ mslpath -w ~/src/project     # in the distribution
```

These folders exist only while the MSL VM is running.

## Set up your code editor

Use VS Code, or VS Code Insiders, VSCodium or Cursor, with the MSL extension. The editor window stays on macOS, while the terminal, language servers, debuggers and extensions run in the distribution. Follow [Get started using VS Code with MSL]({{< relref "/docs/tutorials/msl-vscode" >}}).

## Set up version control with Git

Install Git in the distribution and set up authentication there. See [Get started using Git on MSL]({{< relref "/docs/tutorials/msl-git" >}}).

## Set up a database

Run databases in the distribution and connect to them from macOS over `localhost`. See [Get started with databases on MSL]({{< relref "/docs/tutorials/msl-database" >}}).

## Set up Linux containers

See [Get started with Linux containers on MSL]({{< relref "/docs/tutorials/msl-containers" >}}).

## Basic MSL commands

You manage distributions from a macOS terminal with `msl`, which takes the same arguments as WSL's `wsl.exe`. A command after the options runs in Linux, and pipes work in both directions:

```console
$ msl uname -a                 # run a Linux command from macOS
$ git log | msl -e wc -l       # pipe macOS output into a Linux program
```

[Basic MSL commands]({{< relref "/docs/overview/basic-commands" >}}) lists the rest.

## Mount a disk

`msl --mount <image>` attaches a disk image and mounts it in every distribution. See [Mount a disk in MSL]({{< relref "/docs/how-to/mount-disk" >}}).
