---
title: Advanced settings configuration
weight: 2
description: Configure the MSL VM with ~/.mslconfig and each distribution with /etc/wsl.conf, the same files and keys WSL uses.
---

MSL reads the same two settings files as WSL. `~/.mslconfig` (the `.wslconfig` equivalent) configures the VM that runs every distribution. `/etc/wsl.conf` inside a distribution configures that distribution only.

| | `~/.mslconfig` | `/etc/wsl.conf` |
|---|---|---|
| Scope | The VM, so every distribution | One distribution |
| Configures | Memory, processors, kernel, localhost forwarding, DNS, nested virtualization, idle timeouts, disk size | systemd, a boot command, the default user, the `/mnt/macos` mount, hostname and generated network files |
| Location | Your macOS home directory (`MSL_CONFIG` overrides the path) | `/etc` inside the distribution |
| Applies | At the next VM start | At the next start of the distribution |

A `.wslconfig` from Windows works as `~/.mslconfig` without changes, and a distribution's own `/etc/wsl.conf` is honoured as it is.

## When changes apply

Settings are read when something starts, not while it runs.

- **`/etc/wsl.conf`**: stop the distribution with `msl -t <distro>`, then start it again by running any command in it. `[user] default` is the exception: it applies to the next command you run.
- **`~/.mslconfig`**: run `msl --shutdown`. The next `msl` command starts the VM with the new settings.

You don't have to wait for anything to time out. `msl --status` shows the settings the VM is running with, and lists any `~/.mslconfig` changes that are still waiting for a restart:

```console
$ msl --status
```

If you do nothing, a distribution stops 15 seconds after its last `msl` command ends (`instanceIdleTimeout`), and the VM stops 60 seconds after the last distribution does (`vmIdleTimeout`).

## wsl.conf

`/etc/wsl.conf` is an INI file: sections in brackets, `key = value` lines below them. Section and key names aren't case-sensitive, `#` and `;` start comments, and booleans are `true` or `false` (`1`/`0` and `yes`/`no` also work).

MSL also reads `/etc/msl.conf`. Keys in `msl.conf` override the same keys in `wsl.conf`, so you can keep a `wsl.conf` shared with Windows colleagues and put macOS-only changes in `msl.conf`. Edit either file with `sudo`.

### systemd support

Many distributions, including Ubuntu, are built to run systemd. It's off by default. To turn it on, add to `/etc/wsl.conf`:

```ini
[boot]
systemd = true
```

Then restart the distribution (`msl -t <distro>`). See [Use systemd to manage services]({{< relref "/docs/concepts/systemd" >}}).

### Boot settings

Section: `[boot]`

| Key | Value | Default | Notes |
|---|---|---|---|
| `systemd` | boolean | `false` | Runs systemd as the distribution's init. Needs `/sbin/init` in the image. |
| `command` | string | none | A command that runs as root each time the distribution starts, through `/bin/sh -c`. It runs in the background; startup doesn't wait for it. With systemd, it runs once systemd is up. |

### Automount settings

Section: `[automount]`

| Key | Value | Default | Notes |
|---|---|---|---|
| `enabled` | boolean | `true` | `true` mounts the macOS file system at `<root>macos`, so `/mnt/macos` by default. `false` leaves it out. |
| `root` | string | `/mnt/` | The directory that holds the macOS mount. With `root = /`, macOS files are at `/macos`. |
| `mountFsTab` | boolean | `true` | `true` runs `mount -a` at start, so file systems listed in `/etc/fstab` are mounted. In a systemd distribution, systemd mounts `/etc/fstab` itself. |

WSL's `options` key, the DrvFs mount options (`uid`, `gid`, `umask`, `metadata`, `case`), has no equivalent: the macOS mount isn't DrvFs. See [File access and permissions]({{< relref "/docs/concepts/file-permissions" >}}).

### Network settings

Section: `[network]`

| Key | Value | Default | Notes |
|---|---|---|---|
| `hostname` | string | The Mac's host name | The distribution's hostname. MSL changes characters Linux doesn't allow in a hostname. |
| `generateHosts` | boolean | `true` | `true` makes MSL write `/etc/hosts` and `/etc/hostname` at each start. `/etc/hosts` gets `localhost`, the hostname, `host.internal` for the Mac, and the entries from the Mac's own `/etc/hosts`. |
| `generateResolvConf` | boolean | `true` | `true` makes MSL write `/etc/resolv.conf` at each start. `false` keeps the distribution's own file. |

### Interop settings

Section: `[interop]`

`enabled` and `appendWindowsPath` are accepted and ignored. MSL never runs macOS programs from Linux and never adds macOS directories to `PATH`. See [Working across file systems]({{< relref "/docs/concepts/filesystems#no-macos-tools-from-linux" >}}).

### User settings

Section: `[user]`

| Key | Value | Default | Notes |
|---|---|---|---|
| `default` | string | The user created at first run | The user that `msl` commands run as when you don't pass `-u`. If the user doesn't exist, MSL falls back to the distribution's default user. |

`msl --manage <distro> --set-default-user <user>` sets the default user from macOS instead.

### Settings not available

