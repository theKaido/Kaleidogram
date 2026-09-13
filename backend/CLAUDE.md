# CLAUDE.md

## Coding conventions

- **SQLAlchemy**: sync mode with the classic `Session` pattern. No async DB access.
- **Pydantic**: v2 syntax. Use `model_config = ConfigDict(...)` and `field_validator`, not the v1 `class Config` / `@validator` style.
- **Type hints**: required on all function signatures (parameters and return types).
- **Python naming**: snake_case for variables, functions, files, and modules, following PEP 8.
- **URL naming**: kebab-case in API paths (`/plat-ingredient`, not `/plat_ingredient`), following REST conventions.
- **Imports**: absolute imports from `app.` (e.g. `from app.models.plat import Plat`).
- **Docstrings**: on public functions and classes when the behavior is not obvious from the signature.

## Commands

### Backend

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run the dev server
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Database migrations (Alembic)
alembic revision --autogenerate -m "description"   # Create a new migration
alembic upgrade head                                # Apply migrations
alembic downgrade -1                                # Roll back one migration
```

## Structure du projet

```
allergene_qr_generator/
├── CLAUDE.md
├── .gitignore
└── backend/
    ├── requirements.txt
    ├── alembic.ini
    ├── alembic/                    # Migrations de base de données
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions/
    └── app/
        ├── main.py                 # Point d'entrée FastAPI
        ├── database.py             # Configuration SQLAlchemy
        ├── dependencies/           # Dépendances FastAPI (auth, DB)
        │   ├── auth.py
        │   └── database.py
        ├── models/                 # Modèles SQLAlchemy (tables)
        │   ├── allergene.py
        │   ├── allergeneingredient.py
        │   ├── auth.py
        │   ├── ingredient.py
        │   ├── plat.py
        │   ├── platingredient.py
        │   └── restaurant.py
        ├── routers/                # Endpoints FastAPI par ressource
        │   ├── allergene.py
        │   ├── allergene_ingredient.py
        │   ├── auth.py
        │   ├── ingredient.py
        │   ├── plat.py
        │   ├── plat_ingredient.py
        │   └── restaurant.py
        ├── schemas/                # Schémas Pydantic (validation/sérialisation)
        │   ├── allergene.py
        │   ├── allergene_ingredient.py
        │   ├── auth.py
        │   ├── ingredient.py
        │   ├── plat.py
        │   └── restaurant.py
        └── utils/
            └── security.py         # Hachage mot de passe, JWT
```