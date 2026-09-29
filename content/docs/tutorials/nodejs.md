---
title: Install Node.js on MSL
weight: 8
description: Install Node.js in an MSL distribution with nvm or the distribution's packages, and run dev servers you can open on macOS.
---

Install Node.js inside the distribution, so that `node`, `npm` and native modules all build and run on Linux.

## Install with nvm

[nvm](https://github.com/nvm-sh/nvm) installs and switches between Node.js versions per user, without `sudo`. It's the best choice when your projects need different versions.

1. Install `curl` if the distribution doesn't have it (stock Debian doesn't):

    ```console
    $ sudo apt update && sudo apt install curl
    ```

2. Install nvm with the command from [nvm's README](https://github.com/nvm-sh/nvm#installing-and-updating), then open a new shell.
3. Install Node.js:

    ```console
    $ nvm install --lts          # the current long-term support release
    $ node --version
    $ npm --version
    ```

`nvm ls` lists the installed versions, and `nvm use <version>` switches between them.

## Install from the distribution's packages

If one version is enough, use the package manager. The version is whatever the distribution ships, which is often older than the current release:

```console
$ sudo apt install nodejs npm
```

## Keep projects on the Linux side

Keep projects, and their `node_modules`, in your Linux home directory rather than under `/mnt/macos`. Installs and builds are much faster on the distribution's own disk.

MSL never runs macOS programs from Linux, and never puts macOS directories on Linux's `PATH`. `npm`, `node-gyp` and similar tools therefore find only Linux toolchains, and native modules are built for Linux even if the project is under `/mnt/macos`. Don't share one `node_modules` between macOS and Linux: install dependencies separately on each side. Native modules also need a compiler in the distribution: on Ubuntu or Debian, `sudo apt install build-essential`.

## Run a dev server

A dev server that listens on `localhost` in the distribution is reachable at `localhost` on macOS:

```console
$ npm run dev                    # in the distribution; say it listens on port 3000
```

Open `http://localhost:3000` in a macOS browser. See [Networking]({{< relref "/docs/concepts/networking" >}}).

To edit and debug the project, open it in VS Code with the MSL extension. See [Get started using VS Code with MSL]({{< relref "/docs/tutorials/msl-vscode" >}}).
