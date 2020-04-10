from django.urls import path
from users import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login', views.login, name='user_login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register_customer, name='register_customer'),
    path('customers', views.get_all_customers, name='get_all_customers'),
    path('customer/<int:customer_id>', views.get_customer_details, name='get_customer_details'),
    path('customer/<int:customer_id>/edit/<str:edit_type>', views.edit_customer_details, name='edit_customer_details'),
    path('customer/<int:customer_id>/delete', views.delete_customer_details, name='delete_customer_details')
]
