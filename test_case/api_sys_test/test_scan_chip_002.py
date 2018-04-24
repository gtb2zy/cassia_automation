# -*- coding: utf-8 -*-
'''
测试点：测试两块芯片同时开启扫描能否成功

'''


import unittest, json, sys, os
from contextlib import closing
from threading import Timer
import threading
path = os.getcwd().split('APItest')[0] + 'APItest/lib/'
sys.path.append(path)
from logs import set_logger
from tools import get_api
from tools import get_model


class testcase(unittest.TestCase):
    logger = set_logger(__name__)
    sdk = get_api()
    model = get_model()

    def setUp(self):
        self.timeout = None
        self.flag1 = None
        self.flag2 = None
        self.logger.info('测试两块芯片同时开启扫描能否成功')
        self.timer = Timer(30, self.close)
        self.timer.start()

    def tearDown(self):
        self.timer.cancel()

    def test_chips_start_scan_meanwhile(self):
        if self.model.startswith('S') or self.model.startswith('s'):
            self.assertTrue(True)
        else:
            threading.Thread(target=self.chip0_scan).start()
            threading.Thread(target=self.chip1_scan).start()
            while True:
                if self.flag1 and self.flag2:
                    self.assertTrue(True)
                    self.logger.info('pass')
                    break
                elif self.timeout:
                    self.fail('Case failed,start scan timeout.')
                    self.logger.info('fail')
                    self.logger.error("Step 1:Case failed,start scan timeout.")
                    break

    def chip0_scan(self):
        #step1:chip 1 start scan,then start chip0 scan.
        with closing(self.sdk.scan(chip=0)) as self.sse1:
            count = 0
            for message in self.sse1:
                if count < 300:
                    if message.startswith('data'):
                        # print('chip0',message)
                        count += 1
                    elif 'keep-alive' in message:
                        pass
                    else:
                        self.logger.error('start scan fail,%s' % message)
                else:
                    self.flag1 = True
                    break
                    self.logger.debug(
                        "step1:chip 1 start scan,then start chip0 scan success."
                    )

    def chip1_scan(self):
        #step2:start chip0 scan.
        with closing(self.sdk.scan(chip=1)) as self.sse2:
            count = 0
            for message in self.sse2:
                if count < 300:
                    if message.startswith('data'):
                        # print('chip1',message)
                        count += 1
                    elif 'keep-alive' in message:
                        pass
                    else:
                        self.logger.error('start scan fail,%s' % message)
                else:
                    self.flag2 = True
                    self.logger.debug("step2:start chip0 scan success.")
                    break
                    

    def close(self):
        self.timeout = True


if __name__ == '__main__':
    unittest.main()
