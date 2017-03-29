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
import threading
from . import  scrapDogCatInWeibo
from .data import mongo
import requests
def index(request):
    return render(request,'index.html')

threadLock = threading.Lock()
class scrapThread(threading.Thread):
    def __init__(self,keyword):
        threading.Thread.__init__(self)
        self.keyword = keyword
    def run(self):
        threadLock.acquire()
        s1 = scrapDogCatInWeibo.searchDogAndCatInWeibo(self.keyword)
        s1.initDriver()
        threadLock.release()
@csrf_exempt
def area(request):
    collection = mongo.pethosdb.pethos_citycode
    #get all provinces
    provinces = list(collection.find({'citycode':''}))
    context = {'provinces':provinces}
    return render(request, 'area.html',context)
@csrf_exempt
def getCitiesInProvince(request):
    collection = mongo.pethosdb.pethos_citycode
    adcode = request.GET.get('adcode')
    #get all cities in province
    cities = list(collection.find({'superioradcode':adcode}))
    imeilires = Imeili100Result()
    imeilires.status = Imeili100ResultStatus.ok.value
    imeilires.res = json.loads(bson.json_util.dumps(cities))
    return HttpResponse(json.dumps(imeilires.__dict__,ensure_ascii=False))
@csrf_exempt
def getAreaInCity(request):
    collection = mongo.pethosdb.pethos_citycode
    citycode = request.GET.get('citycode')
    #get all cities in province
    cities = list(collection.find({'citycode':citycode,'superioradcode':''}))
    imeilires = Imeili100Result()
    imeilires.status = Imeili100ResultStatus.ok.value
    imeilires.res = json.loads(bson.json_util.dumps(cities))
    return HttpResponse(json.dumps(imeilires.__dict__,ensure_ascii=False))
@csrf_exempt
def getHospitalInArea(request):
    adcode = request.GET.get('adcode')
    page = 1
    global count
    count = 0
    global pagecount
    pagecount = 0
    url = 'http://restapi.amap.com/v3/place/text?&types=090700|090701|090702&city=' + adcode + '&offset=20&page=' + str(
        page) + '&key=419afc90cd35b470b9f0cc90144757ef&extensions=all'
    if page == 1:
        r = requests.request('GET', url)
        jsontext = r.text
        dict = json.loads(jsontext)
        count = int(dict['count'])
        pagecount = count / 20 if count % 20 == 0 else int(count / 20) + 1
        page += 1
        dict['adcode'] = adcode
        insertpetshos(dict)
    while (page <= pagecount):
        r = requests.request('GET', url)
        jsontext = r.text
        dict = json.loads(jsontext)
        page += 1
        dict['adcode'] = adcode
        insertpetshos(dict)
        time.sleep(4)
def insertpetshos(dict):
    mongo.pethosdb.pethos_hospital.insert_one(dict)
@csrf_exempt
def scrapweibo(request):
    s1 = scrapDogCatInWeibo.searchDogAndCatInWeibo("猫咪")
    s1.initDriver()
    # t1 = scrapThread("猫咪")
    # t1.start()
    # t2 = scrapThread("哈士奇")
    # t2.start()
    # t3 = scrapThread("金毛")
    # t3.start()
    # t4 = scrapThread("狗狗")
    # t4.start()
    imeilires = Imeili100Result()
    imeilires.status = Imeili100ResultStatus.ok.value
    return HttpResponse(json.dumps(imeilires.__dict__, ensure_ascii=False))

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
    weibos = list(collection.find({'timestamp':{"$gte":int(float(startTime)),"$lte":int(float(endTime))}}))
    jsonlist = bson.json_util.dumps(weibos)
    imeilires = Imeili100Result()
    imeilires.status = Imeili100ResultStatus.ok.value
    imeilires.res = json.loads(jsonlist)
    return HttpResponse(json.dumps(imeilires.__dict__,ensure_ascii=False))

