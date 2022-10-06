from django.shortcuts import render
from rest_framework.viewsets import ViewSet, ModelViewSet
from datetime import datetime
from django.db.models import Q

from main.models import Post, Page, Tag
from main.permissions import IsOwnerOrReadOnly
from main.serializers import PostSerializer, PageSerializer, TagSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PageViewSet(ModelViewSet):
    queryset = Page.objects.filter(
        Q(unblock_date__lt=datetime.utcnow()) |
        Q(unblock_date=None)
    ).filter(is_private=False)
    serializer_class = PageSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
