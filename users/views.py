from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from project_gymnasium import settings
from users.forms import CustomerForm, CustomerStatusForm
from users.models import CustomerStatus, Customer, UserAuth, User
from users.validation import get_dashboard_data, is_authenticated, put_customer_post, \
    put_customer_get, get_user_data, post_customer_save, set_login_session


def error404(request, exception):
    return render(request, 'error_404.html')


def error500(request):
    return render(request, 'error_500.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            instance_user_auth = UserAuth.objects.get(username=username, password=password)
            if request.POST.get('stay_login'):
                request.session.set_expiry(None)
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            else:
                request.session.set_expiry(600)
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
            set_login_session(instance_user_auth, request)
            return redirect('dashboard')
        except ObjectDoesNotExist:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'login.html')


def logout(request):
    if not is_authenticated(request): redirect('login')
    try:
        del request.session['user_token']
        del request.session['user_id']
        del request.session['user_name']
        del request.session['user_gym_name']
    except KeyError:
        pass
    return render(request, 'logout.html')


def dashboard(request):
    if not is_authenticated(request): return redirect('login')
    user_id = request.session['user_id']
    data = get_dashboard_data(user_id)
    return render(request, 'dashboard.html', {'data': data, 'user': get_user_data(request)})


def post_customer(request):
    if not is_authenticated(request): return redirect('login')
    user_id = request.session['user_id']
    page = 'register'
    if request.method == 'POST':
        if 'cancel' in request.POST: return redirect('dashboard')
        instance = Customer(user=User.objects.get(id=user_id))
        form_basic = CustomerForm(data=request.POST, instance=instance)
        form_status = CustomerStatusForm(request.POST)
        if form_basic.is_valid() and form_status.is_valid():
            post_customer_save(form_basic, request)
            return redirect('dashboard')
    else:
        form_basic = CustomerForm()
        form_status = CustomerStatusForm()
    return render(request, 'customer_register.html',
                  {'form_basic': form_basic, 'form_status': form_status, 'page': page, 'user': get_user_data(request)})


def get_all_customers(request):
    if not is_authenticated(request): return redirect('login')
    user_id = request.session['user_id']
    if request.method == 'GET':
        instance_objects = CustomerStatus.objects.filter(customer__user=user_id).select_related() \
            .order_by('customer__name')
        return render(request, 'customer_all.html', {'objects': instance_objects, 'user': get_user_data(request)})
    return redirect('dashboard')


def get_customer(request, customer_id):
    if not is_authenticated(request): return redirect('login')
    user_id = request.session['user_id']
    instance_object = CustomerStatus.objects.filter(customer__id=customer_id, customer__user=user_id).select_related()
    return render(request, 'customer_profile.html', {'object': instance_object[0], 'user': get_user_data(request)})


def put_customer(request, customer_id, edit_type):
    if not is_authenticated(request): return redirect('login')
    if request.method == 'POST':
        if 'cancel' in request.POST: return redirect('get_customer', customer_id=customer_id)
        return put_customer_post(request, customer_id, edit_type)
    else:
        return put_customer_get(request, customer_id, edit_type)


def delete_customer(request, customer_id):
    if not is_authenticated(request): return redirect('login')
    user_id = request.session['user_id']
    try:
        Customer.objects.get(id=customer_id, user=user_id).delete()
        messages.success(request, 'Customer deleted successfully')
        return redirect('get_all_customers')
    except ObjectDoesNotExist:
        messages.error(request, 'Something went wrong')
        return redirect('get_customer', customer_id=customer_id)


def get_user(request, user_id):
    if not is_authenticated(request): return redirect('login')
    if user_id == request.session['user_id']:
        instance_object = User.objects.get(id=user_id).__dict__
        return render(request, 'user_profile.html', {'object': instance_object, 'user': get_user_data(request)})
    else:
        messages.error(request, 'Something went wrong')
        return redirect('dashboard')
