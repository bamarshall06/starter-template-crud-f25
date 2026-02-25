import pymysql
import pymysql.cursors
from flask import g
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()


def get_db_config():
    """
    Get database configuration from environment variables.

    Supports two formats:
    1. JAWSDB_URL - Single connection string (Heroku/production)
       Format: mysql://username:password@host:port/database
    2. Separate variables - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME (local dev)

    Returns dict with host, user, password, database, and port.
    """
    jawsdb_url = os.getenv('JAWSDB_URL')

    if jawsdb_url:
        parsed = urlparse(jawsdb_url)
        return {
            'host': parsed.hostname,
            'user': parsed.username,
            'password': parsed.password,
            'database': parsed.path.lstrip('/'),
            'port': parsed.port or 3306
        }

    return {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': 3306
    }


def get_db():
    """
    Get or create database connection for current request.

    Stores connection in Flask's g object for request lifecycle.
    Returns None if connection fails.
    """
    if 'db' in g and g.db is not None and is_connection_open(g.db):
        return g.db

    print("Establishing database connection.")
    try:
        config = get_db_config()
        g.db = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            port=config['port'],
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        print(f"Database connection failed: {e}")
        g.db = None
        return None
    return g.db

def is_connection_open(conn):
    """Check if database connection is still alive."""
    try:
        conn.ping(reconnect=True)
        return True
    except:
        return False


def close_db(exception=None):
    """Close database connection at end of request."""
    db = g.pop('db', None)
    if db is not None:
        print("Closing database connection.")
        db.close()