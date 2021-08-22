from django.urls import path
from web3auth import urls as web3auth_urls
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('new', views.article_new, name='article_new'),
    path('vote/<int:id>/', views.article_vote, name='article_vote'),
    path('detail/<int:id>/', views.article_detail, name='article_detail'),
]