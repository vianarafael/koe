# Koe

## Quick Start

1. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
2. Create and activate virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize database:
   ```bash
   python scripts/migrate.py
   ```
5. Run development server:
   ```bash
   bash scripts/dev.sh
   ```

## Environment Variables

- `STRIPE_API_KEY`: Your Stripe API key (for future payment features).
- `SECRET_KEY`: Secret key for session and security.
- `DATABASE_URL`: SQLite database URL, default `sqlite:///./app.db`.

## Deployment Rough Guide

- Use `scripts/gunicorn.sh` to run production server.
- Configure systemd service with `deploy/systemd/yourapp.service`.
- Configure Nginx reverse proxy with `deploy/nginx/yourapp.conf`.

## Development Workflow

1. Activate virtual environment.
2. Run `bash scripts/dev.sh` to start server with reload.
3. Edit code and templates.
4. Test endpoints and UI.

## Project Scope

Koe tracks Twitter engagement metrics and scores tweets based on configurable point values.

## Notes

- OAuth 2.0 Twitter authentication backend endpoints scaffolded.
- HTMX used for simple dynamic UI.
- SQLite for local data storage.

