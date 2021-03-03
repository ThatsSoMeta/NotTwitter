from django import forms
from django.contrib.auth.forms import UserCreationForm
from twitteruser.models import TwitterUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = TwitterUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)