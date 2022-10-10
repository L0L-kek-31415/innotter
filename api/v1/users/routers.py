from django.urls import path
from rest_framework import routers

from api.v1.pages.views import PageViewSet, SearchPageViewSet
from api.v1.posts.views import PostViewSet
from api.v1.tags.views import TagViewSet
from api.v1.users.views import UserViewSet, SearchUserViewSet, RegisterView


router = routers.SimpleRouter()
router.register(r"page", PageViewSet)
router.register(r"post", PostViewSet)
router.register(r"tag", TagViewSet)
router.register(r"search/page", SearchPageViewSet)
router.register(r"users", UserViewSet)
router.register(r"search/user", SearchUserViewSet)

urlpatterns = router.urls + [
    path("register/", RegisterView.as_view()),
]
