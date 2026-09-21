# CLAUDE.md

## Stack

- React 19 + TypeScript + Vite 8
- Node 24 (LTS), the version used by `frontend/Dockerfile`. Vite requires `^20.19.0` or `>=22.12.0`, ESLint requires `^20.19.0`, `^22.13.0` or `>=24`.
- ESLint 10 with `typescript-eslint`, `eslint-plugin-react-hooks` and `eslint-plugin-react-refresh`
- Tests: Vitest + React Testing Library (planned, not installed yet)

## Coding conventions

- **Props typing**: every component types its props. Implicit `any` is an error in `tsc` (TS7031 on untyped destructured props). ESLint does not catch it, `npm run build` does.
- **Type-only imports**: `verbatimModuleSyntax` is enabled, so types are imported with `import type` or an inline `type` modifier (`import { useState, type Dispatch } from 'react'`).
- **Erasable syntax only**: `erasableSyntaxOnly` is enabled, so no `enum`, `namespace` or constructor parameter properties.
- **Unused code**: `noUnusedLocals` and `noUnusedParameters` are enabled, remove dead code instead of leaving it.
- **Formatting**: no formatter is configured yet. Keep the indentation of the file you edit.

Decisions not made yet (do not assume, ask the author): folder organization (by type or by feature), styling approach, routing library, API client / where `fetch` calls live, where the JWT is stored, file naming and test location.

## Commands

```bash
# Install dependencies from package-lock.json (exact versions)
cd frontend
npm ci

# Run the dev server (http://localhost:5173)
npm run dev

# Lint
npm run lint

# Type check + production build (output in dist/, git-ignored)
npm run build

# Type check only
npx tsc -p tsconfig.app.json --noEmit
```

With Docker, `docker compose up` at the repo root starts the frontend on `http://localhost:5173` (the `frontend/` folder is bind-mounted, so changes are picked up live). After changing `package.json`, `package-lock.json` or the `Dockerfile`, rebuild and renew the anonymous `node_modules` volume:

```bash
docker compose up --build -V frontend
```

Dependency management is done via npm (`package.json` + `package-lock.json`). Add a runtime dependency with `npm install <package>`, a dev-only dependency with `npm install -D <package>`, and commit the updated lock file.

## Structure du projet

```
frontend/
├── CLAUDE.md
├── Dockerfile
├── .dockerignore
├── package.json
├── package-lock.json
├── vite.config.ts
├── eslint.config.js
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── index.html
├── public/
│   └── favicon.svg
└── src/
    ├── main.tsx                    # Point d'entrée React
    ├── App.tsx                     # Composant racine
    └── index.css
```
