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
		self.filter_run_flg=None
		self.tmp=[]
		self.tmp_dup=[]
		self.connect_flag=None
		# t1 = threading.Thread(target=self.start_advertise, args=())
		# t1.setDaemon(True)
		# t1.start()
		self.timeout_timer = threading.Timer(self.conf['case_timeout'], self.time_out)
		self.timeout_timer.start()

	# @ddt.data(*dd['scandata'])
	# def test_scan(self, values):
	#     print("value111==", values)
	#     if self.sdk.model.upper().startswith('S'):
	#         expect_result = values['expect_result_s1000']
	#     else:
	#         expect_result = values['expect_result_other']
	#     print("value==", values)
	#     filter_duplicates = values['filter_duplicates']
	#     filter_name = values['filter_name']
	#     filter_mac = values['filter_mac']
	#     filter_rssi = values['filter_rssi']
	#     filter_uuid = values['filter_uuid']
	#     if values['duration'] ==0:
	#         duration=5
	#     else:
	#         duration = values['duration']
	#     if values['chip']:
	#         chip = values['chip']
	#     else:
	#         chip = 0
	#         values['chip']=chip
	#     if values['active']:
	#         active = values['active']
	#     else:
	#         active = 0
	#         values['active']=active
	#     para = {}
	#     tmp = ['__name__', 'expect_result_s1000', 'expect_result_other']
	#     for key in values:
	#         if values[key] != '' and key not in tmp:
	#             para[key] = values[key]
	#     print('para==', para)
	#     print(len(para))
	#     with closing(self.sdk.scan(**para)) as r:
	#         '''
	#         该部分主要测试过滤相关参数，也就是说
	#         进入到这个部分的测试用例全部是开启扫描成功的
	#         '''
	#         print("para===",r.url)
	#         if r.status_code == 200:
	#             if len(para) ==2:
	#                 t = threading.Thread(target=self.chip_active,args=(r,active))
	#                 t.setDaemon(True)
	#                 t.start()
	#                 while True:
	#                     if self.case_run_flag == 'success':
	#                         return
	#                     elif self.case_run_flag == 'fail':
	#                         self.fail('chip_active failed!')
	#                         return
	#                     elif self.case_run_flag == 'timeout':
	#                         self.fail('chip_active case run time out.')
	#                         return
	#                     else:
	#                         time.sleep(0.5)
	#             if len(para) == 3:
	#                 if filter_duplicates:
	#                     t = threading.Thread(target=self.filter_duplicates, args=(
	#                         r, filter_duplicates, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_duplicates failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_duplicates case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif filter_uuid:
	#                     t = threading.Thread(
	#                         target=self.filter_uuid, args=(r, filter_uuid, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif filter_mac:
	#                     t = threading.Thread(
	#                         target=self.filter_mac, args=(r, filter_mac, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_mac failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_mac case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif filter_rssi:
	#                     t = threading.Thread(
	#                         target=self.filter_rssi, args=(r, filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif filter_name:
	#                     t = threading.Thread(
	#                         target=self.filter_name, args=(r, filter_name, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_name failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_name case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif duration:
	#                     t = threading.Thread(
	#                         target=self.duration_test, args=(r, duration, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 # elif active:
	#                 else:
	#                     for test_result in r.iter_lines():
	#                         test_result = str(test_result, encoding='utf8')
	#                         if test_result.startswith('data'):
	#                             print('start scan success.')
	#                             return
	#             elif len(para) == 4:
	#                 if (duration and filter_duplicates):
	#                     t = threading.Thread(
	#                         target=self.duration_filter_duplicates, args=(r, duration,filter_duplicates,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_duplicates failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_duplicates case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_name):
	#                     t = threading.Thread(
	#                         target=self.duration_filter_name, args=(r, duration,filter_name,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_name failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_name case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_mac):
	#                     t = threading.Thread(
	#                         target=self.duration_filter_mac, args=(r, duration,filter_mac,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_mac failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_mac case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_rssi):
	#                     t = threading.Thread(
	#                         target=self.duration_filter_rssi, args=(r, duration,filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_uuid):
	#                     t = threading.Thread(
	#                         target=self.duration_filter_uuid, args=(r, duration,filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_name):
	#                     t = threading.Thread(target=self.filter_duplicates_name, args=(
	#                         r, filter_duplicates, filter_name,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_duplicates_name failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_duplicates_name case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_mac):
	#                     # 过滤条件为filter_duplicates和filter_name，下面分支语句情况类似
	#                     t = threading.Thread(
	#                         target=self.filter_duplicates_mac, args=(r, filter_duplicates,filter_mac,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_duplicates_mac failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_duplicates_mac case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_uuid):
	#                     # 过滤条件为filter_duplicates和filter_name，下面分支语句情况类似
	#                     t = threading.Thread(
	#                         target=self.filter_duplicates_uuid, args=(r, filter_duplicates,filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_duplicates_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_duplicates_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_rssi):
	#                     # 过滤条件为filter_duplicates和filter_name，下面分支语句情况类似
	#                     t = threading.Thread(
	#                         target=self.filter_duplicates_rssi, args=(r, filter_duplicates,filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_duplicates_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_duplicates_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_name and filter_rssi):
	#                     t = threading.Thread(target=self.filter_name_rssi, args=(
	#                         r, filter_name, filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_name_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_name_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_name and filter_mac):
	#                     t = threading.Thread(target=self.filter_name_mac, args=(
	#                         r, filter_name, filter_mac,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_name_mac failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_name_mac case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_name and filter_uuid):
	#                     t = threading.Thread(target=self.filter_name_uuid, args=(
	#                         r, filter_name, filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_name_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_name_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_mac and filter_rssi):
	#                     t = threading.Thread(target=self.filter_mac_rssi, args=(
	#                         r, filter_mac, filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_mac_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_mac_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_mac and filter_uuid):
	#                     t = threading.Thread(target=self.filter_mac_uuid, args=(
	#                         r, filter_mac, filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_mac_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_mac_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_rssi and filter_uuid):
	#                     t = threading.Thread(target=self.filter_rssi_uuid, args=(
	#                         r, filter_rssi, filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_rssi_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('filter_rssi_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 else:
	#                     self.fail('参数不正确')
	#                     return
	#             elif len(para) == 5:
	#                 if (duration and filter_duplicates and filter_name):
	#                     t = threading.Thread(target=self.duration_filter_duplicates_name, args=(
	#                         r, duration, filter_duplicates,filter_name, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_duplicates_name failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_duplicates_name case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_mac):
	#                     t = threading.Thread(target=self.duration_filter_duplicates_mac, args=(
	#                         r, duration, filter_duplicates,filter_mac, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_duplicates_mac failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_duplicates_mac case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_rssi):
	#                     t = threading.Thread(target=self.duration_filter_duplicates_rssi, args=(
	#                         r, duration, filter_duplicates,filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_duplicates_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_duplicates_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_uuid):
	#                     t = threading.Thread(target=self.duration_filter_duplicates_uuid, args=(
	#                         r, duration, filter_duplicates,filter_uuid, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_duplicates_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_duplicates_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_name and filter_mac):
	#                     t = threading.Thread(target=self.duration_filter_name_mac, args=(
	#                         r, duration, filter_name,filter_mac, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_name_mac failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_name_mac case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_name and filter_rssi):
	#                     t = threading.Thread(target=self.duration_filter_name_rssi, args=(
	#                         r, duration, filter_name,filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_name_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_name_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_name and filter_uuid):
	#                     t = threading.Thread(target=self.duration_filter_name_uuid, args=(
	#                         r, duration, filter_name,filter_uuid, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_name_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_name_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_mac and filter_rssi):
	#                     t = threading.Thread(target=self.duration_filter_mac_rssi, args=(
	#                         r, duration, filter_mac,filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_mac_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_mac_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_mac and filter_uuid):
	#                     t = threading.Thread(target=self.duration_filter_mac_uuid, args=(
	#                         r, duration, filter_mac,filter_uuid, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_mac_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_mac_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_rssi and filter_uuid):
	#                     t = threading.Thread(target=self.duration_filter_uuid_rssi, args=(
	#                         r, duration, filter_uuid,filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_filter_rssi_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_filter_rssi_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_name and filter_mac):
	#                     t = threading.Thread(target=self.filter_duplicates_name_mac,
	#                                          args=(r, filter_duplicates, filter_name,filter_mac,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_duplicates_name_mac failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('case filter_duplicates_name_mac run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_name and filter_rssi):
	#                     t = threading.Thread(target=self.filter_duplicates_name_rssi,
	#                                          args=(r, filter_duplicates, filter_name,filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_duplicates_name_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('case filter_duplicates_name_rssi run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_name and filter_uuid):
	#                     t = threading.Thread(target=self.filter_duplicates_name_uuid,
	#                                          args=(r, filter_duplicates, filter_name,filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_duplicates_name_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('case filter_duplicates_name_uuid run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_name and filter_mac and filter_uuid):
	#                     t = threading.Thread(target=self.filter_name_mac_uuid,
	#                                          args=(r,filter_name,filter_mac,filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_name_mac_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('case filter_name_mac_uuid run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_name and filter_mac and filter_rssi):
	#                     t = threading.Thread(target=self.filter_name_mac_rssi,
	#                                          args=(r, filter_name,filter_mac,filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_name_mac_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('case filter_name_mac_rssi run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_mac and filter_rssi and filter_uuid):
	#                     t = threading.Thread(target=self.filter_mac_rssi_uuid,
	#                                          args=(r, filter_mac, filter_rssi,filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('filter_mac_rssi_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('case filter_mac_rssi_uuid run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#             elif len(para) == 6:
	#                 if (duration and filter_duplicates and filter_name and filter_mac):
	#                     t = threading.Thread(target=self.duration_duplicates_name_mac, args=(
	#                         r, duration, filter_duplicates, filter_name,filter_mac,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_name_mac failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_name_mac case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_name and filter_rssi):
	#                     t = threading.Thread(target=self.duration_duplicates_name_rssi, args=(
	#                         r, duration, filter_duplicates, filter_name,filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_name_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_name_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_name and filter_uuid):
	#                     t = threading.Thread(target=self.duration_duplicates_name_uuid, args=(
	#                         r, duration, filter_duplicates, filter_name,filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_name_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_name_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_mac and filter_uuid):
	#                     t = threading.Thread(target=self.duration_duplicates_mac_uuid, args=(
	#                         r, duration, filter_duplicates, filter_mac, filter_uuid, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_mac_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_mac_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_mac and filter_rssi):
	#                     t = threading.Thread(target=self.duration_duplicates_mac_rssi, args=(
	#                         r, duration, filter_duplicates,filter_mac, filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_mac_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_mac_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_uuid and filter_rssi):
	#                     t = threading.Thread(target=self.duration_duplicates_uuid_rssi, args=(
	#                         r, duration, filter_duplicates,filter_uuid,filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_uuid_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_uuid_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_name and filter_mac and filter_rssi):
	#                     t = threading.Thread(target=self.duration_name_mac_rssi, args=(
	#                         r, duration, filter_name, filter_mac,filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_name_mac_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_name_mac_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_name and filter_mac and filter_uuid):
	#                     t = threading.Thread(target=self.duration_name_mac_uuid, args=(
	#                         r, duration, filter_name, filter_mac,filter_uuid, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_name_mac_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_name_mac_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_name and filter_rssi and filter_uuid):
	#                     t = threading.Thread(target=self.duration_name_rssi_uuid, args=(
	#                         r, duration, filter_name, filter_rssi,filter_uuid, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_name_rssi_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_name_rssi_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_mac and filter_rssi and filter_uuid):
	#                     t = threading.Thread(target=self.duration_mac_rssi_uuid, args=(
	#                         r, duration,filter_mac,filter_rssi,filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_mac_rssi_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_mac_rssi_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_name and filter_uuid and filter_rssi):
	#                     t = threading.Thread(target=self.duplicates_name_uuid_rssi, args=(
	#                         r,filter_duplicates, filter_name, filter_uuid,filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duplicates_name_uuid_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duplicates_name_uuid_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_name and filter_uuid and filter_mac):
	#                     t = threading.Thread(target=self.duplicates_name_uuid_mac, args=(
	#                         r,filter_duplicates, filter_name, filter_uuid,filter_mac,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duplicates_name_uuid_mac failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duplicates_name_uuid_mac case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_name and filter_mac and filter_rssi):
	#                     t = threading.Thread(target=self.duplicates_name_mac_rssi, args=(
	#                         r,filter_duplicates, filter_name, filter_mac,filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duplicates_mac_uuid_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duplicates_mac_uuid_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_mac and filter_uuid and filter_rssi):
	#                     t = threading.Thread(target=self.duplicates_mac_uuid_rssi, args=(
	#                         r, filter_duplicates, filter_mac, filter_uuid, filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duplicates_mac_uuid_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duplicates_mac_uuid_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_name and filter_mac and filter_uuid and filter_rssi):
	#                     t = threading.Thread(target=self.name_mac_uuid_rssi, args=(
	#                         r, filter_name, filter_mac, filter_uuid, filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('name_mac_uuid_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('name_mac_uuid_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#             elif len(para) ==7:
	#                 if (duration and filter_duplicates and filter_name and filter_mac and filter_rssi):
	#                     t = threading.Thread(target=self.duration_duplicates_name_mac_rssi, args=(
	#                         r, duration, filter_duplicates, filter_name, filter_mac, filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_name_mac_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_name_mac_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_name and filter_mac and filter_uuid):
	#                     t = threading.Thread(target=self.duration_duplicates_name_mac_uuid, args=(
	#                         r, duration, filter_duplicates, filter_name, filter_mac, filter_uuid,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_name_mac_uuid failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_name_mac_uuid case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_name and filter_uuid and filter_rssi):
	#                     t = threading.Thread(target=self.duration_duplicates_name_uuid_rssi, args=(
	#                         r, duration, filter_duplicates, filter_name, filter_uuid, filter_rssi,active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_name_uuid_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_name_uuid_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_duplicates and filter_mac and filter_uuid and filter_rssi):
	#                     t = threading.Thread(target=self.duration_duplicates_mac_uuid_rssi, args=(
	#                         r, duration, filter_duplicates, filter_mac, filter_uuid, filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_duplicates_mac_uuid_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_duplicates_mac_uuid_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (filter_duplicates and filter_name and filter_mac and filter_uuid and filter_rssi):
	#                     t = threading.Thread(target=self.duplicates_name_mac_uuid_rssi, args=(
	#                         r, filter_duplicates, filter_name, filter_mac, filter_uuid, filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duplicates_name_mac_uuid_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duplicates_name_mac_uuid_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#                 elif (duration and filter_name and filter_mac and filter_uuid and filter_rssi):
	#                     t = threading.Thread(target=self.duration_name_mac_uuid_rssi, args=(
	#                         r, duration, filter_name, filter_mac, filter_uuid, filter_rssi, active))
	#                     t.setDaemon(True)
	#                     t.start()
	#                     t1 = threading.Thread(target=self.start_advertise, args=())
	#                     t1.setDaemon(True)
	#                     t1.start()
	#                     while True:
	#                         if self.case_run_flag == 'success':
	#                             return
	#                         elif self.case_run_flag == 'fail':
	#                             self.fail('duration_name_mac_uuid_rssi failed!')
	#                             return
	#                         elif self.case_run_flag == 'timeout':
	#                             self.fail('duration_name_mac_uuid_rssi case run time out.')
	#                             return
	#                         else:
	#                             time.sleep(0.5)
	#             elif len(para) ==8:
	#                 t = threading.Thread(target=self.duration_duplicates_name_mac_rssi_uuid, args=(
	#                     r, duration, filter_duplicates, filter_name, filter_mac, filter_rssi, filter_uuid,active))
	#                 t.setDaemon(True)
	#                 t.start()
	#                 t1 = threading.Thread(target=self.start_advertise, args=())
	#                 t1.setDaemon(True)
	#                 t1.start()
	#                 while True:
	#                     if self.case_run_flag == 'success':
	#                         return
	#                     elif self.case_run_flag == 'fail':
	#                         self.fail('duration_duplicates_name_mac_rssi_uuid failed!')
	#                         return
	#                     elif self.case_run_flag == 'timeout':
	#                         self.fail('duration_duplicates_name_mac_rssi_uuid case run time out.')
	#                         return
	#                     else:
	#                         time.sleep(0.5)
	#         else:
	#             self.assertEqual(r.text, expect_result)
	# def get_filter_duplicates(self,filter_duplicates,filters,active,j):
	#     if int(filter_duplicates) ==1:
	#         filter_duplicate=1
	#         count=self.conf['filter_count']
	#     else:
	#         filter_duplicate=0
	#         count = self.conf['unfilter_count']
	#     print("duplicate===",filter_duplicate)
	#     if int(filter_duplicate) == 1:
	#         # 去重的数据是：mac+adData
	#         print("len===",len(self.tmp_dup))
	#         if len(self.tmp_dup) < count:
	#             if filters in self.tmp_dup:
	#                 self.filter_run_flg ='fail'
	#                 print('\n', filters, '\n tmp_dup==', self.tmp_dup)
	#                 return  self.filter_run_flg
	#             else:
	#                 self.tmp_dup.append(filters)
	#                 print("self.dump==",self.tmp_dup)
	#         else:
	#             print("active===",int(active),'\n j==',j)
	#             if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
	#                 self.filter_run_flg = 'success'
	#                 return self.filter_run_flg
	#             else:
	#                 self.filter_run_flg = 'fail'
	#                 print("selff==",self.filter_run_flg)
	#                 return self.filter_run_flg
	#     elif int(filter_duplicate) == 0:
	#         if len(self.tmp_dup) < count:
	#             if filters in self.tmp:
	#                 if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
	#                     self.filter_run_flg = 'success'
	#                     return self.filter_run_flg
	#                 else:
	#                     self.tmp_dup.append(filters)
	#             else:
	#                 self.tmp_dup.append(filters)
	#         else:
	#             if filters in self.tmp_dup:
	#                 print("active11===", int(active), '\n j==', j)
	#                 if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
	#                     self.filter_run_flg='success'
	#                     return self.filter_run_flg
	#                 else:
	#                     self.filter_run_flg='fail'
	#                     return self.filter_run_flg
	#             else:
	#                 self.filter_run_flg='success'
	#                 return self.filter_run_flg
	#                 print("no repeat")
	def check_filters(self,filters,filter_parameter,active,j,rssi_flag=None):
		if len(self.tmp) < self.conf['filter_count']:
			if rssi_flag:
				if filters < filter_parameter:
					print('\n', filters, '≠', filter_parameter, '\n')
					self.case_run_flag = 'fail'
					return self.case_run_flag
				else:
					self.tmp.append(filters)
			else:
				if filters != filter_parameter:
					print('\n', filters, '≠', filter_parameter, '\n')
					self.case_run_flag = 'fail'
					return self.case_run_flag
				else:
					self.tmp.append(filters)
		else:
			if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
				self.case_run_flag ='success'
				return self.case_run_flag
			else:
				self.case_run_flag = 'fail'
				print("a=",active,'j==',j)
				return self.case_run_flag
	def check_filters_all(self,res,fildupli=None,filname=None,filmac=None,filuuid=None,filrssi=None,active=0):
		j=0
		for test_result in res.iter_lines():
			# case_run_flag=None
			test_result = str(test_result, encoding='utf8')
			if test_result.startswith('data'):
				test_result = json.loads(test_result[5:])
				if "adData" in test_result:
					filter = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
					uuid_res=test_result['adData']
				elif "scanData" in test_result:
					filter = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
					uuid_res=test_result['scanData']
					j = j + 1
				filters=''
				filter_parameter=''
				if filname:
					filters=filters+test_result['name']
					filter_parameter=filter_parameter+filname
				if filmac:
					filters = filters + test_result['bdaddrs'][0]['bdaddr']
					filter_parameter = filter_parameter + filmac
				if filuuid:
					filters = filters + self.get_uuid(uuid_res)
					sort_uuid = str(filuuid)[2:] + str(filuuid)[:2]
					filter_parameter = filter_parameter + sort_uuid
				if fildupli:
					if filrssi:
						if int(test_result['rssi']) < int(filrssi):
							print('\n', int(test_result['rssi']), '<', int(filrssi), '\n')
							case_run_flag = 'fail'
							return case_run_flag
						else:
							if filters != filter_parameter:
								print('\n', filters, '≠', filter_parameter, '\n')
								self.case_run_flag = 'fail'
								return case_run_flag
							else:
								if int(fildupli) == 1:
									filter_duplicate = 1
								else:
									filter_duplicate = 0
								print("fil==",filter_duplicate)
								case_run_flag = self.get_filter_duplicates(filter_duplicate, filter, active, j)
								if case_run_flag:
									return case_run_flag
					else:
						if filters != filter_parameter:
							print('\n', filters, '≠', filter_parameter, '\n')
							case_run_flag = 'fail'
							return case_run_flag
						else:
							if int(fildupli) == 1:
								filter_duplicate = 1
							else:
								filter_duplicate = 0
							case_run_flag = self.get_filter_duplicates(filter_duplicate, filter, active, j)
							if case_run_flag:
								return case_run_flag
				else:
					if filters:
						if filrssi:
							if int(filrssi) <=int(test_result['rssi']):
								case_run_flag = self.check_filters(filters, filter_parameter, active, j)
								if case_run_flag:
									return
							else:
								case_run_flag='fail'
								print(int(filrssi),'>',test_result['rssi'])
								return case_run_flag
						else:
							case_run_flag = self.check_filters(filters, filter_parameter, active, j)
							if case_run_flag:
								return
					else:
						if filrssi:
							rssi_flag=True
							case_run_flag = self.check_filters(test_result['rssi'],filrssi, active, j,
															   rssi_flag=rssi_flag)
							if case_run_flag:
								return case_run_flag
						else:
							if self.tmp > int(self.conf['unfilter_count']):
								if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
									case_run_flag = 'success'
									print("chip_active success")
									return case_run_flag
								else:
									case_run_flag = 'fail'
									return case_run_flag
							else:
								if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
									case_run_flag = 'success'
									print("chip_active success")
									return case_run_flag
								else:
									self.tmp.append('1')
	def chip_active(self,res,active):
		self.case_run_flag=self.check_filters_all(res,active=active)
		if self.case_run_flag:
			return
		# count=0
		# j=0
		# for test_result in res.iter_lines():
		#     test_result = test_result.decode()
		#     if test_result.startswith('data'):
		#         test_result = json.loads(test_result[5:])
		#         if "scanData" in test_result:
		#             j = j + 1
		#         if count > int(self.conf['unfilter_count']):
		#             if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
		#                 self.case_run_flag = 'success'
		#                 print("chip_active success")
		#                 return self.case_run_flag
		#             else:
		#                 self.case_run_flag = 'fail'
		#                 return self.case_run_flag
		#         else:
		#             if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
		#                 self.case_run_flag = 'success'
		#                 print("chip_active success")
		#                 return self.case_run_flag
		#             else:
		#                 count = count + 1
	def duration_test(self, res, duration,active):
		j=0
		count=0
		if self.conf['local'] == 'True':
			duration1=self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = test_result.decode()
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							count=count+1
							# print("count===",count)
							if "scanData" in test_result:
								j = j + 1
				except AttributeError:
					pass
				except:
					self.case_run_flag='fail'
					print("e")
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				print("t===",t)
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag='fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag =self.check_filters_all(res,active=active)
				if self.case_run_flag:
					return
		else:
			self.case_run_flag = self.check_filters_all(res, active=active)
			if self.case_run_flag:
				return
	def filter_duplicates(self, res, filter_duplicates, active):
		self.case_run_flag=self.check_filters_all(res,fildupli=filter_duplicates,active=active)
		if self.case_run_flag:
			return
	def filter_uuid(self, res, filter_uuid,active):
		self.case_run_flag=self.check_filters_all(res,filuuid=filter_uuid,active=active)
		if self.case_run_flag:
			return
	def filter_name(self, res, filter_name,active):
		self.case_run_flag=self.check_filters_all(res,filname=filter_name,active=active)
		if self.case_run_flag:
			return
	def filter_rssi(self, res, filter_rssi,active):
		self.case_run_flag=self.check_filters_all(res,filrssi=filter_rssi,active=active)
		if self.case_run_flag:
			return
		# j=0
		# for test_result in res.iter_lines():
		#     test_result = test_result.decode()
		#     if test_result.startswith('data'):
		#         test_result = json.loads(test_result[5:])
		#         filters = int(test_result['rssi'])
		#         if "scanData" in test_result:
		#             j=j+1
		#         if len(self.tmp) < self.conf['filter_count']:
		#             if filters < int(filter_rssi):
		#                 print('\n', filters, '≠', filter_rssi, '\n')
		#                 self.case_run_flag = 'fail'
		#                 return
		#             else:
		#                 self.tmp.append(filters)
		#         else:
		#             if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
		#                 self.case_run_flag = 'success'
		#                 return
		#             else:
		#                 self.case_run_flag = 'fail'
		#                 return
	def filter_mac(self, res, filter_mac,active):
		self.case_run_flag=self.check_filters_all(res,filmac=filter_mac,active=active)
		if self.case_run_flag:
			return
	def duration_filter_duplicates(self,res,duration,filter_duplicates,active):
		j=0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								j = j + 1
							self.case_run_flag=self.get_filter_duplicates(filter_duplicates,filters,active,j)
							if self.case_run_flag:
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag='fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag=self.check_filters_all(res,fildupli=filter_duplicates,active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, active=active)
			if self.case_run_flag:
				return
	def duration_filter_name(self,res,duration,filter_name,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "scanData" in test_result:
								j = j + 1
							filters=test_result['name']
							self.case_run_flag = self.check_filters(filters,filter_name,active,j)
							if self.case_run_flag:
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag ='fail'
					print("scan error")
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					print("t--",t)
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filname=filter_name, active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res,filname=filter_name,active=active)
			if self.case_run_flag:
				return
	def duration_filter_mac(self,res,duration,filter_mac,active):
		j = 0
		print("locsl===",self.conf['local'] )
		if self.conf['local'] == 'True':
			print("duration_type==",type(duration),"shuzhi==",duration)
			duration1 = self.get_duration(duration)
			print('duration1==',duration1)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "scanData" in test_result:
								j = j + 1
							filters=test_result['bdaddrs'][0]['bdaddr']
							self.case_run_flag = self.check_filters(filters,filter_mac,active,j)
							if self.case_run_flag:
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag ='fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag=self.check_filters_all(res,filmac=filter_mac,active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, active=active)
			if self.case_run_flag:
				return
	def duration_filter_uuid(self,res,duration,filter_uuid,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								uuid = self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								uuid = self.get_uuid(test_result['scanData'])
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							if uuid:
								self.case_run_flag = self.check_filters(uuid, sort_uuid, active, j)
								print("sell==",self.case_run_flag)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag='fail'
								print("sel2==", self.case_run_flag)
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag ='fail'
					print("sel3==", self.case_run_flag)
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filuuid=filter_uuid, active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filuuid=filter_uuid, active=active)
			if self.case_run_flag:
				return
	def duration_filter_rssi(self,res,duration,filter_rssi,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "scanData" in test_result:
								j = j + 1
							filters = int(test_result['rssi'])
							if len(self.tmp) < self.conf['filter_count']:
								if filters < int(filter_rssi):
									print('\n', filters, '≠', filter_rssi, '\n')
									self.case_run_flag = 'fail'
									return
								else:
									self.tmp.append(filters)
							else:
								if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
									self.case_run_flag = 'success'
									return
								else:
									self.case_run_flag = 'fail'
									return
				except AttributeError:
					pass
				except:
					self.case_run_flag ='fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filrssi=filter_rssi, active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filrssi=filter_rssi, active=active)
			if self.case_run_flag:
				return
	def filter_duplicates_name(self,res,filter_duplicates,filter_name,active):
		self.case_run_flag=self.check_filters_all(res,fildupli=filter_duplicates,filname=filter_name,active=active)
		if self.case_run_flag:
			return
	def filter_duplicates_mac(self,res,filter_duplicates,filter_mac,active):
		self.case_run_flag = self.check_filters_all(res,fildupli=filter_duplicates,filmac=filter_mac,active=active)
		if self.case_run_flag:
			return
	def filter_duplicates_uuid(self,res,filter_duplicates,filter_uuid,active):
		self.case_run_flag=self.check_filters_all(res,fildupli=filter_duplicates,filuuid=filter_uuid,active=active)
		if self.case_run_flag:
			return
		# j = 0
		# for test_result in res.iter_lines():
		#     test_result = str(test_result, encoding='utf8')
		#     if test_result.startswith('data'):
		#         test_result = json.loads(test_result[5:])
		#         if "adData" in test_result:
		#             filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
		#             uuid = self.get_uuid(test_result['adData'])
		#         elif "scanData" in test_result:
		#             filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
		#             uuid = self.get_uuid(test_result['scanData'])
		#             j = j + 1
		#         sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
		#         if sort_uuid == uuid:
		#             self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
		#             if self.case_run_flag:
		#                 return
		#         else:
		#             print('\n', sort_uuid, '≠', uuid, '\n')
		#             self.case_run_flag='fail'
		#             return
	def filter_duplicates_rssi(self,res,filter_duplicates,filter_rssi,active):
		self.case_run_flag=self.check_filters_all(res,fildupli=filter_duplicates,filrssi=filter_rssi,active=active)
		if self.case_run_flag:
			return
		# j = 0
		# for test_result in res.iter_lines():
		#     test_result = str(test_result, encoding='utf8')
		#     if test_result.startswith('data'):
		#         test_result = json.loads(test_result[5:])
		#         if "adData" in test_result:
		#             filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
		#             rssi = test_result['rssi']
		#         elif "scanData" in test_result:
		#             filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
		#             rssi = test_result['rssi']
		#             j = j + 1
		#         if int(rssi) >=int(filter_rssi):
		#             self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
		#             if self.case_run_flag:
		#                 return
		#         else:
		#             print('\n', rssi, '<', filter_rssi, '\n')
		#             self.case_run_flag='fail'
		#             return
	def filter_name_rssi(self, res, filter_name,filter_rssi,active):
		self.case_run_flag=self.check_filters_all(res,filname=filter_name,filrssi=filter_rssi,active=active)
		if self.case_run_flag:
			return
	def filter_name_uuid(self, res, filter_name,filter_uuid,active):
		self.case_run_flag=self.check_filters_all(res,filname=filter_name,filuuid=filter_uuid,active=active)
		if self.case_run_flag:
			return
	def filter_name_mac(self, res, filter_name,filter_mac,active):
		self.case_run_flag=self.check_filters_all(res,filname=filter_name,filmac=filter_mac,active=active)
		if self.case_run_flag:
			return
	def filter_mac_rssi(self, res, filter_mac,filter_rssi,active):
		self.case_run_flag=self.check_filters_all(res,filmac=filter_mac,filrssi=filter_rssi,active=active)
		if self.case_run_flag:
			return
	def filter_mac_uuid(self, res, filter_mac,filter_uuid,active):
		self.case_run_flag=self.check_filters_all(res,filmac=filter_mac,filuuid=filter_uuid,active=active)
		if self.case_run_flag:
			return
	def filter_rssi_uuid(self, res, filter_rssi,filter_uuid,active):
		self.case_run_flag=self.check_filters_all(res,filrssi=filter_rssi,filuuid=filter_uuid,active=active)
		if self.case_run_flag:
			return
	def duration_filter_duplicates_name(self,res,duration,filter_duplicates,filter_name,active):
		j=0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								j = j + 1
							filters_name=test_result['name']
							if filter_name == filters_name:
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag='fail'
								print(filter_name, '≠',filters_name)
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag='fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag=self.check_filters_all(res,fildupli=filter_duplicates,filname=filter_name,active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,
														active=active)
			if self.case_run_flag:
				return
	def duration_filter_duplicates_mac(self, res, duration, filter_duplicates, filter_mac, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								j = j + 1
							filters_mac = test_result['bdaddrs'][0]['bdaddr']
							if filter_mac == filters_mac:
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filter_mac, '≠',filters_mac)
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filmac=filter_mac,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filmac=filter_mac,
														active=active)
			if self.case_run_flag:
				return
	def duration_filter_duplicates_rssi(self, res, duration, filter_duplicates, filter_rssi, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								j = j + 1
							filters_rssi = test_result['rssi']
							if int(filters_rssi) >= int(filter_rssi):
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(int(filters_rssi),'<',int(filter_rssi))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filrssi=filter_rssi,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filrssi=filter_rssi,
														active=active)
			if self.case_run_flag:
				return
	def duration_filter_duplicates_uuid(self, res, duration, filter_duplicates, filter_uuid, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
								uuid=self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								uuid = self.get_uuid(test_result['scanData'])
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							if uuid == sort_uuid:
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(uuid, '≠',sort_uuid)
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,
														active=active)
			if self.case_run_flag:
				return
	def duration_filter_name_uuid(self, res, duration, filter_name, filter_uuid, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								uuid = self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								uuid = self.get_uuid(test_result['scanData'])
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							filters=test_result['name'] +uuid
							filter_parameter=filter_name+sort_uuid
							self.case_run_flag = self.check_filters(filters, filter_parameter, active, j)
							if self.case_run_flag:
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filname=filter_name, filuuid=filter_uuid,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filname=filter_name, filuuid=filter_uuid,active=active)
			if self.case_run_flag:
				return
	def duration_filter_name_mac(self, res, duration, filter_name, filter_mac, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['name']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['name']
								j = j + 1
							filter_parameter=filter_mac+filter_name
							self.case_run_flag = self.check_filters(filters, filter_parameter, active, j)
							if self.case_run_flag:
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filname=filter_name, filmac=filter_mac,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filname=filter_name, filmac=filter_mac,active=active)
			if self.case_run_flag:
				return
	def duration_filter_name_rssi(self, res, duration, filter_name, filter_rssi, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "scanData" in test_result:
								j = j + 1
							filters=test_result['name']
							filter_parameter=filter_name
							if int(test_result['rssi'] >= int(filter_rssi)):
								self.case_run_flag = self.check_filters(filters, filter_parameter, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag='fail'
								print(int(test_result['rssi'],'<',int(filter_rssi)))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filname=filter_name, filrssi=filter_rssi,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filname=filter_name, filrssi=filter_rssi,active=active)
			if self.case_run_flag:
				return
	def duration_filter_mac_rssi(self, res, duration, filter_mac, filter_rssi, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "scanData" in test_result:
								j = j + 1
							filters=test_result['bdaddrs'][0]['bdaddr']
							filter_parameter = filter_mac
							if int(test_result['rssi'] >= int(filter_rssi)):
								self.case_run_flag = self.check_filters(filters, filter_parameter, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(int(test_result['rssi'], '<', int(filter_rssi)))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filrssi=filter_rssi,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filrssi=filter_rssi, active=active)
			if self.case_run_flag:
				return
	def duration_filter_mac_uuid(self, res, duration, filter_mac, filter_uuid, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								uuid = self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								uuid = self.get_uuid(test_result['scanData'])
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							filters = test_result['bdaddrs'][0]['bdaddr'] + uuid
							filter_parameter = filter_mac + sort_uuid
							self.case_run_flag = self.check_filters(filters, filter_parameter, active, j)
							if self.case_run_flag:
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filuuid=filter_uuid,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filuuid=filter_uuid, active=active)
			if self.case_run_flag:
				return
	def duration_filter_uuid_rssi(self, res, duration,filter_uuid,filter_rssi,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								uuid = self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								uuid = self.get_uuid(test_result['scanData'])
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							filters = uuid
							filter_parameter =sort_uuid
							if int(filter_rssi) < int(test_result['rssi']):
								self.case_run_flag = self.check_filters(filters, filter_parameter, active, j)
								if self.case_run_flag:
									return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filuuid=filter_uuid, filrssi=filter_rssi,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filrssi=filter_rssi, filuuid=filter_uuid, active=active)
			if self.case_run_flag:
				return
	def filter_duplicates_name_mac(self,res,filter_duplicates,filter_name,filter_mac,active):
		self.case_run_flag=self.check_filters_all(res,fildupli=filter_duplicates,filname=filter_name,filmac=filter_mac,active=active)
		if self.case_run_flag:
			return
	def filter_duplicates_name_rssi(self, res, filter_duplicates, filter_name, filter_rssi, active):
		self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,
													filrssi=filter_rssi, active=active)
		if self.case_run_flag:
			return
	def filter_duplicates_name_uuid(self, res, filter_duplicates, filter_name, filter_uuid, active):
		self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,
													filuuid=filter_uuid,active=active)
		if self.case_run_flag:
			return
	def filter_name_mac_rssi(self, res, filter_name, filter_mac, filter_rssi,active):
		self.case_run_flag = self.check_filters_all(res,filname=filter_name,filmac=filter_mac,
													filrssi=filter_rssi,active=active)
		if self.case_run_flag:
			return
	def filter_name_mac_uuid(self,res,filter_name,filter_mac,filter_uuid,active):
		self.case_run_flag=self.check_filters_all(res,filname=filter_name,filmac=filter_mac,filuuid=filter_uuid,active=active)
		if self.case_run_flag:
			return
	def filter_mac_rssi_uuid(self,res,filter_mac,filter_rssi,filter_uuid,active):
		self.case_run_flag=self.check_filters_all(res,filrssi=filter_rssi,filmac=filter_mac,filuuid=filter_uuid,active=active)
		if self.case_run_flag:
			return
	def duration_duplicates_name_mac(self, res, duration, filter_duplicates, filter_name,filter_mac,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								j = j + 1
							filter_all=test_result['name']+test_result['bdaddrs'][0]['bdaddr']
							filter_parameter=filter_name+filter_mac
							if filter_all == filter_parameter:
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filter_all, '≠', filter_parameter)
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,filmac=filter_mac,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,filmac=filter_mac,
														active=active)
			if self.case_run_flag:
				return
	def duration_duplicates_name_uuid(self, res, duration, filter_duplicates, filter_name,filter_uuid,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
								uuid=test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								uuid=test_result["scanData"]
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							filter_all=test_result['name']+self.get_uuid(uuid)
							filter_parameter=filter_name+sort_uuid
							if filter_all == filter_parameter:
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filter_all, '≠', filter_parameter)
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,filuuid=filter_uuid,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,filuuid=filter_uuid,
														active=active)
			if self.case_run_flag:
				return
	def duration_duplicates_name_rssi(self, res, duration, filter_duplicates, filter_name,filter_rssi,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								j = j + 1
							if (test_result['name'] == filter_name ) and (int(filter_rssi) <= int(test_result['rssi'] )):
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(test_result['name'], '≠',filter_name,'or ',int(filter_rssi),'> ',int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,filrssi=filter_rssi,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,filrssi=filter_rssi,
														active=active)
			if self.case_run_flag:
				return
	def duration_duplicates_mac_uuid(self, res, duration, filter_duplicates, filter_mac, filter_uuid, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
								uuid = test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								uuid = test_result["scanData"]
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							filter_all = test_result['bdaddrs'][0]['bdaddr']  + self.get_uuid(uuid)
							filter_parameter = filter_mac + sort_uuid
							if filter_all == filter_parameter:
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filter_all, '≠', filter_parameter)
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,
															filmac=filter_mac,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,
														filmac=filter_mac,
														active=active)
			if self.case_run_flag:
				return
	def duration_duplicates_mac_rssi(self, res, duration, filter_duplicates, filter_mac, filter_rssi, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								j = j + 1
							if (test_result['bdaddrs'][0]['bdaddr'] == filter_mac) and (int(filter_rssi) <= int(test_result['rssi'])):
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(test_result['bdaddrs'][0]['bdaddr'], '≠', filter_mac, 'or ', int(filter_rssi), '> ',
									  int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filmac=filter_mac,
															filrssi=filter_rssi,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filmac=filter_mac,
														filrssi=filter_rssi,
														active=active)
			if self.case_run_flag:
				return
	def duration_duplicates_uuid_rssi(self, res, duration, filter_duplicates,filter_uuid,filter_rssi,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
								uuid = test_result['adData']
							elif "scanData" in test_result:
								filters = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								uuid = test_result["scanData"]
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							filter_all = self.get_uuid(uuid)
							filter_parameter = sort_uuid
							if (filter_all == filter_parameter) and (int(test_result['rssi']) >=int(filter_rssi)):
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filters, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filter_all, '≠', filter_parameter,' or ',int(test_result['rssi']),' < ',int(filter_rssi))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,filrssi=filter_rssi,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,filrssi=filter_rssi,
														active=active)
			if self.case_run_flag:
				return
	def duration_name_mac_uuid(self, res, duration, filter_name,filter_mac,filter_uuid, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								uuid = test_result['adData']
							elif "scanData" in test_result:
								uuid = test_result["scanData"]
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							filter_all = test_result['name'] +test_result['bdaddrs'][0]['bdaddr'] + self.get_uuid(uuid)
							filter_parameter = filter_name +filter_mac + sort_uuid
							self.case_run_flag=self.check_filters(filter_all,filter_parameter,active,j)
							if self.case_run_flag:
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filname=filter_name,filmac=filter_mac,
															filuuid=filter_uuid,active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filname=filter_name,filmac=filter_mac,
														filuuid=filter_uuid,active=active)
			if self.case_run_flag:
				return
	def duration_name_mac_rssi(self, res, duration,filter_name, filter_mac, filter_rssi, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "scanData" in test_result:
								j = j + 1
							filter_all=test_result['name'] +test_result['bdaddrs'][0]['bdaddr']
							filter_parameter=filter_name+filter_mac
							if int(filter_rssi) <= int(test_result['rssi']):
								self.case_run_flag = self.check_filters(filter_all,filter_parameter,active,j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print( int(filter_rssi), '> ',int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filname=filter_name, filmac=filter_mac,
															filrssi=filter_rssi,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filname=filter_name, filmac=filter_mac,
														filrssi=filter_rssi,
														active=active)
			if self.case_run_flag:
				return
	def duration_name_rssi_uuid(self, res, duration, filter_name, filter_rssi, filter_uuid, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								uuid = test_result['adData']
							elif "scanData" in test_result:
								uuid = test_result["scanData"]
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							filter_all = test_result['name'] + self.get_uuid(uuid)
							filter_parameter = filter_name  + sort_uuid
							if int(filter_rssi) <= int(test_result['rssi']):
								self.case_run_flag = self.check_filters(filter_all, filter_parameter, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(int(filter_rssi), '> ', int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filname=filter_name, filrssi=filter_rssi,
															filuuid=filter_uuid, active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filname=filter_name, filrssi=filter_rssi,
														filuuid=filter_uuid, active=active)
			if self.case_run_flag:
				return
	def duration_mac_rssi_uuid(self, res, duration, filter_mac, filter_rssi, filter_uuid, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								uuid = test_result['adData']
							elif "scanData" in test_result:
								uuid = test_result["scanData"]
								j = j + 1
							sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
							filter_all = test_result['bdaddrs'][0]['bdaddr'] + self.get_uuid(uuid)
							filter_parameter =filter_mac + sort_uuid
							if int(filter_rssi) <= int(test_result['rssi']):
								self.case_run_flag = self.check_filters(filter_all, filter_parameter, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(int(filter_rssi), ' > ', int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filrssi=filter_rssi,
															filuuid=filter_uuid, active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filrssi=filter_rssi,
														filuuid=filter_uuid, active=active)
			if self.case_run_flag:
				return
	def duplicates_name_uuid_rssi(self, res, filter_duplicates, filter_name, filter_uuid,filter_rssi, active):
		self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,
													filuuid=filter_uuid,filrssi=filter_rssi, active=active)
		if self.case_run_flag:
			return
	def duplicates_name_uuid_mac(self, res, filter_duplicates, filter_name, filter_uuid,filter_mac, active):
		self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,
													filuuid=filter_uuid,filmac=filter_mac, active=active)
		if self.case_run_flag:
			return
	def duplicates_mac_uuid_rssi(self,res, filter_duplicates, filter_mac, filter_uuid,filter_rssi, active):
		self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filrssi=filter_rssi,
													filuuid=filter_uuid, filmac=filter_mac, active=active)
		if self.case_run_flag:
			return
	def duplicates_name_mac_rssi(self,res, filter_duplicates, filter_name, filter_mac,filter_rssi, active):
		self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filrssi=filter_rssi,
													filname=filter_name, filmac=filter_mac, active=active)
		if self.case_run_flag:
			return
	def name_mac_uuid_rssi(self,res,filter_name, filter_mac,filter_uuid,filter_rssi,active):
		self.case_run_flag = self.check_filters_all(res, filuuid=filter_uuid, filrssi=filter_rssi,
													filname=filter_name, filmac=filter_mac, active=active)
		if self.case_run_flag:
			return
	def duration_duplicates_name_mac_rssi(self, res, duration, filter_duplicates, filter_name,filter_mac, filter_rssi, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
							elif "scanData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								j = j + 1
							filters=test_result['name'] +test_result['bdaddrs'][0]['bdaddr']
							filter_parmeters=filter_name+filter_mac
							if (filters == filter_parmeters) and (int(filter_rssi) <= int(test_result['rssi'])):
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filter, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filters, '≠', filter_parmeters, 'or ', int(filter_rssi), '> ',
									  int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,
															filrssi=filter_rssi,filmac=filter_mac,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,
														filrssi=filter_rssi,filmac=filter_mac,
														active=active)
			if self.case_run_flag:
				return
	def duration_duplicates_name_mac_uuid(self, res, duration, filter_duplicates, filter_name,filter_mac, filter_uuid, active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
								uuid=self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								uuid=self.get_uuid(test_result['scanData'])
								j = j + 1
							filters=test_result['name'] +test_result['bdaddrs'][0]['bdaddr']+uuid
							filter_parmeters=filter_name+filter_mac +(str(filter_uuid[2:])+str(filter_uuid[:2]))
							if (filters == filter_parmeters):
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filter, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filters, '≠', filter_parmeters)
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,
															filuuid=filter_uuid,filmac=filter_mac,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,
														filuuid=filter_uuid,filmac=filter_mac,
														active=active)
			if self.case_run_flag:
				return
	def duration_duplicates_mac_uuid_rssi(self, res, duration, filter_duplicates,filter_mac,filter_uuid,filter_rssi,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
								uuid=self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								uuid=self.get_uuid(test_result['scanData'])
								j = j + 1
							filters = test_result['bdaddrs'][0]['bdaddr'] +uuid
							filter_parmeters = filter_mac + (str(filter_uuid[2:])+str(filter_uuid[:2]))
							if (filters == filter_parmeters) and (int(filter_rssi) <= int(test_result['rssi'])):
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filter, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filters, '≠', filter_parmeters, 'or ', int(filter_rssi), '> ',
									  int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,
															filrssi=filter_rssi, filmac=filter_mac,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,
														filrssi=filter_rssi, filmac=filter_mac,
														active=active)
			if self.case_run_flag:
				return
	def duration_duplicates_name_uuid_rssi(self, res, duration, filter_duplicates,filter_name,filter_uuid,filter_rssi,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
								uuid=self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								uuid=self.get_uuid(test_result['scanData'])
								j = j + 1
							filters = test_result['name'] +uuid
							filter_parmeters = filter_name + (str(filter_uuid[2:])+str(filter_uuid[:2]))
							if (filters == filter_parmeters) and (int(filter_rssi) <= int(test_result['rssi'])):
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filter, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filters, '≠', filter_parmeters, 'or ', int(filter_rssi), '> ',
									  int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,
															filrssi=filter_rssi, filname=filter_name,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filuuid=filter_uuid,
														filrssi=filter_rssi, filname=filter_name,
														active=active)
			if self.case_run_flag:
				return
	def duration_name_mac_uuid_rssi(self, res, duration,filter_name,filter_mac,filter_uuid,filter_rssi,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								uuid=self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								uuid=self.get_uuid(test_result['scanData'])
								j = j + 1
							filters = test_result['name'] +test_result['bdaddrs'][0]['bdaddr'] +uuid
							filter_parmeters = filter_name + filter_mac+(str(filter_uuid[2:])+str(filter_uuid[:2]))
							if  (int(filter_rssi) <= int(test_result['rssi'])):
								self.case_run_flag = self.check_filters(filters,filter_parmeters,active,j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print( int(filter_rssi), '> ',
									  int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filuuid=filter_uuid,
															filrssi=filter_rssi, filname=filter_name,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filuuid=filter_uuid,
														filrssi=filter_rssi, filname=filter_name,
														active=active)
			if self.case_run_flag:
				return
	def duplicates_name_mac_uuid_rssi(self, res, filter_duplicates, filter_name, filter_mac,filter_uuid,filter_rssi, active):
		self.case_run_flag = self.check_filters_all(res, fildupli=filter_duplicates, filname=filter_name,filmac=filter_mac,
													filuuid=filter_uuid, filrssi=filter_rssi,active=active)
		if self.case_run_flag:
			return
	def duration_duplicates_name_mac_rssi_uuid(self, res, duration,filter_duplicates,filter_name, filter_mac,filter_rssi,filter_uuid,active):
		j = 0
		if self.conf['local'] == 'True':
			duration1 = self.get_duration(duration)
			if duration1:
				d1 = datetime.datetime.now()
				try:
					for test_result in res.iter_lines():
						test_result = str(test_result, encoding='utf8')
						if test_result.startswith('data'):
							test_result = json.loads(test_result[5:])
							if "adData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result['adData']
								uuid = self.get_uuid(test_result['adData'])
							elif "scanData" in test_result:
								filter = test_result['bdaddrs'][0]['bdaddr'] + test_result["scanData"]
								uuid = self.get_uuid(test_result['scanData'])
								j = j + 1
							filters = test_result['name'] + test_result['bdaddrs'][0]['bdaddr'] + uuid
							filter_parmeters = filter_name + filter_mac + (str(filter_uuid[2:]) + str(filter_uuid[:2]))
							if (filters == filter_parmeters) and (int(filter_rssi) <= int(test_result['rssi'])):
								self.case_run_flag = self.get_filter_duplicates(filter_duplicates, filter, active, j)
								if self.case_run_flag:
									return
							else:
								self.case_run_flag = 'fail'
								print(filters, '≠', filter_parmeters, 'or ', int(filter_rssi), '> ',
									  int(test_result['rssi']))
								return
				except AttributeError:
					pass
				except:
					self.case_run_flag = 'fail'
					return
				d2 = datetime.datetime.now()
				t = float(((d2 - d1).seconds)) + \
					float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				if t <= duration1:
					if (int(active) == 1 and j > 0) or (int(active) == 0 and j == 0):
						self.case_run_flag = 'success'
						return
					else:
						self.case_run_flag = 'fail'
						return
				else:
					self.case_run_flag = 'fail'
					return
			else:
				self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filuuid=filter_uuid,
															filrssi=filter_rssi, filname=filter_name,fildupli=filter_duplicates,
															active=active)
				if self.case_run_flag:
					return
		else:
			print("AC端不支持duration参数")
			self.case_run_flag = self.check_filters_all(res, filmac=filter_mac, filuuid=filter_uuid,
														filrssi=filter_rssi, filname=filter_name,fildupli=filter_duplicates,
														active=active)
			if self.case_run_flag:
				return
	# @ddt.data(*dd['connectdata'])
	# def test_connect(self, values):
	#     if self.sdk.model.upper().startswith('S'):
	#         expect_result = values['expect_result_s1000']
	#     else:
	#         expect_result = values['expect_result_other']
	#     device = values['device']
	#     chip = values['chip']
	#     try:
	#         chip = int(chip)
	#     except Exception as e:
	#         print(e)
	#         pass
	#     types = values['types']
	#     timeout = values['timeout']
	#     t = threading.Thread(target=self.connect_device, args=(device,chip,types,timeout,expect_result))
	#     t.setDaemon(True)
	#     t.start()
	#     while True:
	#         if self.case_run_flag == 'success':
	#             return
	#         elif self.case_run_flag == 'fail':
	#             self.fail('connect_device failed!')
	#             return
	#         elif self.case_run_flag == 'timeout':
	#             self.fail('connect_device case run time out.')
	#             return
	#         else:
	#             time.sleep(0.5)
	# def connect_device(self,device,chip,types,timeout,expect_result):
	#     # scan_flag = self.scan_to_connect(chip, device)
	#     self.sdk.disconnect_device(device)
	#     if timeout:
	#         time_out = float(timeout) / float(1000)
	#     else:
	#         time_out = 5.0
	#     # if scan_flag:
	#     for i in range(0, 5):
	#         code, body, duration = self.sdk.connect_device(device, types=types, chip=chip, timeout=timeout)
	#         if code == 200:
	#             self.connect_flag = True
	#             if duration <=time_out:
	#                 test_result = str(code) + ',' + body
	#                 self.assertEqual(test_result, expect_result)
	#                 break
	#             else:
	#                 self.case_run_flag='fail'
	#                 print('连接成功后，timeout参数没有生效')
	#                 return
	#         elif code == 500 and (body == 'device not found'):
	#             print("tim==",time_out)
	#             if duration >= time_out:
	#                 test_result = str(code) + ',' + body
	#                 self.assertEqual(test_result, expect_result)
	#                 self.case_run_flag = 'success'
	#                 return
	#             else:
	#                 self.case_run_flag = 'fail'
	#                 return
	#         else:
	#             test_result = str(code) + ',' + body
	#             self.assertEqual(test_result, expect_result)
	#             self.case_run_flag = 'success'
	#             return
	#     if chip is None:
	#         chip = 0
	#     else:
	#         chip = chip
	#     if self.connect_flag:
	#         for i1 in range(1, 4):
	#             code1, body1 = self.sdk.get_devices_list(state='connected')
	#             if code1 == 200:
	#                 txt = json.loads(body1)
	#                 print("txt==", txt)
	#                 for i in range(0, len(txt['nodes'])):
	#                     if txt['nodes'][i]['bdaddrs']['bdaddr'] == device:
	#                         if txt['nodes'][i]['chipId'] == chip:
	#                             print(
	#                                 'ap={0} device={1} connected success'.format(self.conf['hub'], device))
	#                             self.sdk.disconnect_device(device)
	#                             self.case_run_flag = 'success'
	#                             return
	#                         else:
	#                             err = 'ap={0} device={1} connect error'.format(self.conf['hub'], device)
	#                             print(err)
	#                             self.case_run_flag = 'fail'
	#                             return
	# def scan_to_connect(self, chip, dev):
	#     with closing(self.sdk.scan(chip=chip)) as self.sse:
	#         i = 0
	#         scan_flag = False
	#         for da in self.sse.iter_lines():
	#             data = da.decode()
	#             if data.startswith("data"):
	#                 msg = json.loads(data[5:])
	#                 i = i + 1
	#                 if msg['bdaddrs'][0]['bdaddr'] == dev:
	#                     scan_flag = True
	#                     return scan_flag
	#                 elif i >= 200:
	#                     return scan_flag
	# #
	# @ddt.data(*dd['disconnectdata'])
	# def test_disconnect(self, values):
	#     expect_result = values['expect_result']
	#     device = values['device']
	#     timeout = values['timeout']
	#     print("ttt==",timeout)
	#     code, body= self.sdk.disconnect_device(device, timeout=timeout)
	#     if code ==200:
	#         code1, body1 = self.sdk.get_devices_list(state='connected')
	#         if code1 == 200:
	#             txt = json.loads(body1)
	#             print("txt==", txt)
	#             for i in range(0, len(txt['nodes'])):
	#                 if txt['nodes'][i]['bdaddrs']['bdaddr'] == device:
	#                     self.fail("disconnect device{0} failed".format(device))
	#     test_result = str(code) + ',' + body
	#     self.assertEqual(test_result, expect_result)
	# #
	# @ddt.data(*dd['getdevlist'])
	# def test_get_dev_list(self, values):
	#     expect_result = values['expect_result']
	#     connect_state = values['connection_state']
	#     code, body = self.sdk.get_devices_list(connect_state)
	#     if code ==200:
	#         txt = json.loads(body)
	#         if 'nodes' not in txt:
	#             self.fail("get connected list fail")
	#     test_result = int(code)
	#     self.assertEqual(test_result, int(expect_result))
	#
	# @ddt.data(*dd['discover_service'])
	# def test_discover_service(self, values):
	#     device = values['device']
	#     dev_type = values['type']
	#     service_uuid = values['service_uuid']
	#     expect_result = values['expect_result']
	#     devlist=self.get_devlist()
	#     if device in devlist:
	#         pass
	#     else:
	#         for i in range(5):
	#             code,body,_ =self.sdk.connect_device(device, dev_type)
	#             if code ==200:
	#                 devlist1=self.get_devlist()
	#                 if device in devlist1:
	#                     break
	#                 else:
	#                     self.fail("before get service,connect device error")
	#                     break
	#     code, body = self.sdk.discovery_services(device, service_uuid)
	#     test_result = str(code) + ',' + body
	#     self.assertEqual(test_result, expect_result)
	#
	# @ddt.data(*dd['discover_characs'])
	# def test_discover_characs(self, values):
	#     device = values['device']
	#     dev_type = values['type']
	#     server_uuid = str(values['service_uuid'])
	#     expect_result = values['expect_result']
	#     devlist = self.get_devlist()
	#     if device in devlist:
	#         pass
	#     else:
	#         for i in range(5):
	#             code, body, _ = self.sdk.connect_device(device, dev_type)
	#             if code == 200:
	#                 devlist1 = self.get_devlist()
	#                 if device in devlist1:
	#                     break
	#                 else:
	#                     self.fail("before get service,connect device error")
	#                     break
	#     code, body = self.sdk.discovery_characteristics(device, server_uuid)
	#     test_result = str(code) + ',' + body
	#     self.assertEqual(test_result, expect_result)
	#
	# @ddt.data(*dd["discover_charac"])
	# def test_discover_charac(self, values):
	#     device = values['device']
	#     dev_type = values['type']
	#     charac_uuid = values['charac_uuid']
	#     expect_result = values['expect_result']
	#     devlist = self.get_devlist()
	#     if device in devlist:
	#         pass
	#     else:
	#         for i in range(5):
	#             code, body, _ = self.sdk.connect_device(device, dev_type)
	#             if code == 200:
	#                 devlist1 = self.get_devlist()
	#                 if device in devlist1:
	#                     break
	#                 else:
	#                     self.fail("before get service,connect device error")
	#                     break
	#     code, body = self.sdk.discovery_characteristic(device, charac_uuid)
	#     test_result = str(code) + ',' + body
	#     self.assertEqual(test_result, expect_result)
	#
	# @ddt.data(*dd['discover_des'])
	# def test_discover_des(self, values):
	#     device = values['device']
	#     dev_type = values['type']
	#     charac_uuid = values['charac_uuid']
	#     expect_result = values['expect_result']
	#     devlist = self.get_devlist()
	#     if device in devlist:
	#         pass
	#     else:
	#         for i in range(5):
	#             code, body, _ = self.sdk.connect_device(device, dev_type)
	#             if code == 200:
	#                 devlist1 = self.get_devlist()
	#                 if device in devlist1:
	#                     break
	#                 else:
	#                     self.fail("before get service,connect device error")
	#                     break
	#     code, body = self.sdk.discover_descriptors(device, charac_uuid)
	#     test_result = str(code) + ',' + body
	#     self.assertEqual(test_result, expect_result)
	#
	# @ddt.data(*dd['discover_all'])
	# def test_discover_all(self, values):
	#     device = values['device']
	#     dev_type = values['type']
	#     expect_result = values['expect_result']
	#     devlist = self.get_devlist()
	#     if device in devlist:
	#         pass
	#     else:
	#         for i in range(5):
	#             code, body, _ = self.sdk.connect_device(device, dev_type)
	#             if code == 200:
	#                 devlist1 = self.get_devlist()
	#                 if device in devlist1:
	#                     break
	#                 else:
	#                     self.fail("before get service,connect device error")
	#                     break
	#     code, body = self.sdk.discover_all(device)
	#     if code == 200:
	#         self.assertEqual(len(body), len(expect_result))
	#     else:
	#         test_result = str(code) + ',' + body
	#         self.assertEqual(test_result, expect_result)
	#
	# @ddt.data(*dd['read_by_handle'])
	# def test_read_by_handle(self, values):
	#     device = values['device']
	#     dev_type = values['type']
	#     handle = values['handle']
	#     expect_result = values['expect_result']
	#     devlist = self.get_devlist()
	#     if device in devlist:
	#         pass
	#     else:
	#         for i in range(5):
	#             code, body, _ = self.sdk.connect_device(device, dev_type)
	#             if code == 200:
	#                 devlist1 = self.get_devlist()
	#                 if device in devlist1:
	#                     break
	#                 else:
	#                     self.fail("before get service,connect device error")
	#                     break
	#     code, body = self.sdk.read_by_handle(device, handle)
	#     test_result = str(code) + ',' + body
	#     self.assertEqual(test_result, expect_result)
	#
	@ddt.data(*dd['write_by_handle'])
	def test_write_by_handle(self, values):
		device = values['device']
		dev_type = values['type']
		handle = values['handle']
		handle_data = values['handle_data']
		expect_result = values['expect_result']
		devlist = self.get_devlist()
		if device in devlist:
			pass
		else:
			for i in range(5):
				code, body, _ = self.sdk.connect_device(device, dev_type)
				if code == 200:
					devlist1 = self.get_devlist()
					if device in devlist1:
						break
					else:
						self.fail("before get service,connect device error")
						break
		code, body = self.sdk.write_by_handle(device, handle, handle_data)
		## if code ==200:
		## 	code1,msg=self.sdk.read_by_handle(device,handle)
		## 	if code1 ==200:
		## 		if json.loads(msg)["value"] == handle_data:
		## 			pass
		## 		else:
		## 			self.fail("wirte handle failed,写入的值:{0}，读出的值:{1}".format(handle_data,json.loads(msg)["value"]))
		## 			return
		test_result = str(code) + ',' + body
		self.assertEqual(test_result, expect_result)
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
		# 				else:
		# 					self.assertTrue(False)
		# 					self.sdk.disconnect_device(device)
		# 					self.message = None
		# 					break
		# else:
		# 	self.sdk.connect_device(device, types, 0, 10000)
		# 	time.sleep(5)
		# 	self.message = None
		# 	code, body = self.sdk.disconnect_device(device)
		# 	print(code, body)
		# 	while 1:
		# 		if self.time_out_flag:
		# 			self.fail('case time out')
		# 			break
		# 		else:
		# 			if self.message:
		# 				if self.message['handle'] == device:
		# 					self.assertTrue(True)
		# 					self.sdk.disconnect_device(device)
		# 					self.message = None
		# 					break
		# 				else:
		# 					self.assertTrue(False)
		# 					self.sdk.disconnect_device(device)
		# 					self.message = None
		# 					break
	@ddt.data(*dd['recv_notification'])
	def test_recive_notification(self, values):
		device = values['device']
		# expect_result = values['expect_result']
		dev_type = values['device_type']
		devlist = self.get_devlist()
		if device in devlist:
			pass
		else:
			for i in range(5):
				code, body, _ = self.sdk.connect_device(device, dev_type)
				if code == 200:
					devlist1 = self.get_devlist()
					if device in devlist1:
						break
					else:
						self.fail("before get service,connect device error")
						break
		res = self.sdk.recive_notification()
		if res.status_code == 200:
			for line in res.iter_lines():
				message = str(line, encoding='utf-8')
				if message.strip() == ':keep-alive':
					self.connect_flag=True
					break
				else:
					err = 'AP={0} recive_indication_and_notification  code={1},msg={2}'.format(self.conf['hub'],res.status_code,message)
					self.fail(err)
					break
		else:
			err = 'AP={0} recive_indication_and_notification  code={1},msg={2}'.format(self.conf['hub'],
																					   res.status_code, message)
			self.fail(err)
		# 埃微反向通知：你好
		if values['dev_type'] == 'Iw':
			code, text = self.sdk.write_by_handle(device, 39, '21ff310802ffE4BDA0E5A5BD')
			if code == 200:
				debug = 'AP={0}  device={1} 反向通知你好 success code={2},msg={3}'.format(self.conf['hub'], device, code, text)
				print(debug)
			else:
				debug = 'AP={0}  device={1} 反向通知你好 failed code={2},msg={3}'.format(self.conf['hub'], device,
																				   code, text)
				self.fail(debug)
		# 酷思手环反向通知：你好
		elif values['dev_type'] == 'Hw':
			dict_handle = [{'handle': 17, 'handle_value': '0100'},
						   {'handle': 19, 'handle_value': 'ff2006000227'},
						   {'handle': 19, 'handle_value': 'ff000d00040110010102FF0125'},
						   {'handle': 19, 'handle_value': 'FF80140006021002010a01030101E4BDA0E5A589'},
						   {'handle': 19, 'handle_value': 'FFc105BD82'}]
			for i in range(len(dict_handle)):
				handle = dict_handle[i]['handle']
				handle_value = dict_handle[i]['handle_value']
				code, text = self.sdk.write_by_handle(device, handle, handle_value)
				if code == 200:
					debug = 'AP={0}  device={1} 反向通知你好 success,write handle={4},value={5}, code={2},msg={3}'.format(
						self.conf['hub'], device,
						code, text, handle,
						handle_value)
					print(debug)
				else:
					self.fail("反向通知 写入handle error")

		else:
			pass
		# start Thread to receive notification
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
	def get_duration(self,duration):
		if duration or duration ==0:
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
		return duration1
	def start_advertise(self):
		j = 0
		api1 = api(self.common_conf['local_host'], local=True)
		while j < 4:
			for i in range(10, 50):
				i = str(i)
				ad_data = '0201060303F0FF0201' + i + '11094170695F66756E6374696F6E54657374'
				resp_data = '0201060303F0FF030102' + i + '11094170695F66756E6374696F6E54657374'
				code, msg = api1.start_scan_advertise(0, 20, ad_data, resp_data)
				if code == 200 or code == 502:
					time.sleep(1)
					code1,msg1=api1.stop_advertise(0)
					if code1 ==200:
						pass
					else:
						self.case_run_flag = 'fail'
						print("stop advertise failed code={0},msg={1}".format(code1, msg1))
						return
				else:
					self.case_run_flag = 'fail'
					print("start advertise failed code={0},msg={1}".format(code, msg))
					return
			j = j + 1
	def get_devlist(self):
		devlist=[]
		code, body = self.sdk.get_devices_list(state='connected')
		if code == 200:
			txt = json.loads(body)
			for i in range(0, len(txt['nodes'])):
				dev=txt['nodes'][i]['bdaddrs']['bdaddr']
				devlist.append(dev)
		return devlist
	def time_out(self):
		self.case_run_flag = 'timeout'

	def tearDown(self):
		self.timeout_timer.cancel()
if __name__ == '__main__':
	unittest.main(verbosity=2)
