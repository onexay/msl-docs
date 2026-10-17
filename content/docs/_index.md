---
title: Documentation
description: Documentation for MSL, the Modern Subsystem for Linux, which runs Linux distributions on macOS the way WSL runs them on Windows.
---

MSL runs Linux distributions on macOS using the same `wsl.exe` commands and distribution images as WSL. Use these guides to install MSL, set up your workflow, and understand how it works.

## Get started

{{< cards >}}
  {{< card link="install/install" title="Install MSL" subtitle="Install MSL and your first Linux distribution." icon="download" >}}
  {{< card link="overview/basic-commands" title="Learn the commands" subtitle="Use the `msl` command just like `wsl.exe`." icon="terminal" >}}
  {{< card link="tutorials/environment" title="Set up a development environment" subtitle="Configure your Linux account, editor, Git and tools." icon="cog" >}}
  {{< card link="overview/about" title="What is MSL?" subtitle="Learn what MSL does and how it runs Linux on macOS." icon="book-open" >}}
{{< /cards >}}

## Set up your workflow

{{< cards >}}
  {{< card link="tutorials/msl-vscode" title="VS Code" subtitle="Open and work in folders inside a distribution." >}}
  {{< card link="tutorials/msl-git" title="Git" subtitle="Configure Git, sign in to GitHub, and choose where repositories live." >}}
  {{< card link="tutorials/msl-database" title="Databases" subtitle="Run PostgreSQL, SQLite, and other databases from Linux." >}}
  {{< card link="tutorials/msl-containers" title="Linux containers" subtitle="Run Docker Engine inside an MSL distribution." >}}
  {{< card link="tutorials/nodejs" title="Node.js" subtitle="Install Node.js and open development servers from macOS." >}}
  {{< card link="tutorials/linux" title="Linux and Bash" subtitle="Learn the Linux command line and shell basics." >}}
  {{< card link="tutorials/gui-apps" title="Linux GUI apps" subtitle="Options for graphical tools alongside your MSL terminal." >}}
  {{< card link="tutorials/gpu-compute" title="GPU compute" subtitle="Current GPU support and alternatives for Mac workloads." >}}
{{< /cards >}}

## Understand MSL

{{< cards >}}
  {{< card link="concepts/how-it-works" title="How MSL works" subtitle="See how MSL runs distributions in a lightweight virtual machine." icon="server" >}}
  {{< card link="concepts/filesystems" title="Files and mounts" subtitle="Understand how macOS and Linux files are shared." icon="folder" >}}
  {{< card link="concepts/networking" title="Networking" subtitle="Learn how localhost, DNS, and distribution networking work." icon="globe-alt" >}}
  {{< card link="concepts/msl-config" title="MSL configuration" subtitle="Configure advanced distribution and VM settings." icon="cog" >}}
  {{< card link="concepts/systemd" title="systemd" subtitle="Run services and use systemd inside a distribution." >}}
  {{< card link="concepts/file-permissions" title="File permissions" subtitle="Understand Linux permissions on shared files." >}}
{{< /cards >}}

## Troubleshoot and update

{{< cards >}}
  {{< card link="faq" title="Frequently asked questions" subtitle="Answers to common questions about MSL." icon="question-mark-circle" >}}
  {{< card link="troubleshooting" title="Troubleshooting" subtitle="Diagnose common installation and runtime problems." icon="support" >}}
  {{< card link="release-notes" title="Release notes" subtitle="See what changed in MSL, the kernel, and the VS Code extension." icon="clipboard-list" >}}
{{< /cards >}}
