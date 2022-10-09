from rest_framework import routers

from user.api.v1.views.user import UserViewSet, SearchUserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)
router.register(r"search/user", SearchUserViewSet)
