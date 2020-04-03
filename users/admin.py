from django.contrib import admin
from .models import Customer, CustomerStatus

# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerStatus)