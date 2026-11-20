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
