from django.contrib import messages
from django.shortcuts import render, redirect

import sweetify

from users.forms import CustomerForm, CustomerStatusForm
from users.models import CustomerStatus


def login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        print(username,password," Is the values you have entered")
        try:
            user = UserAuth.objects.get(username=username,password=password)
            request.session['auth']=True
            return redirect('dashboard')

        except:
            return HttpResponse("Failed")

    else:
        return render(request, 'login.html')


def register_customer(request):
    if request.method == 'POST':
        if 'cancel' in request.POST: return redirect('dashboard')
        form_basic = CustomerForm(request.POST)
        form_status = CustomerStatusForm(request.POST)
        if form_basic.is_valid() and form_status.is_valid():
            try:
                instance = form_basic.save(commit=True)
                instance = CustomerStatus(customer_id=instance.id, status=request.POST.get('status'))
                CustomerStatusForm(data=request.POST, instance=instance).save(commit=True)
                sweetify.success(request, 'You successfully changed your password')
                messages.success(request, 'Successfully Registered')
                return redirect('dashboard')
            except Exception as err:
                messages.error(request, 'Something Went Wrong :' + str(err))
                return redirect('dashboard')
    else:
        form_basic = CustomerForm()
        form_status = CustomerStatusForm()
    return render(request, 'register.html', {'form_basic': form_basic, 'form_status': form_status})


def dashboard(request):
    return render(request, 'dashboard.html')
