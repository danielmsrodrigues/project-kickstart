# Base components: contract

Not an output file. The contract every stack's base components meet; write them in the stack's idiom (the platform file in `platforms/` gives the location and style mechanism). Few and good: these six, nothing else until a screen needs it.

## Rules for all components

- Styles come from tokens only: colors, spacing, radii, sizes (`size.touch-target`, `size.border`, `size.icon`, `size.focus-ring`), type, shadows, durations. Layout keywords and ratios with no design meaning (`100%`, `flex: 1`, `opacity` on disabled) are fine.
- Variation is a prop (`variant`, `size`, `level`), never a copied component (`PrimaryButton`, `BigCard`).
- Each component owns its own states: pressed (and hover on pointer platforms), focus-visible, disabled, and loading or error where listed. Disabled uses the platform's own mechanism where it has one (SwiftUI `.disabled()` environment, the HTML `disabled` attribute).
- Accessible by default: native element or role, label wired up, visible focus (`action.focus`, `size.focus-ring`; on iOS this shows with Full Keyboard Access), touch target from `size.touch-target`, text that scales with the user's text size setting, respects reduced motion.
- No business logic, no data fetching, no app-specific copy.

## The six

| Component | Must support | Notes |
|-----------|--------------|-------|
| Button | `variant` (primary, secondary, ghost, danger), `size` (sm, md), `disabled`, `loading` | Loading keeps the width and blocks repeat presses. Uses `color.action.*`, `action.primary-active` for hover/pressed, `ink.on-action` and `ink.on-danger`. |
| Input | label (required), `hint`, `error`, `size`, `disabled` | Error text is linked to the field for assistive tech and uses `color.ink.danger`, plus words, never color alone. |
| Card | `variant` (plain, raised), `padding` (a spacing token) | A container, not a layout system. Interactive cards are a variant only when a screen needs one. |
| Text | `variant` (body, muted, small) | Maps to the type scale; inherits color from tokens. |
| Heading | `level` (1-3) | Semantic level and visual size come from the scale; display family if the tokens define one. |
| Stack | `direction` (vertical, horizontal), `gap` (a spacing token), `align` (cross axis: leading/center/trailing for vertical, top/center/bottom for horizontal) | The only way screens add space between components. |

Names follow the stack's convention (`Button.tsx`, `Button.razor`). Where any of the six would clash with a system type (SwiftUI `Button`, `Text`), prefix all six the same way (`DSButton`, `DSText`, `DSCard`, ...) so the set reads as one. Spacing and padding props take a spacing token, not a free number, where the language allows it (an enum of the spacing steps in Swift, a union type in TypeScript).

If the project already has components covering one of these, document that component in the inventory instead of writing a new one.
