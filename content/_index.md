---
title: MSL documentation
layout: hextra-home
---

<section class="msl-home-hero">
  <div class="msl-home-copy">
    <p class="msl-home-eyebrow">Linux on macOS</p>
    <h1>Your Linux environment, on Mac.</h1>
    <p class="msl-home-lede">Run the Linux distributions and <code>wsl.exe</code> commands your team already knows, in a lightweight virtual machine built with Apple’s Virtualization framework.</p>
    <div class="msl-home-actions">
      <a class="msl-home-primary" href="docs/install/install">Install MSL <span aria-hidden="true">→</span></a>
      <a class="msl-home-secondary" href="docs/overview/about">Explore the docs</a>
    </div>
    <p class="msl-home-requirements">Apple silicon · macOS 27 or later</p>
  </div>
  <div class="msl-home-terminal" aria-label="Example MSL terminal session">
    <div class="msl-terminal-titlebar">
      <span class="msl-terminal-dots" aria-hidden="true"><i></i><i></i><i></i></span>
      <span>Ubuntu · MSL</span>
      <span class="msl-terminal-state"><i></i> Running</span>
    </div>
    <pre><code><span class="msl-terminal-prompt">$</span> msl --install Ubuntu
<span class="msl-terminal-prompt">$</span> msl
<span class="msl-terminal-comment"># You are now in Ubuntu</span>
<span class="msl-terminal-prompt">$</span> msl -l -v

  NAME       STATE     VERSION
  Ubuntu     Running   2</code></pre>
  </div>
</section>

<section class="msl-home-capabilities">
  <p class="msl-home-eyebrow">A familiar Linux workflow</p>
  <h2>Work across Mac and Linux without changing your tools.</h2>

  {{< hextra/feature-grid cols="3" >}}
    {{< hextra/feature-card
      title="The wsl.exe command line"
      subtitle="Same arguments, output, and exit codes. Use the scripts and READMEs your team already has."
      link="docs/overview/basic-commands" >}}
    {{< hextra/feature-card
      title="Your Linux distributions"
      subtitle="Use Ubuntu, Debian, Fedora, and other WSL images with their normal first-run setup."
      link="docs/how-to/use-custom-distro" >}}
    {{< hextra/feature-card
      title="Files both ways"
      subtitle="Open Mac files from Linux and browse distribution files in Finder."
      link="docs/concepts/filesystems" >}}
    {{< hextra/feature-card
      title="One localhost"
      subtitle="Reach services running in Linux from Mac apps, with DNS routed through macOS."
      link="docs/concepts/networking" >}}
    {{< hextra/feature-card
      title="VS Code and friends"
      subtitle="Open folders inside a distribution from VS Code, Insiders, VSCodium, or Cursor."
      link="docs/tutorials/msl-vscode" >}}
    {{< hextra/feature-card
      title="Built on Apple virtualization"
      subtitle="Run distributions in one lightweight VM on Apple silicon."
      link="docs/concepts/how-it-works" >}}
  {{< /hextra/feature-grid >}}
</section>
