from django.urls import path
from .views import notification_view, read_notification_view

urlpatterns = [
    path('', notification_view, name='notifications'),
    path(
        'read/<int:notification_id>/',
        read_notification_view,
        name='read'
    ),
]
