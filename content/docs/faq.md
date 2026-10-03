---
title: Frequently asked questions
weight: 7
description: Answers to common questions about MSL, the Modern Subsystem for Linux, from what it's for to files, networking and distributions.
---

## General

### What is MSL?

MSL, the Modern Subsystem for Linux, runs Linux distributions on macOS the way WSL runs them on Windows. The `msl` command takes `wsl.exe`'s arguments and prints the same output, and MSL runs the same distribution images that WSL does. See [What is MSL?]({{< relref "/docs/overview/about" >}}).

### Who is MSL for?

Developers who build software for Linux on a Mac, and especially teams that use both Windows and macOS. With WSL on Windows and MSL on macOS, everyone works in the same Linux distribution, with the same commands, scripts and `wsl.conf`, so setup instructions and bugs don't split by platform.

### What can I do with MSL?

Install a Linux distribution such as Ubuntu or Debian and use it as your development environment: a shell, the distribution's package manager, compilers and language runtimes, databases and other services. From Linux you can work on your macOS files under `/mnt/macos`, and a server you start in a distribution answers on `localhost` on macOS. With the MSL extension, VS Code opens folders inside a distribution. See [Basic MSL commands]({{< relref "/docs/overview/basic-commands" >}}).

### What does a typical workflow look like?

Keep the project in your Linux home directory, open it in VS Code with **MSL: Connect to Distro**, and build, test and debug in Linux, while the editor window and your browser stay on macOS. A web server you start in the distribution is at `http://localhost:<port>` in the browser. Because the environment is the same distribution your colleagues on WSL use, and close to what Linux CI runs, a bug found on one machine reproduces on the others.

### Why use MSL rather than Linux in a regular VM?

MSL keeps one lightweight VM for all your distributions and manages it for you. The VM starts on demand and stops on its own when nothing is running, and starting a distribution is fast because it creates namespaces in the running VM instead of booting a new one. You also get what a plain VM leaves you to set up: your macOS files in Linux, Linux files in Finder, `localhost` forwarding, DNS through macOS, and the `wsl.exe` command line.

### Which Macs does MSL run on?

Macs with Apple silicon, running macOS 27 or later. Distributions are arm64. x86_64-only distributions aren't supported yet ([#40](https://github.com/onexay/msl/issues/40)): `msl --list --online` leaves them out, and `msl --install` refuses them.

### Does MSL use a hypervisor?

It uses Apple's Virtualization.framework, which is part of macOS, and nothing else: no QEMU and no kernel extension. See [How MSL works]({{< relref "/docs/concepts/how-it-works" >}}).

### Can I run virtual machines inside MSL?

On a Mac with an M3 chip or later, MSL turns on nested virtualization, so `/dev/kvm` exists in every distribution: MSL's kernel has KVM built in (a custom kernel needs it too). `nestedVirtualization = false` in `~/.mslconfig` turns it off, as in WSL, and `msl --status` shows whether it's on. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config#main-settings" >}}).

### Can I access the GPU?

Not yet. MSL has no GPU access, and no support for Linux GUI apps. See [GPU acceleration]({{< relref "/docs/tutorials/gpu-compute" >}}) and [GUI apps]({{< relref "/docs/tutorials/gui-apps" >}}).

### Can I connect USB devices?

Not as USB devices. MSL can attach a disk image to the VM with `msl --mount`, but it doesn't pass USB devices from the Mac through to Linux. See [Connect USB devices]({{< relref "/docs/how-to/connect-usb" >}}).

### Is MSL made by Microsoft or Apple?

No. MSL is an independent open-source project, not affiliated with or endorsed by Microsoft or Apple. It follows WSL's command line and file formats so that the two work alike.

## Files

### How do I get to my macOS files?

Every distribution sees the macOS filesystem at `/mnt/macos`, the way WSL shows `C:` at `/mnt/c`. `/Users/me/src` on macOS is `/mnt/macos/Users/me/src` in Linux, and `mslpath` converts between the two. See [Working across file systems]({{< relref "/docs/concepts/filesystems" >}}).

### How do I use a macOS file with a Linux program?

Open it under `/mnt/macos`, or run `msl` from the macOS directory the file is in: `msl` starts in the same directory, under `/mnt/macos`. For example, from a macOS terminal:

```console
$ cd ~/Downloads
$ msl -e wc -l notes.txt
```

### Are files in Linux different from files under /mnt/macos?

Yes. Files in the distribution's own filesystem, such as your Linux home directory, behave as on any Linux system: case-sensitive names, Linux permissions and ownership, symlinks. Files under `/mnt/macos` live on macOS: names are usually case-insensitive, macOS checks permissions as your macOS user, and access is slower. Build and test in the Linux home directory when speed or case sensitivity matters. See [File access and permissions]({{< relref "/docs/concepts/file-permissions" >}}).

### How do I see Linux files from macOS?

While the VM runs, each distribution's files are at `~/.msl/distros/<distro>`, and in Finder under Locations. The folders disappear when the VM stops; starting any distribution brings them back.

### How do I use my Git credentials?

MSL never runs macOS programs from Linux, so Git in a distribution can't call macOS's Keychain helper. Set credentials up inside the distribution, for example with an SSH key or a credential helper there. See [Get started with Git]({{< relref "/docs/tutorials/msl-git" >}}).

## Networking

### How do I reach a Linux server from macOS?

Use `localhost`. A server listening on `localhost` in any distribution answers on `localhost` on macOS, over IPv4 and IPv6:

```console
$ python3 -m http.server 8000      # in the distribution
$ curl http://localhost:8000       # on macOS
```

If macOS already uses the port, MSL skips it and logs that in `~/Library/Application Support/msl/msld.log`. From a distribution, the name `host.internal` reaches macOS. See [Networking]({{< relref "/docs/concepts/networking" >}}).

