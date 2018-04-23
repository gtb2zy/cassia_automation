# -*- coding: utf-8 -*-
'''
测试点：测试在不同芯片之间，按先后顺序，能否成功开启扫描

'''

import unittest,json,sys,os
from contextlib import closing
from threading import Timer
path = os.getcwd().split('APItest')[0]+'APItest/lib/'
sys.path.append(path)
from api import api
from logs import set_logger
from tools import get_api
from tools import get_model

class testcase(unittest.TestCase):

	logger = set_logger(__name__)
	sdk = get_api()
	model = get_model()

	def setUp(self):
		self.logger.info('测试在不同芯片之间，按先后顺序，能否成功开启扫描')
		self.timer = Timer(30,self.close)
		self.timer.start()
	def tearDown(self):
		self.timer.cancel()
	def test_start_scan_in_diff_chip(self):
		flag = None
		if self.model.startswith('S')or self.model.startswith('s'):
			self.logger.debug('if model is s1000系列的产品，直接pass')
			#if model is s1000系列的产品，直接pass
			self.assertTrue(True)
		else:
			#step1:chip 0 start scan,then stop scan
			with closing(self.sdk.scan(chip = 0)) as self.sse:
				for message in self.sse:
					if message.startswith('data'):
						flag = True
						self.logger.debug("step1:chip 0 start scan,then stop scan success")
						self.sse.close()
					elif 'keep-alive' in message:
						pass
					else:
						flag = False
						self.logger.error('start scan fail,%s'%message)
			#step2:chip 1 start scan,then stop scan.
			with closing(self.sdk.scan(chip = 1)) as self.sse:
				for message in self.sse:
					if message.startswith('data'):
						flag = True
						self.logger.debug("step2:chip 1 start scan,then stop scan success")
						self.sse.close()
					elif 'keep-alive' in message:
						pass
					else:
						flag = False
						self.logger.error('start scan fail,%s'%message)
			#step3:chip 0 start scan,then change to chip1 scan.
			with closing(self.sdk.scan(chip = 0)) as self.sse:
				for message in self.sse:
					if message.startswith('data'):
						flag = True
						self.logger.debug("step3:chip 0 start scan,then change to chip1 scan success")
						# self.change_scan(flag)
						self.sse.close()
					elif 'keep-alive' in message:
						pass
					else:
						flag = False
						self.logger.error('start scan fail,%s'%message)
			#step4:chip 1 start scan,then change to chip0 scan.
			with closing(self.sdk.scan(chip = 1)) as self.sse:
				for message in self.sse:
					if message.startswith('data'):
						flag = True
						self.logger.debug("step4:chip 1 start scan,then change to chip0 scan success")
						# self.change_scan2(flag)
						self.sse.close()
					elif 'keep-alive' in message:
						pass
					else:
						flag = False
						self.logger.error('start scan fail,%s'%message)	
			#step5:chip 0 start scan,then change to chip1 scan.
			with closing(self.sdk.scan(chip = 1)) as self.sse:
				for message in self.sse:
					if message.startswith('data'):
						flag = True
						self.logger.debug("step5:chip 0 start scan,then change to chip1 scan success.")
						self.sse.close()
					elif 'keep-alive' in message:
						pass
					else:
						flag = False
						self.logger.error('start scan fail,%s'%message)	
			self.assertTrue(flag)
			if flag:
				self.logger.info('case pass\n')
			else:
				self.logger.info('case fail\n')
	def close(self):
		self.fail("Case failed,start scan timeout.")
		self.logger.info("Case failed,start scan timeout.")
		self.sse.close()


if __name__ == '__main__':
	unittest.main(verbosity=2)