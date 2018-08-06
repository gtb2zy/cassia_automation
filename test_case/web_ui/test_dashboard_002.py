# coding:utf-8
import unittest
from UiTest import UiTest


class test_dashboard(UiTest):

    def setUp(self):
        UiTest._init(self)

    def tearDown(self):
        self.bs.quit()

    def test_click_of_nav_menu(self):
        if not self.login():
            print('login failed,test end with error!')
            self.bs.quit()
        for i in range(0, 9):
            li = self.bs.find_elements_by_css_selector(
                '.pure-menu.pure-menu-open li')[i]
            a = li.find_element_by_tag_name('a')
            url = a.get_attribute('href')
            a.click()
            self.bs.implicitly_wait(10)
            if url != self.bs.current_url:
                self.save_png(self._testMethodName)
                self.fail('page jump failed!')


if __name__ == '__main__':

    unittest.main(verbosity=2)
