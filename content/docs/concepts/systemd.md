---
title: Use systemd to manage services
weight: 5
description: Turn on systemd in an MSL distribution, manage services with systemctl, and keep services running when no terminal is open.
---

Many Linux distributions, including Ubuntu and Debian, use systemd to start and manage services such as databases, web servers and Docker. MSL can run systemd in a distribution, as WSL does, so `systemctl` and service units work as on any Linux machine.

## Enable systemd

systemd is off by default. Turn it on per distribution in `/etc/wsl.conf`:

```console
$ sudo nano /etc/wsl.conf        # in the distribution
```

```ini
[boot]
systemd = true
```

Then restart the distribution, from macOS:

```console
$ msl -t Ubuntu                  # stop it
$ msl -d Ubuntu                  # start it again, with systemd
```

The image must have systemd installed, at `/sbin/init`. If it doesn't, the setting is ignored and the distribution starts without it.

## Check that it's running

```console
$ systemctl is-system-running          # "running", or "degraded" if a unit failed
$ systemctl list-units --type=service
```

MSL reports a systemd distribution as running, and runs your command in it, only once systemd has started. The first start can take a few seconds longer than without systemd.

Some units assume Windows or a real console. MSL masks them each time the distribution starts: Ubuntu's `wsl-pro-service.service` (which talks to a Windows agent), `console-getty.service` and `getty@tty1.service`. The masks live in `/run`, so the image isn't changed. MSL also masks systemd's default network `.link` file so the network interface stays `eth0`, unless you have your own in `/etc/systemd/network`.

## Manage services

Use `systemctl` as usual:

```console
$ sudo systemctl enable --now postgresql
$ systemctl status postgresql
$ journalctl -u postgresql
```

A service listening on a TCP port is reachable from macOS on `localhost`. See [Networking]({{< relref "/docs/concepts/networking#localhost" >}}).

## Keep services running

A distribution stops when nothing uses it: 15 seconds after its last `msl` session ends (`instanceIdleTimeout`). Only `msl` sessions count as activity: shells, commands run with `msl`, and VS Code windows connected to the distribution. Services and containers running inside don't. When the distribution stops, its services stop with it, and their ports stop answering on macOS.

To keep services up:

- **Keep a session open.** Leave a terminal with `msl` running, or a VS Code window connected to the distribution. The distribution stays up for as long as that session lasts.
- **Turn the idle stop off.** Set `instanceIdleTimeout = -1` in `~/.mslconfig`, then run `msl --shutdown`. Distributions then run until you stop them with `msl -t <distro>` or `msl --shutdown`.

```ini
[general]
instanceIdleTimeout = -1
```

{{< callout type="info" >}}
With `instanceIdleTimeout = -1`, the VM also keeps running, because it stops only after the last distribution does. The memory it uses goes back to macOS only when the VM stops, so run `msl --shutdown` when you're done. See [How MSL works]({{< relref "/docs/concepts/how-it-works#memory" >}}).
{{< /callout >}}

## How distributions stop

Stopping is clean, whether by `msl -t`, `msl --shutdown` or the idle timeout. MSL asks systemd to power the distribution off, so services stop in order and journald closes its files. Anything still running after 10 seconds is killed. `msl --shutdown --force` stops the VM at once, without waiting.

## Without systemd: [boot] command

To start one program when a distribution starts, without systemd, use `[boot] command` in `/etc/wsl.conf`. It runs as root through `/bin/sh -c`, in the background, each time the distribution starts:

```ini
[boot]
command = service ssh start
```

The same idle rules apply: the program stops when the distribution does.
