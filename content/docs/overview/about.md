---
title: What is MSL?
weight: 1
description: MSL, the Modern Subsystem for Linux, runs Linux distributions on macOS the way WSL runs them on Windows.
---

MSL, the Modern Subsystem for Linux, runs a Linux environment on your Mac without a separate virtual machine to set up and manage. The `msl` command is `wsl.exe` for macOS: it takes the same arguments, prints the same output and returns the same exit codes. MSL needs Apple silicon and macOS 27 or later.

Teams split across Windows and macOS usually end up with two developer setups, two sets of instructions and two sets of bugs. With WSL on Windows and MSL on macOS, everyone develops in the same Linux distribution, from the same image, with the same commands, scripts and `wsl.conf`.

With MSL you can:

- Install and run Linux distributions from Microsoft's WSL distribution list, such as Ubuntu and Debian, using their arm64 images unmodified. See [Install MSL]({{< relref "/docs/install/install" >}}), or [import any Linux distribution]({{< relref "/docs/how-to/use-custom-distro" >}}).
- Keep each distribution's files in its own Linux file system, and browse them in Finder.
- Work with your macOS files from Linux, under `/mnt/macos` (like `/mnt/c` in WSL).
- Run Bash and the usual command-line tools (`grep`, `sed`, `awk`, `vim`, `tmux`), and the Linux builds of languages such as Python, Node.js, Go, Rust and C/C++.
- Install software with the distribution's own package manager, and run services with systemd.
- Run Linux commands from a macOS terminal, with pipes in both directions: `git log | msl -e wc -l`.
- Reach a server in a distribution at `localhost` on macOS.
- Open folders inside a distribution from VS Code, like VS Code's WSL extension on Windows. See [Get started with VS Code]({{< relref "/docs/tutorials/msl-vscode" >}}).

Some things WSL does aren't available: running macOS programs from Linux, GUI apps, GPU access and x86_64 distributions. [Comparing MSL and WSL]({{< relref "/docs/overview/compare-wsl" >}}) lists the differences.

MSL is open source. See [MSL open source code]({{< relref "/docs/overview/opensource" >}}).

## How MSL runs Linux

MSL runs a Linux kernel in one lightweight utility VM, using only Apple's Virtualization.framework. Each distribution runs inside that VM with its own `init` and its own mount, PID, UTS and cgroup namespaces, as in WSL 2. The distributions share the VM's kernel, memory, CPUs and network, so they have one IP address and one `localhost` between them.

Because a distribution is a set of namespaces rather than a VM of its own, starting one doesn't boot a VM. An idle distribution stops after 15 seconds, and the VM stops 60 seconds after the last distribution does, handing its memory back to macOS. `msld` itself stays running, idle, until you log out.

On macOS, `msl` talks to `msld`, a per-user service that the first `msl` command starts. `msld` runs the VM and keeps the list of distributions. MSL installs no kernel extension or login item; launchd starts `msld` on demand through a LaunchAgent. [How MSL works]({{< relref "/docs/concepts/how-it-works" >}}) goes into more detail.

MSL is an independent project. It isn't affiliated with or endorsed by Microsoft or Apple.
