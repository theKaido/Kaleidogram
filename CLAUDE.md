# CLAUDE.md

## Overview

Web application that allows restaurant owners to generate QR codes which, once scanned by their customers, display the list of allergens present in each dish.

Product goal: help restaurant owners comply with their legal obligations to display allergens on the premises.

## Working mode

This is a learning project. Priority is deep understanding by the author, not delivery speed.

**Rules for Claude Code:**

1. Socratic mode by default. Ask questions and suggest directions. The author writes the code.
2. Do NOT write or modify code without an explicit request, including boilerplate (Vite config, package.json, Dockerfile, etc.).
3. For business logic or architecture, make the author reason first. Never implement before they have thought it through.
4. If a code generation request would skip an important learning, flag it and propose a pedagogical alternative.
5. Signal shortcuts that would cost in understanding or add technical debt.
6. No flattery. Direct feedback. Correct misunderstandings bluntly.

## License

Released under the GNU Affero General Public License v3.0 (AGPL-3.0), as a learning project and open source contribution.

## Tech stack

- Backend: FastAPI + SQLAlchemy + PostgreSQL, JWT authentication with OAuth2 password flow
- Frontend: React + TypeScript + Vite
- Database: PostgreSQL locally for dev, Supabase planned for production deployment
- Containerization: Docker and Docker Compose for the dev environment
- CI/CD: GitHub Actions for tests and builds

## Git workflow

This project follows the Gitflow branching model.

- `main` branch: stable version only, protected
- `develop` branch: default integration branch, protected
- `feature/xxx` branches: one per feature, branched off `develop` and merged back via Pull Request
- Any change requires a PR, even when working solo
- The CI must be green before merging
- Manually review the diff before every merge

## Technical discipline

- Systematic testing: pytest on the backend, Vitest + React Testing Library on the frontend
- One feature = one branch = associated tests
- Docker from day one, not added at the end of the project
- README kept up to date on every major stack or behavior change
- Explicit commits, conventional commits recommended (feat:, fix:, test:, docs:, refactor:)

## Current state

Backend FastAPI started on the `develop` branch, around 35 commits. Frontend to be created. LICENSE and full README to be added. CI to be configured.

## Project resources

- **Repo**: https://github.com/theKaido/allergene_qr_generator
- **Author**: Jonny MATHANARUBAN (theKaido)
- **Contact**: jonnymthdev@gmail.com
