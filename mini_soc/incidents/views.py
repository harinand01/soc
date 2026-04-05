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
