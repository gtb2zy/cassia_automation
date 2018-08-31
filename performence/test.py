import requests
import base64
import json
import threading
import os
import time
import paramiko
import csv

config = {}
scanning_aps = []
scan_data_count = 0
counts = 0
REDIRECTED = True


def myprint(string):
    if REDIRECTED:
        with open('/tmp/performence/log.log', 'a', encoding='utf8') as f:
            f.writelines(string)
    else:
        print(string)


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
        print('配置文件打开失败', e)


# 设置请求头
def set_header():
    global headers, sethead_timer
    use_info = config['user'] + ':' + config['pwd']
    # 编码开发者帐号
    encode_info = base64.b64encode(use_info.encode('utf-8'))
    head = {'Content-Type': 'application/json',
            'Authorization': 'Basic ' + encode_info.decode("utf-8")}
    data = {'grant_type': 'client_credentials'}
    try:
        # 发起请求
        res = requests.post(
            config['host'] + '/oauth2/token', data=json.dumps(data), headers=head)
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
    headers = {'Content-Type': 'application/json',
               'version': '1', 'Authorization': 'Bearer ' + TOKEN}
    # print(headers)
    sethead_timer = threading.Timer(3500, set_header)
    sethead_timer.start()


def revive_data():
    # print('thread %s is running...' % threading.current_thread().name)
    HOST = config['host']
    global scan_data_count, res
    host = HOST + '/aps/events'
    try:
        res = requests.get(host, headers=headers, stream=True)
        for line in res.iter_lines():
            s = str(line, encoding='utf-8')
            if 'scan' in s:
                scan_data_count = scan_data_count + 1
    except Exception as e:
        if str(e) == "'NoneType' object has no attribute 'read'":
            pass
        else:
            print('SSE closeed!', e)


# 计算AP的sap秒速度，该速度为平均值
def scan_speed():
    global speed_timer, counts
    per_time = 10
    if len(scanning_aps) > 0:
        speed = int((scan_data_count - counts) /
                    (per_time * len(scanning_aps)))
        print('当前扫描AP数量为%d,平均每台AP的扫描速度为:%d\n' % (len(scanning_aps), speed))
    else:
        print('WARNING:NO AP SCANNING NOW!!!\n')
        speed_timer = threading.Timer(per_time, scan_speed)
        speed_timer.start()
        return
    date = time.strftime('%m-%d:%H:%M:%S', time.localtime())
    with open('speed.txt', 'a') as f:
        f.write(date + '--' + str(speed) + '\n')
    counts = scan_data_count
    speed_timer = threading.Timer(per_time, scan_speed)
    speed_timer.start()

# 逐渐开启AP扫描


def scan_by_interval(hubs):
    INTERVAL = config['interval']
    PER_COUNT = config['per_count']
    print('online hubs:', len(hubs))
    i = 0
    j = PER_COUNT
    tmp = []
    while True:
        if len(hubs) > PER_COUNT:
            if i < j:
                tmp.append(hubs[i])
                i = i + 1
            else:
                start_scan(tmp)
                time.sleep(INTERVAL)
                tmp = []
                j = j + PER_COUNT
                if j > len(hubs):
                    while j < len(hubs) - 1:
                        tmp.append(hubs[i])
                        j = j + 1
                    start_scan(tmp)
                    break
        else:
            start_scan(hubs)


def start_scan(hubs):
    global scanning_aps
    HOST = config['host']
    host = HOST + '/aps/scan/open'
    data = {"aps": hubs, "chip": 0, "active": 0}
    res = requests.post(host, data=json.dumps(data), headers=headers)
    if res.status_code == 202:
        scanning_aps += hubs
        print('当前扫描的AP数量为：', len(scanning_aps))


def get_online_hubs():
    HOST = config['host']
    res = requests.get(HOST + '/cassia/hubs', headers=headers)
    res_hub_info = json.loads(res.text)
    hubs = []
    if len(res_hub_info) > 0:
        for i in res_hub_info:
            if isinstance(i, dict):
                hubs.append(i['mac'])
        return hubs
    else:
        print('no ap online!!')


