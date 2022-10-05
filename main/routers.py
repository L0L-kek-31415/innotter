from rest_framework import routers
from main.views import PostViewSet, PageViewSet, TagViewSet


router = routers.SimpleRouter()
router.register(r'page', PageViewSet)
router.register(r'post', PostViewSet)
router.register(r'tag', TagViewSet)