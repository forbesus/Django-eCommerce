from django.db import models

Gender_Choices = (('M', 'Male'), ('F', 'Female'))


# Create your models here
class Customer(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=40)
    contact_no = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender_Choices)
    proof_id_no = models.CharField(max_length=20)
    address = models.TextField(max_length=100)
