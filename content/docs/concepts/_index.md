---
title: Concepts
weight: 4
sidebar:
  open: false
---

How MSL works across macOS and Linux: files, settings, networking and services.

{{< cards >}}
  {{< card link="filesystems" title="Working across file systems" subtitle="Where to keep files, how macOS and Linux see each other's files, and how to mix macOS and Linux commands with MSL." >}}
  {{< card link="msl-config" title="Advanced settings configuration" subtitle="Configure the MSL VM with ~/.mslconfig and each distribution with /etc/wsl.conf, the same files and keys WSL uses." >}}
  {{< card link="file-permissions" title="File access and permissions" subtitle="How Linux permissions and ownership work on macOS files under /mnt/macos, and on distribution files seen from macOS in ~/.msl/distros." >}}
  {{< card link="networking" title="Networking considerations" subtitle="How MSL distributions reach the network, share localhost with macOS, resolve names through macOS, and reach servers on the Mac." >}}
  {{< card link="systemd" title="Use systemd to manage services" subtitle="Turn on systemd in an MSL distribution, manage services with systemctl, and keep services running when no terminal is open." >}}
  {{< card link="how-it-works" title="How MSL works" subtitle="The parts of MSL, how distributions share one lightweight VM, when things start and stop, and where MSL keeps its state on macOS." >}}
{{< /cards >}}
