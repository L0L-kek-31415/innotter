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
from api.v1.pages.service import PageActions
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
    queryset = Page.objects.filter(
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
        "create": [IsAuthenticated],
        "follow": (IsAuthenticated, IsPageNotBlocked),
        "unfollow": (IsAuthenticated, IsPageNotBlocked),
        "block": (IsAuthenticated, IsModer | IsAdminUser),
    }

    def check_permissions(self, request):
        handler = getattr(self, request.method.lower(), None)
        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(
                handler.__name__
            )
        super().check_permissions(request)

    @action(detail=True, methods=("post",))
    def follow(self, request, pk=None):
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, self.get_object())
        return Response(
            {"message": PageActions(page, request.user).start_follow()},
            status.HTTP_200_OK,
        )

    @action(detail=True, methods=("post",))
    def unfollow(self, request, pk=None):
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, self.get_object())
        return Response(
            {"message": PageActions(page, request.user).stop_follow()},
            status.HTTP_200_OK,
        )

    @action(detail=True, methods=("post",))
    def block(self, request, pk=None):
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, self.get_object())
        serializer = PageUnblockDateSerializer(data=request.data)
        serializer.is_valid()
        new_date = serializer.data["unblock_date"]
        return Response(
            {"message": PageActions(page=page, unblock_date=new_date).block_page()}
        )


class SearchPageViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = PageSerializer
    permission_classes = (AllowAny,)
    queryset = Page.objects.all()
    filterset_fields = ("uuid", "tags", "name")
