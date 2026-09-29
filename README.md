# MSL documentation

The documentation site for [MSL](https://github.com/onexay/msl), the Modern Subsystem for Linux: Linux distributions on macOS, the way WSL runs them on Windows.

It's organised like Microsoft's [WSL documentation](https://learn.microsoft.com/en-us/windows/wsl/), so each topic is where a WSL user expects it. It's built with [Hugo](https://gohugo.io/) and the [Hextra](https://imfing.github.io/hextra/) theme.

```console
$ hugo server          # preview at http://localhost:1313/msl-docs/
```

The site isn't published yet. CI builds it on every push and uploads the result as an artifact.

[CONTRIBUTING.md](CONTRIBUTING.md) covers the page layout and writing style. Report problems with MSL itself in [onexay/msl](https://github.com/onexay/msl/issues), and problems with these pages here.

## Licence

Apache-2.0 ([LICENSE](LICENSE)). MSL is an independent project, not affiliated with or endorsed by Microsoft or Apple.
