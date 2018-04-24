# -*- coding: utf-8 -*-
'''
测试点：测试chip0 local扫描的同时进行cloud扫描

'''
import unittest, json, sys, os, json
from contextlib import closing
from threading import Timer
import threading
path = os.getcwd().split('APItest')[0] + 'APItest/lib/'
sys.path.append(path)
import tools
from logs import set_logger


class testcase(unittest.TestCase):
    logger = set_logger(__name__)
    local_sdk,cloud_sdk = tools.get_all_api()
    model = tools.get_model()
    filters = tools.get_filter()
    timeout = tools.read_job_config()['case_timeout']

    def setUp(self):
        self.timeout_flag = None
        self.flag1 = None
        self.flag2 = None
        self.logger.info('测试chip0 local扫描的同时进行cloud扫描')
        self.timer = Timer(self.timeout, self.set_timeout)
        self.timer.start()

    def tearDown(self):
        self.timer.cancel()

    def test_scan_on_cloud_local(self):
        a = threading.Thread(target=self.local_scan)
        b = threading.Thread(target=self.cloud_scan)
        a.setDaemon(True)
        b.setDaemon(True)
        b.start()
        a.start()

        while True:
            if self.flag1 and self.flag2:
                self.assertTrue(True)
                self.logger.info('pass\n')
                break
            elif self.timeout_flag:
                self.logger.info('fail\n')
                self.fail('Case failed,start scan timeout.')
                self.logger.error("Case failed,start scan timeout.")
                break
    def local_scan(self):
        #step1:start chip0 local scan.
        with closing(self.local_sdk.scan()) as self.sse2:
            count = 0
            for message in self.sse2:
                if message.startswith('data'):
                    if count<300:
                        count += 1
                    else:
                        self.flag2 = True
                        self.logger.debug('Step 1:chip0 start local scan success.')
                        break

    def cloud_scan(self):
        #step2:start chip0 cloud scan.
        with closing(self.local_sdk.scan()) as self.sse1:
            count = 0
            for message in self.sse1:
                if message.startswith('data'):
                    if count<300:
                        count += 1
                    else:
                        self.flag2 = True
                        self.logger.debug('Step 1:chip0 start cloud scan success.')
                        break
    def set_timeout(self):
        self.timeout_flag = True
if __name__ == '__main__':
    unittest.main()