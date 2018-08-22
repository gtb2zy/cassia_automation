# encode:utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import unittest
import os
import time

HOST = 'http://168.168.30.253/'


class UiTest(unittest.TestCase):
    """UI测试基础类，封装通用的测试方法和测试属性
        bs：浏览器对象，每个测试脚本都需要使用该对象
        func login：封装了登录配置的AC的过程，用于简化登录过程
    """

    def _init(self):
        self._username = 'admin'
        self._password = '1q2w#E$R'
        self.bs = webdriver.Chrome()
        self.bs.set_page_load_timeout(20)
        self.action = ActionChains(self.bs)

    def open(self):
        self.bs.get(HOST)
        self.bs.implicitly_wait(10)

    def login(self):
        self.open()
        self.bs.find_element_by_name('username').send_keys(self._username)
        self.bs.find_element_by_name('password').send_keys(self._password)
        self.bs.find_element_by_tag_name('button').click()
        self.bs.implicitly_wait(5)
        try:
            self.bs.find_element_by_link_text(self._username)
            # print('login success')
            return True
        except Exception as e:
            return False

    def save_png(self, classname):
        t = time.asctime().split()
        str_t = '_' + t[2] + '_' + t[3]
        str_t = str_t.replace(':', '_')
        path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/'
        png_name = path + 'logs/screen_shot/' + classname + str_t + '.png'
        self.bs.get_screenshot_as_file(png_name)

    def click(self, ele):
        self.action.click(ele).perform()

    def stop_auto_fresh(self):
        self.bs.find_element_by_css_selector('div.user select').click()
        sel = self.bs.find_element_by_css_selector('div.user select')
        select = Select(sel)
        s = select.select_by_index(3)
        self.click(s)

if __name__ == '__main__':
    test = UiTest()
    test._init()
    test.login()
    test.stop_auto_fresh()

