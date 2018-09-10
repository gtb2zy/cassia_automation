import requests
import base64
import json
import threading
import time
import socket
import os
import paramiko
import csv
import logging

CLIENTS = []
client_configs = []
hubs = 0
BAK_APS = []
OFFLINE_APS = 0
CLIENT_INFO = []
TESTING = True
config = {}
REDIRECTED = False
logger = None


def get_logger():
    logger = logging.getLogger(__name__)
    formater = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    file_hander = logging.FileHandler('log.log', encoding='utf8')
    file_hander.setFormatter(formater)
    logger.addHandler(file_hander)
    logger.setLevel(logging.INFO)
    return logger


def myprint(*string):
    if REDIRECTED:
        for s in string:
            logger.info(s)
    else:
        print(*string)


def init_config():
    global config
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
                        if key == 'HOST':
                            config['host'] = value
                        elif key == 'server':
                            config['server'] = value
                        elif key == 'user':
                            config['user'] = value
                        elif key == 'pwd':
                            config['pwd'] = value
                        elif key == 'PROCESS_COUNT':
                            config['process_count'] = int(value)
                            config['process_no'] = 0
                        elif key == 'INTERVAL':
                            config['interval'] = int(value)
                        elif key == 'PER_COUNT':
                            config['per_count'] = int(value)
                        elif key == 'test_time':
                            config['test_time'] = int(value)
                        elif key == 'MAX_OFFLINE':
                            config['max_offline'] = int(value)
                        elif key == 'test_mode':
                            config['test_mode'] = value
                        elif key == 'ac_root_pwd':
                            config['ac_root_pwd'] = value
                        elif key == 'data_path':
                            config['data_path'] = value
                        else:
                            pass
    except Exception as e:
        myprint('配置文件打开失败', e)


def init_para():
    global client_configs, hubs, BAK_APS
    i = 0
    client_cfg = {}
    PROCESS_COUNT = config['process_count']
    set_header()
    hubs = get_online_hubs(headers)
    while i < config['max_offline']:
        # 预留一定数量的AP，掉线AP的备份
        BAK_APS.append(hubs.pop())
        i = i + 1
    hubs_per_pc = int(len(hubs) / PROCESS_COUNT)

    # 为每个客户端预生成测试数据
    for pc in range(0, PROCESS_COUNT):
        sleep_time = config['interval'] * int((hubs_per_pc / config['per_count'])) * pc
        start = hubs_per_pc * pc
        end = hubs_per_pc * (pc + 1)
        hub = hubs[start:end]
        # str_hub = ','.join(hub)
        client_cfg['msg_type'] = 'config_res'
        client_cfg['sleep_time'] = sleep_time
        client_cfg['interval'] = config['interval']
        client_cfg['per_count'] = config['per_count']
        client_cfg['hubs'] = hub
        client_cfg['user'] = config['user']
        client_cfg['pwd'] = config['pwd']
        client_cfg['host'] = config['host']
        client_cfg['test_mode'] = config['test_mode']
        client_configs.append(str(client_cfg))


# 设置请求头
def set_header():
    global headers, sethead_timer
    use_info = config['user'] + ':' + config['pwd']
    # 编码开发者帐号
    encode_info = base64.b64encode(use_info.encode('utf-8'))
    head = {'Content-Type': 'application/json', 'Authorization': 'Basic ' + encode_info.decode("utf-8")}
    data = {'grant_type': 'client_credentials'}
    try:
        # 发起请求
        res = requests.post(config['host'] + '/oauth2/token', data=json.dumps(data), headers=head)
        # myprint(res.url)
        # myprint(res.text,res.status_code)
        if res.status_code == 200:
            res_body = json.loads(res.text)
            # myprint(res_body.get("access_token"))
            TOKEN = res_body.get("access_token")
        elif res.status_code == 401:
            myprint('开发帐号错误')
        elif res.status_code == 400:
            myprint('API路径错误')
    except Exception as e:
        myprint(e)
    # myprint(TOKEN)
    headers = {'Content-Type': 'application/json', 'version': '1', 'Authorization': 'Bearer ' + TOKEN}
    # myprint(headers)
    sethead_timer = threading.Timer(3500, set_header)
    sethead_timer.start()


def connect_to_client(sock, addr):
    global data
    while True:
        if TESTING:
            try:
                data = sock.recv(1024)
                message = str(data, encoding='utf-8')
                data_type = message.split('+')[0].strip()
                # print(message)
                send_para(sock, message, data_type, addr)
            except ConnectionResetError:
                sock.close()
        else:
            break


