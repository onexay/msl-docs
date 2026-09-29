---
title: Get started with Linux and Bash
weight: 9
description: A short introduction to the Linux command line in an MSL distribution, for people new to Linux.
---

If you're new to Linux, this page covers the basics of working in a distribution's shell. Most distributions use Bash as the default shell, and macOS's Terminal works much the same way, so a lot of it will be familiar.

## Open a shell

From a macOS terminal:

```console
$ msl                    # the default distribution, in the macOS directory you're in
$ msl ~                  # starting in your Linux home directory
$ msl -d Debian          # another distribution
```

Type `exit`, or press Ctrl-D, to leave. To run a single command without opening a shell, put it after `msl`: `msl ls -la`.

## Find your way around

```console
$ pwd                    # the directory you're in
$ ls -la                 # its contents, including hidden files
$ cd ~/src               # go to a directory; ~ is your home directory
$ cd ..                  # up one level
$ cd /mnt/macos/Users    # macOS files
```

Linux file names are case-sensitive: `Notes.txt` and `notes.txt` are different files.

## Work with files

```console
$ mkdir project          # create a directory
$ touch notes.txt        # create an empty file
$ cp notes.txt copy.txt  # copy
$ mv copy.txt old.txt    # move or rename
$ rm old.txt             # delete; there's no trash
$ cat notes.txt          # print a file
$ less notes.txt         # page through a file; q to quit
$ nano notes.txt         # edit a file in the terminal
```

## Install software

Each distribution has a package manager. Ubuntu and Debian use `apt`:

```console
$ sudo apt update                  # refresh the package lists
$ sudo apt install htop            # install a package
$ sudo apt upgrade                 # upgrade everything installed
```

Fedora uses `dnf`, and openSUSE uses `zypper`.

## Run commands as root

`sudo` runs a command with administrator rights. It asks for your Linux password, the one you set when you installed the distribution. From macOS, `msl -u root` opens a shell as root, which also works if you've forgotten your password (see [Set up an MSL development environment]({{< relref "/docs/tutorials/environment#set-up-your-linux-username-and-password" >}})).

## Combine commands

A pipe (`|`) sends one command's output to the next, and `>` writes it to a file:

```console
$ ls -la | grep txt              # only lines containing "txt"
$ history | tail -20             # your last 20 commands
$ ps aux > processes.txt         # save the output to a file
```

Pipes also work between macOS and Linux:

```console
$ git log | msl -e wc -l         # on macOS: a macOS command into a Linux one
```

## Get help

`man <command>` shows a command's manual (press q to quit), and most commands print a summary with `--help`.

## Next

- [Basic MSL commands]({{< relref "/docs/overview/basic-commands" >}}): managing distributions from macOS
- [Set up an MSL development environment]({{< relref "/docs/tutorials/environment" >}})
