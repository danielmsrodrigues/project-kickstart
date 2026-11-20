<!--
Template for docs/DESIGN.md. Fill from the design-system step (source, answers, or the
existing system). Every value named here must exist in design/tokens.json (or, for an
existing system, in its real token source). Name tokens; don't copy their values here,
so a sync can't leave stale numbers behind. Delete sections that would hold a guess.
Delete this comment block.
-->
# Design

**Direction:** {{ONE SENTENCE: the aesthetic direction, specific to this product and its users, e.g. "Calm, paper-like reading tool for night-shift nurses: low contrast at rest, one sharp accent for what needs action now."}}

Source of truth: [`design/tokens.json`]({{RELATIVE PATH}}) → generated {{LIST OF GENERATED FILES, e.g. `src/styles/tokens.css`}} with `{{BUILD_TOKENS_COMMAND}}`. Never edit generated files by hand.
Components: [{{COMPONENTS_DIR}}/README.md]({{RELATIVE PATH}}).
{{ORIGIN LINE, e.g. "Imported from a Claude Design handoff on YYYY-MM-DD; external tools are import sources, not the source of truth."}}

## Tokens

| Group | Tokens | Use for |
|-------|--------|---------|
| Color: surface | {{e.g. `surface.base`, `surface.raised`}} | {{Page and container backgrounds}} |
| Color: ink | {{...}} | {{Text and icons, including on-action and danger}} |
| Color: action | {{...}} | {{Interactive elements and their states (hover, focus) only; never decoration}} |
| Color: edge | {{...}} | {{Borders and dividers}} |
| Spacing | {{step names, e.g. `1x` … `10x` (multiples of the 4px base)}} | {{Gaps, padding, margins. Nothing in between.}} |
| Size | {{touch-target, icon, border, focus-ring, content-max}} | {{Fixed dimensions components share}} |
| Radius | {{...}} | {{Which elements get which radius, by hierarchy}} |
| Type | {{families, size scale, weights}} | {{Roles: body, display, numerals...}} |
| Motion | {{durations}} | {{...}} |

{{THEMES: light/dark or other modes, and how they switch (system setting, data-theme attribute, trait collection).}}

## Layout

- {{GRID / COLUMN RULE; max content width from `size.content-max`}}
- {{ALIGNMENT RULE: left-aligned, centered, when}}
- {{DENSITY: how much breathing room, where spacing gets larger}}
- {{RESPONSIVE / SIZE-CLASS BEHAVIOUR}}

## Motion

- {{WHEN MOTION IS USED (usually: to answer a user action or show what changed) AND WHEN NOT}}
- Respect reduced-motion settings.

## Accessibility floor

- Text contrast meets WCAG AA in every theme ({{note any token pair checked}}).
- Visible focus state on every interactive component.
- Touch targets at least {{44pt / 44px}}.

## Avoid

{{FILL FROM THE DIRECTION. Name the generic defaults this product must not fall into, concretely, as values or patterns. Seed list to adapt (keep what applies, add product-specific ones, and take the current calibration list from the frontend-design skill when it is installed):}}

- {{A default palette chosen for no reason (e.g. the stock cream-and-terracotta or black-and-neon look) instead of one from this product's world}}
- {{One radius and one soft grey shadow on every element regardless of hierarchy}}
- {{Content chopped into identical cards; gradient washes as decoration}}
- {{Template chrome: all-caps eyebrow labels over every heading, "→" appended to every link, numbered markers on content that is not a sequence}}
- {{Entrance animations on every section; hover effects on every card}}
- {{Hardcoded values in screens. Every color, size, spacing and radius comes from a token.}}
