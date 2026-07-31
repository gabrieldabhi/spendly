#!/usr/bin/env python
"""Script to seed a realistic Indian user into the database."""

import sqlite3
import random
from werkzeug.security import generate_password_hash
from datetime import datetime

# Indian first and last names from different regions
INDIAN_FIRST_NAMES = [
    'Rahul', 'Priya', 'Amit', 'Ananya', 'Vikram', 'Sneha', 'Rohit', 'Pooja',
    'Arjun', 'Kavita', 'Sameer', 'Meera', 'Nitin', 'Shreya', 'Manoj', 'Divya',
    'Sachin', 'Rashi', 'Deepak', 'Isha', 'Rajesh', 'Aarti', 'Kiran', 'Swati',
    'Anil', 'Neha', 'Sunil', 'Ekta', 'Vijay', 'Manisha', 'Sanjeev', 'Pallavi',
    'Gautam', 'Rani', 'Harsh', 'Nidhi', 'Kartik', 'Anjali', 'Dinesh', 'Bhavya',
    'Prakash', 'Sonia', 'Mukesh', 'Tina', 'Jignesh', 'Hina', 'Bhavesh', 'Kajal',
    'Chetan', 'Monalisa', 'Paresh', 'Shital', 'Alok', 'Dipika', 'Rajiv', 'Anita',
    'Suresh', 'Lata', 'Mahesh', 'Geeta', 'Pụnu', 'Rina',
]

INDIAN_LAST_NAMES = [
    'Sharma', 'Patel', 'Gupta', 'Mehta', 'Desai', 'Verma', 'Reddy', 'Kumar',
    'Singh', 'Yadav', 'Jain', 'Bhatt', 'Shah', 'Nair', 'Chopra', 'Malhotra',
    'Agarwal', 'Varma', 'Dubey', 'Pandey', 'Srivastava', 'Misra', 'Bansal', 'Das',
    'Jha', 'Iyer', 'Iyengar', 'Shenoy', 'Pai', 'Rao', 'Nambiar', 'Menon',
    'Pillai', 'Kaur', 'Chauhan', 'Rathod', 'Meena', 'Solanki', 'Choudhary', 'Thakur',
    'Dabhi', 'Parmar', 'Trivedi', 'Oza', 'Vora', 'Khadia',
]


def get_random_indian_name():
    """Generate a random Indian first + last name."""
    first = random.choice(INDIAN_FIRST_NAMES)
    last = random.choice(INDIAN_LAST_NAMES)
    return f"{first} {last}"


def generate_email(name):
    """Generate email from name with random 2-3 digit suffix."""
    # Extract first and last name
    parts = name.split()
    if len(parts) >= 2:
        first = parts[0].lower()
        last = parts[-1].lower()
    else:
        first = parts[0].lower()
        last = "user"

    # Random 2-3 digit number
    suffix = random.randint(10, 999)

    return f"{first}.{last}{suffix}@gmail.com"


def email_exists(db, email):
    """Check if email already exists in users table."""
    cursor = db.execute('SELECT COUNT(*) FROM users WHERE email = ?', (email,))
    count = cursor.fetchone()[0]
    return count > 0


def generate_unique_user(db):
    """Generate a unique Indian user that doesn't exist in the database."""
    while True:
        name = get_random_indian_name()
        email = generate_email(name)

        if not email_exists(db, email):
            return {
                'name': name,
                'email': email,
                'password_hash': generate_password_hash('password123'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }


def main():
    # Connect to the database (same as in db.py)
    db_path = 'expense_tracker.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')

    try:
        # Ensure users table exists
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

        # Generate unique user
        user = generate_unique_user(conn)

        # Insert user
        cursor = conn.execute(
            'INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
            (user['name'], user['email'], user['password_hash'], user['created_at'])
        )

        user_id = cursor.lastrowid
        conn.commit()

        print(f"User seeded successfully:")
        print(f"  id: {user_id}")
        print(f"  name: {user['name']}")
        print(f"  email: {user['email']}")

    finally:
        conn.close()


if __name__ == '__main__':
    main()
