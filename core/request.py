# request.py
import json
import urllib.parse


class Request:
    def __init__(self, env):
        self.env = env
        self.method = env.get('REQUEST_METHOD', 'GET')
        self.path = env.get('PATH_INFO', '/')
        self._body = None

    @property
    def body(self):
        if self._body is None:
            content_length = int(self.env.get('CONTENT_LENGTH', 0) or 0)
            if content_length > 0:
                self._body = self.env['wsgi.input'].read(content_length)
            else:
                self._body = b''
        return self._body

    @property
    def data(self):
        if not self.body:
            return {}

        content_type = self.env.get('CONTENT_TYPE', '')

        if 'application/json' in content_type:
            return json.loads(self.body.decode('utf-8'))

        if 'application/x-www-form-urlencoded' in content_type:
            decoded = self.body.decode('utf-8')
            parsed = urllib.parse.parse_qs(decoded)
            return {key: value[0] for key, value in parsed.items()}

        return {}
