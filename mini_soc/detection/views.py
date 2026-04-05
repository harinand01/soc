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
