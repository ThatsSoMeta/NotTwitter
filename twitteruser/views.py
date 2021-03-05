from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import TwitterUser
from tweet.models import Tweet

# Create your views here.


def user_detail_view(request, username):
    user = TwitterUser.objects.get(username=username)
    tweets = Tweet.objects.filter(author=user).order_by('-id')
    return render(
        request,
        'user_detail.html',
        {'currentuser': user, 'tweets': tweets}
    )


@login_required
def follow_user(request, username):
    currentuser = TwitterUser.objects.get(username=request.user.username)
    user = TwitterUser.objects.get(username=username)
    currentuser.following.add(user)
    currentuser.save()
    user.followers.add(currentuser)
    user.save()
    return redirect(f'/users/{user.username}')


@login_required
def unfollow_user(request, username):
    currentuser = TwitterUser.objects.get(username=request.user.username)
    user = TwitterUser.objects.get(username=username)
    currentuser.following.remove(user)
    currentuser.save()
    user.followers.remove(currentuser)
    user.save()
    return redirect(f'/users/{user.username}')


@login_required
def view_all_users(request):
    users = TwitterUser.objects.filter(
        ~Q(username=request.user.username)
    )
    return render(
        request,
        'user_list.html',
        {'users': users}
    )
