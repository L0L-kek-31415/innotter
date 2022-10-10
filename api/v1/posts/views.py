from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from main.models import Post
from api.v1.posts.serializers import PostDetailSerializer, PostSerializer
from api.v1.pages.base import SerializersMixin
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
