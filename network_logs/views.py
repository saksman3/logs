from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.core.mail import *
from . models import Log, Server
from network_logs.forms import EmailForm,LogSearchForm
from django.db import connection
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
# Create your views here.
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from .filters import *
from rest_framework import viewsets
from . Serializers import *
from rest_framework.generics import RetrieveAPIView,ListAPIView

class LogDetailAPIView(RetrieveAPIView):
     queryset=Log.objects.all()
     serializer_class = LogSerializer

class ServerDetailAPIView(viewsets.ModelViewSet):
     queryset=Server.objects.all()
     serializer_class = ServerDetailSerializer  

         
class LogViewSet(viewsets.ModelViewSet):
      
      serializer_class = LogSerializer
      def get_queryset(self):
          queryset = Log.objects.all()
          id = self.request.query_params.get('id',None)
          if(id is not None):
              queryset = Log.objects.filter(serverID_id=id)
          return queryset    

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

""" class LogFilter(BaseFilter):
    search_fields = {
        'search_text' : ['log_desc'],
        'search_logid_exact' : { 'operator' : '__exact', 'fields' : ['logID'] },
        'search_logTime' : { 'operator' : '__gte', 'fields' : ['log_time'] },
        'search_logDate' : { 'operator' : '__exact', 'fields' : ['logDate'] },
    }

class LogSearchList(SearchListView):
    model = Log
    template_name = "network_logs\search.html"
    form_class = LogSearchForm
    filter_class = LogFilter
    def get_queryset(self):
        return {'object_list':Log.objects.all()}
    '''def get(self,request,pk):
        servers = Log.objects.filter(serverID_id = pk)
        return render(request, 'network_logs\search.html', {'object_list': servers})'''

def search_listing(request,pk):
    search_string = request.GET.get('search')
    logs_filter = Log.objects.filter(Q(logDate__contains=search_string) & Q(serverID_id=pk))
    paginator = Paginator(logs_filter, 25) # Show 25 contacts per page
    return render(request, 'network_logs\detail.html', {'server': servers})

def detail(request,pk):
    # serverID = Server.objects.get(pk=pk)
    log = Log.objects.filter(serverID_id=pk)
    paginator = Paginator(log, 25)
    page = request.GET.get('page')
    logs = paginator.get_page(page)
    return render(request,'network_logs\detail.html',{'server':logs})

class IndexView(generic.ListView):
      #server_list = Server.objects.all()
      #paginator = Paginator(server_list,25)

      #template_name = "network_logs\index.html"
      def get(self,request):
          server_list = Server.objects.all()
          paginator = Paginator(server_list, 25) # Show 25 contacts per page

          page = request.GET.get('page')
          servers = paginator.get_page(page)
          return render(request, 'network_logs\index.html', {'object_list': servers})

class DetailView(generic.DetailView):
    # template_name = 'network_logs\detail.html'

    def get(self,request,pk):
        log = Log.objects.filter(serverID_id=pk)
        server = Server.objects.get(pk=pk)
        serv_name = server.server_name
        paginator = Paginator(log, 25)
        page = request.GET.get('page')
        logs = paginator.get_page(page)
        count=log.count()

        return render(request,'network_logs\detail.html',{'server':logs,"logs_count":count,"name":serv_name,"id":pk})

    def post(self,request,pk):
        email = request.POST.get('email')
        log = request.POST.get('logID')
        print(email+'-'+log)
        logD = Log.objects.get(pk=log);
        print(logD.log_desc)
        body='<strong style="color:blue;">Log Date: </strong>'+str(logD.logDate)+' '+logD.log_desc
        serv = logD.serverID
        subject = str(logD.logDate)+' '+str(serv)+' '+'- Log'
        send_mail(subject,body,'saksman3@gmail.com',[email],fail_silently=False)
        url =reverse_lazy('network_logs:detail',kwargs={"pk": pk})
        return HttpResponseRedirect(url)

'''    def get(self,request,pk):
        form = EmailForm()
        return render(request,self.template_name,{'form':form})
        send_mail('test','hello these is just a test-mail,','saksman3@gmail.com',['fomawica@bit-degree.com'],fail_silently=False)
def get(request,pk):
    form =EmailForm()
    return render(request,'network_logs\detail.html',{'form':form})'''

def Filter(request):
    filter_filt = log_Filter(request.GET, queryset = Log.objects.all().order_by('logID'))
    paginator = Paginator(filter_filt.qs,25)
    page = request.GET.get('page')
    logs = paginator.get_page(page)

    return render(request, 'network_logs\serv.html',{'logs': logs,'tab':filter_filt})
 """