---
title: Get started with databases on MSL
weight: 4
description: Install PostgreSQL, SQLite and other databases in an MSL distribution, run them as services, and connect from macOS.
---

Databases run in an MSL distribution as they do on any Linux machine: install them with the distribution's package manager and run them as systemd services. A database listening on `localhost` in the distribution is reachable on `localhost` on macOS, so tools on either side can connect.

This guide uses Ubuntu. Other distributions have the same databases under their own package names.

## Prerequisites

- MSL with a distribution installed. See [Install MSL]({{< relref "/docs/install/install" >}}).
- systemd enabled in the distribution, so databases run as services. Ubuntu's WSL images enable it already. See [Use systemd to manage services]({{< relref "/docs/concepts/systemd" >}}).

## PostgreSQL

Install it:

```console
$ sudo apt update
$ sudo apt install postgresql
```

The package starts PostgreSQL as a service, listening on `127.0.0.1:5432`. Check it:

```console
$ systemctl is-active postgresql
active
$ sudo -u postgres psql -c 'select version()'
```

### Create a user and a database

```console
$ sudo -u postgres createuser --pwprompt $USER
$ sudo -u postgres createdb --owner $USER myapp
$ psql -h localhost myapp
```

`-h localhost` connects over TCP with the password you set. Without it, `psql` uses the Unix socket and Ubuntu's peer authentication, which works for the Linux user of the same name.

### Connect from macOS

Port 5432 is forwarded to `localhost` on macOS while the distribution runs. Any PostgreSQL client or GUI tool on the Mac can connect to `localhost:5432` with the user and password you created:

```console
$ psql -h localhost -U <your Linux user> myapp        # on macOS, if you have psql there
```

If a PostgreSQL server already runs on macOS on port 5432, MSL can't forward the port, and it logs that in `~/Library/Application Support/msl/msld.log`. Stop one of them, or change `port` in the distribution's `postgresql.conf`. See [Networking considerations]({{< relref "/docs/concepts/networking#localhost" >}}).

## SQLite

SQLite is a library and a file, with no server to run:

```console
$ sudo apt install sqlite3
$ sqlite3 ~/myapp.db 'create table notes (body text)'
```

Keep database files in the Linux home directory rather than under `/mnt/macos`, where file access is slower. See [Working across file systems]({{< relref "/docs/concepts/filesystems" >}}).

## Other databases

MySQL, MariaDB, Redis and other servers packaged by your distribution install the same way: install the package, check its service with `systemctl`, and connect to its port on `localhost` from macOS. This guide was tested with PostgreSQL.

## Keep a database running

A distribution stops 15 seconds after its last `msl` session ends: the last shell, `msl -e` command or VS Code window. A running database doesn't keep it running, so closing your last terminal stops the database cleanly with the distribution. It starts again with the distribution.

To keep it running with no terminal open, turn off the idle stop in `~/.mslconfig` on macOS:

```ini
[general]
instanceIdleTimeout = -1
```

Run `msl --shutdown` for the change to apply. The VM then keeps its memory until you run `msl --shutdown`. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

## Back up a database

Use the database's own dump tool, such as `pg_dump`, and copy the dump to macOS through `/mnt/macos`:

```console
$ pg_dump myapp > /mnt/macos/Users/<you>/Backups/myapp.sql
```

To back up the whole distribution instead, use `msl --export`, or `msl --export --vhd` for a copy of its disk. See [Import any Linux distribution]({{< relref "/docs/how-to/use-custom-distro" >}}).

## Durability

A committed transaction isn't guaranteed to be on the Mac's SSD. The database's `fsync` reaches macOS's file cache, not the SSD: MSL flushes a distribution's disk when it's detached and at `msl --shutdown`. If MSL or the VM crashes, committed data is kept. If macOS crashes or the Mac loses power, recent commits can be lost and the file system can be damaged. Run `msl --shutdown` before relying on data surviving a power loss, and keep dumps of data you can't recreate. See [Durability]({{< relref "/docs/how-to/disk-space#durability" >}}).
