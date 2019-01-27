from rest_framework import serializers
from network_logs.models import *
class ServerSerializer(serializers.ModelSerializer):
    #url=serializers.HyperlinkedIdentityField(view_name="network_logs:server-detail")
    class Meta:
        model = Server
        fields = ('serverID','server_name')

class LogSerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="network_logs:logs-detail")
    class Meta:
        model = Log
        fields = ('logID','logDate','log_desc','serverID')
class ServerDetailSerializer(serializers.ModelSerializer):
     logs =  LogSerializer(many=True)
     class Meta:
         model = Server
         fields = ('serverID','server_name','logs')
