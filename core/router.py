# router.py
class RouterNode:
    def __init__(self):
        self.children = {}
        self.methods = {}
        self.param_name = None
        self.param_type = None


class Router:
    def __init__(self):
        self.root = RouterNode()
        self.error_handlers = {}

    def register_error(self, code, handler):
        self.error_handlers[code] = handler

    def register_route(self, path, handlers):
        node = self.root
        segments = [
            segment
            for segment in path.strip('/').split('/')
            if segment
        ]
        for segment in segments:
            if segment.startswith('<') and segment.endswith('>'):
                segment = segment.strip('<>')
                # saving type 'str' if type isn't specified
                param_type, param_name = (
                    segment.split(':')
                    if ':' in segment
                    else ('str', segment)
                )
                if '*' not in node.children:
                    node.children['*'] = RouterNode()
                node = node.children['*']
                node.param_name = param_name
                node.param_type = param_type
            else:
                if segment not in node.children:
                    node.children[segment] = RouterNode()
                node = node.children[segment]

        for method, func in handlers.items():
            node.methods[method.upper()] = func

    def get_handler(self, path, method):
        node = self.root
        params = {}
        segments = [
            segment
            for segment in path.strip('/').split('/')
            if segment
        ]
        for segment in segments:
            if segment in node.children:
                node = node.children[segment]
            elif '*' in node.children:
                node = node.children['*']
                if node.param_type == 'int' and segment.isdigit():
                    params[node.param_name] = int(segment)
                elif node.param_type == 'str' and isinstance(segment, str):
                    params[node.param_name] = segment
                else:
                    return self.error_handlers.get(404), {}
            else:
                return self.error_handlers.get(404), {}

        if not node.methods:
            return self.error_handlers.get(404), {}

        handler = node.methods.get(method.upper())
        if not handler:
            return (
                self.error_handlers.get(405),
                {'allowed_methods': list(node.methods.keys())}
            )

        return handler, params

    def load_conf(self, routes, errors=None):
        for path, handlers in routes:
            self.register_route(path, handlers)

        if errors:
            for code, handler in errors:
                self.register_error(code, handler)
