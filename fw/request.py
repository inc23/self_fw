from urllib.parse import parse_qs


class Request:

    def __init__(self, environ, settings):
        self.environ = environ
        self.settings = settings
        self._build_get_from_param(environ['QUERY_STRING'])
        self._build_post_from_param(environ['wsgi.input'].read())
        self.extra = dict()

    def __getattr__(self, item):
        return self.extra.get(item)

    def _build_get_from_param(self, param):
        self.GET = parse_qs(param)


    def _build_post_from_param(self, param):
        param = param.decode('utf-8')
        self.POST = parse_qs(param)
