from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from users.forms import CustomerForm, CustomerStatusForm
from users.models import CustomerStatus, Customer, UserAuth, User
from users.validation import get_dashboard_data, is_authenticated, edit_customer_details_post, edit_customer_details_get


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            instance_user_auth = UserAuth.objects.get(username=username, password=password)
            if request.POST.get('stay_login'):
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(600)
            request.session['user_id'] = instance_user_auth.user.id
            request.session['user_token'] = instance_user_auth.token
            return redirect('dashboard')
        except ObjectDoesNotExist:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'login.html')


def logout(request):
    if not is_authenticated(request): redirect('user_login')
    try:
        del request.session['user_token']
        del request.session['user_id']
    except KeyError:
        pass
    return render(request, 'logout.html')


def dashboard(request):
    if not is_authenticated(request): return redirect('user_login')
    user_id = request.session['user_id']
    data = get_dashboard_data(user_id)
    return render(request, 'dashboard.html', {'data': data})


def register_customer(request):
    if not is_authenticated(request): return redirect('user_login')
    user_id = request.session['user_id']
    page = 'register'
    if request.method == 'POST':
        if 'cancel' in request.POST: return redirect('dashboard')
        instance = Customer(user=User.objects.get(id=user_id))
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
    return render(request, 'register.html', {'form_basic': form_basic, 'form_status': form_status, 'page': page})


def get_all_customers(request):
    if not is_authenticated(request): return redirect('user_login')
    user_id = request.session['user_id']
    if request.method == 'GET':
        instance_objects = CustomerStatus.objects.filter(customer__user=user_id).select_related() \
            .order_by('customer__name')
        return render(request, 'view_all_customers.html', {'objects': instance_objects})
    return redirect('dashboard')


def get_customer_details(request, customer_id):
    if not is_authenticated(request): return redirect('user_login')
    user_id = request.session['user_id']
    instance_object = CustomerStatus.objects.filter(customer__id=customer_id).select_related()
    return render(request, 'customer_profile.html', {'object': instance_object[0]})


def edit_customer_details(request, customer_id, edit_type):
    if not is_authenticated(request): return redirect('user_login')
    user_id = request.session['user_id']
    if request.method == 'POST':
        if 'cancel' in request.POST: return redirect('get_customer_details', customer_id=customer_id)
        return edit_customer_details_post(request, customer_id, edit_type)
    else:
        return edit_customer_details_get(request, customer_id, edit_type)


def delete_customer_details(request, customer_id):
    if not is_authenticated(request): return redirect('user_login')
    user_id = request.session['user_id']
    try:
        instance_object = Customer.objects.filter(id=customer_id).delete()
        messages.success(request,'Customer deleted successfully')
        return redirect('get_all_customers')
    except Exception:
        messages.error(request, 'Something went wrong')
        return redirect('get_customer_details', customer_id=customer_id)


def error404(request, exception):
    return render(request, 'error_404.html')


def error500(request):
    return render(request, 'error_500.html')