def send_para(sock, data, data_type, addr):
    global CLIENTS
    if data_type == 'config_req':
        sock.send(bytes(client_configs[config['process_no']], encoding='utf-8'))
        msg = {'msg_type': 'session', 'session': config['process_no']}
        sock.send(bytes(str(msg), encoding='utf-8'))
    elif data_type == 'config_ok':
        CLIENTS.append(sock)
        config['process_no'] = config['process_no'] + 1
        CLIENT_INFO.append({'speed': 0, 'scanning_aps': 0})
        myprint("Client's %s:%s test parameters inited success！\n" % (addr[0], addr[1]))
        if config['process_no'] == config['process_count']:
            myprint('All pc has been inited success,test start !\n')
            start_test()
    elif data_type == 'sync':
        get_speed(data)
    elif data_type == 'bak_ap_scan':
        mac = data.split('+')[1].strip()
        myprint("Bak ap %s start scan success!\n" % mac)
    elif data_type == 'offline':
        start_bak_ap_scan(data)
    elif data_type == 6:
        pass


def start_bak_ap_scan(data):
    # 当有AP掉线，开启备用AP扫描
    global OFFLINE_APS
    mac = int(data.split('+')[1])
    session = int(data.split('+')[2])
    print('AP(%s)offline,will use backup AP ccontinue test！' % mac)
    # 判断离线AP是否超过限制
    if OFFLINE_APS < int(config['max_offline']):
        msg = str({'msg_type': 'bak_ap_scan', 'mac': BAK_APS[session]})
        CLIENTS[session].send(bytes(msg, encoding='utf8'))
        OFFLINE_APS += 1
    else:
        myprint('Too many aps offline,test stop with error!')
        stop_test()


def get_speed(data):
    total_ap = 0
    total_speed = 0
    session = int(data.split('+')[1])
    # myprint('session',session)
    speed = data.split('+')[2]
    scanning_aps = data.split('+')[3]
    CLIENT_INFO[session]['speed'] = speed
    CLIENT_INFO[session]['scanning_aps'] = scanning_aps
    for c in CLIENT_INFO:
        total_speed = total_speed + int(c.get('scanning_aps')) * int(c.get('speed'))
        total_ap = total_ap + int(c.get('scanning_aps'))
    if total_ap > 0:
        aver_speed = total_speed / total_ap
        times = time.strftime('%H-%M-%S', time.localtime(time.time()))
        myprint('%s:Scanning ap count is %d now,average scan speed is %d.\n' % (times, total_ap, aver_speed))


def get_online_hubs(headers):
    res = requests.get(config['host'] + '/cassia/hubs', headers=headers)
    res_hub_info = json.loads(res.text)
    hubs = []
    for i in res_hub_info:
        hubs.append(i['mac'])
    return hubs


def get_scanning_ap():
    total = 0
    global SCANNING_APS
    while True:
        for hub in SCANNING_APS:
            total = total + len(hub)
        if total < len(hubs):
            for client in CLIENTS:
                client.send(bytes('scanning_aps_req', encoding='utf-8'))
                time.sleep(1)
            time.sleep(10)
            total = 0
        else:
            myprint('All AP has started scan success!')
            break


def hubStatus():
    global OFFLINE_APS
    try:
        hub_status = requests.get(config['host'] + '/cassia/hubStatus', headers=headers, stream=True)
        for line in hub_status.iter_lines():
            if TESTING:
                message = str(line, encoding='utf-8')
                if message.startswith('data'):
                    message = json.loads(message[6:])
                    if OFFLINE_APS < int(config['max_offline']):
                        # 判断离线AP是否超过限制，如果超过则停止测试
                        if message['status'] == 'offline':
                            myprint('AP(%s)offline,will use backup AP ccontinue test！' % message['mac'])
                            for hubs in client_configs:
                                if message['mac'] in hubs:
                                    # 定位到离线AP属于哪个client
                                    session = client_configs.index(hubs)
                                    # 向上面定位到的client发送备用AP，并开启扫描
                                    msg = {'msg_type': 'bak_ap_scan', 'bak_aps': BAK_APS[OFFLINE_APS],
                                           'mac': message['mac']}
                                    CLIENTS[session].send(bytes(str(msg), encoding='utf-8'))
                                    msg['msg_type'] = 'scanning_aps_req'
                                    CLIENTS[session].send(bytes(str(msg), encoding='utf-8'))
                                    OFFLINE_APS = OFFLINE_APS + 1
                    else:
                        myprint('Too many AP offline,test failed ,stop!')
                        msg = {'msg_type': 'test_stop'}
                        for client in CLIENTS:
                            client.send(bytes(str(msg), encoding='utf-8'))
                            client.close()
                            time.sleep(1)
            else:
                break
    except Exception as e:
        myprint(e)


def stop_test():
    global TESTING, COPY_TIMER
    myprint("测试完成，准备停止测试...")
    TESTING = False
    sethead_timer.cancel()
    if str(config['test_mode']) == '0':
        try:
            COPY_TIMER.cancel()
        except BaseException:
            pass
    msg = {'msg_type': 'test_stop'}
    for client in CLIENTS:
        try:
            client.send(bytes(str(msg), encoding='utf-8'))
        except Exception as e:
            myprint(e)
            pass
        client.close()
    copy_file(False)


