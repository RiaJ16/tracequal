from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from api.forms import UserForm
from api.models import Usr


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {
                'error': 'Invalid credentials',
                'username': username,
                'no_button': True,
            }
            return render(request, 'authentication/login.html', context)
    else:
        return render(request, 'authentication/login.html', {'no_button': True})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.POST:
        form = UserForm(request.POST)
    else:
        form = UserForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            new_user = Usr.objects.create(
                username=username,
                name=form.cleaned_data['name'],
                lastname=form.cleaned_data['lastname'],
                lastname2=form.cleaned_data['lastname2'],
                email=email
            )
            new_user.set_password(password)
            new_user.save()
            context = {
                'message': 'Account creation successful, you can now log in'
            }
            return render(request, 'authentication/login.html', context)
        else:
            context = {
                'form': form
            }
            return render(request, 'authentication/register.html', context)
    else:
        return render(request, 'authentication/register.html', context)
