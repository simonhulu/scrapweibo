from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
class dianping:

    def __init__(self):
        firefox_capabilities = DesiredCapabilities.CHROME
        firefox_capabilities['marionette'] = True
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        # self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromeDriver")
        self.driver.set_window_size(1920, 1080)
    def godianping(self):
        self.driver.get("http://www.dianping.com/")
if __name__ == "__main__":

