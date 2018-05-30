#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @time:2018-5-14
# @Author haidan li
'''
测试点： s系列：
            芯片0主动扫描，增加duration 7.8s参数功能实现
		x/e系列：
		    芯片0主动扫描，不加duration 参数功能实现；芯片1被动扫描，增加duration 15.58s参数功能，互相不影响，持续时间过后sse断掉
'''
import unittest, json, sys, os, json,time
from contextlib import closing
from threading import Timer
import threading

path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
import tools,datetime
from logs import set_logger

class testcase(unittest.TestCase):
	logger = set_logger(__name__)
	sdk = tools.get_api()
	model = tools.get_model()
	filter_count = int(tools.read_job_config()['filter_count'])
	unfilter_count = int(tools.read_job_config()['unfilter_count'])
	timeout = tools.read_job_config()['case_timeout']
	local=tools.read_job_config()["local"]

	def setUp(self):
		self.timeout_flag = None
		self.flag1 = 0
		self.flag2 = 0
		self.key=None
		self.logger.info('X/E duration 参数测试chip0 主动扫  chip1 被动扫d=5.58s ，S chip0 主动扫d=7.8s ')
		self.timer = Timer(self.timeout, self.set_timeout)
		self.timer.start()

	def tearDown(self):
		self.timer.cancel()
	# 测试方法
    # noinspection PyUnreachableCode


# noinspection PyUnreachableCode,PyUnreachableCode
def test_scan_filter_duplicates(self):
		# duration1=2
		if self.local =="True":
			if self.model.startswith('S') or self.model.startswith('s'):
				a = threading.Thread(target=self.chip0_scan, args=(0,7.8 ))
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
				a = threading.Thread(target=self.chip0_scan, args=(0, ))
				b = threading.Thread(target=self.chip1_scan, args=(1, 5.58))
				a.setDaemon(True)
				b.setDaemon(True)
				b.start()
				a.start()
				while True:
					if self.flag1 == 1 and self.flag2 == 1:
						self.logger.info('pass\n')
						break
					elif self.timeout_flag:
						self.logger.info('fail\n')
						self.fail('Case failed,case timeout.')
						self.logger.error("Case failed,start scan timeout.")
						break
						sys.exit(1)
		else:
			self.logger.info("AC不需要测试duration参数，duration参数只对AP端生效")
			pass
	def chip0_scan(self, active=0, duration=None):
		# step1:chip 1 start passive scan,then start chip0 scan.
		if not duration is None:
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
				duration1=duration
		else:
			duration1=None
		with closing(self.sdk.scan(chip=0, active=active, duration=duration1)) as self.sse1:
			if duration1:
				# time.sleep(duration1+0.5)
				d1=datetime.datetime.now()
				print("start time at",datetime.datetime.now())
				for message in self.sse1:
					continue
				d2=datetime.datetime.now()
				print("end time at ",datetime.datetime.now())
				t=float(((d2-d1).seconds)) + float((d2-d1).microseconds/1000/1000) -0.5
				print("second",t)
				if t <=duration1:
					self.flag1 +=1
					self.logger.info("Step 1:chip0 start scan with  duration success.")
				else:
					self.fail("chip 0 duration failed")
					self.logger.debug("chip 0 duration failed")
			else:
				count=0
				for message in self.sse1:
					if message.startswith("data"):
						msg=json.loads(message[5:])
						count +=1
						print("chip 0 ",count,message)
						if count > self.unfilter_count:
							self.flag1 += 1
							self.logger.info("Step 1:chip0 start scan with no duration success.")
							break


# noinspection PyUnreachableCode
def chip1_scan(self, active=0, duration=None):
		# step2:start chip1 scan.
		# 字符串 扫描5s后停止
		if not duration is None:
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
				duration1=duration
		else:
			duration1=None
		with closing(self.sdk.scan(chip=1, active=active, duration=duration1)) as self.sse1:
			if duration1:
				# time.sleep(duration1+0.5)
				d1 = datetime.datetime.now()
				print("start time at", datetime.datetime.now())
				for message in self.sse1:
					continue
				d2 = datetime.datetime.now()
				print("end time at ", datetime.datetime.now())
				t = float(((d2 - d1).seconds)) + float((d2 - d1).microseconds / 1000 / 1000) - 0.5
				print("second", t)
				if t <= duration1:
					self.flag2 += 1
					self.logger.info("Step 1:chip1 start scan with  duration success.")
				else:
					self.fail("chip 0 duration failed")
					self.logger.debug("chip 1 duration failed")
			else:
				count = 0
				for message in self.sse1:
					if message.startswith("data"):
						msg = json.loads(message[5:])
						count += 1
						print("chip 0 ", count, message)
						if count > self.unfilter_count:
							self.flag2 += 1
							self.logger.info("Step 1:chip1 start scan with no duration success.")
							break
	def set_timeout(self):
		self.timeout_flag = True
if __name__ == '__main__':
	unittest.main()