def start_test():
    global COPY_TIMER
    init_monitor_client()
    start_ac_monitor()
    if str(config['test_mode']) == '0':
        # 开启定时器，定时从AC拷贝测试数据到本地
        COPY_TIMER = threading.Timer(600, copy_file, args=(True,))
        COPY_TIMER.start()
    msg = {'msg_type': 'test_start'}
    for client in CLIENTS:
        # 向所有client发送测试开始信号
        try:
            client.send(bytes(str(msg), encoding='utf-8'))
        except Exception as e:
            myprint(e)
            pass
    # 开启测试结束定时器
    threading.Timer(config['test_time'], stop_test).start()


def start_ac_monitor():
    # 利用实例化的ssh和sftp客户端对象，开启AC上面的性能监控命令和工具
    ip = config['host'].split('/')[2]
    test_time = config['test_time']
    if test_time > 3600 * 3:
        interval = '30'
        count = str(int(int(test_time) / int(interval)))
    else:
        interval = '3'
        count = str(int(int(test_time) / int(interval)))
    cmd1 = '/tmp/nmon_x86_centos6 -f -N -m /tmp/res/ -s ' + interval + ' -c ' + count
    cmd2 = 'top -d ' + interval + ' -n ' + count + ' -b >>/tmp/res/monitor_data_top.txt 2>&1 &'
    cmd3 = 'pidstat -r ' + interval + ' ' + count + ' >>/tmp/res/monitor_data_mem.txt 2>&1 &'
    cmd4 = 'pidstat -d ' + interval + ' ' + count + ' >>/tmp/res/monitor_data_disk.txt 2>&1 &'
    try:
        if str(config['test_mode']) == '0':
            ssh_client.exec_command(cmd2)
            ssh_client.exec_command(cmd3)
            ssh_client.exec_command(cmd4)
        elif str(config['test_mode']) == '1':
            ssh_client.exec_command(cmd1)
            ssh_client.exec_command(cmd2)
        myprint('成功开启AC性能监控，数据文件保存在%s:/tmp/res/\n' % ip)
    except Exception as e:
        myprint('AC性能监控开启失败，\n', e)


def init_monitor_client():
    # 利用实例化的ssh和sftp客户端对象，删除AC上面旧的测试数据文件以及遗留的测试进程
    global sftp_client, ssh_client
    ip = config['host'].split('/')[2]
    try:
        # 初始化sftp客户端
        ftp = paramiko.Transport((ip, 22))
        ftp.connect(username='root', password=config['ac_root_pwd'])
        sftp_client = paramiko.SFTPClient.from_transport(ftp)
        # 初始化ssh客户端
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip, 22, 'root', config['ac_root_pwd'], timeout=5)
        myprint('Monitor client init successed!\n')
    except Exception as e:
        myprint('Monitor client init failed!\n')
        myprint(e)
    try:
        sftp_client.put('nmon_x86_centos6', '/tmp/nmon_x86_centos6')
    except Exception as e:
        myprint(e)
        myprint('自动上传nmon工具失败，请手动上传！')
    try:
        ssh_client.exec_command('mkdir -p /tmp/res/')
        ssh_client.exec_command('killall top')
        ssh_client.exec_command('killall pidstat')
        ssh_client.exec_command('killall nmon_x86_centos6')
        ssh_client.exec_command('chmod 777 /tmp/nmon_x86_centos6')
    except BaseException:
        pass

    src = config['data_path']
    try:
        history_files = sftp_client.listdir(src)
    except BaseException:
        sftp_client.mkdir(src)
        history_files = sftp_client.listdir(src)
    if len(history_files) > 0:
        for file in history_files:
            sftp_client.remove(src + file)
        myprint('成功删除历史遗留数据文件!\n')


# 从AC拷贝数据文件
def copy_file(flag=True):
    global COPY_TIMER
    no = 0
    src = '/tmp/res/'
    myprint('开始从服务器拷贝文件到本地\n')
    try:
        ssh_client.exec_command('mkdir -p %s' % config['data_path'])
    except BaseException:
        pass
    try:
        files = sftp_client.listdir('/tmp/res/')
        for file in files:
            sftp_client.get(src + file, config['data_path'] + file)
        myprint('成功从AC拷贝测试结果文件到目录%s\n' % config['data_path'])
        write_csv()
    except BaseException:
        # 只有在结束测试时，拷贝失败尝试重新拷贝,默认为不重试
        while no < 3:
            try:
                myprint('从服务器copy文件失败,正在重试\n')
                files = sftp_client.listdir('/tmp/res/')
                for file in files:
                    sftp_client.get(src + file, config['data_path'] + file)
                write_csv()
            except Exception as e:
                myprint(e)
            no += 1
        myprint('从服务器copy文件失败，请手动copy\n')

    '''通过标志位判断是否继续调用自身，当停止测试最后一次调用时，flag应该为false,
        否则程序不能自动结束运行。
    '''
    if flag:
        COPY_TIMER = threading.Timer(600, copy_file, )
        COPY_TIMER.start()


