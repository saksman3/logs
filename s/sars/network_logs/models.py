from django.db import models
from django.utils.timezone import now
# from django.datetime import datetime

# Create your models here.
class Server(models.Model):
      server_name = models.CharField(max_length=100)
      serverID = models.AutoField(primary_key=True)

      def __str__(self):
          return self.server_name


class Log(models.Model):
      logID = models.AutoField(primary_key=True)
      logDate = models.DateField(null=True)
      serverID = models.ForeignKey(Server, on_delete=models.CASCADE)
      log_desc = models.CharField(max_length=1000,default='----')
      log_time = models.TimeField(default=now)
