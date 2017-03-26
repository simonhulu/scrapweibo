
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time
import threading
from pymongo import  MongoClient
import pymongo
class searchDogAndCatInWeibo:

    def __init__(self,keyword):
        self.keyword = keyword

    def initDriver(self):
        self.driver = None;
        client = MongoClient()
        db = client['weibo_dog_cat']
        self.collection = db.hotweibo

        firefox_capabilities = DesiredCapabilities.CHROME
        firefox_capabilities['marionette'] = True
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        # self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromeDriver")
        self.driver.set_window_size(1920, 1080)

        try:

            self.driver.get("http://data.weibo.com/index/realtime")
            # self.login()
            time.sleep(10)
            self.seachKeyw()
            time.sleep(20)
            self.realtime()
            time.sleep(20)
            self.f()


        except Exception as e:
            raise e

    def f(self):
        # do something here ...
        # call f() again in 60 seconds
        try:
            divs = self.driver.find_elements_by_class_name("map-feed")
            if divs != None:
                for i, element in enumerate(divs):
                    tt =  element.find_element_by_class_name("map-feed-con")
                    tta = element.find_element_by_tag_name("a")
                    title = (tt.text)
                    aa = element.find_element_by_class_name("map-feed-go")
                    url = (aa.get_attribute("href"))
                    if self.collection.find_one({'url':url}) == None :
                        try:
                            self.collection.insert_one({'url':url,'title':title,'timestamp':time.time(),'keyword':self.keyword})
                        except Exception as ae:
                            raise ae
                        pass

        except Exception as e:
            raise e


        threading.Timer(6, self.f).start()

    def realtime(self):
        wait = WebDriverWait(self.driver, 60);
        try:
            wait.until(expected_conditions.visibility_of_element_located(By.XPATH,"//a[@href='http://data.weibo.com/index/realtime']"))
        except Exception as e:
            pass
        finally:
            link = self.driver.find_element_by_xpath("//a[@href='http://data.weibo.com/index/realtime']");
            link.click()

    def seachKeyw(self):
        wait = WebDriverWait(self.driver, 600)
        try:
            searchCon = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@node-type='searchCon']")))
            searchInput = searchCon.find_element_by_tag_name("input")
            keyword = "猫咪"
            searchInput.send_keys(keyword)
            self.keyword = keyword
            searchbtn = self.driver.find_element(By.CLASS_NAME, "index-search")
            searchbtn.click()
        except Exception as e:
            raise e
        finally:
            # searchCon = self.driver.find_element_by_xpath("//*[@node-type='searchCon']")
            pass
    def login(self):
        loginBtn = self.driver.find_element_by_xpath("//*[@node-type='loginBtn']")
        loginBtn.click()
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(expected_conditions.visibility_of_element_located((By.NAME,'username')))

        except Exception as e:
            raise e
        finally:
            accountInput = self.driver.find_element_by_name("username")
            passwdInput = self.driver.find_element_by_name("password")
            accountInput.send_keys("tmyk104117@126.com");
            passwdInput.send_keys("153931021zsj")
            loginFrame = self.driver.find_element_by_xpath("//*[@node-type='login_frame']")
            btn = loginFrame.find_element_by_xpath("//*[@node-type='submitBtn']")
            btn.click()

if __name__ == "__main__":
   a =  searchDogAndCatInWeibo("猫咪")
   a.initDriver()