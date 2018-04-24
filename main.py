from unittest import TestLoader, TestSuite
import HTMLTestRunner
import time, os, json
from lib.logs import set_logger
from lib.sendReport import send_report


# 代码svn仓库路径为：https://168.168.10.200/svn/QA_versions/自动化测试平台
def main():
    path = os.getcwd().split('APItest')[0] + 'APItest/'
    logger = set_logger('main')
    reports_dir = path + 'reports/'
    test_plan_names = []
    test_plan_comments = []

    with open('config/config.json', encoding='utf8') as conf:
        try:
            conf = json.load(conf)
        except Exception as e:
            logger.error('配置文件格式错误')
            print('配置文件格式错误，请检查:', str(e).split(':')[1])
        suites = []
        plans = conf['test_plans']

        for plan_name, plan_conf in plans.items():
            loader = TestLoader()
            cases = []
            test_plan_names.append(plan_name)
            test_plan_comments.append(plan_conf['comment'])

            for job_name, job_conf in plan_conf['jobs'].items():
                with open('config/job_config.json', 'w', encoding='utf8') as f:
                    # 写临时的job_conf文件，该文件会被job下面对应的case实例化是读取
                    f.write(str(job_conf).replace('\'', '\"'))

                if job_conf['case']:
                    if job_conf['case_path']:
                        case_path = 'test_case/' + job_conf['case_path']
                    else:
                        case_path = 'test_case/'
                    for case in job_conf['case']:
                        # 搜索指定目录下的所有符合匹配规则的case
                        cases.append(loader.discover(case_path, pattern=case))
                else:
                    pass
            # 将所有测试计划全部加载到suites列表
            suites.append(TestSuite(cases))


    for i, suite in enumerate(suites):
        # 按顺序执行所有的test_plan，每个suite都是一个plan
        # threading.Thread(target = run_suite,args = (i,suite)).start()
        if suite:
            now = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = reports_dir + '/report_' + now + '.html'
            with open(filename, 'wb') as f:
                html_test_runner = HTMLTestRunner.HTMLTestRunner(stream=f,
																verbosity=2,
																title=test_plan_names[i],
																description=test_plan_comments[i]
                                                               )
                html_test_runner.run(suite)
                send_report(test_plan_comments[i]).send()

if __name__ == '__main__':
    main()
