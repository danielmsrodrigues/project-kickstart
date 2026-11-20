# Crafted design direction: research, three directions, signature pieces

Read this in step 3b when the user chose the crafted depth. It replaces the single text proposal of origin (c). It may also refine a direction from origin (a) or (b) when the user asks. The goal is a direction a design team would sign off: grounded in real references, chosen from options the user has *seen*, and carried into the product's own pieces.

## 1. Research (a mood board, not a copy)

**What to search: three layers, not just the niche.** Searching only the product's niche ("barbershop app") returns that niche's clichés, the very thing to avoid. Build queries in three layers:

| Layer | Searches for | Example (a barbershop booking app) | Gives |
|-------|--------------|------------------------------------|-------|
| The job, any industry | the flow and the key screen, by what it does | "booking app", "appointment scheduling", "time slot picker", "service selection" | patterns that work: Mobbin, Dribbble |
| The tone, neighboring worlds | brands and places with the same personality, in other trades | "heritage brand identity", "Lisbon signage", "old café branding", "hand-painted lettering" | colors, type, texture |
| The niche, to check only | what the niche already does | "barbershop website" | what to avoid, and where to stand out; never the main source |

Most references come from the first two layers.

**Where.** Spread the queries across these sources, using what each is good for:

| Source | Good for |
|--------|----------|
| dribbble.com (search), behance.net | Visual directions, color, illustration. Many shots are concepts that would not survive real use: take mood, not layouts. |
| mobbin.com | Real apps in production: flows that work (booking, checkout, schedules) |
| godly.website, awwwards.com, land-book.com, siteinspire.com | Modern, well-made websites |
| fontsinuse.com | Type pairings in real projects |
| The product's physical world | Shopfronts, packaging, signage, uniforms, menus. Often the most distinctive source. |

**How.**
- **With a browser tool** (Claude in Chrome, the built-in browser): open the search result pages and look at the thumbnails in screenshots, 20 to 40 in all, then open the 6 to 10 best.
- **Without one:** use web search and fetch, and say plainly that the research worked from descriptions, not images, so it's weaker.
- Respect each site: no sign-ins, no scraping beyond the pages you'd read, and stop at a login wall or CAPTCHA (move to another source).

**Keep 6 to 8 references.** For each one, record the link, what it is, and the one thing to take from it, phrased as a principle: "a single saturated accent on a neutral ground", "condensed display numerals for times", "cards cut like paper tickets". Never take a whole layout, an illustration, a logo or a distinctive mark. Drop references that only show trends unrelated to this product.

**Get the user's reaction before drawing anything.** Show the mood board as images where you can, or else as links, each with what you'd take from it. Then ask, with the question tool when you have one, which references they like and which they don't (multi-select). Taste is visual, and words alone don't capture it. The directions build on what they picked and leave out what they rejected.

**Don't start the directions before the research and this reaction are in.** A direction drafted while the research runs comes from the model's defaults, not from the references.

## 2. Three directions, drawn

Make **three directions that genuinely differ**, each a different answer to the brief rather than three tints of one idea. For each:
- a name and one sentence;
- the 4 to 6 core colors with roles;
- the type pair;
- radius and density;
- the one bold move;
- which references it draws on.

Each direction must pass the generic-defaults check in `design-system.md` and the contrast script (`contrast --pairs`) before it's shown.

**Draw them.** Write one HTML page, outside the repo, that renders the **same real screen of the app** three times, side by side or stacked, one per direction. Pick the screen where the brand shows most, such as choosing a service and time, or the order summary. Use real copy in the app's language, plain HTML and CSS with each direction's values, and Google Fonts. Load `frontend-design` if available while writing it.
- **Publishing:** if you can publish HTML (Artifact tool), publish it privately and give the link. Otherwise give the file path.
- **Visual self-review:** with a browser tool, open it and take one screenshot. Check it against the generic defaults and your own direction sentences. Fix what reads as template, once, before showing it.

Then ask, with buttons when the question tool exists: which direction (A, B or C), or a mix ("B's colors with A's type"). The chosen direction becomes the token values in step 2 of `design-system.md`.

Then save the result in the repo, as part of the confirmed file list:
- the chosen direction's drawing at `docs/design/direction.html`: the visual reference for building the real screens, which keeps the look from being lost between this step and the implementation;
- the references in `docs/DESIGN.md` under "References", each with its link and what was taken from it;
- a line in `docs/DESIGN.md` pointing at `docs/design/direction.html`.

## 3. Signature components

Besides the six base components, pick the **two or three pieces where the product's character lives**, such as an order ticket, a time-slot picker or a week planner. Add them to the confirmed file list as components:
- with props and variants;
- in the inventory;
- in the component contract's rules (tokens only, states, accessibility).

Design them from the chosen direction and its references. They are what makes the design system recognizably this product's.

## Cost

This depth costs roughly twice the plain step: the research, one drawn page and two or three extra components. The plain depth skips sections 1 to 3.
