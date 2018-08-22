import sys,os
import threading
import random
import time
import json
from contextlib import closing

path = os.getcwd().split('cassia_automation')[0] + 'cassia_automation/lib/'
sys.path.append(path)
from api import
from download_logs import Download_logs
# from logs import set_logger
import logs
from tools import read_stability_config,get_device_list
loop_error = False
class test_stability():
	debug=[]
	err=[]
	def __init__(self,conf):
		self.case_end_flag = False
		self.time_out_flag = False
		self.conf = conf
		self.sdk = api(self.conf['host'], self.conf['hub'], self.conf['user'], self.conf['pwd'])
		filename = "stability_debug.log"
		# error_file = "stability_error_" + "".join(self.conf['hub'].split(':')) + '.txt'
		self.logger = logs.set_logger(__name__,filename=filename)
		self.downlogs=Download_logs(self.conf['local_host'],22,'root','3_5*rShsen')
	def update_token(self):
		global headers
		headers = self.sdk.set_header()
		self.sdk.headers = headers
		timert = threading.Timer(350, self.update_token)
		timert.start()
		print("TOKEN更新")
	# def init_run_env(self):
	# 	# self.time_out_flag = False
	# 	self.case_end_flag = False

	def start_timer(self):
		# start timer to set timeout flag
		# scan也有自己的超时机制20s，此时的超时机制应该大于scan接口本身的超时机制
		self.timer = threading.Timer(21, self.set_timeout)
		self.timer.start()
	def end_timer(self):
		# cancel the timer to set timeout flag
		self.timer.cancel()
	def set_timeout(self):
		global loop_error
		loop_error=True
	def loop(self,device_conf):
		print("开始时间：", time.time())
		self.loop = 1
		global loop_error
		timert = threading.Timer(600, self.update_token)
		timert.start()
		while not loop_error:
			start = 'AP %s 开始第%d次循环...\n' % (self.sdk.hub, self.loop)
			print(start)
			self.test_scan()
			self.test_connect_device(device_conf)
			self.test_connected_devlist()
			self.test_discover_service(device_conf)
			self.test_discover_characteristics(device_conf)
			self.test_discover_the_characteristics(device_conf)
			self.test_discover_descriptors(device_conf)
			self.test_discover_all(device_conf)
			self.test_read_by_handle(device_conf)
			self.test_write_by_handle(device_conf)
			self.test_recive_indication_and_notification(device_conf)
			self.test_disconnect_device(device_conf)
			self.test_stop_advertise()
			time.sleep(1)
			end = 'AP %s 第%d次循环成功结束...\n' % (self.sdk.hub, self.loop)
			print(end)
			self.debug.append(end)
			for msg in self.debug:
				self.logger.debug(msg)
			self.debug = []
			self.loop += 1
		print("循环异常结束")

		conn_flag=self.downlogs.connect()
		if conn_flag:
			desDirectory=self.conf['model'] + '_' + self.conf['hub'].split(':')+'_log/'
			self.downlogs.get_logs(desDirectory)
		else:
			err='获取异常AP的log失败，ssh连接失败'
			self.err.append(err)
		self.errend()
		timert.cancel()
	def errend(self):
		end = 'AP %s 第%d次循环异常结束...\n' % (self.sdk.hub, self.loop)
		print(end)
		for msg in self.err:
			self.logger.error(msg)
		exit(1)
	def test_scan(self):
		global loop_error
		with closing(self.sdk.scan(chip=0)) as self.sse:
			i = 0
			self.start_timer()
			for da in self.sse.iter_lines():
				data = da.decode()
				if data.startswith("data"):
					i = i + 1
					if i >= 200:
						debug = 'AP %s chip 0 start scan success!' % self.sdk.hub
						self.debug.append(debug)
						print("AP={0} chip 0 start scan success!".format(self.sdk.hub))
						self.end_timer()
						self.sse.close()
						break
					else:
						pass
				else:
					if loop_error:
						if i >0:
							loop_error=False
							self.end_timer()
							break
						else:
							err = 'AP %s chip 0 start scan failed! MSG:%s' % (self.sdk.hub, data)
							self.err.append(err)
							print(err)
							self.end_timer()
							break
		if self.conf['model'].upper().startswith('S'):
			self.case_end_flag = True
		else:
			with closing(self.sdk.scan(chip=1)) as self.sse:
				j = 0
				self.start_timer()
				for da in self.sse.iter_lines():
					data = da.decode()
					if data.startswith("data"):
						j = j + 1
						if j >= 200:
							debug = 'AP %s chip 1 start scan success!' % self.sdk.hub
							self.debug.append(debug)
							print("AP={0} chip 1 start scan success!".format(self.sdk.hub))
							self.end_timer()
							self.sse.close()
							break
						else:
							pass
					else:
						if loop_error:
							if i > 0:
								loop_error = False
								self.end_timer()
								break
							else:
								err = 'AP %s chip 1 start scan failed! MSG:%s' % (self.sdk.hub, data)
								self.err.append(err)
								print(err)
								self.end_timer()
								break
	def scan_to_connect(self,chip, dev):
		with closing(self.sdk.scan(chip=chip)) as self.sse:
			i = 0
			scan_flag = False
			for da in self.sse.iter_lines():
				data = da.decode()
				if data.startswith("data"):
					msg = json.loads(data[5:])
					i = i + 1
					if msg['bdaddrs'][0]['bdaddr'] == dev:
						scan_flag = True
						return scan_flag
					elif i >= 200:
						return scan_flag
	def test_connect_device(self, device_conf):
		j = 0
		global loop_error
		connect_flag = False
		for devtype in device_conf:
			types = device_conf[devtype]['device_type']
			timeout1 = 5000
			device_list = []
			connect_device=[]
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
				scan_flag=self.scan_to_connect(chip,device)
				if scan_flag:
					for i in range(0, 5):
						code, body, duration = self.sdk.connect_device(device, types, chip, timeout1)
						if code == 200:
							connect_flag = True
							j += 1
							break
					if connect_flag:
						for i1 in range(1, 4):
							code1, body1 = self.sdk.get_devices_list(state='connected')
							if code1 == 200:
								txt = json.loads(body1)
								print("txt==", txt)
								for i in range(0, len(txt['nodes'])):
									if txt['nodes'][i]['bdaddrs']['bdaddr'] == device:
										if txt['nodes'][i]['chipId'] == chip:
											print(
												'ap={0} device={1} connected success'.format(self.conf['hub'], device))
											connect_device.append(device)
											break
										else:
											err = 'ap={0} device={1} connect error'.format(self.conf['hub'], device)
											self.err.append(err)
											loop_error = True
											break
							break
		if j == 0:
			err = 'ap={0} device={1} all connected failed'.format(self.conf['hub'], device_list)
			self.err.append(err)
			loop_error = True
		else:
			debug='ap={0} device={1} all connected success'.format(self.conf['hub'], connect_device)
			self.debug.append(debug)
			self.case_end_flag = True
	def test_disconnect_device(self,device_conf):
		self.conn_flag = False
		global loop_error
		devices = []
		j = 0
		while not self.conn_flag:
			code, body = self.sdk.get_devices_list('connected')
			msg = json.loads(body)['nodes']
			if code == 200:
				if len(msg) == 0:
					self.test_connect_device(device_conf)
				else:
					for i in range(len(msg)):
						devices.append(msg[i]['bdaddrs']['bdaddr'])
						self.conn_flag = True
			else:
				loop_error = True
				err = 'ap={0} get device disconnect before get devlist failed,return code={1},msg={2}'.format(self.conf['hub'],																					   code, text)
				self.err.append(err)
				# self.end_timer()
				break
		for dev in devices:
			code, text = self.sdk.disconnect_device(dev)
			if code ==200:
				j = j +1
		if j ==0:
			loop_error = True
			err = 'ap={0} get disconnect failed,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.err.append(err)
			print(err)
		else:
			code, body = self.sdk.get_devices_list('connected')
			if code==200:
				if len(json.loads(body)['nodes'])==0:
					self.case_end_flag=True
					debug = 'ap={0} get disconnect success,return code={1},msg={2}'.format(self.conf['hub'], code, text)
					self.debug.append(debug)
				else:
					loop_error = True
					err = 'ap={0} get disconnect failed,return code={1},msg={2}'.format(self.conf['hub'], code, text)
					self.err.append(err)
					# print(debug)
			else:
				loop_error = True
				err='ap={0}test disconnect api call connected device list error,code={1},msg={2}'.format(self.conf['hub'],code,body)
				self.err.append(err)
				# print(debug)
	def test_connected_devlist(self):
		code, body1 = self.sdk.get_devices_list('connected')
		global loop_error
		if code == 200:
			print("body==", body1)
			txt = json.loads(body1)['nodes']
			for i1 in range(0, len(txt)):
				if txt[i1]["connectionState"] == "connected":
					debug='AP {0} get connected device:{1} success'.format(self.conf['hub'],txt[i1]['bdaddrs']['bdaddr'])
					print(debug)
					self.debug.append(debug)
					self.case_end_flag=True
					break
				else:
					loop_error = True
					err = 'ap={0} get connected device list,return code={1}'.format(self.conf['hub'], code)
					self.err.append(err)
					break
		else:
			loop_error = True
			err = 'ap={0} get connected device list,return code={1}'.format(self.conf['hub'], code)
			self.err.append(err)
	def test_discover_service(self, device_conf):
		self.conn_flag = False
		global loop_error
		devices = []
		j = 0
		sevice_uuid2=''
		while not self.conn_flag:
			code, body = self.sdk.get_devices_list('connected')
			msg = json.loads(body)['nodes']
			print("ap测试={0} code测试={1}".format(self.conf['hub'], code))
			if code == 200:
				if len(msg) == 0:
					self.test_connect_device(device_conf)
				else:
					for i in range(len(msg)):
						devices.append(msg[i]['bdaddrs']['bdaddr'])
						self.conn_flag = True
			else:
				loop_error = True
				err = 'ap={0} get services before get devlist failed,return code={1},msg={2}'.format(self.conf['hub'],
																									   code, text)
				self.err.append(err)
				# self.end_timer()
				break
		for dev in devices:
			for value in device_conf.values():
				if dev in value['devices']:
					sevice_uuid2 = value['service_uuid']
					break
			code, text = self.sdk.discovery_services(device=dev, uuid=sevice_uuid2)
			if code ==200:
				j = j +1
				print("功能service：", text)
				break
		print("j==",j)
		if j ==0:
			loop_error = True
			err = 'ap={0} get services failed,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.err.append(err)
		else:
			self.case_end_flag = True
			debug = 'ap={0} get services success,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.debug.append(debug)
	def test_discover_characteristics(self, device_conf):
		self.conn_flag = False
		global loop_error
		devices=[]
		j=0
		sevice_uuid1=''
		while not self.conn_flag:
			code, body = self.sdk.get_devices_list('connected')
			msg = json.loads(body)['nodes']
			print("ap测试特性={0} code测试特性={1}".format(self.conf['hub'], code))
			if code == 200:
				if len(msg) == 0:
					self.test_connect_device(device_conf)
					print("flag特性===", self.conn_flag)
				else:
					for i in range(len(msg)):
						devices.append(msg[i]['bdaddrs']['bdaddr'])
						self.conn_flag = True
			else:
				loop_error = True
				err = 'ap={0} get characteristic before get devlist failed,return code={1},msg={2}'.format(
					self.conf['hub'], code, text)
				self.err.append(err)
				break
		for dev in devices:
			for value in device_conf.values():
				if dev in value['devices']:
					sevice_uuid1 = value['service_uuid']
					break
			code, text = self.sdk.discovery_characteristics(dev, sevice_uuid1)
			if code ==200:
				j = j +1
				print("功能characteristic：", text)
				break
		print("j==",j)
		if j ==0:
			loop_error = True
			err = 'ap={0} get characteristic failed,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.err.append(err)
		else:
			self.case_end_flag = True
			debug = 'ap={0} get characteristic success,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.debug.append(debug)
	def test_discover_the_characteristics(self,device_conf):
		self.conn_flag = False
		global loop_error
		devices=[]
		j=0
		charac_uuid=''
		while not self.conn_flag:
			code, body = self.sdk.get_devices_list('connected')
			msg = json.loads(body)['nodes']
			print("ap测试the特性={0} code测试the特性={1}".format(self.conf['hub'], code))
			if code == 200:
				if len(msg) == 0:
					self.test_connect_device(device_conf)
					print("flag特性===", self.conn_flag)
				else:
					for i in range(len(msg)):
						devices.append(msg[i]['bdaddrs']['bdaddr'])
						self.conn_flag = True
			else:
				loop_error = True
				err = 'ap={0} get the characteristic before get devlist failed,return code={1},msg={2}'.format(
					self.conf['hub'], code, text)
				self.err.append(err)
				break
		for dev in devices:
			for value in device_conf.values():
				if dev in value['devices']:
					charac_uuid = value['charac_uuid']
					break
			code, text = self.sdk.discovery_characteristic(dev, charac_uuid)
			if code ==200:
				j = j +1
				print("功能the characteristic：", text)
				break
		print("j==",j)
		if j ==0:
			loop_error = True
			err = 'ap={0} get the characteristic failed,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.err.append(err)
		else:
			self.case_end_flag = True
			debug = 'ap={0} get the characteristic success,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.debug.append(debug)
	def test_discover_all(self, device_conf):
		self.conn_flag = False
		global loop_error
		devices = []
		j = 0
		while not self.conn_flag:
			code, body = self.sdk.get_devices_list('connected')
			msg = json.loads(body)['nodes']
			print("ap测试all={0} code测试all={1}".format(self.conf['hub'], code))
			if code == 200:
				if len(msg) == 0:
					self.test_connect_device(device_conf)
				else:
					for i in range(len(msg)):
						devices.append(msg[i]['bdaddrs']['bdaddr'])
						self.conn_flag = True
			else:
				loop_error = True
				err = 'ap={0} get the all before get devlist failed,return code={1},msg={2}'.format(
					self.conf['hub'], code, text)
				self.err.append(err)
				break
		for dev in devices:
			code, text = self.sdk.discover_all(dev)
			if code ==200:
				j = j +1
				print("功能all：", text)
				break
		print("j==",j)
		if j ==0:
			loop_error = True
			err = 'ap={0} get the all failed,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.err.append(err)
		else:
			self.case_end_flag = True
			debug = 'ap={0} get the all success,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.debug.append(debug)
	def test_discover_descriptors(self, device_conf):
		self.conn_flag = False
		global loop_error
		devices = []
		j = 0
		charac_uuid=''
		while not self.conn_flag:
			code, body = self.sdk.get_devices_list('connected')
			msg = json.loads(body)['nodes']
			print("ap测试descriptors={0} code测试descriptors={1}".format(self.conf['hub'], code))
			if code == 200:
				if len(msg) == 0:
					self.test_connect_device(device_conf)
					print("flag descriptors===", self.conn_flag)
				else:
					for i in range(len(msg)):
						devices.append(msg[i]['bdaddrs']['bdaddr'])
						self.conn_flag = True
			else:
				loop_error = True
				err = 'ap={0} get the descriptors before get devlist failed,return code={1},msg={2}'.format(
					self.conf['hub'], code, text)
				self.err.append(err)
				break
		for dev in devices:
			for value in device_conf.values():
				if dev in value['devices']:
					charac_uuid = value['charac_uuid']
					break
			code, text = self.sdk.discover_descriptors(dev, charac_uuid)
			if code ==200:
				j = j +1
				print("功能descriptors", text)
				break
		print("j==",j)
		if j ==0:
			loop_error = True
			err = 'ap={0} get the descriptors failed,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.err.append(err)
		else:
			self.case_end_flag = True
			debug = 'ap={0} get the descriptors success,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.debug.append(debug)
	def test_read_by_handle(self,device_conf):
		self.conn_flag = False
		global loop_error
		devices=[]
		j=0
		handle='1'
		while not self.conn_flag:
			code, body = self.sdk.get_devices_list('connected')
			msg = json.loads(body)['nodes']
			print("ap测试read by handle={0} code={1}".format(self.conf['hub'], code))
			if code == 200:
				if len(msg) == 0:
					self.test_connect_device(device_conf)
					print("flag readby handle===", self.conn_flag)
				else:
					for i in range(len(msg)):
						devices.append(msg[i]['bdaddrs']['bdaddr'])
						self.conn_flag = True
			else:
				loop_error = True
				err = 'ap={0} get the read by handle before get devlist failed,return code={1},msg={2}'.format(
					self.conf['hub'], code, text)
				self.err.append(err)
				break
		for dev in devices:
			for value in device_conf.values():
				if dev in value['devices']:
					handle = value['handle']
					break
			code, text = self.sdk.read_by_handle(dev, handle)
			if code ==200:
				j = j +1
				print("功能：", text)
				break
		print("j==",j)
		if j ==0:
			loop_error = True
			err = 'ap={0} get the read handle failed,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.err.append(err)
		else:
			self.case_end_flag = True
			debug = 'ap={0} get the read handle success,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.debug.append(debug)
	def test_write_by_handle(self,device_conf):
		self.conn_flag = False
		global loop_error
		devices=[]
		j=0
		handle='17'
		handle_value='0100'
		while not self.conn_flag:
			code, body = self.sdk.get_devices_list('connected')
			msg = json.loads(body)['nodes']
			print("ap测试read by handle={0} code={1}".format(self.conf['hub'], code))
			if code == 200:
				if len(msg) == 0:
					self.test_connect_device(device_conf)
					print("flag writeby handle===", self.conn_flag)
				else:
					for i in range(len(msg)):
						devices.append(msg[i]['bdaddrs']['bdaddr'])
						self.conn_flag = True
			else:
				loop_error = True
				err = 'ap={0} write by handle before get devlist failed,return code={1},msg={2}'.format(
					self.conf['hub'], code, text)
				self.err.append(err)
				break
		for dev in devices:
			for value in device_conf.values():
				if dev in value['devices']:
					handle = value['handle']
					handle_value = value['handle_value']
					break
			code, text = self.sdk.write_by_handle(dev, handle,handle_value)
			if code ==200:
				j = j +1
				code,text=self.sdk.read_by_handle(dev,handle)
				if code ==200:
					if json.loads(text)["value"] ==handle_value:
						debug='AP={0} device={1}  write by handle success code={2},msg={3}'.format(self.conf['hub'],dev, code, text)
						self.debug.append(debug)
						break
					else:
						err = 'AP={0} device={1}  write by handle values failed code={2},msg={3}'.format(self.conf['hub'],
																									 dev, code, text)
						self.err.append(err)
						loop_error=True
						break
			else:
				debug = 'AP={0} device={1}  write by handle  failed code={2},msg={3}'.format(self.conf['hub'],
																								   dev, code, text)
				self.debug.append(debug)
		if j ==0:
			loop_error = True
			err = 'ap={0}  write handle failed,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.err.append(err)
		else:
			self.case_end_flag = True
			debug = 'ap={0}  write handle success,return code={1},msg={2}'.format(self.conf['hub'], code, text)
			self.debug.append(debug)
	def test_recive_indication_and_notification(self,device_conf):
		self.conn_flag = False
		global loop_error
		devices = []
		j = 0
		self.success_flag=False
		while not self.conn_flag:
			code, body = self.sdk.get_devices_list('connected')
			msg = json.loads(body)['nodes']
			print("ap测试recive indication&notification 获取连接设备={0} code={1}".format(self.conf['hub'], code))
			if code == 200:
				if len(msg) == 0:
					self.test_connect_device(device_conf)
				else:
					for i in range(len(msg)):
						devices.append(msg[i]['bdaddrs']['bdaddr'])
					self.conn_flag = True
			else:
				loop_error = True
				err = 'ap={0} recive indication&notification before get devlist failed,return code={1},msg={2}'.format(
					self.conf['hub'], code, text)
				self.err.append(err)
				break
		print("devices==", devices)
		for dev in devices:
			print("value==",device_conf)
			print("dev===",dev)
			for key,values in device_conf.items():
				if dev in values['devices']:
					device_model = values['device_model']
					break
			res = self.sdk.recive_notification()
			print("recive_notification rescode==",res.status_code)
			if res.status_code == 200:
				for line in res.iter_lines():
					message = str(line, encoding='utf-8')
					if message.strip() == ':keep-alive':
						self.success_flag=True
						print('self.success_flag===',self.success_flag)
						break
					else:
						loop_error=True
						err = 'AP={0} recive_indication_and_notification success code={1},msg={2}'.format(self.conf['hub'],
																											res.status_code, message)
						self.err.append(err)
						break
				print("device_model==",device_model)
				if self.success_flag:
					# 埃微反向通知：你好
					if device_model == 'Iw':
						code, text = self.sdk.write_by_handle(dev, 39, '21ff310802ffE4BDA0E5A5BD')
						if code==200:
							debug='AP={0}  device={1} 反向通知你好 success code={2},msg={3}'.format(self.conf['hub'],dev,code,text)
							self.debug.append(debug)
							j=j+1
						else:
							debug = 'AP={0}  device={1} 反向通知你好 failed code={2},msg={3}'.format(self.conf['hub'], dev,
																								code, text)
							self.debug.append(debug)
							# 酷思手环反向通知：你好
					elif device_model == 'Hw':
						dict_handle = [{'handle': 17, 'handle_value': '0100'},
										{'handle': 19, 'handle_value': 'ff2006000227'},
										{'handle': 19, 'handle_value': 'ff000d00040110010102FF0125'},
										{'handle': 19, 'handle_value': 'FF80140006021002010a01030101E4BDA0E5A589'},
										{'handle': 19, 'handle_value': 'FFc105BD82'}]
						for i in range(len(dict_handle)):
							handle = dict_handle[i]['handle']
							handle_value = dict_handle[i]['handle_value']
							code, text = self.sdk.write_by_handle(dev, handle, handle_value)
							if code == 200:
								debug = 'AP={0}  device={1} 反向通知你好 success,write handle={4},value={5}, code={2},msg={3}'.format(
									self.conf['hub'], dev,
									code, text, handle,
									handle_value)
								self.debug.append(debug)
								print(debug)
								success1=len(dict_handle) -1
								if i ==success1:
									j=j+1
							else:
								# loop_error = True
								# debug = 'AP={0}  device={1} 反向通知你好 failed,write handle={4},value={5}, code={2},msg={3}'.format(
								# 	self.conf['hub'], dev, code, text, handle, handle_value)
								# print(debug)
								break
		if j == 0:
			loop_error = True
			err = 'ap={0}  接收通知 failed'.format(self.conf['hub'])
			self.err.append(err)
		else:
			self.case_end_flag = True
			debug = 'ap={0}  接收通知 success'.format(self.conf['hub'])
			self.debug.append(debug)
	def test_advertise_data(self):
		global loop_error
		if self.conf['model'].upper().startswith('S'):
			chip = 0
		else:
			random1 = random.randint(1, 10)
			if random1 % 2 == 1:
				chip = 1
			else:
				chip = 0
		interval=20
		adv_data='02010605094C696864'
		resp_data='5094C696864'
		code,msg=self.sdk.start_advertise(chip,interval,adv_data,resp_data)
		if code == 200:
			debug='AP={0} start_advertise success,code={1},message={2}'.format(self.conf['hub'],code,msg)
			self.debug.append(debug)
			print(debug)
			return code,chip
		else:
			loop_error=True
			err = 'AP={0} start_advertise failed,code={1},message={2}'.format(self.conf['hub'], code, msg)
			self.err.append(err)
			print(err)
			return code,chip
	def test_stop_advertise(self):
		# 这个接口将广播和停止广播一起测试了
		global loop_error
		code,chip=self.test_advertise_data()
		if code == 200:
			code1,msg=self.sdk.stop_advertise(chip)
			if code1 ==200:
				debug = 'AP={0} stop advertise success,code={1}'.format(self.conf['hub'], code1)
				self.debug.append(debug)
				print(debug)
			else:
				loop_error = True
				err = 'AP={0} stop advertise failed,code={1}'.format(self.conf['hub'], code1)
				self.err.append(err)
				print(err)
		else:
			loop_error = True
			err = 'AP={0} before stop advertise failed,code={1}'.format(self.conf['hub'], code)
			self.err.append(err)
			print(err)
def main():
	conf1 = read_stability_config()
	# ap_list = ['E1000','S2000','X1000']
	ap_list = ['S1000']
	thread = []
	for ap in ap_list:
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