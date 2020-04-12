from django.urls import path

from users import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    # Customers Urls
    path('customers/register', views.post_customer, name='post_customer'),
    path('customers', views.get_all_customers, name='get_all_customers'),
    path('customer/<int:customer_id>/details', views.get_customer, name='get_customer'),
    path('customer/<int:customer_id>/edit/<str:edit_type>', views.put_customer, name='put_customer'),
    path('customer/<int:customer_id>/delete', views.delete_customer, name='delete_customer'),

    # User Urls
    path('user/<int:user_id>/details', views.get_user, name='get_user'),
]
