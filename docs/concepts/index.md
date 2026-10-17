---
title: Concepts
sidebar_position: 4
---

How MSL works across macOS and Linux: files, settings, networking and services.

<CardGrid>
  <Card title="Working across file systems" href="/docs/concepts/filesystems/" description="Where to keep files, how macOS and Linux see each other's files, and how to mix macOS and Linux commands with MSL." />
  <Card title="Advanced settings configuration" href="/docs/concepts/msl-config/" description="Configure the MSL VM with ~/.mslconfig and each distribution with /etc/wsl.conf, the same files and keys WSL uses." />
  <Card title="File access and permissions" href="/docs/concepts/file-permissions/" description="How Linux permissions and ownership work on macOS files under /mnt/macos, and on distribution files seen from macOS in ~/.msl/distros." />
  <Card title="Networking considerations" href="/docs/concepts/networking/" description="How MSL distributions reach the network, share localhost with macOS, resolve names through macOS, and reach servers on the Mac." />
  <Card title="Use systemd to manage services" href="/docs/concepts/systemd/" description="Turn on systemd in an MSL distribution, manage services with systemctl, and keep services running when no terminal is open." />
  <Card title="How MSL works" href="/docs/concepts/how-it-works/" description="The parts of MSL, how distributions share one lightweight VM, when things start and stop, and where MSL keeps its state on macOS." />
</CardGrid>
