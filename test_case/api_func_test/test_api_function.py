#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @time:2018-7-26
# @Author haidan li
'''
command:使用ddt加载excel的数据实现功能测试。每个接口的正常系和异常系都再excel里面
'''
import json
import os
import sys
import time
import datetime
import unittest
from contextlib import closing
import threading
import tools

path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
import ddt
from ExcelUtil import ExcelUtil
from tools import read_job_config, get_api
from api import api


@ddt.ddt
class test_api(unittest.TestCase):
    conf = read_job_config()
    print('conf---', conf)
    sdk = get_api()
    path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/'
    testdata = ExcelUtil(path + 'test_data/' + conf['data_file'])
    dd = testdata.get_all()
    common_conf = tools.read_common_config()

    def setUp(self):
        self.case_run_flag = None
        # self.timeout_timer = threading.Timer(self.conf['case_timeout'], self.time_out)
        # self.timeout_timer.start()

    @ddt.data(*dd['scandata'])
    def test_scan(self, values):
        print("value111==", values)
        if self.sdk.model.upper().startswith('S'):
            expect_result = values['expect_result_s1000']
        else:
            expect_result = values['expect_result_other']
        print("value==", values)
        filter_duplicates = values['filter_duplicates']
        filter_name = values['filter_name']
        filter_mac = values['filter_mac']
        filter_rssi = values['filter_rssi']
        filter_uuid = values['filter_uuid']
        duration = values['duration']
        if values['chip']:
            chip = values['chip']
        else:
            chip = 0
        if values['active']:
            active = values['active']
        else:
            active = 0
        para = {}
        tmp = ['__name__', 'expect_result_s1000', 'expect_result_other']
        for key in values:
            if values[key] != '' and key not in tmp:
                para[key] = values[key]
        print('para==', para)
        print(len(para))
        interval = 1
        adv_data = '02010605094C696864'
        resp_data = '5094C696864'
        api1 = api(self.common_conf['local_host'], local=True)
        code, msg = api1.start_advertise(0, interval, adv_data, resp_data)
        if code == 200:
            pass
        else:
            self.case_run_flag = 'fail'
            print("start advertise failed code={0},msg={1}".format(code, msg))
            return
        with closing(self.sdk.scan(**para)) as r:
            '''
            该部分主要测试过滤相关参数，也就是说
            进入到这个部分的测试用例全部是开启扫描成功的
            '''
            if r.status_code == 200:
                if len(para) == 3:
                    if filter_duplicates:
                        t = threading.Thread(target=self.filter_duplicates, args=(
                            r, filter_duplicates, active))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif filter_uuid:
                        t = threading.Thread(
                            target=self.filter_uuid, args=(r, filter_uuid, active))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif filter_mac:
                        t = threading.Thread(
                            target=self.filter_mac, args=(r, filter_mac, active))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif filter_rssi:
                        t = threading.Thread(
                            target=self.filter_rssi, args=(r, filter_rssi, active))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif filter_name:
                        t = threading.Thread(
                            target=self.filter_name, args=(r, filter_name, active))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif duration:
                        t = threading.Thread(
                            target=self.duration_test, args=(r, duration, active))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('duration failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('duration case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    # elif active:
                    else:
                        for test_result in r.iter_lines():
                            test_result = str(test_result, encoding='utf8')
                            if test_result.startswith('data'):
                                print('start scan success.')
                                return
                elif len(para) == 4:
                    if (duration and chip) or (duration and active):
                        t = threading.Thread(
                            target=self.duration_test, args=(r, duration))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('duration failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('duration case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    if (filter_duplicates and chip) or (filter_duplicates and active):
                        print("active11==", active)
                        t = threading.Thread(target=self.filter_duplicates, args=(
                            r, filter_duplicates, active))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter_duplicates failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail(
                                    'filter_duplicates case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif filter_duplicates and filter_name:
                        # 过滤条件为filter_duplicates和filter_name，下面分支语句情况类似
                        t = threading.Thread(
                            target=self.filter_duplicates_name, args=(r, filter_name))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run time out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif filter_duplicates and filter_rssi:
                        t = threading.Thread(
                            target=self.filter_duplicates_rssi, args=(r, filter_rssi,))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif filter_name and filter_rssi:
                        t = threading.Thread(target=self.filter_name_rssi, args=(
                            r, filter_name, filter_rssi))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif filter_name and filter_uuid:
                        t = threading.Thread(target=self.filter_name_uuid, args=(
                            r, filter_name, filter_uuid))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                    elif filter_uuid and filter_rssi:
                        t = threading.Thread(target=self.filter_uuid_rssi, args=(
                            r, filter_uuid, filter_rssi))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail('case run tome out.')
                                return
                            else:
                                time.sleep(0.5)
                elif len(para) == 5:
                    if filter_duplicates and filter_name and filter_rssi:
                        t = threading.Thread(target=self.filter_duplicates_name_rssi,
                                             args=(r, filter_rssi, filter_name))
                        t.setDaemon(True)
                        t.start()
                        while True:
                            if self.case_run_flag == 'success':
                                return
                            elif self.case_run_flag == 'fail':
                                self.fail('filter duplicate_name_rssi failed!')
                                return
                            elif self.case_run_flag == 'timeout':
                                self.fail(
                                    'case filter duplicate_name_rssi run tome out.')
                                return
                            else:
                                time.sleep(0.5)
            else:
                print("r.text===", r.text, r.status_code)
                print("result==", expect_result)
                self.assertEqual(r.text, expect_result)

    def duration_test(self, res, duration):
        print('local==', self.conf['local'])
        if self.conf['local'] == 'True':
            if duration:
                # 字符串扫描5s后停止
                if isinstance(duration, str):
                    duration1 = 5
                    print("字符串duration=", duration1)
                # 负数和0  扫描5s后停止
                elif duration <= 0:
                    duration1 = 5
                    print("负数和0 duration=", duration1)
                # 小数位数小于等于3时，会按照设置的时间停止扫描；小数位数大于3时，参数不起效，一直扫描数据
                elif duration > float(str(duration)[:5]):
                    duration1 = None
                    print("小数位数大于3 duration=", duration1)
                else:
                    print("rrr=", round(duration, 3))
                    duration1 = duration
                    print("整数浮点数duration=", duration1)
            else:
                # 不设置duration就是一直可以扫描数据
                duration1 = None
            if duration1:
                d1 = datetime.datetime.now()
                try:
                    for msg in res.iter_lines():
                        continue
                except AttributeError as e:
                    print("error==", e)
                d2 = datetime.datetime.now()
                t = float(((d2 - d1).seconds)) + \
                    float((d2 - d1).microseconds / 1000 / 1000) - 0.5
                if t <= duration1:
                    self.case_run_flag = 'success'
                    return
                else:
                    self.case_run_flag = 'fail'
                    return
            else:
                count = 0
                for msg in res.iter_lines():
                    message = msg.decode()
                    if message.startswith("data"):
                        count += 1
                        # print("chip 0 ", count, message)
                        if count > int(self.conf['unfilter_count']):
                            self.case_run_flag = 'success'
                            return
        else:
            self.case_run_flag = 'success'
            print("AC端不支持duration参数")
            return

    def filter_duplicates_name(self, res, filter_name):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                filters = test_result['bdaddrs'][0][
                    'bdaddr'] + test_result['adData']
                if test_result['name'] == filter_name:
                    if len(tmp) < self.conf['filter_count']:
                        if filters in tmp:
                            self.case_run_flag = 'fail'
                            print('\n', test_result, '\n', tmp)
                            return
                        else:
                            print(test_result)
                            tmp.append(filters)
                    else:
                        self.case_run_flag = 'success'
                        return
                else:
                    self.case_run_flag = 'fail'
                    print('\n', test_result, '\n', tmp)
                    return

    def filter_duplicates_rssi(self, res, filter_rssi):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                filters = test_result['bdaddrs'][0][
                    'bdaddr'] + test_result['adData']
                if len(tmp) < self.conf['filter_count']:
                    if filters in tmp or int(test_result['rssi']) < int(filter_rssi):
                        print(int(test_result['rssi']), '\n', tmp)
                        self.case_run_flag = 'fail'
                        return
                    else:
                        tmp.append(filters)
                        print(test_result)
                else:
                    self.case_run_flag = 'success'
                    return

    def filter_duplicates_name_rssi(self, res, filter_rssi, filter_name):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                filters = test_result['bdaddrs'][0][
                    'bdaddr'] + test_result['adData']
                if test_result['name'] == filter_name:
                    if len(tmp) < self.conf['filter_count']:
                        if filters in tmp or int(test_result['rssi']) < int(filter_rssi):
                            print(int(test_result['rssi']), '\n', tmp)
                            self.case_run_flag = 'fail'
                            return
                        else:
                            tmp.append(filters)
                            print(test_result)
                    else:
                        self.case_run_flag = 'success'
                        return
                else:
                    print(int(test_result['rssi']), '\n',
                          test_result['name'], '\n',  tmp)
                    self.case_run_flag = 'fail'
                    return

    def filter_duplicates(self, res, filter_duplicates, active):
        tmp = []
        print("	def filter_duplicates(self, res,filter_duplicates,active):")
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                print("test_result==", test_result)
                if active == 1:
                    if "adData" in test_result:
                        filters = test_result['bdaddrs'][0][
                            'bdaddr'] + test_result['adData']
                    elif "scanData" in test_result:
                        filters = test_result['bdaddrs'][0][
                            'bdaddr'] + test_result["scanData"]
                else:
                    print("active0==", active)
                    filters = test_result['bdaddrs'][0][
                        'bdaddr'] + test_result['adData']
                if filter_duplicates == 1:
                    # 去重的数据是：mac+adData
                    if len(tmp) < self.conf['filter_count']:
                        if filters in tmp:
                            self.case_run_flag = 'fail'
                            print('\n', test_result, '\n', tmp)
                            return
                        else:
                            print(test_result)
                            tmp.append(filters)
                    else:
                        self.case_run_flag = 'success'
                        return
                else:
                    print("test_result11==", test_result)
                    if len(tmp) < self.conf['unfilter_count']:
                        if filters in tmp:
                            self.case_run_flag = 'success'
                            return
                        else:
                            tmp.append(filters)
                    else:
                        if filters in tmp:
                            self.case_run_flag = 'success'
                            return
                        else:
                            self.case_run_flag = 'fail'
                            return

    def filter_name_rssi(self, res, filter_name, filter_rssi):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                filters = test_result['name']
                if len(tmp) < self.conf['filter_count']:
                    if filters != filter_name or int(test_result['rssi']) < int(filter_rssi):
                        self.case_run_flag = 'fail'
                        print('\n', test_result, '\n', tmp)
                        return
                    else:
                        print(test_result)
                        tmp.append(filters)
                else:
                    self.case_run_flag = 'success'
                    return

    def filter_name_uuid(self, res, filter_name, filter_uuid):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                expect = filter_name + \
                    str(filter_uuid)[2:] + str(filter_uuid)[:2]
                uuid = self.get_uuid(test_result['adData'])
                if uuid:
                    filters = test_result['name'] + uuid
                    if len(tmp) < self.conf['filter_count']:
                        if filters != expect:
                            self.case_run_flag = 'fail'
                            print(filters, expect)
                            return
                        else:
                            tmp.append(filters)
                            print(test_result)
                    else:
                        self.case_run_flag = 'success'
                        return

    def filter_uuid_rssi(self, res, filter_uuid, filter_rssi):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                uuid = self.get_uuid(test_result['adData'])
                sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
                if uuid:
                    filters = uuid
                    if len(tmp) < self.conf['filter_count']:
                        if filters != sort_uuid or int(test_result['rssi']) < int(filter_rssi):
                            print(filters, sort_uuid, '\n',
                                  test_result['rssi'] < filter_rssi)
                            self.case_run_flag = 'fail'
                            return
                        else:
                            tmp.append(filters)
                            print(test_result)
                    else:
                        self.case_run_flag = 'success'
                        return
                else:
                    self.case_run_flag = 'fail'
                    print(test_result)
                    return

    def filter_uuid(self, res, filter_uuid):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                uuid = self.get_uuid(test_result['adData'])
                sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
                if uuid:
                    filters = uuid
                    if len(tmp) < self.conf['filter_count']:
                        if filters != sort_uuid:
                            print('\n', filters, '≠', filter_uuid, '\n')
                            self.case_run_flag = 'fail'
                            return
                        else:
                            tmp.append(filters)
                            print(test_result)
                    else:
                        self.case_run_flag = 'success'
                        return
                else:
                    self.case_run_flag = 'fail'
                    print(test_result)
                    return

    def filter_name(self, res, filter_name):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                filters = test_result['name']
                if len(tmp) < self.conf['filter_count']:
                    if filters != filter_name:
                        print('\n', filters, '≠', filter_name, '\n')
                        self.case_run_flag = 'fail'
                        return
                    else:
                        tmp.append(filters)
                        print(test_result)
                else:
                    self.case_run_flag = 'success'
                    return

    def filter_rssi(self, res, filter_rssi):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                filters = int(test_result['rssi'])
                if len(tmp) < self.conf['filter_count']:
                    if filters < int(filter_rssi):
                        print('\n', filters, '≠', filter_rssi, '\n')
                        self.case_run_flag = 'fail'
                        return
                    else:
                        tmp.append(filters)
                        print(test_result)
                else:
                    self.case_run_flag = 'success'
                    return

    def filter_mac(self, res, filter_mac):
        tmp = []
        for test_result in res.iter_lines():
            test_result = str(test_result, encoding='utf8')
            if test_result.startswith('data'):
                test_result = json.loads(test_result[5:])
                filters = test_result['bdaddrs'][0]['bdaddr']
                if len(tmp) < self.conf['filter_count']:
                    if filters != filter_mac:
                        print('\n', filters, '≠', filter_mac, '\n')
                        self.case_run_flag = 'fail'
                        return
                    else:
                        tmp.append(filters)
                        print(test_result)
                else:
                    self.case_run_flag = 'success'
                    return
    # @ddt.data(*dd['connectdata'])
    # def test_connect(self, values):
    # 	if self.sdk.model.upper().startswith('S'):
    # 		expect_result = values['expect_result_s1000']
    # 	else:
    # 		expect_result = values['expect_result_other']
    # 	device = values['device']
    # 	chip = values['chip']
    # 	try:
    # 		chip = int(chip)
    # 	except Exception as e:
    # 		print(e)
    # 		pass
    # 	types = values['types']
    # 	timeout = values['timeout']
    # 	self.sdk.disconnect_device(device)
    # 	if chip:
    # 		code, body, duration = self.sdk.connect_device(device, types, chip, timeout)
    # 		if body == 'chip is busy':
    # 			time.sleep(3)
    # 			code, body, duration = self.sdk.connect_device(device, types, chip, timeout)
    # 	else:
    # 		code, body, duration = self.sdk.connect_device(device, types, timeout=timeout)
    # 		if body == 'chip is busy':
    # 			time.sleep(3)
    # 			code, body, duration = self.sdk.connect_device(device, types, timeout=timeout)
    # 	test_result = str(code) + ',' + body
    # 	self.assertEqual(test_result, expect_result)
    # 	if int(code) == 200:
    # 		self.sdk.disconnect_device(device)
    # #
    # @ddt.data(*dd['disconnectdata'])
    # def test_disconnect(self, values):
    # 	expect_result = values['expect_result']
    # 	device = values['device']
    # 	timeout = values['timeout']
    # 	code, body = self.sdk.disconnect_device(device, timeout)
    # 	test_result = str(code) + ',' + body
    # 	self.assertEqual(test_result, expect_result)
    # #
    # @ddt.data(*dd['getdevlist'])
    # def test_get_dev_list(self, values):
    # 	expect_result = values['expect_result']
    # 	connect_state = values['connection_state']
    # 	code, _ = self.sdk.get_devices_list(connect_state)
    # 	test_result = int(code)
    # 	self.assertEqual(test_result, int(expect_result))
    #
    # @ddt.data(*dd['discover_service'])
    # def test_discover_service(self, values):
    # 	device = values['device']
    # 	dev_type = values['type']
    # 	service_uuid = values['service_uuid']
    # 	expect_result = values['expect_result']
    # 	i = 0
    # 	while i <= 3:
    # 		self.sdk.connect_device(device, dev_type)
    # 		time.sleep(2)
    # 		if device in self.sdk.get_devices_list('connected')[1]:
    # 			break
    # 		i += 1
    # 	code, body = self.sdk.discovery_services(device, service_uuid)
    # 	test_result = str(code) + ',' + body
    # 	self.assertEqual(test_result, expect_result)
    #
    # @ddt.data(*dd['discover_characs'])
    # def test_discover_characs(self, values):
    # 	device = values['device']
    # 	dev_type = values['type']
    # 	server_uuid = str(values['service_uuid'])
    # 	expect_result = values['expect_result']
    # 	i = 0
    # 	while i <= 3:
    # 		self.sdk.connect_device(device, dev_type)
    # 		time.sleep(2)
    # 		if device in self.sdk.get_devices_list('connected')[1]:
    # 			break
    # 		i += 1
    # 	code, body = self.sdk.discovery_characteristics(device, server_uuid)
    # 	test_result = str(code) + ',' + body
    # 	self.assertEqual(test_result, expect_result)
    #
    # @ddt.data(*dd["discover_charac"])
    # def test_discover_charac(self, values):
    # 	device = values['device']
    # 	dev_type = values['type']
    # 	charac_uuid = values['charac_uuid']
    # 	expect_result = values['expect_result']
    # 	i = 0
    # 	while i <= 3:
    # 		self.sdk.connect_device(device, dev_type)
    # 		time.sleep(2)
    # 		if device in self.sdk.get_devices_list('connected')[1]:
    # 			break
    # 		i += 1
    # 	code, body = self.sdk.discovery_charateristic(device, charac_uuid)
    # 	test_result = str(code) + ',' + body
    # 	self.assertEqual(test_result, expect_result)
    #
    # @ddt.data(*dd['discover_des'])
    # def test_discover_des(self, values):
    # 	device = values['device']
    # 	dev_type = values['type']
    # 	charac_uuid = values['charac_uuid']
    # 	expect_result = values['expect_result']
    # 	i = 0
    # 	while i <= 3:
    # 		self.sdk.connect_device(device, dev_type)
    # 		time.sleep(2)
    # 		if device in self.sdk.get_devices_list('connected')[1]:
    # 			break
    # 		i += 1
    # 	code, body = self.sdk.discover_descriptors(device, charac_uuid)
    # 	test_result = str(code) + ',' + body
    # 	self.assertEqual(test_result, expect_result)
    #
    # @ddt.data(*dd['discover_all'])
    # def test_discover_all(self, values):
    # 	device = values['device']
    # 	dev_type = values['type']
    # 	expect_result = values['expect_result']
    # 	i = 0
    # 	while i <= 3:
    # 		self.sdk.connect_device(device, dev_type)
    # 		time.sleep(2)
    # 		if device in self.sdk.get_devices_list('connected')[1]:
    # 			break
    # 		i += 1
    # 	code, body = self.sdk.discover_all(device)
    # 	if code == 200:
    # 		self.assertEqual(len(body), len(expect_result))
    # 	else:
    # 		test_result = str(code) + ',' + body
    # 		self.assertEqual(test_result, expect_result)
    #
    # @ddt.data(*dd['read_by_handle'])
    # def test_read_by_handle(self, values):
    # 	device = values['device']
    # 	dev_type = values['type']
    # 	handle = values['handle']
    # 	expect_result = values['expect_result']
    # 	i = 0
    # 	while i <= 3:
    # 		self.sdk.connect_device(device, dev_type)
    # 		time.sleep(2)
    # 		if device in self.sdk.get_devices_list('connected')[1]:
    # 			break
    # 		i += 1
    # 	code, body = self.sdk.read_by_handle(device, handle)
    # 	test_result = str(code) + ',' + body
    # 	self.assertEqual(test_result, expect_result)
    #
    # @ddt.data(*dd['write_by_handle'])
    # def test_write_by_handle(self, values):
    # 	device = values['device']
    # 	dev_type = values['type']
    # 	handle = values['handle']
    # 	handle_data = values['handle_data']
    # 	expect_result = values['expect_result']
    # 	i = 0
    # 	while i <= 3:
    # 		self.sdk.connect_device(device, dev_type)
    # 		time.sleep(2)
    # 		if device in self.sdk.get_devices_list('connected')[1]:
    # 			break
    # 		i += 1
    # 	else:
    # 		print('device connected failed!!!')
    # 	code, body = self.sdk.write_by_handle(device, handle, handle_data)
    # 	test_result = str(code) + ',' + body
    # 	self.assertEqual(test_result, expect_result)
    #
    # @ddt.data(*dd['get_connect_state'])
    # def test_get_device_connect_state(self, values):
    # 	self.message = None
    # 	device = values['device']
    # 	types = values['type']
    # 	expect_result = values['expect_result']
    # 	res = self.sdk.get_device_connect_state()
    # 	t = threading.Thread(target=self.recv_message, args=(res,))
    # 	t.setDaemon(True)
    # 	t.start()
    # 	if expect_result == 'connected':
    # 		self.sdk.disconnect_device(device)
    # 		time.sleep(5)
    # 		self.message = None
    # 		code, body, duration = self.sdk.connect_device(device, types, 0, 10000)
    # 		print(code, body)
    # 		while 1:
    # 			if self.time_out_flag:
    # 				self.fail('case time out')
    # 				break
    # 			else:
    # 				if self.message:
    # 					if self.message['handle'] == device:
    # 						self.assertTrue(True)
    # 						self.sdk.disconnect_device(device)
    # 						self.message = None
    # 						break
    # 					else:
    # 						self.assertTrue(False)
    # 						self.sdk.disconnect_device(device)
    # 						self.message = None
    # 						break
    # 	else:
    # 		self.sdk.connect_device(device, types, 0, 10000)
    # 		time.sleep(5)
    # 		self.message = None
    # 		code, body = self.sdk.disconnect_device(device)
    # 		print(code, body)
    # 		while 1:
    # 			if self.time_out_flag:
    # 				self.fail('case time out')
    # 				break
    # 			else:
    # 				if self.message:
    # 					if self.message['handle'] == device:
    # 						self.assertTrue(True)
    # 						self.sdk.disconnect_device(device)
    # 						self.message = None
    # 						break
    # 					else:
    # 						self.assertTrue(False)
    # 						self.sdk.disconnect_device(device)
    # 						self.message = None
    # 						break
    # @ddt.data(*dd['recv_notification'])
    # def test_recive_notification(self, values):
    # 	device = values['device']
    # 	expect_result = values['expect_result']
    # 	dev_type = values['device_type']
    # 	i = 0
    # 	while i <= 3:
    # 		self.sdk.connect_device(device, dev_type)
    # 		time.sleep(2)
    # 		if device in self.sdk.get_devices_list('connected')[1]:
    # 			break
    # 		i += 1
    # 	else:
    # 		self.fail('device connected failed!!!')
    # 		return
    # 	# start Thread to receive notification
    # 	res = self.sdk.recive_notification()
    # 	t = threading.Thread(target=self.recv_message, args=(res,))
    # 	t.setDaemon(True)
    # 	t.start()
    # 	# wtite handle to open device notification
    # 	code, _ = self.sdk.write_by_handle(device, '17', '0100')
    # 	print(1, code)
    # 	if code == '200':
    # 		start_handle = values['start_handle']
    # 		srart_handle_value1 = values['start_handle_value1']
    # 		srart_handle_value2 = values['start_handle_value2']
    # 		stop_handle_value = values['stop_handle_value']
    # 		code, body = self.sdk.write_by_handle(device, start_handle, srart_handle_value1)
    # 		print(2, code, body)
    # 		if code == '200':
    # 			code, _ = self.sdk.write_by_handle(device, start_handle, srart_handle_value2)
    # 			print(3, code)
    # 			if code == '200':
    # 				while 1:
    # 					if self.message:
    # 						print(self.message)
    # 						self.assertEqual(self.message, expect_result)
    # 						self.sdk.write_by_handle(device, start_handle, stop_handle_value)
    # 						break
    # 				return
    # 	self.fail('write handle failed!')

    @staticmethod
    def get_uuid(data):
        start = 0
        head_length = int(data[start:start + 2], 16)
        start = 2 + head_length * 2
        data_length = int(data[start:start + 2], 16)
        start = start + 2
        adv_data = data[start:start + data_length * 2]
        adv_tpye = int(adv_data[0:2], 16)
        if 2 <= adv_tpye <= 7:
            uuid = adv_data[2:]
            # print(uuid)
            return str(uuid)
        else:
            return None

    def recv_message(self, res):
        for msg in res:
            print(msg)
            if msg != ':keep-alive':
                try:
                    self.message = json.loads(msg)
                except:
                    pass

    def time_out(self):
        self.case_run_flag = 'timeout'

    def tearDown(self):
        pass
        # self.timeout_timer.cancel()
if __name__ == '__main__':
    unittest.main(verbosity=2)
