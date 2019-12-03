from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=15)
    password = models.CharField(max_length=30)
    isadmin = models.IntegerField(default=0)