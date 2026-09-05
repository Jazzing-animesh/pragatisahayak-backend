# PragatiSahayak Backend

Flask foundation for an AI business advisory platform serving rural Indian entrepreneurs.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the Flask API server (port 8080 in the managed preview)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `python -m app.seed.seed_locations` — seed locations from `artifacts/api-server`
- `python -m app.seed.seed_schemes` — seed government schemes from `artifacts/api-server`
- `python -m app.seed.seed_categories` — seed business categories from `artifacts/api-server`
- Required env: `DATABASE_URL` (SQLite by default; PostgreSQL is supported when configured)

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Flask 3.1 with Flask-CORS and Flask-SQLAlchemy
- DB: SQLite by default, PostgreSQL supported through SQLAlchemy
- Validation: shared Python validators in `artifacts/api-server/app/utils`
- Runtime: Python 3.11

## Where things live

- `artifacts/api-server/app/__init__.py` — Flask application factory and database initialization
- `artifacts/api-server/app/models/` — SQLAlchemy models and serialization methods
- `artifacts/api-server/app/seed/` — idempotent location, scheme, and category seed scripts
- `artifacts/api-server/app/utils/validators.py` — request validation helpers
- `artifacts/api-server/app/routes/health.py` — foundation health endpoint

## Architecture decisions

- The Flask service is the active API runtime; the existing TypeScript scaffold remains in place for compatibility with the generated workspace.
- SQLite is the default local database so the foundation runs without provisioning PostgreSQL.
- Seed scripts stop when their table already contains data, making repeated setup safe.

## Product

The backend foundation provides rural location context, business-category economics, government financing schemes, competitor records, and user password hashing for the advisory product.

## User preferences

No additional user preferences have been recorded.

## Gotchas

- Run seed modules from `artifacts/api-server` so Python resolves the `app` package correctly.
- The managed API preview routes `/api/health` to the Flask health blueprint.

## Pointers

- See the `pnpm-workspace` skill for workspace structure and package details.
