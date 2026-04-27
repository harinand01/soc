from django.shortcuts import render, redirect
import os
import re
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from logs.models import RequestLog

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
        RequestLog.objects.all().delete()
        return redirect('logs_index')
    logs = get_logs()
    total_logs = len(logs)
    return render(request, 'logs.html', {'logs': logs, 'total_logs': total_logs})

@csrf_exempt
def receive_log(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received log:", data)
            
            required_fields = ['user', 'ip', 'path', 'method', 'status']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return JsonResponse(
                    {"status": "warning", "message": f"Missing required fields: {', '.join(missing_fields)}"},
                    status=400
                )
            
            user = data.get('user', 'anonymous')
            ip = data.get('ip', '0.0.0.0')
            path = data.get('path', '')
            method = data.get('method', '')
            status = data.get('status', 200)

            RequestLog.objects.create(
                user=user,
                ip=ip,
                path=path,
                method=method,
                status=status
            )
            return JsonResponse({"message": "log received"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

def get_logs_api(request):
    if request.method == 'GET':
        logs = RequestLog.objects.all().order_by('-timestamp')[:50]
        data = [{
            'user': log.user,
            'ip': log.ip,
            'path': log.path,
            'method': log.method,
            'status': log.status,
            'timestamp': log.timestamp.isoformat(),
        } for log in logs]
        return JsonResponse({'logs': data})
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
