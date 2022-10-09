from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from main.models import Tag
from main.api.v1.serializers.tag import TagSerializer


class TagViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
