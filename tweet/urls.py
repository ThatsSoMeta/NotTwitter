from django.urls import path
from .views import (
    tweet_view,
    like_tweet,
    unlike_tweet,
    tweet_detail_view
)

urlpatterns = [
    path('', tweet_view, name='tweet'),
    path('<int:id>/', tweet_detail_view, name='tweet'),
    path('like/<int:tweet_id>/', like_tweet, name='like'),
    path('unlike/<int:tweet_id>/', unlike_tweet, name='unlike'),
]