# 提取测试数据，并写入到data_path目录下的data.csv文件中
def write_csv():
    data_path = config['data_path']
    for file in os.listdir(data_path):
        filename, extend_name = file.split('.')[0], file.split('.')[1]
        if extend_name == 'txt':
            myprint('开始处理测试数据文件%s...\n' % filename)
            with open(data_path + file, 'r', encoding='utf-8') as f:
                nfm_rows = [['name', 'CPU', 'MEM']]
                ac_rows = [['name', 'CPU', 'MEM']]
                mongod_rows = [['name', 'CPU', 'MEM']]
                cpu_total_rows = [['name', 'us', 'sy', 'id', 'wa', 'si']]
                mem_total_rows = [['name', 'free', 'used', 'total', 'buff']]
                nodes = {}
                for line in f:
                    try:
                        if 'NFM' in line:
                            data = line.split()
                            name, cpu, mem = data[11], data[8], data[9]
                            nfm_rows.append([name, cpu, mem])
                        elif 'node' in line:
                            data = line.split()
                            if data[0] in nodes:
                                name, cpu, mem = data[11] + '_' + data[0], data[8], data[9]
                                nodes.get(data[0]).append([name, cpu, mem])
                            else:
                                nodes[data[0]] = [['name', 'CPU', 'MEM']]
                                name, cpu, mem = data[11] + '_' + data[0], data[8], data[9]
                                nodes.get(data[0]).append([name, cpu, mem])
                        elif 'AC' in line:
                            data = line.split()
                            name, cpu, mem = data[11], data[8], data[9]
                            ac_rows.append([name, cpu, mem])
                        elif 'mongod' in line:
                            data = line.split()
                            name, cpu, mem = data[11], data[8], data[9]
                            mongod_rows.append([name, cpu, mem])
                        elif line.startswith('Cpu'):
                            data = line.split()
                            cpu_total_rows.append(
                                ['CPU_total', data[1].split('%')[0], data[2].split('%')[0], data[4].split('%')[0],
                                 data[5].split('%')[0], data[7].split('%')[0]])
                        elif line.startswith('Mem'):
                            data = line.split()
                            mem_total_rows.append(
                                ['MEM_total', int(int(data[5][:-1]) / 1024), int(int(data[3][:-1]) / 1024),
                                 int(int(data[1][:-1]) / 1024), int(int(data[7][:-1]) / 1024)])
                    except BaseException:
                        pass
                with open(data_path + filename + '.csv', 'w', newline='') as f:
                    csv_write = csv.writer(f, dialect='excel')
                    min_len = min(len(ac_rows), len(nfm_rows), len(mongod_rows), len(mem_total_rows),
                                  len(cpu_total_rows))
                    for i in range(min_len):
                        row = []
                        node = [x[i] for _, x in nodes.items()]
                        for x in node:
                            for y in x:
                                row.append(y)
                        L = ac_rows[i] + nfm_rows[i] + mongod_rows[i] + mem_total_rows[i] + cpu_total_rows[i] + row
                        csv_write.writerow(L)
            myprint('数据处理完成，结果文件到目录%s\n' % data_path)


def main():
    global TESTING, logger
    init_config()
    init_para()
    logger = get_logger()
    sk = socket.socket()
    # localIP = socket.gethostbyname(socket.gethostname())  # 获取本机IP，windows
    localIP = config['server']
    sk.bind((localIP, 8080))
    sk.listen(5)
    myprint("#######################################################")
    myprint("Monitor stared,listening on %s waiting for client connect...." % localIP)
    myprint("#######################################################")
    # 等待测试客户端连接
    while config['process_no'] != config['process_count']:
        try:
            sock, addr = sk.accept()
            myprint('New connect from :', addr)
            sock.send(bytes('client_hello', encoding='utf-8'))
            threading.Thread(target=connect_to_client, args=(sock, addr)).start()
        except Exception as e:
            myprint(e)

    # 阻塞主线程，监听测试中止信号ctrl + c
    try:
        while TESTING:
            # 通过TESTING变量判断测试是否正常完成
            time.sleep(1)
    except KeyboardInterrupt:
        # 一旦程序抛出KeyboardInterrupt异常，捕获异常，退出程序
        stop_test(CLIENTS)
        myprint('检测到CTRL-C，测试终止....')


if __name__ == '__main__':
    main()
