from django.urls import path

from users import views

urlpatterns = [
    path('', views.login, name='user_login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register_customer, name='register_customer')
]
