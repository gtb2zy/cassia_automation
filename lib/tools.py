import sys
import os
import json
path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
from logs import set_logger
from api import api


logger = set_logger(__name__)


def read_config():
    '''
    读取主配置文件，并返回文件内容
    :return: dict
    '''
    try:
        path = os.getcwd().split('cassia_automation')[
            0] + 'cassia_automation/config/config.json'
        with open(path, encoding='utf8') as conf:
            conf = json.load(conf)
            if isinstance(conf, dict):
                logger.debug('Read config success.')
            else:
                logger.error('config para error.')
                raise BaseException('config para error!')
    except Exception as e:
        logger.error('Config file read failed!')
        print('ERROR:Config file read failed!', e)
    return conf


def read_job_config():
    '''
    读取config目录下面的job_config文件，并返回value
    :return: dict
    '''

    try:
        path = os.getcwd().split('cassia_automation')[
            0] + 'cassia_automation/config/job_config.json'
        with open(path, encoding='utf8') as conf:
            conf = json.load(conf)
            if isinstance(conf, dict):
                logger.debug('Read config success.')
            else:
                logger.error('config para error.')
                raise BaseException('config para error!')
    except Exception as e:
        logger.error('Config file read failed!')
        print('ERROR:Config file read failed!', e)
    return conf


def read_stability_config():
    '''
    读取config目录下面的stability_config文件，并返回value
    :return: dict
    '''
    try:
        path = os.getcwd().split('cassia_automation')[
            0] + 'cassia_automation/config/environments.json'
        with open(path, encoding='utf8') as conf:
            conf = json.load(conf)
            if isinstance(conf, dict):
                logger.debug('Read config success.')
            else:
                logger.error('config para error.')
                raise BaseException('config para error!')
    except Exception as e:
        logger.error('Config file read failed!')
        print('ERROR:Config file read failed!', e)
    return conf['stability_env']


def read_common_config():
    '''
    读取config目录下面的common参数，并返回value
    :return: dict
    '''

    try:
        path = os.getcwd().split('cassia_automation')[
            0] + 'cassia_automation/config/config.json'
        with open(path, encoding='utf8') as conf:
            conf = json.load(conf)
            if isinstance(conf, dict):
                logger.debug('Read common config success.')
            else:
                logger.error('common config para error.')
                raise BaseException('common config para error!')
    except Exception as e:
        logger.error('Config common file read failed!')
        print('ERROR:Config common file read failed!', e)
    return conf['common_paramter']


def get_device_list(model, ap):
    # 获取系统测试的的device_list
    try:
        path = os.getcwd().split('cassia_automation')[
            0] + 'cassia_automation/config/devices.json'
        with open(path, encoding='utf8') as conf:
            conf = json.load(conf)[model]
            if isinstance(conf, dict):
                print("logger.debug('Read devices.json success.')")
            else:
                print("logger.error('devices.json para error.')")
                raise BaseException('devices.json para error!')
    except Exception as e:
        print("logger.error('devices.json read failed!')")
        print('ERROR:devices.json read failed!', e)
    dev_list = {}
    dev_fnlist = {}
    device_list = []
    for dev_type in conf:
        dev_list[dev_type] = conf[dev_type]
        device_list_tmp = conf[dev_type]['devices']
        for node1 in [x for x in device_list_tmp[ap].lstrip('[').rstrip(']').split(',')]:
            if node1:
                device_list.append(node1.strip("'"))
        dev_list[dev_type]['devices'] = device_list
        device_list = []
    env_list = read_stability_config()[model][ap]['device']
    for i in env_list.lstrip('[').rstrip(']').split(','):
        devtype = i.strip("'")
        dev_fnlist[devtype] = dev_list[devtype]
    return dev_fnlist


def get_stability_devices(key):
    try:
        path = os.getcwd().split('cassia_automation')[
            0] + 'cassia_automation/config/devices.json'
        with open(path, encoding='utf8') as conf:
            conf = json.load(conf)
            if isinstance(conf, dict):
                logger.debug('Read config success.')
            else:
                logger.error('config para error.')
                raise BaseException('config para error!')
    except Exception as e:
        logger.error('Config file read failed!')
        print('ERROR:Config file read failed!', e)
    return conf[key]


def get_api():
    '''
    根据配置文件中的job_config中的字段local，返回对应的API对象
    :return: local = true返回本地API对象，local=false返回云API对象
    '''
    conf = read_job_config()
    if isinstance(conf, dict):
        logger.debug('Read config success.')
    else:
        logger.error('config para error.')
        raise BaseException('config para error!')
    if conf['local'] == 'True':
        return api(conf['local_host'], local=True, model=conf['model'])
    else:
        return api(conf['host'], conf['hub'], conf['user'], conf['pwd'], False, conf['model'])


def get_all_api():
    '''
    直接同时返回本地和云端API
    :return:class obj
    '''
    conf = read_job_config()
    local_api = api(conf['local_host'], local=True)
    cloud_api = api(conf['host'], conf['hub'], conf['user'], conf['pwd'])
    return local_api, cloud_api


def get_model():
    '''
    返回config文件中的model字段值
    :return: str
    '''
    conf = read_job_config()
    if conf['model']:
        model = conf['model']
        return model
    else:
        logger.error('Hub model not set.')
        raise BaseException('Please set hub model in conf file!')


def get_filter():
    '''
    读取目录config下面的job_config配置文件中的fiter字段并返回
    :return: dict
    '''
    conf = read_job_config()
    return conf['filter']


def get_uuid(data):
    start = 0
    head_length = int(data[start:start + 2], 16)
    start = 2 + head_length * 2
    data_length = int(data[start:start + 2], 16)
    start = start + 2
    adv_data = data[start:start + data_length * 2]
    adv_tpye = int(adv_data[0:2], 16)
    if adv_tpye >= 2 and adv_tpye <= 7:
        start = start + 2
        uuid = adv_data[2:]
        # print(uuid)
        return str(uuid)
    else:
        return None


if __name__ == '__main__':

    sdk = get_api()
    for x in sdk.scan():
        print(x)
