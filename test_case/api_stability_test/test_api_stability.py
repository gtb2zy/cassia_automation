import sys,os
import threading
import random

path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
from api import api
from logs import set_logger
from tools import read_stability_config,get_stability_devices



class test_stability():

	time_out_flag = False
	case_end_flag = False
	loop_error = False
	debug = []

	def __init__(self,conf):
		self.conf = conf
		self.sdk = api(self.conf['host'], self.conf['hub'], self.conf['user'], self.conf['pwd'])
		debug_file = "stability_debug_" + "".join(self.conf['hub'].split(':')) + ".txt"
		error_file = "stability_error_" + "".join(self.conf['hub'].split(':')) + '.txt'
		self.logger = set_logger(__name__, debugfile=debug_file, errorfile=error_file)

	def init_run_env(self):
		self.time_out_flag = False
		self.case_end_flag = False

	def start_timer(self):
		#start timer to set timeout flag
		self.timer = threading.Timer(self.conf['case_timeout'],self.set_timeout)
		self.timer.start()

	def end_timer(self):
		#cancel the timer to set timeout flag
		self.timer.cancel()

	def set_timeout(self):
		self.time_out_flag = True

	def run_test(self,func):
		self.start_timer()
		self.init_run_env()
		t = threading.Thread(target = func)
		t.setDaemon(True)
		t.start()
		while True:
			if self.time_out_flag:
				self.loop_error = True
				err =  'AP %s 扫描开启失败\n' % (self.sdk.hub)
				self.debug.append(err)
				print(err)
				self.errorend()
				break
			if self.case_end_flag:
				print(self.case_end_flag)
				self.end_timer()
				pass
				break

	def loop(self,devices):
		self.loop = 1
		while not self.loop_error:
			start = 'AP %s 开始第%d次循环...\n' % (self.sdk.hub, self.loop)
			print(start)
			self.debug.append(start)
			'''
			此处添加测试方法；
			测试方法会按照添加顺序执行；
			一个方法失败，会导致整个循环报错停止。
			'''
			#测试方法
			self.run_test(self.test_scan)
			self.run_test(self.test_connect_device)
			# self.run_test(self.test_connect_device)
			end = 'AP %s 第%d次循环成功结束...\n' % (self.sdk.hub, self.loop)
			print(end)
			self.debug.append(end)
			for msg in self.debug:
				self.logger.info(msg)
			self.debug = []
			self.loop += 1

	def errorend(self):
		end = 'AP %s 第%d次循环异常结束...\n' % (self.sdk.hub, self.loop)
		print(end)
		for msg in self.debug:
			self.logger.error(msg)

	def test_scan(self):
		for data in self.sdk.scan(chip = 0):
			if str(data).startswith('data'):
				debug =  'AP %s chip 0 start scan success!'%self.sdk.hub
				self.debug.append(debug)
				break
		if self.conf['model'].upper().startswith('S'):
			print(self.conf['model'].upper())
			self.case_end_flag = True
			print('AP %s start scan success!'%self.sdk.hub)
		else:
			for data in self.sdk.scan(chip=1):
				if str(data).startswith('data'):
					debug = 'AP %s start scan success!' % self.sdk.hub
					self.debug.append(debug)
					print(debug)
					self.case_end_flag = True
					break

	def test_connect_device(self):
		j=0
		connect_flag=False
		for device in self.conf['device']:
			random1 = random.randint(1, 10)
			if random1 % 2 == 1:
				chip = 1
			else:
				chip = 0
			types=self.conf['device_type']
			timeout1=5000
			self.sdk.disconnect_device(device)
			for i in range(0,4):
				code, body, duration = self.sdk.connect_device(device, types, chip, timeout1)
				time.sleep(1)
				if code ==200:
					connect_flag=True
					break
			if connect_flag:
				for i1 in range(1, 4):
					code1, body1 = self.sdk.get_devices_list(state='connected')
					sleep(1)
					if code1 == 200:
						txt = json.load(body1)['nodes']
						for i1 in range(0, len(txt['nodes'])):
							if txt['nodes'][i]['bdaddrs']['bdaddr'] == device:
								if txt['nodes'][i]['chipId'] == chip:
									print('ap={0} device={1} connected success'.format(self.conf['hub'], device))
								else:
									debug = 'ap={0} device={1} connect failed'.format(self.conf['hub'], device)
									self.debug.append(debug)
							else:
								debug = 'ap={0} device={1} connect failed'.format(self.conf['hub'], device)
								self.debug.append(debug)
					break

		if j ==0:
			err='ap={0} device={1} all connected failed'.format(self.conf['hub'],device_list)
			self.debug.append(err)
			self.loop_error = True

def main():
	conf1 = read_stability_config()
    devices = get_stability_devices('')
	ap_list = ['S2000', 'X1000', 'E1000']
	for ap in ap_list:
		for conf in conf1[ap].values():
			test = test_stability(conf)
			threading.Thread(target=test.loop,args = (devices)).start()
if __name__ == '__main__':
	main()