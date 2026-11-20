# Showing the design system

A tokens file and a folder of components can't be looked at. Every time the design system is created or changed, end by showing all of it on one page:
the direction and voice, the components, and the tokens (colors in light and dark with their contrast, type, spacing, sizes, radii, shadows, motion).

## Tool version

`design/build_tokens.py` is the plugin's tool, copied into the project. If the project's copy lacks a command or flag used below (`python3 design/build_tokens.py preview --help`), it predates this plugin version. Replace it with `cp <plugin>/skills/kickstart/scripts/build_tokens.py design/build_tokens.py`, and say so in the report. `<plugin>` is two levels above this skill's directory.

## Which form

- **Your Artifact tool offers the "Design System" type** (the format Claude Design uses): build the full system, with cover, brand book, tokens and components with live previews. Follow `claude-design-system.md` and skip the rest of this file except "Tell the user".
- **Otherwise:** generate the page below. It shows the direction, the Avoid list and the tokens. Components are seen in the running app.

## Local page

```bash
python3 design/build_tokens.py preview design/tokens.json --out design/preview.html --title "<Project name> Design System" --design-md docs/DESIGN.md [--css <font stylesheet> ...]
```

- `--css` takes the stylesheets that load the project's fonts, relative to `design/`. With Fontsource that's `../node_modules/@fontsource/<font>/index.css`.
- `design/preview.html` is generated output, and the base `.gitignore` ignores it.

## Published page (no Design System type)

If you can publish an HTML page (an Artifact tool without the Design System type), publish the page there too:
```bash
T=$(mktemp -d) && python3 design/build_tokens.py preview design/tokens.json --out "$T/index.html" --title "<Project name> Design System" --google-fonts --fragment --design-md docs/DESIGN.md
```
Publish `$T/index.html` privately with a generic `icon` such as `palette`. Write the link into `docs/DESIGN.md` as `Preview: <link>`; later runs republish to it.

## Tell the user

End with the link, or the file path when there is no link. Add one line on what it shows. If a part couldn't be made (the component bundle failed, publishing isn't available), say which and why. Never skip it silently.
