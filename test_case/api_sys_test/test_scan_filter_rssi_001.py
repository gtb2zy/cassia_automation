# -*- coding: utf-8 -*-
# @time:2018-4-25
# @Author haidan li
'''
测试点： s系列：
            芯片0主动扫描，filter rssi信号强度过滤功能实现
		x/e系列：
		    芯片0主动扫描加filter rssi过滤，芯片1主动扫描加filter rssi 过滤功能，互相不影响，能正常过滤
'''
import unittest,sys, os, json
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
	filters = tools.get_filter()
	filter_count = int(tools.read_job_config()['filter_count'])
	unfilter_count = int(tools.read_job_config()['unfilter_count'])
	timeout = tools.read_job_config()['case_timeout']
	def setUp(self):
		self.timeout_flag = None
		self.flag1 = 0
		self.flag2 = 0
		self.logger.info('测试X/E chip0 chip1 filter rssi主动扫描，S chip0 filter rssi 主动扫描')
		self.timer = Timer(self.timeout, self.set_timeout)
		self.timer.start()

	def tearDown(self):
		self.timer.cancel()
	# 测试方法
    # noinspection PyUnreachableCode
    def test_scan_filter_rssi(self):
		if self.model.startswith('S') or self.model.startswith('s'):
			a = threading.Thread(target=self.chip0_scan, args=(0, self.filters['filter_rssi']))
			a.setDaemon(True)
			a.start()
			while True:
				if self.flag1 == 1 :
					self.assertTrue(True)
					self.logger.info('pass\n')
					break
				elif self.timeout_flag:
					self.logger.info('fail\n')
					self.fail('Case failed,start scan timeout.')
					self.logger.error("Case failed,start scan timeout.")
					break
		else:
			a = threading.Thread(target=self.chip0_scan, args=(0, self.filters['filter_rssi']))
			b = threading.Thread(target=self.chip1_scan, args=(0, self.filters['filter_rssi']))
			a.setDaemon(True)
			b.setDaemon(True)
			b.start()
			a.start()
			while True:
				if self.flag1==1 and self.flag2==1:
					self.assertTrue(True)
					self.logger.info('pass\n')
					break
				elif self.timeout_flag:
					self.logger.info('fail\n')
					self.fail('Case failed,case timeout.')
					self.logger.error("Case failed,start scan timeout.")
					# break
					sys.exit(1)

    # noinspection PyUnreachableCode
    def chip0_scan(self, active=0, filter_rssi=None):
		# step1:chip 1 start passive scan,then start chip0 scan.
		with closing(self.sdk.scan(chip=0, active=active, filter_rssi=filter_rssi)) as self.sse1:
			count = 0
			for message in self.sse1:
				if message.startswith('data'):
					msg = json.loads(message[5:])
				if filter_rssi:
					# 进入开启过滤的扫描结果判断流程
					if count < self.filter_count:
						print('chip0', count, message)
						rssi = int(msg['rssi'])
						rssi_threshold=int(self.filters['filter_rssi'])
						if rssi >= rssi_threshold:
							count += 1
						else:
							self.fail("filter rssi failed")
							self.logger.debug("filter rssi failed")
							break
					else:
						self.flag1 += 1
						self.logger.debug('Step 1:chip0 start scan with filter rssi success.')
						break
				else:
					# 进入不开启过滤的扫描结果判断流程
					if count < self.unfilter_count:
						print('chip0', count, message)
						count += 1
					else:
						self.flag1 += 1
						self.logger.debug('Step 1:chip0 start scan with no filter rssi success.')
						break


# noinspection PyUnreachableCode
def chip1_scan(self, active=0, filter_rssi=None):
		# step2:start chip0 scan.
		with closing(self.sdk.scan(chip=1, active=active, filter_rssi=filter_rssi)) as self.sse2:
			count = 0
			for message in self.sse2:
				if message.startswith('data'):
					msg = json.loads(message[5:])
					if filter_rssi:
						# 进入开启过滤的扫描结果判断流程
						if count < self.filter_count:
							print('chip1', count, message)
							rssi = int(msg['rssi'])
							rssi_threshold = int(self.filters['filter_rssi'])
							if rssi >= rssi_threshold:
								count += 1
							else:
								self.fail("filter rssi failed")
								self.logger.debug("filter rssi failed")
								break
						else:
							self.flag2 += 1
							self.logger.debug('Step 1:chip1 start scan with filter rssi success.')
							break
					else:
						# 进入不开启过滤的扫描结果判断流程
						if count < self.unfilter_count:
							print('chip1', count, message)
							count += 1
						else:
							self.flag2 += 1
							self.logger.debug('Step 1:chip1 start scan with no filter rssi success.')
							break
	def set_timeout(self):
		self.timeout_flag = True


if __name__ == '__main__':
	unittest.main()
