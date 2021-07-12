from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('new', views.article_new, name='article_new'),
    path('vote/<int:id>/', views.article_vote, name='article_vote'),
]