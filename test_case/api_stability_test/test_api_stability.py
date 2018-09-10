import sys
import os
import threading
import random
import time
import json
from contextlib import closing

path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
from api import api
from logs import set_logger
from tools import read_stability_config, get_device_list
loop_error = False


class test_stability():

    # time_out_flag = False
    # case_end_flag = False
    # loop_error = False
    debug = []

    def __init__(self, conf):
        self.case_end_flag = False
        self.time_out_flag = False
        self.conf = conf
        self.sdk = api(self.conf['host'], self.conf[
                       'hub'], self.conf['user'], self.conf['pwd'])
        debug_file = "stability_debug_" + \
            "".join(self.conf['hub'].split(':')) + ".txt"
        error_file = "stability_error_" + \
            "".join(self.conf['hub'].split(':')) + '.txt'
        self.logger = set_logger(
            __name__, debugfile=debug_file, errorfile=error_file)

    def update_token(self):
        global headers
        headers = self.sdk.set_header()
        self.sdk.headers = headers
        timert = threading.Timer(350, self.update_token)
        timert.start()
        print("TOKEN更新")

    def init_run_env(self):
        self.time_out_flag = False
        self.case_end_flag = False

    def start_timer(self):
        # start timer to set timeout flag
        self.init_run_env()

        # self.timer = threading.Timer(self.conf['case_timeout'],self.set_timeout)
        self.timer = threading.Timer(5, self.set_timeout)
        self.timer.start()

    def end_timer(self):
        # cancel the timer to set timeout flag
        self.timer.cancel()

    def set_timeout(self):
        self.time_out_flag = True

    def loop(self, device_conf):
        print("开始时间：", time.time())
        self.loop = 1
        global loop_error
        timert = threading.Timer(600, self.update_token)
        timert.start()
        # self.test_discover_service(device_conf)
        while not loop_error:
            # if self.time_out_flag:
            #     print("time_out_flag==",self.time_out_flag)
            #     err = 'AP %s 超时导致失败\n' % (self.sdk.hub)
            #     self.debug.append(err)
            #     print("err==",err)
            #     self.errend()
            #     break
            # else:
            start = 'AP %s 开始第%d次循环...\n' % (self.sdk.hub, self.loop)
            print(start)
            # self.test_scan()
            self.test_connect_device(device_conf)
            self.test_connected_devlist()
            self.test_discover_service(device_conf)
            self.test_discover_characteristics(device_conf)
            self.test_discover_the_characteristics(device_conf)
            self.test_discover_descriptors(device_conf)
            self.test_discover_all(device_conf)
            time.sleep(1)
            end = 'AP %s 第%d次循环成功结束...\n' % (self.sdk.hub, self.loop)
            print(end)
            self.debug.append(end)
            for msg in self.debug:
                self.logger.info(msg)
            self.debug = []
            self.loop += 1
        print()
            print()
        timert.cancel()

    def errend(self):
        end = 'AP %s 第%d次循环异常结束...\n' % (self.sdk.hub, self.loop)
        print(end)
        for msg in self.debug:
            self.logger.error(msg)
        exit(1)

    def test_scan(self):
        print("start scan:", time.time())
        with closing(self.sdk.scan(chip=0)) as self.sse:
            i = 0
            for da in self.sse:
                data = da.decode()
                if data.startswith("data"):
                    debug = 'AP %s chip 0 start scan success!' % self.sdk.hub
                    self.debug.append(debug)
                    i = i + 1
                    if i >= 200:
                        print("AP={0} chip 0 start scan success!".format(
                            self.sdk.hub))
                        self.sse.close()
                        break
                    else:
                        pass
                else:
                    pass
        if self.conf['model'].upper().startswith('S'):
            print(self.conf['model'].upper())
            self.case_end_flag = True
            print('AP %s start scan success!' % self.sdk.hub)
        else:
            with closing(self.sdk.scan(chip=0)) as self.sse:
                j = 0
                for da in self.sse:
                    data = da.decode()
                    if data.startswith("data"):
                        # print("str(data)==", str(data))
                        debug = 'AP %s chip 0 start scan success!' % self.sdk.hub
                        self.debug.append(debug)
                        j = j + 1
                        if j >= 200:
                            print("AP={0} chip 1 start scan success!".format(
                                self.sdk.hub))
                            self.sse.close()
                            break
                        else:
                            pass
                    else:
                        pass
        print("end scan:", time.time())

    def test_connect_device(self, device_conf):
        j = 0
        global loop_error
        connect_flag = False
        for devtype in device_conf:
            types = device_conf[devtype]['device_type']
            timeout1 = 5000
            device_list = []
            for device in device_conf[devtype]['devices']:
                self.sdk.disconnect_device(device)
                device_list.append(device)
                if self.conf['model'].upper().startswith('S'):
                    chip = 0
                else:
                    random1 = random.randint(1, 10)
                    if random1 % 2 == 1:
                        chip = 1
                    else:
                        chip = 0
                for i in range(0, 5):
                    code, body, duration = self.sdk.connect_device(
                        device, types, chip, timeout1)
                    if code == 200:
                        connect_flag = True
                        j += 1
                        break
                if connect_flag:
                    for i1 in range(1, 4):
                        code1, body1 = self.sdk.get_devices_list(
                            state='connected')
                        if code1 == 200:
                            txt = json.loads(body1)
                            print("txt==", txt)
                            for i in range(0, len(txt['nodes'])):
                                if txt['nodes'][i]['bdaddrs']['bdaddr'] == device:
                                    if txt['nodes'][i]['chipId'] == chip:
                                        print('ap={0} device={1} connected success'.format(
                                            self.conf['hub'], device))
                                        break
                                    else:
                                        debug = 'ap={0} device={1} connect error'.format(
                                            self.conf['hub'], device)
                                        self.debug.append(debug)
                                        loop_error = True
                                        break
                        break
        if j == 0:
            err = 'ap={0} device={1} all connected failed'.format(
                self.conf['hub'], device_list)
            self.debug.append(err)
            loop_error = True
        else:
            self.case_end_flag = True

    def test_connected_devlist(self):
        code, body1 = self.sdk.get_devices_list('connected')
        global loop_error
        if code == 200:
            print("body==", body1)
            txt = json.loads(body1)['nodes']
            for i1 in range(0, len(txt)):
                if txt[i1]["connectionState"] == "connected":
                    print(" AP{0} get connected device:{1} success".format(
                        self.conf['hub'], txt[i1]['bdaddrs']['bdaddr']))
                else:
                    loop_error = True
                    debug = 'ap={0} get connected device list,return code={1}'.format(self.conf[
                                                                                      'hub'], code)
                    self.debug.append(debug)
                    break
            self.case_end_flag = True
        else:
            loop_error = True
            debug = 'ap={0} get connected device list,return code={1}'.format(self.conf[
                                                                              'hub'], code)
            self.debug.append(debug)

    def test_discover_service(self, device_conf):
        self.conn_flag = False
        global loop_error
        while not self.conn_flag:
            code, body = self.sdk.get_devices_list('connected')
            msg = json.loads(body)['nodes']
            print("ap测试={0} code测试={1}".format(self.conf['hub'], code))
            if code == 200:
                if len(msg) == 0:
                    self.test_connect_device(device_conf)
                    print("flag===", self.conn_flag)
                else:
                    dev = msg[0]['bdaddrs']['bdaddr']
                    for value in device_conf.values():
                        if dev in value['devices']:
                            sevice_uuid = value['service_uuid']
                            self.conn_flag = True
                            break
            else:
                loop_error = True
                debug = 'ap={0} get services before get devlist failed,return code={1},msg={2}'.format(
                    self.conf['hub'], code, text)
                self.debug.append(debug)
                # self.end_timer()
                break
        code, text = self.sdk.discovery_services(device=dev, uuid=sevice_uuid)
        if code == 200:
            self.case_end_flag = True
            print("服务：", text)
        else:
            loop_error = True
            debug = 'ap={0} get services failed,return code={1},msg={2}'.format(self.conf[
                                                                                'hub'], code, text)
            self.debug.append(debug)

    def test_discover_characteristics(self, device_conf):
        self.conn_flag = False
        global loop_error
        while not self.conn_flag:
            code, body = self.sdk.get_devices_list('connected')
            msg = json.loads(body)['nodes']
            print("ap测试特性={0} code测试特性={1}".format(self.conf['hub'], code))
            if code == 200:
                if len(msg) == 0:
                    self.test_connect_device(device_conf)
                    print("flag特性===", self.conn_flag)
                else:
                    dev = msg[0]['bdaddrs']['bdaddr']
                    for value in device_conf.values():
                        if dev in value['devices']:
                            sevice_uuid = value['service_uuid']
                            self.conn_flag = True
                            break
            else:
                loop_error = True
                debug = 'ap={0} get characteristic before get devlist failed,return code={1},msg={2}'.format(
                    self.conf['hub'],                                                                                                      code, text)
                self.debug.append(debug)
                # self.end_timer()
                break
        code, text = self.sdk.discovery_characteristics(dev, sevice_uuid)
        if code == 200:
            self.case_end_flag = True
            print("功能：", text)
        else:
            loop_error = True
            debug = 'ap={0} get characteristic failed,return code={1},msg={2}'.format(
                self.conf['hub'], code, text)
            self.debug.append(debug)

    def test_discover_the_characteristics(self, device_conf):
        self.conn_flag = False
        global loop_error
        while not self.conn_flag:
            code, body = self.sdk.get_devices_list('connected')
            msg = json.loads(body)['nodes']
            print("ap测试the特性={0} code测试the特性={1}".format(
                self.conf['hub'], code))
            if code == 200:
                if len(msg) == 0:
                    self.test_connect_device(device_conf)
                    print("flag特性===", self.conn_flag)
                else:
                    dev = msg[0]['bdaddrs']['bdaddr']
                    for value in device_conf.values():
                        if dev in value['devices']:
                            charac_uuid = value['charac_uuid']
                            self.conn_flag = True
                            break
            else:
                loop_error = True
                debug = 'ap={0} get the characteristic before get devlist failed,return code={1},msg={2}'.format(
                    self.conf['hub'], code, text)
                self.debug.append(debug)
                break
        code, text = self.sdk.discovery_characteristic(dev, charac_uuid)
        if code == 200:
            self.case_end_flag = True
            print("功能the charactersitic：", text)
        else:
            loop_error = True
            debug = 'ap={0} get the characteristic failed,return code={1},msg={2}'.format(
                self.conf['hub'], code, text)
            self.debug.append(debug)

    def test_discover_all(self, device_conf):
        self.conn_flag = False
        global loop_error
        while not self.conn_flag:
            code, body = self.sdk.get_devices_list('connected')
            msg = json.loads(body)['nodes']
            print("ap测试all={0} code测试all={1}".format(self.conf['hub'], code))
            if code == 200:
                if len(msg) == 0:
                    self.test_connect_device(device_conf)
                else:
                    dev = msg[0]['bdaddrs']['bdaddr']
                    self.conn_flag = True
            else:
                loop_error = True
                debug = 'ap={0} get the all before get devlist failed,return code={1},msg={2}'.format(
                    self.conf['hub'], code, text)
                self.debug.append(debug)
                break
        code, text = self.sdk.discover_all(dev)
        if code == 200:
            self.case_end_flag = True
            print("功能all：", text)
        else:
            loop_error = True
            debug = 'ap={0} get the all failed,return code={1},msg={2}'.format(self.conf[
                                                                               'hub'], code, text)
            self.debug.append(debug)

    def test_discover_descriptors(self, device_conf):
        self.conn_flag = False
        global loop_error
        while not self.conn_flag:
            code, body = self.sdk.get_devices_list('connected')
            msg = json.loads(body)['nodes']
            print("ap测试descriptors={0} code测试descriptors={1}".format(
                self.conf['hub'], code))
            if code == 200:
                if len(msg) == 0:
                    self.test_connect_device(device_conf)
                    print("flag descriptors===", self.conn_flag)
                else:
                    dev = msg[0]['bdaddrs']['bdaddr']
                    for value in device_conf.values():
                        if dev in value['devices']:
                            charac_uuid = value['charac_uuid']
                            self.conn_flag = True
                            break
            else:
                loop_error = True
                debug = 'ap={0} get the descriptors before get devlist failed,return code={1},msg={2}'.format(
                    self.conf['hub'], code, text)
                self.debug.append(debug)
                # self.end_timer()
                break
        code, text = self.sdk.discover_descriptors(dev, charac_uuid)
        if code == 200:
            self.case_end_flag = True
            print("功能descriptors：", text)
        else:
            loop_error = True
            debug = 'ap={0} get the descriptors failed,return code={1},msg={2}'.format(
                self.conf['hub'], code, text)
            self.debug.append(debug)


def main():
    conf1 = read_stability_config()
    ap_list = ['E1000']
    thread = []
    for ap in ap_list:
        # device_aplist = get_device_list[ap]
        conf_ap = conf1[ap]
        i = 1
        print("conf==", conf1[ap])
        for key in conf_ap:
            # device_conf['model']=ap
            i = i + 1
            device_conf = get_device_list(ap, key)
            # device_list=device_aplist[key]
            conf = conf1[ap][key]
            test = test_stability(conf)
            t = threading.Thread(target=test.loop, args=(device_conf,))
            thread.append(t)
            print("device配置:", device_conf)
    for t in thread:
        t.setDaemon(True)
        t.start()
    t.join()
    if loop_error:
        print("loop_error:", loop_error)
        print("异常退出")
        exit(1)
    print("当前线程-=", threading.active_count())
if __name__ == '__main__':
    main()
