---
title: How-to
weight: 5
sidebar:
  open: false
---

Task-focused guides for distributions, disks and scripting.

{{< cards >}}
  {{< card link="use-custom-distro" title="Import any Linux distribution" subtitle="Import an arm64 Linux root filesystem or disk image as an MSL distribution with msl --import, and back up or move distributions with --export." >}}
  {{< card link="build-custom-distro" title="Build a custom distribution" subtitle="Package a Linux distribution as a .wsl image that MSL installs like the ones in Microsoft's list, with its own first-run setup and Finder icon." >}}
  {{< card link="mount-disk" title="Mount a disk in MSL" subtitle="Attach a Linux disk image to MSL's VM with msl --mount, and reach it from every distribution under /mnt/msl." >}}
  {{< card link="connect-usb" title="Connect USB devices" subtitle="USB device passthrough isn't available in MSL; how to reach USB drives and devices instead." >}}
  {{< card link="case-sensitivity" title="Adjust case sensitivity" subtitle="How file name case works in MSL distributions and in macOS files under /mnt/macos, and how to get case-sensitive storage for a project." >}}
  {{< card link="disk-space" title="Manage disk space" subtitle="How MSL stores each distribution on its own sparse disk, and how to check, grow, compact, move, export and import disks." >}}
  {{< card link="json-output" title="Use JSON output in scripts" subtitle="Read MSL's state from scripts, editors and CI with --json on --list, --status and --version." >}}
{{< /cards >}}