### How do I run an SSH server?

Install and start the distribution's SSH server as on any Linux system, for example as a systemd service (see [systemd]({{< relref "/docs/concepts/systemd" >}})). Its port is forwarded to `localhost` on macOS like any other listening port. If macOS's Remote Login already uses port 22, give the distribution's server another port, since MSL doesn't forward a port macOS already uses. Forwarded ports listen on the Mac's loopback addresses only, so the server is reachable from the Mac itself, not from other machines.

The distribution must be running for the server to answer: see [Why does my server stop when I close the terminal?](#why-does-my-server-stop-when-i-close-the-terminal)

### Why does my server stop when I close the terminal?

A distribution stops about 15 seconds (`instanceIdleTimeout`) after its last `msl` session ends. Only `msl` sessions count as activity: shells, `msl -e` commands and VS Code connections. Services and background processes don't, even under systemd, so a database, a web server or a container stops with the distribution. To keep distributions running, turn the idle stop off in `~/.mslconfig`, then run `msl --shutdown` so the change applies:

```ini
[general]
instanceIdleTimeout = -1
```

The VM itself stops `vmIdleTimeout` (60 seconds by default) after the last distribution stops. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

### Can I run Docker?

Yes. Docker Engine from the distribution's packages runs in a distribution with systemd enabled, and a container port published with `-p` answers on `localhost` on macOS. See [Get started with Linux containers]({{< relref "/docs/tutorials/msl-containers" >}}).

### Why can't my distribution reach the internet?

The VM reaches the network through macOS, with NAT, and looks up names through macOS's own resolver. So if macOS can resolve and reach a host, a distribution normally can too, including over a VPN with split DNS. Things to check:

- whether the name resolves in the distribution: `getent hosts example.com`;
- whether the distribution keeps its own `/etc/resolv.conf` (`generateResolvConf = false` in `/etc/wsl.conf`);
- whether you set `dnsTunneling = false` in `~/.mslconfig`, which uses the VM network's DNS server instead of macOS's resolver;
- `msld.log` in `~/Library/Application Support/msl/`.

See [Troubleshooting]({{< relref "/docs/troubleshooting" >}}).

## Distributions

### How do I uninstall a distribution?

`msl --unregister <Distro>` deletes the distribution and all its files. It can't be undone; export the distribution first if you might want it back.

### How do I back up a distribution?

Export it to a tar file, and import it to restore it:

```console
$ msl --export Ubuntu ~/Backups/ubuntu.tar.gz --format tar.gz
$ msl --import Ubuntu-restored ~/msl/Ubuntu-restored ~/Backups/ubuntu.tar.gz
```

The location is the folder for the restored distribution's disk, `ext4.img`. To copy the whole disk instead of a tar file, use `msl --export <Distro> <file> --vhd` and `msl --import <Distro> <location> <file> --vhd`. See [Import any Linux distribution]({{< relref "/docs/how-to/use-custom-distro" >}}).

### How do I move my distributions to another Mac?

Export each distribution with `msl --export` and import it on the other Mac with `msl --import`. `msl --export` writes a plain tar file, the same format `wsl --import` takes. `msl --export <Distro> <file> --vhd` copies the distribution's disk instead, which `msl --import <Distro> <location> <file> --vhd` registers on the other Mac.

### Can I move a distribution to another drive?

Yes, as in WSL:

```console
$ msl --manage Ubuntu --move /Volumes/External/Ubuntu
```

MSL stops the distribution and moves its disk, `ext4.img`, into that folder. A distribution from MSL 0.1.11 or earlier, still on the shared `data.img`, gets a disk of its own there. See [Manage disk space]({{< relref "/docs/how-to/disk-space#move-a-distribution" >}}).

### How do I set the default user?

```console
$ msl --manage Ubuntu --set-default-user me
```

Or set `default` in the `[user]` section of the distribution's `/etc/wsl.conf`. The user must already exist in the distribution.

### How do I change the language of a distribution?

Sessions take their locale from the distribution's `/etc/default/locale` or `/etc/locale.conf`, as login shells do. Change it with the distribution's own tools, for example on Ubuntu or Debian:

```console
$ sudo update-locale LANG=en_US.UTF-8
```

The locale must be installed in the distribution. Open a new session afterwards.

### Can I use wsl.conf?

Yes. MSL reads `/etc/msl.conf`, falling back to `/etc/wsl.conf`, and supports the `[boot]`, `[user]`, `[automount]` and `[network]` settings that apply on macOS. `[interop]` settings are read and ignored. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

### Can I use MSL in production?

MSL is built for development on your own Mac, not for serving production workloads. It manages the VM for you: a distribution stops about 15 seconds after its last `msl` session ends, even with services still running in it, and the VM stops a minute after the last distribution does. You can turn these timeouts off (`instanceIdleTimeout` and `vmIdleTimeout`, where `-1` means never), but the environment is still tied to your macOS login, the Linux kernel comes with MSL, and every distribution has full access to your macOS files. A disk added while another distribution was running is also, until the VM restarts, mounted through the Mac file share, where `fsync` doesn't reach the SSD right away. See [Durability]({{< relref "/docs/how-to/disk-space#durability" >}}).

## Project

### Where can I give feedback?

- Report bugs and ask for features as [issues in onexay/msl](https://github.com/onexay/msl/issues). For a bug, include the output of `msl --version` and `msl --status`, and the relevant lines of `msld.log`.
- Report problems with these docs in [onexay/msl-docs](https://github.com/onexay/msl-docs/issues).
- Report security problems privately, as described in [Security model]({{< relref "/docs/security" >}}).

Planned work is in the [milestones](https://github.com/onexay/msl/milestones).
