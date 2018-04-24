# -*- coding: utf-8 -*-
'''
测试点：测试chip0 filter name主动扫描，chip1 不加过虑主动扫描

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
    sdk = tools.get_api()
    model = tools.get_model()
    filters = tools.get_filter()
    timeout = tools.read_job_config()['case_timeout']

    def setUp(self):
        self.timeout_flag = None
        self.flag1 = None
        self.flag2 = None
        self.logger.info('测试chip0 filter name主动扫描，chip1 不加过虑主动扫描')
        self.timer = Timer(self.timeout, self.set_timeout)
        self.timer.start()

    def tearDown(self):
        self.timer.cancel()

    #测试方法
    def test_scan_filter_name(self):
        if self.model.startswith('S') or self.model.startswith('s'):
            a = threading.Thread(target=self.chip0_scan,args = (1,self.filters['filter_name']))
            b = threading.Thread(target=self.chip0_scan,args = (1,))
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
        else:
            a = threading.Thread(target=self.chip0_scan,args = (1,self.filters['filter_name']))
            b = threading.Thread(target=self.chip1_scan,args = (1,))
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

    def chip0_scan(self,active = 0,filter_name = None):
        #step1:chip 1 start passive scan,then start chip0 scan.
        with closing(self.sdk.scan(chip=0,active=active,filter_name =filter_name )) as self.sse1:
            count = 0
            for message in self.sse1:
                if message.startswith('data'):
                    msg = json.loads(message[5:])
                if filter_name: 
                    #进入开启过滤的扫描结果判断流程
                    if count<20:
                        print('chip0', count, message)
                        name = msg['name']
                        if name != self.filters['filter_name']:
                            self.fail('filter name failed.')
                            self.logger.debug('filter name failed.')
                            break
                        else:
                            count += 1
                    else:
                        self.flag1 = True
                        self.logger.debug('Step 1:chip0 start scan with filter name success.')
                        break
                else:
                    #进入不开启过滤的扫描结果判断流程
                    if count<300:
                        print('chip0', count, message)
                        count += 1
                    else:
                        self.flag1 = True
                        self.logger.debug('Step 1:chip0 start scan with no filter name success.')
                        break                            

    def chip1_scan(self,active = 0,filter_name = None):
        #step2:start chip0 scan.
        with closing(self.sdk.scan(chip=1,active = active,filter_name = filter_name)) as self.sse2:
            count = 0
            tmp_name = []
            for message in self.sse2:
                if message.startswith('data'):
                    msg = json.loads(message[5:])
                    if filter_name:
                        if count<20:
                            print('chip1', count, message)
                            name = msg['name']
                            if name != filter_name:
                                self.fail('filter name failed.')
                                self.logger.debug('filter name failed.')
                                break
                            else:
                                count += 1
                        else:
                            self.flag2 = True
                            self.logger.debug('Step 2:chip1 start scan with filter name success.')
                            break
                    else:
                    #进入不开启过滤的扫描结果判断流程
                        if count<300:
                            print('chip1', count, message)
                            count += 1
                        else:
                            self.flag2 = True
                            self.logger.debug('Step 2:chip1 start scan with no filter name success.')
                            break                            
   
    def set_timeout(self):
        self.timeout_flag = True

if __name__ == '__main__':
    unittest.main()