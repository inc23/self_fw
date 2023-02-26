from datetime import datetime
from fw.view import View
from fw.response import Response
from fw.template_engine import build_template


class HomePage(View):

    def get(self, request, *args, **kwargs):
        body = build_template(request,
                              {'time': str(datetime.now()),
                               'lst': range(10),
                               'session_id': request.session_id
                               },
                              'home.html'
                              )
        return Response(request=request, body=body)


class Hello(View):

    def get(self, request, *args, **kwargs):
        body = build_template(request,
                              {'name': 'incognito'},
                              'hello.html'
                              )
        return Response(request=request, body=body)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')[0]
        body = build_template(request,
                              {'name': name},
                              'hello.html'
                              )
        return Response(request=request, body=body)
#
