from flask import Flask, render_template

from app.server.context import db

db.init_if_not_exists()
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
