# coding:utf-8
from UiTest import UiTest
import unittest
import time


class apPageTest(UiTest):
    """测试AC 路由器页面的stats页面"""

    def setUp(self):
        UiTest._init(self)
        self.bs.maximize_window()
        self.login()
        self.stop_auto_fresh()
        self.bs.find_element_by_css_selector('.ap').click()
        self.bs.implicitly_wait(20)

    def tearDown(self):
        self.bs.quit()

    def test_reboot_ap(self):
        sel = 'div.pure-box table.ap-data tbody tr:first-child td:first-child input'
        self.bs.find_element_by_css_selector(sel).click()
        time.sleep(0.2)
        self.bs.find_element_by_css_selector(
            'button.icon-icon_more.icomoon').click()
        time.sleep(3)
        router = self.bs.find_element_by_css_selector(
            'div.moreOperte div:nth-child(2)')
        print(dir(router))
        print(router.value_of_css_property('size'))
        js = "var event = document.createEvent('MouseEvents');\
                event.initMouseEvent('mouseover',true,true,document.defaultView);\
                arguments[0].dispatchEvent(event);"
        self.bs.execute_script(js, router)
        # self.action.move_to_element_with_offset(router, 1657, 292).perform()
        time.sleep(10)
        self.bs.find_element_by_css_selector(
            'div.itembox div:nth-child(1)').click()
        time.sleep(10)


if __name__ == '__main__':
    unittest.main()
