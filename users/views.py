from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from users.forms import CustomerForm


def login(request):
    return render(request, 'login.html')


def register_customer(request):
    if request.method == 'POST':
        if 'cancel' in request.POST: return render(request, 'dashboard.html')
        form = CustomerForm(request.POST)
        if True:
            form.save(commit=True)
            return render(request, 'dashboard.html')
    else:
        form = CustomerForm()
    return render(request, 'register.html', {'form': form})


def dashboard(request):
    return render(request, 'dashboard.html')
