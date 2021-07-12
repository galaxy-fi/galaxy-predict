from django.contrib import admin
from .models import Article, UserInfo

admin.site.register(Article)
admin.site.register(UserInfo)