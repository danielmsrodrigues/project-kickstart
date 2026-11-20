# Stack: Node.js + TypeScript

Defaults only. Commands found in `package.json` scripts and the lockfile win.

## Commands

| Purpose | Default |
|---------|---------|
| Install | `npm install` (pnpm: `pnpm install`, yarn: `yarn`, bun: `bun install`) |
| Build | `npm run build` |
| Test | `npm test` |
| Single test | `npm test -- <path>` |
| Lint | `npm run lint` |
| Format | `npm run format` |
| Type-check | `npm run typecheck` (script running `tsc --noEmit`) |
| Run | `npm run dev` or `npm start` |

## Scaffold (empty repo)

Both scaffolders refuse a non-empty directory: run them in a temporary directory and move the result in (see `references/scaffolding.md`). Always pass a relative name (`app`) from inside that directory: create-vite treats an absolute path such as `/var/folders/.../app` as relative and scaffolds into `./var/folders/...` under the current directory. Neither installs or runs git with these flags.

| Building | Command (run inside the temporary directory `<tmp>`; the project lands in `<tmp>/app`) |
|----------|-----------------------------------------|
| Single-page app (React, Vue, Svelte, Solid, Preact, Lit, vanilla) | `cd <tmp> && npx --yes create-vite@latest app --template <react-ts\|vue-ts\|svelte-ts\|solid-ts\|preact-ts\|lit-ts\|vanilla-ts> --no-interactive --no-immediate`; add `--eslint` for React, otherwise create-vite sets up Oxlint |
| Full-stack React app (server rendering, API routes) | `cd <tmp> && npx --yes create-next-app@latest app --ts --tailwind --eslint --app --src-dir --use-npm --skip-install --disable-git --yes` |
| CLI or library | No scaffolder: write `package.json` (`"type": "module"`, `build`/`test`/`lint` scripts) and `tsconfig.json` by hand, and list them as `create` lines |

Then `npm install`. create-vite has no test runner: add `npm install -D vitest` and a `"test": "vitest run"` script. Tailwind v4 with Vite: `npm install -D tailwindcss @tailwindcss/vite`, add `tailwindcss()` to `plugins` in `vite.config.ts`, and make the CSS entry start with `@import "tailwindcss";`. The scaffold's demo styles (`src/index.css`, `src/App.css`) are full of literal colors: replace them when the design system is wired in.


## Conventions

- `"strict": true` in `tsconfig.json`; no `any` without a comment saying why.
- ES modules (`"type": "module"`) unless the project already uses CommonJS.
- Source in `src/`, tests next to the code as `*.test.ts` (or in `test/` if the project already does that).
- Files in kebab-case, types and classes in PascalCase, functions and variables in camelCase.
- One package manager per repo; commit its lockfile.

## Don'ts

- Don't edit generated output (`dist/`, `build/`) by hand.
- Don't mix package managers or commit more than one lockfile.

## Permissions

Allow the exact scripts used in `CLAUDE.md`. Replace `npm run` with the detected package manager. No `npx`/`pnpm dlx` entries: they can download and run packages.
