from django.shortcuts import render
from .models import Alert
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    alerts = Alert.objects.order_by('-timestamp')
    return render(request, 'alerts.html', {'alerts': alerts})
