from datetime import datetime

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.models import Page
from user.permissions import IsModer, IsOwner, IsOwnerOrModerOrAdmin
from main.permissions import IsPageBlocked, IsPagePrivate
from main.api.v1.serializers.page import (
    PageDetailSerializer,
    PageSerializer,
    PageFollowersSerializer,
)
from main.api.v1.views.base import SerializersMixin


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
    }
    permission_classes = []
    permission_classes_per_method = {
        "list": [AllowAny],
        "update": [IsAuthenticated, IsOwnerOrModerOrAdmin],
        "destroy": [IsAuthenticated, IsOwnerOrModerOrAdmin],
        "follow": [IsAuthenticated, IsPageBlocked],
        "check_followers": [IsAuthenticated, IsOwnerOrModerOrAdmin],
    }

    def check_permissions(self, request):
        try:
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(
                handler.__name__
            )

        super().check_permissions(request)

    @staticmethod
    def is_user_follower(user, page):
        return page.followers.filter(id=user.id).exists()

    @staticmethod
    def is_user_send_follow_request(user, page):
        return page.follow_requests.filter(id=user.id).exists()

    @staticmethod
    def add_user_to_follow_request(user, page):
        page.follow_requests.add(user)

    @staticmethod
    def add_user_to_followers(user, page):
        page.followers.add(user)

    @action(detail=True, methods=("post",))
    def follow(self, request, pk=None):
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, self.get_object())
        if self.is_user_follower(
            request.user, page
        ) or self.is_user_send_follow_request(request.user, page):
            return Response(
                {"message": "You are already sent follow request"},
                status.HTTP_400_BAD_REQUEST,
            )
        if page.is_private:
            self.add_user_to_follow_request(request.user, page)
        else:
            self.add_user_to_followers(request.user, page)
        return Response({"message": "Ok"}, status.HTTP_200_OK)

    @action(detail=True, methods=("get", "post"))
    def check_followers(self, request, pk=None):
        pass


class SearchPageViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = PageSerializer
    permission_classes = [AllowAny]
    queryset = Page.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("uuid", "tags", "name")
