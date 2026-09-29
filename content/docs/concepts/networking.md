---
title: Networking considerations
weight: 4
description: How MSL distributions reach the network, share localhost with macOS, resolve names through macOS, and reach servers on the Mac.
---

The MSL VM reaches the network through macOS using NAT, like WSL 2's default networking mode. All distributions share one network namespace: they have the same IP address, and one `localhost` between them.

## Identify IP addresses

Every distribution has the same address, on the VM's network interface `eth0`:

```console
$ ip -4 addr show eth0          # in any distribution
```

The Mac, seen from Linux, is the VM's default gateway. MSL adds it to each distribution's `/etc/hosts` as `host.internal`:

```console
$ ip route show default         # in the distribution: "default via <Mac's address>"
$ getent hosts host.internal
```

You rarely need either address: use `localhost` from macOS, and `host.internal` from Linux.

## localhost

A server that listens on `localhost`, or on all addresses, in any distribution answers on `localhost` on macOS, over IPv4 and IPv6:

```console
$ python3 -m http.server 8000      # in a distribution
$ curl http://localhost:8000       # on macOS
```

MSL watches the TCP ports that Linux programs listen on and opens the same ports on macOS's `127.0.0.1` and `::1`. Forwarding stops when the program stops listening. UDP isn't forwarded.

- **Port already in use on macOS.** If a macOS program already uses the port, MSL skips it and logs it in `~/Library/Application Support/msl/msld.log`. Stop the macOS program, or use another port in Linux.
- **Other users on the Mac.** Forwarded ports are on the Mac's loopback address, so any user logged in to the same Mac can connect to them, as with WSL's localhost forwarding.
- **Turning it off.** Set `localhostForwarding = false` in `~/.mslconfig`, then run `msl --shutdown`. See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config#main-settings" >}}).

Forwarded ports are for connections from the Mac itself. MSL doesn't expose distribution ports to other machines on your network.

## Reach a server on the Mac from Linux

Use `host.internal`:

```console
$ curl http://host.internal:3000    # a server running on macOS, from a distribution
```

The macOS server must listen on an address the VM can reach, not only on `127.0.0.1`, and the macOS firewall must allow the connection.

## DNS

Name lookups go through macOS's own resolver, so they give the same answers as on the Mac: VPNs with split DNS, custom resolvers in `/etc/resolver`, `.local` names and entries in the Mac's `/etc/hosts` all work. Each distribution's `/etc/resolv.conf` points at a small resolver inside the VM, `10.255.255.254`, which forwards to macOS. This is WSL's `dnsTunneling`, and it's on by default.

- To use the VM network's DNS server instead, set `dnsTunneling = false` in `~/.mslconfig`.
- To manage `/etc/resolv.conf` yourself, set `generateResolvConf = false` under `[network]` in the distribution's `/etc/wsl.conf`.

## Hostname and /etc/hosts

A distribution's hostname is the Mac's host name, with any characters Linux doesn't allow replaced. MSL writes `/etc/hostname` and `/etc/hosts` each time the distribution starts. `/etc/hosts` contains `localhost`, the hostname, `host.internal`, and the entries from the Mac's own `/etc/hosts`, except its loopback ones.

In `/etc/wsl.conf`, `[network] hostname` sets another hostname, and `generateHosts = false` keeps your own `/etc/hosts` and `/etc/hostname`, as in WSL.

## Not available

- **Mirrored networking.** WSL's `networkingMode = mirrored`, which gives Linux the host's own network interfaces, isn't supported. MSL uses NAT only.
- **Other networking modes and settings.** `networkingMode`, `firewall`, `autoProxy` and the other WSL networking keys in `.wslconfig` are accepted and ignored.
