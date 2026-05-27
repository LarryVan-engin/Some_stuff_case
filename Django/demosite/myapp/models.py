from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=100)
    describtion = models.TextField(blank=True)

class Device(models.Model):
    STATUS_CHOICES = [
        ('offline', 'Offline'),
        ('online', 'Online'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    create_at = models.DateTimeField(default=timezone.now)

# Create your models here.
class SensorData(models.Model):

    SENSOR_DATA = [
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('light', 'Light'),
    ]
    sensor_type = models.CharField(max_length=20, choices=SENSOR_DATA)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

class LightStatus(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    is_on = models.BooleanField(default=False)
    brightness = models.IntegerField(default=0)  # Brightness level from 0 to 100

    def toggle(self):
        self.is_on = not self.is_on
        self.save()
        return self.is_on
    
