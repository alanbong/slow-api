# wsgi.py
from wsgiref.simple_server import make_server

from core.request import Request
from urls import router


def app(env, res):
    request = Request(env)
    view, params = router.get_handler(request.path, request.method)
    if request.method in ('POST', 'PATCH', 'PUT'):
        status, headers, body = view(request.data, **params)
    else:
        status, headers, body = view(**params)

    res(status, headers)
    return [body]

httpd = make_server('localhost', 8080, app)
httpd.serve_forever()
