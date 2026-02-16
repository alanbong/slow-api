# urls.py
from core.router import Router
from views import (
        home_view, users_list_view, user_detail_view,
        not_found_view, method_not_allowed
)


ROUTES = [
    ('/', {'GET': home_view}),
    ('users/', {'GET': users_list_view}),
    ('users/<int:user_id>/', {'GET': user_detail_view}),
]
ERRORS = [
    (404, not_found_view),
    (405, method_not_allowed),
]

router = Router()
router.load_conf(ROUTES, ERRORS)
