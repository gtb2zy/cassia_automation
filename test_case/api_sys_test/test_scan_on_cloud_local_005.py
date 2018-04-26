# -*- coding: utf-8 -*-
'''
测试点：先开始local扫描的,然后停止，最后进行cloud扫描

'''
import unittest, time, sys, os
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
        self.logger.info('测试点：测试chip0 local扫描的同时,chip1进行cloud扫描')
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

    def test_step(self):
        self.flag = None
        #step1:start local scan.
        with closing(self.local_sdk.scan(chip = 1)) as self.sse2:
            count = 0
            for message in self.sse2:
                if message.startswith('data'):
                    if count<100:
                        print('local',count, message)
                        count += 1
                    else:
                        self.flag = True
                        self.logger.debug('Step 1: start local scan success.')
                        break
        #step3:停止本地扫描
        time.sleep(3)
        self.logger.debug('Step 2: stop local scan success.')
        #step2:start cloud scan.
        with closing(self.cloud_sdk.scan(chip = 0)) as self.sse1:
            count = 0
            for message in self.sse1:
                if message.startswith('data'):
                    if count<100:
                        print('cloud',count,message)
                        count += 1
                    else:
                        self.flag = True
                        self.logger.debug('Step 3:start cloud scan success.')
                        break

    def set_timeout(self):
        self.timeout_flag = True

if __name__ == '__main__':
    unittest.main()