from django.contrib import admin
from django.urls import path, include
from main.routers import router
from user.routers import router as user_router
from rest_framework_simplejwt import views as jwt_views
from user.views import RegisterApi

from main.views import PostViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user/', include(user_router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterApi.as_view()),
    path('', include(router.urls)),
]
