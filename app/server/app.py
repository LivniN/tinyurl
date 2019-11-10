import os

from flask import Flask, render_template, request, redirect, send_from_directory, jsonify

from app.server.context import db, ServerError
from app.server.utils import get_unique_tiny_path, get_base_url

db.init_if_not_exists()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post_new_url', methods=['POST'])
def post_new_url():
    request_json = request.get_json()
    base_url = request_json.get('base_url')
    if not base_url:
        return jsonify({'success': False, 'error': 'Missing base_url attribute'})
    tiny_url = db.get_exists_tiny_url(base_url)
    if tiny_url:
        return jsonify({'success': True, 'tiny_url': tiny_url})
    tiny_url = request.host_url + get_unique_tiny_path()
    try:
        db.insert_new_url(base_url, tiny_url)
    except ServerError:
        return jsonify({'success': False, 'error': 'Failed to get short url'})
    return jsonify({'success': True, 'tiny_url': tiny_url})


@app.route('/error-page')
def error_page():
    return render_template('custom_error_page.html')


@app.errorhandler(404)
def not_found(error):
    try:
        base_url = get_base_url(request.base_url)
        if base_url:
            return redirect(base_url)
        else:
            return redirect('/error-page')
    except ServerError:
        return redirect('/error-page')


@app.errorhandler(Exception)
def method_not_allowed(error):
    return redirect('/error-page')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.png')
