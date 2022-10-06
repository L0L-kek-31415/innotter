from rest_framework import serializers
from main.models import Post, Page, Tag


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("page", "content", "reply_to")


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"
