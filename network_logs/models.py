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
      serverID = models.ForeignKey('Server',related_name="logs", on_delete=models.CASCADE)
      log_desc = models.CharField(max_length=1000,default='----')
      log_time = models.TimeField(default=now)
      def __str__(self):
          return str(self.logID)+' - '+str(self.logDate)

      class Meta:
        unique_together = ('serverID', 'logDate')
        ordering = ['logID']

      def __unicode__(self):
        return '%d: %s' % (self.logID, self.logDate)
