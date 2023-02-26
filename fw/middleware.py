from uuid import uuid4
from urllib.parse import parse_qs


class BaseMiddleware:

    def to_request(self, request):
        pass

    def to_response(self, response):
        pass


class Session(BaseMiddleware):

    def to_response(self, response):
        if not response.request.session_id:
            response.headers.update(
                {'Set-Cookie': f'session_id={uuid4()}'}
            )

    def to_request(self, request):
        cookies = request.environ.get('HTTP_COOKIE')
        if not cookies:
            return
        session_id = parse_qs(cookies)['session_id']
        request.extra['session_id'] = session_id

middleware = [Session]

