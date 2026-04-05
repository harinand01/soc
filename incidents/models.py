from django.db import models
from alerts.models import Alert

class Incident(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]
    alert = models.OneToOneField(Alert, on_delete=models.CASCADE, related_name='incident')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Incident for {self.alert.attack_type}"
