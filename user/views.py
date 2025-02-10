from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from user.forms import LoginForm


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
    return render(request, 'user_auth/logout.html')

def logout_func(request):
    logout(request)
    return redirect('logout_page')