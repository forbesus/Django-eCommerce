import datetime

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone

from users.forms import CustomerForm, CustomerStatusForm
from users.models import CustomerStatus, UserAuth, Customer, User


def is_authenticated(request):
    try:
        user_id = request.session['user_id']
        user_token = request.session['user_token']
        UserAuth.objects.get(user__id=user_id, token=user_token)
        return True
    except KeyError:
        messages.info(request, "Please Login First")
        return False
    except ObjectDoesNotExist:
        messages.info(request, "Please Login First")
        return False


def set_login_session(instance_user_auth, request):
    request.session['user_id'] = instance_user_auth.user.id
    request.session['user_token'] = instance_user_auth.token


def get_dashboard_data(user):
    data = {}
    instance_objects = CustomerStatus.objects.filter(customer__user=user).select_related()
    data.update(active_customers=instance_objects.filter(status=1).count(),
                total_customers=instance_objects.count(),
                total_revenue=instance_objects.aggregate(Sum('fees_paid'))['fees_paid__sum'])
    return data


def get_user_data(request):
    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
        user_object = {
            'id': user_id,
            'name': user.name,
            'gym_name': user.gym_name
        }
        return user_object
    except ObjectDoesNotExist:
        del request.session['user_id']
        del request.session['user_token']


def post_customer_save(form_basic, request):
    try:
        form_basic = form_basic.save(commit=True)
        instance = CustomerStatus(customer=form_basic, status=request.POST.get('status'))
        CustomerStatusForm(data=request.POST, instance=instance).save(commit=True)
        messages.success(request, 'Successfully Registered')
    except Exception as err:
        messages.error(request, 'Something Went Wrong :' + str(err))


def put_customer_get(request, customer_id, edit_type):
    page = 'update'
    user_id = request.session['user_id']
    if edit_type == 'basic':
        instance_object_basic = Customer.objects.get(id=customer_id, user=user_id)
        form_basic = CustomerForm(initial=instance_object_basic.__dict__)
        return render(request, 'customer_register.html',
                      {'form_basic': form_basic, 'page': page, 'customer_id': customer_id, 'edit_type': edit_type,
                       'user': get_user_data(request)})
    elif edit_type == 'status':
        instance_object_status = CustomerStatus.objects.get(customer__id=customer_id, customer__user=user_id)
        status = instance_object_status.status
        form_status = CustomerStatusForm(initial=instance_object_status.__dict__)
        return render(request, 'customer_register.html',
                      {'form_status': form_status, 'page': page, 'customer_id': customer_id, 'edit_type': edit_type,
                       'status': status, 'user': get_user_data(request)})


def put_customer_post(request, customer_id, edit_type):
    page = 'update'
    user_id = request.session['user_id']
    if edit_type == 'basic':
        instance_object_basic = Customer.objects.get(id=customer_id, user=user_id)
        updated_instance = get_updated_fields(instance_object_basic.__dict__, request.POST)
        if updated_instance:
            try:
                for attr, val in updated_instance.items():
                    setattr(instance_object_basic, attr, val)
                instance_object_basic.save()
                messages.success(request, 'Customer updated successfully')
            except Exception:
                messages.error(request, 'Something went wrong')
        else:
            messages.info(request, 'Nothing to update')
    elif edit_type == 'status':
        instance_object_status = CustomerStatus.objects.get(customer__id=customer_id, customer__user=user_id)
        updated_instance = get_updated_fields(instance_object_status.__dict__, request.POST)
        if updated_instance:
            updated_instance['updated_at'] = timezone.now()
            try:
                for attr, val in updated_instance.items():
                    setattr(instance_object_status, attr, val)
                instance_object_status.save()
                messages.success(request, 'Customer updated successfully')
            except Exception:
                messages.error(request, 'Something went wrong')
        else:
            messages.info(request, 'Nothing to update')
    return redirect('get_customer', customer_id=customer_id)


def get_updated_fields(current, updated):
    update_dict = {}
    for key, val in current.items():
        u_val = updated.get(key)
        if key in ('dob', 'start_date', 'end_date'):
            u_val = datetime.datetime.strptime(u_val, "%Y-%m-%d").date()
        if key in ('total_fees', 'fees_paid', 'fees_remaining', 'status'):
            u_val = int(u_val)
        if key in updated and val != u_val:
            update_dict.update({key: u_val})
    return update_dict
