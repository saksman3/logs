from django.contrib import admin
from network_logs.models import Log, Server

admin.site.register(Log)
admin.site.register(Server)
