from django.contrib import admin
from django.urls import path, include
from logs import views as logs_views
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin123'
        )
        return HttpResponse("Admin created")
    return HttpResponse("Admin already exists")

urlpatterns = [
    path('create-admin/', create_admin),
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('logs/', include('logs.urls')),
    path('api/logs/', logs_views.api_receive_log, name='api_receive_log'),
    path('detection/', include('detection.urls')),
    path('alerts/', include('alerts.urls')),
    path('incidents/', include('incidents.urls')),
    path('reports/', include('reports.urls')),
]
