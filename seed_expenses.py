#!/usr/bin/env python
"""Script to seed expenses for a user."""

import sqlite3
import random
import sys
from datetime import datetime, timedelta
import calendar

# Category configuration with weights, amount ranges, and Indian descriptions
CATEGORIES = [
    ('Food', 0.30, 50, 800, [
        'Grocery shopping', 'Restaurant dinner', 'Lunch at office canteen',
        'Breakfast', 'Vegetables and fruits', 'Dairy products',
        'Snacks', 'Tea and coffee', 'HomeDelivery order', 'Sweet shop'
    ]),
    ('Transport', 0.15, 20, 500, [
        'Auto rickshaw fare', 'Bus fare', 'Metro ticket',
        'Petrol for bike', 'Taxi ride', 'Ola/Uber cab',
        'Train ticket', 'Parking charges'
    ]),
    ('Bills', 0.15, 200, 3000, [
        'Electricity bill', 'Mobile recharge', 'Internet bill',
        'DTH recharge', 'Gas cylinder', 'Water bill',
        'House rent', 'Maintenance charges'
    ]),
    ('Health', 0.10, 100, 2000, [
        'Medicine purchase', 'Doctor consultation', 'Hospital bills',
        'Dental checkup', 'Eye checkup', 'Gym membership',
        'Yoga classes', 'Ayurvedic treatment'
    ]),
    ('Entertainment', 0.10, 100, 1500, [
        'Movie tickets', 'Concert tickets', 'Amusement park entry',
        'Streaming subscription', 'Books purchase', 'board Games',
        'Weekend outing'
    ]),
    ('Shopping', 0.15, 200, 5000, [
        'Clothing purchase', 'Footwear', 'Electronics',
        'Furniture', 'Kitchen utensils', 'Home appliances',
        'Gifts', 'Cosmetics'
    ]),
    ('Other', 0.05, 50, 1000, [
        'Miscellaneous expense', 'Donation', 'Tips',
        'Stationery', 'Repairs', 'Subscriptions'
    ]),
]


def parse_args():
    """Parse command line arguments."""
    if len(sys.argv) < 4:
        print("Usage: /seed-expenses <user_id> <count> <months> Example: /seed-expenses 1 50 6")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
        count = int(sys.argv[2])
        months = int(sys.argv[3])
        return user_id, count, months
    except ValueError:
        print("Usage: /seed-expenses <user_id> <count> <months> Example: /seed-expenses 1 50 6")
        sys.exit(1)


def verify_user(db, user_id):
    """Verify user exists in database."""
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return user is not None


def generate_expenses(user_id, count, months):
    """Generate random expenses."""
    expenses = []
    today = datetime.now()

    # Calculate start date (today - months)
    start_date = today - timedelta(days=months * 30)

    # Pre-compute category weights for efficient selection
    categories, weights = zip(*[(cat[0], cat[1]) for cat in CATEGORIES])

    for _ in range(count):
        # Select category based on weights
        category = random.choices(categories, weights=weights, k=1)[0]

        # Find the category config
        cat_config = None
        for c in CATEGORIES:
            if c[0] == category:
                cat_config = c
                break

        # Generate random date within the past <months> months
        random_days = random.randint(0, months * 30)
        expense_date = today - timedelta(days=random_days)
        date_str = expense_date.strftime('%Y-%m-%d')

        # Generate amount (rupees)
        min_amt, max_amt = cat_config[2], cat_config[3]
        amount = round(random.uniform(min_amt, max_amt), 2)

        # Generate description
        descriptions = cat_config[4]
        description = random.choice(descriptions)

        expenses.append({
            'user_id': user_id,
            'amount': amount,
            'category': category,
            'date': date_str,
            'description': description
        })

    return expenses


def main():
    user_id, count, months = parse_args()

    # Connect to database
    db_path = 'expense_tracker.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')

    try:
        # Verify user exists
        if not verify_user(conn, user_id):
            print(f"No user found with id {user_id}.")
            return

        # Ensure expenses table exists
        conn.execute('''
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
        conn.commit()

        # Generate expenses
        expenses = generate_expenses(user_id, count, months)

        # Insert all in a single transaction
        try:
            for expense in expenses:
                conn.execute(
                    'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                    (expense['user_id'], expense['amount'], expense['category'],
                     expense['date'], expense['description'])
                )
            conn.commit()

            # Print confirmation
            print(f"{count} expenses inserted.")

            # Calculate date range
            dates = [e['date'] for e in expenses]
            date_range = f"{min(dates)} to {max(dates)}"
            print(f"Date range: {date_range}")

            # Print sample of 5 records
            print("\nSample of 5 records:")
            for expense in expenses[:5]:
                print(f"  Amount: Rs {expense['amount']}, Category: {expense['category']}, "
                      f"Date: {expense['date']}, Description: {expense['description']}")

        except Exception as e:
            conn.rollback()
            print(f"Error inserting expenses: {e}")
            sys.exit(1)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
