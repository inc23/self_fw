import re
from typing import Type, List
from fw.exception import NotAllowed, NotFound
from fw.request import Request


class FrameWork:

    def __init__(self, urls, settings, middleware):
        self.urls = urls
        self.settings = settings
        self.middleware = middleware

    def __call__(self, environ, start_response):
        from pprint import pprint; pprint(environ)
        pprint(environ['PATH_INFO'])
        view = self._get_view(environ)
        request = self._get_request(environ)
        self.apply_to_request(request)
        response = self._get_response(environ, view, request)
        self.apply_to_response(response)
        start_response(response.status_code, response.headers.items())
        return iter([response.body])

    def _prepare_url(self, url):
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, url):
        url = self._prepare_url(url)
        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view
        raise NotFound

    def _get_view(self, environ: dict):
        url = environ['PATH_INFO']
        view = self._find_view(url)
        return view()

    def _get_request(self, environ):
        return Request(environ, self.settings)

    def _get_response(self, environ, view, request):
        method = environ['REQUEST_METHOD'].lower()
        if hasattr(view, method):
            return getattr(view, method)(request)
        raise NotAllowed

    def apply_to_request(self, request):
        for i in self.middleware:
            i().to_request(request)

    def apply_to_response(self, response):
        for i in self.middleware:
            i().to_response(response)