---
title: How MSL works
weight: 6
description: The parts of MSL, how distributions share one lightweight VM, when things start and stop, and where MSL keeps its state on macOS.
---

MSL is built the way WSL 2 is: one lightweight Linux VM runs every distribution, and each distribution is an isolated set of processes inside it rather than a VM of its own. The VM runs on Apple's Virtualization.framework, with no other hypervisor or kernel extension.

## The parts

```text
msl (command)  ──▶  msld (background service, one per macOS user)
                      │  runs the VM, forwards ports, serves ~/.msl/distros
                      ▼
               Linux VM (MSL kernel)
                 ├─ Ubuntu   (its own init and processes)
                 └─ Debian   (its own init and processes)
```

- **`msl`** is the command you run. It takes `wsl.exe`'s arguments and passes each request to `msld`.
- **`msld`** is a background process that runs as your macOS user. The first `msl` command starts it, and it stays until you log out or `msl --update` replaces it. It isn't a LaunchAgent or a login item, and it needs no administrator rights.
- **The VM** runs MSL's Linux kernel. `msld` starts it when a distribution first needs it.
- **Each distribution** runs inside the VM with its own init: MSL's own, or systemd if you [turn it on]({{< relref "/docs/concepts/systemd" >}}).

## What distributions share

Distributions are isolated from each other with Linux namespaces, as in WSL 2.

| Shared by all distributions | Separate for each distribution |
|---|---|
| The kernel, memory and processors | The file system: its own disk, `ext4.img`, and its own mounts |
| The network: one IP address and one `localhost` | Processes and process IDs |
| The macOS file system at `/mnt/macos` | Hostname |
| Disks attached with `msl --mount`, at `/mnt/msl` | Control groups, and init (systemd or MSL's) |

Because a distribution is a set of namespaces rather than a VM, it starts in milliseconds once the VM is up. Isolation between distributions is the same as in WSL 2: good enough to keep them from getting in each other's way, but weaker than separate VMs.

The VM has 16 disk slots, because Virtualization.framework can't add a disk to a running VM. `msld` attaches every distribution's disk when the VM starts, and a distribution's disk when you use it. With all slots taken, the stopped distribution used longest ago gives its slot up. See [Manage disk space]({{< relref "/docs/how-to/disk-space" >}}).

## Starting and stopping

Everything starts on demand and stops when it's idle:

1. The first `msl` command starts `msld`, which starts the VM and then the distribution.
2. A distribution stops 15 seconds after its last `msl` session ends: a shell, a command, or a VS Code connection (`instanceIdleTimeout`). Services running inside don't keep it up.
3. The VM stops 60 seconds after the last distribution does (`vmIdleTimeout`).

`msl -t <distro>` stops one distribution now, and `msl --shutdown` stops all of them and the VM. Both timeouts are set in `~/.mslconfig`. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}).

## Memory

The VM gets 50% of the Mac's memory by default (`memory` in `~/.mslconfig`). Memory the VM has used goes back to macOS only when the VM stops, not while it runs: Virtualization.framework doesn't return freed guest memory to macOS ([#37](https://github.com/onexay/msl/issues/37)). WSL's `autoMemoryReclaim` is accepted and has no effect.

In practice, the idle timeouts return memory for you: when you stop using MSL, the VM stops a minute or so later. To get it back now, run `msl --shutdown`.

## The kernel

MSL runs its own build of Linux, from [msl-kernel](https://github.com/onexay/msl-kernel), bundled with each release. `msl --version` shows which one.

The kernel uses 16 KiB memory pages, like the Mac itself, where most Arm Linux systems use 4 KiB. With 4 KiB pages, a Virtualization.framework bug corrupts the VM's memory when macOS runs short of memory ([#48](https://github.com/onexay/msl/issues/48)). Distribution packages work with 16 KiB pages; a program built on the assumption of 4 KiB pages may not. `getconf PAGESIZE` prints `16384`. See [Troubleshooting]({{< relref "/docs/troubleshooting" >}}).

With `nestedVirtualization` on (the default) and a Mac with an M3 chip or later, the VM can run virtual machines of its own: `/dev/kvm` exists when the kernel has KVM.

The VM keeps one machine identifier across boots, and its own `/etc/machine-id` is that identifier's UUID. Distributions keep their own `/etc/machine-id`.

`kernel` in `~/.mslconfig` boots a kernel of your own instead.

## Where MSL keeps its state

| What | Where on macOS |
|---|---|
| Distributions' disks | `~/Library/Application Support/msl/distros/<id>/ext4.img`, or the location you chose |
| The list of distributions, the machine identifier, logs and sockets | `~/Library/Application Support/msl/` |
| Distribution files, while the VM runs | `~/.msl/distros/<distro>` |
| Downloaded images and the VS Code Server | `~/Library/Caches/msl/` |
| VM settings | `~/.mslconfig`, if you create it |
| MSL itself | `~/.local` by default, or the prefix you installed to |

`msl --uninstall` removes MSL itself and keeps your distributions and settings. See [Update and uninstall MSL]({{< relref "/docs/install/upgrade" >}}).
