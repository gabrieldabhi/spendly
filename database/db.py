import sqlite3
from flask import current_app, g
from werkzeug.security import generate_password_hash
import datetime


def get_db():
    """Get a SQLite database connection with row_factory and foreign keys enabled.

    Returns a database connection that:
    - Has row_factory set to sqlite3.Row for dictionary-like access
    - Has foreign keys enabled via PRAGMA
    - Reuses connection if already exists in flask g
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config.get('DATABASE', 'expense_tracker.db')
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


def init_db():
    """Create all tables using CREATE TABLE IF NOT EXISTS.

    Creates the following tables:
    - users: stores user registration and authentication data
    - expenses: stores expense records linked to users
    """
    db = get_db()

    # Create users table
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create expenses table
    db.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    db.commit()


def seed_db():
    """Insert sample data for development.

    Adds sample demo user and 8 sample expenses for testing and development purposes.
    Only inserts data if tables are empty.
    """
    db = get_db()

    # Check if users table is empty
    user_count = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]

    if user_count == 0:
        # Hash the demo password
        password_hash = generate_password_hash('demo123')

        # Insert demo user
        db.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            ('Demo User', 'demo@spendly.com', password_hash)
        )

        # Get demo user ID
        user_id = db.execute(
            'SELECT id FROM users WHERE email = ?', ('demo@spendly.com',)
        ).fetchone()['id']

        # Get current month and year
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month

        # Generate dates spread across current month
        # Using different days to spread out the dates
        dates = [
            f"{current_year}-{current_month:02d}-01",
            f"{current_year}-{current_month:02d}-05",
            f"{current_year}-{current_month:02d}-10",
            f"{current_year}-{current_month:02d}-12",
            f"{current_year}-{current_month:02d}-15",
            f"{current_year}-{current_month:02d}-18",
            f"{current_year}-{current_month:02d}-22",
            f"{current_year}-{current_month:02d}-25",
        ]

        # Insert 8 sample expenses across all 7 categories (Food appears twice)
        expenses = [
            (user_id, 50.00, 'Food', 'Grocery shopping', dates[0]),
            (user_id, 25.50, 'Transport', 'Bus fare', dates[1]),
            (user_id, 120.00, 'Bills', 'Electricity bill', dates[2]),
            (user_id, 75.00, 'Health', 'Medicine purchase', dates[3]),
            (user_id, 40.00, 'Entertainment', 'Movie tickets', dates[4]),
            (user_id, 150.00, 'Shopping', 'Clothing purchase', dates[5]),
            (user_id, 30.00, 'Food', 'Restaurant dinner', dates[6]),
            (user_id, 20.00, 'Other', 'Miscellaneous expense', dates[7]),
        ]

        db.executemany(
            'INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)',
            expenses
        )

        db.commit()
        print("Database seeded with demo user and 8 sample expenses!")
    else:
        print("Database already contains data, skipping seed.")
