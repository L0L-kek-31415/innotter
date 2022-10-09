from django.contrib import admin
from django.urls import path, include
from main.routers import router
from user.routers import router as user_router
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view

from user.api.v1.views.user import RegisterApi


schema_view = get_swagger_view(title="Pastebin API")

urlpatterns = [
    path("lol/", schema_view),
    path("admin/", admin.site.urls),
    path("user/", include(user_router.urls)),
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
    path("register/", RegisterApi.as_view()),
    path("", include(router.urls)),
]
