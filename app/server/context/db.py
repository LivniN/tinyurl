import sqlite3

from app.server.context import config, log

insert_new_url_query = "INSERT INTO urls (base_url, tiny_url) VALUES (?, ?)"
create_table_query = "CREATE TABLE IF NOT EXISTS urls (base_url TEXT UNIQUE , tiny_url TEXT UNIQUE )"
last_insert_rowid = "SELECT max(ROWID) from urls"
get_base_url_query = "SELECT base_url from urls WHERE tiny_url=?"


def get_connection(db_path=config['db']['db_path']):
    con = sqlite3.connect(db_path)
    return con


def init_if_not_exists():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_query)


def get_last_rowid():
    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            return cursor.execute(last_insert_rowid).fetchone()[0]
        except sqlite3.Error as e:
            log.error(f"Database error: {e}")
            raise e
        except Exception as e:
            log.error(f"Exception in query: {e}")
            raise e


def insert_new_url(base_url, tiny_url):
    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(insert_new_url_query, (base_url, tiny_url))
        except sqlite3.Error as e:
            log.error(f"Database error: {e}")
            raise e
        except Exception as e:
            log.error(f"Exception in query: {e}")
            raise e


def get_base_url(tiny_url):
    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            try:
                return cursor.execute(get_base_url_query, (tiny_url,)).fetchone()[0]
            except TypeError:
                return None
        except sqlite3.Error as e:
            log.error(f"Database error: {e}")
            raise e
        except Exception as e:
            log.error(f"Exception in query: {e}")
            raise e
