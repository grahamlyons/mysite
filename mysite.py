from os import environ

from flask import Flask
from response_headers_middleware import ResponseHeaders

GNU_TERRY_PRATCHETT = ('X-Clacks-Overhead', 'GNU Terry Pratchett')

app = Flask(__name__)
app.wsgi_app = ResponseHeaders(app.wsgi_app, [GNU_TERRY_PRATCHETT])

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
