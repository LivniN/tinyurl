import datetime
import string

from app.server.context import db

legal_url_chars = list(string.ascii_letters) + list(map(chr, range(48, 58)))


def get_unique_tiny_path():
    next_id = db.get_last_rowid() + 1
    tiny_path = "_"
    while next_id > 0:
        tiny_path += (legal_url_chars[next_id % 62])
        next_id = int(next_id / 62)
    return tiny_path


def get_short_url(long_url, host_url):
    short_url = db.get_exists_short_url(long_url)
    if short_url:
        return short_url
    short_url = host_url + get_unique_tiny_path()
    db.insert_new_url(long_url, short_url)
    return short_url


def get_long_url(short_url):
    long_url = db.get_long_url(short_url)
    if long_url and long_url.find("http://") != 0 and long_url.find("https://") != 0:
        long_url = "http://" + long_url
    return long_url


def sign_redirect():
    db.insert_data_to_redirection_stats()


def sign_bad_request():
    db.insert_data_to_error_stats()


def get_stats():
    url_redirection_registrations_count = db.get_url_redirection_registrations_count()
    stats_data = {
        'url_redirection_registrations_count': url_redirection_registrations_count,
        'time_stats': {
            'labels': ['last minute', 'last hour', 'last day'],
            'data_objects': [
                {
                    'label': 'error',
                    'data': get_list_of_values(db.get_error_stats),
                    'backgroundColor': '#910d0d',
                },
                {
                    'label': 'redirect',
                    'data': get_list_of_values(db.get_redirection_stats),
                    'backgroundColor': '#0d912e',
                }
            ],
        },
    }
    return stats_data


def get_list_of_values(db_function):
    last_minute = db_function(datetime.datetime.now() - datetime.timedelta(minutes=1))
    last_hour = db_function(datetime.datetime.now() - datetime.timedelta(hours=1))
    last_day = db_function(datetime.datetime.now() - datetime.timedelta(hours=24))
    label_data = [last_minute, last_hour, last_day]
    return label_data
