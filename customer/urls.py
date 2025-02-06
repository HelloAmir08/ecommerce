from django.urls import path
from customer import views
urlpatterns = [
    path('', views.customer_page, name='customer_page'),
    path('customer-detail/<int:pk>/', views.customer_detail, name='customer_page_detail'),
    path('customers/add/', views.customer_create, name='add_customer'),
    path('customers/edit/<int:pk>/', views.customer_edit, name='edit_customer'),
    path('customers/delete/<int:pk>/', views.customer_delete, name='delete_customer'),
]