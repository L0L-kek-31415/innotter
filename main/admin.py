from django.contrib import admin

from main.models import Tag, Page, Post

admin.site.register([Tag, Page, Post])
