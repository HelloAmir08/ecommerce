from django.urls import path
from user import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path('logout/', views.logout_page, name='logout_page')
]
