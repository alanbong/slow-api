#wsgi.py
from wsgiref.simple_server import make_server

from urls import router


def app(req, res):
    method, path = get_params(req)
    handler, params = router.get_handler(path, method)
    status, headers, body = handler(**params)

    if isinstance(body, str):
        body = body.encode('utf-8')

    headers.append(('Content-Length', str(len(body))))

    res(status, headers)
    return [body]

def get_params(req):
    method = req.get('REQUEST_METHOD', None)
    path = req.get('PATH_INFO', None)
    return method, path

httpd = make_server('localhost', 8080, app)
httpd.serve_forever()
