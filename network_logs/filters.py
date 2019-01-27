from network_logs.models import *
from django import forms
import django_filters

class LogFilter(django_filters.FilterSet):
    # logDate = django_filters.NumberFilter( lookup_expr='year')
    # log_desc = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Log
        fields = ['logID','log_desc',]
class log_Filter(django_filters.FilterSet):
    log_desc = django_filters.CharFilter(lookup_expr='icontains')
    logDate = django_filters.DateFilter("logDate")
    class Meta:
        model = Log
        fields = ['logDate','log_desc']
class ServerFilter(django_filters.FilterSet):
    class Meta:
        model = Server
        fields = ['serverID','server_name']
