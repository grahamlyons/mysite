from os import environ

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = environ.get('OPENSHIFT_PYTHON_PORT')
    if port:
        httpd = make_server('localhost', 8051, application)
        # Wait for a single request, serve it and quit.
        httpd.handle_request()
