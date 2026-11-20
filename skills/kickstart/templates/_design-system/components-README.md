<!--
Template for the component inventory: <components dir>/README.md (default: components/README.md).
One row per component that exists. Delete this comment block.
-->
# Components

Inventory of the design-system components. **Check here before creating a component.** If something similar exists, add a variant or prop to it instead of creating another.

Update this file in the same commit as any component you add, change or remove.

Styles come only from tokens ([design/tokens.json]({{RELATIVE PATH}})); see [docs/DESIGN.md]({{RELATIVE PATH}}) for when to use what.

| Component | File | Use for | Variants / props |
|-----------|------|---------|------------------|
| Button | `{{PATH}}` | {{Triggering an action}} | `variant`: {{primary, secondary, ghost, danger}} · `size`: {{sm, md}} · `disabled`, `loading` |
| Input | `{{PATH}}` | {{Single-line text entry with label, hint and error}} | `size`: {{sm, md}} · `error`, `hint`, `disabled` |
| Card | `{{PATH}}` | {{Grouping related content on a surface}} | `variant`: {{plain, raised}} · `padding`: spacing token |
| Text | `{{PATH}}` | {{Body copy and labels}} | `variant`: {{body, muted, small}} |
| Heading | `{{PATH}}` | {{Section and page titles}} | `level`: {{1, 2, 3}} |
| Stack | `{{PATH}}` | {{Laying out children in a row or column with a token gap}} | `direction`: {{vertical, horizontal}} · `gap`: spacing token · `align` |

## Adding a component

1. Search this table and the components folder for something close. Prefer a new variant.
2. Build it from tokens and existing components only.
3. Add its row here, in the same commit.
