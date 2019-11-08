import sqlite3
from app.server.context import config

insert_new_url_query = "INSERT INTO urls (base_url, tiny_url) VALUES (?, ?)"
create_table_query = "CREATE TABLE IF NOT EXISTS urls (base_url TEXT PRIMARY KEY, tiny_url TEXT)"


def get_connection(db_path=config['db']['db_path']):
    con = sqlite3.connect(db_path)
    return con


def init_if_not_exists():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_query)


def insert_new_url(base_url, tiny_url):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(insert_new_url_query, base_url, tiny_url)
