"""twitterclone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
# from authentication.views import login_view, logout_view, register_view
from tweet.views import homepage_view, tweet_view, like_tweet, unlike_tweet
from twitteruser.views import user_detail_view, follow_user, unfollow_user

urlpatterns = [
    path('accounts/', include('authentication.urls')),
    path('', homepage_view, name='homepage'),
    path('tweet/', tweet_view, name='tweet'),
    path('tweet/like/<int:tweet_id>/', like_tweet, name='like'),
    path('tweet/unlike/<int:tweet_id>/', unlike_tweet, name='unlike'),
    path('users/<str:username>/', user_detail_view, name='details'),
    path('users/follow/<str:username>/', follow_user, name='follow'),
    path('users/unfollow/<str:username>/', unfollow_user, name='follow'),
    path('admin/', admin.site.urls),
]
