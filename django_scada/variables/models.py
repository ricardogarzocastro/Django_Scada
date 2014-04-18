from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import utc
# Create your models here.

class Variable (models.Model):
    user = models.ForeignKey(User)
    server = models.CharField(max_length = 128)
    node = models.CharField(max_length = 128)
    name = models.CharField(max_length = 128)
    value = models.CharField(max_length = 128)
    quality = models.CharField(max_length = 128)
    data_type = models.CharField(max_length = 128)
    access_rights = models.CharField(max_length = 128)
    display = models.NullBooleanField(default=True, null=True)
    def __unicode__(self):
        return self.name        
  
class TimeSeries(models.Model):
    server = models.CharField(max_length = 128)
    name = models.CharField(max_length = 128)
    value = models.CharField(max_length = 128)
    time = models.DateTimeField(blank=True)
    def __unicode__(self):
        return self.name   
        