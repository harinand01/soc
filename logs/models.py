from django.db import models

class RequestLog(models.Model):
    user = models.CharField(max_length=255, default='anonymous')
    ip = models.CharField(max_length=255, null=True, blank=True)
    path = models.CharField(max_length=1024)
    method = models.CharField(max_length=10)
    status = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.ip} - {self.path}"
