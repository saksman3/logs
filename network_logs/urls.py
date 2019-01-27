from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'server',views.ServerViewSet)
router.register(r'logs',views.LogViewSet,base_name="logs")

app_name = 'network_logs'

urlpatterns = [
 url(r'api/',include(router.urls)),
]
