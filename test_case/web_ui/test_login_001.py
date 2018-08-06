#coding:utf-8
from selenium import webdriver
import sys
import os
import time
import unittest

lib_path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(lib_path)
from ExcelUtil import ExcelUtil
import ddt

HOST = 'http://168.168.30.253/'

@ddt.ddt
class login_test(unittest.TestCase):
	path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/'
	testdata = ExcelUtil(path + 'test_data/web_ui.xlsx').get_single('login')
	
	def setUp(self):
		self.bs = webdriver.Chrome()
		self.bs.set_page_load_timeout(60)
	
	def tearDown(self):
		self.bs.quit()
	
	@ddt.data(*testdata)
	def test_login_fail(self, values):
		username = str(values['username'])
		password = str(values['password'])
		expect = values['expect_result']
		self.bs.get(HOST)
		self.bs.find_element_by_name('username').send_keys(username)
		self.bs.find_element_by_name('password').send_keys(password)
		self.bs.find_element_by_class_name('pure-button-primary').click()
		if expect == 'fail':
			if not self.bs.find_element_by_class_name(('error')):
				self.fail('Error tips show error!!!')
				png_name = self.path + '/logs/screen_shot/' + self._testMethodName + '.png'
				self.bs.get_screenshot_as_file(png_name)
		elif expect == 'success':
			time.sleep(1)
			url = self.bs.current_url
			if 'dashboard' not in url:
				png_name = self.path + '/logs/screen_shot/' + self._testMethodName + '.png'
				self.bs.get_screenshot_as_file(png_name)
				self.fail('Login jump to dashboard fail!')
		else:
			print('expect result config error!')


if __name__ == '__main__':
	unittest.main(verbosity=2)
