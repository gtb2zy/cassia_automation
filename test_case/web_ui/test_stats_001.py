# coding:utf-8
from UiTest import UiTest
import unittest


class statsPageTest(UiTest):
    """测试AC web页面的stats页面元素"""

    def setUp(self):
        UiTest._init(self)
        self.login()

    def tearDown(self):
        self.bs.quit()

    def test_display_of_charts(self):
        self.bs.find_element_by_css_selector('.stats').click()
        self.bs.implicitly_wait(20)
        checkResult = self.bs.find_elements_by_class_name('header')
        print(len(checkResult))
        if len(checkResult) != 5:
            self.fail()


if __name__ == '__main__':
    unittest.main()
