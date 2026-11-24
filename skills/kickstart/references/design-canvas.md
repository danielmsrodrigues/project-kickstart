# Drawing the direction on a Claude Design canvas

Read this in step 3b for origin c (None) at the crafted depth, when your Artifact tool lists the **"Design"** type (a types listing, or `action: "quickstart"` with intent `design`). That type is Claude Design inside Claude: a canvas of artboards the user can see, edit and comment on. Without it, follow `design-research.md` instead.

**Nothing in the repo yet.** The canvas lives on claude.ai, outside the repo, like any drawing before the 3b yes. Draft `PRODUCT.md` in a temporary directory, write the artboards in your scratch folder and publish from there. The repo gets these files in step 4, after the 3b list is confirmed.

**Why this way.** In testing, three directions drawn at once came out average every time, with or without design skills. What worked was one direction on a real page, with photographs chosen one by one, reviewed before the user saw it, and then refined by the user on the canvas.

## 1. The brief

Work from the step 1 design and `docs/PRODUCT.md`. Don't interview again, and don't run a mood board round. If the user gave references, use them. Commit to one direction you can name ("caderno de obra": editorial serif, lime white, one azulejo blue) and say it in one line when you show the canvas.

## 2. Imagery

When the product is something people look at (buildings, spaces, food, objects, people), the page needs photographs.
- **The user's own** first.
- **Otherwise, licensed stand-ins:** Wikimedia Commons under CC0, CC BY or CC BY-SA. Pick each one by looking at it: make 360px thumbnails (`sips -Z 360` on macOS) and read those, not the full files.
- **Check what a stand-in says.** Its subject matches the copy next to it. A before/after pair must look like the same kind of building. Nothing in it contradicts the product (an exit sign in a heritage staircase, a modern office in a "restored" room).
- **Credits** go in a note on the canvas, and later in `docs/DESIGN.md`.
- Never fake a picture with boxes, lines or CSS shapes.

## 3. The canvas

Create it from the Design type: publish with its `type_url` and a title naming the project and the surface. Follow the instructions the create result carries, and read its `format.md` and `craft.md`.
- **Design system:** use one only when the user has one for this product. A system from another of their projects doesn't fit; build your own look and say so.
- **One artboard,** as a page (`"expand": "fill"`): the whole landing page for a site, the main screen for an app.
- **Real copy** in the product's language. Facts the user hasn't given are visibly marked: `[morada]`, or example numbers with an asterisk and a footnote.
- **The key interaction works:** a before/after comparator drags, a booking form shows its sent state.

## 4. Review before showing it

Run these on the local copy of the artboard you published from, before the user sees anything:
1. **impeccable.** Invoke `impeccable:impeccable` with `critique <file>`, saying it runs from source only, in this context, with no sub-agents and no browser. It then flags itself as degraded; that is expected. Also run its detector: `impeccable detect --json <file>`. Read its `craft-floor.md` before editing.
2. **Emil Kowalski.** Invoke `emil-design-eng` on the interactions: buttons, the key interaction, form fields.

3. **Generic defaults and contrast.** The review is the generic-defaults check for this path: impeccable's bans, plus the "Avoid" seed list in `templates/_design-system/DESIGN.md`. Then compute contrast with `python3 <skill>/scripts/build_tokens.py contrast --pairs "FG:BG" ...` for every text and background pair the page uses (add `:3` for borders and focus rings), in each theme it has.

Apply the P0 and P1 findings, impeccable's bans (an eyebrow over a heading, decorative section numbers, overused fonts) and every contrast FAIL. Keep the direction. Publish.

## 5. One look at the rendered page

Some problems only show on the page: a before/after pair that doesn't match, bad crops, images too tall at narrow widths, empty areas.
- The canvas is private on claude.ai. Open it in a browser where the user is signed in: Claude in Chrome. The built-in browser has no claude.ai session.
- Open `<canvas url>#play-Main`, wait for it to load, and take screenshots at 0.5 scale: at 1440 wide, then at the narrowest window (Chrome stops near 600px; say that 390 wasn't checked).
- Fix what you see, publish, and close the tab.
- If the user said the machine is busy (recording, low on memory), skip this look, say so, and leave it to them.

## 6. Show it and let the user refine it

Give the link, one line on the direction, and the list of placeholders and stand-ins. The user refines it on the canvas: editing text and spacing, the Tweaks panel, or comments to Claude. Wait until they approve it. Before importing, read the canvas files again, because the user may have edited them.

## 7. Import into the repo

1. Read `project/canvas.json` and each `project/*.dc.html` (Artifact `read` with `paths`).
2. Take the values for `design/tokens.json`: colors, font families, the type sizes actually used, spacing steps, radii, shadows, and motion durations and curves. Name them by role (`design-system.md`, "2. Tokens"). Run the contrast script again on the draft tokens, because the user may have changed colors on the canvas.
3. Save the approved artboard as `docs/design/direction.dc.html`. In `docs/DESIGN.md`, add the canvas link (`Direction: <link>`) and the photo credits under "References".
4. **Signature components:** pick two or three pieces from the canvas where the product's character lives, such as a before/after comparator, a project gallery or the booking form. They join the six base components, as `design-research.md` section 3 describes.

Then continue with "2. Tokens" in `design-system.md`. These files, `docs/PRODUCT.md` and the signature components go in the 3b file list, and are written in step 4 after its yes.
