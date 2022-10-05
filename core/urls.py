from django.contrib import admin
from django.urls import path, include
from main.routers import router
from user.routers import router as user_router
from main.views import PostViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(user_router.urls)),
    path('', include(router.urls)),
]
