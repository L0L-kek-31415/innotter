from datetime import datetime

from django.db.models import Q
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from main.models import Page
from main.permissions import IsModer
from main.serializers import PageDetailSerializer, PageSerializer
from main.views import SerializersMixin


class PageViewSet(
    SerializersMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = (IsModer,)
    queryset = Page.objects.filter(
        Q(unblock_date__lt=datetime.utcnow()) | Q(unblock_date=None)
    )
    serializer_class = PageDetailSerializer
    serializer_action_classes = {
        "list": PageSerializer,
    }
