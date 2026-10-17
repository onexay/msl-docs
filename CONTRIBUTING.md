# Contributing to the MSL docs

The site is organised like Microsoft's [WSL documentation](https://learn.microsoft.com/en-us/windows/wsl/): the same sections in the same order (Overview, Install, Tutorials, Concepts, How-to, Security, FAQ, Troubleshooting, Release notes), and where a WSL page has a counterpart, the same kind of page with similar headings. Someone who knows the WSL docs should find the MSL page in the same place. The text is our own. Don't copy WSL's wording.

Product behaviour is specified by the code in [onexay/msl](https://github.com/onexay/msl). Document what MSL does today. If you aren't sure MSL does something, check the code or try it; don't describe it from what WSL does.

## Build and preview

You need Node.js 22 or later.

```console
$ npm ci
$ npm start
$ npm run build        # what CI builds; broken links fail the build
```

## Pages

- One Markdown or MDX file per page under `docs/<section>/`. The file name is the URL slug; reuse WSL's slug when there's a matching page (`basic-commands`, `filesystems`, `disk-space`).
- Front matter: `title`, `sidebar_position` (order in the sidebar), and `description`, one sentence used in search and link previews.
- Start with one or two sentences that say what the page covers. No "In this article" lists.
- Link to other pages with relative Markdown links, including the `.md` extension, so Docusaurus can rewrite them and fail the build if a page moves: `[Networking](../concepts/networking.md)`, `[localhost](../concepts/networking.md#localhost)`.
- Use the shared `<CardGrid>` and `<Card>` components on section landing pages.
- Where WSL has a feature MSL doesn't (GPU, GUI apps, USB devices), keep the page, say plainly that it isn't available, and give the alternative or the tracking issue.

## Style

- **MSL** in prose (like WSL), `msl` only for the command. **macOS**, not "Mac OS" or "OSX"; "the Mac" for the machine.
- Plain, short sentences. Lead with what the reader does or gets. No marketing words ("seamless", "blazing", "powerful").
- Commands in `console` blocks with a `$ ` prompt. Say whether a command runs on macOS or inside a distribution when it isn't obvious; comments after `#` are fine.
- Use the WSL term in parentheses the first time it helps: "`/mnt/macos` (like `/mnt/c` in WSL)".
- Use Docusaurus admonitions (`:::warning`, `:::tip`, `:::info`) for short callouts. Reserve warnings for things that lose data or break a setup.
- Tables for options and settings; key, default, meaning.
- Link GitHub issues as `[#48](https://github.com/onexay/msl/issues/48)`.

## Commits

Sign off every commit (`git commit -s`, [DCO](https://developercertificate.org/)), as in msl.
