from django.db.models import Q, Count, IntegerField
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from datetime import datetime

from api.v1.posts.tasks import email_for_followers
from main.models import Post, Page
from api.v1.posts.serializers import (
    PostDetailSerializer,
    PostSerializer,
    PrivatePostSerializer,
    PostCreateSerializer,
)
from api.v1.pages.base import SerializersMixin
from user.permissions import IsModer, IsOwner
from api.v1.posts.service import PostService
from main.permissions import IsPageOwner


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
        "create": (IsAuthenticated, IsPageOwner),
        "update": (IsAuthenticated, IsModer | IsOwner | IsAdminUser),
        "destroy": (IsAuthenticated, IsModer | IsOwner | IsAdminUser),
        "reply_to": (IsAuthenticated, IsPageOwner),
    }
    queryset = (
        Post.objects.select_related("page")
        .filter(page__owner__is_blocked=False)
        .filter(
            Q(page__unblock_date__lt=datetime.utcnow())
            | Q(page__unblock_date__isnull=True)
        )
        .annotate(like_count=Count("like"))
    )
    serializer_class = PostDetailSerializer
    serializer_action_classes = {"list": PrivatePostSerializer}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostDetailSerializer(instance)
        if request.user in instance.page.followers.all():
            serializer = PostDetailSerializer(instance)
        elif instance.page.is_private:
            serializer = PrivatePostSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = serializer.validated_data.get("page")
        self.check_object_permissions(request=request, obj=page)
        serializer.save()
        email_for_followers.delay(page.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(IsAuthenticated,),
        url_path="unlike",
    )
    def unlike(self, request, pk=None):
        post = self.get_object()
        return Response(
            PostService(post, request.user).remove_like(), status.HTTP_202_ACCEPTED
        )

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(IsAuthenticated,),
        url_path="like",
    )
    def like(self, request, pk=None):
        post = self.get_object()
        return Response(
            PostService(post, request.user).add_like(), status.HTTP_202_ACCEPTED
        )

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="mylikes",
    )
    def my_likes(self, request):
        queryset = Post.objects.filter(like=request.user).values()
        return Response({"Posts": queryset}, status.HTTP_200_OK)

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="recommendations",
    )
    def my_recommendations(self, request):
        id_page = Page.objects.filter(followers=request.user)
        ids = [item.id for item in id_page]
        queryset = Post.objects.filter(page_id__in=ids)
        return Response({"Recommendations for you": queryset.values()})

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(IsAuthenticated,),
        url_path="reply",
    )
    def reply_to(self, request, pk=None):
        post = self.get_object()
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = serializer.validated_data.get("page")
        self.check_object_permissions(request=request, obj=page)
        serializer.save()
        email_for_followers.delay(page.id)
        PostService(post).add_reply(serializer.data["id"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
