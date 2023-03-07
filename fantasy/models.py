import datetime
import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    class_year = models.CharField(max_length=20)
    year = models.IntegerField()
    position = models.CharField(max_length=50)
    number = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    team = models.CharField(max_length=100)



