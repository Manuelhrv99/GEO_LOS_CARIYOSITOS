from django.db import models

# Create your models here.

class Transport(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Code = models.CharField(max_length=10)
    Transport = models.CharField(max_length=100)
    Longitude = models.FloatField()
    Latitude = models.FloatField()
    Station = models.CharField(max_length=100)
    District_Name = models.CharField(max_length=200)
    Neighborhood_Name = models.CharField(max_length=200)

class Poblaciones(models.Model):
    Latitud = models.FloatField()
    Longitud = models.FloatField()