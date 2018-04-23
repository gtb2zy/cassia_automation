import json,os,sys
import unittest,ddt,datetime,time
from contextlib import closing	
import sseclient,threading
path = os.getcwd().split('APItest')[0] + 'APItest/lib/'
sys.path.append(path)
from ExcelUtil import ExcelUtil
from tools import read_job_config,get_api

@ddt.ddt
class test_api(unittest.TestCase):

	conf = read_job_config()
	sdk = get_api()
	path = os.getcwd().split('APItest')[0]+'APItest/'
	testdata = ExcelUtil(path + 'test_data/' +conf['data_file'])
	dd = testdata.get_all()

	def setUp(self):
		self.timeout_timer = threading.Timer(10,self.time_out)
		self.timeout_timer.start()
		# print(dir(self))

	@ddt.data(*dd['scandata'])
	def test_scan(self,values):
		expect_result = values.pop('expect_result')
		values.pop('__name__')
		filter_duplicates = values['filter_duplicates']
		filter_name = values['filter_name']
		filter_mac = values['filter_mac']
		filter_rssi = values['filter_rssi']
		filter_uuid = values['filter_uuid']
		tmp = []
		flag = None
		with closing(self.sdk.scan(**values)) as r:
			for test_result in r:
				if test_result.startswith('data'):
					'''
					该部分主要测试过滤相关参数，也就是说
					进入到这个部分的测试用例全部是开启扫描成功的
					'''
					test_result = json.loads(test_result[5:])
					
					if filter_duplicates and filter_name:
						#过滤条件为filter_duplicates和filter_name，下面分支语句情况类似
						filters =test_result['bdaddrs'][0]['bdaddr']+test_result['adData']+test_result['name']
						if len(tmp)<30:
							if filters in tmp:
								flag = False
								print('\n',test_result,'\n',tmp)
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return
							else:
								tmp.append(filters)
								flag = True
								# print(flag)
						else:
							r.close()
							self.assertTrue(flag)
							tmp.clear()
							time.sleep(1)
							return				
					elif filter_duplicates and filter_rssi:
						filters =test_result['bdaddrs'][0]['bdaddr']+test_result['adData']
						if len(tmp)<20:
							if filters in tmp or int(test_result['rssi'])<int(filter_rssi):
								flag = False
								print('\n',test_result,'\n',tmp) 
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return
							else:
								tmp.append(filters)
								flag = True
								# print(flag)
						else:
							r.close()
							self.assertTrue(flag)
							tmp.clear()
							time.sleep(1)
							return	
					elif filter_duplicates:
						filters =test_result['bdaddrs'][0]['bdaddr']+test_result['adData']
						if len(tmp)<20:
							if filters in tmp:
								flag = False
								print('\n',test_result,'\n',tmp) 
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return
							else:
								tmp.append(filters)
								flag = True
								# print(flag)
						else:
							r.close()
							self.assertTrue(flag)
							tmp.clear()
							time.sleep(1)
							return							
					elif filter_name and filter_rssi:
						filters =test_result['name']
						if len(tmp)<20:
							if filters != filter_name or int(test_result['rssi'])<int(filter_rssi):
								flag = False
								print('\n',filters,filter_name,test_result['rssi'],filter_rssi,'\n') 
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return
							else:
								tmp.append(filters)
								flag = True
								# print(flag)
						else:
							r.close()
							self.assertTrue(flag)
							tmp.clear()
							time.sleep(1)
							return	
					elif filter_name and filter_uuid:
						expect = filter_name + str(filter_uuid)[2:] + str(filter_uuid)[:2]
						uuid = self.get_uuid(test_result['adData'])
						if uuid:
							filters = test_result['name'] + uuid
							if len(tmp)<20:
								if filters!= expect:
									flag = False
									print(filters,expect) 
									r.close()
									self.assertTrue(flag)
									tmp.clear()
									time.sleep(1)
									return
								else:
									tmp.append(filters)
									flag = True
									# print(flag)
							else:
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return	
						else:
							pass
					elif filter_uuid and filter_rssi:
						uuid = self.get_uuid(test_result['adData'])
						sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
						if uuid:
							filters = uuid
							if len(tmp)<20:
								if filters != sort_uuid or int(test_result['rssi'])<int(filter_rssi):
									flag = False
									print(filters!=sort_uuid,'\n',test_result['rssi']<filter_rssi) 
									r.close()
									self.assertTrue(flag)
									tmp.clear()
									time.sleep(1)
									return
								else:
									tmp.append(filters)
									flag = True
									# print(flag)
							else:
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return	
						else:
							if int(test_result['rssi'])<int(filter_rssi):
								flag = False
								print('\n',test_result['rssi'],filter_rssi,'\n') 
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return										
					elif filter_uuid:
						uuid = self.get_uuid(test_result['adData'])
						sort_uuid = str(filter_uuid)[2:] + str(filter_uuid)[:2]
						if uuid:
							filters = uuid
							if len(tmp)<20:
								if filters != sort_uuid:
									flag = False
									print('\n',filters,'≠',filter_uuid,'\n') 
									r.close()
									self.assertTrue(flag)
									tmp.clear()
									time.sleep(1)
									return
								else:
									tmp.append(filters)
									flag = True
									# print(flag)
							else:
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return	
						else:
							pass						
					elif filter_mac:
						filters =test_result['bdaddrs'][0]['bdaddr']
						if len(tmp)<20:
							if filters != filter_mac:
								flag = False
								print('\n',filters,'≠',filter_mac,'\n') 
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return
							else:
								tmp.append(filters)
								flag = True
								# print(flag)
						else:
							r.close()
							self.assertTrue(flag)
							tmp.clear()
							time.sleep(1)
							return							
					elif filter_rssi:
						filters =int(test_result['rssi'])
						if len(tmp)<20:
							if filters < int(filter_rssi):
								flag = False
								print('\n',filters,'≠',filter_rssi,'\n') 
								r.close()
								self.assertTrue(flag)
								tmp.clear() 
								time.sleep(1)
								return
							else:
								tmp.append(filters)
								flag = True
								# print(flag)
						else:
							r.close()
							self.assertTrue(flag)
							tmp.clear()
							time.sleep(1)
							return						
					elif filter_name:
						filters =test_result['name']
						if len(tmp)<20:
							if filters != filter_name:
								flag = False
								print('\n',filters,'≠',filter_name,'\n') 
								r.close()
								self.assertTrue(flag)
								tmp.clear()
								time.sleep(1)
								return
							else:
								tmp.append(filters)
								flag = True
								# print(flag)
						else:
							r.close()
							self.assertTrue(flag)
							tmp.clear()
							time.sleep(1)
							return
					else:
						#验证没有任何过滤的情况，就是简单的验证是否成功开启扫描
						r.close()
						self.assertTrue(True)
						time.sleep(1)
						return
				else:
					if test_result.startswith('keep-alive'):#过滤keep-live
						pass
					else:	#来到这里的全是开启扫描失败的情况		
						self.assertEqual(test_result,expect_result)
						return

	@ddt.data(*dd['connectdata'])
	def test_connect(self,values):
		expect_result = values['expect_result']
		device = values['device']
		chip = values['chip']
		try:
			chip = int(chip)
		except Exception as e:
			pass
		# print(chip,type(chip))
		types = values['types']
		timeout = values['timeout']
		self.sdk.disconnect_device(device)
		if chip:
			code,body,duration = self.sdk.connect_device(device,types,chip,timeout)
			if body =='chip is busy':
				time.sleep(3)
				code,body,duration = self.sdk.connect_device(device,types,chip,timeout)
		else:
			code,body,duration = self.sdk.connect_device(device,types,timeout = timeout)
			if body =='chip is busy':
				time.sleep(3)
				code,body,duration = self.sdk.connect_device(device,types,timeout = timeout)
		test_result = str(code)+','+body
		self.assertEqual(test_result,expect_result)
		if int(code) == 200:
			self.sdk.disconnect_device(device)

	@ddt.data(*dd['disconnectdata'])
	def test_disconnect(self,values):
		expect_result = values['expect_result']
		device = values['device']
		timeout = values['timeout']
		code,body = self.sdk.disconnect_device(device,timeout)
		self.assertEqual(body,expect_result)

	@ddt.data(*dd['getdevlist'])
	def test_get_dev_list(self,values):
		expect_result = values['expect_result']
		connect_state = values['connection_state']
		code,body = self.sdk.get_devices_list(connect_state)
		self.assertEqual(int(code),int(expect_result))

	@ddt.data(*dd['discover_service'])
	def test_discover_service(self,values):
		device = values['device']
		service_uuid = values['service_uuid']	
		expect_result = values['expect_result']
		self.sdk.connect_device(device)
		code,body = self.sdk.discovery_services(device,service_uuid)
		# print(code,type(code))
		self.assertEqual(body,expect_result)

	@ddt.data(*dd['discover_characs'])
	def test_discover_characs(self,values):
		device = values['device']
		server_uuid = values['service_uuid']	
		expect_result = values['expect_result']		
		code,body = self.sdk.discovery_characteristics(device,server_uuid)
		self.assertEqual(body,expect_result)

	@ddt.data(*dd["discover_charac"])
	def test_discover_charac(self,values):
		device = values['device']
		charac_uuid = values['charac_uuid']	
		expect_result = values['expect_result']		
		code,body = self.sdk.discovery_charateristic(device,charac_uuid)
		self.assertEqual(body,expect_result)

	@ddt.data(*dd['discover_des'])
	def test_discover_des(self,values):
		device = values['device']
		charac_uuid = values['charac_uuid']	
		expect_result = values['expect_result']		
		code,body = self.sdk.discover_descriptors(device,charac_uuid)
		self.assertEqual(body,expect_result)

	@ddt.data(*dd['discover_all'])
	def test_discover_all(self,values):
		device = values['device']
		expect_result = values['expect_result']	
		code,body = self.sdk.discover_all(device)
		self.assertEqual(body,expect_result)

	@ddt.data(*dd['write_by_handle'])
	def test_read_by_handle(self,values):
		device = values['device']
		handle = values['handle']
		expect_result = values['expect_result']	
		code,body = self.sdk.read_by_handle(device,handle)
		self.assertEqual(body,expect_result)		

	@ddt.data(*dd['read_by_handle'])
	def test_write_by_handle():
		device = values['device']
		handle = values['handle']
		handle_data = values['handle_data']
		expect_result = values['expect_result']
		code,body = self.sdk.write_by_handle(device,handle,handle_data)
		self.assertEqual(body,expect_result)

	# @ddt.data(*dd['get_connect_state'])
	# def test_get_device_connect_state(self,values):
	# 	self.message = None
	# 	device = values['device']
	# 	types = values['type']
	# 	expect_result = values['expect_result']
	# 	res = self.sdk.get_device_connect_state()
	# 	client = sseclient.SSEClient(res)
	# 	threading.Thread(target = self.recv_message,args = (client,)).start()
	# 	if expect_result =='connected':
	# 		self.sdk.disconnect_device(device)
	# 		time.sleep(2)
	# 		self.message = None
	# 		code,body,duration =self.sdk.connect_device(device,types,0,10000)
	# 		print(code,body)
	# 		while 1:
	# 			if self.message:
	# 				if self.message['handle']==device:
	# 					self.assertTrue(True)
	# 					self.sdk.disconnect_device(device)
	# 					self.message =None
	# 					break
	# 				else:
	# 					self.assertTrue(False)
	# 					self.sdk.disconnect_device(device)
	# 					self.message =None
	# 					break
	# 	else:
	# 		self.sdk.connect_device(device,types,0,10000)
	# 		time.sleep(2)
	# 		self.message = None
	# 		code,body = self.sdk.disconnect_device(device)
	# 		print(code,body)
	# 		while 1:
	# 			if self.message:
	# 				if self.message['handle']==device:
	# 					self.assertTrue(True)
	# 					self.sdk.disconnect_device(device)
	# 					self.message =None
	# 					break
	# 				else:
	# 					self.assertTrue(False)
	# 					self.sdk.disconnect_device(device)
	# 					self.message =None
	# 					break
	
	@ddt.data(*dd['recv_notification'])
	def test_recive_notification(self,values):
		device = values['device']
		expect_result = values['expect_result']
		res = self.sdk.recive_notification()
		client = sseclient.SSEClient(res)
		threading.Thread(target = self.recv_message,args = (client,)).start()
		while 1:
			if message:
				self.assertEqual(message,expect_result)
				break

	def get_uuid(self,data):
		start = 0
		head_length = int(data[start:start+2],16)	
		start = 2 + head_length*2
		data_length = int(data[start:start+2],16)
		start = start + 2 
		adv_data = data[start:start+data_length*2]
		adv_tpye = int(adv_data[0:2],16)
		if adv_tpye >=2 and adv_tpye <=7:
			start =start +2
			uuid = adv_data[2:]
			# print(uuid)
			return str(uuid)
		else:
			return None		


	def recv_message(self,sseclient):
		for event in sseclient.events():
			 self.message = json.loads(event.data)

	def time_out(self):
		try:
			# self.skipTest('Time out !')
			print('timeout')
			self.fail('Time out !')
		except:
			pass
	def tearDown(self):
		self.timeout_timer.cancel()


if __name__ == '__main__':

	unittest.main(verbosity=2)

