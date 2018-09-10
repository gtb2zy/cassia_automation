import requests
import base64
import json
import threading
import time
import socket
import sys

scanning_aps = []
headers = {}
scan_data_count = 0
counts = 0
SSE_CLIENT = {}
active = None
ac_root_pwd = ''
data_path = ''
TESTING = True
speed = 0
# global MONITOR, ssh_client, sftp_client, copy_timer


# 读取配置文件
def init_config():
    global server
    try:
        with open('test.conf', 'r', encoding='utf-8') as conf:
            for line in conf:
                line = line.strip()
                if line:
                    if line.startswith('#'):
                        pass
                    else:
                        key = line.split('=')[0].strip()
                        value = line.split('=')[1].strip()
                        if key == 'server':
                            server = value
            print('配置文件读取成功,成功获取到server地址！')
    except Exception as e:
        print('配置文件打开失败,无法连接到服务端，测试异常结束！失败原因:\n', e)
        sys.exit()


# 客户端，负责与服务器的连接，并且接收从服务器发来的数据
def connect_to_server():
    global sock
    while True:
        sock = socket.socket()
        sock.connect((server, 8080))
        time.sleep(.5)
        data = sock.recv(1024)
        message = str(data, encoding='utf-8')
        if message == 'client_hello':
            print('Connect to server success!')
            break
        else:
            sock.close()
            sock = None
            print('connect to server failed,wait for reconnect!')
    sock.send(bytes('config_req', encoding='utf-8'))
    while True:
        if TESTING:
            try:
                data = sock.recv(51200)
                message = eval(str(data, encoding='utf-8'))
                data_type = message['msg_type']
                send_para(sock, message, data_type)
            except ConnectionResetError:
                print('服务端异常结束，测试停止！')
                stop_test()
        else:
            return


# 数据处理函数，负责解析从服务器接受到的参数以及向服务器发送数据
def send_para(sock, data, data_type):
    # 定义全局测试参数
    global sessionID
    if data_type == 'config_res':
        get_test_data(data)
        set_header()
    elif data_type == 'test_start':
        start_test()
    elif data_type == 'session':
        sessionID = data['session']
    elif data_type == 'bak_ap_scan':
        mac = data['mac']
        threading.Thread(target=scan, args=(sock, mac, True,)).start()
    elif data_type == 'test_stop':
        stop_test()


def get_test_data(data):
    global START_TIME, INTERVAL, PER_COUNT, HUBS, user, pwd, HOST, test_mode
    sock.send(bytes('config_ok', encoding='utf-8'))
    # 解析并设置从服务器获取的全局测试参数
    START_TIME = data['sleep_time']
    INTERVAL = data['interval']
    PER_COUNT = data['per_count']
    HUBS = data['hubs']
    user = data['user']
    pwd = data['pwd']
    HOST = data['host']
    test_mode = int(data['test_mode'])
    print('######################################################')
    print("     成功从控制器获取测试数据，等待测试开始！")
    print('######################################################')


# 开始AP扫描
def scan(sock, mac, bak=False):
    # print('thread %s is running...' % threading.current_thread().name)
    global scanning_aps, scan_data_count, HOST, headers
    flag = True
    try:
        data = {"event": 1, 'mac': mac}
        res = requests.get(HOST + '/gap/nodes', params=data, headers=headers, stream=True)
        for line in res.iter_lines():
            s = str(line, encoding='utf-8')
            if s.startswith('data'):
                # 检查是否为第一条扫描数据，是第一条的话就将开启扫描的AP数量+1；该条件语句只会执行一次
                if flag:
                    # 检查是否为备用AP开启扫描
                    if bak:
                        print("Bak ap %s start scan success!" % mac)
                        scanning_aps.append(mac)
                        SSE_CLIENT[mac] = res
                        # 向server响应备用AP扫描是否开启成功
                        sock.send(bytes('bak_ap_scan+' + mac, encoding='utf-8'))
                        print('当前扫描的AP总数为：{len(scanning_aps)}\n\n', end='')
                        flag = False
                        scan_data_count = scan_data_count + 1
                    else:
                        print("AP %s start scan success!" % mac)
                        scanning_aps.append(mac)
                        SSE_CLIENT[mac] = res
                        print('当前扫描的AP总数为：%s\n\n' % len(scanning_aps), end='')
                        flag = False
                        scan_data_count = scan_data_count + 1
                else:
                    scan_data_count = scan_data_count + 1
    except Exception as e:
        if str(e) == "'NoneType' object has no attribute 'read'":
            pass
        else:
            print('SSE closeed!', threading.current_thread().name, e)


def sync_to_server():
    global scanning_aps
    while True:
        if TESTING:
            sock.send(
                bytes('sync+' + str(sessionID) + '+' + str(speed) + '+' + str(len(scanning_aps)), encoding='utf-8'))
            time.sleep(10)
        else:
            return


# 计算AP的sap秒速度，该速度为平均值
def scan_speed():
    global scan_data_count, scanning_aps, counts, speed_timer, speed
    per_time = 10
    if len(scanning_aps) > 0:
        speed = int((scan_data_count - counts) / (per_time * len(scanning_aps)))
    else:
        print('WARNING:NO AP SCANNING NOW!!!\n')
        speed_timer = threading.Timer(per_time, scan_speed).start()
        return
    print('当前平均每台AP的扫描速度为:%d\n' % speed)
    date = time.strftime('%m-%d:%H:%M:%S', time.localtime())
    with open('speed.txt', 'a') as f:
        f.write(date + '--' + str(speed) + '\n')
    counts = scan_data_count
    speed_timer = threading.Timer(per_time, scan_speed)
    speed_timer.start()


