from django.contrib import admin
from django.urls import path, include
from logs import views as logs_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('logs/', include('logs.urls')),
    path('api/logs/', logs_views.api_receive_log, name='api_receive_log'),
    path('detection/', include('detection.urls')),
    path('alerts/', include('alerts.urls')),
    path('incidents/', include('incidents.urls')),
    path('reports/', include('reports.urls')),
]
