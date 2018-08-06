# coding:utf-8
import unittest
import os
import sys
import base64
import json
import requests
from UiTest import UiTest
path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
from tools import read_job_config


def set_header():
    config = read_job_config()
    use_info = config['user'] + ':' + config['pwd']
    # 编码开发者帐号
    encode_info = base64.b64encode(use_info.encode('utf-8'))
    head = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + encode_info.decode("utf-8")
    }
    data = {'grant_type': 'client_credentials'}
    try:
        # 发起请求
        res = requests.post(
            config['host'] + '/oauth2/token',
            data=json.dumps(data),
            headers=head)
        # print(res.text,res.status_code)
        if res.status_code == 200:
            res_body = json.loads(res.text)
            # print(res_body.get("access_token"))
            TOKEN = res_body.get("access_token")
        elif res.status_code == 401:
            print('开发帐号错误')
        elif res.status_code == 400:
            print('API路径错误')
    except Exception as e:
        print(e)
    headers = {
        'Content-Type': 'application/json',
        'version': '1',
        'Authorization': 'Bearer ' + TOKEN
    }
    return headers


def get_online_hubs():
    config = read_job_config()
    headers = set_header()
    res = requests.get(config['host'] + '/cassia/hubs', headers=headers)
    res_hub_info = json.loads(res.text)
    hubs = []
    for i in res_hub_info:
        hubs.append(i['mac'])
    return hubs


class test_dashboard(UiTest):

    def setUp(self):
        UiTest._init(self)

    def tearDown(self):
        self.bs.quit()

    def test_display_of_dashboard(self):
        self.login()
        display_ap = int(self.bs.find_element_by_css_selector('b.online').text)
        geted_ap = len(get_online_hubs())
        if display_ap != geted_ap:
            self.save_png(self._testMethodName)
            self.fail('web显示的AP数量为%d,调用接口获取到的AP数量为%d' % (display_ap, geted_ap))


if __name__ == '__main__':
    unittest.main()
