#!/usr/bin/env python
from os import environ

from server import app as application

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = environ.get('OPENSHIFT_PYTHON_PORT', 8051)
    ip = environ.get('OPENSHIFT_PYTHON_IP', '0.0.0.0')
    httpd = make_server('localhost', ip, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
