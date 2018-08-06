class abc:
	def __test(self):
		print('si you fang fa')

	def _test(self):
		self.__test()
		print('_si you fang fa')


abc = abc()
# abc.__test()
abc._test()