from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from twitteruser.forms import CreateUserForm, LoginForm
from twitteruser.models import TwitterUser

# Create your views here.


def register_view(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = TwitterUser.objects.create(
                username=data['username'],
                email=data['email'],
                password=data['password1'],
            )
            if new_user is not None:
                print(new_user)
                login(request, new_user)
                return redirect('/')
    return render(
        request, 'auth/generic_form.html', {'form': form, 'header': "Register"}
    )


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return redirect('/')
    return render(
        request,
        'auth/generic_form.html',
        {
            'form': form,
            'header': 'Login'
        }
    )


def logout_view(request):
    logout(request)
    return redirect('/')
