---
title: Working across file systems
weight: 1
description: Where to keep files, how macOS and Linux see each other's files, and how to mix macOS and Linux commands with MSL.
---

MSL gives Linux and macOS access to each other's files: macOS files appear in every distribution under `/mnt/macos`, and each distribution's files appear on macOS under `~/.msl/distros`. This page covers where to keep your files, how to run Linux commands from macOS, and how to pass paths and environment variables between the two.

## File storage and performance across file systems

Keep a project on the side whose tools work on it. If you build and test with Linux tools, keep the project in the distribution, for example in `/home/<user>/project`. Keep it on macOS only if you mostly work on it with macOS tools.

- Use the Linux file system: `/home/<user>/project`
- Not the macOS file system: `/mnt/macos/Users/<user>/project`

Linux can work on files under `/mnt/macos`, but they're slower than the distribution's own disk, and the macOS side is usually case-insensitive. Use `/mnt/macos` to move files across, and build in the Linux home directory when speed or case sensitivity matters.

A path that starts with `/mnt/macos` is a macOS path seen from Linux: `/mnt/macos/Users/me/src` is `/Users/me/src` on macOS, the way `/mnt/c/Users/me/src` is `C:\Users\me\src` in WSL. `[automount] root` in `/etc/wsl.conf` changes the parent directory; with `root = /`, macOS is at `/macos`. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config#automount-settings" >}}).

## View your current directory in Finder

While the VM is running, each distribution's files are in `~/.msl/distros/<distro>` on macOS, and in Finder under **Locations**, with the distribution's logo.

MSL never runs macOS programs from Linux, so there's no equivalent of `explorer.exe .`. Instead, get the macOS path of a Linux directory with `mslpath` and open it from a macOS terminal:

```console
$ mslpath -a -w .                              # in the distribution
/Users/me/.msl/distros/Ubuntu/home/me/project
$ open /Users/me/.msl/distros/Ubuntu/home/me/project    # on macOS
```

Or in one step from macOS, for your Linux home directory:

```console
$ open "$(msl --cd ~ -e mslpath -a -w .)"
```

`~/.msl/distros` is there only while the VM runs. If it's empty, start any distribution to bring it back.

## Filename and directory case sensitivity

Linux file systems are case-sensitive: `FOO.txt` and `foo.txt` are two files. The macOS file system is usually case-insensitive, so under `/mnt/macos` they're the same file. See [Adjust case sensitivity]({{< relref "/docs/how-to/case-sensitivity" >}}).

## Run Linux tools from a macOS terminal

Run any Linux command from macOS with `msl <command>`:

```console
$ cd ~/src/app
$ msl ls -la
```

A command run this way:

- starts in the macOS directory you ran it from, under `/mnt/macos`;
- runs as the distribution's default user, in the default distribution (`-d` and `-u` pick others);
- goes through the Linux shell, so globs, variables, `sudo`, pipes and redirection inside the command line are handled by Linux.

`msl -e <command>` runs the program directly, without a shell, and passes its exit code back.

```console
$ msl sudo apt update
$ msl -e uname -m
aarch64
```

## Mix macOS and Linux commands

Standard input and output are pipes in both directions, so macOS and Linux commands combine in one pipeline. The shell you typed the pipeline into decides where each part runs.

```console
$ msl ls -la | grep git                  # Linux ls, macOS grep
$ ls -la | msl grep git                  # macOS ls, Linux grep
$ git log --oneline | msl -e wc -l       # macOS git, Linux wc
$ msl ls -la > listing.txt               # the file is written on macOS
```

The command line after `msl` is passed to Linux as it is, so paths in it must be Linux paths:

```console
$ msl -e ls -la /proc/cpuinfo
$ msl ls -la "/mnt/macos/Users/me/My Documents"
```

## No macOS tools from Linux

WSL can run Windows programs from Linux (`notepad.exe`) and adds Windows directories to Linux's `PATH`. MSL does neither, by design: nothing from macOS runs inside a distribution, and no macOS path is added to `PATH`.

That keeps a distribution a plain Linux system. Build tools such as `npm`, `node-gyp` and `configure` find only Linux compilers and libraries, so what you build is always a Linux build, even in a folder under `/mnt/macos`. It also means a Linux program can't start macOS programs on your behalf.

To combine the two, run the macOS side from a macOS terminal and call Linux with `msl`, as in the examples above. `[interop]` settings in `/etc/wsl.conf` are accepted and ignored.

## Share environment variables with MSLENV

`MSLENV` passes macOS environment variables into Linux, like `WSLENV` does from Windows. Set it on macOS to a colon-separated list of variable names, each with optional flags:

| Flag | Meaning |
|---|---|
| none | Pass the value as it is. |
| `/p` | The value is a macOS path: translate it to a Linux path. |
| `/l` | The value is a colon-separated list of macOS paths: translate each one. |
| `/u` | Only when going from macOS to Linux. Always the case in MSL, so it changes nothing. |
| `/w` | Only when going from Linux to macOS. MSL doesn't pass variables that way, so a variable with only `/w` isn't passed. |

```console
$ export PROJECT=/Users/me/src/app
$ MSLENV=PROJECT/p msl -e printenv PROJECT
/mnt/macos/Users/me/src/app
```

`MSLENV` works in one direction only, from macOS into Linux. Inside the distribution, `MSLENV` holds the list it was given.

## Convert paths with mslpath

`mslpath` converts paths between macOS and Linux, like `wslpath`. It's in every distribution as `/usr/bin/mslpath`.

| Option | Converts |
|---|---|
| `-u` (default) | A macOS path to a Linux path. |
| `-w` or `-m` | A Linux path to a macOS path. |
| `-a` | Makes the result absolute, resolving `.` and `..`. |

```console
$ mslpath -u /Users/me/src               # /mnt/macos/Users/me/src
$ mslpath -w /mnt/macos/Users/me/src     # /Users/me/src
$ mslpath -w /etc/hosts                  # /Users/me/.msl/distros/Ubuntu/etc/hosts
$ mslpath -a -u /Users/y/../x            # /mnt/macos/Users/x
```

A Linux path outside `/mnt/macos` converts to its place under `~/.msl/distros/<distro>`, so you can open it in Finder. Relative paths are left as they are unless you add `-a`.
