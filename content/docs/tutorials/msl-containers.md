---
title: Get started with Linux containers on MSL
weight: 5
description: Run Docker Engine inside an MSL distribution with systemd, and reach published container ports from macOS.
---

Docker Engine runs inside an MSL distribution like it does on any Linux machine. There's no separate Docker VM: containers run in the distribution, and their published ports answer on `localhost` on macOS. This guide sets up Docker Engine in Ubuntu.

## Prerequisites

- MSL with a distribution installed. See [Install MSL]({{< relref "/docs/install/install" >}}).
- systemd enabled in the distribution. Ubuntu's WSL images enable it already. For other distributions, see [Use systemd to manage services]({{< relref "/docs/concepts/systemd" >}}).

Check that systemd is running:

```console
$ ps -p 1 -o comm=
systemd
```

## Install Docker Engine

Install Ubuntu's `docker.io` package:

```console
$ sudo apt update
$ sudo apt install docker.io
$ sudo usermod -aG docker $USER      # run docker without sudo
```

Close the shell and open a new one with `msl` so the group change applies. Then check that the service is running:

```console
$ systemctl is-active docker
active
$ docker run --rm hello-world
Hello from Docker!
…
```

## Reach a container from macOS

Publish a container port as usual. MSL forwards it to `localhost` on macOS, like any other port a distribution listens on:

```console
$ docker run -d --name web -p 8080:80 nginx:alpine
```

Open `http://localhost:8080` in a browser on macOS. See [Networking considerations]({{< relref "/docs/concepts/networking#localhost" >}}) for how forwarding works and what happens when macOS already uses the port.

## Keep containers running

A distribution stops 15 seconds after its last `msl` session ends: the last shell, `msl -e` command or VS Code window. Running containers and services don't keep it running, so closing your last terminal stops your containers too.

To keep containers running, either keep a terminal or VS Code window open, or turn off the idle stop in `~/.mslconfig` on macOS:

```ini
[general]
instanceIdleTimeout = -1
```

Run `msl --shutdown` for the change to apply. With the idle stop off, the VM keeps its memory until you run `msl --shutdown`, because memory goes back to macOS only when the VM stops. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

The `docker.io` package enables the Docker service, so Docker starts with the distribution. To start containers with it too, give them a restart policy (`docker run --restart unless-stopped …`).

## Images and architecture

MSL runs arm64 Linux, so use images that include `linux/arm64`, as most official images on Docker Hub do. MSL doesn't support x86_64 (`linux/amd64`) Linux yet ([#40](https://github.com/onexay/msl/issues/40)).

Images and containers are stored in the distribution, on MSL's shared disk. `docker system prune` frees space in the disk; to hand that space back to macOS, see [Manage disk space]({{< relref "/docs/how-to/disk-space" >}}).

## Use Docker from VS Code

Open the distribution in VS Code with the MSL extension ([Get started using VS Code with MSL]({{< relref "/docs/tutorials/msl-vscode" >}})). Docker commands in VS Code's terminal run against the distribution's Docker Engine.
