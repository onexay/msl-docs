---
title: Install MSL
weight: 1
description: Install MSL and a first Linux distribution with one command.
---

You can install MSL and a Linux distribution with one command, then open a shell in it.

## Prerequisites

- A Mac with Apple silicon.
- macOS 26 or later.

MSL doesn't need administrator rights, unless you install it into a system directory such as `/usr/local`.

## Install the MSL command

Open Terminal and run:

```console
$ curl -fsSL https://raw.githubusercontent.com/onexay/msl/main/install.sh | sh
```

The installer asks before each step:

1. **Where to install.** The default, `~/.local`, needs no sudo.
2. **Whether to add MSL to your `PATH`**, in your shell's startup file. Open a new terminal afterwards so the change applies.
3. **Whether to set up the VS Code extension**, if it finds VS Code, VS Code Insiders, VSCodium or Cursor.
4. **Whether to install a Linux distribution now.** It lists what's available and suggests Ubuntu.

To install without piping a script into `sh`, or without questions, see [Manual install steps]({{< relref "/docs/install/install-manual" >}}).

{{< callout type="info" >}}
MSL releases are built by CI and signed ad hoc. They aren't notarised yet.
{{< /callout >}}

## Install a Linux distribution

If you didn't install one with the installer, list the distributions available and install one:

```console
$ msl --list --online
$ msl --install Ubuntu
```

The list is Microsoft's WSL distribution list, limited to the arm64 images MSL can run. To install something that isn't on it, see [Import any Linux distribution]({{< relref "/docs/how-to/use-custom-distro" >}}).

## Set up your Linux user name and password

When a distribution is installed, MSL runs its own first-run setup, as WSL does. For most distributions, that asks you to create a Linux user name and password. The account has no connection to your macOS account, and it becomes the distribution's default user, with `sudo` rights.

Some setup scripts mention Windows, for example "Provisioning the new WSL instance". That's their stock text. MSL skips the steps that need Windows.

## Check your installation

```console
$ msl --version
$ msl --list --verbose
  NAME            STATE           VERSION
* Ubuntu          Running         2
```

`msl --version` shows the MSL, kernel and macOS versions. `msl -l -v` lists your distributions; the `*` marks the default one.

## Open a shell

```console
$ msl
```

This opens a shell in your default distribution, in the macOS directory you ran `msl` from, which Linux sees under `/mnt/macos`. `msl ~` starts in your Linux home directory instead.

## Next steps

- [Set up a development environment]({{< relref "/docs/tutorials/environment" >}})
- [Basic commands for MSL]({{< relref "/docs/overview/basic-commands" >}})
- [Get started with VS Code]({{< relref "/docs/tutorials/msl-vscode" >}})
- [Troubleshooting]({{< relref "/docs/troubleshooting" >}})
