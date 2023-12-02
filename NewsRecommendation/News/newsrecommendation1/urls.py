"""
URL configuration for newsrecommendation1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys

from django.contrib import admin
from django.urls import path

from app.controller.news import create_news, get_all_news, get_news_by_id, recommend_news, delete_news, delete_all_news
from app.controller.likes import create_user_likes
from app.controller.user import create_user, get_all_users, get_user_by_id, delete_user, delete_all_users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_user/', create_user, name='create_user'),
    path('get_all_users/', get_all_users, name='get_all_users'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('get_user_by_id/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('delete_all_users/', delete_all_users, name='delete_all_users'),
    path('create_news/', create_news, name='create_news'),
    path('get_all_news/', get_all_news, name='get_all_news'),
    path('delete_news/<int:news_id>/', delete_news, name='delete_news'),
    path('get_news_by_id/<int:news_id>/', get_news_by_id, name='get_news_by_id'),
    path('delete_all_news/', delete_all_news, name='delete_all_news'),
    path('delete_all_news/', delete_all_news, name='delete_all_news'),
    path('create_user_likes/', create_user_likes, name='create_user_likes'),
    path('recommend_news/<int:news_id>/', recommend_news, name='recommend_news'),
]
