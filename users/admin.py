from django.contrib import admin
from .models import Customer, CustomerStatus, UserAuth, User

# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerStatus)
admin.site.register(User)
admin.site.register(UserAuth)
