from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from user.forms import LoginForm, RegisterForm


# Create your views here.


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('product_list')
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Invalid login')
    context = {
        'form': form
    }
    return render(request, 'user_auth/login.html', context=context)


def logout_page(request):
    logout(request)
    return render(request, 'user_auth/logout.html')


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'user_auth/register.html', context)


def user_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = RegisterForm(instance=user)

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'user_auth/user_profile.html', context)
