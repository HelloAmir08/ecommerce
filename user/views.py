from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from user.models import User
from user.forms import LoginForm

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


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
                messages.error(request, 'Invalid login')

    return render(request, 'user_auth/login.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('login')


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from .forms import RegisterForm


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            try:
                validate_password(form.cleaned_data['password'])
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
                return render(request, 'user_auth/register.html', {'form': form})
            user.set_password(user.password)
            if user.is_verified:
                user.is_active = True
                user.is_staff = True
                user.is_superuser = True
                user.save()
                messages.success(request, 'Your account has been successfully created.')
                return redirect('login')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Verify your email'
            message = render_to_string('user_auth/verify_email_message.html', {
                'user': request.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(subject, message, to=[user.email])
            email.content_subtype = 'html'
            email.send()

            messages.success(request, 'We have sent you a verification email. Please check your inbox.')
            return redirect('login')

    return render(request, 'user_auth/register.html', {'form': form})


def user_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = RegisterForm(instance=user)

    return render(request, 'user_auth/user_profile.html', {'form': form, 'user': user})


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect('login')
    else:
        messages.warning(request, 'The verification link is invalid or has expired.')

    return render(request, 'user_auth/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'user_auth/verify_email_complete.html')
