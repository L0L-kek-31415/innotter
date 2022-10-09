from rest_framework import serializers
from main.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("id", "name", "owner", "description", "tags", "image", "is_private")


class PageDetailSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = (
            "name",
            "uuid",
            "description",
            "tags",
            "owner",
            "followers",
            "image",
            "follow_requests",
            "is_private",
        )
        read_only_field = fields


class PageFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("follow_requests", "followers")
