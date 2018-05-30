#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @time:2018-5-9
# @Author haidan li
'''
测试点： s系列：
            芯片0被动扫描，不加filter duplicate过滤功能实现
		x/e系列：
		    芯片0主动扫描加filter duplicate过滤，芯片1被动扫描不加filter duplicate 过滤功能，互相不影响，能正常过滤
'''
import unittest, json, sys, os, json,time
from contextlib import closing
from threading import Timer
import threading

path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
import tools
from logs import set_logger

class testcase(unittest.TestCase):
	logger = set_logger(__name__)
	sdk = tools.get_api()
	model = tools.get_model()
	filter_count = int(tools.read_job_config()['filter_count'])
	unfilter_count = int(tools.read_job_config()['unfilter_count'])
	timeout = tools.read_job_config()['case_timeout']
	def setUp(self):
		self.timeout_flag = None
		self.flag1 = 0
		self.flag2 = 0
		self.key=None
		self.logger.info('X/E 测试chip0  filter duplicate主动扫描 chip1 不加filter duplicate被动扫描，S chip0 不加filter duplicate 被动扫描')
		self.timer = Timer(self.timeout, self.set_timeout)
		self.timer.start()

	def tearDown(self):
		self.timer.cancel()
	# 测试方法
    # noinspection PyUnreachableCode


# noinspection PyUnreachableCode
def test_scan_filter_duplicates(self):
		if self.model.startswith('S') or self.model.startswith('s'):
			a = threading.Thread(target=self.chip0_scan, args=(1, ))
			a.setDaemon(True)
			a.start()
			while True:
				if self.flag1 == 1:
					self.logger.info('pass\n')
					break
				elif self.timeout_flag:
					self.logger.info('fail\n')
					self.fail('Case failed,start scan timeout.')
					self.logger.error("Case failed,start scan timeout.")
					break
		else:
			a = threading.Thread(target=self.chip0_scan, args=(0, 1))
			b = threading.Thread(target=self.chip1_scan, args=(1, ))
			a.setDaemon(True)
			b.setDaemon(True)
			b.start()
			a.start()
			while True:
				if self.flag1==1 and self.flag2==1:
					self.logger.info('pass\n')
					break
				elif self.timeout_flag:
					self.logger.info('fail\n')
					self.fail('Case failed,case timeout.')
					self.logger.error("Case failed,start scan timeout.")
					# break
					sys.exit(1)
	def chip0_scan(self, active=0, filter_duplicates=0):
		# step1:chip 1 start passive scan,then start chip0 scan.
		with closing(self.sdk.scan(chip=0, active=active, filter_duplicates=filter_duplicates)) as self.sse1:
			count = 0
			tmp=[]
			for message in self.sse1:
				if message.startswith('data'):
					msg = json.loads(message[5:])
				if filter_duplicates:
					if active ==1:
						if "adData" in msg:
							filters=msg['bdaddrs'][0]['bdaddr']+msg['adData']
						elif "scanData" in msg:
							filters=msg['bdaddrs'][0]['bdaddr']+msg["scanData"]
					else:
						filters=msg['bdaddrs'][0]['bdaddr']+msg['adData']
					# 进入开启过滤的扫描结果判断流程
					if len(tmp) < self.filter_count:
						if filters in tmp:
							tmp.clear()
							time.sleep(1)
							self.fail("filter duplicate failed")
							self.logger.debug("filter duplicate failed")
							break
						else:
							tmp.append(filters)
							print('chip0 ', len(tmp), message)
					else:
						self.flag1 += 1
						self.logger.info('Step 1:chip0 start scan with filter duplicates success.')
						break
				else:
					# 进入不开启过滤的扫描结果判断流程
					if count < self.unfilter_count:
						print('chip0', count, message)
						count += 1
					else:
						self.flag1 += 1
						self.logger.debug('Step 1:chip0 start scan with no filter duplicates success.')
						break


# noinspection PyUnreachableCode
def chip1_scan(self, active=0, filter_duplicates=None):
		# step2:start chip0 scan.
		with closing(self.sdk.scan(chip=1, active=active, filter_duplicates=filter_duplicates)) as self.sse2:
			count = 0
			tmp=[]
			for message in self.sse2:
				if message.startswith('data'):
					msg = json.loads(message[5:])
					if filter_duplicates:
						if active == 1:
							if "adData" in msg:
								filters = msg['bdaddrs'][0]['bdaddr'] + msg['adData']
							elif "scanData" in msg:
								filters = msg['bdaddrs'][0]['bdaddr'] + msg["scanData"]
						else:
							filters = msg['bdaddrs'][0]['bdaddr'] + msg['adData']
						# 进入开启过滤的扫描结果判断流程
						if len(tmp) < self.filter_count:
							if filters in tmp:
								tmp.clear()
								time.sleep(1)
								self.fail("filter duplicate failed")
								self.logger.debug("filter duplicate failed")
								break
							else:
								tmp.append(filters)
								print('chip1 ', len(tmp), message)
						else:
							self.flag2 += 1
							self.logger.info('Step 1:chip1 start scan with filter duplicates success.')
							break
					else:
						# 进入不开启过滤的扫描结果判断流程
						if count < self.unfilter_count:
							print('chip1', count, message)
							count += 1
						else:
							self.flag2 += 1
							self.logger.debug('Step 1:chip1 start scan with no filter duplicate success.')
							break
	def set_timeout(self):
		self.timeout_flag = True


if __name__ == '__main__':
	unittest.main()
