from rest_framework import serializers
from main.models import Post, Page
from django.db.models import Count


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("content", "page")
        read_only_field = fields


class PostDetailSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField()

    class Meta:
        model = Post
        # fields = ("__all__")
        fields = ("id", "page", "content", "reply_to", "like", "like_count")
        read_only_field = fields
