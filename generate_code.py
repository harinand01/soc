import os

base_dir = r"c:\uknown"

def write(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# urls.py main
write("mini_soc/urls.py", """
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('logs/', include('logs.urls')),
    path('detection/', include('detection.urls')),
    path('alerts/', include('alerts.urls')),
    path('incidents/', include('incidents.urls')),
    path('reports/', include('reports.urls')),
]
""")

# alerts models
write("alerts/models.py", """
from django.db import models

class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    ip_address = models.GenericIPAddressField()
    attack_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attack_type} from {self.ip_address}"
""")

write("alerts/admin.py", """
from django.contrib import admin
from .models import Alert
admin.site.register(Alert)
""")

# incidents models
write("incidents/models.py", """
from django.db import models
from alerts.models import Alert

class Incident(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]
    alert = models.OneToOneField(Alert, on_delete=models.CASCADE, related_name='incident')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Incident for {self.alert.attack_type}"
""")

write("incidents/admin.py", """
from django.contrib import admin
from .models import Incident
admin.site.register(Incident)
""")

# urls for all apps
apps = ['dashboard', 'logs', 'detection', 'alerts', 'incidents', 'reports']
for app in apps:
    write(f"{app}/urls.py", f"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='{app}_index'),
]
""")

# Views
write("dashboard/views.py", """
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
""")

write("logs/views.py", """
from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required

def get_logs():
    log_file = os.path.join(settings.BASE_DIR, 'logs.txt')
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for line in f.readlines()[-100:]:  # Read last 100 logs
                parts = line.strip().split('|')
                if len(parts) == 4:
                    logs.append({
                        'timestamp': parts[0],
                        'ip': parts[1],
                        'event': parts[2],
                        'status': parts[3]
                    })
    return list(reversed(logs))

@login_required
def index(request):
    if request.method == 'POST' and 'clear' in request.POST:
        log_file = os.path.join(settings.BASE_DIR, 'logs.txt')
        if os.path.exists(log_file):
            open(log_file, 'w').close()
        return redirect('logs_index')
    return render(request, 'logs.html', {'logs': get_logs()})
""")

write("detection/views.py", """
from django.shortcuts import render, redirect
import os
from django.conf import settings
from alerts.models import Alert
from incidents.models import Incident
from collections import defaultdict
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    results = []
    if request.method == 'POST':
        log_file = os.path.join(settings.BASE_DIR, 'logs.txt')
        if os.path.exists(log_file):
            failed_logins = defaultdict(int)
            with open(log_file, 'r') as f:
                for line in f.readlines():
                    parts = line.strip().split('|')
                    if len(parts) == 4 and parts[2] == 'Login' and parts[3] == 'Failed':
                        failed_logins[parts[1]] += 1
            
            for ip, count in failed_logins.items():
                if count >= 5:
                    alert, created = Alert.objects.get_or_create(
                        ip_address=ip,
                        attack_type='Brute Force Login',
                        defaults={'severity': 'High'}
                    )
                    if created:
                        Incident.objects.create(alert=alert)
                        results.append(f"Detected Brute Force from {ip} ({count} attempts). Alert generated.")
        
        if not results:
            results.append("No new threats detected.")
            
    return render(request, 'detection.html', {'results': results})
""")

write("alerts/views.py", """
from django.shortcuts import render
from .models import Alert
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    alerts = Alert.objects.order_by('-timestamp')
    return render(request, 'alerts.html', {'alerts': alerts})
""")

write("incidents/views.py", """
from django.shortcuts import render, redirect
from .models import Incident
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == 'POST':
        incident_id = request.POST.get('incident_id')
        status = request.POST.get('status')
        notes = request.POST.get('notes')
        
        try:
            incident = Incident.objects.get(id=incident_id)
            incident.status = status
            incident.notes = notes
            incident.save()
        except Incident.DoesNotExist:
            pass
        return redirect('incidents_index')

    incidents = Incident.objects.select_related('alert').order_by('-created_at')
    return render(request, 'incidents.html', {
        'incidents': incidents,
        'status_choices': Incident.STATUS_CHOICES
    })
""")

write("reports/views.py", """
from django.shortcuts import render
from alerts.models import Alert
from django.contrib.auth.decorators import login_required
import json

@login_required
def index(request):
    # Analytics data for Chart.js
    severities = ['Low', 'Medium', 'High', 'Critical']
    severity_counts = [Alert.objects.filter(severity=s).count() for s in severities]
    
    top_ips_query = Alert.objects.values('ip_address')
    ip_counts = {}
    for entry in top_ips_query:
        ip_counts[entry['ip_address']] = ip_counts.get(entry['ip_address'], 0) + 1
        
    sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_ips_labels = [ip[0] for ip in sorted_ips]
    top_ips_data = [ip[1] for ip in sorted_ips]

    context = {
        'severity_labels': json.dumps(severities),
        'severity_data': json.dumps(severity_counts),
        'ips_labels': json.dumps(top_ips_labels),
        'ips_data': json.dumps(top_ips_data)
    }
    return render(request, 'reports.html', context)
""")

# Create base dummy logs
write("logs.txt", """
2023-10-25 10:00:01|192.168.1.5|Login|Success
2023-10-25 10:05:12|10.0.0.15|Login|Failed
2023-10-25 10:05:15|10.0.0.15|Login|Failed
2023-10-25 10:05:17|10.0.0.15|Login|Failed
2023-10-25 10:05:19|10.0.0.15|Login|Failed
2023-10-25 10:05:22|10.0.0.15|Login|Failed
2023-10-25 10:10:00|192.168.1.20|Data Read|Success
2023-10-25 10:12:00|172.16.0.50|Login|Failed
2023-10-25 10:12:10|172.16.0.50|Login|Failed
2023-10-25 10:15:00|192.168.1.5|Logout|Success
""")

print("Done generating code.")
