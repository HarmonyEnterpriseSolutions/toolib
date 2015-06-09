# - *- coding: Cp1251 -*-
"""
	hd = ' '.join(rsplit(str(h), 3))
	hs, hu = self._speller.spellNumber(h, UNITS['грн.'])
	ls, lu = self._speller.spellNumber(l, UNITS['коп.'])
	ld = "%02d" %(l,)
	return "%s (%s) %s %s %s" % (hd, hs.capitalize(), hu, ld, lu)
"""

from Unit import Unit
from toolib.util.lang import import_module_relative

class NumberSpeller(object):


	def __init__(self, locale):
		"""
		locale is like 'uk_UA', etc
		"""
		config = import_module_relative("config_%s" % locale, __name__)
		self.__dict__.update(config.__dict__)
		

	def _spell999(self, value, unit, forceUnit=False):

		n = value % 100
		if n >= 20:
			n = n % 10

		# jython filter of tuple returns list
		res = tuple(filter(None, (
			self.S900[value / 100 % 10],
			self.S90 [value / 10  % 10],
			self.S20 [unit.gender][n],
		)))

		if res or forceUnit:
			return res + (unit.getText(n),)
		else:
			return ()
			

	def spellNumber(self, value, unit):

		minus = value < 0
		if minus:
			value = abs(value)	

		if value == 0:
			number = self.ZERO
			res_unit = unit.getText(0)
		else:
			units = (unit,) + self.UNIT
			l = ()
			i = 0
			while value > 0 or i==0:
				try:
					curUnit = units[i]
				except IndexError:
					curUnit = Unit(Unit.MALE, "*10^%d" % (i*3,))

				l = self._spell999(
					value % 1000, 
					curUnit,
					forceUnit = (i == 0),
				) + l
				value /= 1000
				i+=1

			number = " ".join(l[:-1])
			res_unit = l[-1]

		#number = unicode(number)
		#number = number.decode('Cp1251')

		if minus:
			number = ' '.join((self.MINUS, number))

		return number, res_unit


	#def spellCurrency(self, value, hunit, lunit):
	#	"""
	#	pattern = "$h{%3d (%S) }[грн.] $l{%d }[коп.]"
	#
	#	"""
	#	value = int(round(value * 100))
	# 
	#	h = value / 100
	#	l = value % 100
	#	hs, hu = self.spellNumber(h, **hunit)
	#	#rint hs, hu
	#	ls, lu = self.spellNumber(l, **lunit)
	#	#rint ls, lu
	#	return ' '.join(rsplit(str(h), 3)), hs, hu, str(l), ls, lu



if __name__ == '__main__':
	import toolib.startup
	toolib.startup.startup()
	#for i in xrange(1):
	#	NumberSpeller().spellNumber(i, UNITS["гривня"])
	speller1 = NumberSpeller('uk_UA')
	speller2 = NumberSpeller('ru_RU')
	n = -12345678
	print ' '.join((speller1.spellNumber(n, Unit(Unit.FEMALE, u"гривня",  u"гривні",  u"гривень"))))
	print ' '.join((speller2.spellNumber(n, Unit(Unit.FEMALE, u"гривна",  u"гривни",  u"гривен"))))

	print ' '.join((speller1.spellNumber(n, Unit(Unit.NEUTER, u"місце",  u"місця",  u"місць"))))
	print ' '.join((speller2.spellNumber(n, Unit(Unit.NEUTER, u"место",  u"места",  u"мест"))))

