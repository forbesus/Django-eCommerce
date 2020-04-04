from django.urls import path
from users import views

urlpatterns = [
    path('', views.login, name='user_login'),
    path('logout', views.logout,name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register_customer, name='register_customer'),
    path('customers', views.get_all_customers, name='get_all_customers'),
    path('customer/<int:customer_id>', views.get_customer_details, name='get_customer_details')
]
