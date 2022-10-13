from django.urls import path, include


urlpatterns = [
    path("api/", include("api.v1.urls")),
    path("", include("api.urls")),
]
