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

    def _add_ap(self):
        self.bs.find_element_by_css_selector('button.btn-discover').click()
        time.sleep(0.1)
        sel = 'div#el-ap-discover tr:nth-child(2) td:first-child input.pure-checkbox.btn-chk'
        check = self.bs.find_element_by_css_selector(sel)
        self.mac = check.get_attribute('t-id')
        while not check.is_selected():
            self.click(check)
            time.sleep(0.1)
        time.sleep(0.1)
        self.bs.find_element_by_css_selector('button.btn-add-all').click()

    def _check_added_ap(self):
        find_macs = self.bs.find_elements_by_css_selector(
            'table.ap-data tr td:nth-child(7)')
        macs = [mac.text for mac in find_macs]
        if self.mac in macs:
            print('ap %s added success!' % self.mac)
        else:
            self.save_png(self._testMethodName)
            self.fail('ap %s add failed!' % self.mac)

    def test_add_ap(self):
        self._add_ap()
        self.bs.refresh()
        self._check_added_ap()
        self.bs.refresh()
        self._delete_ap()
        self._check_delete_ap()

    def _check_delete_ap(self):
        self.bs.refresh()
        find_macs = self.bs.find_elements_by_css_selector(
            'table.ap-data tr td:nth-child(7)')
        macs = [mac.text for mac in find_macs]
        print(self.mac)
        if self.mac not in macs:
            print('ap %s deleted success!' % self.mac)
        else:
            self.save_png(self._testMethodName)
            self.fail('ap %s deleted failed!' % self.mac)

    def _delete_ap(self):
        self.bs.refresh()
        aps = self.bs.find_elements_by_css_selector(
            'div.pure-box table.ap-data tbody tr td input')
        for ap in aps:
            mac = ap.get_attribute('t-id')
            if self.mac == mac:
                index = aps.index(ap) + 1
                break
        sel = 'div.pure-box table.ap-data tbody tr:nth-child(%s) td:first-child input' % index
        self.bs.find_element_by_css_selector(sel).click()
        time.sleep(0.1)
        self.bs.find_element_by_css_selector('div#el-ap button.icon-icon_delete').click()
        time.sleep(0.3)
        self.bs.find_element_by_css_selector('div.modal-footer > button.btn-ok').click()


if __name__ == '__main__':
    unittest.main()
