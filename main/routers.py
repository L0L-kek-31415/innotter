from rest_framework import routers

from api.v1.pages.views import PageViewSet
from api.v1.posts.views import PostViewSet
from api.v1.tags.views import TagViewSet

router = routers.SimpleRouter()
router.register(r"page", PageViewSet)
router.register(r"post", PostViewSet)
router.register(r"tag", TagViewSet)
