# - *- coding: Cp1251 -*-

class Unit(object):

	MALE = 0
	FEMALE = 1
	NEUTER = 2

	#        0, 1, 2, 3, 4,    5...
	INDEX = [2, 0, 1, 1, 1] + [2] * 15

	def __init__(self, gender, case1=None, case2=None, case3=None):
		self.gender = gender
		self._cases = case1, case2 or case1, case3 or case1

	def getText(self, value):
		return self._cases[self.INDEX[value]]
