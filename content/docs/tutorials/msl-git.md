---
title: Get started using Git on MSL
weight: 3
description: Install and configure Git in an MSL distribution, authenticate to GitHub and other hosts, and choose where to keep your repositories.
---

Git runs inside the distribution, like the rest of your Linux toolchain. This guide installs it, sets up your identity and authentication, and explains where to keep repositories.

## Install Git

Most distributions include Git, or have it one command away. On Ubuntu or Debian:

```console
$ sudo apt update && sudo apt install git
$ git --version
```

On Fedora, use `sudo dnf install git`.

## Set your name and email

Git records these in every commit you make:

```console
$ git config --global user.name "Your Name"
$ git config --global user.email "you@example.com"
```

## Authenticate

MSL never runs macOS programs from Linux. Git inside the distribution therefore can't use macOS's Keychain credential helper, or the Git and SSH keys you set up on macOS. Set up authentication in the distribution itself, with either of these.

### SSH keys

Create a key in the distribution and add the public key to your Git host:

```console
$ ssh-keygen -t ed25519 -C "you@example.com"
$ cat ~/.ssh/id_ed25519.pub         # paste this into your Git host's SSH keys settings
$ ssh -T git@github.com             # check the connection
```

Then clone with SSH URLs, such as `git@github.com:owner/repo.git`.

### GitHub CLI

For GitHub over HTTPS, install the [GitHub CLI](https://cli.github.com/) in the distribution and log in. It stores a token and sets itself up as Git's credential helper:

```console
$ gh auth login
$ gh auth setup-git
```

## Where to keep repositories

Clone into your Linux home directory, for example `~/src`:

```console
$ mkdir -p ~/src && cd ~/src
$ git clone git@github.com:owner/repo.git
```

Git is much faster on the distribution's own disk than on macOS files under `/mnt/macos`. The Linux side is also case-sensitive, like the Linux systems your code runs on.

A repository on macOS works from Linux too, under `/mnt/macos`. Files there appear to belong to whichever Linux user reads them, so Git's ownership check (`safe.directory`) passes. Use this for occasional work, not for a repository you build in every day. See [Working across file systems]({{< relref "/docs/concepts/filesystems" >}}).

## Line endings

macOS and Linux both use LF line endings, so moving files between them never changes line endings. If teammates on Windows work on the same repository, add a `.gitattributes` file so that every platform checks files out the same way, for example:

```text
* text=auto eol=lf
```

## Ignore files

Add a `.gitignore` for build output and dependencies, such as `node_modules/` or `target/`. GitHub keeps [templates for common languages](https://github.com/github/gitignore).

## Git in VS Code

In a VS Code window connected to a distribution, the Source Control view uses the Git in that distribution, with the configuration and authentication you set up above. See [Get started using VS Code with MSL]({{< relref "/docs/tutorials/msl-vscode" >}}).
