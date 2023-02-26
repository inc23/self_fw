class Response:

    def __init__(self, request, status_code='200', headers = None, body=''):
        self.status_code = status_code
        self.body = b''
        self.headers = dict()
        self._set_base_headers()
        if headers is not None:
            self._update_headers(headers)
        self._set_body(body)
        self.request = request
        self.extra = dict()

    def __getattr__(self, item):
        return self.extra.get(item)

    def _set_base_headers(self):
        self.headers = {
            'Content-Type': "text/html; charset=utf-8",
            "Content-Length": 0
        }

    def _update_headers(self, headers):
        self.headers.update(headers)

    def _set_body(self, body):
        self.body = body.encode('utf-8')
        self._update_headers(
            {"Content-Length": str(len(self.body))}
        )
