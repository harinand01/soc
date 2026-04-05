from django.shortcuts import render
from alerts.models import Alert
from incidents.models import Incident
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    total_alerts = Alert.objects.count()
    high_alerts = Alert.objects.filter(severity__in=['High', 'Critical']).count()
    open_incidents = Incident.objects.filter(status='Open').count()
    recent_alerts = Alert.objects.order_by('-timestamp')[:5]
    
    return render(request, 'dashboard.html', {
        'total_alerts': total_alerts,
        'high_alerts': high_alerts,
        'open_incidents': open_incidents,
        'recent_alerts': recent_alerts,
    })
