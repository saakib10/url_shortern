from datetime import datetime
from .serializer import UrltSerializer
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect,Http404,HttpResponseForbidden
from rest_framework.views import APIView
from .forms import ShortenerForm 
from .models import Shortener
from django.utils import timezone
from rest_framework.response import Response
import requests

class ApiForUrlList(APIView):
    
    def get(self,request,):
        data = Shortener.objects.all()
        serialize = UrltSerializer(data, many= True)

        return Response(serialize.data)
    
    def post(self):
        pass

def home_view(request):
    template = 'app_short/home.html'

    context = {}
    context['form'] = ShortenerForm()
    update_url_status()

    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':

        used_form = ShortenerForm(request.POST)

        if used_form.is_valid():
            shortened_object = used_form.save()
            new_url = request.build_absolute_uri('/') + shortened_object.short_url
            long_url = shortened_object.long_url
            context['new_url']  = new_url
            context['long_url'] = long_url
             
            return render(request, template, context)

        context['errors'] = used_form.errors

        return render(request, template, context)

def redirect_url_view(request, shortened_part):
    if request.user.is_authenticated:
        update_url_status()
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.times_followed += 1   
        shortener.save()
        if shortener.status == "enable": 
            return HttpResponseRedirect(shortener.long_url)
        else:
            raise Http404('Sorry this link is Expires :(')
    else:
        return HttpResponseForbidden('NOT AUTHENTICATED')

#URL List API Data Process
def render_api_data(request):
    urls = requests.get(f"{request.build_absolute_uri('/')}url_api/").json()
    context = {"urls" : urls, "act" : request.build_absolute_uri('/')}
    update_url_status()
    return render(request,"url_list.html",context)


def update_url_status():
    urls = Shortener.objects.all().filter(status = "enable")
    for url in urls:
        shortener = Shortener.objects.get(short_url = url.short_url)
        now = timezone.now()
        
        if now > shortener.active_time:
            shortener.status = "disable"
        shortener.save()