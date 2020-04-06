from django.contrib import messages
from django.shortcuts import render, redirect
from users.forms import CustomerForm, CustomerStatusForm
from users.models import CustomerStatus, Customer, UserAuth
from users.validation import get_dashboard_data

USER_ID = 1


def login(request):
    if request.method == 'GET':
        messages.info(request, "Please Login")
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = UserAuth.objects.get(username=username, password=password)
            request.session['user_id'] = user.user_id
            request.session['auth_login'] = True
            return redirect('dashboard')
        except:
            messages.error(request, 'Username or Password is incorrect')
            return render(request, 'login.html')


def logout(request):
    try:
        del request.session['auth_login']
        del request.session['user_id']
    except KeyError:
        pass
    return render(request, 'logout.html')


def dashboard(request):
    data = get_dashboard_data(USER_ID)
    return render(request, 'dashboard.html', {'data': data})


def register_customer(request):
    if request.method == 'POST':
        if 'cancel' in request.POST: return redirect('dashboard')
        instance = Customer(user_map_id=USER_ID)
        form_basic = CustomerForm(data=request.POST, instance=instance)
        form_status = CustomerStatusForm(request.POST)
        if form_basic.is_valid() and form_status.is_valid():
            try:
                form_basic = form_basic.save(commit=True)
                instance = CustomerStatus(customer=form_basic, status=request.POST.get('status'))
                CustomerStatusForm(data=request.POST, instance=instance).save(commit=True)
                messages.success(request, 'Successfully Registered')
                return redirect('dashboard')
            except Exception as err:
                messages.error(request, 'Something Went Wrong :' + str(err))
                return redirect('dashboard')
    else:
        form_basic = CustomerForm()
        form_status = CustomerStatusForm()
    return render(request, 'register.html', {'form_basic': form_basic, 'form_status': form_status})


def get_all_customers(request):
    if request.method == 'GET':
        instance_objects = CustomerStatus.objects.filter(customer__user_map_id=USER_ID).select_related() \
            .order_by('-customer__created_at')
        return render(request, 'view_all_customers.html', {'objects': instance_objects})
    return redirect('dashboard')


def get_customer_details(request, customer_id):
    instance_object = CustomerStatus.objects.filter(customer__id=customer_id).select_related()
    return render(request, 'customer_profile.html', {'object': instance_object[0]})


def error404(request, exception):
    return render(request, 'error_404.html')


def error500(request):
    return render(request, 'error_500.html')
