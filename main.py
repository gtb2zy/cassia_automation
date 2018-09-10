from unittest import TestLoader, TestSuite
import time
import re
import os
import json
import base64
import threading
import paramiko
import requests
from collections import namedtuple
from lib import tools

path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/'
conf = tools.read_config()
logger = tools.set_logger(__name__)
EXIT = False
REDIRECTED = False
# 代码svn仓库路径为：https://168.168.10.200/svn/QA_versions/自动化测试平台


def myprint(*string):
    if REDIRECTED:
        with open('/tmp/performence/log.log', 'a', encoding='utf8') as f:
            for s in string:
                f.writelines(str(s) + '\n')
    else:
        print(*string)


# 性能测试入口
def performenceTest(name, testplan: dict):
    if testplan['ac_version'] == 1.2 or testplan['ac_version'] == 1.3:
        version = testplan['ac_version']
        myprint('AC 版本为%s,开始性能测试' % version)
    else:
        myprint('ac version error!')
        return
    for key in testplan.keys():
        overwrite_conf_file(key, testplan[key])
    host = namedtuple('host', ['ip', 'user', 'passwd'])
    s = eval(testplan['server'])
    server = host(s[0], s[1], s[2])
    wtps = [host(x[0], x[1], x[2]) for x in eval(testplan['wtps'])]
    clients = [host(x[0], x[1], x[2]) for x in eval(testplan['clients'])]

    # 按照配置文件，开启模拟AP
    per_wtp_count = int(testplan['start_ap_count'] / len(wtps))
    for wtp in wtps:
        index = wtps.index(wtp)
        start = index * per_wtp_count
        sftp_wtp, ssh_wtp = init_monitor_client(wtp)
        prepare_ap(ssh_wtp, sftp_wtp, testplan, start, per_wtp_count)
    while True:
        # 判断所有模拟AP是否全部上线
        online_ap_count = len(get_online_ap(testplan))
        if online_ap_count > int(testplan['start_ap_count']):
            myprint('所有模拟AP已全部上线！\n')
            break
        else:
            myprint('当前已有%d台模拟AP上线' % online_ap_count)
            time.sleep(1)

    # 在子线程中开启测试工具服务端，方便持续读取测试数据
    sftp_s, ssh_s = init_monitor_client(server)
    time.sleep(10)
    t = threading.Thread(target=prepare_server, args=(ssh_s, sftp_s, version))
    t.setDaemon(True)
    t.start()
    time.sleep(10)

    # 开启所有的测试工具客户端
    if version == 1.2:
        for client in clients:
            sftp_c, ssh_c = init_monitor_client(client)
            prepare_client(ssh_c, sftp_c, client)


# 获取当前上线的AP数量
def get_online_ap(testplan):
    host = testplan['HOST']
    headers = _set_header(testplan, host)
    res = requests.get(host + '/cassia/hubs', headers=headers)
    res_hub_info = json.loads(res.text)
    hubs = []
    for i in res_hub_info:
        if isinstance(i, dict):
            hubs.append(i['mac'])
    return hubs


# 设置请求头
def _set_header(testplan, host):
    use_info = testplan['user'] + ':' + testplan['pwd']
    # 编码开发者帐号
    encode_info = base64.b64encode(use_info.encode('utf-8'))
    head = {'Content-Type': 'application/json', 'Authorization': 'Basic ' + encode_info.decode("utf-8")}
    data = {'grant_type': 'client_credentials'}
    try:
        # 发起请求
        res = requests.post(host + '/oauth2/token', data=json.dumps(data), headers=head)
        # myprint(res.url)
        if res.status_code == 200:
            res_body = json.loads(res.text)
            TOKEN = res_body.get("access_token")
        elif res.status_code == 401:
            myprint('开发帐号错误')
        elif res.status_code == 400:
            myprint('API路径错误')
    except Exception as e:
        myprint(e)
    if TOKEN:
        # 拼接请求头
        headers = {'Content-Type': 'application/json', 'version': '1', 'Authorization': 'Bearer ' + TOKEN}
        return headers


def overwrite_conf_file(line_flag, replace):
    """
    替换原来文件中的某一行。
    line_flag:标志字符串，一般去该行‘=’之前的内容即可，用来查找将要替换的行
    replace：用来替换的字符串，会替换匹配行的‘=’之后的内容
    """
    with open(path + 'performence/test.conf', 'r', encoding='utf8') as f:
        file = ''
        for line in f.readlines():
            if line.startswith(line_flag):
                if line_flag == 'server':
                    line = line_flag + ' = ' + str(re.findall(r"[(]'(.*?)',", replace)[0]) + '\n'
                else:
                    line = line_flag + ' = ' + str(replace) + '\n'
            file += line
    with open(path + 'performence/test.conf', 'w', encoding='utf8') as f:
        f.writelines(file)


