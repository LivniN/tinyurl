import os

from flask import Flask, render_template, request, redirect, send_from_directory, jsonify

from app.server import utils
from app.server.context import db, ServerError

db.init_if_not_exists()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stats')
def stats_page():
    stats_data = utils.get_stats()
    return render_template('stats.html', stats_data=stats_data)


@app.route('/post_new_url', methods=['POST'])
def post_new_url():
    request_json = request.get_json()
    base_url = request_json.get('base_url')
    if not base_url:
        return jsonify({'success': False, 'error': 'Missing base_url attribute'})
    tiny_url = utils.get_tiny_url(base_url=base_url, host_url=request.host_url)
    try:
        db.insert_new_url(base_url, tiny_url)
    except ServerError:
        return jsonify({'success': False, 'error': 'Failed to get short url'})
    return jsonify({'success': True, 'tiny_url': tiny_url})


@app.errorhandler(404)
def redirect_or_not_found(error):
    try:
        base_url = utils.get_base_url(request.base_url)
    except ServerError:
        return error_page()
    if base_url:
        utils.sign_redirect()
        return redirect(base_url)
    return error_page()


@app.errorhandler(Exception)
def method_not_allowed(error):
    return error_page()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.png')


def error_page():
    utils.sign_bad_request()
    return render_template('custom_error_page.html')
