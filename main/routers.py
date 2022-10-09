from rest_framework import routers

from main.api.v1.views.page import PageViewSet, SearchPageViewSet
from main.api.v1.views.post import PostViewSet
from main.api.v1.views.tag import TagViewSet

router = routers.SimpleRouter()
router.register(r"page", PageViewSet)
router.register(r"post", PostViewSet)
router.register(r"tag", TagViewSet)
router.register(r"search/page", SearchPageViewSet)
