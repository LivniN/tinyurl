from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS

from app.server import utils
from app.server.context import db, ServerError

db.init_if_not_exists()
app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def index():
    return render_template('./client/index.html')


@app.route('/stats', methods=['GET'])
def stats_page():
    stats_data = utils.get_stats()
    return jsonify({'success': True, 'stats_data': stats_data})


@app.route('/post_new_url', methods=['POST'])
def post_new_url():
    request_json = request.get_json()
    long_url = request_json.get('long_url')
    if not long_url:
        return jsonify({'success': False, 'error': 'Missing long_url attribute'})
    try:
        short_url = utils.get_short_url(long_url=long_url, host_url=request.host_url)
    except ServerError:
        return jsonify({'success': False, 'error': 'Failed to get short url'})
    return jsonify({'success': True, 'short_url': short_url})


@app.errorhandler(404)
def redirect_or_not_found(error):
    try:
        long_url = utils.get_long_url(request.base_url)
    except ServerError:
        return error_page()
    if long_url:
        utils.sign_redirect()
        return redirect(long_url)
    return error_page()


@app.errorhandler(Exception)
def method_not_allowed(error):
    return error_page()


def error_page():
    utils.sign_bad_request()
    return redirect('custom_error_page.html')
