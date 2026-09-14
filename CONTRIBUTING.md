# Contributing to Kaléidogram

Thanks for your interest in contributing. This document describes how to set up the project locally and the conventions used in this repository.

## Prerequisites

- **Python**: 3.14 (used in the project's local dev virtual environment). No version is pinned via `pyproject.toml` or `.python-version` in the repo yet — 3.11+ should work given the dependency set, but 3.14 is what's actually been used and tested.
- **PostgreSQL**: no specific version is pinned in the repo. Any recent PostgreSQL version (14+) should work.
- **Node.js**: not applicable yet. The frontend (React + Vite + TypeScript) has not been initialized. This section will be updated once it exists.

The project has a `docker-compose.yaml` at the repo root (backend + PostgreSQL). This is the recommended way to run the project locally — see [Docker setup](#docker-setup) below. A direct/local setup without containers is also documented further down for reference.

## Docker setup

Prerequisites: Docker and Docker Compose (Docker Desktop on macOS/Windows).

1. Clone the repository:

   ```bash
   git clone git@github.com:theKaido/kaleidogram.git
   cd kaleidogram
   ```

2. Create a `.env` file at the repo root (next to `docker-compose.yaml`) with the following variables:

   ```bash
   POSTGRES_USER=<user>
   POSTGRES_PASSWORD=<password>
   POSTGRES_DB=<db-name>
   JWT_SECRET_KEY=<your-secret-key>
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. Start the stack:

   ```bash
   docker compose up
   ```

   This builds the backend image, starts PostgreSQL (with a healthcheck gating backend startup), runs Alembic migrations, then starts the dev server with `--reload`. The `backend/` folder is bind-mounted into the container, so code changes on the host are picked up live.

The API is then available at `http://localhost:8000` (`/docs` for the interactive Swagger UI).

To rebuild the image after changing `pyproject.toml`/`poetry.lock` or the `Dockerfile`:

```bash
docker compose build backend
docker compose up
```

To reset the database (wipes all data):

```bash
docker compose down -v
```

## Local setup (without Docker)

1. Clone the repository:

   ```bash
   git clone git@github.com:theKaido/kaleidogram.git
   cd kaleidogram/backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv python_venv
   source python_venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Make sure PostgreSQL is running locally. If you don't have a running instance, start one, for example:

   ```bash
   pg_ctl -D /usr/local/var/postgres start
   createdb kaleidogram
   ```

5. Create your local environment file. There is no `.env.example` committed yet — create `backend/.env` manually with the following variables (all read via `os.getenv` in the codebase):

   ```bash
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/kaleidogram
   JWT_SECRET_KEY=<your-secret-key>
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. Apply database migrations:

   ```bash
   alembic upgrade head
   ```

7. Run the dev server:

   ```bash
   uvicorn app.main:app --reload
   ```

The API is then available at `http://127.0.0.1:8000`.

## Project structure

```
kaleidogram/
├── CLAUDE.md              # Shared project context
├── README.md
├── backend/
│   ├── CLAUDE.md          # Backend-specific conventions
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/           # Database migrations
│   │   └── versions/
│   └── app/
│       ├── main.py        # FastAPI entry point
│       ├── database.py    # SQLAlchemy setup
│       ├── dependencies/  # FastAPI dependencies (auth, DB session)
│       ├── models/        # SQLAlchemy models
│       ├── routers/       # API endpoints, one module per resource
│       ├── schemas/       # Pydantic schemas (validation/serialization)
│       └── utils/         # Security helpers (password hashing, JWT)
└── frontend/               # Not initialized yet (React + Vite + TypeScript planned)
```

## Git workflow

This project follows Gitflow:

- `main`: production-ready code only, protected.
- `develop`: default integration branch. Feature/fix branches target this branch.
- Branch naming: `feat/xxx`, `fix/xxx`, `docs/xxx`, `chore/xxx`, branched off `develop`.

Every change goes through a Pull Request, even for solo work on this repo.

## Commit convention

Commits follow [Conventional Commits](https://www.conventionalcommits.org/).

Examples:

```
feat: add JWT authentication on password update endpoint
fix: correct type of sub claim from int to str
docs: add project structure to CLAUDE.md
chore: add python-dotenv dependency
refactor: extract CurrentUser dependency from auth router
```

## Pull request process

1. Open the PR against `develop`, not `main`.
2. Write a clear description: what changed and why, not just what.
3. Make sure the CI is green before requesting review (once CI is configured).
4. As the project gains contributors, at least one review will be required before merge. Until then, a self-review of the diff is expected before merging.

## Code style

- **SQLAlchemy**: sync mode with the classic `Session` pattern, no async DB access.
- **Pydantic**: v2 syntax (`model_config = ConfigDict(...)`, `field_validator`).
- **Type hints**: required on all function signatures.
- **Python naming**: snake_case for variables, functions, files, and modules (PEP 8).
- **URL naming**: kebab-case in API paths (e.g. `/plat-ingredient`).
- **Imports**: absolute imports from `app.` (e.g. `from app.models.plat import Plat`).
- **Docstrings**: on public functions and classes when behavior isn't obvious from the signature.

No automated linter or formatter (Ruff, Black, ESLint) is configured in this repo yet. Follow the conventions above by hand until tooling is added.

See [`backend/CLAUDE.md`](backend/CLAUDE.md) for the source of truth on these conventions.

## Running tests

Tests suite to be added. There is currently no `tests/` directory, `pytest.ini`, or `conftest.py` in the repo.

## Reporting issues

Use [GitHub Issues](https://github.com/theKaido/kaleidogram/issues).

When filing a bug report, include:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, PostgreSQL version)

When filing a feature request, include:

- The problem you're trying to solve
- The proposed solution, if you have one
- Any alternatives you considered