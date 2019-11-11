import datetime
import sqlite3

from app.server.context import config, log, ServerError

create_tinyurls_table_query = "CREATE TABLE IF NOT EXISTS tinyurls (base_url TEXT UNIQUE , tiny_url TEXT UNIQUE)"
create_stats_table_query = "CREATE TABLE IF NOT EXISTS stats (timestamp TIMESTAMP , action TEXT NOT NULL)"
insert_new_url_query = "INSERT INTO tinyurls (base_url, tiny_url) VALUES (?, ?)"
last_insert_rowid = "SELECT max(ROWID) FROM tinyurls"
get_base_url_from_tiny_url_query = "SELECT base_url FROM tinyurls WHERE tiny_url=?"
get_exists_tiny_url_query = "SELECT tiny_url FROM tinyurls WHERE base_url=?"
count_url_redirection_registrations_query = "SELECT COUNT(*) FROM tinyurls"
insert_data_to_stats_query = "INSERT INTO stats (timestamp, action) VALUES (?, ?)"
get_stats_query = "SELECT action, COUNT(*) FROM stats WHERE timestamp >= ? GROUP BY action"


def get_connection(db_path=config['db']['db_path']):
    try:
        con = sqlite3.connect(db_path)
        return con
    except sqlite3.Error as e:
        log.error(f"Database error: {e}")
        raise ServerError(f"error while trying to connect to db")


def db_executor(query, args_tuple=tuple()):
    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            return cursor.execute(query, args_tuple)
        except sqlite3.Error as e:
            log.error(f"Database error: {e}")
            raise ServerError(f"error while executing query: {query} with args: {args_tuple}, {e}")


def init_if_not_exists():
    db_executor(create_tinyurls_table_query)


def get_last_rowid():
    result = db_executor(last_insert_rowid).fetchone()[0]
    return result if result else 0


def insert_new_url(base_url, tiny_url):
    db_executor(insert_new_url_query, (base_url, tiny_url))


def get_exists_tiny_url(base_url):
    result = db_executor(get_exists_tiny_url_query, (base_url,)).fetchone()
    return result[0] if result else None


def get_base_url(tiny_url):
    result = db_executor(get_base_url_from_tiny_url_query, (tiny_url,)).fetchone()
    return result[0] if result else None


def get_url_redirection_registrations_count():
    result = db_executor(count_url_redirection_registrations_query).fetchone()
    return result[0] if result else 0


def insert_data_to_stats(action):
    db_executor(insert_data_to_stats_query, (datetime.datetime.now(), action))


def get_stats(date_time_to_compare):
    result = db_executor(get_stats_query, (date_time_to_compare,)).fetchall()
    return result