def start_ac_monitor(test_time):
    # 开始新的监控进程，生成全新的测试文件
    HOST = config['host']
    ip = HOST.split('/')[2]
    INTERVAL = config['interval']
    if test_time > 3600 * 3:
        INTERVAL = '30'
        count = str(int(test_time) / int(INTERVAL))
    else:
        INTERVAL = '3'
        count = str(int(test_time) / int(INTERVAL))
    cmd1 = '/tmp/performence/nmon_x86_centos6 -f -N -m /root/res/ -s ' + INTERVAL + ' -c ' + count
    cmd2 = 'top -d ' + INTERVAL + ' -n ' + count + \
        ' -b >>/tmp/performence/monitor_data_top.txt 2>&1 &'
    cmd3 = 'pidstat -r ' + INTERVAL + ' ' + count + \
        ' >>/tmp/performence/monitor_data_mem.txt 2>&1 &'
    cmd4 = 'pidstat -d ' + INTERVAL + ' ' + count + \
        ' >>/tmp/performence/monitor_data_disk.txt 2>&1 &'
    try:
        ssh_client.exec_command(cmd1)
        ssh_client.exec_command(cmd2)
        ssh_client.exec_command(cmd3)
        ssh_client.exec_command(cmd4)
        print('成功开启AC性能监控，数据文件保存在%s:/root/res/\n' % ip)
    except Exception as e:
        print('AC性能监控开启失败，\n', e)


def init_monitor_client():
    # 初始化性能监控工具
    global sftp_client, ssh_client
    HOST = config['host']
    ip = HOST.split('/')[2]
    try:
        # 初始化sftp客户端
        ftp = paramiko.Transport((ip, 22))
        ftp.connect(username='root', password=config['ac_root_pwd'])
        sftp_client = paramiko.SFTPClient.from_transport(ftp)
        # 初始化ssh客户端
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip, 22, 'root', config['ac_root_pwd'])
        print('Monitor client init successed!\n')
    except Exception as e:
        print('Monitor client init failed!\n')
        print(e)
    try:
        ssh_client.exec_command('killall top')
        ssh_client.exec_command('killall pidstat')
        ssh_client.exec_command('killall nmon_x86_centos6')
    except:
        pass
    src = '/root/res/'
    try:
        history_files = sftp_client.listdir(src)
    except Exception as e:
        print(e)
        sftp_client.mkdir(src)
        history_files = sftp_client.listdir(src)
    if len(history_files) > 0:
        print('删除历史遗留数据文件!\n')
        for file in history_files:
            sftp_client.remove(src + file)

# 从AC拷贝数据文件


def copy_file():
    global COPY_TIMER
    no = 0
    src = '/root/res/'
    path = config['data_path']
    print('开始从服务器拷贝文件到本地\n')
    try:
        files = sftp_client.listdir('/root/res/')
        for file in files:
            sftp_client.get(src + file, path + file)
        print('成功从AC拷贝测试结果文件到目录%s\n' % path)
    except Exception as e:
        # 只有在结束测试时，拷贝失败尝试重新拷贝,默认为不重试
        while no < 3:
            try:
                print('从服务器copy文件失败,正在重试\n')
                files = sftp_client.listdir('/root/res/')
                for file in files:
                    sftp_client.get(src + file, path + file)
            except Exception as e:
                print(e)
            no += 1
        print('从服务器copy文件失败，请手动copy\n', e)
        return

    write_csv()
    '''通过标志位判断是否继续调用自身，当停止测试最后一次调用时，flag应该为false,
        否则程序不能自动结束运行。
    '''
    # if flag:
    #   COPY_TIMER = threading.Timer(600,copy_file,)
    #   COPY_TIMER.start()
    # else:
    #   pass

# 提取测试数据，并写入到data_path目录下的data.csv文件中


