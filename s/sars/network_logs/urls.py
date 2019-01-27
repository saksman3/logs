from django.conf.urls import url
from . import views

app_name = 'network_logs'

urlpatterns = [
 url(r'^$', views.IndexView.as_view(), name="index"),

  ## url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),
 url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),
# url(r'send/(?P<pk>[0-9]+)/$',views.send,name='send'),
 url(r'^(?P<pk>[0-9]+)/listing/$',views.search_listing, name="listing"),
 #url(r'^(?P<pk>[0-9]+)/detail/$',views.detail,name='detail'),
 url(r'^(?P<pk>[0-9]+)/search/$',views.LogSearchList.as_view(), name="listing"),
 #url(r'^look/$',views.lookup, name="lookup"),
 # url(r'^searchServer/$',views.searchServer),
 url(r'^filter/$',views.Filter, name='filter'),
]
