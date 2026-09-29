# Contributing to the MSL docs

The site is organised like Microsoft's [WSL documentation](https://learn.microsoft.com/en-us/windows/wsl/): the same sections in the same order (Overview, Install, Tutorials, Concepts, How-to, Security, FAQ, Troubleshooting, Release notes), and where a WSL page has a counterpart, the same kind of page with similar headings. Someone who knows the WSL docs should find the MSL page in the same place. The text is our own. Don't copy WSL's wording.

Product behaviour is specified by the code in [onexay/msl](https://github.com/onexay/msl). Document what MSL does today. If you aren't sure MSL does something, check the code or try it; don't describe it from what WSL does.

## Build and preview

You need [Hugo](https://gohugo.io/installation/) (extended, 0.146 or later) and Go, for the [Hextra](https://imfing.github.io/hextra/) theme module.

```console
$ hugo server          # http://localhost:1313/msl-docs/
$ hugo --minify        # what CI builds; a broken relref fails it
```

## Pages

- One Markdown file per page under `content/docs/<section>/`. The file name is the URL slug; reuse WSL's slug when there's a matching page (`basic-commands`, `filesystems`, `disk-space`).
- Front matter: `title`, `weight` (order in the sidebar), and `description`, one sentence used in search and link previews.
- Start with one or two sentences that say what the page covers. No "In this article" lists.
- Link to other pages with `relref`, so links survive moves and broken ones fail the build: `[Networking]({{< relref "/docs/concepts/networking" >}})`, `[localhost]({{< relref "/docs/concepts/networking#localhost" >}})`.
- Where WSL has a feature MSL doesn't (GPU, GUI apps, USB devices), keep the page, say plainly that it isn't available, and give the alternative or the tracking issue.

## Style

- **MSL** in prose (like WSL), `msl` only for the command. **macOS**, not "Mac OS" or "OSX"; "the Mac" for the machine.
- Plain, short sentences. Lead with what the reader does or gets. No marketing words ("seamless", "blazing", "powerful").
- Commands in `console` blocks with a `$ ` prompt. Say whether a command runs on macOS or inside a distribution when it isn't obvious; comments after `#` are fine.
- Use the WSL term in parentheses the first time it helps: "`/mnt/macos` (like `/mnt/c` in WSL)".
- Callouts only for things that lose data or break a setup: `{{< callout type="warning" >}}…{{< /callout >}}`. Use `type="info"` sparingly.
- Tables for options and settings; key, default, meaning.
- Link GitHub issues as `[#48](https://github.com/onexay/msl/issues/48)`.

## Commits

Sign off every commit (`git commit -s`, [DCO](https://developercertificate.org/)), as in msl.
