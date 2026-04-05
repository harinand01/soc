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
