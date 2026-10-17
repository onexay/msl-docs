---
title: How-to
sidebar_position: 5
---

Task-focused guides for distributions, disks and scripting.

<CardGrid>
  <Card title="Import any Linux distribution" href="/docs/how-to/use-custom-distro/" description="Import an arm64 Linux root filesystem or disk image as an MSL distribution with msl --import, and back up or move distributions with --export." />
  <Card title="Build a custom distribution" href="/docs/how-to/build-custom-distro/" description="Package a Linux distribution as a .wsl image that MSL installs like the ones in Microsoft's list, with its own first-run setup and Finder icon." />
  <Card title="Mount a disk in MSL" href="/docs/how-to/mount-disk/" description="Attach a Linux disk image to MSL's VM with msl --mount, and reach it from every distribution under /mnt/msl." />
  <Card title="Connect USB devices" href="/docs/how-to/connect-usb/" description="USB device passthrough isn't available in MSL; how to reach USB drives and devices instead." />
  <Card title="Adjust case sensitivity" href="/docs/how-to/case-sensitivity/" description="How file name case works in MSL distributions and in macOS files under /mnt/macos, and how to get case-sensitive storage for a project." />
  <Card title="Manage disk space" href="/docs/how-to/disk-space/" description="How MSL stores each distribution on its own sparse disk, and how to check, grow, compact, move, export and import disks." />
  <Card title="Use JSON output in scripts" href="/docs/how-to/json-output/" description="Read MSL's state from scripts, editors and CI with --json on --list, --status and --version." />
</CardGrid>
