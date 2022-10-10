from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view


from api.v1.users.views import RegisterApi


schema_view = get_swagger_view(title="Pastebin API")

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
]