WSL's `[boot] protectBinfmt` and `initTimeout`, and the `[gpu]` and `[time]` sections, have no effect in MSL.

### Example wsl.conf

```ini
# Mount macOS files at /macos instead of /mnt/macos, and process /etc/fstab.
[automount]
enabled = true
root = /
mountFsTab = true

# Use a fixed hostname and your own /etc/resolv.conf.
[network]
hostname = devbox
generateHosts = true
generateResolvConf = false

# Commands run as this user unless you pass -u.
[user]
default = me

# Run systemd, and a command at every start.
[boot]
systemd = true
command = mkdir -p /run/myapp
```

## .mslconfig

`~/.mslconfig` doesn't exist until you create it. It's an INI file, like `.wslconfig`. The VM section is `[msl2]`; `[wsl2]` works too, so you can copy a `.wslconfig` as it is.

- Keys MSL doesn't use, including the rest of `.wslconfig`'s keys, are accepted and ignored.
- A value MSL can't read prints a warning and falls back to the default. A malformed file never stops the VM from starting. `msl --status` lists the warnings.
- Sizes are bytes, or a number with `KB`, `MB`, `GB` or `TB` (also `K`, `M`, `G`, `T`), for example `8GB`. The units are binary: `1GB` is 1024 MB.
- Paths are macOS paths; `~` means your home directory.

### Main settings

Section: `[msl2]` (or `[wsl2]`)

| Key | Value | Default | Notes |
|---|---|---|---|
| `memory` | size | 50% of the Mac's memory | How much memory the VM gets. It goes back to macOS only when the VM stops; see [How MSL works]({{< relref "/docs/concepts/how-it-works#memory" >}}). |
| `processors` | number | All of the Mac's processors | How many processors the VM gets. |
| `kernel` | path | The kernel bundled with MSL | A custom arm64 Linux kernel image. |
| `kernelCommandLine` | string | none | Extra kernel command-line arguments, added after MSL's own. |
| `localhostForwarding` | boolean | `true` | Makes TCP ports that Linux programs listen on reachable on `localhost` on macOS. See [Networking]({{< relref "/docs/concepts/networking#localhost" >}}). |
| `dnsTunneling` | boolean | `true` | `true` resolves names through macOS's resolver. `false` uses the VM network's DNS server. |
| `nestedVirtualization` | boolean | `true` | Lets the VM run virtual machines of its own: `/dev/kvm` exists in the distributions on a Mac with an M3 chip or later (MSL's kernel has KVM; a custom `kernel` needs it too). `msl --status` shows whether it's on. |
| `vmIdleTimeout` | number | `60000` | Milliseconds the VM waits after the last distribution stops before it shuts down. `-1` keeps it running. |
| `defaultVhdSize` | size | 256 GB, or the size of the Mac's disk if smaller | Maximum size of each new distribution's disk. `msl --install --vhd-size` overrides it for one distribution, and `msl --manage <distro> --resize` grows an existing disk. From 4 GB to 4 TB. See [Manage disk space]({{< relref "/docs/how-to/disk-space" >}}). |
| `fileViewTransport` | `unix` or `tcp` | `unix` | How `~/.msl/distros` is served to macOS. `unix` uses a socket only your user can open. `tcp` uses a port on `127.0.0.1`, which other users on the Mac can reach. |

### General settings

Section: `[general]`

| Key | Value | Default | Notes |
|---|---|---|---|
| `instanceIdleTimeout` | number | `15000` | Milliseconds a distribution keeps running after its last `msl` command or VS Code connection ends. Services and containers running inside don't count as activity. `-1` keeps distributions running until you stop them, and so keeps the VM and its memory too. See [systemd]({{< relref "/docs/concepts/systemd#keep-services-running" >}}). |

### Experimental settings

Section: `[experimental]`

| Key | Value | Default | Notes |
|---|---|---|---|
| `autoMemoryReclaim` | `disabled`, `gradual` or `dropCache` | `dropCache` | Accepted for compatibility, with no effect: macOS gets the VM's memory back only when the VM stops ([#37](https://github.com/onexay/msl/issues/37)). |

### Example .mslconfig

```ini
# Settings for the VM that runs every distribution.
[msl2]
# At most 8 GB of memory and 4 processors.
memory = 8GB
processors = 4

# Keep the VM for 5 minutes after the last distribution stops.
vmIdleTimeout = 300000

# Give each new distribution a disk with room for 512 GB.
defaultVhdSize = 512GB

[general]
# Keep distributions running for a minute after the last command ends.
instanceIdleTimeout = 60000
```

## Environment variables

These are set on macOS, in the shell you run `msl` from.

| Variable | Effect |
|---|---|
| `MSL_CONFIG` | Path of the VM settings file, instead of `~/.mslconfig`. |
| `MSLENV` | macOS variables to pass into Linux. See [Share environment variables with MSLENV]({{< relref "/docs/concepts/filesystems#share-environment-variables-with-mslenv" >}}). |
| `MSL_ERROR_CODES=1` | Adds a wsl.exe-style `Error code:` line to error messages. |
| `MSL_DISTRIBUTION_LIST_URL` | A distribution list to use instead of Microsoft's, for `msl --list --online` and `msl --install`. |
