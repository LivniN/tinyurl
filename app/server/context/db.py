import sqlite3

from app.server.context import config, log, ServerError

insert_new_url_query = "INSERT INTO urls (base_url, tiny_url) VALUES (?, ?)"
create_table_query = "CREATE TABLE IF NOT EXISTS urls (base_url TEXT UNIQUE , tiny_url TEXT UNIQUE )"
last_insert_rowid = "SELECT max(ROWID) from urls"
get_base_url_from_tiny_url_query = "SELECT base_url from urls WHERE tiny_url=?"
get_exists_tiny_url_query = "SELECT tiny_url from urls WHERE base_url=?"


def get_connection(db_path=config['db']['db_path']):
    con = sqlite3.connect(db_path)
    return con


def init_if_not_exists():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_query)


def db_executor(query, args_tuple=tuple()):
    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            return cursor.execute(query, args_tuple)
        except sqlite3.Error as e:
            log.error(f"Database error: {e}")
            raise ServerError
        except Exception as e:
            log.error(f"Exception in query: {e}")
            raise ServerError


def get_last_rowid():
    return db_executor(last_insert_rowid).fetchone()[0]


def insert_new_url(base_url, tiny_url):
    db_executor(insert_new_url_query, (base_url, tiny_url))


def get_exists_tiny_url(base_url):
    result = db_executor(get_exists_tiny_url_query, (base_url,)).fetchone()
    return result[0] if result else None


def get_base_url(tiny_url):
    result = db_executor(get_base_url_from_tiny_url_query, (tiny_url,)).fetchone()
    return result[0] if result else None
