"""
URL configuration for newsrecommendation project.

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

from app.views.news import create_news_list, get_all_news, get_news_by_id, recommend_news, delete_news, delete_all_news
from app.views.user import create_user, get_all_users, get_user_by_id, delete_user, delete_all_users
from django.contrib import admin
from django.urls import path
from app.views.user import create_user
from app.views.reccomandation import recommend
from app.views.user import user_login
from app.views.news import update_rating

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_login, name='home'),
    path('create_user/', create_user, name='create_user'),
    path('get_all_users/', get_all_users, name='get_all_users'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('get_user_by_id/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('delete_all_users/', delete_all_users, name='delete_all_users'),
    path('create_news_list/', create_news_list, name='create_news_list'),
    path('get_all_news/', get_all_news, name='get_all_news'),
    path('delete_news/<int:news_id>/', delete_news, name='delete_news'),
    path('get_news_by_id/<int:news_id>/', get_news_by_id, name='get_news_by_id'),
    path('delete_all_news/', delete_all_news, name='delete_all_news'),
    path('delete_all_news/', delete_all_news, name='delete_all_news'),
    path('recommend_news/<int:news_id>/', recommend_news, name='recommend_news'),
    path('recommend/<int:user_id>/', recommend, name='recommend'),
    path('login/', user_login, name='user_login'),
    path('update_rating/', update_rating, name='update_rating'),
]
