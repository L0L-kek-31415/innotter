from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from main.models import Post
from main.api.v1.serializers.post import PostDetailSerializer, PostSerializer
from main.api.v1.views.base import SerializersMixin
from user.permissions import IsModer


class PostViewSet(
    SerializersMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = (
        IsAuthenticated,
        IsModer,
    )
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    serializer_action_classes = {
        "list": PostSerializer,
    }
