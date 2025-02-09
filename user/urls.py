from django.urls import path
from .views import custom_login_view

urlpatterns = [
    path("", custom_login_view, name="login"),
]
