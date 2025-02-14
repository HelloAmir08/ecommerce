from django.urls import path
from user import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path('logout/', views.logout_page, name='logout_page'),
    path('register/', views.register_page, name="register"),
    path('user-profile/', views.user_profile_view, name="user_profile"),
]
