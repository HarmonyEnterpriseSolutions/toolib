#-*- coding: Cp1251 -*-

__all__ = ['create_parser_int_with_unit']

import re
REC_VALUE = re.compile(u'''(\d+)([^\d]*)''')

def create_parser_int_with_unit(units):
	
	def _int_with_unit(value):
		m = REC_VALUE.search(value)
		if m:
			v, unit = m.groups()
			#print
			#print v, unit
			return int(v) * units.get(unit.strip().lower(), 1)
		else:
			return 0

	return _int_with_unit	


def test():
	values = [
		u'  100�',
		u'1100�  ',
		u'200�',
		u'20  ��',
	]

	parse = create_parser_int_with_unit({ u'�' : 1, u'��' : 1000, u'g' : 1, u'kg' : 1000 })

	for value in values:
		print value, parse(value)


if __name__ == '__main__':
	test()