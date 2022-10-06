from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from datetime import datetime
from django.db.models import Q

from main.models import Post, Page, Tag
from main.permissions import IsOwnerOrReadOnly
from main.serializers import (PostSerializer, PageSerializer, TagSerializer,
                              PostDetailSerializer, PageDetailSerializer)


class SerializersMixin:
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

class PostViewSet(SerializersMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    serializer_action_classes = {
        'list': PostSerializer,
    }


class PageViewSet(SerializersMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Page.objects.filter(
        Q(unblock_date__lt=datetime.utcnow()) |
        Q(unblock_date=None)
    )
    serializer_class = PageDetailSerializer
    serializer_action_classes = {
        'list': PageSerializer,
    }
    permission_classes = (IsOwnerOrReadOnly,)




class TagViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

