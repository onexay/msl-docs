---
title: Security model
weight: 6
description: What MSL runs where, what Linux and macOS can reach of each other, and how to verify a release and report a vulnerability.
---

MSL runs Linux distributions in one lightweight virtual machine on behalf of one macOS user. This page describes the boundaries that set, what each side can reach, and the known weak spots.

## What runs where

- `msl` and its service, `msld`, run as your macOS user, never as root. `msld` holds one entitlement, `com.apple.security.virtualization`, which Virtualization.framework needs to start a VM. The two processes `msld` starts to carry data, `msl-portd` (forwarded ports) and `msl-fileviewd` (`~/.msl/distros`), also run as your user and hold no entitlements.
- The Linux kernel and every distribution run inside the VM. Root in a distribution is root in that distribution's namespaces, not on macOS.
- Installing MSL needs no administrator rights, unless you choose a system prefix such as `/usr/local`. MSL installs no kernel extension or login item. Its LaunchAgent, `~/Library/LaunchAgents/dev.msl.msld.plist`, runs nothing at login: launchd starts `msld`, as your user, when you first run `msl`.

## Isolation

The VM is the security boundary between Linux and macOS.

Distributions aren't isolated from each other by separate VMs. As in WSL 2, they share one kernel and one network namespace, and each has its own mount, PID, UTS and cgroup namespaces. Treat all your distributions as one trust zone: they share the VM's localhost, and no VM boundary separates one distribution's root from another's.

## What macOS exposes to Linux

By design, every distribution gets:

- the macOS filesystem at `/mnt/macos`, with your macOS user's permissions. Any Linux user in any distribution can read and write what you can;
- name resolution through macOS's resolver;
- outbound network access through NAT.

MSL never runs macOS programs from Linux, and never puts macOS paths on the Linux `PATH`. There's no equivalent of WSL's Windows interop.

## What Linux exposes to macOS

| What | Who can reach it |
|---|---|
| The control socket, `~/Library/Application Support/msl/msld.sock` | Your user only (mode 0600). |
| Streams the VS Code extension opens into a distribution, with `msl --connect` through the control socket | Your user only. A stream reaches a distribution as its default user, to a local TCP port or to a Unix socket under `~/.vscode-server/msl/`; other Unix sockets are refused. |
| Forwarded ports on `127.0.0.1` and `::1` | Every local user on the Mac, as with WSL's localhost forwarding. Nothing is published on other interfaces. Turn forwarding off with `localhostForwarding = false`. |
| Distribution files in `~/.msl/distros` | Your user only; see below. |

### The `~/.msl/distros` file view

Each distribution's files are served to macOS over NFSv3 through a Unix socket in MSL's folder (mode 0600), not a network port. macOS's NFS client connects from the kernel as root, so the socket's permissions alone wouldn't stop another local user from mounting it. MSL therefore checks every NFS call (in `msl-fileviewd`, which carries the files): only calls that carry your user ID or root's (the kernel's own) get through, and a mount is accepted only while `msld` itself is mounting ([#1](https://github.com/onexay/msl/issues/1)). Another local user can't mount the view, and gets an authentication error for anything in your mounts.

{{< callout type="warning" >}}
With `fileViewTransport = tcp` in `~/.mslconfig`, the view is served on a `127.0.0.1` port instead. The same checks apply, but any local program can connect to the port and claim any user ID. Don't use that setting on a Mac that other people log in to.
{{< /callout >}}

## Releases

- Releases are built by CI and signed ad hoc. They aren't notarised yet. `install.sh` removes the quarantine attribute from the files it installs.
- Each release's tarball has a SHA-256 checksum file (`.sha256`). Newer releases also sign it with the release key (`.sha256.asc`). `install.sh` always checks the checksum, and checks the signature when `gpg` is installed. v0.1.1 and other releases without a `.sha256.asc` are verified by the checksum alone.
- If you'd rather not pipe `install.sh` into a shell, read it first: it's short. Or download the release yourself and install it with `--from`; see [Install MSL]({{< relref "/docs/install/install" >}}).

### Verify a release by hand

The release key is `509D 39A8 78FD EBBB CAF7  B715 FA9B 1101 AF64 043C` (RSA 4096, onexay). It's published on [keys.openpgp.org](https://keys.openpgp.org/search?q=509D39A878FDEBBBCAF7B715FA9B1101AF64043C) and at [github.com/onexay.gpg](https://github.com/onexay.gpg).

```console
$ gpg --keyserver hkps://keys.openpgp.org --recv-keys 509D39A878FDEBBBCAF7B715FA9B1101AF64043C
$ gpg --verify msl-<version>-macos-arm64.tar.gz.sha256.asc msl-<version>-macos-arm64.tar.gz.sha256
$ shasum -a 256 -c msl-<version>-macos-arm64.tar.gz.sha256
```

## Supported versions

Only the latest release gets security fixes. Update with `msl --update`.

## Report a vulnerability

Report vulnerabilities privately, with GitHub's **Report a vulnerability** button on the [msl Security tab](https://github.com/onexay/msl/security/advisories/new). Don't open a public issue.

Include the MSL version (`msl --version`), your macOS version and the steps to reproduce. You'll get an acknowledgement within 7 days. Once a fix is released, a GitHub security advisory announces it and credits you, unless you'd rather not be named.
