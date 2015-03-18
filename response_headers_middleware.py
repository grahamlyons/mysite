
class ResponseHeaders(object):

    def __init__(self, app, headers):
        self.app = app
        self.headers = headers

    def __call__(self, env, start_response):
        def _start_response(status, headers, exc_info=None):
            headers + self.headers
            return start_response(status, headers, exc_info)
        appiter = self.app(env, _start_response)
        for item in appiter:
            yield item

        if hasattr(appiter, 'close'):
            appiter.close()


