from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.


@login_required
def notification_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(
        request,
        'notifications.html',
        {'notifications': notifications}
    )


@login_required
def read_notification_view(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return redirect('/notifications/')
