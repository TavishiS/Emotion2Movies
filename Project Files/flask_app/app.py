from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Welcome to "Movie for Me"!</h1>'