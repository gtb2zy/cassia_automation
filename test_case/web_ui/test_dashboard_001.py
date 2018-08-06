# coding:utf-8
from UiTest import UiTest
import unittest


class test_dashboard(UiTest):

    def setUp(self):
        UiTest._init(self)

    def tearDown(self):
        self.bs.quit()

    def test_username_displlay(self):
        self.login()
        username = self._get_login_username()
        self.assertEqual(username, self._username)

    def test_link_of_username(self):
        self.login()
        a = self.bs.find_element_by_class_name(
            'user-profile').find_element_by_tag_name('a')
        url = a.get_attribute('href')
        a.click()
        self.bs.implicitly_wait(5)
        self.assertEqual(url, self.bs.current_url)

    def _get_login_username(self):
        try:
            ele = self.bs.find_element_by_class_name('user-profile')
            username = ele.find_element_by_tag_name('span').text
        except Exception as e:
            print(e)
            username = None
        return username


if __name__ == '__main__':

    unittest.main(verbosity=2)
