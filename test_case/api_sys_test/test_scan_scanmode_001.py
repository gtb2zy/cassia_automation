# -*- coding: utf-8 -*-
'''
测试点：测试设备的主被动扫描切换功能

'''

import unittest, json, sys, os, json
from contextlib import closing
from threading import Timer
path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
from tools import get_api, get_model
from logs import set_logger


class testcase(unittest.TestCase):
    logger = set_logger(__name__)
    api = get_api()
    model = get_model()

    def setUp(self):
        self.logger.info('测试设备的主被动扫描切换功能')
        self.timer = Timer(30, self.close)
        self.timer.start()

    def tearDown(self):
        self.timer.cancel()

    # noinspection PyUnreachableCode,PyUnreachableCode,PyUnreachableCode,PyUnreachableCode,PyUnreachableCode,PyUnreachableCode,PyUnreachableCode
    def test_change_scan_mode(self):
        flag = None
        count = 0
        if self.model.startswith('S') or self.model.startswith('s'):
            with closing(self.api.scan(active=0)) as self.sse1:
                count = 0
                for data1 in self.sse1:
                    if count < 200:
                        if 'scanData' in data1:
                            self.fail('passive scan start fail')
                            self.logger.error('passive scan start fail')
                            break
                        else:
                            count += 1
                            flag = True
                    else:
                        flag = True
                        # self.sse.close()
                        self.logger.debug('Step1:passive scan start success')
                        break
            with closing(self.api.scan(active=1)) as self.sse2:
                count = 0
                for data2 in self.sse2:
                    if count < 200:
                        if 'scanData' in data2:
                            flag = True
                            self.logger.debug(
                                'Step2:Active scan start success')
                            break
                        else:
                            count += 1
                    else:
                        self.fail('Active scan start failed')
                        self.logger.error('Step2:Active scan start fail')
                        break
            with closing(self.api.scan(active=0)) as self.sse3:
                count = 0
                for data3 in self.sse3:
                    if count < 200:
                        if 'scanData' in data3:
                            self.fail('passive scan start fail')
                            self.logger.error('passive scan start fail')
                            break
                        else:
                            count += 1
                    else:
                        flag = True
                        self.logger.debug('Step3:passive scan start success')
                        break
            with closing(self.api.scan(active=1)) as self.sse4:
                count = 0
                for data4 in self.sse4:
                    if count < 200:
                        if 'scanData' in data4:
                            flag = True
                            self.logger.debug('Step5:Active scan start success')
                            break
                        else:
                            count += 1
                    else:
                        self.fail('Active scan start failed')
                        self.logger.error('Step5:Active scan start fail')
                        break
            self.assertTrue(flag)
            if flag:
                self.logger.info('pass\n')
            else:
                self.logger.info('fail\n')
        else:
            with closing(self.api.scan(active=0)) as self.sse1:
                count = 0
                for data1 in self.sse1:
                    if count < 200:
                        if 'scanData' in data1:
                            self.fail('passive scan start fail')
                            self.sse1.close()
                            self.logger.error('passive scan start fail')
                        else:
                            count += 1
                            flag = True
                    else:
                        flag = True
                        # self.sse.close()
                        self.logger.debug('Step1:passive scan start success')
                        break
            with closing(self.api.scan(active=1)) as self.sse2:
                count = 0
                for data2 in self.sse2:
                    if count < 200:
                        if 'scanData' in data2:
                            flag = True
                            self.logger.debug(
                                'Step1:Active scan start success')
                            break
                        else:
                            count += 1
                            flag = True
                    else:
                        self.fail('Active scan start failed')
                        self.sse2.close()
                        self.logger.error('Step2:Active scan start success')
            with closing(self.api.scan(active=0)) as self.sse3:
                count = 0
                for data3 in self.sse3:
                    if count < 200:
                        if 'scanData' in data3:
                            self.fail('passive scan start fail')
                            self.sse3.close()
                            self.logger.error('passive scan start fail')
                        else:
                            count += 1
                            flag = True
                    else:
                        flag = True
                        self.logger.debug('Step3:passive scan start success')
                        break
            with closing(self.api.scan(active=1)) as self.sse4:
                count = 0
                for data4 in self.sse4:
                    if count < 200:
                        if 'scanData' in data4:
                            flag = True
                            self.logger.debug(
                                'Step1:Active scan start success')
                            break
                        else:
                            count += 1
                            flag = True
                    else:
                        self.fail('Active scan start failed')
                        self.sse4.close()
                        self.logger.error('Step4:Active scan start success')
            with closing(self.api.scan(chip=1, active=0)) as self.sse5:
                count = 0
                for data1 in self.sse5:
                    if count < 200:
                        if 'scanData' in data1:
                            self.fail('passive scan start fail')
                            self.sse5.close()
                            self.logger.error('passive scan start fail')
                        else:
                            count += 1
                            flag = True
                    else:
                        flag = True
                        # self.sse.close()
                        self.logger.debug('Step1:passive scan start success')
                        break
            with closing(self.api.scan(chip=1, active=1)) as self.sse6:
                count = 0
                for data2 in self.sse6:
                    if count < 200:
                        if 'scanData' in data2:
                            flag = True
                            self.logger.debug(
                                'Step1:Active scan start success')
                            break
                        else:
                            count += 1
                            flag = True
                    else:
                        self.fail('Active scan start failed')
                        self.sse6.close()
                        self.logger.error('Step2:Active scan start success')
            with closing(self.api.scan(chip=1, active=0)) as self.sse7:
                count = 0
                for data3 in self.sse7:
                    if count < 200:
                        if 'scanData' in data3:
                            self.fail('passive scan start fail')
                            self.sse7.close()
                            self.logger.error('passive scan start fail')
                        else:
                            count += 1
                            flag = True
                    else:
                        flag = True
                        self.logger.debug('Step3:passive scan start success')
                        break
            with closing(self.api.scan(chip=1, active=1)) as self.sse8:
                count = 0
                for data4 in self.sse8:
                    if count < 200:
                        if 'scanData' in data4:
                            flag = True
                            self.logger.debug(
                                'Step1:Active scan start success')
                            break
                        else:
                            count += 1
                            flag = True
                    else:
                        self.fail('Active scan start failed')
                        self.sse8.close()
                        self.logger.error('Step4:Active scan start success')
            if flag:
                self.logger.info('pass\n')
            else:
                self.logger.info('fail\n')

    # noinspection PyUnreachableCode
    def close(self):
        self.fail("Case failed,start scan timeout.")
        self.logger.error("Case failed,start scan timeout.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
