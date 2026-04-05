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
