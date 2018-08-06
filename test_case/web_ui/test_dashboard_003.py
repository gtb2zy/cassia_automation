# coding:utf-8
import unittest
from UiTest import UiTest


class testDashboard(UiTest):

    def setUp(self):
        UiTest._init(self)

    def tearDown(self):
        self.bs.quit()

    def test_user_help(self):
        self.login()
        self.bs.find_element_by_class_name('user-help').click()
        self.bs.switch_to.frame(self.bs.find_element_by_tag_name('iframe'))
        tips = self.bs.find_elements_by_class_name('help_tip')
        print(len(tips))
        if len(tips) == 10:
            self.bs.switch_to.default_content()
        else:
            self.save_png(self._testMethodName)
            self.fail("帮助页面打开失败，请检查截图文件('logs/screen_shot/')")
        div = self.bs.find_element_by_class_name('modal-footer')
        div.find_element_by_tag_name('button').click()


if __name__ == '__main__':
    unittest.main()
