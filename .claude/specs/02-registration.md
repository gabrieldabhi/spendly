# Spec: Registration

## Overview

Implement the backend logic for user registration. The `/register` route already exists as a GET endpoint rendering `register.html` with a complete form. This step adds the POST handler to process form submissions, validate input, hash passwords with werkzeug, insert new users into the database, and redirect to the login page on success. This is the first authentication feature and enables users to create accounts before they can track expenses.

## Depends on

- Step 01: Database Setup (database schema, `get_db()`, `init_db()`, `seed_db()` already implemented)
- The `users` table must exist with columns: `id`, `name`, `email` (UNIQUE), `password_hash`, `created_at`

## Routes

- `GET /register` — renders registration form (already exists)
- `POST /register` — processes form submission, creates user account — public access

## Database changes

No database changes. The `users` table already exists with the required schema from Step 01.

## Templates

- **Modify:** `templates/register.html` — already exists with form and error display. No changes needed unless validation messages need adjustment.

## Files to change

- `app.py` — add POST handler for `/register`, import `generate_password_hash` from `werkzeug.security`, import `get_db` from `database.db`

## Files to create

- None

## New dependencies

No new dependencies. Use:
- `werkzeug.security.generate_password_hash` (already in requirements.txt)
- `sqlite3` (standard library)

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with werkzeug's `generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for all internal links in templates
- Return `render_template()` for HTML pages (not raw strings)
- Use `abort()` for HTTP errors
- Form validation: check for empty fields, valid email format, password minimum length (8 chars), duplicate email
- On validation error: re-render `register.html` with error message
- On success: redirect to `/login` with a success message (can use flash or query param)

## Definition of done

- [ ]  `POST /register` route exists in `app.py`
- [ ]  Form submission validates: name not empty, email format valid, password >= 8 chars
- [ ]  Duplicate email shows error "Email already registered"
- [ ]  Password is hashed using `generate_password_hash` before storage
- [ ]  New user inserted into `users` table with parameterized query
- [ ]  On success, redirects to `/login`
- [ ]  On validation error, re-renders `register.html` with error message
- [ ]  App starts without errors
- [ ]  Can register a new user via the web form
- [ ]  New user can then log in (tested in next step)

---