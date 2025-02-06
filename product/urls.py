from django.urls import path
from product import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('comment_detail/<int:pk>/save/', views.comment_detail, name='comment_detail'),
]