import unittest,json,sys,os
from contextlib import closing
from threading import Timer
import 	threading
path = os.getcwd().split('APItest')[0] + 'APItest/lib/'
sys.path.append(path)
from api import api
from tools import get_cloud_api, get_model
from logs import set_logger

class testcase(unittest.TestCase):
	logger = set_logger(__name__)

	def setUp(self):
		pass
	def tearDown(self):
		pass