# 开启模拟AP
def prepare_ap(ssh_client, ftp_client, testplan, start, count):
    myprint('正在启动AP模拟工具...')
    try:
        # exec_cmd(ssh_client, 'mkdir -p /tmp/performence/ap/')
        ssh_client.exec_command('mkdir -p /tmp/performence/ap/')
    except BaseException:
        pass
    try:
        # exec_cmd(ssh_client, 'mkdir /etc/config')
        ssh_client.exec_command('mkdir -p /etc/config')
    except BaseException:
        pass
    ac = get_ac()
    msg = '<WTP_STATIC_AC_IPV4_ADDR>%s' % ac
    # 上传测试文件
    ssh_client.exec_command('killall WTP;killall python3')
    time.sleep(3)
    ftp_client.put(path + "performence/ap/dev-test", '/tmp/performence/ap/dev-test')
    ftp_client.put(path + "performence/ap/run.sh", '/tmp/performence/ap/run.sh')
    ftp_client.put(path + "performence/ap/scan_data.lua", '/tmp/performence/ap/scan_data.lua')
    ftp_client.put(path + "performence/ap/WTP", '/tmp/performence/ap/WTP')
    ftp_client.close()
    ssh_client.exec_command("echo '%s' >/etc/config/wtp.cfg" % msg)
    ssh_client.exec_command('chmod -R 777 /tmp/performence/ap/')
    ssh_client.exec_command('cd /tmp/performence/ap/;./run.sh %d %d >/dev/null &' % (start, start + count))
    while True:
        _, out, _ = ssh_client.exec_command('ps aux|grep WTP|wc -l')
        running = out.read().strip()
        if running is not None:
            running = int(str(running, encoding='utf8'))
            if running >= count:
                break
            else:
                myprint('当前已开启模拟AP数量为%d' % running)
                time.sleep(1)
    cmd = 'cd /tmp/performence/ap/;./dev-test %d %d speed 1' % (count, start * 2 - 1)
    exec_cmd(ssh_client, cmd)
    ssh_client.close()
    myprint("AP模拟工具开启成功！\n")


def get_ac():
    with open(path + 'performence/test.conf', encoding='utf8') as f:
        for line in f.readlines():
            if 'HOST' in line:
                ac = re.findall(r'//(.+?)/', line)[0]
                return ac


# 初始化压力测试工具服务器端运行环境，并开启服务
def prepare_server(ssh_client, ftp_client, version):
    global EXIT
    myprint('初始化压力测试工具服务器端运行环境...')
    try:
        ssh_client.exec_command('mkdir -p /tmp/performence/')
    except BaseException:
        pass
    # 上传测试文件,开启测试服务端
    ftp_client.put(path + "performence/nmon_x86_centos6", '/tmp/performence/nmon_x86_centos6')
    ftp_client.put(path + "performence/test.conf", '/tmp/performence/test.conf')
    if version == 1.2:
        ftp_client.put(path + "performence/server8.py", '/tmp/performence/server8.py')
        ssh_client.exec_command('cd /tmp/performence/;python3 server8.py > log.log &')
    else:
        ftp_client.put(path + "performence/test.py", '/tmp/performence/test.py')
        ssh_client.exec_command('cd /tmp/performence/;python3 test.py')
    ftp_client.close()
    myprint('服务端环境初始化成功，服务端成功启动！\n')

    # 持续读取server的返回消息
    before = []
    while not EXIT:
        _, stdout, _ = ssh_client.exec_command('cd /tmp/performence/;tail -n 20 log.log')
        lines = stdout.readlines()
        for line in lines:
            if line not in before:
                myprint(line)
                if '测试完成' in line:
                    EXIT = True
        before = lines
        time.sleep(1)


# 初始化压力测试工具客户端，并运行
def prepare_client(ssh_client, ftp_client, client):
    global EXIT
    myprint('初始化压力测试工具客户端(主机：%s)运行环境...' % client[0])
    try:
        ssh_client.exec_command('mkdir -p /tmp/performence/')
    except BaseException:
        pass
    # 上传测试文件
    ftp_client.put(path + "performence/client8.py", '/tmp/performence/client8.py')
    ftp_client.put(path + "performence/test.conf", '/tmp/performence/test.conf')
    # 开启测试客户端
    ssh_client.exec_command('cd /tmp/performence/;python3 client8.py > /dev/null &')
    ssh_client.close()
    ftp_client.close()
    myprint('压力测试工具客户端(主机：%s)运行环境初始化成功，客户端成功启动！\n' % client[0])


