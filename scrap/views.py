from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import time
from .data import mongo as weibodata
from .data.Imeili100Result import Imeili100Result,Imeili100ResultStatus
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
import pymongo
import json
import bson.json_util
def index(request):
    return render(request,'index.html')

@csrf_exempt
def fetchWeibo(request):
    page = 0
    startTime = time.time()
    endTime = time.time()
    if request.method == 'GET':
        page = request.GET.get('page', 0)
        startTime = request.GET.get('startTime', time.time())
        endTime = request.GET.get('endTime', time.time())
    elif request.method == 'POST':
        page = request.POST.get('page', 0)
        startTime = request.POST.get('startTime', time.time())
        endTime = request.POST.get('endTime', time.time())
    collection = weibodata.db['hotweibo']
    print(type(startTime))
    weibos = list(collection.find({'timestamp':{"$gte":int(float(startTime)),"$lte":int(float(endTime))}}))
    jsonlist = bson.json_util.dumps(weibos)
    imeilires = Imeili100Result()
    imeilires.status = Imeili100ResultStatus.ok.value
    imeilires.res = json.loads(jsonlist)
    return HttpResponse(json.dumps(imeilires.__dict__,ensure_ascii=False))
