import string
from app.server.context import db

legal_url_chars = list(string.ascii_letters) + list(map(chr, range(48, 58)))


def get_unique_tiny_path():
    next_id = db.get_last_rowid() + 1
    tiny_path = ""
    while next_id > 0:
        tiny_path += (legal_url_chars[next_id % 62])
        next_id = int(next_id / 62)
    return tiny_path


def get_base_url(tiny_url):
    base_url = db.get_base_url(tiny_url)
    if base_url:
        if base_url.find("http://") != 0 and base_url.find("https://") != 0:
            base_url = "http://" + base_url
    return base_url
