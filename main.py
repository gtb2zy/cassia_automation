from unittest import TestLoader, TestSuite
import time
import os
import json
import threading
import paramiko
from collections import namedtuple
from lib import tools

path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/'
conf = tools.read_config()
logger = tools.set_logger(__name__)
# 代码svn仓库路径为：https://168.168.10.200/svn/QA_versions/自动化测试平台


def performenceTest(name, testplan: dict):
    host = namedtuple('host', ['ip', 'user', 'passwd'])
    s = eval(testplan['client'])
    server = host(s[0], s[1], s[2])
    clients = [host(x[0], x[1], x[2]) for x in eval(testplan['client'])]
    sftp_s, ssh_s = init_monitor_client(server)
    prepare_server(ssh_s, sftp_s)
    for client in clients:
        sftp_c, ssh_c = init_monitor_client(client)
        prepare_client(ssh_c, sftp_c)
    


def prepare_server(ssh_client, ftp_client):
    try:
        ssh_client.exec_command('mkdir /tmp/performence/')
    except BaseException:
        pass
    ftp_client.put(path + "performence/nmon_x86_centos6", '/tmp/performence/nmon_x86_centos6')
    ftp_client.put(path + "performence/test.conf", '/tmp/performence/test.conf')
    ssh_client.exec_command('chmod 777 /tmp/performence/nmon_x86_centos6')
    ftp_client.put(path + "performence/server8.py", '/tmp/performence/server8.py')


def prepare_client(ssh_client, ftp_client):
    try:
        ssh_client.exec_command('mkdir /tmp/performence/')
    except BaseException:
        pass
    ftp_client.put(path + "performence/client8.py", '/tmp/performence/client8.py')
    ftp_client.put(path + "performence/test.conf", '/tmp/performence/test.conf')


def init_monitor_client(host):  # 初始化性能监控工具
    try:
        # 初始化sftp客户端
        # noinspection PyTypeChecker
        ftp = paramiko.Transport((host.ip, 22))
        ftp.connect(username=host.user, password=host.passwd)
        sftp_client = paramiko.SFTPClient.from_transport(ftp)
        # 初始化ssh客户端
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host.ip, 22, host.user, host.passwd, timeout=5)
        print('Monitor client init successed!\n')
    except Exception as e:
        print('Monitor client init failed!\n')
        print(e)
    return sftp_client, ssh_client
    try:
        sftp_client.put('nmon_x86_centos6', '/tmp/nmon_x86_centos6')
    except Exception as e:
        print(e)
        print('自动上传nmon工具失败，请手动上传！')
    try:
        ssh_client.exec_command('killall top')
        ssh_client.exec_command('killall pidstat')
        ssh_client.exec_command('killall nmon_x86_centos6')
        ssh_client.exec_command('chmod 777 /tmp/nmon_x86_centos6')
    except BaseException:
        pass


def functionTest(name, testplan: dict):
    if not isinstance(testplan, dict):
        logger.debug('测试计划配置错误，测试异常终止，请检查conig文件!')
        print('测试计划配置错误，测试异常终止，请检查conig文件!')
        return
    reports_dir = path + 'reports/'
    test_plan_comment = testplan['comment']
    loader = TestLoader()
    cases = []
    for job_name, job_conf in testplan['jobs'].items():
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
                print(case_path, case)
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
            print('Test paln type is wrong! Please check config file!')
    pass


if __name__ == '__main__':
    main()
