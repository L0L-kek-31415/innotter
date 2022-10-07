from rest_framework import routers

from api.v1.users.views import UserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)
