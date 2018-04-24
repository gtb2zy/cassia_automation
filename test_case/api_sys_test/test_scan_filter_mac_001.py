# -*- coding: utf-8 -*-
'''
测试点：测试chip0不加过虑主动扫描，chip1 filter mac 主动扫描

'''
import unittest, json, sys, os, json
from contextlib import closing
from threading import Timer
import threading

path = os.getcwd().split('APItest')[0] + 'APItest/lib/'
sys.path.append(path)
import tools


class testcase(unittest.TestCase):
    logger = tools.set_logger(__name__)
    sdk = tools.get_cloud_api()
    model = tools.get_model()
    filters = tools.get_filter()
    timeout = tools.read_job_config()['case_timeout']

    def setUp(self):
        self.timeout_flag = None
        self.flag1 = None
        self.flag2 = None
        self.logger.info('测试chip0不加过虑主动扫描，chip1 filter mac 主动扫描')
        self.timer = Timer(5, self.set_timeout)
        self.timer.start()

    def tearDown(self):
        self.timer.cancel()

    # 测试方法
    def test_scan_filter_mac(self):
        if self.model.startswith('S') or self.model.startswith('s'):
            a= threading.Thread(target=self.chip0_scan, args=(1,))
            a.setDaemon(True)
            a.start()
            b = threading.Thread(target=self.chip0_scan, args=(1, self.filters['filter_mac']))
            b.setDaemon(True)
            b.start()
            while True:
                if self.flag1 and self.flag2:
                    self.assertTrue(True)
                    self.logger.info('pass\n')
                    break
                elif self.timeout_flag:
                    self.logger.info('fail\n')
                    self.fail('Case failed,case test timeout.')
                    self.logger.error("Case failed,case test timeout.")
                    break
        else:
            a = threading.Thread(target=self.chip0_scan, args=(1,))
            b = threading.Thread(target=self.chip0_scan, args=(1, self.filters['filter_mac']))
            a.start()
            b.setDaemon(True)
            b.start()
            a.setDaemon(True)

            while True:
                if self.flag1 and self.flag2:
                    self.assertTrue(True)
                    self.logger.info('pass\n')
                    break
                elif self.timeout_flag:
                    self.logger.info('fail\n')
                    try:
                        self.fail('Case failed,start scan timeout.')
                    except:
                        print('Case failed,start scan timeout.')
                    self.logger.error("Case failed,start scan timeout.")
                    break

    def chip0_scan(self, active=0, filter_mac=None):
        # step1:chip 1 start passive scan,then start chip0 scan.
        with closing(self.sdk.scan(chip=0, active=active, filter_mac=filter_mac)) as self.sse1:
            count = 0
            for message in self.sse1:
                if message.startswith('data'):
                    msg = json.loads(message[5:])
                if filter_mac:
                    # 进入开启过滤的扫描结果判断流程
                    if count < 20:
                        print('chip0', count, message)
                        mac = msg['bdaddrs'][0]['bdaddr']
                        if mac != self.filters['filter_mac']:
                            self.fail('filter mac failed.')
                            self.logger.debug('filter mac failed.')
                            break
                        else:
                            count += 1
                    else:
                        self.flag1 = True
                        self.logger.debug('Step 1:chip0 start scan with filter mac success.')
                        break
                else:
                    # 进入不开启过滤的扫描结果判断流程
                    if count < 300:
                        print('chip0', count, message)
                        count += 1
                    else:
                        self.flag1 = True
                        self.logger.debug('Step 1:chip0 start scan with no filter mac success.')
                        break

    def chip1_scan(self, active=0, filter_mac=None):
        # step2:start chip0 scan.
        with closing(self.sdk.scan(chip=1, active=active, filter_mac=filter_mac)) as self.sse2:
            count = 0
            for message in self.sse2:
                if message.startswith('data'):
                    msg = json.loads(message[5:])
                    if filter_mac:
                        if count < 20:
                            print('chip1', count, message)
                            mac = msg['bdaddrs'][0]['bdaddr']
                            if mac != filter_mac:
                                self.fail('filter mac failed.')
                                self.logger.debug('filter mac failed.')
                                break
                            else:
                                count += 1
                        else:
                            self.flag2 = True
                            self.logger.debug('Step 2:chip1 start scan with filter mac success.')
                            break
                    else:
                        # 进入不开启过滤的扫描结果判断流程
                        if count < 300:
                            print('chip1', count, message)
                            count += 1
                        else:
                            self.flag2 = True
                            self.logger.debug('Step 2:chip1 start scan with no filter mac success.')
                            break

    def set_timeout(self):
        self.timeout_flag = True


if __name__ == '__main__':
    unittest.main()