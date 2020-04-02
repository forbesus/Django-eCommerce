import datetime

from django import forms

from users.models import Customer

Gender_Choices = (('M', 'Male'), ('F', 'Female'))


class DateInput(forms.DateInput):
    input_type = 'date'


class CustomerForm(forms.ModelForm):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
                           required=True,
                           max_length=40)
    contact_no = forms.CharField(label='Contact No',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact No.'}),
                                 required=True,
                                 max_length=10)
    email = forms.CharField(label='Email address',
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                            required=False,
                            max_length=50)
    dob = forms.DateField(label='Date of Birth',
                          initial=datetime.date.today,
                          widget=DateInput(attrs={'class': 'form-control'}),
                          required=True)
    gender = forms.ChoiceField(label='Gender',
                               choices=Gender_Choices,
                               widget=forms.Select(attrs={'class': 'form-control'}),
                               required=True
                               )
    proof_id_no = forms.CharField(label='Adhar No',
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adhar No.'}),
                                  required=True,
                                  max_length=20
                                  )
    address = forms.CharField(label='Address',
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Address'}),
                              required=True,
                              max_length=100
                              )

    class Meta:
        model = Customer
        fields = ['name', 'contact_no', 'email', 'dob', 'gender', 'proof_id_no', 'address']
