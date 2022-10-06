from rest_framework import serializers
from main.models import Post, Page, Tag


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("content",)


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("page", "content", "reply_to")
        read_only_field = fields


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("name", "description", "tags", "image")


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
        )
        read_only_field = fields


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
