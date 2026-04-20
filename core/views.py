# views.py
from core.drivers.filedriver import FileDriver
from core.templator import TemplateEngine


class BaseView:
    template_name = None
    driver_class = FileDriver
    engine_class = TemplateEngine
    base_dir = 'templates'

    status = '200 OK'

    def __init__(self):
        full_path = self.base_dir + '/' + self.template_name
        self.driver = self.driver_class(full_path)
        self.engine = self.engine_class()

    def render(self, data):
        template = self.driver.read()
        rendered_template = self.engine.parse(template, data)
        body = rendered_template.encode('utf-8')
        headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(body)))
        ]

        return self.status, headers, body

    def redirect(self, location):
        return '302 Found', [('Location', location)], b''

    def get(self, *args, **kwargs):
        return '405 Method Not Allowed', [], b''

    def post(self, *args, **kwargs):
        return '405 Method Not Allowed', [], b''

    def patch(self, *args, **kwargs):
        return '405 Method Not Allowed', [], b''

    def delete(self, *args, **kwargs):
        return '405 Method Not Allowed', [], b''
