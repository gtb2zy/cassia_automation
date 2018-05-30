from selenium import webdriver
import sys,os,time
import unittest

driver_path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/webdriver/'
lib_path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
print(lib_path)
sys.path.append(driver_path)
sys.path.append(lib_path)
from ExcelUtil import ExcelUtil
import ddt


# noinspection PyUnreachableCode
@ddt.ddt
class login_test(unittest.TestCase):
    path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/'
    testdata = ExcelUtil(path + 'test_data/web_ui.xlsx').get_single('login')

    def setUp(self):
        self.bs = webdriver.Chrome()

    def tearDown(self):
        self.bs.quit()

    # noinspection PyUnreachableCode,PyUnreachableCode
    @ddt.data(*testdata)
    def test_login_fail(self,values):
        username = str(values['username'])
        password = str(values['password'])
        print(username,password)
        self.bs.get('http://168.168.30.253/')
        a = self.bs.find_element_by_name('username')
        a.send_keys(username)
        self.bs.find_element_by_name('password').send_keys(password)
        self.bs.find_element_by_class_name('pure-button-primary').click()
        if self.bs.find_element_by_class_name(('error')):
            # png_name = self.path + '/logs/screen_shot/' + self._testMethodName + '.png'
            # self.bs.get_screenshot_as_file(png_name)
            pass
        else:
            self.fail('password error tips error!!!')
            png_name = self.path + '/logs/screen_shot/' + self._testMethodName + '.png'
            self.bs.get_screenshot_as_file(png_name)
        time.sleep(1)

if __name__ == '__main__':
    unittest.main(verbosity=2)