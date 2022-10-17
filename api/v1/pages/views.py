from datetime import datetime

from django.db.models import Q
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.models import Page
from user.permissions import IsModer, IsOwner
from main.permissions import IsPageNotBlocked
from api.v1.pages.serializers import (
    PageDetailSerializer,
    PageSerializer,
    PageFollowersSerializer,
    PageUnblockDateSerializer,
)
from api.v1.pages.service import PageService
from api.v1.pages.base import SerializersMixin


class PageViewSet(
    SerializersMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Page.objects.prefetch_related("follow_requests").filter(
        Q(unblock_date__lt=datetime.utcnow()) | Q(unblock_date=None)
    )
    serializer_class = PageDetailSerializer
    serializer_action_classes = {
        "list": PageSerializer,
        "follow": PageFollowersSerializer,
        "unfollow": PageFollowersSerializer,
    }
    permission_classes = []
    permission_classes_per_method = {
        "list": (AllowAny,),
        "options": (AllowAny,),
        "retrieve": (AllowAny,),
        "update": (IsAuthenticated, IsModer | IsOwner | IsAdminUser),
        "destroy": (IsAuthenticated, IsModer | IsOwner | IsAdminUser),
    }

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=("post",),
        url_path="request/accept",
        permission_classes=(IsAuthenticated, IsModer | IsAdminUser | IsOwner),
    )
    def accept_follow_request(self, request, pk=None):
        page = self.get_object()
        serializer = PageFollowersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            PageService(page).accept_follow_request(serializer.data["follow_requests"])
        )

    @action(
        detail=True,
        methods=("post",),
        url_path="request/deny",
        permission_classes=(IsAuthenticated, IsModer | IsAdminUser | IsOwner),
    )
    def deny_follow_request(self, request, pk=None):
        page = self.get_object()
        serializer = PageFollowersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            PageService(page).deny_follow_request(serializer.data["follow_requests"])
        )

    @action(
        detail=True,
        methods=("post",),
        url_path="follow",
        permission_classes=(IsAuthenticated, IsPageNotBlocked),
    )
    def follow(self, request, pk=None):
        page = self.get_object()
        return Response(
            {
                "message": PageService(
                    page, user=request.user, user_id=request.user.id
                ).start_follow()
            },
            status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=("post",),
        url_path="unfollow",
        permission_classes=(IsAuthenticated,),
    )
    def unfollow(self, request, pk=None):
        page = self.get_object()
        return Response(
            {
                "message": PageService(
                    page, user=request.user, user_id=request.user.id
                ).stop_follow()
            },
            status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=("post",),
        url_path="block",
        permission_classes=(IsAuthenticated, IsModer | IsAdminUser),
    )
    def block(self, request, pk=None):
        page = self.get_object()
        serializer = PageUnblockDateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_date = serializer.data["unblock_date"]
        return Response(
            {"message": PageService(page=page, unblock_date=new_date).block_page()}
        )


class SearchPageViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = PageSerializer
    permission_classes = (AllowAny,)
    queryset = Page.objects.filter(
        Q(unblock_date__lt=datetime.utcnow()) | Q(unblock_date=None)
    )
    filterset_fields = ("uuid", "tags", "name")
