from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from api.v1.users.routers import router

schema_view = get_swagger_view(title="Pastebin API")

urlpatterns = [
    path("api/", include("api.v1.urls")),
    path("", include("api.urls")),
]
