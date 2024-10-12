import sqlite3
from flask import g

db_path = 'data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(db_path)
        g._database = db
    return db

def init_db():
    db = get_db()
    with db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS pdfs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                owner TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS maps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                owner TEXT NOT NULL
            )
        ''')

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()