def write_csv():
    data_path = 'result/'
    for file in os.listdir(data_path):
        filename = file.split('.')[0]
        if filename == 'monitor_data_top':
            print('开始处理测试数据文件...\n')
            with open(data_path + file, 'r', encoding='utf-8') as f:
                nfm_rows = [['name', 'CPU', 'MEM']]
                ac_rows = [['name', 'CPU', 'MEM']]
                mongod_rows = [['name', 'CPU', 'MEM']]
                node_rows = [['name', 'CPU', 'MEM']]
                cpu_total_rows = [['name', 'us', 'sy', 'id', 'wa', 'si']]
                mem_total_rows = [['name', 'free', 'used', 'total', 'buff']]
                for line in f:
                    # print(line)
                    try:
                        if 'NFM' in line:
                            data = line.split()
                            name, cpu, mem = data[11], data[8], data[9]
                            nfm_rows.append([name, cpu, mem])
                        elif 'node' in line:
                            # print(line)
                            data = line.split()
                            name, cpu, mem = data[11] + \
                                '_' + data[0], data[8], data[9]
                            node_rows.append([name, cpu, mem])
                        elif 'AC' in line:
                            # print(line)
                            data = line.split()
                            name, cpu, mem = data[11], data[8], data[9]
                            ac_rows.append([name, cpu, mem])
                        elif 'mongod' in line:
                            data = line.split()
                            name, cpu, mem = data[11], data[8], data[9]
                            mongod_rows.append([name, cpu, mem])
                        elif line.startswith('Cpu'):
                            data = line.split()
                            cpu_total_rows.append(['CPU_total', data[1].split('%')[0], data[2].split('%')[0],
                                                   data[4].split('%')[0], data[
                                5].split('%')[0],
                                data[7].split('%')[0]])
                        elif line.startswith('Mem'):
                            data = line.split()
                            mem_total_rows.append(['MEM_total', int(int(data[5][:-1]) / 1024),
                                                   int(int(
                                                       data[3][:-1]) / 1024), int(int(data[1][:-1]) / 1024),
                                                   int(int(data[7][:-1]) / 1024)])
                        else:
                            pass
                    except:
                        pass
                # print(min(len(nfm_rows),len(ac_rows),len(mongod_rows)))
            with open(data_path + 'monitor_data_top.csv', 'w', newline='') as f:
                csv_write = csv.writer(f, dialect='excel')
                min_len = min(len(ac_rows), len(nfm_rows), len(
                    mongod_rows), len(mem_total_rows), len(cpu_total_rows))
                for i in range(min_len):
                    L = ac_rows[i] + nfm_rows[i] + mongod_rows[i] + \
                        mem_total_rows[i] + cpu_total_rows[i] + node_rows[i]
                    csv_write.writerow(L)
            path = os.getcwd() + '/' + data_path
            print('数据处理完成，结果文件到目录%s\n' % path)


def stability():
    TEST_TIME = config['test_time']
    set_header()
    init_monitor_client()
    hubs = get_online_hubs()
    start_ac_monitor(TEST_TIME)
    threading.Timer(TEST_TIME, stop_test).start()
    threading.Thread(target=revive_data).start()
    start_scan(hubs)
    # threading.Thread(target = start_scan,args = (hubs,)).start()
    threading.Thread(target=scan_speed).start()
    print("Start stability test success!!!")


def performance():
    INTERVAL = config['interval']
    PER_COUNT = config['per_count']
    set_header()
    init_monitor_client()
    hubs = get_online_hubs()
    test_time = int(len(hubs) / PER_COUNT + 1) * INTERVAL
    start_ac_monitor(test_time)
    threading.Timer(test_time, stop_test).start()
    threading.Thread(target=revive_data).start()
    threading.Thread(target=scan_by_interval, args=(hubs,)).start()
    threading.Thread(target=scan_speed).start()
    print("Start performance test success!!!")


def start_test():
    global config
    TEST_MODE = config['test_mode']
    if TEST_MODE == '1':
        performance()
    elif TEST_MODE == '0':
        stability()
    else:
        print("ERROR TEST_MODE:%s,ONLY SUPPORT 'performance' and 'stability'" % TEST_MODE)


def stop_test():
    print("Stop test!!!")
    try:
        res.close()
    except Exception as e:
        print(e)
    try:
        sethead_timer.cancel()
    except Exception as e:
        print(e)
    try:
        speed_timer.cancel()
    except Exception as e:
        print(e)
    copy_file()
    print("Stop test success!!!")


def main():
    init_config()
    start_test()


if __name__ == '__main__':

    main()
