---
title: MSL documentation
layout: hextra-home
---

{{< hextra/hero-headline >}}
Modern Subsystem for Linux
{{< /hextra/hero-headline >}}

{{< hextra/hero-subtitle >}}
Linux distributions on macOS, the way WSL runs them on Windows
{{< /hextra/hero-subtitle >}}

<div class="hx:mt-6 hx:mb-6 hx:flex hx:flex-wrap hx:gap-2">
{{< hextra/hero-button text="Install MSL" link="docs/install/install" >}}
{{< hextra/hero-button text="What is MSL?" link="docs/overview/about" >}}
</div>

```console
$ msl --install Ubuntu        # Microsoft's WSL image for arm64
$ msl                         # a shell in Ubuntu, in the macOS directory you're in
$ msl -l -v
  NAME            STATE           VERSION
* Ubuntu          Running         2
```

<div class="hx:mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="The wsl.exe command line"
    subtitle="Same arguments, output and exit codes. Scripts and READMEs written for WSL work with msl."
    link="docs/overview/basic-commands" >}}
  {{< hextra/feature-card
    title="WSL's distribution images"
    subtitle="Ubuntu, Debian, Fedora and more, unmodified, with their own first-run setup and /etc/wsl.conf."
    link="docs/how-to/use-custom-distro" >}}
  {{< hextra/feature-card
    title="Files both ways"
    subtitle="macOS files at /mnt/macos in Linux; each distribution's files in Finder."
    link="docs/concepts/filesystems" >}}
  {{< hextra/feature-card
    title="One localhost"
    subtitle="A server in a distribution answers on localhost on macOS. DNS goes through macOS, so VPNs work."
    link="docs/concepts/networking" >}}
  {{< hextra/feature-card
    title="VS Code"
    subtitle="Open folders inside a distribution, like VS Code's WSL extension on Windows."
    link="docs/tutorials/msl-vscode" >}}
  {{< hextra/feature-card
    title="Apple native"
    subtitle="One lightweight VM on Apple's Virtualization.framework. Apple silicon, macOS 26 or later."
    link="docs/concepts/how-it-works" >}}
{{< /hextra/feature-grid >}}
