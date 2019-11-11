import datetime
import sqlite3

from app.server.context import config, log, ServerError

create_tinyurls_table_query = "CREATE TABLE IF NOT EXISTS tinyurls (long_url TEXT UNIQUE , short_url TEXT UNIQUE)"
create_redirection_stats_table_query = "CREATE TABLE IF NOT EXISTS redirection_stats (timestamp TIMESTAMP)"
create_error_stats_table_query = "CREATE TABLE IF NOT EXISTS error_stats (timestamp TIMESTAMP)"
insert_new_url_query = "INSERT INTO tinyurls (long_url, short_url) VALUES (?, ?)"
last_insert_rowid = "SELECT max(ROWID) FROM tinyurls"
get_long_url_from_short_url_query = "SELECT long_url FROM tinyurls WHERE short_url=?"
get_exists_short_url_query = "SELECT short_url FROM tinyurls WHERE long_url=?"
count_url_redirection_registrations_query = "SELECT COUNT(*) FROM tinyurls"
insert_data_to_redirection_stats_query = "INSERT INTO redirection_stats (timestamp) VALUES (?)"
insert_data_to_error_stats_query = "INSERT INTO error_stats (timestamp) VALUES (?)"
get_redirection_stats_query = "SELECT COUNT(*) FROM redirection_stats WHERE timestamp >= ? "
get_error_stats_query = "SELECT COUNT(*) FROM error_stats WHERE timestamp >= ? "


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
    db_executor(create_redirection_stats_table_query)
    db_executor(create_error_stats_table_query)


def get_last_rowid():
    result = db_executor(last_insert_rowid).fetchone()[0]
    return result if result else 0


def insert_new_url(long_url, short_url):
    db_executor(insert_new_url_query, (long_url, short_url))


def get_exists_short_url(long_url):
    result = db_executor(get_exists_short_url_query, (long_url,)).fetchone()
    return result[0] if result else None


def get_long_url(short_url):
    result = db_executor(get_long_url_from_short_url_query, (short_url,)).fetchone()
    return result[0] if result else None


def get_url_redirection_registrations_count():
    result = db_executor(count_url_redirection_registrations_query).fetchone()
    return result[0] if result else 0


def insert_data_to_redirection_stats():
    db_executor(insert_data_to_redirection_stats_query, (datetime.datetime.now(),))


def insert_data_to_error_stats():
    db_executor(insert_data_to_error_stats_query, (datetime.datetime.now(),))


def get_redirection_stats(date_time_to_compare):
    result = db_executor(get_redirection_stats_query, (date_time_to_compare,)).fetchone()[0]
    return result


def get_error_stats(date_time_to_compare):
    result = db_executor(get_error_stats_query, (date_time_to_compare,)).fetchone()[0]
    return result
