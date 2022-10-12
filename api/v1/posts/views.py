from django.db.models import Q, Count, IntegerField
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from datetime import datetime

from main.models import Post, Page
from api.v1.posts.serializers import PostDetailSerializer, PostSerializer
from api.v1.pages.base import SerializersMixin
from user.permissions import IsModer, IsOwner
from api.v1.posts.service import PostService


class PostViewSet(
    SerializersMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = []
    permission_classes_per_method = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "create": (IsAuthenticated,),
        "update": (IsAuthenticated, IsModer | IsOwner | IsAdminUser),
        "destroy": (IsAuthenticated, IsModer | IsOwner | IsAdminUser),
    }
    queryset = Post.objects.filter(
        page__owner__is_blocked=False).filter(
        Q(page__unblock_date__lt=datetime.utcnow()) |
        Q(page__unblock_date__isnull=True)).annotate(like_count=Count('like'))
    serializer_class = PostDetailSerializer
    serializer_action_classes = {
        "list": PostSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if PostService.check_page_owner(serializer.data["page"], request.user.id):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("You can use only your own pages")

    @action(detail=True, methods=("post",),
            permission_classes=(IsAuthenticated,),
            url_path="unlike")
    def unlike(self, request, pk=None):
        post = self.get_object()
        return Response(PostService(post, request.user).remove_like(), status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=("post",),
            permission_classes=(IsAuthenticated,),
            url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        return Response(PostService(post, request.user).add_like(), status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=("get",),
            permission_classes=(IsAuthenticated,),
            url_path="mylikes")
    def my_likes(self, request):
        queryset = Post.objects.filter(like=request.user).values()
        serializer = PostSerializer(data=queryset)
        serializer.is_valid()
        return Response({"Posts": queryset}, status.HTTP_200_OK)

