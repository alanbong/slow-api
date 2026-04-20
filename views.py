# views.py
from models import User, Car
from core.views import BaseView


def home_view():
    body = 'home'.encode('utf-8')
    return '200 OK', [('Content-Type', 'text/html')], body


class UserListView(BaseView):
    template_name = 'users.txt'

    def get(self):
        users = User().all()
        return self.render({'users': users})


class UserCreateView(BaseView):
    template_name = 'user_form.txt'

    def get(self):
        return self.render({})

    def post(self, request_data):
        User().create(**request_data)
        return self.redirect('/users/')


class UserDetailView(BaseView):
    template_name = 'user_detail.txt'

    def get(self, user_id):
        user = User().get(user_id)
        user_cars = Car().filter(uid=user_id)
        return self.render({'user': user, 'cars': user_cars})

    def patch(self, request_data, user_id):
        User().update(user_id, request_data)
        return self.redirect(f'/users/{user_id}/')

    def delete(self, user_id):
        User().delete(user_id)
        return self.redirect('/users/')


def not_found_view():
    body = 'Not Found'.encode('utf-8')
    return (
        '404 Not Found',
        [('content-type', 'text/html')],
        body
    )


def method_not_allowed(allowed_methods=None):
    body = f'Allowed methods: {allowed_methods}'
    return (
        '405 Method Not Allowed',
        [('content-type', 'text/html')],
        body
    )
