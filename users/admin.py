from django.contrib import admin
from .models import Customer, CustomerStatus, UserAuth

# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerStatus)
admin.site.register(UserAuth)
