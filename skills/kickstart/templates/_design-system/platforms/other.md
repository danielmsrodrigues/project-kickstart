<!-- Not an output file. Read only the platform you are building for. Paths are defaults; an existing project's layout wins. Commands run from the repo root. -->

## Other UI stacks

Flutter, Android Compose, desktop toolkits: use the `--ts` or `--css` output as a reference, write the equivalent theme by hand, and say so in DESIGN.md. Contributing a generator is welcome.

## Component libraries

If the project uses a component library (MUI, Chakra, shadcn/ui, Vuetify, MudBlazor, Fluent UI, Syncfusion, Radzen, ...), its components are the base set: don't wrap every one of them.

- Feed the tokens into the library's own theme API (theme object, CSS variables or theme file), generated from or pointing at the token output. Check the library's docs for the current API; don't fork its CSS.
- Write a base component only where the library has no equivalent.
- The inventory lists the library components the project uses, with the variants allowed.

**Any stack:** `python3 design/build_tokens.py check <dirs> [--allow GLOB ...]` reports, outside token files and ignoring comments:
- hex, `rgb()`/`hsl()`, and primitives used directly (`--color-palette-*`)
- Tailwind arbitrary values (`p-[13px]`, `bg-[#…]`) and default palette classes
- px/rem literals on spacing, radius, size and type properties in CSS and style objects
- SwiftUI color literals and system colors, number literals in padding/spacing/frame/corner radius/line width/line spacing, literal font sizes and system text styles

It exits 1 when it finds any, and 2 when a path does not exist.
