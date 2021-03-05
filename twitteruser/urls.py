from django.urls import path
from .views import (
    user_detail_view,
    follow_user,
    unfollow_user,
    view_all_users
)

urlpatterns = [
    path('all/', view_all_users, name='users'),
    path('<str:username>/', user_detail_view, name='details'),
    path('follow/<str:username>/', follow_user, name='follow'),
    path('unfollow/<str:username>/', unfollow_user, name='follow'),
]