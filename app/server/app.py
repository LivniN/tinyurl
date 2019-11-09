import json
import os

from flask import Flask, render_template, request, abort, redirect, send_from_directory, jsonify, make_response

from app.server.context import db
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
        abort(404)
    tiny_url = request.host_url + get_unique_tiny_path()
    try:
        db.insert_new_url(base_url, tiny_url)
    except:
        return jsonify({'success': False,'error': 'failed to get short url'})
    return jsonify({'success': True, 'tiny_url': tiny_url})


@app.errorhandler(404)
def not_found(error):
    try:
        base_url = get_base_url(request.base_url)
        if base_url:
            return redirect(base_url)
    finally:
        return jsonify({'error': 'Not found'})


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.png')
