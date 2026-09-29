---
title: Use JSON output in scripts
weight: 7
description: Read MSL's state from scripts, editors and CI with --json on --list, --status and --version.
---

WSL's commands print text meant for people. MSL prints the same text, and adds `--json` to its query commands so scripts don't have to parse tables. This is an MSL addition; without `--json`, the output is exactly `wsl.exe`'s.

| Command | JSON |
|---|---|
| `msl --list --json` (with `--all`, `--running`, `--verbose` or `--quiet`) | installed distributions |
| `msl --list --online --json` | distributions available to install |
| `msl --status --json` | the default distribution, and the VM's state and settings |
| `msl --version --json` | MSL, kernel and macOS versions |

`--json` can go anywhere among these options (`msl -l -v --json`) or first (`msl --json --status`). Other commands, such as `--install` or `--shutdown`, reject it: their exit code tells you whether they worked. A `--json` after a Linux command belongs to that program: `msl -e jq --json …`.

## Examples

These use [`jq`](https://jqlang.org) on macOS.

```console
$ msl -l --json | jq -r '.distributions[] | select(.default) | .name'
Ubuntu
$ msl -l --running --json | jq '.distributions | length'
1
$ msl --status --json | jq '.vm.running'
true
$ msl --version --json | jq -r .kernel
6.18.15-msl-21f0ec7
```

Check for a distribution before installing it:

```sh
if ! msl -l --json 2>/dev/null | jq -e '.distributions[] | select(.name == "Debian")' >/dev/null; then
  msl --install Debian --no-launch
fi
```

## Conventions

- **One object on stdout**, ending with a newline: pretty-printed on a terminal, compact when piped, keys sorted.
- **`"schema": 1`** at the top level. It changes only for breaking changes. New fields can appear at any time, so ignore fields you don't know.
- **camelCase field names.** A field with no known value is left out rather than set to `null`. For example, `uptimeMs` is missing when the VM is stopped.
- **Raw numbers:** sizes in bytes, times in milliseconds. A timeout of `-1` means "never".
- **Exit codes are `wsl.exe`'s.** `--json` changes the format, never the exit code. `msl --list --json` with nothing installed fails with exit code 255, as `wsl --list` does. With nothing running, `--running --json` prints an empty list and exits 0.
- **Errors go to stderr** as a JSON object, and stdout stays empty. The `code` is always included:

  ```json
  {"error": {"code": "Msl/Service/MSL_E_DEFAULT_DISTRO_NOT_FOUND", "message": "Modern Subsystem for Linux has no installed distributions.\n…"}, "schema": 1}
  ```

## `msl --list --json`

```json
{
  "distributions": [
    {"default": true, "id": "0f2b9f9d-00b0-407f-8d90-6a6a7fa65dbc", "name": "Debian", "state": "Running", "version": 2}
  ],
  "schema": 1
}
```

`state` is `Running` or `Stopped`. `--running` and `--all` filter the list; `--verbose` and `--quiet` make no difference.

## `msl --list --online --json`

```json
{
  "distributions": [
    {"architectures": ["arm64", "x86_64"], "default": true, "emulated": false, "friendlyName": "Ubuntu", "name": "Ubuntu"}
  ],
  "schema": 1
}
```

The list holds the distributions MSL can install on this Mac. `default` marks the one `msl --install` picks when you don't name one.

## `msl --status --json`

```json
{
  "defaultDistribution": "Debian",
  "defaultVersion": 2,
  "schema": 1,
  "vm": {
    "pendingChanges": [],
    "running": true,
    "settings": {
      "dnsTunneling": true,
      "instanceIdleTimeoutMs": 15000,
      "kernel": "6.18.15-msl (bundled)",
      "kernelCommandLine": "console=hvc0 ip=dhcp net.ifnames=0 loglevel=4",
      "localhostForwarding": true,
      "memoryBytes": 19327352832,
      "processors": 12,
      "vmIdleTimeoutMs": 60000
    },
    "settingsFile": "/Users/you/.mslconfig",
    "settingsFileExists": true,
    "uptimeMs": 2517
  },
  "warnings": []
}
```

- `vm.settings` is what the running VM booted with, or, when it's stopped, what the next start will use.
- `vm.pendingChanges` lists `~/.mslconfig` changes that apply after `msl --shutdown`, such as `{"setting": "memoryBytes", "from": "8589934592", "to": "4294967296"}`.
- `warnings` holds the `~/.mslconfig` problems that text mode prints to stderr.

See [Advanced settings configuration]({{< relref "/docs/concepts/msl-config" >}}) for the settings themselves.

## `msl --version --json`

```json
{"commit": "3af5916", "kernel": "6.18.15-msl-76f230e", "macos": "27.0.0", "msl": "0.1.7", "prefix": "/Users/you/.local", "schema": 1}
```

`msl` is the plain version, for comparing; the text output adds the commit (`0.1.7+3af5916`). `commit` ends in `.dirty` for a build with uncommitted changes. `prefix` is where MSL is installed, and is missing for a development build.
