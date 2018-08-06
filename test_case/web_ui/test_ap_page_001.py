# coding:utf-8
from UiTest import UiTest
import unittest
import time


class apPageTest(UiTest):
    """测试AC 路由器页面的stats页面filter model功能"""

    def setUp(self):
        UiTest._init(self)
        self.login()
        self._get_models()

    def tearDown(self):
        self.bs.quit()

    def _get_models(self):
        self.bs.find_element_by_css_selector('.ap').click()
        self.bs.implicitly_wait(20)
        self.bs.find_element_by_css_selector(
            'span#filter-ap-model span:first-child').click()
        spans = self.bs.find_elements_by_css_selector('span[class=main]>span')
        spans.pop(0)
        self.models = [span.text for span in spans]

    def test_filter_of_model(self):
        for m in self.models:
            spans = self.bs.find_elements_by_css_selector(
                'span[class=main]>span')
            for s in spans:
                if s.text == m:
                    s.click()
                    time.sleep(0.1)
                    # spans.remove(s)
                    aps = self.bs.find_elements_by_css_selector(
                        'table.pure-table-horizontal.ap-data tr td:nth-child(8)')
                    if len(aps) > 0:
                        for ap in aps:
                            if ap.text != m:
                                self.save_png(self._testMethodName)
                                self.fail('型号过滤出现问题，详细情况请见截图')
                        print('过滤%s成功' % m)
            self.bs.find_element_by_css_selector(
                'span#filter-ap-model span:first-child').click()


if __name__ == '__main__':
    unittest.main()
