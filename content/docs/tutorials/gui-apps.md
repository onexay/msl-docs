---
title: Run Linux GUI apps
weight: 7
description: MSL doesn't run Linux GUI apps. How to work with graphical tools from a distribution instead.
---

MSL doesn't run Linux GUI apps. It has no equivalent of WSLg, so X11 and Wayland programs in a distribution have no display to open windows on.

## Alternatives

- **Web interfaces.** A server in a distribution that listens on `localhost` is reachable at `localhost` on macOS. Open tools with a web UI, such as Jupyter or a dev server, in a macOS browser. See [Networking]({{< relref "/docs/concepts/networking" >}}).
- **VS Code.** Edit, debug and browse files in the distribution from VS Code on macOS. See [Get started using VS Code with MSL]({{< relref "/docs/tutorials/msl-vscode" >}}).
- **macOS apps on Linux files.** Open files in the distribution with macOS apps through `~/.msl/distros/<distro>` in Finder. See [Working across file systems]({{< relref "/docs/concepts/filesystems" >}}).
