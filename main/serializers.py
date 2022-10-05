from rest_framework import serializers
from main.models import Post, Page, Tag


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"