from django.db.models import Sum

from users.models import CustomerStatus


def get_dashboard_data(user):
    data = {}
    instance_objects = CustomerStatus.objects.filter(customer__user_map_id=user).select_related()
    data.update(active_customers=instance_objects.filter(status=1).count(),
                total_customers=instance_objects.count(),
                total_revenue=instance_objects.aggregate(Sum('fees_paid'))['fees_paid__sum'])
    return data

def auth_login(request):
    return request.session['auth_login']
