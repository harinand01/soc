from django.shortcuts import render, redirect
import os
import re
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def get_logs():
    log_file = r'C:\soc_logs\logs.txt'
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    is_error = 'fail' in line.lower() or 'error' in line.lower()
                    logs.append({'text': line, 'is_error': is_error})
    return list(reversed(logs))

@login_required
def index(request):
    if request.method == 'POST' and 'clear' in request.POST:
        log_file = r'C:\soc_logs\logs.txt'
        if os.path.exists(log_file):
            open(log_file, 'w').close()
        return redirect('logs_index')
    logs = get_logs()
    total_logs = len(logs)
    return render(request, 'logs.html', {'logs': logs, 'total_logs': total_logs})

@csrf_exempt
def api_receive_log(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event = data.get('event', 'UNKNOWN')
            ip = data.get('ip', '0.0.0.0')
            timestamp = data.get('timestamp', '')
            user = data.get('user')

            log_dir = 'soc_logs'
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, 'logs.txt')

            log_entry = f"[{timestamp}] {event} | IP={ip}"
            if user:
                log_entry += f" | USER={user}"
            log_entry += "\n"

            with open(log_file, 'a') as f:
                f.write(log_entry)

            return JsonResponse({"status": "saved"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)
