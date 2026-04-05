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