def exec_cmd(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    try:
        myprint(str(stdin.read(), encoding='utf8'))
    except BaseException:
        pass
    try:
        myprint(str(stdout.read(), encoding='utf8'))
    except BaseException:
        pass
    try:
        myprint(str(stderr.read(), encoding='utf8'))
    except BaseException:
        pass


# 建立到目标主机的ssh和sftp连接
def init_monitor_client(host):
    # 初始化性能监控工具
    try:
        # 初始化sftp客户端
        myprint('sftp正在连接主机%s ...' % host.ip)
        ftp = paramiko.Transport((host.ip, 22))
        ftp.connect(username=host.user, password=host.passwd)
        sftp_client = paramiko.SFTPClient.from_transport(ftp)
        myprint('sftp成功连接到主机%s!' % host.ip)
    except Exception as e:
        myprint('sftp连接主机%s失败！' % host.ip)
        myprint(e)
    try:
        # 初始化ssh客户端
        myprint('ssh正在连接主机%s ...' % host.ip)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host.ip, 22, host.user, host.passwd, timeout=5)
        myprint('ssh成功连接主机%s!' % host.ip)
    except Exception as e:
        myprint('ssh连接主机%s失败！' % host.ip)
        myprint(e)
    return sftp_client, ssh_client


# 功能测试入口
def functionTest(name, testplan: dict):
    if not isinstance(testplan, dict):
        logger.debug('测试计划配置错误，测试异常终止，请检查conig文件!')
        myprint('测试计划配置错误，测试异常终止，请检查conig文件!')
        return
    reports_dir = path + 'reports/'
    test_plan_comment = testplan['comment']
    jobs = eval(testplan['jobs'])
    loader = TestLoader()
    cases = []
    for job_name, job_conf in jobs.items():
        # 遍历测试计划下面得所有测试任务
        with open('config/job_config.json', 'w', encoding='utf8') as f:
            # 写临时的job_conf文件，
            tmp = {}
            tmp['case_timeout'] = testplan['case_timeout']
            tmp['filter_count'] = testplan['filter_count']
            tmp['unfilter_count'] = testplan['unfilter_count']
            tmp['case_path'] = job_conf['case_path']
            tmp['case'] = job_conf['case']
            with open('config/environments.json') as envs:
                envs = json.load(envs)
                env = envs[job_conf['env']]
                tmp = dict(tmp, **env)
            f.write(str(tmp).replace('\'', '\"'))

        if job_conf['case']:
            # add test cases in test job.
            if job_conf['case_path']:
                # 如果不指定case路径，默认添加所有case执行
                case_path = path + 'test_case/' + job_conf['case_path']
            else:
                case_path = path + 'test_case/'
            for case in job_conf['case']:
                # 搜索指定目录下的所有符合匹配规则的case
                myprint(case_path, case)
                cases.append(loader.discover(case_path, pattern=case))
        else:
            pass
    # 将所有测试case全部加载到suite
    suite = TestSuite(cases)

    # 执行测试计划
    now = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = reports_dir + 'report_' + now + '.html'
    with open(filename, 'wb') as f:
        html_test_runner = tools.HTMLTestRunner.HTMLTestRunner(stream=f,
                                                               verbosity=2,
                                                               title=name,
                                                               description=test_plan_comment
                                                               )
        html_test_runner.run(suite)
        # 通过邮件发送测试报告
        # send_report(test_plan_comments[i]).send()


def main():
    test_plans = conf['test_plans']
    for name, plan in test_plans.items():
        # 检查测试计划的测试类型，判断是功能测试还是性能测试
        if plan['test_type'] == 0:
            threading.Thread(target=functionTest, args=(name, plan,)).start()
        elif plan['test_type'] == 1:
            threading.Thread(target=performenceTest, args=(name, plan,)).start()
        else:
            myprint('Test paln type is error! Please check config file!')
    try:
        while not EXIT:
            # 监听程序退出
            time.sleep(1)
    except KeyboardInterrupt:
        myprint('检测到CTRL-C，测试终止....')


if __name__ == '__main__':
    main()
