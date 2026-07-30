# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** is a Flask-based personal expense tracking web application. It's a multi-step educational project where students implement features incrementally. The application allows users to track expenses, view spending patterns, and manage budgets.


## Architecture

```text
spendly/
├── app.py                 # All routes – single file, no blueprints
├── database/
│   └── db.py              # SQLite helpers: get_db(), init_db(), seed_db()
├── templates/
│   ├── base.html          # Shared layout – all templates must extend this
│   └── *.html             # One template per page
├── static/
│   ├── css/
│   │   ├── style.css      # Global styles
│   │   └── landing.css    # Landing-page-only styles
│   └── js/
│       └── main.js        # Vanilla JS only
└── requirements.txt
```

### Where things belong:

- New routes → `app.py` only, no blueprints
- DB logic → `database/db.py` only, never inline in routes
- New pages → new `.html` file extending `base.html`
- Page-specific styles → new `.css` file, not inline `<style>` tags

---

## Code style

- Python: PEP 8, `snake_case` for all variables and functions
- Templates: Jinja2 with `url_for()` for every internal link — never hardcode URLs
- Route functions: one responsibility only — fetch data, render template, done
- DB queries: always use parameterized queries (`?` placeholders) — never f-strings in SQL
- Error handling: use `abort()` for HTTP errors, not bare `return "error string"`

---

## Tech constraints

- **Flask only** — no FastAPI, no Django, no other web frameworks
- **SQLite only** — no PostgreSQL, no SQLAlchemy ORM, no external DB
- **Vanilla JS only** — no React, no jQuery, no npm packages
- **No new pip packages** — work within `requirements.txt` as-is unless explicitly told otherwise
- Python 3.10+ assumed — f-strings and `match` statements are fine

---

## Development Commands

### Setup
```bash
# Create virtual environment (already exists in repo)
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run Flask development server
python app.py
# Server starts on http://localhost:5001 with debug mode

# Or use Flask command
flask --app app run --port 5001 --debug
```

### Testing
```bash
# Run all tests with pytest
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_filename.py

# Run specific test function
pytest tests/test_filename.py::test_function_name
```

------💡

## Implemented vs stub routes

| Route | Status |
|------|--------|
| `GET /` | Implemented — renders `landing.html` |
| `GET /register` | Implemented — renders `register.html` |
| `GET /login` | Implemented — renders `login.html` |
| `GET /logout` | Stub — Step 3 |
| `GET /profile` | Stub — Step 4 |
| `GET /expenses/add` | Stub — Step 7 |
| `GET /expenses/<id>/edit` | Stub — Step 8 |
| `GET /expenses/<id>/delete` | Stub — Step 9 |

**Do not implement a stub route unless the active task explicitly targets that step.**

------

### Test Files Location
Tests will be added to a `tests/` directory (not yet created). Test dependencies included in requirements.txt:
- pytest==8.3.5
- pytest-flask==1.3.0

## Project Conventions

### Flask Routes
- All routes defined in `app.py`
- Route functions return `render_template()` for HTML pages
- Route naming follows the pattern: page name (e.g., `landing`, `register`, `login`)
- Placeholder routes return simple strings and will be implemented with proper templates

### Templates
- Extend `base.html` using `{% extends "base.html" %}`
- Use `{% block title %}` for page titles
- Use `{% block head %}` for page-specific CSS
- Use `{% block content %}` for main page content
- Use `{% block scripts %}` for page-specific JavaScript
- Use `url_for()` for generating URLs to routes and static files

### Static Files
- CSS files in `static/css/`
- JavaScript files in `static/js/`
- Reference in templates using `url_for('static', filename='css/style.css')`

### Database
- SQLite database file: `expense_tracker.db`
- Connection management in `database/db.py`
- Expected functions: `get_db()`, `init_db()`, `seed_db()`
- Foreign keys are enabled
- Row factory is configured

### Git
- Main branch: `main`
- Recent commits follow pattern: `page: description` (e.g., `landing: add youtube modal`)
- Database file (`expense_tracker.db`) is in .gitignore
- Virtual environment (`venv/`) is in .gitignore
- Python cache files (`__pycache__/`, `*.pyc`, `*.pyo`) are in .gitignore

## Implementation Roadmap

Based on git history and placeholder routes, the implementation follows this progression:

1. **Database Setup** - `database/db.py` with SQLite connection, table creation, seeding
2. **Landing Page** - Complete (hero, features, dashboard mockup, YouTube modal)
3. **Legal Pages** - Complete (Terms and Conditions, Privacy Policy)
4. **Authentication** - Register, Login, Logout (templates exist, backend to implement)
5. **User Profile** - Profile page route exists as placeholder
6. **Expense Management** - CRUD operations for expenses (routes exist as placeholders)

## Key Features Implemented

- Responsive navigation bar with brand icon and auth links
- Landing page with hero section, feature cards, CTA section
- Dashboard mockup visualization in landing page
- YouTube video modal with open/close functionality (Escape key support)
- Forms for registration and login (frontend only)
- Terms and Conditions page with styling
- Privacy Policy page with styling

## File Modification Notes

- `app.py` - Contains placeholder routes that need implementation
- `database/db.py` - Empty file, needs database setup code
- `main.js` - Contains YouTube modal functions, will be extended with more JS
- Templates - Registration and login forms need backend form handling

---

## Warnings and things to avoid

- **Never use raw string returns for stub routes** once a step is implemented — always render a template.
- **Never hardcode URLs** in templates — always use `url_for()`.
- **Never put DB logic in route functions** — it belongs in `database/db.py`.
- **Never install new packages** mid-feature without flagging it — keep `requirements.txt` in sync.
- **Never use JS frameworks** — the frontend is intentionally vanilla.
- **`database/db.py` is currently empty** — do not assume helper functions exist until the step that implements them.
- **FK enforcement is manual** — SQLite foreign keys are off by default; `get_db()` must run `PRAGMA foreign_keys = ON` on every connection.
- The app runs on **port 5001**, not the Flask default 5000 — don't change this.

---