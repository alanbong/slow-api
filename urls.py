# urls.py
from core.router import Router
from views import (
    home_view, UserCreateView, UserDetailView,
    UserListView,
    not_found_view, method_not_allowed
)


ROUTES = [
    ('/', {'GET': home_view}),
    ('users/', {
        'GET': UserListView,
        'POST': UserCreateView,
    }),
    ('users/<int:user_id>/', {'GET': UserDetailView}),
]
ERRORS = [
    (404, not_found_view),
    (405, method_not_allowed),
]

router = Router()
router.load_conf(ROUTES, ERRORS)
