from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import  MongoClient
import pymongo
import  requests
import json
import time
class dianping:

    def __init__(self):
        firefox_capabilities = DesiredCapabilities.CHROME
        firefox_capabilities['marionette'] = True
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        # self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromeDriver")
        self.driver.set_window_size(1920, 1080)
    def godianping(self):
        self.driver.get("http://www.dianping.com/")
import xlrd

client = MongoClient()
db = client['pethos']
collection = db.pethos_citycode
pethos_hospital = db.pethos_hospital
def readexcel():
    data = xlrd.open_workbook("/Users/zhangshijie/Downloads/AMap_API_Table/citys.xlsx")
    table = data.sheet_by_index(1)  # 通过索引顺序获取
    nrows = table.nrows
    ncols = table.ncols

    for i in range(nrows):
        rowlist = table.row_values(i)
        if i >0:
            name = rowlist[0]
            adcode = (rowlist[1])
            citycode = (rowlist[2])
            superioradcode = (rowlist[3])
            if type(superioradcode) != str:
                superioradcode = int(superioradcode)
            collection.insert({'name':name,'adcode':adcode,'citycode':citycode,'superioradcode':superioradcode})
def fetchos():
    # jsonlist = bson.json_util.dumps(weibos)
    citys = list(collection.find({}))
    # lastone =  pethos_hospital.find().sort({'$natural': -1}).limit(1)
    result = pethos_hospital.find().sort([("_id", pymongo.DESCENDING)]).limit(1)

    if True:
        a = 2
        print(id(a))
    print(a)

    if result.count():
        for r in result:
            lastone = r
            break
    else:
        lastone = None
    if lastone != None :
        lastadcode = lastone['adcode']
        lastpage = lastone['pageindex']
        lastpagecount = lastone['pagecount']
        if lastpage == lastpagecount:
            lastadcode = -1
        pagecount = lastpagecount
        page = lastpage
    else:
        lastadcode = -1
    for i in range(len(citys)):

        dict = citys[i]
        adcode = dict['adcode']

        if int(adcode) < int(lastadcode):
            continue
        elif int(adcode) > int(lastadcode):
            page =1
            pagecount = -1
        superioradcode = dict['superioradcode']
        if superioradcode == '' or superioradcode == None:
            continue

        if page == 1:
            url = 'http://restapi.amap.com/v3/place/text?&types=090700|090701|090702&city=' + adcode + '&offset=20&page=' + str(
                page) + '&key=419afc90cd35b470b9f0cc90144757ef&extensions=all'
            r = requests.request('GET', url)
            jsontext = r.text
            dict = json.loads(jsontext)
            count = int(dict['count'])
            dict['adcode'] = adcode
            dict['pageindex'] = page
            pagecount = count/20 if  count%20 == 0 else int(count/20)+1
            dict['pagecount'] = pagecount
            page += 1
            insertpetshos(dict)
        while(page<=pagecount):
            url = 'http://restapi.amap.com/v3/place/text?&types=090700|090701|090702&city=' + adcode + '&offset=20&page=' + str(
                page) + '&key=419afc90cd35b470b9f0cc90144757ef&extensions=all'
            r = requests.request('GET', url)
            jsontext = r.text
            dict = json.loads(jsontext)
            dict['adcode'] = adcode
            dict['pageindex'] = page
            dict['pagecount'] = pagecount
            page += 1

            insertpetshos(dict)
            time.sleep(4)


def insertpetshos(dict):
    pethos_hospital.insert_one(dict)
    # pois = dict['pois']
    # for index in range(len(pois)):
    #     saveDict = {}
    #     poi = pois[index]
    #     address = poi['address']
    #     saveDict['address'] = address
    #     adname = poi['adname']
    #     saveDict['adname'] = adname
    #     alias = poi['alias']
    #     saveDict['alias'] = alias
    #     business_area = poi['business_area']
    #     saveDict['business_area'] = business_area
    #     emaillist = poi['email']
    #     email = ''
    #     for emailIndex in range(len(emaillist)):
    #         email = email + "|"+emaillist[emailIndex]
    #     saveDict['email'] = email
    #     entr_location = poi['entr_location']
    #     saveDict['entr_location'] = entr_location
    #     name = poi['name']
    #     saveDict['name'] = name
    #     pcode = poi['pcode']
    #     saveDict['pcode'] = pcode
    #     photosUrl = ''
    #     photos = poi['photos']
    #     for photoIndex in range(len(photos)):
    #         photosUrl = photosUrl+"|"+photos[photoIndex]['url']
    #     saveDict['photos'] = photosUrl
    #     tel = poi['tel']
    #     saveDict['tel'] = tel
    #     webSiteUrl = ''
    #     websites = poi['website']
    #     for webSiteIndex in range(len(websites)):
    #         webSiteUrl = webSiteUrl +"|"+websites[webSiteIndex]
    #     saveDict['website'] = websites
    #     amapid = poi['id']
    #     saveDict['amapid'] = amapid
    #     print(json.dumps(saveDict))
    #     pethos_hospital.insert(json.dumps(saveDict))





if __name__ == "__main__":
    # readexcel()
    fetchos()
