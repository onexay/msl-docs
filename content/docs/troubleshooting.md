---
title: Troubleshooting MSL
weight: 8
description: Where to find MSL's logs and status, and fixes for common problems with installing, starting, files, networking, disk space and VS Code.
---

Start with the tools below, then look for your problem in the sections that follow. If it isn't there, [report a bug](#report-a-bug).

## Where to look

| Tool | What it tells you |
|---|---|
| `msl --status` | The default distribution, the VM's effective settings (memory, CPUs, kernel, networking, idle timeouts), the disk's size and free space, and any `~/.mslconfig` changes waiting for a restart. |
| `msl --version` | The MSL, kernel and macOS versions. |
| `~/Library/Application Support/msl/msld.log` | The service's log: VM starts and stops, idle timeouts, port forwarding, errors. |
| `~/Library/Application Support/msl/console.log` | The VM's console output, including the Linux kernel's messages. |
| `MSL_ERROR_CODES=1 msl …` | Adds WSL-style `Error code:` lines to error messages. |
| `msl --debug-shell` | A root BusyBox shell in the VM itself, outside every distribution. |

## Installation

**`msl: command not found` right after installing.** The installer adds MSL's `bin` directory to `PATH` in your shell's startup file (`~/.zshrc`, `~/.bash_profile`, `~/.config/fish/config.fish` or `~/.profile`). Open a new terminal so the change applies. If you installed with `--no-path`, run `msl` by its full path, for example `~/.local/bin/msl`.

**MSL 0.1.9 doesn't start on macOS 26.** 0.1.9 was built with a newer Xcode than macOS 26 supports, so its `msld` fails to start there. Reinstall with the one-line installer from [Install MSL]({{< relref "/docs/install/install" >}}); your distributions are kept. 0.1.10 and later are fine.

## Starting distributions

**The first-run setup mentions Windows.** Some distributions' setup scripts print WSL wording, such as "Provisioning the new WSL instance". That's their stock text. MSL skips the setup steps that need Windows.

**A distribution is x86_64-only.** Not supported yet ([#40](https://github.com/onexay/msl/issues/40)). `msl --list --online` leaves these distributions out, and `msl --install` refuses them.

**A program fails with page-size errors, or won't start.** MSL's kernel uses 16 KiB memory pages, like the Mac itself, because 4 KiB pages in the VM hit a Virtualization.framework problem that corrupts memory when macOS runs short of it ([#48](https://github.com/onexay/msl/issues/48)). `getconf PAGESIZE` shows `16384`. Current distributions work with this, including allocators such as jemalloc. A program built on the assumption of 4 KiB pages (for example with `--with-lg-page=12`) fails to start or to map files on any 16 KiB or 64 KiB Arm Linux. Use your distribution's package, or rebuild the program without that assumption.

**A server, database or container stops when I close the terminal.** A distribution stops about 15 seconds after its last `msl` session ends. Only `msl` sessions count as activity (shells, `msl -e` commands, VS Code connections), not services running in the distribution, even under systemd. To keep distributions running, set this in `~/.mslconfig` and run `msl --shutdown` so it applies:

```ini
[general]
instanceIdleTimeout = -1
```

See [systemd]({{< relref "/docs/concepts/systemd" >}}) and [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

**A `~/.mslconfig` change has no effect.** VM settings apply the next time the VM starts. `msl --status` lists changes that are still pending; `msl --shutdown` stops the VM so the next command starts it with them.

**MSL uses more memory than the distributions need.** Virtualization.framework doesn't give memory back to macOS while the VM runs, so it returns only when the VM stops: after `vmIdleTimeout` with nothing running, or with `msl --shutdown`. `autoMemoryReclaim` has no effect on macOS. [#37](https://github.com/onexay/msl/issues/37) explains why. To cap what the VM can take, set `memory` in `~/.mslconfig`.

## Files

**`~/.msl/distros` is empty.** The folders there are mounts that exist only while the VM runs. Start any distribution, for example with `msl -e true`, and they come back.

**A build is slow, or file names clash, under `/mnt/macos`.** Files under `/mnt/macos` live on macOS: access is slower than the distribution's own disk, and names are usually case-insensitive. Work in your Linux home directory instead. See [Working across file systems]({{< relref "/docs/concepts/filesystems" >}}).

**A path from an old script doesn't exist.** MSL 0.1.7 renamed `/mnt/mac` to `/mnt/macos`, and the `MSL_MAC_*` variables to `MSL_MACOS_*`. There's no compatibility link.

## Networking

**A port isn't reachable from macOS.** MSL forwards ports that servers in a distribution listen on, on `localhost` or on all addresses. If macOS already uses the port, MSL skips it and logs that in `msld.log`; stop the macOS program or use another port. Check also that `localhostForwarding` isn't `false` in `~/.mslconfig`, and that the distribution is still running (see the idle stop above).

**Names don't resolve, or resolve differently from macOS.** Distributions resolve names through macOS's resolver, so VPNs, split DNS, `/etc/resolver` entries and `.local` names behave as on macOS. If they don't, check whether `dnsTunneling = false` is set in `~/.mslconfig`, or whether the distribution keeps its own `/etc/resolv.conf` (`generateResolvConf = false` in `/etc/wsl.conf`). See [Networking]({{< relref "/docs/concepts/networking" >}}).

## Disk space

**`data.img` stays large after deleting files.** Deleting files frees space inside the disk, not on macOS. MSL hands freed space back when the VM shuts down; to do it now, run `msl --manage <Distro> --compact`.

**A distribution runs out of space.** All distributions share one disk. `msl --status` shows its size and what's free. Grow it:

```console
$ msl --shutdown
$ msl --manage Ubuntu --resize 512GB
```

If `msl --status` warns that macOS is nearly out of space, free space on macOS first: the disk is sparse, so the distributions can't see that macOS has run out, and their writes fail when it does. See [Manage disk space]({{< relref "/docs/how-to/disk-space" >}}).

## VS Code

**"No remote extension installed to resolve msl".** The extension didn't start. The IDE's extension host log (**Output › Log (Extension Host)**) shows `CANNOT use API proposal: resolvers`. Run `msl --manage-ide`, or add `"enable-proposed-api": ["onexay.msl"]` to `argv.json` yourself with **Preferences: Configure Runtime Arguments**. Then quit the IDE with ⌘Q; closing the window isn't enough.

**"msl --list --verbose --json exited with 255".** The extension found an MSL older than 0.1.3. Run `msl --manage-ide --install` with the MSL you want it to use, or set the `msl.path` setting.

**`bash: warning: setlocale: … cannot change locale` in the terminal.** The VS Code Server started without the distribution's locale. MSL 0.1.9 and later start it with the locale from `/etc/default/locale`. After updating, reload the window or run `msl --shutdown`.

The extension's own log is under **Output › MSL**. See [Get started with VS Code]({{< relref "/docs/tutorials/msl-vscode" >}}).

## Report a bug

Open a [bug report](https://github.com/onexay/msl/issues/new/choose) with:

- the output of `msl --version` and `msl --status`;
- the steps that reproduce the problem;
- the relevant lines from `msld.log` and `console.log`, with anything private removed.

Report security problems privately instead, as described in [Security model]({{< relref "/docs/security" >}}).
