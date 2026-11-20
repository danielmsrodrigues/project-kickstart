# Sync mode

Use when the project already has `design/tokens.json` and the user brings a new export (Claude Design, Figma, a tokens file) or asks to sync the design system. For reading the export, see `design-import.md`.

1. **Candidate.** Convert the new source into a candidate tokens file in a temporary location, with the same extraction and names as the existing file. Keep a token's name when its role is the same. A rename is a removal plus an addition.
2. **Diff.** Run `python3 design/build_tokens.py diff design/tokens.json <candidate>`. It prints added (`+`), removed (`-`) and changed (`~`) tokens, plus tokens that change only through an alias, with each token's CSS and code names.
3. **Usages.** Search the codebase once for every changed or removed token, in all the forms it takes:
   - the dotted name (`action.primary`), as in DESIGN.md
   - the CSS variable (`--color-action-primary`)
   - the code name (`actionPrimary`)
   - with Tailwind, the utility suffix (`action-primary`, as in `bg-action-primary`)

   List the affected components from the inventory.
4. **Blockers.** Removed tokens that are still in use are blockers; list each with `file:line`. On the web nothing fails at build time, because Tailwind drops the class silently. In Swift and TypeScript it is a compile error.
5. **Component changes** the export implies (new components, variants), checked against the inventory: extend before adding.
6. **Wait for a yes** (buttons when available). Apply only what's approved: `tokens.json`, rebuild, components, DESIGN.md, inventory.
7. **Verify.** Removed tokens' forms have zero hits. `check`, lint and build pass. Offer a commit; don't make one unasked.
