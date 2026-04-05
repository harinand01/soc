from django.shortcuts import render, redirect
import os
import re
from django.conf import settings
from alerts.models import Alert
from incidents.models import Incident
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def auto_detect(request):
    new_alerts = False
    log_file = r'C:\soc_logs\logs.txt'
    log_count = 0
    if os.path.exists(log_file):
        failed_logins = defaultdict(int)
        with open(log_file, 'r') as f:
            lines = f.readlines()
            log_count = len(lines)
            for line in lines:
                evt_msg = line.strip().lower()
                if 'failed' in evt_msg:
                    ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                    if ip_match:
                        ip = ip_match.group(0)
                        failed_logins[ip] += 1
                        print(f"[DEBUG] Failed attempt from {ip}. Total: {failed_logins[ip]}")
        
        for ip, count in failed_logins.items():
            print(f"[DEBUG] Final count for IP {ip}: {count}")
            if count >= 5:
                print(f"[DEBUG] Detection triggered for IP {ip}!")
                alert, created = Alert.objects.get_or_create(
                    ip_address=ip,
                    attack_type='Brute Force',
                    defaults={'severity': 'High'}
                )
                if created:
                    Incident.objects.create(alert=alert)
                    new_alerts = True
    
    return JsonResponse({'new_alerts': new_alerts, 'log_count': log_count})

@login_required
def index(request):
    results = []
    if request.method == 'POST':
        log_file = r'C:\soc_logs\logs.txt'
        if os.path.exists(log_file):
            failed_logins = defaultdict(int)
            with open(log_file, 'r') as f:
                for line in f.readlines():
                    evt_msg = line.strip().lower()
                    if 'failed' in evt_msg:
                        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                        if ip_match:
                            ip = ip_match.group(0)
                            failed_logins[ip] += 1
                            print(f"[DEBUG] Failed attempt from {ip}. Total: {failed_logins[ip]}")
            
            for ip, count in failed_logins.items():
                print(f"[DEBUG] Final count for IP {ip}: {count}")
                if count >= 5:
                    print(f"[DEBUG] Detection triggered for IP {ip}!")
                    alert, created = Alert.objects.get_or_create(
                        ip_address=ip,
                        attack_type='Brute Force',
                        defaults={'severity': 'High'}
                    )
                    if created:
                        Incident.objects.create(alert=alert)
                        results.append(f"Detected Brute Force from {ip} ({count} attempts). Alert generated.")
        
        if not results:
            results.append("No new threats detected.")
            
    return render(request, 'detection.html', {'results': results})
