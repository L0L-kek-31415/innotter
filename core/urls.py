from django.contrib import admin
from django.urls import path, include
from main.routers import router
from user.routers import router as user_router
from rest_framework_simplejwt import views as jwt_views

from user.views import RegisterApi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/user/", include(user_router.urls)),
    path(
        "api/v1/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/v1/register/", RegisterApi.as_view()),
    path("api/v1/", include(router.urls)),
]
