from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

from api.v1.pages.views import PageViewSet, SearchPageViewSet
from api.v1.posts.views import PostViewSet
from api.v1.tags.views import TagViewSet
from api.v1.users.views import UserViewSet, SearchUserViewSet, RegisterApi


router = routers.SimpleRouter()
schema_view = get_swagger_view(title="Pastebin API")

router.register(r"page", PageViewSet)
router.register(r"post", PostViewSet)
router.register(r"tag", TagViewSet)
router.register(r"search/page", SearchPageViewSet)
router.register(r"users", UserViewSet)
router.register(r"search/user", SearchUserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", RegisterApi.as_view()),
    path("swagger/", schema_view),
    path(
        "token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("", include(router.urls)),
]
