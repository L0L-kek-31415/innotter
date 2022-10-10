from django.urls import path, include
from api.v1.users.routers import router

urlpatterns = [
    path("v1/", include("api.v1.users.routers")),
]
