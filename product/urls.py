from django.urls import path
from product import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/comment/', views.comment_detail, name='comment_detail'),
]
