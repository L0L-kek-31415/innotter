from django.shortcuts import render
from rest_framework.viewsets import ViewSet, ModelViewSet
from main.models import Post, Page, Tag
from main.serializers import PostSerializer, PageSerializer, TagSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer