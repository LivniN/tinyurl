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


def get_tiny_url(base_url, host_url):
    tiny_url = db.get_exists_tiny_url(base_url)
    if tiny_url:
        return tiny_url
    tiny_url = host_url + get_unique_tiny_path()
    db.insert_new_url(base_url, tiny_url)
    return tiny_url


def get_base_url(tiny_url):
    base_url = db.get_base_url(tiny_url)
    if base_url and base_url.find("http://") != 0 and base_url.find("https://") != 0:
        base_url = "http://" + base_url
    return base_url


def sign_redirect():
    db.insert_data_to_stats('redirect')


def sign_bad_request():
    db.insert_data_to_stats('error')


def get_stats():
    url_redirection_registrations_count = db.get_url_redirection_registrations_count()
    last_minute = dict((k, v) for k, v in db.get_stats(datetime.datetime.now() - datetime.timedelta(minutes=1)))
    last_hour = dict((k, v) for k, v in db.get_stats(datetime.datetime.now() - datetime.timedelta(hours=1)))
    last_day = dict((k, v) for k, v in db.get_stats(datetime.datetime.now() - datetime.timedelta(hours=24)))
    stats_data = {
        'url_redirection_registrations_count': url_redirection_registrations_count,
        'time_stats': {
            'labels': ['last minute', 'last hour', 'last day'],
            'data_objects': [
                {
                    'label': 'error',
                    'data': get_list_of_values('error', last_minute, last_hour, last_day),
                    'backgroundColor': '#910d0d',
                },
                {
                    'label': 'redirect',
                    'data': get_list_of_values('redirect', last_minute, last_hour, last_day),
                    'backgroundColor': '#0d912e',
                }
            ],
        },
    }
    return stats_data


def get_list_of_values(label, last_min, last_hour, last_day):
    label_data = [last_min.get(label, 0),
                  last_hour.get(label, 0),
                  last_day.get(label, 0)
                  ]
    return label_data
