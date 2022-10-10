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
)
from api.v1.pages.service import (
    add_block,
    is_user_send_follow_request,
    is_user_follower,
    del_user_from_follow_request,
    del_user_from_followers,
    add_user_to_follow_request,
    add_user_to_followers,
)
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
        "update": (IsAuthenticated, IsModer | IsOwner | IsAdminUser),
        "destroy": (IsAuthenticated, IsModer | IsOwner | IsAdminUser),
        # "create": [IsAuthenticated],
        "follow": (IsAuthenticated, IsPageNotBlocked),
        "unfollow": (IsAuthenticated, IsPageNotBlocked),
        "block": (IsAuthenticated, IsModer | IsAdminUser),
    }

    def check_permissions(self, request):
        try:
            handler = getattr(self, self.action.lower())
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

    @action(detail=True, methods=("post",))
    def follow(self, request, pk=None):
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, self.get_object())
        if is_user_follower(request.user, page) or is_user_send_follow_request(
            request.user, page
        ):
            return Response(
                {"message": "You are already sent follow request"},
                status.HTTP_400_BAD_REQUEST,
            )
        if page.is_private:
            add_user_to_follow_request(request.user, page)
        else:
            add_user_to_followers(request.user, page)
        return Response(status.HTTP_200_OK)

    @action(detail=True, methods=("post",))
    def unfollow(self, request, pk=None):
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, self.get_object())
        if is_user_follower(request.user, page):
            del_user_from_followers(request.user, page)
        elif is_user_send_follow_request(request.user, page):
            del_user_from_follow_request(request.user, page)
        return Response(
            {"message": "You're not in followers/follow requests"},
            status.HTTP_202_ACCEPTED,
        )

    @action(detail=True, methods=("post",))
    def block(self, request, pk=None):
        page = self.get_object()
        self.check_permissions(request)
        print(page.unblock_date)
        self.check_object_permissions(request, self.get_object())
        new_block_date = PageDetailSerializer(data=request.data)
        add_block(page, new_block_date)

    @action(detail=True, methods=("get", "post"))
    def check_followers(self, request, pk=None):

        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, self.get_object())
        if page.is_private:
            if request.method == "GET":
                serializer = PageFollowersSerializer(page)
                return Response(
                    {
                        "follow_requests": serializer.data["follow_requests"],
                        "followers": serializer.data["followers"],
                    },
                    status.HTTP_200_OK,
                )
            else:
                follow_requests = list(
                    page.follow_requests.values_list("pk", flat=True)
                )
                request.data.update({"follow_requests": follow_requests})
                serializer = PageFollowersSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.update(page, request.data)
                    return Response(status.HTTP_200_OK)
                return Response(
                    {"message": "Your data is not valid"}, status.HTTP_400_BAD_REQUEST
                )


class SearchPageViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = PageSerializer
    permission_classes = (AllowAny,)
    queryset = Page.objects.all()
    filterset_fields = ("uuid", "tags", "name")