# 设置请求头
def set_header():
    global headers, set_head_timer, HOST, TOKEN
    use_info = user + ':' + pwd
    # 编码开发者帐号
    encode_info = base64.b64encode(use_info.encode('utf-8'))
    head = {'Content-Type': 'application/json', 'Authorization': 'Basic ' + encode_info.decode("utf-8")}
    data = {'grant_type': 'client_credentials'}
    try:
        # 发起请求
        res = requests.post(HOST + '/oauth2/token', data=json.dumps(data), headers=head)
        # print(res.text,res.status_code)
        if res.status_code == 200:
            res_body = json.loads(res.text)
            # print(res_body.get("access_token"))
            TOKEN = res_body.get("access_token")
        elif res.status_code == 401:
            print('开发帐号错误')
        elif res.status_code == 400:
            print('API路径错误')
    except Exception as e:
        print(e)
    headers = {'Content-Type': 'application/json', 'version': '1', 'Authorization': 'Bearer ' + TOKEN}
    set_head_timer = threading.Timer(3500, set_header, (user, pwd))
    set_head_timer.start()


# 一次性开启所有在线AP扫描
def all_ap_scan(sock, hubs):
    print('AP总数量为%d，开始扫描！\n' % len(hubs))
    threads = []
    for hub in hubs:
        threads.append(threading.Thread(target=scan, args=(sock, hub,)))
    for t in threads:
        t.start()


# 分步骤逐渐开启AP扫描
def scan_by_interval(hubs, interval, per_count, start_time=0):
    i = 0
    j = per_count
    # 根据start_time，判断什么时候开始扫描
    time.sleep(start_time)
    print('AP总数量为%d，开始扫描！\n' % len(hubs))
    while True:
        if i < j:
            threading.Thread(target=scan, args=(sock, hubs[i],)).start()
            i = i + 1
        else:
            j = j + per_count
            if j > len(hubs):
                while j < len(hubs) - 1:
                    threading.Thread(target=scan, args=(sock, hubs[i],)).start()
                    j = j + 1
                break
            time.sleep(interval)


def hubStatus():
    global OFFLINE_APS, scanning_aps
    hub_status = requests.get(HOST + '/cassia/hubStatus', headers=headers, stream=True)
    for line in hub_status.iter_lines():
        if TESTING:
            message = str(line, encoding='utf-8')
            if message.startswith('data'):
                message = json.loads(message[6:])
                # 判断离线AP,准备开启备用AP扫描
                if message['status'] == 'offline':
                    scanning_aps.remove(message['mac'])
                    print('AP(%s)offline,will use backup AP ccontinue test！' % message['mac'])
                    msg = 'offline+%s+%d' % (message['mac'], sessionID)
                    sock.send(bytes(msg, encoding='utf8'))
        else:
            return


def start_test():
    # 开启子线程监控AP离线
    t = threading.Thread(target=hub_status)
    t.setDaemon(True)
    t.start()
    if test_mode == 0:
        print('开始稳定性测试。。。\n')
        # 开启所有AP扫描
        all_ap_scan(sock, HUBS)
        # 开启子线程，监控AP离线事件
        threading.Thread(target=hubStatus).start()
        # 开启定时器，时时计算扫描速度
        threading.Timer(10, scan_speed).start()
        time.sleep(10)
        # 开启定时器，时时同步测试状态到服务端
        threading.Thread(target=sync_to_server).start()
    elif test_mode == 1:
        print('开始性能测试。。。\n')
        if START_TIME > 0:
            print('According to test plan config,Waiting %d seconds to start test...' % START_TIME)
        threading.Thread(target=scan_by_interval, args=(HUBS, INTERVAL, PER_COUNT, START_TIME,)).start()
        threading.Timer(10, scan_speed).start()
        threading.Thread(target=sync_to_server).start()


def stop_test():
    global TESTING
    TESTING = False
    try:
        sock.close()
        speed_timer.cancel()
        print('Stop ap scan speed monitor thread!\n')
        set_head_timer.cancel()
        print('Stop token update thread!\n')
    except Exception as e:
        print(e)
    print('Stopping ap scan...\n')
    for key, value in SSE_CLIENT.items():
        value.close()
    print('All ap have stoped scan!\n\nTest finished!\n')


# 监控AP上下线
def hub_status():
    global SSE_CLIENT, MONITOR, scaning_aps
    try:
        MONITOR = requests.get(HOST + '/cassia/hubStatus', headers=headers, stream=True)
        for line in MONITOR.iter_lines():
            message = str(line, encoding='utf-8')
            if message.startswith('data'):
                message = json.loads(message[6:])
                if message['status'] == 'online':
                    print('AP %s 上线，尝试开启扫描...' % message['mac'])
                    threading.Thread(target=scan, args=(None, message['mac'], False)).start()
                elif message['status'] == 'offline':
                    print('AP %s 离线，正在停止扫描...' % message['mac'])
                    SSE_CLIENT.get(message['mac']).close()
                    SSE_CLIENT.pop(message['mac'])
                    scaning_aps.remove(message['mac'])
                    print('当前扫描的AP总数为：%s\n\n' % len(scaning_aps), end='')
            else:
                pass
    except BaseException:
        print('Stop monitor ap.')


def main():
    global headers, speed_timer, server
    try:
        host = sys.argv[1]
        server = host
    except IndexError:
        print('未通过命令行获取到server地址，尝试读取配置文件！')
        init_config()
    try:
        connect_to_server()
    except Exception as e:
        print('Connected to server failed!\n', e)


if __name__ == '__main__':
    main()
