from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from main.models import Post
from main.serializers import PostDetailSerializer, PostSerializer
from main.views import SerializersMixin


class PostViewSet(
    SerializersMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    serializer_action_classes = {
        "list": PostSerializer,
    }
